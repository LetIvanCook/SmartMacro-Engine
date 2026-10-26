using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.RateLimiting;
using Microsoft.Extensions.Options;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Options;

namespace SmartMacro.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
[EnableRateLimiting("research")]
public class ResearchController : ControllerBase
{
    private readonly ICompetitorResearchService _researchService;
    private readonly ResearchOptions _options;
    private readonly ILogger<ResearchController> _logger;

    public ResearchController(
        ICompetitorResearchService researchService,
        IOptions<ResearchOptions> options,
        ILogger<ResearchController> logger)
    {
        _researchService = researchService;
        _options = options.Value;
        _logger = logger;
    }

    [HttpPost("analyze")]
    [ProducesResponseType(typeof(CompetitorAnalysisResult), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status400BadRequest)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status403Forbidden)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status429TooManyRequests)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status502BadGateway)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status503ServiceUnavailable)]
    public async Task<IActionResult> AnalyzeCompetitor(
        [FromBody] CompetitorAnalysisRequest request,
        CancellationToken cancellationToken)
    {
        if (!_options.Enabled)
        {
            _logger.LogWarning("Competitor research endpoint requested but Research:Enabled is false.");
            return Problem(
                statusCode: StatusCodes.Status403Forbidden,
                title: "Feature Disabled",
                detail: "Competitor research feature is currently disabled.");
        }

        var result = await _researchService.AnalyzeCompetitorAsync(request, cancellationToken);
        return Ok(result);
    }
}
