using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Interfaces;

namespace SmartMacro.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class OptimizationsController : ControllerBase
{
    private readonly IOptimizationService _optimizationService;

    public OptimizationsController(IOptimizationService optimizationService)
    {
        _optimizationService = optimizationService;
    }

    [HttpPost("generate-plan")]
    public async Task<ActionResult<OptimizationResultDto>> GeneratePlan(
        [FromBody] OptimizationRequestDto request)
    {
        // AuthService issues JWT with Sub claim mapping to ClaimTypes.NameIdentifier
        var userIdString = User.FindFirstValue(ClaimTypes.NameIdentifier);
        
        if (string.IsNullOrEmpty(userIdString) || !long.TryParse(userIdString, out var userId))
        {
            return Unauthorized();
        }

        var result = await _optimizationService.GenerateMealPlanAsync(userId, request);
        return Ok(result);
    }
}
