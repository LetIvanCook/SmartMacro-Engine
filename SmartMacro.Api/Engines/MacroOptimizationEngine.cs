using Google.OrTools.LinearSolver;
using SmartMacro.Api.DTOs;

namespace SmartMacro.Api.Engines;

/// <summary>
/// Triển khai bài toán Tối ưu hóa có ràng buộc (Constraint Optimization)
/// sử dụng Google OR-Tools GLOP solver (Linear Programming).
///
/// Bài toán:
///   - Biến quyết định: grams[i] = số gam cần ăn từ thực phẩm thứ i.
///   - Ràng buộc: tổng macro (Protein, Carbs, Fat) nằm trong biên độ ±5% mục tiêu.
///   - Hàm mục tiêu: Minimize |tổng Kcal tính toán - TargetKcal|.
///
/// Solver trả về phân bổ gam tối ưu cho từng thực phẩm, hoặc Infeasible
/// nếu kho hiện tại không đủ nguyên liệu để đáp ứng ràng buộc.
/// </summary>
public class MacroOptimizationEngine : IMacroOptimizationEngine
{
    /// <summary>
    /// Biên độ sai số chấp nhận được cho các ràng buộc macro (±5%).
    /// </summary>
    private const double Tolerance = 0.05;

    /// <summary>
    /// Ngưỡng tối thiểu (gam) để coi một thực phẩm là "được chọn".
    /// Các giá trị nhỏ hơn bị coi là noise số học và bị loại bỏ.
    /// </summary>
    private const double MinGramsThreshold = 0.5;

    /// <inheritdoc />
    public OptimizationResult CalculateOptimalMeal(
        DailyTargetDto target,
        List<InventoryItemDto> availableInventory)
    {
        // ──────────────────────────────────────────────────────────────
        // Guard clauses
        // ──────────────────────────────────────────────────────────────
        if (target is null)
            return Fail("Target macro không được null.");

        if (availableInventory is null || availableInventory.Count == 0)
            return Fail("Kho thực phẩm trống — không có nguyên liệu nào để tối ưu.");

        try
        {
            return SolveLinearProgram(target, availableInventory);
        }
        catch (Exception ex)
        {
            return Fail($"Lỗi runtime khi giải bài toán LP: {ex.Message}");
        }
    }

    /// <summary>
    /// Xây dựng và giải mô hình Quy hoạch tuyến tính (LP) bằng GLOP solver.
    /// </summary>
    private OptimizationResult SolveLinearProgram(
        DailyTargetDto target,
        List<InventoryItemDto> inventory)
    {
        // ──────────────────────────────────────────────────────────────
        // 1. Khởi tạo Solver
        // ──────────────────────────────────────────────────────────────
        // GLOP = Google Linear Optimization Package — chuyên dùng cho LP liên tục.
        Solver solver = Solver.CreateSolver("GLOP");
        if (solver is null)
            return Fail("Không thể khởi tạo GLOP solver. Kiểm tra cài đặt Google.OrTools.");

        int n = inventory.Count;

        // ──────────────────────────────────────────────────────────────
        // 2. Định nghĩa Biến Quyết định (Decision Variables)
        // ──────────────────────────────────────────────────────────────
        // grams[i] = số gam sử dụng từ thực phẩm thứ i.
        // Ràng buộc: 0 <= grams[i] <= QuantityGrams (tồn kho thực tế).
        var grams = new Variable[n];
        for (int i = 0; i < n; i++)
        {
            grams[i] = solver.MakeNumVar(
                0.0,
                (double)inventory[i].QuantityGrams,
                $"grams_{inventory[i].FoodId}");
        }

        // ──────────────────────────────────────────────────────────────
        // 3. Định nghĩa các Ràng buộc Macro (±5% Tolerance)
        // ──────────────────────────────────────────────────────────────

        // ── 3a. Ràng buộc PROTEIN ───────────────────────────────────
        // Σ (grams[i] × ProteinGPer100g[i] / 100) ∈ [target × 0.95, target × 1.05]
        AddMacroConstraint(
            solver, grams, inventory,
            item => (double)item.ProteinGPer100g,
            (double)target.TargetProteinG,
            "protein");

        // ── 3b. Ràng buộc CARBS ─────────────────────────────────────
        // Σ (grams[i] × CarbsGPer100g[i] / 100) ∈ [target × 0.95, target × 1.05]
        AddMacroConstraint(
            solver, grams, inventory,
            item => (double)item.CarbsGPer100g,
            (double)target.TargetCarbsG,
            "carbs");

        // ── 3c. Ràng buộc FAT ───────────────────────────────────────
        // Σ (grams[i] × FatGPer100g[i] / 100) ∈ [target × 0.95, target × 1.05]
        AddMacroConstraint(
            solver, grams, inventory,
            item => (double)item.FatGPer100g,
            (double)target.TargetFatG,
            "fat");

        // ──────────────────────────────────────────────────────────────
        // 4. Hàm Mục tiêu: Minimize |totalKcal - targetKcal|
        // ──────────────────────────────────────────────────────────────
        // LP không hỗ trợ absolute value trực tiếp. Ta dùng kỹ thuật
        // biến phụ (auxiliary variable) để tuyến tính hóa:
        //   deviation >= totalKcal - targetKcal
        //   deviation >= -(totalKcal - targetKcal)
        //   Minimize deviation
        // ──────────────────────────────────────────────────────────────

        double targetKcal = (double)target.TargetKcal;

        // Biến phụ đại diện cho |sai lệch Kcal|
        Variable deviation = solver.MakeNumVar(0.0, double.PositiveInfinity, "kcal_deviation");

        // Constraint: deviation >= Σ(grams[i] * kcalPer100g[i] / 100) - targetKcal
        //           → Σ(grams[i] * kcalPer100g[i] / 100) - deviation <= targetKcal
        Constraint kcalUpperDev = solver.MakeConstraint(double.NegativeInfinity, targetKcal, "kcal_upper_dev");
        for (int i = 0; i < n; i++)
        {
            kcalUpperDev.SetCoefficient(grams[i], (double)inventory[i].KcalPer100g / 100.0);
        }
        kcalUpperDev.SetCoefficient(deviation, -1.0);

        // Constraint: deviation >= -(Σ(grams[i] * kcalPer100g[i] / 100) - targetKcal)
        //           → Σ(grams[i] * kcalPer100g[i] / 100) + deviation >= targetKcal
        Constraint kcalLowerDev = solver.MakeConstraint(targetKcal, double.PositiveInfinity, "kcal_lower_dev");
        for (int i = 0; i < n; i++)
        {
            kcalLowerDev.SetCoefficient(grams[i], (double)inventory[i].KcalPer100g / 100.0);
        }
        kcalLowerDev.SetCoefficient(deviation, 1.0);

        // Objective: Minimize deviation
        Objective objective = solver.Objective();
        objective.SetCoefficient(deviation, 1.0);
        objective.SetMinimization();

        // ──────────────────────────────────────────────────────────────
        // 5. Giải bài toán
        // ──────────────────────────────────────────────────────────────
        Solver.ResultStatus status = solver.Solve();

        if (status != Solver.ResultStatus.OPTIMAL && status != Solver.ResultStatus.FEASIBLE)
        {
            return Fail(
                $"Solver trả về trạng thái: {status}. " +
                "Không tìm được nghiệm khả thi — kho thực phẩm hiện tại không đủ " +
                "để đáp ứng mục tiêu macro trong biên độ ±5%.");
        }

        // ──────────────────────────────────────────────────────────────
        // 6. Trích xuất kết quả
        // ──────────────────────────────────────────────────────────────
        var result = new OptimizationResult
        {
            IsSuccessful = true,
            Message = status == Solver.ResultStatus.OPTIMAL
                ? "Tìm được nghiệm tối ưu (OPTIMAL)."
                : "Tìm được nghiệm khả thi (FEASIBLE) nhưng có thể chưa phải tối ưu nhất."
        };

        for (int i = 0; i < n; i++)
        {
            double gramsValue = grams[i].SolutionValue();

            // Bỏ qua thực phẩm có số gam quá nhỏ (noise số học từ solver)
            if (gramsValue < MinGramsThreshold)
                continue;

            decimal calculatedGrams = Math.Round((decimal)gramsValue, 2);

            result.Items.Add(new OptimizedFoodItem
            {
                FoodId = inventory[i].FoodId,
                FoodName = inventory[i].FoodName,
                CalculatedGrams = calculatedGrams
            });

            // Tính tổng macro thực tế dựa trên nghiệm
            result.TotalKcal += calculatedGrams * inventory[i].KcalPer100g / 100m;
            result.TotalProtein += calculatedGrams * inventory[i].ProteinGPer100g / 100m;
            result.TotalCarbs += calculatedGrams * inventory[i].CarbsGPer100g / 100m;
            result.TotalFat += calculatedGrams * inventory[i].FatGPer100g / 100m;
        }

        // Làm tròn tổng macro đến 2 chữ số thập phân
        result.TotalKcal = Math.Round(result.TotalKcal, 2);
        result.TotalProtein = Math.Round(result.TotalProtein, 2);
        result.TotalCarbs = Math.Round(result.TotalCarbs, 2);
        result.TotalFat = Math.Round(result.TotalFat, 2);

        return result;
    }

    /// <summary>
    /// Thêm một cặp ràng buộc (lower bound + upper bound) cho một loại macro.
    /// Biên độ: targetValue × (1 - Tolerance) ≤ Σ(grams[i] × macroPer100g[i] / 100) ≤ targetValue × (1 + Tolerance)
    /// </summary>
    private static void AddMacroConstraint(
        Solver solver,
        Variable[] grams,
        List<InventoryItemDto> inventory,
        Func<InventoryItemDto, double> getMacroPer100g,
        double targetValue,
        string macroName)
    {
        double lowerBound = targetValue * (1.0 - Tolerance);
        double upperBound = targetValue * (1.0 + Tolerance);

        Constraint constraint = solver.MakeConstraint(lowerBound, upperBound, $"ct_{macroName}");

        for (int i = 0; i < inventory.Count; i++)
        {
            // Hệ số = macroPer100g / 100 (chuyển đổi từ "per 100g" sang "per 1g")
            double coefficient = getMacroPer100g(inventory[i]) / 100.0;
            constraint.SetCoefficient(grams[i], coefficient);
        }
    }

    /// <summary>Helper tạo kết quả thất bại với message mô tả.</summary>
    private static OptimizationResult Fail(string message) => new()
    {
        IsSuccessful = false,
        Message = message
    };
}
