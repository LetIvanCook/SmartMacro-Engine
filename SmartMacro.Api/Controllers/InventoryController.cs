using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Interfaces;
using System.Security.Claims;

namespace SmartMacro.Api.Controllers;

[ApiController]
[Route("api/inventory")]
[Authorize]
public class InventoryController : ControllerBase
{
    private readonly IInventoryService _inventoryService;

    public InventoryController(IInventoryService inventoryService)
    {
        _inventoryService = inventoryService;
    }

    private long GetUserId()
    {
        var userIdString = User.FindFirstValue(ClaimTypes.NameIdentifier);
        if (string.IsNullOrEmpty(userIdString) || !long.TryParse(userIdString, out var userId))
        {
            throw new UnauthorizedAccessException("Người dùng chưa được xác thực đúng cách.");
        }
        return userId;
    }

    [HttpGet]
    public async Task<ActionResult<List<InventoryItemResponseDto>>> GetMyInventory()
    {
        var userId = GetUserId();
        var result = await _inventoryService.GetMyInventoryAsync(userId);
        return Ok(result);
    }

    [HttpPost]
    public async Task<ActionResult<InventoryItemResponseDto>> AddItem([FromBody] CreateInventoryItemRequestDto request)
    {
        var userId = GetUserId();
        var result = await _inventoryService.AddItemAsync(userId, request);
        return CreatedAtAction(nameof(GetMyInventory), new { id = result.InventoryId }, result);
    }

    [HttpPut("{itemId}")]
    public async Task<ActionResult<InventoryItemResponseDto>> UpdateItem(long itemId, [FromBody] UpdateInventoryItemRequestDto request)
    {
        var userId = GetUserId();
        var result = await _inventoryService.UpdateItemAsync(userId, itemId, request);
        return Ok(result);
    }

    [HttpDelete("{itemId}")]
    public async Task<IActionResult> DeleteItem(long itemId)
    {
        var userId = GetUserId();
        await _inventoryService.DeleteItemAsync(userId, itemId);
        return NoContent();
    }
}
