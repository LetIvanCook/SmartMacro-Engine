using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Models;

namespace SmartMacro.Api.Services;

public class AuthService : IAuthService
{
    private readonly IUserService _userService;
    private readonly IConfiguration _configuration;

    public AuthService(IUserService userService, IConfiguration configuration)
    {
        _userService = userService;
        _configuration = configuration;
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

        // 5. Generate token & response
        var token = GenerateJwtToken(createdUser);

        return new AuthResponseDto
        {
            Token = token,
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

        // 3. Generate token & response
        var token = GenerateJwtToken(user);

        return new AuthResponseDto
        {
            Token = token,
            UserId = user.UserId,
            Email = user.Email,
            FullName = user.FullName
        };
    }

    private string GenerateJwtToken(User user)
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

        var token = new JwtSecurityToken(
            issuer: jwtSettings["Issuer"],
            audience: jwtSettings["Audience"],
            claims: claims,
            expires: DateTime.UtcNow.AddDays(Convert.ToDouble(jwtSettings["ExpireDays"])),
            signingCredentials: creds
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
