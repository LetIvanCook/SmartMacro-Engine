using Microsoft.EntityFrameworkCore;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Models;

namespace SmartMacro.Api.Services;

/// <summary>
/// Triển khai CRUD cho DailyTarget (Nhánh A — bảng lịch sử theo ngày).
/// Logic "target hôm nay" dùng đúng cách Dashboard và Optimization đang dùng:
///   DateOnly.FromDateTime(DateTime.Now)  +  dt.TargetDate == today
/// </summary>
public class DailyTargetService : IDailyTargetService
{
    private readonly SmartMacroDbContext _db;

    public DailyTargetService(SmartMacroDbContext db)
    {
        _db = db;
    }

    /// <inheritdoc />
    public async Task<List<DailyTargetResponseDto>> GetMyTargetsAsync(long userId)
    {
        return await _db.DailyTargets
            .Where(dt => dt.UserId == userId)
            .OrderByDescending(dt => dt.TargetDate)
            .Select(dt => MapToDto(dt))
            .ToListAsync();
    }

    /// <inheritdoc />
    public async Task<DailyTargetResponseDto> GetTodayTargetAsync(long userId)
    {
        // Dùng đúng logic DateOnly.FromDateTime(DateTime.Now), khớp với
        // DashboardService (line 29) và OptimizationService (line 41).
        var today = DateOnly.FromDateTime(DateTime.Now);

        var target = await _db.DailyTargets
            .Where(dt => dt.UserId == userId && dt.TargetDate == today)
            .Select(dt => MapToDto(dt))
            .FirstOrDefaultAsync();

        if (target is null)
            throw new NotFoundException($"Chưa có mục tiêu macro cho ngày hôm nay ({today:yyyy-MM-dd}).");

        return target;
    }

    /// <inheritdoc />
    public async Task<DailyTargetResponseDto> CreateTargetAsync(long userId, CreateDailyTargetRequestDto request)
    {
        ValidateMacros(request.TargetKcal, request.TargetProteinG, request.TargetCarbsG, request.TargetFatG);

        var targetDate = request.Date ?? DateOnly.FromDateTime(DateTime.Now);

        // Kiểm tra trùng lặp (UQ_target_user_date)
        var alreadyExists = await _db.DailyTargets
            .AnyAsync(dt => dt.UserId == userId && dt.TargetDate == targetDate);

        if (alreadyExists)
            throw new ConflictException(
                $"Đã tồn tại mục tiêu macro cho ngày {targetDate:yyyy-MM-dd}. Dùng PUT /api/daily-targets/{{id}} để cập nhật.");

        var entity = new DailyTarget
        {
            UserId = userId,
            TargetDate = targetDate,
            TargetKcal = request.TargetKcal,
            TargetProteinG = request.TargetProteinG,
            TargetCarbsG = request.TargetCarbsG,
            TargetFatG = request.TargetFatG,
            CreatedAt = DateTime.Now
        };

        _db.DailyTargets.Add(entity);
        await _db.SaveChangesAsync();

        return MapToDto(entity);
    }

    /// <inheritdoc />
    public async Task<DailyTargetResponseDto> UpdateTargetAsync(long userId, long targetId, UpdateDailyTargetRequestDto request)
    {
        ValidateMacros(request.TargetKcal, request.TargetProteinG, request.TargetCarbsG, request.TargetFatG);

        var entity = await _db.DailyTargets
            .FirstOrDefaultAsync(dt => dt.TargetId == targetId && dt.UserId == userId);

        if (entity is null)
            throw new NotFoundException(
                $"Mục tiêu macro với ID {targetId} không tồn tại hoặc không thuộc về người dùng hiện tại.");

        entity.TargetKcal = request.TargetKcal;
        entity.TargetProteinG = request.TargetProteinG;
        entity.TargetCarbsG = request.TargetCarbsG;
        entity.TargetFatG = request.TargetFatG;

        await _db.SaveChangesAsync();

        return MapToDto(entity);
    }

    /// <inheritdoc />
    public async Task DeleteTargetAsync(long userId, long targetId)
    {
        var entity = await _db.DailyTargets
            .FirstOrDefaultAsync(dt => dt.TargetId == targetId && dt.UserId == userId);

        if (entity is null)
            throw new NotFoundException(
                $"Mục tiêu macro với ID {targetId} không tồn tại hoặc không thuộc về người dùng hiện tại.");

        _db.DailyTargets.Remove(entity);
        await _db.SaveChangesAsync();
    }

    // ──────────────────────────────────────────────────────────────
    // Private helpers
    // ──────────────────────────────────────────────────────────────

    /// <summary>
    /// Validate rằng tất cả macro > 0.
    /// Dùng ArgumentException (400) — giữ đúng pattern hiện tại của InventoryService.
    /// </summary>
    private static void ValidateMacros(decimal kcal, decimal protein, decimal carbs, decimal fat)
    {
        if (kcal <= 0)
            throw new ArgumentException("TargetKcal phải lớn hơn 0.");
        if (protein <= 0)
            throw new ArgumentException("TargetProteinG phải lớn hơn 0.");
        if (carbs <= 0)
            throw new ArgumentException("TargetCarbsG phải lớn hơn 0.");
        if (fat <= 0)
            throw new ArgumentException("TargetFatG phải lớn hơn 0.");
    }

    private static DailyTargetResponseDto MapToDto(DailyTarget entity) => new()
    {
        Id = entity.TargetId,
        TargetDate = entity.TargetDate,
        TargetKcal = entity.TargetKcal,
        TargetProteinG = entity.TargetProteinG,
        TargetCarbsG = entity.TargetCarbsG,
        TargetFatG = entity.TargetFatG
    };
}
