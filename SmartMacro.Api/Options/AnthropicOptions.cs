using System.ComponentModel.DataAnnotations;

namespace SmartMacro.Api.Options;

public class AnthropicOptions
{
    public const string SectionName = "Anthropic";

    public string ApiKey { get; set; } = string.Empty;

    [Required]
    [Url]
    public string BaseUrl { get; set; } = "https://api.anthropic.com/";

    [Required]
    public string Model { get; set; } = "claude-sonnet-5-5";

    [Range(1, 100000)]
    public int MaxTokens { get; set; } = 4096;

    [Range(1, 600)]
    public int TimeoutSeconds { get; set; } = 90;
}
