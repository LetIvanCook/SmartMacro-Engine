using SmartMacro.Api.DTOs;
using SmartMacro.Api.Interfaces;

namespace SmartMacro.Api.Services;

public class CompetitorResearchHistoryStore : ICompetitorResearchHistoryStore
{
    private const int MaxStoredReports = 100;
    private readonly object _lock = new();
    private readonly List<CompetitorAnalysisResult> _reports = new();

    private bool _isRunning;
    private bool _autoResearchEnabled;
    private int _intervalMinutes;
    private DateTime? _lastRunAtUtc;
    private DateTime? _nextRunAtUtc;
    private int _totalRuns;
    private int _succeededTargets;
    private int _failedTargets;
    private string? _lastError;

    public void AddReport(CompetitorAnalysisResult result)
    {
        lock (_lock)
        {
            _reports.Insert(0, result);
            if (_reports.Count > MaxStoredReports)
            {
                _reports.RemoveAt(_reports.Count - 1);
            }
        }
    }

    public IReadOnlyList<CompetitorAnalysisResult> GetLatestReports(int count = 10)
    {
        lock (_lock)
        {
            var take = Math.Clamp(count, 1, MaxStoredReports);
            return _reports.Take(take).ToList().AsReadOnly();
        }
    }

    public CompetitorResearchRunStatus GetRunStatus()
    {
        lock (_lock)
        {
            return new CompetitorResearchRunStatus
            {
                IsRunning = _isRunning,
                AutoResearchEnabled = _autoResearchEnabled,
                IntervalMinutes = _intervalMinutes,
                LastRunAtUtc = _lastRunAtUtc,
                NextRunAtUtc = _nextRunAtUtc,
                TotalRuns = _totalRuns,
                SucceededTargets = _succeededTargets,
                FailedTargets = _failedTargets,
                LastError = _lastError,
                TotalStoredReports = _reports.Count
            };
        }
    }

    public void RecordRunStarted()
    {
        lock (_lock)
        {
            _isRunning = true;
            _lastError = null;
        }
    }

    public void RecordRunCompleted(int succeededTargets, int failedTargets, DateTime? nextRunAtUtc, string? lastError = null)
    {
        lock (_lock)
        {
            _isRunning = false;
            _lastRunAtUtc = DateTime.UtcNow;
            _nextRunAtUtc = nextRunAtUtc;
            _totalRuns++;
            _succeededTargets += succeededTargets;
            _failedTargets += failedTargets;
            _lastError = lastError;
        }
    }

    public void UpdateConfigStatus(bool autoResearchEnabled, int intervalMinutes)
    {
        lock (_lock)
        {
            _autoResearchEnabled = autoResearchEnabled;
            _intervalMinutes = intervalMinutes;
        }
    }
}
