using AutoMapper;
using AutoMapper.QueryableExtensions;
using Microsoft.EntityFrameworkCore;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Models;

namespace SmartMacro.Api.Services;

public class InventoryService : IInventoryService
{
    private readonly SmartMacroDbContext _db;
    private readonly IMapper _mapper;

    public InventoryService(SmartMacroDbContext db, IMapper mapper)
    {
        _db = db;
        _mapper = mapper;
    }

    public async Task<List<InventoryItemResponseDto>> GetMyInventoryAsync(long userId)
    {
        return await _db.UserFoodInventories
            .Where(i => i.UserId == userId)
            .ProjectTo<InventoryItemResponseDto>(_mapper.ConfigurationProvider)
            .ToListAsync();
    }

    public async Task<InventoryItemResponseDto> AddItemAsync(long userId, CreateInventoryItemRequestDto request)
    {
        if (request.QuantityGrams <= 0)
            throw new ArgumentException("Số lượng phải lớn hơn 0.");

        var foodExists = await _db.Foods.AnyAsync(f => f.FoodId == request.FoodId);
        if (!foodExists)
            throw new NotFoundException($"Thực phẩm với ID {request.FoodId} không tồn tại.");

        // Check for existing item without ExpiryDate to merge, respecting unique constraint on (UserId, FoodId, ExpiryDate)
        var existingItem = await _db.UserFoodInventories
            .FirstOrDefaultAsync(i => i.UserId == userId && i.FoodId == request.FoodId && i.ExpiryDate == null);

        long inventoryIdToReturn;

        if (existingItem != null)
        {
            existingItem.QuantityGrams += request.QuantityGrams;
            existingItem.UpdatedAt = DateTime.UtcNow;
            inventoryIdToReturn = existingItem.InventoryId;
        }
        else
        {
            var newItem = new UserFoodInventory
            {
                UserId = userId,
                FoodId = request.FoodId,
                QuantityGrams = request.QuantityGrams,
                UpdatedAt = DateTime.UtcNow
            };
            _db.UserFoodInventories.Add(newItem);
            await _db.SaveChangesAsync(); // Cần save để lấy ID trước khi return
            inventoryIdToReturn = newItem.InventoryId;
        }

        await _db.SaveChangesAsync();

        // Tải lại bằng ProjectTo để trả về đủ FoodName và Macro
        return await GetInventoryItemDtoAsync(userId, inventoryIdToReturn);
    }

    public async Task<InventoryItemResponseDto> UpdateItemAsync(long userId, long itemId, UpdateInventoryItemRequestDto request)
    {
        if (request.QuantityGrams <= 0)
            throw new ArgumentException("Số lượng phải lớn hơn 0.");

        var item = await _db.UserFoodInventories
            .FirstOrDefaultAsync(i => i.InventoryId == itemId && i.UserId == userId);

        if (item == null)
            throw new NotFoundException($"Mục kho với ID {itemId} không tồn tại hoặc không thuộc về người dùng hiện tại.");

        item.QuantityGrams = request.QuantityGrams;
        item.UpdatedAt = DateTime.UtcNow;

        await _db.SaveChangesAsync();

        return await GetInventoryItemDtoAsync(userId, itemId);
    }

    public async Task DeleteItemAsync(long userId, long itemId)
    {
        var item = await _db.UserFoodInventories
            .FirstOrDefaultAsync(i => i.InventoryId == itemId && i.UserId == userId);

        if (item == null)
            throw new NotFoundException($"Mục kho với ID {itemId} không tồn tại hoặc không thuộc về người dùng hiện tại.");

        _db.UserFoodInventories.Remove(item);
        await _db.SaveChangesAsync();
    }

    private async Task<InventoryItemResponseDto> GetInventoryItemDtoAsync(long userId, long inventoryId)
    {
        return await _db.UserFoodInventories
            .Where(i => i.InventoryId == inventoryId && i.UserId == userId)
            .ProjectTo<InventoryItemResponseDto>(_mapper.ConfigurationProvider)
            .FirstAsync();
    }
}
