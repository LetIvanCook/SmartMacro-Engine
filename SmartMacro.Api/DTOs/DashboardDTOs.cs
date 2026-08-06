namespace SmartMacro.Api.DTOs;

/// <summary>
/// Phẳng hóa dữ liệu từ UserFoodInventory + Food thành một DTO duy nhất.
/// Mỗi item đại diện cho một dòng trong kho thực phẩm đang còn hàng.
/// </summary>
public class InventoryItemResponseDto
{
    public long InventoryId { get; set; }

    /// <summary>ID thực phẩm — cần cho Engine để định danh kết quả tối ưu.</summary>
    public long FoodId { get; set; }

    /// <summary>Tên thực phẩm — được project trực tiếp từ bảng Food qua navigation property.</summary>
    public string FoodName { get; set; } = null!;

    public decimal QuantityGrams { get; set; }
    public DateOnly? ExpiryDate { get; set; }
    public decimal KcalPer100g { get; set; }
    public decimal ProteinGPer100g { get; set; }
    public decimal CarbsGPer100g { get; set; }
    public decimal FatGPer100g { get; set; }
}

/// <summary>
/// Mục tiêu macro hàng ngày đã được tính toán trước.
/// Chỉ chứa 4 con số cần thiết cho Dashboard — không expose TargetId hay FK.
/// </summary>
public class DailyTargetDto
{
    public decimal TargetKcal { get; set; }
    public decimal TargetProteinG { get; set; }
    public decimal TargetCarbsG { get; set; }
    public decimal TargetFatG { get; set; }
}

/// <summary>
/// Composite DTO (Chunky API Pattern).
/// Gom thông tin User + Mục tiêu hôm nay + Kho thực phẩm vào MỘT response duy nhất,
/// giúp client chỉ cần GỌI MỘT LẦN API để render toàn bộ Dashboard.
/// </summary>
public class UserDashboardResponseDto
{
    public long UserId { get; set; }
    public string? FullName { get; set; }
    public string GoalType { get; set; } = null!;

    /// <summary>Mục tiêu macro của ngày hôm nay. Null nếu chưa được tính.</summary>
    public DailyTargetDto? TodayTarget { get; set; }

    /// <summary>Danh sách thực phẩm trong kho còn số lượng > 0.</summary>
    public List<InventoryItemResponseDto> AvailableInventory { get; set; } = new();
}
