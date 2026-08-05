namespace SmartMacro.Api.DTOs;

public class OptimizationRequestDto
{
    public long? DailyTargetId { get; set; }
    public List<long>? IncludeFoodIds { get; set; }
}

public class OptimizationResultDto
{
    public string SolverStatus { get; set; } = null!;
    public decimal TotalDeviationScore { get; set; }
    public MacroSummaryDto TargetMacros { get; set; } = null!;
    public MacroSummaryDto AchievedMacros { get; set; } = null!;
    public List<AllocatedFoodItemDto> AllocatedItems { get; set; } = new();
}

public class AllocatedFoodItemDto
{
    public long FoodId { get; set; }
    public string FoodName { get; set; } = null!;
    public decimal QuantityGrams { get; set; }
    public decimal Kcal { get; set; }
    public decimal ProteinG { get; set; }
    public decimal CarbsG { get; set; }
    public decimal FatG { get; set; }
}

public class MacroSummaryDto
{
    public decimal Kcal { get; set; }
    public decimal ProteinG { get; set; }
    public decimal CarbsG { get; set; }
    public decimal FatG { get; set; }
}
