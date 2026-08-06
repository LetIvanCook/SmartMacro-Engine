namespace SmartMacro.Api.DTOs;

/// <summary>
/// DTO trả về cho client khi query Food.
/// CategoryName được project từ navigation property Food.Category
/// qua AutoMapper ProjectTo — không cần Include().
/// </summary>
public class FoodResponseDto
{
    public long FoodId { get; set; }
    public string FoodName { get; set; } = null!;
    public short? CategoryId { get; set; }
    public string? CategoryName { get; set; }
    public decimal KcalPer100g { get; set; }
    public decimal ProteinGPer100g { get; set; }
    public decimal CarbsGPer100g { get; set; }
    public decimal FatGPer100g { get; set; }
    public decimal? FiberGPer100g { get; set; }
    public bool IsVerified { get; set; }
    public string Source { get; set; } = null!;
    public DateTime CreatedAt { get; set; }
}

/// <summary>
/// Request DTO cho tìm kiếm Food có phân trang.
/// Keyword: partial match, case-insensitive trên FoodName.
/// CategoryId: filter chính xác theo danh mục (optional).
/// </summary>
public class FoodSearchRequestDto
{
    public string? Keyword { get; set; }
    public short? CategoryId { get; set; }
    public int Page { get; set; } = 1;
    public int PageSize { get; set; } = 20;
}

/// <summary>
/// Request DTO để tạo mới Food.
/// Tên field khớp chính xác với entity Food trong DbContext.
/// </summary>
public class CreateFoodRequestDto
{
    public string FoodName { get; set; } = null!;
    public short? CategoryId { get; set; }
    public decimal KcalPer100g { get; set; }
    public decimal ProteinGPer100g { get; set; }
    public decimal CarbsGPer100g { get; set; }
    public decimal FatGPer100g { get; set; }
    public decimal? FiberGPer100g { get; set; }
}

/// <summary>
/// Request DTO để cập nhật Food — cùng fields với Create.
/// </summary>
public class UpdateFoodRequestDto : CreateFoodRequestDto { }
