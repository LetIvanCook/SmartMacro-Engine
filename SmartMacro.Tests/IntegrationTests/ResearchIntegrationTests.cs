using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using FluentAssertions;
using Microsoft.AspNetCore.TestHost;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Options;
using Moq;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Options;

namespace SmartMacro.Tests.IntegrationTests;

public class ResearchIntegrationTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly CustomWebApplicationFactory _factory;

    public ResearchIntegrationTests(CustomWebApplicationFactory factory)
    {
        _factory = factory;
    }

    private async Task<string> GetUserTokenAsync(HttpClient client)
    {
        var registerDto = new RegisterRequestDto
        {
            Email = $"research_test_{Guid.NewGuid()}@example.com",
            Password = "StrongPassword123!",
            FullName = "Research Integration User",
            BiologicalSex = "male",
            ActivityLevel = "moderate",
            GoalType = "cutting",
            DateOfBirth = new DateOnly(1995, 5, 20)
        };

        var registerRes = await client.PostAsJsonAsync("/api/auth/register", registerDto);
        registerRes.EnsureSuccessStatusCode();

        var authResponse = await registerRes.Content.ReadFromJsonAsync<AuthResponseDto>();
        return authResponse!.AccessToken;
    }

    [Fact]
    public async Task Analyze_WithoutToken_ReturnsUnauthorized401()
    {
        // Arrange
        var client = _factory.CreateClient();
        var request = new CompetitorAnalysisRequest
        {
            TargetUrl = "https://cronometer.com/",
            FocusTopic = "Macro tracking"
        };

        // Act
        var response = await client.PostAsJsonAsync("/api/research/analyze", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Unauthorized);
    }

    [Fact]
    public async Task Analyze_WhenFeatureDisabled_ReturnsForbidden403()
    {
        // Arrange
        var client = _factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureTestServices(services =>
            {
                services.AddSingleton<IOptions<ResearchOptions>>(
                    Microsoft.Extensions.Options.Options.Create(new ResearchOptions
                    {
                        Enabled = false // Feature explicitly disabled
                    }));
            });
        }).CreateClient();

        var token = await GetUserTokenAsync(client);
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

        var request = new CompetitorAnalysisRequest
        {
            TargetUrl = "https://cronometer.com/",
            FocusTopic = "Macro tracking"
        };

        // Act
        var response = await client.PostAsJsonAsync("/api/research/analyze", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Forbidden);
    }

    [Fact]
    public async Task Analyze_WithInvalidUrl_ReturnsBadRequest400()
    {
        // Arrange
        var client = _factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureTestServices(services =>
            {
                services.AddSingleton<IOptions<ResearchOptions>>(
                    Microsoft.Extensions.Options.Options.Create(new ResearchOptions
                    {
                        Enabled = true,
                        AllowedHosts = ["cronometer.com"]
                    }));

                var mockService = new Mock<ICompetitorResearchService>();
                mockService.Setup(s => s.AnalyzeCompetitorAsync(It.IsAny<CompetitorAnalysisRequest>(), It.IsAny<CancellationToken>()))
                    .ThrowsAsync(new InvalidResearchTargetException("Only HTTPS protocol is permitted for research targets."));
                services.AddScoped(_ => mockService.Object);
            });
        }).CreateClient();

        var token = await GetUserTokenAsync(client);
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

        var request = new CompetitorAnalysisRequest
        {
            TargetUrl = "http://cronometer.com/", // Invalid HTTP scheme
            FocusTopic = "Macro tracking"
        };

        // Act
        var response = await client.PostAsJsonAsync("/api/research/analyze", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.BadRequest);
    }

    [Fact]
    public async Task Analyze_WhenFeatureEnabledAndValidRequest_ReturnsOk200WithResult()
    {
        // Arrange
        var expectedResult = new CompetitorAnalysisResult
        {
            CompetitorName = "Cronometer",
            IdentifiedFeatures = ["Barcode scanner", "Micronutrient breakdown"],
            ProposedEngineImprovements = ["Add micronutrient constraints to GLOP LP solver"],
            SuggestedEndpoints = ["POST /api/optimizations/micronutrients"],
            SourceUrl = "https://cronometer.com/",
            AnalyzedAtUtc = DateTime.UtcNow
        };

        var client = _factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureTestServices(services =>
            {
                services.AddSingleton<IOptions<ResearchOptions>>(
                    Microsoft.Extensions.Options.Options.Create(new ResearchOptions
                    {
                        Enabled = true
                    }));

                var mockService = new Mock<ICompetitorResearchService>();
                mockService.Setup(s => s.AnalyzeCompetitorAsync(It.IsAny<CompetitorAnalysisRequest>(), It.IsAny<CancellationToken>()))
                    .ReturnsAsync(expectedResult);
                services.AddScoped(_ => mockService.Object);
            });
        }).CreateClient();

        var token = await GetUserTokenAsync(client);
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

        var request = new CompetitorAnalysisRequest
        {
            TargetUrl = "https://cronometer.com/",
            FocusTopic = "Micronutrients"
        };

        // Act
        var response = await client.PostAsJsonAsync("/api/research/analyze", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        var result = await response.Content.ReadFromJsonAsync<CompetitorAnalysisResult>();
        result.Should().NotBeNull();
        result!.CompetitorName.Should().Be("Cronometer");
        result.IdentifiedFeatures.Should().Contain("Barcode scanner");
        result.ProposedEngineImprovements.Should().ContainSingle().Which.Should().Contain("GLOP LP solver");
    }
}
