using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using SmartMacro.Api.Exceptions;

namespace SmartMacro.Api.Middleware;

public class GlobalExceptionHandler : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        var (statusCode, title, detail) = exception switch
        {
            ArgumentException => (StatusCodes.Status400BadRequest, "Bad Request", exception.Message),
            NotFoundException => (StatusCodes.Status404NotFound, "Resource Not Found", exception.Message),
            EmptyInventoryException => (StatusCodes.Status422UnprocessableEntity, "Unprocessable Entity", exception.Message),
            ConflictException => (StatusCodes.Status409Conflict, "Conflict", exception.Message),
            _ => (StatusCodes.Status500InternalServerError, "Internal Server Error", "An unexpected error occurred.")
        };

        // Nếu là lỗi 500 thì để fallback cho default handler xử lý (có thể log lỗi), 
        // hoặc ta có thể xử lý luôn tại đây. Theo yêu cầu: "fallback exception khác → 500 ProblemDetails mặc định của framework."
        // Việc return false sẽ nhường quyền cho các IExceptionHandler khác hoặc middleware mặc định.
        if (statusCode == StatusCodes.Status500InternalServerError)
        {
            return false;
        }

        httpContext.Response.StatusCode = statusCode;

        var problemDetails = new ProblemDetails
        {
            Status = statusCode,
            Title = title,
            Detail = detail
        };

        await httpContext.Response.WriteAsJsonAsync(problemDetails, cancellationToken);

        return true;
    }
}
