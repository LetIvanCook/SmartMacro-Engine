using System.ComponentModel.DataAnnotations;

namespace SmartMacro.Api.Options;

public class ResearchOptions
{
    public const string SectionName = "Research";

    public bool Enabled { get; set; } = false;

    [Required]
    public string[] AllowedHosts { get; set; } = [
        "macrofactor.com",
        "cronometer.com",
        "myfitnesspal.com",
        "eatthismuch.com"
    ];

    [Range(100, 500000)]
    public int MaxContentChars { get; set; } = 30000;

    [Range(1, 300)]
    public int NavigationTimeoutSeconds { get; set; } = 30;

    [Range(1, 20)]
    public int MaxConcurrentBrowsers { get; set; } = 2;

    [Range(1, 168)]
    public int CacheHours { get; set; } = 24;

    public bool AutoResearchEnabled { get; set; } = false;

    [Range(1, 43200)]
    public int IntervalMinutes { get; set; } = 1440;

    [Range(0, 3600)]
    public int InitialDelaySeconds { get; set; } = 30;

    public List<ScheduledResearchTarget> ScheduledTargets { get; set; } = [
        new ScheduledResearchTarget
        {
            TargetUrl = "https://cronometer.com/",
            FocusTopic = "dynamic energy expenditure and micronutrient target tracking"
        },
        new ScheduledResearchTarget
        {
            TargetUrl = "https://macrofactor.com/",
            FocusTopic = "smart macro planning and dynamic metabolic adaptation"
        }
    ];
}

public class ScheduledResearchTarget
{
    [Required]
    [Url]
    public string TargetUrl { get; set; } = string.Empty;

    [Required]
    [StringLength(200)]
    public string FocusTopic { get; set; } = string.Empty;
}
