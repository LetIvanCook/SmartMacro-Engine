using FluentAssertions;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Engines;

namespace SmartMacro.Tests.Engines;

/// <summary>
/// Bộ Unit Test cho MacroOptimizationEngine (Google OR-Tools GLOP solver).
///
/// Kỹ thuật áp dụng:
///   - Phân vùng tương đương (Equivalence Partitioning):
///       • Valid partition: kho đủ nguyên liệu, target khả thi → OPTIMAL
///       • Invalid partition: kho thiếu, target mâu thuẫn, kho rỗng → INFEASIBLE
///   - Phân tích giá trị biên (Boundary Value Analysis):
///       • Biên dưới tồn kho: chỉ có vừa đủ / thiếu 1 đơn vị
///       • Biên ±5% tolerance: macro tổng phải nằm trong [0.95×target, 1.05×target]
///       • Biên 0: danh sách rỗng, target có giá trị 0
///
/// Không cần Moq — MacroOptimizationEngine là class thuật toán thuần túy,
/// không gọi database hay bất kỳ external dependency nào.
/// </summary>
public class MacroOptimizationEngineTests
{
    private readonly MacroOptimizationEngine _engine = new();

    // ══════════════════════════════════════════════════════════════
    // HELPER: Tạo InventoryItemResponseDto nhanh
    // ══════════════════════════════════════════════════════════════
    private static InventoryItemResponseDto CreateFood(
        long foodId, string name, decimal quantityGrams,
        decimal kcal, decimal protein, decimal carbs, decimal fat)
        => new()
        {
            InventoryId = foodId,
            FoodId = foodId,
            FoodName = name,
            QuantityGrams = quantityGrams,
            KcalPer100g = kcal,
            ProteinGPer100g = protein,
            CarbsGPer100g = carbs,
            FatGPer100g = fat
        };

    // ══════════════════════════════════════════════════════════════
    // TEST 1: Happy Path — Kho dồi dào, target khả thi
    // Phân vùng: Valid Input → Expected OPTIMAL
    // ══════════════════════════════════════════════════════════════

    [Fact]
    public void CalculateOptimalMeal_ValidTargetAndAbundantInventory_ReturnsSuccessful()
    {
        // ── Arrange ─────────────────────────────────────────────
        var target = new DailyTargetDto
        {
            TargetKcal = 2000m,
            TargetProteinG = 150m,
            TargetCarbsG = 200m,
            TargetFatG = 66m
        };

        var inventory = new List<InventoryItemResponseDto>
        {
            //                          ID   Name             Qty     Kcal  Pro   Carb  Fat
            CreateFood(1, "Ức gà",       5000m, 165m, 31m,  0m,   3.6m),
            CreateFood(2, "Gạo trắng",   5000m, 130m, 2.7m, 28m,  0.3m),
            CreateFood(3, "Dầu olive",   5000m, 884m, 0m,   0m,   100m)
        };

        // ── Act ─────────────────────────────────────────────────
        var result = _engine.CalculateOptimalMeal(target, inventory);

        // ── Assert ──────────────────────────────────────────────
        result.IsSuccessful.Should().BeTrue(
            "kho thực phẩm đủ đa dạng và dồi dào để đáp ứng mọi ràng buộc macro");

        result.Items.Should().NotBeEmpty(
            "solver phải chọn ít nhất 1 thực phẩm");

        // Tổng Macro phải nằm trong biên độ ±5% so với Target (Boundary Value Analysis)
        result.TotalProtein.Should().BeInRange(
            target.TargetProteinG * 0.95m,
            target.TargetProteinG * 1.05m,
            "Protein phải nằm trong ±5% target");

        result.TotalCarbs.Should().BeInRange(
            target.TargetCarbsG * 0.95m,
            target.TargetCarbsG * 1.05m,
            "Carbs phải nằm trong ±5% target");

        result.TotalFat.Should().BeInRange(
            target.TargetFatG * 0.95m,
            target.TargetFatG * 1.05m,
            "Fat phải nằm trong ±5% target");

        // Không thực phẩm nào được gợi ý vượt quá tồn kho
        foreach (var item in result.Items)
        {
            var sourceInventory = inventory.First(i => i.FoodId == item.FoodId);
            item.CalculatedGrams.Should().BeLessThanOrEqualTo(
                sourceInventory.QuantityGrams,
                $"{item.FoodName} không được vượt quá tồn kho {sourceInventory.QuantityGrams}g");
        }
    }

    // ══════════════════════════════════════════════════════════════
    // TEST 2: Exact Match — 1 nguyên liệu duy nhất, tính toán chính xác
    // Phân vùng: Minimal Valid Input (biên dưới số lượng nguyên liệu)
    // ══════════════════════════════════════════════════════════════

    [Fact]
    public void CalculateOptimalMeal_ExactSingleItemMatch_ReturnsCorrectGrams()
    {
        // ── Arrange ─────────────────────────────────────────────
        // Whey Protein Isolate: 90g protein / 100g, gần 0 carbs & fat
        // Target: 30g Protein → cần đúng 33.33g bột
        var target = new DailyTargetDto
        {
            TargetKcal = 120m,      // ~33.33g × 360kcal/100g
            TargetProteinG = 30m,
            TargetCarbsG = 0m,
            TargetFatG = 0m
        };

        var inventory = new List<InventoryItemResponseDto>
        {
            CreateFood(1, "Whey Protein Isolate", 500m, 360m, 90m, 0m, 0m)
        };

        // ── Act ─────────────────────────────────────────────────
        var result = _engine.CalculateOptimalMeal(target, inventory);

        // ── Assert ──────────────────────────────────────────────
        result.IsSuccessful.Should().BeTrue(
            "bài toán có nghiệm duy nhất rõ ràng: 33.33g Whey");

        result.Items.Should().ContainSingle(
            "chỉ có 1 loại thực phẩm trong kho nên chỉ 1 item được chọn");

        var whey = result.Items[0];
        whey.FoodName.Should().Be("Whey Protein Isolate");

        // 30g protein / (90g protein per 100g) × 100 = 33.33g
        // Biên độ ±5% → [31.67, 35.00]
        whey.CalculatedGrams.Should().BeApproximately(33.33m, 1.67m,
            "cần ~33.33g Whey để đạt 30g Protein (±5% tolerance)");
    }

    // ══════════════════════════════════════════════════════════════
    // TEST 3: Inventory Exhaustion — Kho không đủ nguyên liệu
    // Phân vùng: Invalid — tồn kho thấp hơn nhu cầu
    // Biên: QuantityGrams < Required Grams (boundary violation)
    // ══════════════════════════════════════════════════════════════

    [Fact]
    public void CalculateOptimalMeal_TargetExceedsInventory_ReturnsInfeasible()
    {
        // ── Arrange ─────────────────────────────────────────────
        // Cần 100g Protein → cần ~322g ức gà (31g pro/100g)
        // Nhưng kho chỉ có 50g ức gà → max 15.5g protein → INFEASIBLE
        var target = new DailyTargetDto
        {
            TargetKcal = 530m,
            TargetProteinG = 100m,
            TargetCarbsG = 0m,
            TargetFatG = 0m
        };

        var inventory = new List<InventoryItemResponseDto>
        {
            CreateFood(1, "Ức gà", 50m, 165m, 31m, 0m, 3.6m)
        };

        // ── Act ─────────────────────────────────────────────────
        var result = _engine.CalculateOptimalMeal(target, inventory);

        // ── Assert ──────────────────────────────────────────────
        result.IsSuccessful.Should().BeFalse(
            "50g ức gà chỉ cung cấp tối đa 15.5g protein, không đủ 100g target");

        // Đảm bảo thuật toán KHÔNG gợi ý số lượng vượt quá tồn kho
        result.Items.Should().BeEmpty(
            "khi Infeasible, không nên có item nào trong kết quả");
    }

    // ══════════════════════════════════════════════════════════════
    // TEST 4: Conflicting Macros — Target mâu thuẫn với nguyên liệu có sẵn
    // Phân vùng: Invalid — không tồn tại tổ hợp nào thỏa mãn
    // ══════════════════════════════════════════════════════════════

    [Fact]
    public void CalculateOptimalMeal_ConflictingMacros_ReturnsInfeasible()
    {
        // ── Arrange ─────────────────────────────────────────────
        // Target: cần 100g Carbs, 0g Fat
        // Kho chỉ có nguồn Fat thuần (dầu ăn, bơ đậu phộng) → 0 Carbs
        // → Không thể đáp ứng ràng buộc Carbs → INFEASIBLE
        var target = new DailyTargetDto
        {
            TargetKcal = 400m,
            TargetProteinG = 0m,
            TargetCarbsG = 100m,
            TargetFatG = 0m
        };

        var inventory = new List<InventoryItemResponseDto>
        {
            CreateFood(1, "Dầu ăn",        1000m, 884m, 0m, 0m, 100m),
            CreateFood(2, "Bơ đậu phộng",  1000m, 588m, 25m, 20m, 50m)
        };

        // ── Act ─────────────────────────────────────────────────
        var result = _engine.CalculateOptimalMeal(target, inventory);

        // ── Assert ──────────────────────────────────────────────
        result.IsSuccessful.Should().BeFalse(
            "kho chỉ có nguồn Fat, không thể cung cấp 100g Carbs với 0g Fat");

        result.Message.Should().NotBeNullOrWhiteSpace(
            "khi Infeasible, phải có message giải thích lý do thất bại");
    }

    // ══════════════════════════════════════════════════════════════
    // TEST 5: Empty Inventory — Kho rỗng
    // Phân vùng: Boundary — danh sách có 0 phần tử
    // Đảm bảo không ném RuntimeException (crash-safety)
    // ══════════════════════════════════════════════════════════════

    [Fact]
    public void CalculateOptimalMeal_EmptyInventory_ReturnsInfeasible()
    {
        // ── Arrange ─────────────────────────────────────────────
        var target = new DailyTargetDto
        {
            TargetKcal = 2000m,
            TargetProteinG = 150m,
            TargetCarbsG = 200m,
            TargetFatG = 66m
        };

        var emptyInventory = new List<InventoryItemResponseDto>();

        // ── Act ─────────────────────────────────────────────────
        // Không được ném Exception — phải trả về kết quả an toàn
        var act = () => _engine.CalculateOptimalMeal(target, emptyInventory);

        // ── Assert ──────────────────────────────────────────────
        var result = act.Should().NotThrow(
            "empty inventory phải được xử lý gracefully, không crash app")
            .Subject;

        result.IsSuccessful.Should().BeFalse(
            "không thể tối ưu hóa khi kho thực phẩm trống");

        result.Items.Should().BeEmpty(
            "kết quả rỗng khi không có nguyên liệu nào");
    }
}
