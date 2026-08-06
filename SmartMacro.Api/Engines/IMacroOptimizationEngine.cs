using SmartMacro.Api.DTOs;

namespace SmartMacro.Api.Engines;

/// <summary>
/// Contract cho Macro Optimization Engine.
/// Nhận mục tiêu macro ngày + danh sách kho thực phẩm,
/// trả về phân bổ gam tối ưu cho từng loại thực phẩm.
/// </summary>
public interface IMacroOptimizationEngine
{
    /// <summary>
    /// Giải bài toán Quy hoạch tuyến tính (LP) để phân bổ khẩu phần ăn tối ưu.
    /// </summary>
    /// <param name="target">Mục tiêu macro hàng ngày (Kcal, Protein, Carbs, Fat).</param>
    /// <param name="availableInventory">Danh sách thực phẩm trong kho còn hàng (quantity > 0).</param>
    /// <returns>
    /// Kết quả tối ưu hóa chứa số gam cụ thể cho từng thực phẩm.
    /// <see cref="OptimizationResult.IsSuccessful"/> = false nếu không tìm được nghiệm khả thi.
    /// </returns>
    OptimizationResult CalculateOptimalMeal(
        DailyTargetDto target,
        List<InventoryItemResponseDto> availableInventory);
}
