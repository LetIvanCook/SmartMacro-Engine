using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Interfaces;

namespace SmartMacro.Api.Controllers;

[ApiController]
[Route("api/food-categories")]
[Authorize]
public class FoodCategoriesController : ControllerBase
{
    private readonly IFoodCategoryService _foodCategoryService;

    public FoodCategoriesController(IFoodCategoryService foodCategoryService)
    {
        _foodCategoryService = foodCategoryService;
    }

    [HttpGet]
    public async Task<ActionResult<List<FoodCategoryResponseDto>>> GetAll()
    {
        var categories = await _foodCategoryService.GetAllCategoriesAsync();
        return Ok(categories);
    }

    [HttpPost]
    public async Task<ActionResult<FoodCategoryResponseDto>> Create(
        [FromBody] CreateFoodCategoryRequestDto request)
    {
        var category = await _foodCategoryService.CreateCategoryAsync(request);
        return CreatedAtAction(nameof(GetAll), null, category);
    }
    [HttpPut("{id}")]
    public async Task<ActionResult<FoodCategoryResponseDto>> Update(short id, [FromBody] UpdateFoodCategoryRequestDto request)
    {
        var category = await _foodCategoryService.UpdateCategoryAsync(id, request);
        return Ok(category);
    }

    [HttpDelete("{id}")]
    public async Task<ActionResult> Delete(short id)
    {
        await _foodCategoryService.DeleteCategoryAsync(id);
        return NoContent();
    }
}
