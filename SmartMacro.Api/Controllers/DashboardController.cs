using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SmartMacro.Api.Interfaces;

namespace SmartMacro.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class DashboardController : ControllerBase
{
    private readonly IDashboardService _dashboardService;

    public DashboardController(IDashboardService dashboardService)
    {
        _dashboardService = dashboardService;
    }

    /// <summary>
    /// Chunky API — Trả về toàn bộ dữ liệu Dashboard trong MỘT response duy nhất.
    /// Client chỉ cần gọi GET /api/dashboard/{userId}/dashboard để có đủ thông tin render UI.
    /// </summary>
    [HttpGet("{userId}/dashboard")]
    public async Task<IActionResult> GetDashboard(long userId)
    {
        var result = await _dashboardService.GetUserDashboardAsync(userId);

        if (result is null)
            return NotFound(new { Message = $"User with ID {userId} not found." });

        return Ok(result);
    }
}
