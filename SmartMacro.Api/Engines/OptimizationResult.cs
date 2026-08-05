namespace SmartMacro.Api.Engines;

/// <summary>
/// Kết quả tối ưu hóa từ MacroOptimizationEngine.
/// Chứa trạng thái thành công/thất bại, tổng macro tính toán được,
/// và danh sách chi tiết số gam của từng thực phẩm.
/// </summary>
public class OptimizationResult
{
    /// <summary>
    /// <c>true</c> nếu solver tìm được nghiệm OPTIMAL hoặc FEASIBLE.
    /// <c>false</c> nếu bài toán Infeasible (không thể đáp ứng ràng buộc)
    /// hoặc xảy ra lỗi runtime.
    /// </summary>
    public bool IsSuccessful { get; set; }

    /// <summary>Thông báo mô tả kết quả hoặc lý do thất bại.</summary>
    public string Message { get; set; } = string.Empty;

    // ── Tổng macro tính toán được từ nghiệm tối ưu ─────────────
    public decimal TotalKcal { get; set; }
    public decimal TotalProtein { get; set; }
    public decimal TotalCarbs { get; set; }
    public decimal TotalFat { get; set; }

    /// <summary>
    /// Danh sách chi tiết các thực phẩm được chọn và số gam tối ưu.
    /// Chỉ chứa các item có CalculatedGrams > 0 (đã lọc bỏ item không dùng).
    /// </summary>
    public List<OptimizedFoodItem> Items { get; set; } = new();
}

/// <summary>
/// Một dòng kết quả tối ưu — đại diện cho lượng gam cụ thể
/// cần sử dụng từ một loại thực phẩm trong kho.
/// </summary>
public class OptimizedFoodItem
{
    public long FoodId { get; set; }
    public string FoodName { get; set; } = null!;

    /// <summary>Số gam tối ưu tính bởi LP solver — đã làm tròn 2 chữ số thập phân.</summary>
    public decimal CalculatedGrams { get; set; }
}
