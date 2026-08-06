using SmartMacro.Api.DTOs;

namespace SmartMacro.Api.Interfaces;

public interface IFoodService
{
    Task<PagedResult<FoodResponseDto>> SearchFoodsAsync(FoodSearchRequestDto request);
    Task<FoodResponseDto> GetFoodByIdAsync(long id);
    Task<FoodResponseDto> CreateFoodAsync(CreateFoodRequestDto request);
    Task<FoodResponseDto> UpdateFoodAsync(long id, UpdateFoodRequestDto request);
    Task DeleteFoodAsync(long id);
}
