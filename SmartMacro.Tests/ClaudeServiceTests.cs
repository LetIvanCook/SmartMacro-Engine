using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using FluentAssertions;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Moq;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Options;
using SmartMacro.Api.Services;

namespace SmartMacro.Tests;

public class ClaudeServiceTests
{
    private readonly Mock<ILogger<ClaudeService>> _mockLogger = new();

    private ClaudeService CreateService(
        HttpMessageHandler handler,
        string apiKey = "test-api-key",
        string model = "claude-sonnet-5-5",
        int maxTokens = 4096)
    {
        var options = Microsoft.Extensions.Options.Options.Create(new AnthropicOptions
        {
            ApiKey = apiKey,
            Model = model,
            MaxTokens = maxTokens,
            BaseUrl = "https://api.anthropic.com/",
            TimeoutSeconds = 30
        });

        var httpClient = new HttpClient(handler)
        {
            BaseAddress = new Uri("https://api.anthropic.com/")
        };

        return new ClaudeService(httpClient, options, _mockLogger.Object);
    }

    [Fact]
    public async Task SendPromptAsync_WhenApiKeyIsEmpty_ThrowsAnthropicConfigurationException()
    {
        // Arrange
        var handler = new FakeHttpMessageHandler((_, _) =>
            Task.FromResult(new HttpResponseMessage(HttpStatusCode.OK)));
        var service = CreateService(handler, apiKey: "");

        // Act
        var act = () => service.SendPromptAsync("Hello");

        // Assert
        await act.Should().ThrowAsync<AnthropicConfigurationException>()
            .WithMessage("*Anthropic API key is not configured*");
    }

    [Fact]
    public async Task SendPromptAsync_When200SuccessWithMultipleContentBlocks_ConcatenatesTextCorrectly()
    {
        // Arrange
        var responsePayload = new ClaudeResponseDto
        {
            Id = "msg_123",
            Type = "message",
            Role = "assistant",
            Model = "claude-sonnet-5-5",
            StopReason = "end_turn",
            Content =
            [
                new ClaudeContentDto { Type = "text", Text = "Block 1 content." },
                new ClaudeContentDto { Type = "text", Text = "Block 2 content." }
            ]
        };

        var handler = new FakeHttpMessageHandler((req, _) =>
        {
            var res = new HttpResponseMessage(HttpStatusCode.OK)
            {
                Content = JsonContent.Create(responsePayload)
            };
            return Task.FromResult(res);
        });

        var service = CreateService(handler);

        // Act
        var result = await service.SendPromptAsync("Analyze this");

        // Assert
        result.Should().Be("Block 1 content.\nBlock 2 content.");
    }

    [Fact]
    public async Task SendPromptAsync_When401Unauthorized_ThrowsAnthropicApiExceptionWith401()
    {
        // Arrange
        var errorResponse = new AnthropicErrorResponse
        {
            Type = "error",
            Error = new AnthropicErrorDetail
            {
                Type = "authentication_error",
                Message = "Invalid API key provided"
            }
        };

        var handler = new FakeHttpMessageHandler((_, _) =>
        {
            var res = new HttpResponseMessage(HttpStatusCode.Unauthorized)
            {
                Content = JsonContent.Create(errorResponse)
            };
            res.Headers.Add("request-id", "req_auth_err_401");
            return Task.FromResult(res);
        });

        var service = CreateService(handler);

        // Act
        var act = () => service.SendPromptAsync("Hello");

        // Assert
        var ex = await act.Should().ThrowAsync<AnthropicApiException>();
        ex.Which.StatusCode.Should().Be(HttpStatusCode.Unauthorized);
        ex.Which.ErrorType.Should().Be("authentication_error");
        ex.Which.Message.Should().Contain("Invalid API key provided");
    }

    [Fact]
    public async Task SendPromptAsync_When429TooManyRequests_ThrowsAnthropicApiExceptionWith429()
    {
        // Arrange
        var errorResponse = new AnthropicErrorResponse
        {
            Type = "error",
            Error = new AnthropicErrorDetail
            {
                Type = "rate_limit_error",
                Message = "Rate limit reached"
            }
        };

        var handler = new FakeHttpMessageHandler((_, _) =>
        {
            var res = new HttpResponseMessage(HttpStatusCode.TooManyRequests)
            {
                Content = JsonContent.Create(errorResponse)
            };
            return Task.FromResult(res);
        });

        var service = CreateService(handler);

        // Act
        var act = () => service.SendPromptAsync("Hello");

        // Assert
        var ex = await act.Should().ThrowAsync<AnthropicApiException>();
        ex.Which.StatusCode.Should().Be(HttpStatusCode.TooManyRequests);
        ex.Which.ErrorType.Should().Be("rate_limit_error");
    }

    [Fact]
    public async Task SendPromptAsync_When500InternalServerError_ThrowsAnthropicApiExceptionWith500()
    {
        // Arrange
        var errorResponse = new AnthropicErrorResponse
        {
            Type = "error",
            Error = new AnthropicErrorDetail
            {
                Type = "api_error",
                Message = "Internal server error"
            }
        };

        var handler = new FakeHttpMessageHandler((_, _) =>
        {
            var res = new HttpResponseMessage(HttpStatusCode.InternalServerError)
            {
                Content = JsonContent.Create(errorResponse)
            };
            return Task.FromResult(res);
        });

        var service = CreateService(handler);

        // Act
        var act = () => service.SendPromptAsync("Hello");

        // Assert
        var ex = await act.Should().ThrowAsync<AnthropicApiException>();
        ex.Which.StatusCode.Should().Be(HttpStatusCode.InternalServerError);
        ex.Which.ErrorType.Should().Be("api_error");
    }

    [Fact]
    public async Task SendPromptAsync_WhenResponseBodyInvalidJson_ThrowsAnthropicApiException()
    {
        // Arrange
        var handler = new FakeHttpMessageHandler((_, _) =>
        {
            var res = new HttpResponseMessage(HttpStatusCode.BadGateway)
            {
                Content = new StringContent("<html><body>502 Bad Gateway from Proxy</body></html>")
            };
            return Task.FromResult(res);
        });

        var service = CreateService(handler);

        // Act
        var act = () => service.SendPromptAsync("Hello");

        // Assert
        var ex = await act.Should().ThrowAsync<AnthropicApiException>();
        ex.Which.StatusCode.Should().Be(HttpStatusCode.BadGateway);
        ex.Which.Message.Should().Contain("502 Bad Gateway");
    }

    [Fact]
    public async Task SendPromptAsync_SendsExpectedHeadersAndPayload()
    {
        // Arrange
        HttpRequestMessage? capturedRequest = null;
        string? capturedBody = null;

        var responsePayload = new ClaudeResponseDto
        {
            Id = "msg_ok",
            Content = [new ClaudeContentDto { Type = "text", Text = "OK response" }]
        };

        var handler = new FakeHttpMessageHandler(async (req, _) =>
        {
            capturedRequest = req;
            if (req.Content != null)
            {
                capturedBody = await req.Content.ReadAsStringAsync();
            }
            return new HttpResponseMessage(HttpStatusCode.OK)
            {
                Content = JsonContent.Create(responsePayload)
            };
        });

        var service = CreateService(handler, apiKey: "custom-secret-key-123", model: "claude-sonnet-5-5", maxTokens: 2048);

        // Act
        await service.SendPromptAsync("My test user prompt", "My test system prompt");

        // Assert
        capturedRequest.Should().NotBeNull();
        capturedRequest!.Headers.Contains("x-api-key").Should().BeTrue();
        capturedRequest.Headers.GetValues("x-api-key").Should().ContainSingle().Which.Should().Be("custom-secret-key-123");
        capturedRequest.Headers.Contains("anthropic-version").Should().BeTrue();
        capturedRequest.Headers.GetValues("anthropic-version").Should().ContainSingle().Which.Should().Be("2023-06-01");

        capturedBody.Should().NotBeNull();
        using var jsonDoc = JsonDocument.Parse(capturedBody!);
        var root = jsonDoc.RootElement;
        root.GetProperty("model").GetString().Should().Be("claude-sonnet-5-5");
        root.GetProperty("max_tokens").GetInt32().Should().Be(2048);
        root.GetProperty("system").GetString().Should().Be("My test system prompt");
        var messages = root.GetProperty("messages");
        messages.GetArrayLength().Should().Be(1);
        messages[0].GetProperty("role").GetString().Should().Be("user");
        messages[0].GetProperty("content").GetString().Should().Be("My test user prompt");
    }

    [Fact]
    public async Task SendPromptAsync_WhenStopReasonMaxTokens_LogsWarningAndReturnsText()
    {
        // Arrange
        var responsePayload = new ClaudeResponseDto
        {
            Id = "msg_truncated",
            StopReason = "max_tokens",
            Content = [new ClaudeContentDto { Type = "text", Text = "Partial text before cutoff" }]
        };

        var handler = new FakeHttpMessageHandler((_, _) =>
            Task.FromResult(new HttpResponseMessage(HttpStatusCode.OK)
            {
                Content = JsonContent.Create(responsePayload)
            }));

        var service = CreateService(handler);

        // Act
        var result = await service.SendPromptAsync("Generate long text");

        // Assert
        result.Should().Be("Partial text before cutoff");
        _mockLogger.Verify(
            x => x.Log(
                LogLevel.Warning,
                It.IsAny<EventId>(),
                It.Is<It.IsAnyType>((v, t) => v.ToString()!.Contains("max_tokens")),
                It.IsAny<Exception?>(),
                It.IsAny<Func<It.IsAnyType, Exception?, string>>()),
            Times.Once);
    }

    private class FakeHttpMessageHandler : HttpMessageHandler
    {
        private readonly Func<HttpRequestMessage, CancellationToken, Task<HttpResponseMessage>> _handler;

        public FakeHttpMessageHandler(Func<HttpRequestMessage, CancellationToken, Task<HttpResponseMessage>> handler)
        {
            _handler = handler;
        }

        protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            return _handler(request, cancellationToken);
        }
    }
}
