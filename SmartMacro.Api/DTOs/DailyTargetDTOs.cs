namespace SmartMacro.Api.DTOs;

/// <summary>
/// Response DTO cho một bản ghi DailyTarget (Nhánh A — bảng lịch sử theo ngày).
/// Expose TargetId để client có thể dùng trong PUT/DELETE.
/// </summary>
public class DailyTargetResponseDto
{
    public long Id { get; set; }
    public DateOnly TargetDate { get; set; }
    public decimal TargetKcal { get; set; }
    public decimal TargetProteinG { get; set; }
    public decimal TargetCarbsG { get; set; }
    public decimal TargetFatG { get; set; }
}

/// <summary>
/// Request DTO dùng khi tạo target mới.
/// Date mặc định là hôm nay nếu không truyền.
/// </summary>
public class CreateDailyTargetRequestDto
{
    /// <summary>Ngày áp dụng target. Null = mặc định hôm nay (DateOnly.FromDateTime(DateTime.Now)).</summary>
    public DateOnly? Date { get; set; }
    public decimal TargetKcal { get; set; }
    public decimal TargetProteinG { get; set; }
    public decimal TargetCarbsG { get; set; }
    public decimal TargetFatG { get; set; }
}

/// <summary>
/// Request DTO dùng khi cập nhật target đã có (không cho phép đổi ngày — chỉ update macro).
/// </summary>
public class UpdateDailyTargetRequestDto
{
    public decimal TargetKcal { get; set; }
    public decimal TargetProteinG { get; set; }
    public decimal TargetCarbsG { get; set; }
    public decimal TargetFatG { get; set; }
}
