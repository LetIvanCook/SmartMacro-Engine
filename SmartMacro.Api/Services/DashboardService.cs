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

        // 1. Thông tin cơ bản của User (SELECT 3 cột: user_id, full_name, goal_type)
        var user = await _db.Users
            .AsNoTracking()
            .Where(u => u.UserId == userId)
            .Select(u => new { u.UserId, u.FullName, u.GoalType })
            .FirstOrDefaultAsync();

        if (user is null)
            return null;

        // 2. Mục tiêu macro hôm nay
        var todayTarget = await _db.DailyTargets
            .AsNoTracking()
            .Where(dt => dt.UserId == userId && dt.TargetDate == today)
            .ProjectTo<DailyTargetDto>(_mapper.ConfigurationProvider)
            .FirstOrDefaultAsync();

        // 3. Kho thực phẩm còn hàng (quantity > 0)
        var availableInventory = await _db.UserFoodInventories
            .AsNoTracking()
            .Where(inv => inv.UserId == userId && inv.QuantityGrams > 0)
            .ProjectTo<InventoryItemResponseDto>(_mapper.ConfigurationProvider)
            .ToListAsync();

        // Gom kết quả vào Composite DTO — client nhận MỘT payload duy nhất.
        return new UserDashboardResponseDto
        {
            UserId = user.UserId,
            FullName = user.FullName,
            GoalType = user.GoalType,
            TodayTarget = todayTarget,
            AvailableInventory = availableInventory
        };
    }
}
