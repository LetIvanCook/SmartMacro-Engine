using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using Microsoft.Extensions.Options;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Options;

namespace SmartMacro.Api.Services;

public class ClaudeService : IClaudeService
{
    private readonly HttpClient _httpClient;
    private readonly AnthropicOptions _options;
    private readonly ILogger<ClaudeService> _logger;

    public ClaudeService(
        HttpClient httpClient,
        IOptions<AnthropicOptions> options,
        ILogger<ClaudeService> logger)
    {
        _httpClient = httpClient;
        _options = options.Value;
        _logger = logger;
    }

    public async Task<string> SendPromptAsync(
        string userPrompt,
        string? systemPrompt = null,
        CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(_options.ApiKey))
        {
            throw new AnthropicConfigurationException("Anthropic API key is not configured.");
        }

        var requestDto = new ClaudeRequestDto
        {
            Model = _options.Model,
            MaxTokens = _options.MaxTokens,
            System = systemPrompt,
            Messages =
            [
                new ClaudeMessageDto
                {
                    Role = "user",
                    Content = userPrompt
                }
            ]
        };

        using var request = new HttpRequestMessage(HttpMethod.Post, "v1/messages")
        {
            Content = JsonContent.Create(requestDto)
        };

        request.Headers.Add("x-api-key", _options.ApiKey);
        if (!request.Headers.Contains("anthropic-version"))
        {
            request.Headers.Add("anthropic-version", "2023-06-01");
        }

        var response = await _httpClient.SendAsync(request, cancellationToken);

        if (!response.IsSuccessStatusCode)
        {
            response.Headers.TryGetValues("request-id", out var requestIds);
            var requestId = requestIds?.FirstOrDefault();

            var errorBody = await response.Content.ReadAsStringAsync(cancellationToken);
            string? errorType = null;
            string? errorMessage = null;

            try
            {
                var errorObj = JsonSerializer.Deserialize<AnthropicErrorResponse>(errorBody);
                errorType = errorObj?.Error?.Type;
                errorMessage = errorObj?.Error?.Message;
            }
            catch
            {
                // Body was not in JSON format
            }

            errorMessage ??= errorBody;

            _logger.LogError(
                "Anthropic API call failed with status {StatusCode}, RequestId: {RequestId}, ErrorType: {ErrorType}, ErrorMessage: {ErrorMessage}",
                (int)response.StatusCode,
                requestId,
                errorType,
                errorMessage);

            throw new AnthropicApiException(
                response.StatusCode,
                $"Anthropic API returned {(int)response.StatusCode} ({response.StatusCode}): {errorMessage}",
                errorType);
        }

        var responseDto = await response.Content.ReadFromJsonAsync<ClaudeResponseDto>(cancellationToken: cancellationToken);
        if (responseDto?.Content == null || responseDto.Content.Count == 0)
        {
            throw new AnthropicApiException(HttpStatusCode.BadGateway, "Anthropic API returned an empty content array.");
        }

        if (string.Equals(responseDto.StopReason, "max_tokens", StringComparison.OrdinalIgnoreCase))
        {
            _logger.LogWarning(
                "Anthropic API response was truncated due to reaching max_tokens ({MaxTokens}).",
                _options.MaxTokens);
        }

        var textBlocks = responseDto.Content
            .Where(c => c.Type == "text" && !string.IsNullOrEmpty(c.Text))
            .Select(c => c.Text);

        return string.Join("\n", textBlocks);
    }
}
