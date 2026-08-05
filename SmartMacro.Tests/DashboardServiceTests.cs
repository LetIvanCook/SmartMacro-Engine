using AutoMapper;
using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using SmartMacro.Api.Models;
using SmartMacro.Api.Profiles;
using SmartMacro.Api.Services;

namespace SmartMacro.Tests;

/// <summary>
/// Unit tests cho <see cref="DashboardService"/>.
/// Sử dụng EF Core InMemory Database + real AutoMapper configuration
/// để đảm bảo ProjectTo&lt;T&gt;() hoạt động đúng với LINQ queries.
/// </summary>
public class DashboardServiceTests : IDisposable
{
    private readonly SmartMacroDbContext _db;
    private readonly IMapper _mapper;
    private readonly DashboardService _sut; // System Under Test

    public DashboardServiceTests()
    {
        // ──────────────────────────────────────────────────────────────
        // Setup InMemory Database — mỗi test instance có DB riêng biệt
        // nhờ unique database name, tránh cross-test contamination.
        // ──────────────────────────────────────────────────────────────
        var options = new DbContextOptionsBuilder<SmartMacroDbContext>()
            .UseInMemoryDatabase(databaseName: $"SmartMacro_Test_{Guid.NewGuid()}")
            .Options;

        _db = new SmartMacroDbContext(options);

        // ──────────────────────────────────────────────────────────────
        // Setup real AutoMapper — dùng cùng Profile với Production code
        // để đảm bảo mapping rules nhất quán.
        // ──────────────────────────────────────────────────────────────
        var mapperConfig = new MapperConfiguration(cfg =>
        {
            cfg.AddProfile<SmartMacroMappingProfile>();
        });
        mapperConfig.AssertConfigurationIsValid(); // Fail fast nếu mapping sai
        _mapper = mapperConfig.CreateMapper();

        // ──────────────────────────────────────────────────────────────
        // Tạo System Under Test
        // ──────────────────────────────────────────────────────────────
        _sut = new DashboardService(_db, _mapper);
    }

    public void Dispose()
    {
        _db.Database.EnsureDeleted();
        _db.Dispose();
    }

    // ══════════════════════════════════════════════════════════════════
    // Test Case 1: User không tồn tại → trả về null
    // ══════════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetUserDashboardAsync_UserNotFound_ReturnsNull()
    {
        // Arrange
        var nonExistentUserId = 999L;

        // Act
        var result = await _sut.GetUserDashboardAsync(nonExistentUserId);

        // Assert
        result.Should().BeNull("vì userId không tồn tại trong database");
    }

    // ══════════════════════════════════════════════════════════════════
    // Test Case 2: User tồn tại → trả về đúng UserDashboardResponseDto
    //              với DailyTarget và Inventory data tương ứng
    // ══════════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetUserDashboardAsync_UserExists_ReturnsDashboardDto()
    {
        // Arrange — Seed dữ liệu test
        var today = DateOnly.FromDateTime(DateTime.Now);
        const long userId = 1L;

        var user = new User
        {
            UserId = userId,
            FullName = "Nguyen Van A",
            GoalType = "cutting",
            Email = "test@example.com",
            PasswordHash = new string('x', 60),
            DateOfBirth = new DateOnly(1995, 5, 15),
            BiologicalSex = "male",
            ActivityLevel = "moderate",
            Status = "active",
            CreatedAt = DateTime.UtcNow,
            UpdatedAt = DateTime.UtcNow
        };

        var dailyTarget = new DailyTarget
        {
            TargetId = 1,
            UserId = userId,
            TargetDate = today,
            TargetKcal = 2000m,
            TargetProteinG = 150m,
            TargetCarbsG = 200m,
            TargetFatG = 70m,
            CreatedAt = DateTime.UtcNow
        };

        var food = new Food
        {
            FoodId = 1,
            FoodName = "Uc Ga",
            KcalPer100g = 165m,
            ProteinGPer100g = 31m,
            CarbsGPer100g = 0m,
            FatGPer100g = 3.6m,
            IsVerified = true,
            Source = "user_submitted",
            CreatedAt = DateTime.UtcNow
        };

        var inventory = new UserFoodInventory
        {
            InventoryId = 1,
            UserId = userId,
            FoodId = 1,
            QuantityGrams = 500m,
            Food = food,
            UpdatedAt = DateTime.UtcNow
        };

        _db.Users.Add(user);
        _db.DailyTargets.Add(dailyTarget);
        _db.Foods.Add(food);
        _db.UserFoodInventories.Add(inventory);
        await _db.SaveChangesAsync();

        // Act
        var result = await _sut.GetUserDashboardAsync(userId);

        // Assert — Kiểm tra composite DTO
        result.Should().NotBeNull("vì userId tồn tại trong database");

        // Kiểm tra thông tin User
        result!.UserId.Should().Be(userId);
        result.FullName.Should().Be("Nguyen Van A");
        result.GoalType.Should().Be("cutting");

        // Kiểm tra DailyTarget (macro hôm nay)
        result.TodayTarget.Should().NotBeNull("vì đã seed DailyTarget cho hôm nay");
        result.TodayTarget!.TargetKcal.Should().Be(2000m);
        result.TodayTarget.TargetProteinG.Should().Be(150m);
        result.TodayTarget.TargetCarbsG.Should().Be(200m);
        result.TodayTarget.TargetFatG.Should().Be(70m);

        // Kiểm tra Inventory
        result.AvailableInventory.Should().HaveCount(1);
        result.AvailableInventory[0].FoodName.Should().Be("Uc Ga");
        result.AvailableInventory[0].QuantityGrams.Should().Be(500m);
        result.AvailableInventory[0].KcalPer100g.Should().Be(165m);
        result.AvailableInventory[0].ProteinGPer100g.Should().Be(31m);
    }

    // ══════════════════════════════════════════════════════════════════
    // Test Case 3: User tồn tại nhưng không có DailyTarget & Inventory trống
    // → TodayTarget = null, AvailableInventory = empty list
    // ══════════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetUserDashboardAsync_UserExistsNoTargetNoInventory_ReturnsDto_WithNullTargetAndEmptyInventory()
    {
        // Arrange
        const long userId = 2L;

        var user = new User
        {
            UserId = userId,
            FullName = "Tran Thi B",
            GoalType = "bulking",
            Email = "b@example.com",
            PasswordHash = new string('x', 60),
            DateOfBirth = new DateOnly(1998, 3, 20),
            BiologicalSex = "female",
            ActivityLevel = "high",
            Status = "active",
            CreatedAt = DateTime.UtcNow,
            UpdatedAt = DateTime.UtcNow
        };

        _db.Users.Add(user);
        await _db.SaveChangesAsync();

        // Act
        var result = await _sut.GetUserDashboardAsync(userId);

        // Assert
        result.Should().NotBeNull();
        result!.UserId.Should().Be(userId);
        result.FullName.Should().Be("Tran Thi B");
        result.GoalType.Should().Be("bulking");

        result.TodayTarget.Should().BeNull("vì chưa có DailyTarget cho ngày hôm nay");
        result.AvailableInventory.Should().BeEmpty("vì kho thực phẩm trống");
    }

    // ══════════════════════════════════════════════════════════════════
    // Test Case 4: Inventory chỉ trả về items có QuantityGrams > 0
    // → Items với quantity = 0 phải bị loại khỏi kết quả
    // ══════════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetUserDashboardAsync_InventoryWithZeroQuantity_ExcludesEmptyItems()
    {
        // Arrange
        const long userId = 3L;

        var user = new User
        {
            UserId = userId,
            FullName = "Le Van C",
            GoalType = "maintenance",
            Email = "c@example.com",
            PasswordHash = new string('x', 60),
            DateOfBirth = new DateOnly(1990, 1, 1),
            BiologicalSex = "male",
            ActivityLevel = "low",
            Status = "active",
            CreatedAt = DateTime.UtcNow,
            UpdatedAt = DateTime.UtcNow
        };

        var food1 = new Food
        {
            FoodId = 10,
            FoodName = "Com Trang",
            KcalPer100g = 130m,
            ProteinGPer100g = 2.7m,
            CarbsGPer100g = 28m,
            FatGPer100g = 0.3m,
            IsVerified = true,
            Source = "user_submitted",
            CreatedAt = DateTime.UtcNow
        };

        var food2 = new Food
        {
            FoodId = 11,
            FoodName = "Trung Ga",
            KcalPer100g = 155m,
            ProteinGPer100g = 13m,
            CarbsGPer100g = 1.1m,
            FatGPer100g = 11m,
            IsVerified = true,
            Source = "user_submitted",
            CreatedAt = DateTime.UtcNow
        };

        // Inventory item CÒN hàng (quantity > 0)
        var inventoryWithStock = new UserFoodInventory
        {
            InventoryId = 10,
            UserId = userId,
            FoodId = 10,
            QuantityGrams = 300m,
            Food = food1,
            UpdatedAt = DateTime.UtcNow
        };

        // Inventory item HẾT hàng (quantity = 0) — phải bị loại
        var inventoryEmpty = new UserFoodInventory
        {
            InventoryId = 11,
            UserId = userId,
            FoodId = 11,
            QuantityGrams = 0m,
            Food = food2,
            UpdatedAt = DateTime.UtcNow
        };

        _db.Users.Add(user);
        _db.Foods.AddRange(food1, food2);
        _db.UserFoodInventories.AddRange(inventoryWithStock, inventoryEmpty);
        await _db.SaveChangesAsync();

        // Act
        var result = await _sut.GetUserDashboardAsync(userId);

        // Assert
        result.Should().NotBeNull();
        result!.AvailableInventory.Should().HaveCount(1,
            "chỉ inventory có QuantityGrams > 0 mới được trả về");
        result.AvailableInventory[0].FoodName.Should().Be("Com Trang");
        result.AvailableInventory[0].QuantityGrams.Should().Be(300m);
    }
}
