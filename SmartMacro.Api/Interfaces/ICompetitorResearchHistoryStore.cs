using SmartMacro.Api.DTOs;

namespace SmartMacro.Api.Interfaces;

public interface ICompetitorResearchHistoryStore
{
    void AddReport(CompetitorAnalysisResult result);
    IReadOnlyList<CompetitorAnalysisResult> GetLatestReports(int count = 10);
    CompetitorResearchRunStatus GetRunStatus();
    void RecordRunStarted();
    void RecordRunCompleted(int succeededTargets, int failedTargets, DateTime? nextRunAtUtc, string? lastError = null);
    void UpdateConfigStatus(bool autoResearchEnabled, int intervalMinutes);
}
