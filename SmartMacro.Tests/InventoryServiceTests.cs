using AutoMapper;
using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Models;
using SmartMacro.Api.Profiles;
using SmartMacro.Api.Services;

namespace SmartMacro.Tests;

public class InventoryServiceTests : IDisposable
{
    private readonly SmartMacroDbContext _db;
    private readonly IMapper _mapper;
    private readonly InventoryService _sut;

    public InventoryServiceTests()
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

        _sut = new InventoryService(_db, _mapper);
    }

    public void Dispose()
    {
        _db.Database.EnsureDeleted();
        _db.Dispose();
    }

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

    private Food SeedFood(long id, string name)
    {
        var food = new Food { FoodId = id, FoodName = name, Source = "test" };
        _db.Foods.Add(food);
        return food;
    }

    private UserFoodInventory SeedInventory(long inventoryId, long userId, long foodId, decimal qty)
    {
        var inv = new UserFoodInventory { InventoryId = inventoryId, UserId = userId, FoodId = foodId, QuantityGrams = qty, UpdatedAt = DateTime.UtcNow };
        _db.UserFoodInventories.Add(inv);
        return inv;
    }

    [Fact]
    public async Task GetMyInventoryAsync_ReturnsOnlyUserRecords()
    {
        // Arrange
        SeedUser(1); SeedUser(2);
        SeedFood(1, "Ga");
        SeedInventory(1, 1, 1, 100m); // User 1
        SeedInventory(2, 2, 1, 200m); // User 2
        await _db.SaveChangesAsync();

        // Act
        var result = await _sut.GetMyInventoryAsync(1);

        // Assert
        result.Should().HaveCount(1);
        result[0].InventoryId.Should().Be(1);
        result[0].QuantityGrams.Should().Be(100m);
    }

    [Fact]
    public async Task AddItemAsync_ValidData_CreatesNewRecord()
    {
        // Arrange
        SeedUser(1);
        SeedFood(1, "Ga");
        await _db.SaveChangesAsync();

        var request = new CreateInventoryItemRequestDto { FoodId = 1, QuantityGrams = 150m };

        // Act
        var result = await _sut.AddItemAsync(1, request);

        // Assert
        result.Should().NotBeNull();
        result.InventoryId.Should().BeGreaterThan(0);
        result.FoodId.Should().Be(1);
        result.FoodName.Should().Be("Ga");
        result.QuantityGrams.Should().Be(150m);

        var inDb = await _db.UserFoodInventories.SingleAsync();
        inDb.UserId.Should().Be(1);
        inDb.QuantityGrams.Should().Be(150m);
    }

    [Fact]
    public async Task AddItemAsync_FoodDoesNotExist_ThrowsNotFoundException()
    {
        var request = new CreateInventoryItemRequestDto { FoodId = 999, QuantityGrams = 100m };
        await _sut.Invoking(s => s.AddItemAsync(1, request))
            .Should().ThrowAsync<NotFoundException>();
    }

    [Fact]
    public async Task AddItemAsync_ExistingFood_MergesQuantity()
    {
        // Arrange
        SeedUser(1);
        SeedFood(1, "Ga");
        SeedInventory(1, 1, 1, 100m);
        await _db.SaveChangesAsync();

        var request = new CreateInventoryItemRequestDto { FoodId = 1, QuantityGrams = 50m };

        // Act
        var result = await _sut.AddItemAsync(1, request);

        // Assert
        result.InventoryId.Should().Be(1); // Same ID
        result.QuantityGrams.Should().Be(150m); // Merged

        var inDb = await _db.UserFoodInventories.ToListAsync();
        inDb.Should().HaveCount(1);
        inDb[0].QuantityGrams.Should().Be(150m);
    }

    [Fact]
    public async Task AddItemAsync_ZeroOrNegativeQuantity_ThrowsArgumentException()
    {
        var request = new CreateInventoryItemRequestDto { FoodId = 1, QuantityGrams = 0m };
        await _sut.Invoking(s => s.AddItemAsync(1, request))
            .Should().ThrowAsync<ArgumentException>();
    }

    [Fact]
    public async Task UpdateItemAsync_Valid_UpdatesQuantity()
    {
        SeedUser(1); SeedFood(1, "Ga");
        SeedInventory(1, 1, 1, 100m);
        await _db.SaveChangesAsync();

        var request = new UpdateInventoryItemRequestDto { QuantityGrams = 120m };

        var result = await _sut.UpdateItemAsync(1, 1, request);

        result.QuantityGrams.Should().Be(120m);
        var inDb = await _db.UserFoodInventories.FindAsync(1L);
        inDb!.QuantityGrams.Should().Be(120m);
    }

    [Fact]
    public async Task UpdateItemAsync_OtherUserItem_ThrowsNotFoundException()
    {
        SeedUser(1); SeedUser(2); SeedFood(1, "Ga");
        SeedInventory(1, 2, 1, 100m); // Belongs to User 2
        await _db.SaveChangesAsync();

        var request = new UpdateInventoryItemRequestDto { QuantityGrams = 120m };

        await _sut.Invoking(s => s.UpdateItemAsync(1, 1, request)) // User 1 tries to update User 2's item
            .Should().ThrowAsync<NotFoundException>();
    }

    [Fact]
    public async Task DeleteItemAsync_Valid_RemovesItem()
    {
        SeedUser(1); SeedFood(1, "Ga");
        SeedInventory(1, 1, 1, 100m);
        await _db.SaveChangesAsync();

        await _sut.DeleteItemAsync(1, 1);

        var inDb = await _db.UserFoodInventories.FindAsync(1L);
        inDb.Should().BeNull();
    }

    [Fact]
    public async Task DeleteItemAsync_OtherUserItem_ThrowsNotFoundException()
    {
        SeedUser(1); SeedUser(2); SeedFood(1, "Ga");
        SeedInventory(1, 2, 1, 100m);
        await _db.SaveChangesAsync();

        await _sut.Invoking(s => s.DeleteItemAsync(1, 1))
            .Should().ThrowAsync<NotFoundException>();
    }
}
