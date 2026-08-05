using SmartMacro.Api.DTOs;

namespace SmartMacro.Api.Interfaces;

/// <summary>
/// Định nghĩa contract cho tầng Business Logic của Dashboard.
/// Controller chỉ cần biết interface này — không cần biết implementation chi tiết.
/// </summary>
public interface IDashboardService
{
    /// <summary>
    /// Truy vấn song song và gom toàn bộ dữ liệu Dashboard cho một User.
    /// </summary>
    /// <param name="userId">ID của User cần lấy Dashboard.</param>
    /// <returns>
    /// Composite DTO chứa thông tin User, DailyTarget hôm nay, và kho thực phẩm.
    /// Trả về <c>null</c> nếu không tìm thấy User.
    /// </returns>
    Task<UserDashboardResponseDto?> GetUserDashboardAsync(long userId);
}
