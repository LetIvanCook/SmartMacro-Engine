using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Models;
using Microsoft.EntityFrameworkCore;
using System.Security.Cryptography;

namespace SmartMacro.Api.Services;

public class AuthService : IAuthService
{
    private readonly IUserService _userService;
    private readonly IConfiguration _configuration;
    private readonly SmartMacroDbContext _dbContext;

    public AuthService(IUserService userService, IConfiguration configuration, SmartMacroDbContext dbContext)
    {
        _userService = userService;
        _configuration = configuration;
        _dbContext = dbContext;
    }

    public async Task<AuthResponseDto> RegisterAsync(RegisterRequestDto request)
    {
        // 1. Kiểm tra email tồn tại
        var existingUser = await _userService.GetUserByEmailAsync(request.Email);
        if (existingUser != null)
        {
            throw new ConflictException("Email đã được sử dụng.");
        }

        // 2. Hash password
        var passwordHash = BCrypt.Net.BCrypt.HashPassword(request.Password);

        // 3. Tạo User entity
        var user = new User
        {
            Email = request.Email,
            PasswordHash = passwordHash,
            FullName = request.FullName,
            DateOfBirth = request.DateOfBirth,
            BiologicalSex = request.BiologicalSex,
            ActivityLevel = request.ActivityLevel,
            GoalType = request.GoalType,
            Status = "active",
            CreatedAt = DateTime.UtcNow,
            UpdatedAt = DateTime.UtcNow
        };

        // 4. Lưu xuống DB
        var createdUser = await _userService.CreateUserAsync(user);

        // 5. Generate tokens
        var (accessToken, expiresAt) = GenerateJwtToken(createdUser);
        var refreshToken = GenerateRefreshToken();

        // 6. Lưu RefreshToken vào DB
        var refreshTokenEntity = new RefreshToken
        {
            TokenHash = HashToken(refreshToken),
            UserId = createdUser.UserId,
            CreatedAt = DateTime.UtcNow,
            ExpiresAt = DateTime.UtcNow.AddDays(Convert.ToDouble(_configuration["Jwt:RefreshTokenExpireDays"] ?? "7"))
        };
        _dbContext.RefreshTokens.Add(refreshTokenEntity);
        await _dbContext.SaveChangesAsync();

        return new AuthResponseDto
        {
            AccessToken = accessToken,
            RefreshToken = refreshToken,
            AccessTokenExpiry = expiresAt,
            UserId = createdUser.UserId,
            Email = createdUser.Email,
            FullName = createdUser.FullName
        };
    }

    public async Task<AuthResponseDto> LoginAsync(LoginRequestDto request)
    {
        // 1. Tìm user theo email
        var user = await _userService.GetUserByEmailAsync(request.Email);
        if (user == null)
        {
            throw new ArgumentException("Email hoặc mật khẩu không đúng.");
        }

        // 2. Verify password
        var isPasswordValid = BCrypt.Net.BCrypt.Verify(request.Password, user.PasswordHash);
        if (!isPasswordValid)
        {
            throw new ArgumentException("Email hoặc mật khẩu không đúng.");
        }

        // 3. Generate tokens
        var (accessToken, expiresAt) = GenerateJwtToken(user);
        var refreshToken = GenerateRefreshToken();

        // 4. Lưu RefreshToken vào DB
        var refreshTokenEntity = new RefreshToken
        {
            TokenHash = HashToken(refreshToken),
            UserId = user.UserId,
            CreatedAt = DateTime.UtcNow,
            ExpiresAt = DateTime.UtcNow.AddDays(Convert.ToDouble(_configuration["Jwt:RefreshTokenExpireDays"] ?? "7"))
        };
        _dbContext.RefreshTokens.Add(refreshTokenEntity);
        await _dbContext.SaveChangesAsync();

        return new AuthResponseDto
        {
            AccessToken = accessToken,
            RefreshToken = refreshToken,
            AccessTokenExpiry = expiresAt,
            UserId = user.UserId,
            Email = user.Email,
            FullName = user.FullName
        };
    }

    private (string token, DateTime expiresAt) GenerateJwtToken(User user)
    {
        var jwtSettings = _configuration.GetSection("Jwt");
        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtSettings["Key"]!));
        var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, user.UserId.ToString()),
            new Claim(JwtRegisteredClaimNames.Email, user.Email),
            new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
        };

        var expireMinutes = Convert.ToDouble(jwtSettings["ExpireMinutes"] ?? "15");
        var expiresAt = DateTime.UtcNow.AddMinutes(expireMinutes);

        var token = new JwtSecurityToken(
            issuer: jwtSettings["Issuer"],
            audience: jwtSettings["Audience"],
            claims: claims,
            expires: expiresAt,
            signingCredentials: creds
        );

        return (new JwtSecurityTokenHandler().WriteToken(token), expiresAt);
    }

    private string GenerateRefreshToken()
    {
        var randomNumber = new byte[64];
        using var rng = RandomNumberGenerator.Create();
        rng.GetBytes(randomNumber);
        return Convert.ToBase64String(randomNumber);
    }

    public async Task<AuthResponseDto> RefreshTokenAsync(string refreshToken)
    {
        var tokenHash = HashToken(refreshToken);
        var tokenEntity = await _dbContext.RefreshTokens
            .Include(rt => rt.User)
            .FirstOrDefaultAsync(rt => rt.TokenHash == tokenHash);

        if (tokenEntity == null)
        {
            throw new NotFoundException("Refresh token không tồn tại.");
        }

        if (!tokenEntity.IsActive)
        {
            throw new UnauthorizedException("Refresh token đã hết hạn hoặc bị thu hồi.");
        }

        // Token rotation: revoke old token
        tokenEntity.RevokedAt = DateTime.UtcNow;

        // Generate new tokens
        var (newAccessToken, expiresAt) = GenerateJwtToken(tokenEntity.User);
        var newRefreshToken = GenerateRefreshToken();

        var newRefreshTokenEntity = new RefreshToken
        {
            TokenHash = HashToken(newRefreshToken),
            UserId = tokenEntity.UserId,
            CreatedAt = DateTime.UtcNow,
            ExpiresAt = DateTime.UtcNow.AddDays(Convert.ToDouble(_configuration["Jwt:RefreshTokenExpireDays"] ?? "7"))
        };

        _dbContext.RefreshTokens.Add(newRefreshTokenEntity);
        await _dbContext.SaveChangesAsync();

        return new AuthResponseDto
        {
            AccessToken = newAccessToken,
            RefreshToken = newRefreshToken,
            AccessTokenExpiry = expiresAt,
            UserId = tokenEntity.User.UserId,
            Email = tokenEntity.User.Email,
            FullName = tokenEntity.User.FullName
        };
    }

    public async Task RevokeTokenAsync(string refreshToken, long userId)
    {
        var tokenHash = HashToken(refreshToken);
        var tokenEntity = await _dbContext.RefreshTokens
            .FirstOrDefaultAsync(rt => rt.TokenHash == tokenHash && rt.UserId == userId);

        if (tokenEntity == null || !tokenEntity.IsActive)
        {
            throw new NotFoundException("Refresh token không tồn tại hoặc không còn hiệu lực.");
        }

        tokenEntity.RevokedAt = DateTime.UtcNow;
        await _dbContext.SaveChangesAsync();
    }

    private static string HashToken(string token)
    {
        var bytes = SHA256.HashData(Encoding.UTF8.GetBytes(token));
        return Convert.ToHexString(bytes).ToLowerInvariant();
    }
}
