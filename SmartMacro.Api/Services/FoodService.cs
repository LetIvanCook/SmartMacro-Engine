using AutoMapper;
using AutoMapper.QueryableExtensions;
using Microsoft.EntityFrameworkCore;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Models;

namespace SmartMacro.Api.Services;

public class FoodService : IFoodService
{
    private readonly SmartMacroDbContext _db;
    private readonly IMapper _mapper;

    public FoodService(SmartMacroDbContext db, IMapper mapper)
    {
        _db = db;
        _mapper = mapper;
    }

    /// <inheritdoc />
    public async Task<PagedResult<FoodResponseDto>> SearchFoodsAsync(FoodSearchRequestDto request)
    {
        var query = _db.Foods.AsQueryable();

        // Filter theo keyword — partial match, case-insensitive (SQL Server mặc định CI)
        if (!string.IsNullOrWhiteSpace(request.Keyword))
        {
            var keyword = request.Keyword.Trim();
            query = query.Where(f => f.FoodName.Contains(keyword));
        }

        // Filter theo CategoryId
        if (request.CategoryId.HasValue)
        {
            query = query.Where(f => f.CategoryId == request.CategoryId.Value);
        }

        var totalCount = await query.CountAsync();

        // ProjectTo để EF Core sinh SQL SELECT chỉ lấy cột cần thiết + LEFT JOIN food_categories
        var items = await query
            .OrderBy(f => f.FoodName)
            .Skip((request.Page - 1) * request.PageSize)
            .Take(request.PageSize)
            .ProjectTo<FoodResponseDto>(_mapper.ConfigurationProvider)
            .ToListAsync();

        return new PagedResult<FoodResponseDto>
        {
            Items = items,
            TotalCount = totalCount,
            Page = request.Page,
            PageSize = request.PageSize
        };
    }

    /// <inheritdoc />
    public async Task<FoodResponseDto> GetFoodByIdAsync(long id)
    {
        var food = await _db.Foods
            .Where(f => f.FoodId == id)
            .ProjectTo<FoodResponseDto>(_mapper.ConfigurationProvider)
            .FirstOrDefaultAsync();

        if (food is null)
            throw new NotFoundException($"Thực phẩm với ID {id} không tồn tại.");

        return food;
    }

    /// <inheritdoc />
    public async Task<FoodResponseDto> CreateFoodAsync(CreateFoodRequestDto request)
    {
        // Validate FoodCategoryId nếu có
        await ValidateCategoryExistsAsync(request.CategoryId);

        var food = new Food
        {
            FoodName = request.FoodName,
            CategoryId = request.CategoryId,
            KcalPer100g = request.KcalPer100g,
            ProteinGPer100g = request.ProteinGPer100g,
            CarbsGPer100g = request.CarbsGPer100g,
            FatGPer100g = request.FatGPer100g,
            FiberGPer100g = request.FiberGPer100g,
            IsVerified = false,
            Source = "user_submitted",
            CreatedAt = DateTime.UtcNow
        };

        _db.Foods.Add(food);
        await _db.SaveChangesAsync();

        // Reload bằng ProjectTo để trả về DTO đầy đủ (bao gồm CategoryName)
        return await GetFoodByIdAsync(food.FoodId);
    }

    /// <inheritdoc />
    public async Task<FoodResponseDto> UpdateFoodAsync(long id, UpdateFoodRequestDto request)
    {
        var food = await _db.Foods.FindAsync(id);
        if (food is null)
            throw new NotFoundException($"Thực phẩm với ID {id} không tồn tại.");

        // Validate FoodCategoryId nếu có
        await ValidateCategoryExistsAsync(request.CategoryId);

        food.FoodName = request.FoodName;
        food.CategoryId = request.CategoryId;
        food.KcalPer100g = request.KcalPer100g;
        food.ProteinGPer100g = request.ProteinGPer100g;
        food.CarbsGPer100g = request.CarbsGPer100g;
        food.FatGPer100g = request.FatGPer100g;
        food.FiberGPer100g = request.FiberGPer100g;

        await _db.SaveChangesAsync();

        // Reload bằng ProjectTo để trả về DTO đầy đủ (bao gồm CategoryName mới)
        return await GetFoodByIdAsync(food.FoodId);
    }

    /// <inheritdoc />
    public async Task DeleteFoodAsync(long id)
    {
        var food = await _db.Foods.FindAsync(id);
        if (food is null)
            throw new NotFoundException($"Thực phẩm với ID {id} không tồn tại.");

        _db.Foods.Remove(food);
        await _db.SaveChangesAsync();
    }

    /// <summary>
    /// Validate rằng CategoryId tồn tại trong DB (nếu được cung cấp).
    /// Throw NotFoundException nếu category không tồn tại.
    /// </summary>
    private async Task ValidateCategoryExistsAsync(short? categoryId)
    {
        if (categoryId.HasValue)
        {
            var exists = await _db.FoodCategories
                .AnyAsync(c => c.CategoryId == categoryId.Value);

            if (!exists)
                throw new NotFoundException($"Danh mục thực phẩm với ID {categoryId} không tồn tại.");
        }
    }
}
