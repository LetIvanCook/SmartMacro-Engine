namespace SmartMacro.Api.Interfaces;

public interface ITargetUrlValidator
{
    Task ValidateAsync(string url, CancellationToken cancellationToken = default);
    bool IsHostAllowed(string host);
}
