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
