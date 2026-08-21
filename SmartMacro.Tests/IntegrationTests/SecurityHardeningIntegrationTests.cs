using System.Net;
using System.Net.Http.Json;
using FluentAssertions;
using SmartMacro.Api.DTOs;

namespace SmartMacro.Tests.IntegrationTests;

public class SecurityHardeningIntegrationTests
{
    [Fact]
    public async Task Login_RateLimiting_RejectsSixthRequestWith429()
    {
        // Arrange - use isolated factory instance for clean rate limiter state
        using var factory = new CustomWebApplicationFactory();
        var client = factory.CreateClient();

        var loginRequest = new LoginRequestDto
        {
            Email = "ratelimit_login@example.com",
            Password = "WrongPassword!"
        };

        // Act & Assert - First 5 requests should reach the endpoint (returns 400 Bad Request because user doesn't exist)
        for (int i = 1; i <= 5; i++)
        {
            var response = await client.PostAsJsonAsync("/api/auth/login", loginRequest);
            response.StatusCode.Should().Be(HttpStatusCode.BadRequest, $"Request #{i} should not be rate limited");
        }

        // 6th request within the 1-minute window should be rejected with 429 Too Many Requests
        var sixthResponse = await client.PostAsJsonAsync("/api/auth/login", loginRequest);
        sixthResponse.StatusCode.Should().Be(HttpStatusCode.TooManyRequests, "Request #6 must be rate limited");
    }

    [Fact]
    public async Task Refresh_RateLimiting_RejectsSixthRequestWith429()
    {
        // Arrange - use isolated factory instance for clean rate limiter state
        using var factory = new CustomWebApplicationFactory();
        var client = factory.CreateClient();

        var refreshRequest = new RefreshTokenRequestDto
        {
            RefreshToken = "dummy-refresh-token"
        };

        // Act & Assert - First 5 requests should reach the endpoint (returns 404 Not Found)
        for (int i = 1; i <= 5; i++)
        {
            var response = await client.PostAsJsonAsync("/api/auth/refresh", refreshRequest);
            response.StatusCode.Should().Be(HttpStatusCode.NotFound, $"Request #{i} should not be rate limited");
        }

        // 6th request within the 1-minute window should be rejected with 429 Too Many Requests
        var sixthResponse = await client.PostAsJsonAsync("/api/auth/refresh", refreshRequest);
        sixthResponse.StatusCode.Should().Be(HttpStatusCode.TooManyRequests, "Request #6 must be rate limited");
    }

    [Fact]
    public async Task NonSensitiveEndpoint_NotRateLimited_AllowsMoreThanFiveRequests()
    {
        // Arrange
        using var factory = new CustomWebApplicationFactory();
        var client = factory.CreateClient();

        // Act & Assert - Send 7 requests to non-rate-limited endpoint (/health)
        for (int i = 1; i <= 7; i++)
        {
            var response = await client.GetAsync("/health");
            response.StatusCode.Should().Be(HttpStatusCode.OK, $"Request #{i} to /health should succeed and not be rate limited");
        }
    }

    [Fact]
    public async Task Cors_AllowedOrigin_ReturnsAllowOriginHeader()
    {
        // Arrange
        using var factory = new CustomWebApplicationFactory();
        var client = factory.CreateClient();

        var request = new HttpRequestMessage(HttpMethod.Get, "/health");
        request.Headers.Add("Origin", "http://localhost:3000");

        // Act
        var response = await client.SendAsync(request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        response.Headers.Contains("Access-Control-Allow-Origin").Should().BeTrue();
        response.Headers.GetValues("Access-Control-Allow-Origin").Should().Contain("http://localhost:3000");
    }

    [Fact]
    public async Task Cors_ProductionAllowedOrigin_ReturnsAllowOriginHeader()
    {
        // Arrange
        using var factory = new CustomWebApplicationFactory();
        var client = factory.CreateClient();

        var request = new HttpRequestMessage(HttpMethod.Get, "/health");
        request.Headers.Add("Origin", "https://app.smartmacro.example.com");

        // Act
        var response = await client.SendAsync(request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        response.Headers.Contains("Access-Control-Allow-Origin").Should().BeTrue();
        response.Headers.GetValues("Access-Control-Allow-Origin").Should().Contain("https://app.smartmacro.example.com");
    }

    [Fact]
    public async Task Cors_DisallowedOrigin_DoesNotReturnAllowOriginHeader()
    {
        // Arrange
        using var factory = new CustomWebApplicationFactory();
        var client = factory.CreateClient();

        var request = new HttpRequestMessage(HttpMethod.Get, "/health");
        request.Headers.Add("Origin", "https://evil.example.com");

        // Act
        var response = await client.SendAsync(request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        response.Headers.Contains("Access-Control-Allow-Origin").Should().BeFalse(
            "CORS policy should not provide Access-Control-Allow-Origin header to unauthorized origins");
    }

    [Fact]
    public async Task Cors_PreflightRequest_AllowedOrigin_ReturnsCorsHeaders()
    {
        // Arrange
        using var factory = new CustomWebApplicationFactory();
        var client = factory.CreateClient();

        var request = new HttpRequestMessage(HttpMethod.Options, "/api/auth/login");
        request.Headers.Add("Origin", "http://localhost:3000");
        request.Headers.Add("Access-Control-Request-Method", "POST");
        request.Headers.Add("Access-Control-Request-Headers", "content-type");

        // Act
        var response = await client.SendAsync(request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NoContent);
        response.Headers.Contains("Access-Control-Allow-Origin").Should().BeTrue();
        response.Headers.GetValues("Access-Control-Allow-Origin").Should().Contain("http://localhost:3000");
        response.Headers.Contains("Access-Control-Allow-Methods").Should().BeTrue();
    }

    [Fact]
    public async Task Cors_PreflightRequest_DisallowedOrigin_DoesNotReturnAllowOriginHeader()
    {
        // Arrange
        using var factory = new CustomWebApplicationFactory();
        var client = factory.CreateClient();

        var request = new HttpRequestMessage(HttpMethod.Options, "/api/auth/login");
        request.Headers.Add("Origin", "https://evil.example.com");
        request.Headers.Add("Access-Control-Request-Method", "POST");
        request.Headers.Add("Access-Control-Request-Headers", "content-type");

        // Act
        var response = await client.SendAsync(request);

        // Assert
        response.Headers.Contains("Access-Control-Allow-Origin").Should().BeFalse(
            "Preflight request from disallowed origin should not receive Access-Control-Allow-Origin header");
    }
}
