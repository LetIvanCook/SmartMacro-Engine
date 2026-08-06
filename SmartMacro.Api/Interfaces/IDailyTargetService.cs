using SmartMacro.Api.DTOs;

namespace SmartMacro.Api.Interfaces;

public interface IDailyTargetService
{
    /// <summary>Lấy toàn bộ target của user (sắp xếp theo ngày giảm dần).</summary>
    Task<List<DailyTargetResponseDto>> GetMyTargetsAsync(long userId);

    /// <summary>
    /// Lấy target của hôm nay, dùng đúng logic DateOnly.FromDateTime(DateTime.Now)
    /// khớp với DashboardService và OptimizationService.
    /// Throws NotFoundException nếu chưa có target cho hôm nay.
    /// </summary>
    Task<DailyTargetResponseDto> GetTodayTargetAsync(long userId);

    /// <summary>
    /// Tạo target mới. Nếu Date == null → mặc định hôm nay.
    /// Throws ConflictException nếu đã có target cho ngày đó.
    /// Throws ArgumentException nếu bất kỳ macro nào ≤ 0.
    /// </summary>
    Task<DailyTargetResponseDto> CreateTargetAsync(long userId, CreateDailyTargetRequestDto request);

    /// <summary>
    /// Cập nhật macro của target đã có.
    /// Throws NotFoundException nếu targetId không tồn tại hoặc không thuộc userId.
    /// Throws ArgumentException nếu bất kỳ macro nào ≤ 0.
    /// </summary>
    Task<DailyTargetResponseDto> UpdateTargetAsync(long userId, long targetId, UpdateDailyTargetRequestDto request);

    /// <summary>
    /// Xoá target.
    /// Throws NotFoundException nếu targetId không tồn tại hoặc không thuộc userId.
    /// </summary>
    Task DeleteTargetAsync(long userId, long targetId);
}
