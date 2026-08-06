using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Interfaces;
using System.Security.Claims;

namespace SmartMacro.Api.Controllers;

[ApiController]
[Route("api/daily-targets")]
[Authorize]
public class DailyTargetsController : ControllerBase
{
    private readonly IDailyTargetService _dailyTargetService;

    public DailyTargetsController(IDailyTargetService dailyTargetService)
    {
        _dailyTargetService = dailyTargetService;
    }

    private long GetUserId()
    {
        var userIdString = User.FindFirstValue(ClaimTypes.NameIdentifier);
        if (string.IsNullOrEmpty(userIdString) || !long.TryParse(userIdString, out var userId))
            throw new UnauthorizedAccessException("Người dùng chưa được xác thực đúng cách.");
        return userId;
    }

    /// <summary>Lấy toàn bộ daily targets của user hiện tại (sắp xếp mới nhất trước).</summary>
    [HttpGet]
    public async Task<ActionResult<List<DailyTargetResponseDto>>> GetMyTargets()
    {
        var userId = GetUserId();
        var result = await _dailyTargetService.GetMyTargetsAsync(userId);
        return Ok(result);
    }

    /// <summary>Convenience endpoint — lấy target của đúng ngày hôm nay.</summary>
    [HttpGet("today")]
    public async Task<ActionResult<DailyTargetResponseDto>> GetTodayTarget()
    {
        var userId = GetUserId();
        var result = await _dailyTargetService.GetTodayTargetAsync(userId);
        return Ok(result);
    }

    /// <summary>Tạo target mới. Date mặc định là hôm nay nếu không truyền.</summary>
    [HttpPost]
    public async Task<ActionResult<DailyTargetResponseDto>> CreateTarget([FromBody] CreateDailyTargetRequestDto request)
    {
        var userId = GetUserId();
        var result = await _dailyTargetService.CreateTargetAsync(userId, request);
        return CreatedAtAction(nameof(GetMyTargets), new { id = result.Id }, result);
    }

    /// <summary>Cập nhật macro của target đã có (không đổi ngày).</summary>
    [HttpPut("{id}")]
    public async Task<ActionResult<DailyTargetResponseDto>> UpdateTarget(long id, [FromBody] UpdateDailyTargetRequestDto request)
    {
        var userId = GetUserId();
        var result = await _dailyTargetService.UpdateTargetAsync(userId, id, request);
        return Ok(result);
    }

    /// <summary>Xoá target theo ID.</summary>
    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteTarget(long id)
    {
        var userId = GetUserId();
        await _dailyTargetService.DeleteTargetAsync(userId, id);
        return NoContent();
    }
}
