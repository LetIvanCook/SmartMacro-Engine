namespace SmartMacro.Api.DTOs;

public class CreateInventoryItemRequestDto
{
    public long FoodId { get; set; }
    public decimal QuantityGrams { get; set; }
}

public class UpdateInventoryItemRequestDto
{
    public decimal QuantityGrams { get; set; }
}
