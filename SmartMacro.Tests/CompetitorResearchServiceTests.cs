using System.Net;
using FluentAssertions;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Moq;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Options;
using SmartMacro.Api.Services;

namespace SmartMacro.Tests;

public class CompetitorResearchServiceTests
{
    private readonly Mock<ITargetUrlValidator> _mockUrlValidator = new();
    private readonly Mock<IPageContentFetcher> _mockContentFetcher = new();
    private readonly Mock<IClaudeService> _mockClaudeService = new();
    private readonly Mock<ILogger<CompetitorResearchService>> _mockLogger = new();
    private readonly IMemoryCache _memoryCache = new MemoryCache(new MemoryCacheOptions());
    private readonly IOptions<ResearchOptions> _options = Microsoft.Extensions.Options.Options.Create(new ResearchOptions
    {
        CacheHours = 24,
        MaxContentChars = 30000
    });

    private CompetitorResearchService CreateService()
    {
        return new CompetitorResearchService(
            _mockUrlValidator.Object,
            _mockContentFetcher.Object,
            _mockClaudeService.Object,
            _memoryCache,
            _options,
            _mockLogger.Object);
    }

    [Fact]
    public async Task AnalyzeCompetitorAsync_ValidCleanJson_ReturnsParsedResult()
    {
        // Arrange
        var request = new CompetitorAnalysisRequest
        {
            TargetUrl = "https://cronometer.com/features",
            FocusTopic = "Macro tracking & micronutrients"
        };

        const string pageText = "Cronometer tracks up to 84 micronutrients and macro targets.";
        _mockContentFetcher
            .Setup(f => f.FetchTextAsync(request.TargetUrl, It.IsAny<CancellationToken>()))
            .ReturnsAsync(pageText);

        const string cleanJson = """
            {
              "competitor_name": "Cronometer",
              "identified_features": ["Detailed micronutrient breakdown", "Dynamic macro targets"],
              "proposed_engine_improvements": ["Add micronutrient lower-bound constraints to GLOP LP solver"],
              "suggested_endpoints": ["POST /api/optimizations/micronutrients"]
            }
            """;

        _mockClaudeService
            .Setup(c => c.SendPromptAsync(It.IsAny<string>(), It.IsAny<string?>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(cleanJson);

        var service = CreateService();

        // Act
        var result = await service.AnalyzeCompetitorAsync(request);

        // Assert
        result.Should().NotBeNull();
        result.CompetitorName.Should().Be("Cronometer");
        result.IdentifiedFeatures.Should().HaveCount(2).And.Contain("Detailed micronutrient breakdown");
        result.ProposedEngineImprovements.Should().ContainSingle().Which.Should().Contain("GLOP LP solver");
        result.SuggestedEndpoints.Should().ContainSingle().Which.Should().Be("POST /api/optimizations/micronutrients");
        result.SourceUrl.Should().Be(request.TargetUrl);
        result.AnalyzedAtUtc.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(5));
    }

    [Fact]
    public async Task AnalyzeCompetitorAsync_JsonWithMarkdownCodeFence_StripsFenceAndReturnsResult()
    {
        // Arrange
        var request = new CompetitorAnalysisRequest
        {
            TargetUrl = "https://macrofactor.com/macro-program",
            FocusTopic = "Expenditure algorithm"
        };

        _mockContentFetcher
            .Setup(f => f.FetchTextAsync(request.TargetUrl, It.IsAny<CancellationToken>()))
            .ReturnsAsync("MacroFactor dynamically calculates expenditure based on weight and food logs.");

        const string fencedJson = """
            ```json
            {
              "competitor_name": "MacroFactor",
              "identified_features": ["Adaptive metabolic expenditure calculation"],
              "proposed_engine_improvements": ["Incorporate energy balance differential into daily target engine"],
              "suggested_endpoints": ["GET /api/expenditure/estimate"]
            }
            ```
            """;

        _mockClaudeService
            .Setup(c => c.SendPromptAsync(It.IsAny<string>(), It.IsAny<string?>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(fencedJson);

        var service = CreateService();

        // Act
        var result = await service.AnalyzeCompetitorAsync(request);

        // Assert
        result.Should().NotBeNull();
        result.CompetitorName.Should().Be("MacroFactor");
        result.IdentifiedFeatures.Should().Contain("Adaptive metabolic expenditure calculation");
    }

    [Fact]
    public async Task AnalyzeCompetitorAsync_MalformedJson_ThrowsAnthropicApiExceptionBadGateway()
    {
        // Arrange
        var request = new CompetitorAnalysisRequest
        {
            TargetUrl = "https://myfitnesspal.com/food",
            FocusTopic = "Barcode scanner"
        };

        _mockContentFetcher
            .Setup(f => f.FetchTextAsync(request.TargetUrl, It.IsAny<CancellationToken>()))
            .ReturnsAsync("MyFitnessPal barcode scanner.");

        _mockClaudeService
            .Setup(c => c.SendPromptAsync(It.IsAny<string>(), It.IsAny<string?>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync("Sorry, as an AI model I cannot fulfill this request.");

        var service = CreateService();

        // Act
        var act = () => service.AnalyzeCompetitorAsync(request);

        // Assert
        var ex = await act.Should().ThrowAsync<AnthropicApiException>();
        ex.Which.StatusCode.Should().Be(HttpStatusCode.BadGateway);
        ex.Which.ErrorType.Should().Be("json_parse_error");
    }

    [Fact]
    public async Task AnalyzeCompetitorAsync_CacheHit_DoesNotCallFetcherOrClaude()
    {
        // Arrange
        var request = new CompetitorAnalysisRequest
        {
            TargetUrl = "https://cronometer.com/faq",
            FocusTopic = "Integration"
        };

        _mockContentFetcher
            .Setup(f => f.FetchTextAsync(request.TargetUrl, It.IsAny<CancellationToken>()))
            .ReturnsAsync("Page content about integration.");

        const string jsonResponse = """
            {
              "competitor_name": "Cronometer",
              "identified_features": ["Garmin sync"],
              "proposed_engine_improvements": ["Auto-sync activity burns to daily target"],
              "suggested_endpoints": ["POST /api/integrations/garmin"]
            }
            """;

        _mockClaudeService
            .Setup(c => c.SendPromptAsync(It.IsAny<string>(), It.IsAny<string?>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(jsonResponse);

        var service = CreateService();

        // Act 1 - Initial call
        var firstResult = await service.AnalyzeCompetitorAsync(request);

        // Act 2 - Second call with identical URL and FocusTopic
        var secondResult = await service.AnalyzeCompetitorAsync(request);

        // Assert
        firstResult.Should().NotBeNull();
        secondResult.Should().NotBeNull();
        secondResult.CompetitorName.Should().Be("Cronometer");

        // Fetcher and Claude should have been invoked exactly ONCE
        _mockContentFetcher.Verify(f => f.FetchTextAsync(request.TargetUrl, It.IsAny<CancellationToken>()), Times.Once);
        _mockClaudeService.Verify(c => c.SendPromptAsync(It.IsAny<string>(), It.IsAny<string?>(), It.IsAny<CancellationToken>()), Times.Once);
    }

    [Fact]
    public async Task AnalyzeCompetitorAsync_WrapsContentInCompetitorPageTags()
    {
        // Arrange
        var request = new CompetitorAnalysisRequest
        {
            TargetUrl = "https://eatthismuch.com/how-it-works",
            FocusTopic = "Meal generator"
        };

        const string rawContent = "EatThisMuch automatically generates weekly meal plans.";
        _mockContentFetcher
            .Setup(f => f.FetchTextAsync(request.TargetUrl, It.IsAny<CancellationToken>()))
            .ReturnsAsync(rawContent);

        string? capturedUserPrompt = null;
        string? capturedSystemPrompt = null;

        _mockClaudeService
            .Setup(c => c.SendPromptAsync(It.IsAny<string>(), It.IsAny<string?>(), It.IsAny<CancellationToken>()))
            .Callback<string, string?, CancellationToken>((user, sys, _) =>
            {
                capturedUserPrompt = user;
                capturedSystemPrompt = sys;
            })
            .ReturnsAsync("""
                {
                  "competitor_name": "EatThisMuch",
                  "identified_features": ["Meal generator"],
                  "proposed_engine_improvements": ["Support meal schedule variety"],
                  "suggested_endpoints": ["POST /api/optimizations/weekly"]
                }
                """);

        var service = CreateService();

        // Act
        await service.AnalyzeCompetitorAsync(request);

        // Assert
        capturedUserPrompt.Should().NotBeNull();
        capturedUserPrompt.Should().Contain("<competitor_page>");
        capturedUserPrompt.Should().Contain("</competitor_page>");
        capturedUserPrompt.Should().Contain(rawContent);

        capturedSystemPrompt.Should().NotBeNull();
        capturedSystemPrompt.Should().Contain("untrusted");
        capturedSystemPrompt.Should().Contain("Google OR-Tools");
    }
}
