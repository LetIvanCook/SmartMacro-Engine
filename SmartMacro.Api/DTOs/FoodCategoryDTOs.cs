namespace SmartMacro.Api.DTOs;

public class FoodCategoryResponseDto
{
    public short CategoryId { get; set; }
    public string CategoryName { get; set; } = null!;
}

public class CreateFoodCategoryRequestDto
{
    public string CategoryName { get; set; } = null!;
}
