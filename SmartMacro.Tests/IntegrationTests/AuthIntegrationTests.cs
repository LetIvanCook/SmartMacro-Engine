using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using FluentAssertions;
using SmartMacro.Api.DTOs;

namespace SmartMacro.Tests.IntegrationTests;

public class AuthIntegrationTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly HttpClient _client;

    public AuthIntegrationTests(CustomWebApplicationFactory factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task Register_ValidData_ReturnsOkAndCreatesUser()
    {
        // Arrange
        var request = new RegisterRequestDto
        {
            Email = $"test{Guid.NewGuid()}@example.com",
            Password = "Password123!",
            FullName = "Test User",
            DateOfBirth = new DateOnly(1990, 1, 1),
            BiologicalSex = "male",
            ActivityLevel = "active",
            GoalType = "cutting"
        };

        // Act
        var response = await _client.PostAsJsonAsync("/api/auth/register", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        var responseData = await response.Content.ReadFromJsonAsync<AuthResponseDto>();
        responseData.Should().NotBeNull();
        responseData!.AccessToken.Should().NotBeNullOrEmpty();
        responseData.Email.Should().Be(request.Email);
    }

    [Fact]
    public async Task Register_ExistingEmail_ReturnsConflict()
    {
        // Arrange
        var email = $"test{Guid.NewGuid()}@example.com";
        var request = new RegisterRequestDto
        {
            Email = email,
            Password = "Password123!",
            FullName = "Test User",
            DateOfBirth = new DateOnly(1990, 1, 1),
            BiologicalSex = "male",
            ActivityLevel = "active",
            GoalType = "cutting"
        };
        await _client.PostAsJsonAsync("/api/auth/register", request);

        // Act
        var response = await _client.PostAsJsonAsync("/api/auth/register", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Conflict);
    }

    [Fact]
    public async Task Login_ValidCredentials_ReturnsOkAndAccessToken()
    {
        // Arrange
        var request = new RegisterRequestDto
        {
            Email = $"test{Guid.NewGuid()}@example.com",
            Password = "Password123!",
            FullName = "Test User",
            DateOfBirth = new DateOnly(1990, 1, 1),
            BiologicalSex = "male",
            ActivityLevel = "active",
            GoalType = "cutting"
        };
        await _client.PostAsJsonAsync("/api/auth/register", request);

        var loginRequest = new LoginRequestDto
        {
            Email = request.Email,
            Password = request.Password
        };

        // Act
        var response = await _client.PostAsJsonAsync("/api/auth/login", loginRequest);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        var responseData = await response.Content.ReadFromJsonAsync<AuthResponseDto>();
        responseData.Should().NotBeNull();
        responseData!.AccessToken.Should().NotBeNullOrEmpty();
    }

    [Fact]
    public async Task Login_InvalidPassword_ReturnsBadRequest()
    {
        // Arrange
        var email = $"test{Guid.NewGuid()}@example.com";
        var request = new RegisterRequestDto
        {
            Email = email,
            Password = "Password123!",
            FullName = "Test User",
            DateOfBirth = new DateOnly(1990, 1, 1),
            BiologicalSex = "male",
            ActivityLevel = "active",
            GoalType = "cutting"
        };
        await _client.PostAsJsonAsync("/api/auth/register", request);

        var loginRequest = new LoginRequestDto
        {
            Email = email,
            Password = "WrongPassword!"
        };

        // Act
        var response = await _client.PostAsJsonAsync("/api/auth/login", loginRequest);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.BadRequest);
    }

    [Fact]
    public async Task ProtectedEndpoint_WithoutAccessToken_ReturnsUnauthorized()
    {
        // Act
        var response = await _client.GetAsync("/api/food-categories");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Unauthorized);
    }

    [Fact]
    public async Task ProtectedEndpoint_WithValidAccessToken_ReturnsOk()
    {
        // Arrange
        var email = $"test{Guid.NewGuid()}@example.com";
        var registerRequest = new RegisterRequestDto
        {
            Email = email,
            Password = "Password123!",
            FullName = "Test User",
            DateOfBirth = new DateOnly(1990, 1, 1),
            BiologicalSex = "male",
            ActivityLevel = "active",
            GoalType = "cutting"
        };
        var authResponse = await _client.PostAsJsonAsync("/api/auth/register", registerRequest);
        var authData = await authResponse.Content.ReadFromJsonAsync<AuthResponseDto>();
        
        var request = new HttpRequestMessage(HttpMethod.Get, "/api/food-categories");
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", authData!.AccessToken);

        // Act
        var response = await _client.SendAsync(request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
    }

    [Fact]
    public async Task Refresh_ValidToken_ReturnsNewTokens()
    {
        // Arrange
        var request = new RegisterRequestDto
        {
            Email = $"test{Guid.NewGuid()}@example.com",
            Password = "Password123!",
            FullName = "Test User",
            DateOfBirth = new DateOnly(1990, 1, 1),
            BiologicalSex = "male",
            ActivityLevel = "active",
            GoalType = "cutting"
        };
        var response = await _client.PostAsJsonAsync("/api/auth/register", request);
        var authData = await response.Content.ReadFromJsonAsync<AuthResponseDto>();

        var refreshRequest = new RefreshTokenRequestDto
        {
            RefreshToken = authData!.RefreshToken
        };

        // Act
        var refreshResponse = await _client.PostAsJsonAsync("/api/auth/refresh", refreshRequest);

        // Assert
        refreshResponse.StatusCode.Should().Be(HttpStatusCode.OK);
        var refreshData = await refreshResponse.Content.ReadFromJsonAsync<AuthResponseDto>();
        refreshData.Should().NotBeNull();
        refreshData!.AccessToken.Should().NotBeNullOrEmpty();
        refreshData.RefreshToken.Should().NotBeNullOrEmpty();
        refreshData.AccessToken.Should().NotBe(authData.AccessToken);
        refreshData.RefreshToken.Should().NotBe(authData.RefreshToken);
    }

    [Fact]
    public async Task Refresh_InvalidToken_ReturnsNotFound()
    {
        // Arrange
        var refreshRequest = new RefreshTokenRequestDto
        {
            RefreshToken = "invalid-token"
        };

        // Act
        var response = await _client.PostAsJsonAsync("/api/auth/refresh", refreshRequest);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task Logout_ValidToken_RevokesToken()
    {
        // Arrange
        var request = new RegisterRequestDto
        {
            Email = $"test{Guid.NewGuid()}@example.com",
            Password = "Password123!",
            FullName = "Test User",
            DateOfBirth = new DateOnly(1990, 1, 1),
            BiologicalSex = "male",
            ActivityLevel = "active",
            GoalType = "cutting"
        };
        var response = await _client.PostAsJsonAsync("/api/auth/register", request);
        var authData = await response.Content.ReadFromJsonAsync<AuthResponseDto>();

        var logoutRequest = new RefreshTokenRequestDto
        {
            RefreshToken = authData!.RefreshToken
        };

        var requestMessage = new HttpRequestMessage(HttpMethod.Post, "/api/auth/logout")
        {
            Content = JsonContent.Create(logoutRequest)
        };
        requestMessage.Headers.Authorization = new AuthenticationHeaderValue("Bearer", authData.AccessToken);

        // Act
        var logoutResponse = await _client.SendAsync(requestMessage);

        // Assert
        logoutResponse.StatusCode.Should().Be(HttpStatusCode.OK);

        // Act 2: Thử refresh lại token đã bị revoke
        var refreshResponse = await _client.PostAsJsonAsync("/api/auth/refresh", logoutRequest);

        // Assert 2
        refreshResponse.StatusCode.Should().Be(HttpStatusCode.Unauthorized);
    }
}
