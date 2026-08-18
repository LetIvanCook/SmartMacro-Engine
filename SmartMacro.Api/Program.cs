using System.Text;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using SmartMacro.Api.Engines;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Models;
using SmartMacro.Api.Services;
using Microsoft.AspNetCore.RateLimiting;
using Serilog;

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog((context, services, configuration) => configuration
    .ReadFrom.Configuration(context.Configuration)
    .ReadFrom.Services(services)
    .Enrich.FromLogContext()
    .Enrich.WithMachineName()
    .Enrich.WithEnvironmentName()
    .Enrich.WithProperty("Application", "SmartMacroEngine")
    .WriteTo.Console(new Serilog.Formatting.Json.JsonFormatter())
    .WriteTo.File(
        path: "logs/smartmacro-.log",
        rollingInterval: RollingInterval.Day,
        retainedFileCountLimit: 14));

builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.ReferenceHandler = System.Text.Json.Serialization.ReferenceHandler.IgnoreCycles;
    });

// ── DbContext & AutoMapper ──────────────────────────────────────
builder.Services.AddDbContext<SmartMacroDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));
builder.Services.AddAutoMapper(AppDomain.CurrentDomain.GetAssemblies());

// ── Health Checks Configuration ────────────────────────────────
builder.Services.AddHealthChecks()
    .AddDbContextCheck<SmartMacroDbContext>(tags: new[] { "ready" });

// ── Authentication & JWT ────────────────────────────────────────
var jwtSettings = builder.Configuration.GetSection("Jwt");
builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuer = true,
        ValidateAudience = true,
        ValidateLifetime = true,
        ValidateIssuerSigningKey = true,
        ValidIssuer = jwtSettings["Issuer"],
        ValidAudience = jwtSettings["Audience"],
        IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtSettings["Key"]!))
    };
});

// ── Swagger Configuration ───────────────────────────────────────
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "SmartMacro API", Version = "v1" });

    // Cấu hình truyền JWT Token vào Header (Nút Authorize)
    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Description = "Nhập 'Bearer' [khoảng trắng] và chuỗi token của bạn vào ô bên dưới.\r\n\r\nVí dụ: \"Bearer eyJhbGci...\"",
        Name = "Authorization",
        In = ParameterLocation.Header,
        Type = SecuritySchemeType.ApiKey,
        Scheme = "Bearer"
    });

    c.AddSecurityRequirement(new OpenApiSecurityRequirement()
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                {
                    Type = ReferenceType.SecurityScheme,
                    Id = "Bearer"
                },
                Scheme = "oauth2",
                Name = "Bearer",
                In = ParameterLocation.Header,
            },
            new List<string>()
        }
    });
});

// ── Service Layer Registration ──────────────────────────────────
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddScoped<IAuthService, AuthService>();
builder.Services.AddScoped<IDashboardService, DashboardService>();
builder.Services.AddScoped<IMacroOptimizationEngine, MacroOptimizationEngine>();
builder.Services.AddScoped<IOptimizationService, OptimizationService>();
builder.Services.AddScoped<IFoodService, FoodService>();
builder.Services.AddScoped<IFoodCategoryService, FoodCategoryService>();
builder.Services.AddScoped<IInventoryService, InventoryService>();
builder.Services.AddScoped<IDailyTargetService, DailyTargetService>();

// ── Exception Handling ──────────────────────────────────────────
builder.Services.AddExceptionHandler<SmartMacro.Api.Middleware.GlobalExceptionHandler>();
builder.Services.AddProblemDetails();

// ── Rate Limiting ───────────────────────────────────────────────
builder.Services.AddRateLimiter(options =>
{
    options.AddFixedWindowLimiter("AuthPolicy", opt =>
    {
        opt.PermitLimit = 5;
        opt.Window = TimeSpan.FromMinutes(1);
        opt.QueueLimit = 0;
    });
    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;
});

// ── CORS Configuration ──────────────────────────────────────────
builder.Services.AddCors(options =>
{
    options.AddPolicy("ProductionCors", policy =>
    {
        var allowedOrigins = builder.Configuration
            .GetSection("Cors:AllowedOrigins")
            .Get<string[]>() ?? [];

        policy.WithOrigins(allowedOrigins)
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

app.UseExceptionHandler(); // Phải nằm trên cùng của request pipeline
app.UseSerilogRequestLogging(options =>
{
    options.MessageTemplate =
        "HTTP {RequestMethod} {RequestPath} responded {StatusCode} in {Elapsed:0.0000} ms";
    options.EnrichDiagnosticContext = (diagnosticContext, httpContext) =>
    {
        diagnosticContext.Set("CorrelationId", httpContext.TraceIdentifier);
    };
});

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseCors("ProductionCors");

app.UseRateLimiter();

app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();
app.MapHealthChecks("/health", new Microsoft.AspNetCore.Diagnostics.HealthChecks.HealthCheckOptions
{
    Predicate = _ => false
});
app.MapHealthChecks("/health/ready", new Microsoft.AspNetCore.Diagnostics.HealthChecks.HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});

// ── Auto-apply EF Core Migrations on Startup ────────────────────
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<SmartMacroDbContext>();
    if (db.Database.IsSqlServer())
    {
        try
        {
            db.Database.Migrate();
        }
        catch (Exception ex)
        {
            var logger = scope.ServiceProvider.GetRequiredService<ILogger<Program>>();
            logger.LogError(ex, "Không thể tự động Migrate Database. Hãy đảm bảo SQL Server đang chạy và ConnectionString hợp lệ.");
        }
    }
}

try
{
    Log.Information("Starting SmartMacro API host...");
    app.Run();
}
catch (Exception ex)
{
    Log.Fatal(ex, "Host terminated unexpectedly");
}
finally
{
    Log.CloseAndFlush();
}

public partial class Program { }
