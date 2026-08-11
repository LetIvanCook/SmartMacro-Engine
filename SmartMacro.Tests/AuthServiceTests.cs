using System.IdentityModel.Tokens.Jwt;
using FluentAssertions;
using Microsoft.Extensions.Configuration;
using Moq;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Models;
using SmartMacro.Api.Services;
using SmartMacro.Api.Exceptions;
using Microsoft.EntityFrameworkCore;

namespace SmartMacro.Tests;

/// <summary>
/// Unit tests cho AuthService.
/// Sử dụng Moq để giả lập IUserService và IConfiguration.
/// </summary>
public class AuthServiceTests
{
    private readonly Mock<IUserService> _userServiceMock;
    private readonly IConfiguration _configuration;
    private readonly SmartMacroDbContext _dbContext;
    private readonly AuthService _sut;

    public AuthServiceTests()
    {
        _userServiceMock = new Mock<IUserService>();

        // Setup in-memory configuration for JWT settings
        var inMemorySettings = new Dictionary<string, string?>
        {
            {"Jwt:Key", "SmartMacroSuperSecretKeyForJwtTokens123!@#"},
            {"Jwt:Issuer", "SmartMacroApiTest"},
            {"Jwt:Audience", "SmartMacroClientTest"},
            {"Jwt:ExpireDays", "1"}
        };
        _configuration = new ConfigurationBuilder()
            .AddInMemoryCollection(inMemorySettings)
            .Build();

        var dbOptions = new DbContextOptionsBuilder<SmartMacroDbContext>()
            .UseInMemoryDatabase(databaseName: "SmartMacroTestDb_" + Guid.NewGuid().ToString())
            .Options;
        _dbContext = new SmartMacroDbContext(dbOptions);

        _sut = new AuthService(_userServiceMock.Object, _configuration, _dbContext);
    }

    [Fact]
    public async Task Register_ValidData_CreatesUserSuccessfully()
    {
        // Arrange
        var request = new RegisterRequestDto
        {
            Email = "test@example.com",
            Password = "StrongPassword123!",
            FullName = "Test User",
            DateOfBirth = new DateOnly(1990, 1, 1),
            BiologicalSex = "male",
            ActivityLevel = "moderate",
            GoalType = "maintenance"
        };

        // Giả lập email chưa tồn tại (trả về null)
        _userServiceMock.Setup(x => x.GetUserByEmailAsync(request.Email))
            .ReturnsAsync((User?)null);

        // Giả lập hàm CreateUserAsync trả về đối tượng User sau khi lưu (có UserId)
        _userServiceMock.Setup(x => x.CreateUserAsync(It.IsAny<User>()))
            .ReturnsAsync((User u) => 
            {
                u.UserId = 1;
                return u;
            });

        // Act
        var response = await _sut.RegisterAsync(request);

        // Assert
        response.Should().NotBeNull();
        response.UserId.Should().Be(1);
        response.Email.Should().Be(request.Email);
        response.FullName.Should().Be(request.FullName);
        response.AccessToken.Should().NotBeNullOrEmpty("vì JWT token phải được sinh ra sau khi đăng ký thành công");
        response.RefreshToken.Should().NotBeNullOrEmpty("vì Refresh token phải được sinh ra");

        // Xác minh rằng hàm CreateUserAsync đã được gọi 1 lần
        _userServiceMock.Verify(x => x.CreateUserAsync(It.Is<User>(u => 
            u.Email == request.Email && 
            u.FullName == request.FullName &&
            !string.IsNullOrEmpty(u.PasswordHash) // Password đã được hash
        )), Times.Once);
    }

    [Fact]
    public async Task Login_ValidCredentials_ReturnsJwtToken()
    {
        // Arrange
        var request = new LoginRequestDto
        {
            Email = "test@example.com",
            Password = "StrongPassword123!"
        };

        // Giả lập User đã được lưu trong DB với password hash hợp lệ
        var passwordHash = BCrypt.Net.BCrypt.HashPassword(request.Password);
        var existingUser = new User
        {
            UserId = 1,
            Email = request.Email,
            FullName = "Test User",
            PasswordHash = passwordHash,
            Status = "active"
        };

        _userServiceMock.Setup(x => x.GetUserByEmailAsync(request.Email))
            .ReturnsAsync(existingUser);

        // Act
        var response = await _sut.LoginAsync(request);

        // Assert
        response.Should().NotBeNull();
        response.UserId.Should().Be(existingUser.UserId);
        response.Email.Should().Be(existingUser.Email);
        response.AccessToken.Should().NotBeNullOrEmpty("vì đăng nhập thành công phải sinh ra token hợp lệ");
        response.RefreshToken.Should().NotBeNullOrEmpty("vì Refresh token phải được sinh ra");

        // Parse token để kiểm tra sơ bộ
        var handler = new JwtSecurityTokenHandler();
        var jwtToken = handler.ReadJwtToken(response.AccessToken);
        jwtToken.Issuer.Should().Be("SmartMacroApiTest");
        jwtToken.Audiences.Should().Contain("SmartMacroClientTest");
    }

    [Fact]
    public async Task Register_EmailAlreadyExists_ThrowsException()
    {
        // Arrange
        var request = new RegisterRequestDto
        {
            Email = "exist@example.com",
            Password = "password123"
        };

        _userServiceMock.Setup(x => x.GetUserByEmailAsync(request.Email))
            .ReturnsAsync(new User { Email = request.Email }); // Giả lập user đã tồn tại

        // Act & Assert
        var exception = await Assert.ThrowsAsync<ConflictException>(() => _sut.RegisterAsync(request));
        exception.Message.Should().Be("Email đã được sử dụng.");
    }

    [Fact]
    public async Task Login_InvalidPassword_ThrowsException()
    {
        // Arrange
        var request = new LoginRequestDto
        {
            Email = "test@example.com",
            Password = "WrongPassword!"
        };

        var correctHash = BCrypt.Net.BCrypt.HashPassword("CorrectPassword!");
        var existingUser = new User
        {
            UserId = 1,
            Email = request.Email,
            PasswordHash = correctHash
        };

        _userServiceMock.Setup(x => x.GetUserByEmailAsync(request.Email))
            .ReturnsAsync(existingUser);

        // Act & Assert
        var exception = await Assert.ThrowsAsync<ArgumentException>(() => _sut.LoginAsync(request));
        exception.Message.Should().Be("Email hoặc mật khẩu không đúng.");
    }
}
