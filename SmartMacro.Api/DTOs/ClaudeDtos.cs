using System.Text.Json.Serialization;

namespace SmartMacro.Api.DTOs;

public class ClaudeRequestDto
{
    [JsonPropertyName("model")]
    public string Model { get; set; } = string.Empty;

    [JsonPropertyName("max_tokens")]
    public int MaxTokens { get; set; }

    [JsonPropertyName("system")]
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public string? System { get; set; }

    [JsonPropertyName("messages")]
    public List<ClaudeMessageDto> Messages { get; set; } = [];
}

public class ClaudeMessageDto
{
    [JsonPropertyName("role")]
    public string Role { get; set; } = "user";

    [JsonPropertyName("content")]
    public string Content { get; set; } = string.Empty;
}

public class ClaudeResponseDto
{
    [JsonPropertyName("id")]
    public string? Id { get; set; }

    [JsonPropertyName("type")]
    public string? Type { get; set; }

    [JsonPropertyName("role")]
    public string? Role { get; set; }

    [JsonPropertyName("content")]
    public List<ClaudeContentDto>? Content { get; set; }

    [JsonPropertyName("model")]
    public string? Model { get; set; }

    [JsonPropertyName("stop_reason")]
    public string? StopReason { get; set; }

    [JsonPropertyName("usage")]
    public AnthropicUsageDto? Usage { get; set; }
}

public class ClaudeContentDto
{
    [JsonPropertyName("type")]
    public string? Type { get; set; }

    [JsonPropertyName("text")]
    public string? Text { get; set; }
}

public class AnthropicUsageDto
{
    [JsonPropertyName("input_tokens")]
    public int? InputTokens { get; set; }

    [JsonPropertyName("output_tokens")]
    public int? OutputTokens { get; set; }
}

public class AnthropicErrorResponse
{
    [JsonPropertyName("type")]
    public string? Type { get; set; }

    [JsonPropertyName("error")]
    public AnthropicErrorDetail? Error { get; set; }
}

public class AnthropicErrorDetail
{
    [JsonPropertyName("type")]
    public string? Type { get; set; }

    [JsonPropertyName("message")]
    public string? Message { get; set; }
}
