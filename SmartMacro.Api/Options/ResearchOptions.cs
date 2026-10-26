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
}
