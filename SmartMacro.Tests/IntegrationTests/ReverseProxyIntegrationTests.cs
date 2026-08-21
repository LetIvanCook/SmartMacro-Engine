using System.Net;
using FluentAssertions;

namespace SmartMacro.Tests.IntegrationTests;

public class ReverseProxyIntegrationTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly HttpClient _client;

    public ReverseProxyIntegrationTests(CustomWebApplicationFactory factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task RequestWithForwardedHeaders_IsProcessedSuccessfullyWithoutRedirectLoop()
    {
        // Arrange
        using var request = new HttpRequestMessage(HttpMethod.Get, "/health");
        request.Headers.Add("X-Forwarded-Proto", "https");
        request.Headers.Add("X-Forwarded-For", "203.0.113.195");
        request.Headers.Add("X-Forwarded-Host", "app.smartmacro.example.com");

        // Act
        var response = await _client.SendAsync(request);

        // Assert: /health endpoint must respond 200 OK directly, not 307/308 redirect
        response.StatusCode.Should().Be(HttpStatusCode.OK);
    }

    [Fact]
    public async Task HealthEndpoint_DirectHttp_RespondsHealthy()
    {
        // Act
        var response = await _client.GetAsync("/health");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
    }
}
