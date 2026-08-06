using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Models;
using SmartMacro.Api.Services;

namespace SmartMacro.Tests;

/// <summary>
/// Tests cho DailyTargetService — Nhánh A (bảng lịch sử theo TargetDate).
/// Dùng EF Core InMemory + Guid isolation để mỗi test có DB riêng biệt.
/// </summary>
public class DailyTargetServiceTests : IDisposable
{
    private readonly SmartMacroDbContext _db;
    private readonly DailyTargetService _sut;

    public DailyTargetServiceTests()
    {
        var options = new DbContextOptionsBuilder<SmartMacroDbContext>()
            .UseInMemoryDatabase(databaseName: $"SmartMacro_DailyTarget_{Guid.NewGuid()}")
            .Options;

        _db = new SmartMacroDbContext(options);
        _sut = new DailyTargetService(_db);
    }

    public void Dispose()
    {
        _db.Database.EnsureDeleted();
        _db.Dispose();
    }

    // ──────────────────────────────────────────────────────────────
    // Seed helpers
    // ──────────────────────────────────────────────────────────────

    private User SeedUser(long id)
    {
        var user = new User
        {
            UserId = id,
            Email = $"user{id}@test.com",
            PasswordHash = new string('x', 60),
            FullName = $"User {id}",
            DateOfBirth = new DateOnly(1995, 5, 15),
            ActivityLevel = "moderate",
            BiologicalSex = "male",
            GoalType = "maintain",
            Status = "active",
            CreatedAt = DateTime.UtcNow,
            UpdatedAt = DateTime.UtcNow
        };
        _db.Users.Add(user);
        return user;
    }

    private DailyTarget SeedTarget(long id, long userId, DateOnly date,
        decimal kcal = 2000m, decimal protein = 150m, decimal carbs = 200m, decimal fat = 70m)
    {
        var target = new DailyTarget
        {
            TargetId = id,
            UserId = userId,
            TargetDate = date,
            TargetKcal = kcal,
            TargetProteinG = protein,
            TargetCarbsG = carbs,
            TargetFatG = fat,
            CreatedAt = DateTime.UtcNow
        };
        _db.DailyTargets.Add(target);
        return target;
    }

    private static CreateDailyTargetRequestDto ValidCreateRequest(DateOnly? date = null) => new()
    {
        Date = date,
        TargetKcal = 2000m,
        TargetProteinG = 150m,
        TargetCarbsG = 200m,
        TargetFatG = 70m
    };

    // ──────────────────────────────────────────────────────────────
    // CreateTargetAsync
    // ──────────────────────────────────────────────────────────────

    [Fact]
    public async Task CreateTargetAsync_ValidData_ReturnsCorrectDto()
    {
        // Arrange
        SeedUser(1);
        await _db.SaveChangesAsync();

        var request = ValidCreateRequest(new DateOnly(2030, 1, 15));

        // Act
        var result = await _sut.CreateTargetAsync(1, request);

        // Assert
        result.Should().NotBeNull();
        result.Id.Should().BeGreaterThan(0);
        result.TargetDate.Should().Be(new DateOnly(2030, 1, 15));
        result.TargetKcal.Should().Be(2000m);
        result.TargetProteinG.Should().Be(150m);
        result.TargetCarbsG.Should().Be(200m);
        result.TargetFatG.Should().Be(70m);

        var inDb = await _db.DailyTargets.SingleAsync();
        inDb.UserId.Should().Be(1);
        inDb.TargetDate.Should().Be(new DateOnly(2030, 1, 15));
    }

    [Fact]
    public async Task CreateTargetAsync_DateIsNull_DefaultsToToday()
    {
        // Arrange
        SeedUser(1);
        await _db.SaveChangesAsync();

        var today = DateOnly.FromDateTime(DateTime.Now);
        var request = ValidCreateRequest(date: null);

        // Act
        var result = await _sut.CreateTargetAsync(1, request);

        // Assert
        result.TargetDate.Should().Be(today);
    }

    [Theory]
    [InlineData(0, 150, 200, 70, "TargetKcal")]
    [InlineData(-1, 150, 200, 70, "TargetKcal")]
    [InlineData(2000, 0, 200, 70, "TargetProteinG")]
    [InlineData(2000, -5, 200, 70, "TargetProteinG")]
    [InlineData(2000, 150, 0, 70, "TargetCarbsG")]
    [InlineData(2000, 150, -1, 70, "TargetCarbsG")]
    [InlineData(2000, 150, 200, 0, "TargetFatG")]
    [InlineData(2000, 150, 200, -1, "TargetFatG")]
    public async Task CreateTargetAsync_MacroLeOrZero_ThrowsArgumentException(
        decimal kcal, decimal protein, decimal carbs, decimal fat, string fieldName)
    {
        // Arrange
        var request = new CreateDailyTargetRequestDto
        {
            Date = new DateOnly(2030, 1, 15),
            TargetKcal = kcal,
            TargetProteinG = protein,
            TargetCarbsG = carbs,
            TargetFatG = fat
        };

        // Act & Assert
        await _sut.Invoking(s => s.CreateTargetAsync(1, request))
            .Should().ThrowAsync<ArgumentException>()
            .WithMessage($"*{fieldName}*");
    }

    [Fact]
    public async Task CreateTargetAsync_DuplicateDate_ThrowsConflictException()
    {
        // Arrange
        SeedUser(1);
        var date = new DateOnly(2030, 6, 1);
        SeedTarget(1, 1, date);
        await _db.SaveChangesAsync();

        var request = ValidCreateRequest(date);

        // Act & Assert
        await _sut.Invoking(s => s.CreateTargetAsync(1, request))
            .Should().ThrowAsync<ConflictException>()
            .WithMessage($"*{date:yyyy-MM-dd}*");
    }

    [Fact]
    public async Task CreateTargetAsync_SameDateDifferentUser_Succeeds()
    {
        // Arrange
        SeedUser(1); SeedUser(2);
        var date = new DateOnly(2030, 6, 1);
        SeedTarget(1, 1, date); // User 1 already has target
        await _db.SaveChangesAsync();

        // Act — User 2 creates target for same date
        var request = ValidCreateRequest(date);
        var result = await _sut.CreateTargetAsync(2, request);

        // Assert
        result.Should().NotBeNull();
        result.TargetDate.Should().Be(date);
        (await _db.DailyTargets.CountAsync()).Should().Be(2);
    }

    // ──────────────────────────────────────────────────────────────
    // GetMyTargetsAsync
    // ──────────────────────────────────────────────────────────────

    [Fact]
    public async Task GetMyTargetsAsync_ReturnsOnlyOwnTargetsOrderedDescending()
    {
        // Arrange
        SeedUser(1); SeedUser(2);
        SeedTarget(1, 1, new DateOnly(2030, 1, 1));
        SeedTarget(2, 1, new DateOnly(2030, 1, 3));
        SeedTarget(3, 2, new DateOnly(2030, 1, 2)); // Other user
        await _db.SaveChangesAsync();

        // Act
        var result = await _sut.GetMyTargetsAsync(1);

        // Assert
        result.Should().HaveCount(2);
        result[0].TargetDate.Should().Be(new DateOnly(2030, 1, 3)); // Most recent first
        result[1].TargetDate.Should().Be(new DateOnly(2030, 1, 1));
    }

    // ──────────────────────────────────────────────────────────────
    // GetTodayTargetAsync — khớp đúng logic Dashboard/Optimization
    // ──────────────────────────────────────────────────────────────

    [Fact]
    public async Task GetTodayTargetAsync_TargetExistsForToday_ReturnsIt()
    {
        // Arrange
        SeedUser(1);
        // "Today" theo DateOnly.FromDateTime(DateTime.Now) — cùng cách Dashboard dùng
        var today = DateOnly.FromDateTime(DateTime.Now);
        SeedTarget(1, 1, today, kcal: 1800m, protein: 130m, carbs: 180m, fat: 60m);
        await _db.SaveChangesAsync();

        // Act
        var result = await _sut.GetTodayTargetAsync(1);

        // Assert
        result.Should().NotBeNull();
        result.TargetDate.Should().Be(today);
        result.TargetKcal.Should().Be(1800m);
        result.TargetProteinG.Should().Be(130m);
        result.TargetCarbsG.Should().Be(180m);
        result.TargetFatG.Should().Be(60m);
    }

    [Fact]
    public async Task GetTodayTargetAsync_NoTargetForToday_ThrowsNotFoundException()
    {
        // Arrange
        SeedUser(1);
        // Past target exists but NOT for today
        SeedTarget(1, 1, new DateOnly(2020, 1, 1));
        await _db.SaveChangesAsync();

        // Act & Assert
        await _sut.Invoking(s => s.GetTodayTargetAsync(1))
            .Should().ThrowAsync<NotFoundException>();
    }

    [Fact]
    public async Task GetTodayTargetAsync_OtherUserHasTodayTarget_ThrowsNotFoundException()
    {
        // Arrange — User 2 has today's target, User 1 does not
        SeedUser(1); SeedUser(2);
        var today = DateOnly.FromDateTime(DateTime.Now);
        SeedTarget(1, 2, today); // User 2's target
        await _db.SaveChangesAsync();

        // Act & Assert — User 1 requesting → NotFoundException, not 403
        await _sut.Invoking(s => s.GetTodayTargetAsync(1))
            .Should().ThrowAsync<NotFoundException>();
    }

    // ──────────────────────────────────────────────────────────────
    // UpdateTargetAsync
    // ──────────────────────────────────────────────────────────────

    [Fact]
    public async Task UpdateTargetAsync_Valid_UpdatesMacrosCorrectly()
    {
        // Arrange
        SeedUser(1);
        SeedTarget(1, 1, new DateOnly(2030, 1, 1), kcal: 2000m, protein: 150m, carbs: 200m, fat: 70m);
        await _db.SaveChangesAsync();

        var request = new UpdateDailyTargetRequestDto
        {
            TargetKcal = 1800m,
            TargetProteinG = 140m,
            TargetCarbsG = 180m,
            TargetFatG = 60m
        };

        // Act
        var result = await _sut.UpdateTargetAsync(1, 1, request);

        // Assert
        result.TargetKcal.Should().Be(1800m);
        result.TargetProteinG.Should().Be(140m);
        result.TargetCarbsG.Should().Be(180m);
        result.TargetFatG.Should().Be(60m);
        result.TargetDate.Should().Be(new DateOnly(2030, 1, 1)); // Date không đổi

        var inDb = await _db.DailyTargets.FindAsync(1L);
        inDb!.TargetKcal.Should().Be(1800m);
    }

    [Fact]
    public async Task UpdateTargetAsync_TargetNotFound_ThrowsNotFoundException()
    {
        SeedUser(1);
        await _db.SaveChangesAsync();

        var request = new UpdateDailyTargetRequestDto
        {
            TargetKcal = 1800m,
            TargetProteinG = 140m,
            TargetCarbsG = 180m,
            TargetFatG = 60m
        };

        await _sut.Invoking(s => s.UpdateTargetAsync(1, 999, request))
            .Should().ThrowAsync<NotFoundException>();
    }

    [Fact]
    public async Task UpdateTargetAsync_OtherUserTarget_ThrowsNotFoundException()
    {
        // Arrange — target belongs to User 2
        SeedUser(1); SeedUser(2);
        SeedTarget(1, 2, new DateOnly(2030, 1, 1));
        await _db.SaveChangesAsync();

        var request = new UpdateDailyTargetRequestDto
        {
            TargetKcal = 1800m,
            TargetProteinG = 140m,
            TargetCarbsG = 180m,
            TargetFatG = 60m
        };

        // User 1 tries to update User 2's target → 404, not 403
        await _sut.Invoking(s => s.UpdateTargetAsync(1, 1, request))
            .Should().ThrowAsync<NotFoundException>();
    }

    [Theory]
    [InlineData(0, 150, 200, 70)]
    [InlineData(2000, -1, 200, 70)]
    [InlineData(2000, 150, 0, 70)]
    [InlineData(2000, 150, 200, -5)]
    public async Task UpdateTargetAsync_MacroLeOrZero_ThrowsArgumentException(
        decimal kcal, decimal protein, decimal carbs, decimal fat)
    {
        SeedUser(1);
        SeedTarget(1, 1, new DateOnly(2030, 1, 1));
        await _db.SaveChangesAsync();

        var request = new UpdateDailyTargetRequestDto
        {
            TargetKcal = kcal,
            TargetProteinG = protein,
            TargetCarbsG = carbs,
            TargetFatG = fat
        };

        await _sut.Invoking(s => s.UpdateTargetAsync(1, 1, request))
            .Should().ThrowAsync<ArgumentException>();
    }

    // ──────────────────────────────────────────────────────────────
    // DeleteTargetAsync
    // ──────────────────────────────────────────────────────────────

    [Fact]
    public async Task DeleteTargetAsync_Valid_RemovesRecord()
    {
        // Arrange
        SeedUser(1);
        SeedTarget(1, 1, new DateOnly(2030, 1, 1));
        await _db.SaveChangesAsync();

        // Act
        await _sut.DeleteTargetAsync(1, 1);

        // Assert — record biến mất khỏi DB
        var inDb = await _db.DailyTargets.FindAsync(1L);
        inDb.Should().BeNull();
        (await _db.DailyTargets.CountAsync()).Should().Be(0);
    }

    [Fact]
    public async Task DeleteTargetAsync_TargetNotFound_ThrowsNotFoundException()
    {
        SeedUser(1);
        await _db.SaveChangesAsync();

        await _sut.Invoking(s => s.DeleteTargetAsync(1, 999))
            .Should().ThrowAsync<NotFoundException>();
    }

    [Fact]
    public async Task DeleteTargetAsync_OtherUserTarget_ThrowsNotFoundException()
    {
        // Arrange — target belongs to User 2
        SeedUser(1); SeedUser(2);
        SeedTarget(1, 2, new DateOnly(2030, 1, 1));
        await _db.SaveChangesAsync();

        // User 1 tries to delete User 2's target → 404, not 403
        await _sut.Invoking(s => s.DeleteTargetAsync(1, 1))
            .Should().ThrowAsync<NotFoundException>();
    }
}
