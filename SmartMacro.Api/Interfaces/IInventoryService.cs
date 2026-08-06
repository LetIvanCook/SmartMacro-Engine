using SmartMacro.Api.DTOs;

namespace SmartMacro.Api.Interfaces;

public interface IInventoryService
{
    Task<List<InventoryItemResponseDto>> GetMyInventoryAsync(long userId);
    Task<InventoryItemResponseDto> AddItemAsync(long userId, CreateInventoryItemRequestDto request);
    Task<InventoryItemResponseDto> UpdateItemAsync(long userId, long itemId, UpdateInventoryItemRequestDto request);
    Task DeleteItemAsync(long userId, long itemId);
}
