using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace SmartMacro.Api.DTOs;

public class CompetitorAnalysisRequest
{
    [Required]
    [Url]
    public string TargetUrl { get; set; } = string.Empty;

    [Required]
    [StringLength(200, MinimumLength = 1)]
    public string FocusTopic { get; set; } = string.Empty;
}

public class CompetitorAnalysisResult
{
    [JsonPropertyName("competitor_name")]
    public string CompetitorName { get; set; } = string.Empty;

    [JsonPropertyName("identified_features")]
    public List<string> IdentifiedFeatures { get; set; } = [];

    [JsonPropertyName("proposed_engine_improvements")]
    public List<string> ProposedEngineImprovements { get; set; } = [];

    [JsonPropertyName("suggested_endpoints")]
    public List<string> SuggestedEndpoints { get; set; } = [];

    [JsonPropertyName("source_url")]
    public string SourceUrl { get; set; } = string.Empty;

    [JsonPropertyName("analyzed_at_utc")]
    public DateTime AnalyzedAtUtc { get; set; } = DateTime.UtcNow;
}

public class CompetitorResearchRunStatus
{
    [JsonPropertyName("is_running")]
    public bool IsRunning { get; set; }

    [JsonPropertyName("auto_research_enabled")]
    public bool AutoResearchEnabled { get; set; }

    [JsonPropertyName("interval_minutes")]
    public int IntervalMinutes { get; set; }

    [JsonPropertyName("last_run_at_utc")]
    public DateTime? LastRunAtUtc { get; set; }

    [JsonPropertyName("next_run_at_utc")]
    public DateTime? NextRunAtUtc { get; set; }

    [JsonPropertyName("total_runs")]
    public int TotalRuns { get; set; }

    [JsonPropertyName("succeeded_targets")]
    public int SucceededTargets { get; set; }

    [JsonPropertyName("failed_targets")]
    public int FailedTargets { get; set; }

    [JsonPropertyName("last_error")]
    public string? LastError { get; set; }

    [JsonPropertyName("total_stored_reports")]
    public int TotalStoredReports { get; set; }
}
