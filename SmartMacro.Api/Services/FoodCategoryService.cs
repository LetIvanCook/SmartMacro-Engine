using AutoMapper;
using AutoMapper.QueryableExtensions;
using Microsoft.EntityFrameworkCore;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Models;

namespace SmartMacro.Api.Services;

public class FoodCategoryService : IFoodCategoryService
{
    private readonly SmartMacroDbContext _db;
    private readonly IMapper _mapper;

    public FoodCategoryService(SmartMacroDbContext db, IMapper mapper)
    {
        _db = db;
        _mapper = mapper;
    }

    /// <inheritdoc />
    public async Task<List<FoodCategoryResponseDto>> GetAllCategoriesAsync()
    {
        return await _db.FoodCategories
            .OrderBy(c => c.CategoryName)
            .ProjectTo<FoodCategoryResponseDto>(_mapper.ConfigurationProvider)
            .ToListAsync();
    }

    /// <inheritdoc />
    public async Task<FoodCategoryResponseDto> CreateCategoryAsync(CreateFoodCategoryRequestDto request)
    {
        // Check trùng tên — DB có unique constraint UQ_food_categories_name,
        // nhưng pre-check để trả lỗi nghiệp vụ rõ ràng thay vì lộ raw SQL exception.
        var nameExists = await _db.FoodCategories
            .AnyAsync(c => c.CategoryName == request.CategoryName);

        if (nameExists)
            throw new ConflictException($"Danh mục '{request.CategoryName}' đã tồn tại.");

        var category = new FoodCategory
        {
            CategoryName = request.CategoryName
        };

        _db.FoodCategories.Add(category);
        await _db.SaveChangesAsync();

        return _mapper.Map<FoodCategoryResponseDto>(category);
    }
}
