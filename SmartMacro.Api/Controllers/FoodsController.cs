using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Interfaces;

namespace SmartMacro.Api.Controllers;

[ApiController]
[Route("api/foods")]
[Authorize]
public class FoodsController : ControllerBase
{
    private readonly IFoodService _foodService;

    public FoodsController(IFoodService foodService)
    {
        _foodService = foodService;
    }

    [HttpGet]
    public async Task<ActionResult<PagedResult<FoodResponseDto>>> Search(
        [FromQuery] FoodSearchRequestDto request)
    {
        var result = await _foodService.SearchFoodsAsync(request);
        return Ok(result);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<FoodResponseDto>> GetById(long id)
    {
        var food = await _foodService.GetFoodByIdAsync(id);
        return Ok(food);
    }

    [HttpPost]
    public async Task<ActionResult<FoodResponseDto>> Create(
        [FromBody] CreateFoodRequestDto request)
    {
        var food = await _foodService.CreateFoodAsync(request);
        return CreatedAtAction(nameof(GetById), new { id = food.FoodId }, food);
    }

    [HttpPut("{id}")]
    public async Task<ActionResult<FoodResponseDto>> Update(
        long id, [FromBody] UpdateFoodRequestDto request)
    {
        var food = await _foodService.UpdateFoodAsync(id, request);
        return Ok(food);
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(long id)
    {
        await _foodService.DeleteFoodAsync(id);
        return NoContent();
    }
}
