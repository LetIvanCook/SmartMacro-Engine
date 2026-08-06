using System;
using System.Collections.Generic;

namespace SmartMacro.Api.Models;

public partial class UserFoodInventory
{
    public long InventoryId { get; set; }

    public long UserId { get; set; }

    public long FoodId { get; set; }

    public decimal QuantityGrams { get; set; }

    public DateOnly? ExpiryDate { get; set; }

    public string? UnitNote { get; set; }

    public DateTime UpdatedAt { get; set; }

    public virtual Food Food { get; set; } = null!;

    public virtual ICollection<MealLog> MealLogs { get; set; } = new List<MealLog>();

    public virtual User User { get; set; } = null!;
}
