using System.Net;

namespace SmartMacro.Api.Exceptions;

public class AnthropicApiException : Exception
{
    public HttpStatusCode StatusCode { get; }
    public string? ErrorType { get; }

    public AnthropicApiException(HttpStatusCode statusCode, string message, string? errorType = null, Exception? innerException = null)
        : base(message, innerException)
    {
        StatusCode = statusCode;
        ErrorType = errorType;
    }
}
