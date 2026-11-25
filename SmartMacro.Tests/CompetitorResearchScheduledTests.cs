using FluentAssertions;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Moq;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Options;
using SmartMacro.Api.Services;

namespace SmartMacro.Tests;

public class CompetitorResearchScheduledTests
{
    [Fact]
    public void HistoryStore_AddReport_MaintainsLifoAndLimit()
    {
        // Arrange
        var store = new CompetitorResearchHistoryStore();

        // Act
        for (int i = 1; i <= 105; i++)
        {
            store.AddReport(new CompetitorAnalysisResult
            {
                CompetitorName = $"Competitor_{i}",
                SourceUrl = $"https://competitor{i}.com"
            });
        }

        // Assert
        var latest10 = store.GetLatestReports(10);
        latest10.Should().HaveCount(10);
        latest10[0].CompetitorName.Should().Be("Competitor_105");

        var status = store.GetRunStatus();
        status.TotalStoredReports.Should().Be(100);
    }

    [Fact]
    public void HistoryStore_RecordRunLifecycle_UpdatesStatusCorrectly()
    {
        // Arrange
        var store = new CompetitorResearchHistoryStore();
        store.UpdateConfigStatus(autoResearchEnabled: true, intervalMinutes: 60);

        // Act - Run Started
        store.RecordRunStarted();
        var statusStarted = store.GetRunStatus();
        statusStarted.IsRunning.Should().BeTrue();
        statusStarted.AutoResearchEnabled.Should().BeTrue();
        statusStarted.IntervalMinutes.Should().Be(60);

        // Act - Run Completed
        var nextRun = DateTime.UtcNow.AddMinutes(60);
        store.RecordRunCompleted(succeededTargets: 2, failedTargets: 1, nextRunAtUtc: nextRun, lastError: "Rate limit");

        // Assert
        var statusCompleted = store.GetRunStatus();
        statusCompleted.IsRunning.Should().BeFalse();
        statusCompleted.TotalRuns.Should().Be(1);
        statusCompleted.SucceededTargets.Should().Be(2);
        statusCompleted.FailedTargets.Should().Be(1);
        statusCompleted.LastError.Should().Be("Rate limit");
        statusCompleted.NextRunAtUtc.Should().Be(nextRun);
    }

    [Fact]
    public async Task BackgroundService_WhenFeatureDisabled_DoesNotExecuteTargets()
    {
        // Arrange
        var mockScopeFactory = new Mock<IServiceScopeFactory>();
        var mockHistoryStore = new Mock<ICompetitorResearchHistoryStore>();
        var mockLogger = new Mock<ILogger<CompetitorResearchBackgroundService>>();

        var options = new ResearchOptions
        {
            Enabled = false,
            AutoResearchEnabled = true,
            InitialDelaySeconds = 0
        };

        var mockOptions = new Mock<IOptionsMonitor<ResearchOptions>>();
        mockOptions.Setup(o => o.CurrentValue).Returns(options);

        var service = new CompetitorResearchBackgroundService(
            mockScopeFactory.Object,
            mockOptions.Object,
            mockHistoryStore.Object,
            mockLogger.Object);

        using var cts = new CancellationTokenSource();
        cts.CancelAfter(50);

        // Act
        await service.StartAsync(cts.Token);
        await Task.Delay(100);
        await service.StopAsync(CancellationToken.None);

        // Assert: Scope should not be created because Enabled is false
        mockScopeFactory.Verify(f => f.CreateScope(), Times.Never);
    }

    [Fact]
    public async Task BackgroundService_RunCycleSafelyAsync_ExecutesTargetsAndResilientToErrors()
    {
        // Arrange
        var mockService = new Mock<ICompetitorResearchService>();
        mockService.Setup(s => s.AnalyzeCompetitorAsync(
            It.Is<CompetitorAnalysisRequest>(r => r.TargetUrl.Contains("cronometer")),
            It.IsAny<CancellationToken>()))
            .ReturnsAsync(new CompetitorAnalysisResult
            {
                CompetitorName = "Cronometer",
                SourceUrl = "https://cronometer.com/"
            });

        mockService.Setup(s => s.AnalyzeCompetitorAsync(
            It.Is<CompetitorAnalysisRequest>(r => r.TargetUrl.Contains("macrofactor")),
            It.IsAny<CancellationToken>()))
            .ThrowsAsync(new InvalidOperationException("Scraping timeout"));

        var serviceCollection = new ServiceCollection();
        serviceCollection.AddScoped(_ => mockService.Object);
        var serviceProvider = serviceCollection.BuildServiceProvider();

        var mockScope = new Mock<IServiceScope>();
        mockScope.Setup(s => s.ServiceProvider).Returns(serviceProvider);

        var mockScopeFactory = new Mock<IServiceScopeFactory>();
        mockScopeFactory.Setup(f => f.CreateScope()).Returns(mockScope.Object);

        var historyStore = new CompetitorResearchHistoryStore();
        var mockLogger = new Mock<ILogger<CompetitorResearchBackgroundService>>();

        var options = new ResearchOptions
        {
            Enabled = true,
            AutoResearchEnabled = true,
            IntervalMinutes = 60,
            ScheduledTargets =
            [
                new ScheduledResearchTarget { TargetUrl = "https://cronometer.com/", FocusTopic = "macros" },
                new ScheduledResearchTarget { TargetUrl = "https://macrofactor.com/", FocusTopic = "metabolism" }
            ]
        };

        var mockOptions = new Mock<IOptionsMonitor<ResearchOptions>>();
        mockOptions.Setup(o => o.CurrentValue).Returns(options);

        var backgroundService = new CompetitorResearchBackgroundService(
            mockScopeFactory.Object,
            mockOptions.Object,
            historyStore,
            mockLogger.Object);

        // Act
        await backgroundService.RunCycleSafelyAsync(options, CancellationToken.None);

        // Assert
        var status = historyStore.GetRunStatus();
        status.TotalRuns.Should().Be(1);
        status.SucceededTargets.Should().Be(1);
        status.FailedTargets.Should().Be(1);
        status.LastError.Should().Be("Scraping timeout");

        var reports = historyStore.GetLatestReports(10);
        reports.Should().HaveCount(1);
        reports[0].CompetitorName.Should().Be("Cronometer");
    }

    [Fact]
    public async Task BackgroundService_TriggerRunNowAsync_WhenDisabled_ReturnsFalse()
    {
        // Arrange
        var mockScopeFactory = new Mock<IServiceScopeFactory>();
        var mockHistoryStore = new Mock<ICompetitorResearchHistoryStore>();
        var mockLogger = new Mock<ILogger<CompetitorResearchBackgroundService>>();

        var options = new ResearchOptions { Enabled = false };
        var mockOptions = new Mock<IOptionsMonitor<ResearchOptions>>();
        mockOptions.Setup(o => o.CurrentValue).Returns(options);

        var service = new CompetitorResearchBackgroundService(
            mockScopeFactory.Object,
            mockOptions.Object,
            mockHistoryStore.Object,
            mockLogger.Object);

        // Act
        var triggered = await service.TriggerRunNowAsync();

        // Assert
        triggered.Should().BeFalse();
    }
}
