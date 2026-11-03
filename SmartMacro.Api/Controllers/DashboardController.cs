using System.Security.Claims;
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
    /// Lấy dữ liệu tổng hợp Dashboard của người dùng hiện tại (dựa trên JWT token).
    /// </summary>
    [HttpGet("summary")]
    public async Task<IActionResult> GetMySummary()
    {
        var userIdString = User.FindFirstValue(ClaimTypes.NameIdentifier);
        if (string.IsNullOrEmpty(userIdString) || !long.TryParse(userIdString, out var userId))
        {
            return Unauthorized();
        }

        var result = await _dashboardService.GetUserDashboardAsync(userId);
        if (result is null)
            return NotFound(new { Message = $"User with ID {userId} not found." });

        return Ok(result);
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
