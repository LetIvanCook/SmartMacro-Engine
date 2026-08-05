using AutoMapper;
using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using Moq;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Engines;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Models;
using SmartMacro.Api.Profiles;
using SmartMacro.Api.Services;

namespace SmartMacro.Tests;

public class OptimizationServiceTests : IDisposable
{
    private readonly SmartMacroDbContext _db;
    private readonly IMapper _mapper;
    private readonly Mock<IMacroOptimizationEngine> _mockEngine;
    private readonly OptimizationService _sut;

    public OptimizationServiceTests()
    {
        var options = new DbContextOptionsBuilder<SmartMacroDbContext>()
            .UseInMemoryDatabase(databaseName: $"SmartMacro_Test_{Guid.NewGuid()}")
            .Options;

        _db = new SmartMacroDbContext(options);

        var mapperConfig = new MapperConfiguration(cfg =>
        {
            cfg.AddProfile<SmartMacroMappingProfile>();
        });
        mapperConfig.AssertConfigurationIsValid();
        _mapper = mapperConfig.CreateMapper();

        _mockEngine = new Mock<IMacroOptimizationEngine>();

        _sut = new OptimizationService(_db, _mapper, _mockEngine.Object);
    }

    public void Dispose()
    {
        _db.Database.EnsureDeleted();
        _db.Dispose();
    }

    [Fact]
    public async Task GenerateMealPlanAsync_TargetNotFound_ThrowsNotFoundException()
    {
        // Arrange
        var userId = 1L;
        var request = new OptimizationRequestDto { DailyTargetId = 999 };

        // Act & Assert
        await _sut.Invoking(s => s.GenerateMealPlanAsync(userId, request))
            .Should().ThrowAsync<NotFoundException>();
    }

    [Fact]
    public async Task GenerateMealPlanAsync_EmptyInventory_ThrowsEmptyInventoryException()
    {
        // Arrange
        var userId = 2L;
        var today = DateOnly.FromDateTime(DateTime.UtcNow);
        
        var dailyTarget = new DailyTarget
        {
            TargetId = 1,
            UserId = userId,
            TargetDate = today,
            TargetKcal = 2000m,
            CreatedAt = DateTime.UtcNow
        };
        _db.DailyTargets.Add(dailyTarget);
        await _db.SaveChangesAsync();

        var request = new OptimizationRequestDto();

        // Act & Assert
        await _sut.Invoking(s => s.GenerateMealPlanAsync(userId, request))
            .Should().ThrowAsync<EmptyInventoryException>();
    }

    [Fact]
    public async Task GenerateMealPlanAsync_Infeasible_ReturnsInfeasibleStatusWithoutThrowing()
    {
        // Arrange
        var userId = 3L;
        var today = DateOnly.FromDateTime(DateTime.UtcNow);
        
        var dailyTarget = new DailyTarget
        {
            TargetId = 2,
            UserId = userId,
            TargetDate = today,
            TargetKcal = 2000m,
            TargetProteinG = 150m,
            TargetCarbsG = 200m,
            TargetFatG = 70m,
            CreatedAt = DateTime.UtcNow
        };
        
        var food = new Food { FoodId = 1, FoodName = "Ga", KcalPer100g = 100, Source = "user_submitted", CreatedAt = DateTime.UtcNow };
        var inventory = new UserFoodInventory { InventoryId = 1, UserId = userId, FoodId = 1, QuantityGrams = 100, Food = food, UpdatedAt = DateTime.UtcNow };
        
        _db.DailyTargets.Add(dailyTarget);
        _db.Foods.Add(food);
        _db.UserFoodInventories.Add(inventory);
        await _db.SaveChangesAsync();

        _mockEngine.Setup(e => e.CalculateOptimalMeal(It.IsAny<DailyTargetDto>(), It.IsAny<List<InventoryItemDto>>()))
            .Returns(new OptimizationResult
            {
                IsSuccessful = false,
                Message = "Infeasible constraint"
            });

        var request = new OptimizationRequestDto();

        // Act
        var result = await _sut.GenerateMealPlanAsync(userId, request);

        // Assert
        result.Should().NotBeNull();
        result.SolverStatus.Should().Be("INFEASIBLE");
        result.AllocatedItems.Should().BeEmpty();
    }

    [Fact]
    public async Task GenerateMealPlanAsync_HappyPath_ReturnsOptimalStatusAndAllocations()
    {
        // Arrange
        var userId = 4L;
        var today = DateOnly.FromDateTime(DateTime.UtcNow);
        
        var dailyTarget = new DailyTarget
        {
            TargetId = 3,
            UserId = userId,
            TargetDate = today,
            TargetKcal = 2000m,
            TargetProteinG = 150m,
            TargetCarbsG = 200m,
            TargetFatG = 70m,
            CreatedAt = DateTime.UtcNow
        };
        
        var food = new Food { FoodId = 2, FoodName = "Uc Ga", KcalPer100g = 165m, ProteinGPer100g = 31m, CarbsGPer100g = 0m, FatGPer100g = 3.6m, Source = "user_submitted", CreatedAt = DateTime.UtcNow };
        var inventory = new UserFoodInventory { InventoryId = 2, UserId = userId, FoodId = 2, QuantityGrams = 500m, Food = food, UpdatedAt = DateTime.UtcNow };
        
        _db.DailyTargets.Add(dailyTarget);
        _db.Foods.Add(food);
        _db.UserFoodInventories.Add(inventory);
        await _db.SaveChangesAsync();

        var mockEngineResult = new OptimizationResult
        {
            IsSuccessful = true,
            Message = "Tìm được nghiệm tối ưu (OPTIMAL).",
            TotalKcal = 1990m,
            TotalProtein = 151m,
            TotalCarbs = 198m,
            TotalFat = 69m,
            Items = new List<OptimizedFoodItem>
            {
                new OptimizedFoodItem { FoodId = 2, FoodName = "Uc Ga", CalculatedGrams = 300m }
            }
        };

        _mockEngine.Setup(e => e.CalculateOptimalMeal(It.IsAny<DailyTargetDto>(), It.IsAny<List<InventoryItemDto>>()))
            .Returns(mockEngineResult);

        var request = new OptimizationRequestDto();

        // Act
        var result = await _sut.GenerateMealPlanAsync(userId, request);

        // Assert
        result.Should().NotBeNull();
        result.SolverStatus.Should().Be("OPTIMAL");
        result.AchievedMacros.Kcal.Should().Be(1990m);
        result.AllocatedItems.Should().HaveCount(1);
        result.AllocatedItems[0].QuantityGrams.Should().Be(300m);
        result.AllocatedItems[0].FoodName.Should().Be("Uc Ga");
    }
}
