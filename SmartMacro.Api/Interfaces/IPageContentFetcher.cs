namespace SmartMacro.Api.Interfaces;

public interface IPageContentFetcher
{
    Task<string> FetchTextAsync(string url, CancellationToken cancellationToken = default);
}
