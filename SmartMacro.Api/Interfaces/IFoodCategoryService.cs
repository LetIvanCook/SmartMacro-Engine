using SmartMacro.Api.DTOs;

namespace SmartMacro.Api.Interfaces;

public interface IFoodCategoryService
{
    Task<List<FoodCategoryResponseDto>> GetAllCategoriesAsync();
    Task<FoodCategoryResponseDto> CreateCategoryAsync(CreateFoodCategoryRequestDto request);
}
