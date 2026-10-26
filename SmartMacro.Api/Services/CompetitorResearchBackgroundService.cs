using System.Threading.Channels;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Options;

namespace SmartMacro.Api.Services;

public class CompetitorResearchBackgroundService : BackgroundService, ICompetitorResearchScheduler
{
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly IOptionsMonitor<ResearchOptions> _options;
    private readonly ICompetitorResearchHistoryStore _historyStore;
    private readonly ILogger<CompetitorResearchBackgroundService> _logger;
    private readonly Channel<bool> _triggerChannel = Channel.CreateBounded<bool>(new BoundedChannelOptions(1)
    {
        FullMode = BoundedChannelFullMode.DropOldest
    });
    private readonly SemaphoreSlim _executionLock = new(1, 1);

    public CompetitorResearchBackgroundService(
        IServiceScopeFactory scopeFactory,
        IOptionsMonitor<ResearchOptions> options,
        ICompetitorResearchHistoryStore historyStore,
        ILogger<CompetitorResearchBackgroundService> logger)
    {
        _scopeFactory = scopeFactory;
        _options = options;
        _historyStore = historyStore;
        _logger = logger;
    }

    public async Task<bool> TriggerRunNowAsync(CancellationToken cancellationToken = default)
    {
        var options = _options.CurrentValue;
        if (!options.Enabled)
        {
            _logger.LogWarning("Manual trigger ignored: Research feature is disabled.");
            return false;
        }

        return _triggerChannel.Writer.TryWrite(true);
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        var currentOptions = _options.CurrentValue;
        _historyStore.UpdateConfigStatus(currentOptions.AutoResearchEnabled, currentOptions.IntervalMinutes);

        var initialDelay = TimeSpan.FromSeconds(Math.Max(0, currentOptions.InitialDelaySeconds));
        _logger.LogInformation("CompetitorResearchBackgroundService started. Initial delay: {Delay} seconds.", initialDelay.TotalSeconds);

        try
        {
            await Task.Delay(initialDelay, stoppingToken);
        }
        catch (OperationCanceledException)
        {
            return;
        }

        while (!stoppingToken.IsCancellationRequested)
        {
            var options = _options.CurrentValue;
            _historyStore.UpdateConfigStatus(options.AutoResearchEnabled, options.IntervalMinutes);

            if (options.Enabled && options.AutoResearchEnabled && options.ScheduledTargets.Count > 0)
            {
                await RunCycleSafelyAsync(options, stoppingToken);
            }

            var interval = TimeSpan.FromMinutes(Math.Max(1, options.IntervalMinutes));
            try
            {
                // Wait for either interval timer or manual trigger signal
                using var cts = CancellationTokenSource.CreateLinkedTokenSource(stoppingToken);
                var delayTask = Task.Delay(interval, cts.Token);
                var triggerTask = _triggerChannel.Reader.WaitToReadAsync(cts.Token).AsTask();

                var completedTask = await Task.WhenAny(delayTask, triggerTask);
                cts.Cancel(); // Cancel the other task

                if (completedTask == triggerTask && await _triggerChannel.Reader.WaitToReadAsync(CancellationToken.None))
                {
                    while (_triggerChannel.Reader.TryRead(out _)) { }
                    _logger.LogInformation("Competitor research manual trigger received. Executing cycle now...");
                    await RunCycleSafelyAsync(_options.CurrentValue, stoppingToken);
                }
            }
            catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested)
            {
                break;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Unexpected error in CompetitorResearchBackgroundService loop.");
                await Task.Delay(TimeSpan.FromSeconds(10), stoppingToken);
            }
        }

        _logger.LogInformation("CompetitorResearchBackgroundService is stopping.");
    }

    public async Task RunCycleSafelyAsync(ResearchOptions options, CancellationToken cancellationToken)
    {
        if (!await _executionLock.WaitAsync(0, cancellationToken))
        {
            _logger.LogInformation("A competitor research cycle is already running. Skipping concurrent execution.");
            return;
        }

        try
        {
            _historyStore.RecordRunStarted();
            _logger.LogInformation("Starting competitor research cycle for {Count} scheduled targets...", options.ScheduledTargets.Count);

            using var scope = _scopeFactory.CreateScope();
            var researchService = scope.ServiceProvider.GetRequiredService<ICompetitorResearchService>();

            var succeeded = 0;
            var failed = 0;
            string? lastError = null;

            foreach (var target in options.ScheduledTargets)
            {
                if (cancellationToken.IsCancellationRequested) break;

                try
                {
                    _logger.LogInformation("Executing automated research on target: {TargetUrl} ({FocusTopic})...", target.TargetUrl, target.FocusTopic);
                    var request = new CompetitorAnalysisRequest
                    {
                        TargetUrl = target.TargetUrl,
                        FocusTopic = target.FocusTopic
                    };

                    var result = await researchService.AnalyzeCompetitorAsync(request, cancellationToken);
                    _historyStore.AddReport(result);
                    succeeded++;
                    _logger.LogInformation("Automated research completed successfully for {TargetUrl}. Identified competitor: {CompetitorName}.", target.TargetUrl, result.CompetitorName);
                }
                catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
                {
                    throw;
                }
                catch (Exception ex)
                {
                    failed++;
                    lastError = ex.Message;
                    _logger.LogWarning(ex, "Automated research failed for target {TargetUrl}: {Message}", target.TargetUrl, ex.Message);
                }
            }

            var nextRunAtUtc = DateTime.UtcNow.AddMinutes(Math.Max(1, options.IntervalMinutes));
            _historyStore.RecordRunCompleted(succeeded, failed, nextRunAtUtc, lastError);
            _logger.LogInformation("Competitor research cycle finished. Succeeded: {Succeeded}, Failed: {Failed}. Next scheduled run: {NextRunUtc}.", succeeded, failed, nextRunAtUtc);
        }
        finally
        {
            _executionLock.Release();
        }
    }
}
