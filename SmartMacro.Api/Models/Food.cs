using System;
using System.Collections.Generic;

namespace SmartMacro.Api.Models;

public partial class Food
{
    public long FoodId { get; set; }

    public short? CategoryId { get; set; }

    public string FoodName { get; set; } = null!;

    public string? Barcode { get; set; }

    public decimal KcalPer100g { get; set; }

    public decimal ProteinGPer100g { get; set; }

    public decimal CarbsGPer100g { get; set; }

    public decimal FatGPer100g { get; set; }

    public decimal? FiberGPer100g { get; set; }

    public bool IsVerified { get; set; }

    public string Source { get; set; } = null!;

    public long? CreatedBy { get; set; }

    public DateTime CreatedAt { get; set; }

    public virtual FoodCategory? Category { get; set; }

    public virtual User? CreatedByNavigation { get; set; }

    public virtual ICollection<MealLog> MealLogs { get; set; } = new List<MealLog>();

    public virtual ICollection<UserFoodInventory> UserFoodInventories { get; set; } = new List<UserFoodInventory>();
}
