namespace SmartMacro.Api.Interfaces;

public interface IClaudeService
{
    Task<string> SendPromptAsync(string userPrompt, string? systemPrompt = null, CancellationToken cancellationToken = default);
}
