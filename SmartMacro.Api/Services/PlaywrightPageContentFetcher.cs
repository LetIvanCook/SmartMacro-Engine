using System.Text.RegularExpressions;
using Microsoft.Extensions.Options;
using Microsoft.Playwright;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Options;

namespace SmartMacro.Api.Services;

public class PlaywrightPageContentFetcher : IPageContentFetcher, IAsyncDisposable
{
    private readonly ResearchOptions _options;
    private readonly ITargetUrlValidator _urlValidator;
    private readonly ILogger<PlaywrightPageContentFetcher> _logger;
    private readonly SemaphoreSlim _browserSemaphore;
    private readonly SemaphoreSlim _initLock = new(1, 1);
    private IPlaywright? _playwright;
    private IBrowser? _browser;
    private bool _disposed;

    public PlaywrightPageContentFetcher(
        IOptions<ResearchOptions> options,
        ITargetUrlValidator urlValidator,
        ILogger<PlaywrightPageContentFetcher> logger)
    {
        _options = options.Value;
        _urlValidator = urlValidator;
        _logger = logger;
        _browserSemaphore = new SemaphoreSlim(_options.MaxConcurrentBrowsers, _options.MaxConcurrentBrowsers);
    }

    private async Task<IBrowser> EnsureBrowserAsync()
    {
        if (_browser != null)
        {
            return _browser;
        }

        await _initLock.WaitAsync();
        try
        {
            if (_browser == null)
            {
                _logger.LogInformation("Initializing Playwright and launching headless Chromium instance...");
                _playwright = await Playwright.CreateAsync();
                _browser = await _playwright.Chromium.LaunchAsync(new BrowserTypeLaunchOptions
                {
                    Headless = true
                });
            }
            return _browser;
        }
        finally
        {
            _initLock.Release();
        }
    }

    public async Task<string> FetchTextAsync(string url, CancellationToken cancellationToken = default)
    {
        await _browserSemaphore.WaitAsync(cancellationToken);
        try
        {
            var browser = await EnsureBrowserAsync();

            await using var context = await browser.NewContextAsync(new BrowserNewContextOptions
            {
                UserAgent = "SmartMacroResearchBot/1.0"
            });

            var page = await context.NewPageAsync();

            await page.RouteAsync("**/*", async route =>
            {
                var requestUrl = route.Request.Url;
                if (Uri.TryCreate(requestUrl, UriKind.Absolute, out var uri))
                {
                    if (route.Request.ResourceType == "document" && !_urlValidator.IsHostAllowed(uri.Host))
                    {
                        await route.AbortAsync();
                        return;
                    }
                }
                await route.ContinueAsync();
            });

            try
            {
                await page.GotoAsync(url, new PageGotoOptions
                {
                    WaitUntil = WaitUntilState.NetworkIdle,
                    Timeout = _options.NavigationTimeoutSeconds * 1000
                });
            }
            catch (TimeoutException)
            {
                _logger.LogWarning("Navigation to {Url} timed out with NetworkIdle, falling back to DOMContentLoaded.", url);
                await page.GotoAsync(url, new PageGotoOptions
                {
                    WaitUntil = WaitUntilState.DOMContentLoaded,
                    Timeout = _options.NavigationTimeoutSeconds * 1000
                });
            }

            // Post-navigation validation to prevent redirect out of allowlist
            await _urlValidator.ValidateAsync(page.Url, cancellationToken);

            var script = @"() => {
                const elementsToRemove = document.querySelectorAll('script, style, svg, noscript, iframe, nav, footer');
                elementsToRemove.forEach(el => el.remove());
                const main = document.querySelector('main');
                return main ? main.innerText : document.body.innerText;
            }";

            var rawText = await page.EvaluateAsync<string>(script) ?? string.Empty;
            var normalizedText = Regex.Replace(rawText, @"\s+", " ").Trim();

            if (normalizedText.Length > _options.MaxContentChars)
            {
                normalizedText = normalizedText[.._options.MaxContentChars];
            }

            return normalizedText;
        }
        finally
        {
            _browserSemaphore.Release();
        }
    }

    public async ValueTask DisposeAsync()
    {
        if (_disposed)
        {
            return;
        }

        _disposed = true;

        if (_browser != null)
        {
            await _browser.CloseAsync();
            _browser = null;
        }

        _playwright?.Dispose();
        _playwright = null;

        _initLock.Dispose();
        _browserSemaphore.Dispose();

        GC.SuppressFinalize(this);
    }
}
