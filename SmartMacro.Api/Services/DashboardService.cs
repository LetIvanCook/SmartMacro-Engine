using AutoMapper;
using AutoMapper.QueryableExtensions;
using Microsoft.EntityFrameworkCore;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Models;

namespace SmartMacro.Api.Services;

/// <summary>
/// Triển khai business logic cho Dashboard.
/// Nhận SmartMacroDbContext và IMapper qua constructor injection —
/// toàn bộ logic truy vấn được tập trung tại đây thay vì nằm rải rác trong Controller.
/// </summary>
public class DashboardService : IDashboardService
{
    private readonly SmartMacroDbContext _db;
    private readonly IMapper _mapper;

    public DashboardService(SmartMacroDbContext db, IMapper mapper)
    {
        _db = db;
        _mapper = mapper;
    }

    /// <inheritdoc />
    public async Task<UserDashboardResponseDto?> GetUserDashboardAsync(long userId)
    {
        var today = DateOnly.FromDateTime(DateTime.Now);

        // ──────────────────────────────────────────────────────────────
        // Truy vấn song song 3 luồng dữ liệu độc lập.
        // Mỗi Task sẽ chạy một câu SQL riêng biệt, tận dụng tối đa
        // khả năng xử lý đồng thời của SQL Server.
        // ──────────────────────────────────────────────────────────────

        // Luồng 1: Thông tin cơ bản của User.
        // Chỉ SELECT 3 cột: user_id, full_name, goal_type.
        // Dùng anonymous type projection thay vì .Find() để tránh kéo toàn bộ entity.
        var userTask = _db.Users
            .Where(u => u.UserId == userId)
            .Select(u => new { u.UserId, u.FullName, u.GoalType })
            .FirstOrDefaultAsync();

        // Luồng 2: Mục tiêu macro hôm nay.
        // ProjectTo<DailyTargetDto> sẽ sinh SELECT chỉ 4 cột macro,
        // bỏ qua TargetId, UserId, ComputedFromRuleId, CreatedAt.
        var targetTask = _db.DailyTargets
            .Where(dt => dt.UserId == userId && dt.TargetDate == today)
            .ProjectTo<DailyTargetDto>(_mapper.ConfigurationProvider)
            .FirstOrDefaultAsync();

        // Luồng 3: Kho thực phẩm còn hàng (quantity > 0).
        // ProjectTo<InventoryItemResponseDto> sẽ sinh JOIN foods ON food_id
        // và SELECT chỉ 5 cột cần thiết — không kéo toàn bộ Food entity.
        var inventoryTask = _db.UserFoodInventories
            .Where(inv => inv.UserId == userId && inv.QuantityGrams > 0)
            .ProjectTo<InventoryItemResponseDto>(_mapper.ConfigurationProvider)
            .ToListAsync();

        // Chờ cả 3 task hoàn thành song song.
        await Task.WhenAll(userTask, targetTask, inventoryTask);

        // ──────────────────────────────────────────────────────────────
        // Kiểm tra User tồn tại — trả về null để Controller quyết định HTTP status.
        // ──────────────────────────────────────────────────────────────
        var user = userTask.Result;
        if (user is null)
            return null;

        // ──────────────────────────────────────────────────────────────
        // Gom kết quả vào Composite DTO — client nhận MỘT payload duy nhất.
        // ──────────────────────────────────────────────────────────────
        return new UserDashboardResponseDto
        {
            UserId = user.UserId,
            FullName = user.FullName,
            GoalType = user.GoalType,
            TodayTarget = targetTask.Result,          // null nếu chưa có target hôm nay
            AvailableInventory = inventoryTask.Result  // empty list nếu kho trống
        };
    }
}
