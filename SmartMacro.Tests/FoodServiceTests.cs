using AutoMapper;
using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Models;
using SmartMacro.Api.Profiles;
using SmartMacro.Api.Services;

namespace SmartMacro.Tests;

/// <summary>
/// Unit tests cho <see cref="FoodService"/>.
/// Sử dụng EF Core InMemory Database + real AutoMapper configuration
/// để đảm bảo ProjectTo&lt;T&gt;() hoạt động đúng với LINQ queries.
/// Pattern: Guid-based DB isolation (giống DashboardServiceTests).
/// </summary>
public class FoodServiceTests : IDisposable
{
    private readonly SmartMacroDbContext _db;
    private readonly IMapper _mapper;
    private readonly FoodService _sut;

    public FoodServiceTests()
    {
        var options = new DbContextOptionsBuilder<SmartMacroDbContext>()
            .UseInMemoryDatabase(databaseName: $"SmartMacro_Test_{Guid.NewGuid()}")
            .Options;

        _db = new SmartMacroDbContext(options);

        var mapperConfig = new MapperConfiguration(cfg =>
        {
            cfg.AddProfile<SmartMacroMappingProfile>();
        }, Microsoft.Extensions.Logging.Abstractions.NullLoggerFactory.Instance);
        mapperConfig.AssertConfigurationIsValid();
        _mapper = mapperConfig.CreateMapper();

        _sut = new FoodService(_db, _mapper);
    }

    public void Dispose()
    {
        _db.Database.EnsureDeleted();
        _db.Dispose();
    }

    // ── Seed Helpers ────────────────────────────────────────────────

    private FoodCategory SeedCategory(short id = 1, string name = "Protein")
    {
        var category = new FoodCategory { CategoryId = id, CategoryName = name };
        _db.FoodCategories.Add(category);
        return category;
    }

    private Food SeedFood(
        long id, string name, short? categoryId = 1,
        decimal kcal = 165m, decimal protein = 31m, decimal carbs = 0m, decimal fat = 3.6m)
    {
        var food = new Food
        {
            FoodId = id,
            FoodName = name,
            CategoryId = categoryId,
            KcalPer100g = kcal,
            ProteinGPer100g = protein,
            CarbsGPer100g = carbs,
            FatGPer100g = fat,
            IsVerified = true,
            Source = "user_submitted",
            CreatedAt = DateTime.UtcNow
        };
        _db.Foods.Add(food);
        return food;
    }

    // ── Search Tests ────────────────────────────────────────────────

    [Fact]
    public async Task SearchFoodsAsync_WithKeyword_ReturnsMatchingFoods()
    {
        // Arrange
        SeedCategory();
        SeedFood(1, "Uc Ga");
        SeedFood(2, "Ga Quay");
        SeedFood(3, "Com Trang", kcal: 130m, protein: 2.7m, carbs: 28m, fat: 0.3m);
        await _db.SaveChangesAsync();

        var request = new FoodSearchRequestDto { Keyword = "Ga", Page = 1, PageSize = 10 };

        // Act
        var result = await _sut.SearchFoodsAsync(request);

        // Assert
        result.Should().NotBeNull();
        result.TotalCount.Should().Be(2);
        result.Items.Should().HaveCount(2);
        result.Items.Should().AllSatisfy(f => f.FoodName.Should().Contain("Ga"));
        result.Page.Should().Be(1);
        result.PageSize.Should().Be(10);
        result.TotalPages.Should().Be(1);
    }

    [Fact]
    public async Task SearchFoodsAsync_NoMatch_ReturnsEmptyList()
    {
        // Arrange
        SeedCategory();
        SeedFood(1, "Uc Ga");
        await _db.SaveChangesAsync();

        var request = new FoodSearchRequestDto { Keyword = "XYZ_KHONG_TON_TAI", Page = 1, PageSize = 10 };

        // Act
        var result = await _sut.SearchFoodsAsync(request);

        // Assert
        result.Should().NotBeNull();
        result.TotalCount.Should().Be(0);
        result.Items.Should().BeEmpty();
        result.HasNextPage.Should().BeFalse();
    }

    [Fact]
    public async Task SearchFoodsAsync_FilterByCategoryId_ReturnsFilteredFoods()
    {
        // Arrange
        SeedCategory(1, "Protein");
        SeedCategory(2, "Carbs");
        SeedFood(1, "Uc Ga", categoryId: 1);
        SeedFood(2, "Com Trang", categoryId: 2, kcal: 130m, protein: 2.7m, carbs: 28m, fat: 0.3m);
        SeedFood(3, "Trung Ga", categoryId: 1);
        await _db.SaveChangesAsync();

        var request = new FoodSearchRequestDto { CategoryId = 1, Page = 1, PageSize = 10 };

        // Act
        var result = await _sut.SearchFoodsAsync(request);

        // Assert
        result.TotalCount.Should().Be(2);
        result.Items.Should().HaveCount(2);
        result.Items.Should().AllSatisfy(f => f.CategoryId.Should().Be(1));
    }

    [Fact]
    public async Task SearchFoodsAsync_Pagination_ReturnsCorrectPage()
    {
        // Arrange
        SeedCategory();
        for (int i = 1; i <= 5; i++)
            SeedFood(i, $"Food_{i:D2}");
        await _db.SaveChangesAsync();

        var request = new FoodSearchRequestDto { Page = 2, PageSize = 2 };

        // Act
        var result = await _sut.SearchFoodsAsync(request);

        // Assert
        result.TotalCount.Should().Be(5);
        result.Items.Should().HaveCount(2);
        result.Page.Should().Be(2);
        result.TotalPages.Should().Be(3);
        result.HasNextPage.Should().BeTrue();
        result.HasPreviousPage.Should().BeTrue();
    }

    [Fact]
    public async Task SearchFoodsAsync_IncludesCategoryName_ViaProjectTo()
    {
        // Arrange
        SeedCategory(1, "Thit");
        SeedFood(1, "Uc Ga", categoryId: 1);
        await _db.SaveChangesAsync();

        var request = new FoodSearchRequestDto { Page = 1, PageSize = 10 };

        // Act
        var result = await _sut.SearchFoodsAsync(request);

        // Assert — CategoryName phải được project từ navigation, không null
        result.Items.Should().ContainSingle();
        result.Items[0].CategoryName.Should().Be("Thit");
        result.Items[0].CategoryId.Should().Be(1);
    }

    // ── GetById Tests ───────────────────────────────────────────────

    [Fact]
    public async Task GetFoodByIdAsync_FoodExists_ReturnsFoodDto()
    {
        // Arrange
        SeedCategory(1, "Protein");
        SeedFood(1, "Uc Ga", categoryId: 1);
        await _db.SaveChangesAsync();

        // Act
        var result = await _sut.GetFoodByIdAsync(1);

        // Assert
        result.Should().NotBeNull();
        result.FoodId.Should().Be(1);
        result.FoodName.Should().Be("Uc Ga");
        result.CategoryName.Should().Be("Protein");
        result.KcalPer100g.Should().Be(165m);
        result.ProteinGPer100g.Should().Be(31m);
    }

    [Fact]
    public async Task GetFoodByIdAsync_FoodNotFound_ThrowsNotFoundException()
    {
        // Act & Assert
        await _sut.Invoking(s => s.GetFoodByIdAsync(999))
            .Should().ThrowAsync<NotFoundException>();
    }

    // ── Create Tests ────────────────────────────────────────────────

    [Fact]
    public async Task CreateFoodAsync_ValidData_ReturnsFoodResponseDto()
    {
        // Arrange
        SeedCategory(1, "Protein");
        await _db.SaveChangesAsync();

        var request = new CreateFoodRequestDto
        {
            FoodName = "Uc Ga Moi",
            CategoryId = 1,
            KcalPer100g = 165m,
            ProteinGPer100g = 31m,
            CarbsGPer100g = 0m,
            FatGPer100g = 3.6m,
            FiberGPer100g = 0.5m
        };

        // Act
        var result = await _sut.CreateFoodAsync(request);

        // Assert
        result.Should().NotBeNull();
        result.FoodId.Should().BeGreaterThan(0);
        result.FoodName.Should().Be("Uc Ga Moi");
        result.CategoryId.Should().Be(1);
        result.CategoryName.Should().Be("Protein");
        result.KcalPer100g.Should().Be(165m);
        result.FiberGPer100g.Should().Be(0.5m);
        result.IsVerified.Should().BeFalse("vì food mới luôn chưa verified");
        result.Source.Should().Be("user_submitted");
    }

    [Fact]
    public async Task CreateFoodAsync_InvalidCategoryId_ThrowsNotFoundException()
    {
        // Arrange — không seed category nào
        var request = new CreateFoodRequestDto
        {
            FoodName = "Test Food",
            CategoryId = 999,
            KcalPer100g = 100m,
            ProteinGPer100g = 10m,
            CarbsGPer100g = 10m,
            FatGPer100g = 5m
        };

        // Act & Assert
        await _sut.Invoking(s => s.CreateFoodAsync(request))
            .Should().ThrowAsync<NotFoundException>()
            .WithMessage("*999*");
    }

    [Fact]
    public async Task CreateFoodAsync_NullCategoryId_Succeeds()
    {
        // Arrange — CategoryId là optional (short?)
        var request = new CreateFoodRequestDto
        {
            FoodName = "Food Khong Co Category",
            CategoryId = null,
            KcalPer100g = 100m,
            ProteinGPer100g = 10m,
            CarbsGPer100g = 20m,
            FatGPer100g = 5m
        };

        // Act
        var result = await _sut.CreateFoodAsync(request);

        // Assert
        result.Should().NotBeNull();
        result.CategoryId.Should().BeNull();
        result.CategoryName.Should().BeNull();
    }

    // ── Update Tests ────────────────────────────────────────────────

    [Fact]
    public async Task UpdateFoodAsync_ValidData_ReturnsUpdatedFood()
    {
        // Arrange
        SeedCategory(1, "Protein");
        SeedCategory(2, "Carbs");
        SeedFood(1, "Uc Ga", categoryId: 1);
        await _db.SaveChangesAsync();

        var request = new UpdateFoodRequestDto
        {
            FoodName = "Uc Ga Updated",
            CategoryId = 2,
            KcalPer100g = 170m,
            ProteinGPer100g = 32m,
            CarbsGPer100g = 1m,
            FatGPer100g = 4m
        };

        // Act
        var result = await _sut.UpdateFoodAsync(1, request);

        // Assert
        result.Should().NotBeNull();
        result.FoodName.Should().Be("Uc Ga Updated");
        result.CategoryId.Should().Be(2);
        result.CategoryName.Should().Be("Carbs");
        result.KcalPer100g.Should().Be(170m);
    }

    [Fact]
    public async Task UpdateFoodAsync_FoodNotFound_ThrowsNotFoundException()
    {
        // Arrange
        var request = new UpdateFoodRequestDto
        {
            FoodName = "Test",
            KcalPer100g = 100m,
            ProteinGPer100g = 10m,
            CarbsGPer100g = 10m,
            FatGPer100g = 5m
        };

        // Act & Assert
        await _sut.Invoking(s => s.UpdateFoodAsync(999, request))
            .Should().ThrowAsync<NotFoundException>();
    }

    [Fact]
    public async Task UpdateFoodAsync_InvalidCategoryId_ThrowsNotFoundException()
    {
        // Arrange
        SeedCategory(1, "Protein");
        SeedFood(1, "Uc Ga", categoryId: 1);
        await _db.SaveChangesAsync();

        var request = new UpdateFoodRequestDto
        {
            FoodName = "Uc Ga",
            CategoryId = 999,
            KcalPer100g = 165m,
            ProteinGPer100g = 31m,
            CarbsGPer100g = 0m,
            FatGPer100g = 3.6m
        };

        // Act & Assert
        await _sut.Invoking(s => s.UpdateFoodAsync(1, request))
            .Should().ThrowAsync<NotFoundException>()
            .WithMessage("*999*");
    }

    // ── Delete Tests ────────────────────────────────────────────────

    [Fact]
    public async Task DeleteFoodAsync_FoodExists_RemovesFromDb()
    {
        // Arrange
        SeedCategory();
        SeedFood(1, "Uc Ga");
        await _db.SaveChangesAsync();

        // Act
        await _sut.DeleteFoodAsync(1);

        // Assert — entity không còn trong DB
        var foodInDb = await _db.Foods.FindAsync(1L);
        foodInDb.Should().BeNull("vì food đã bị xóa");

        // Double-check qua GetById
        await _sut.Invoking(s => s.GetFoodByIdAsync(1))
            .Should().ThrowAsync<NotFoundException>();
    }

    [Fact]
    public async Task DeleteFoodAsync_FoodNotFound_ThrowsNotFoundException()
    {
        // Act & Assert
        await _sut.Invoking(s => s.DeleteFoodAsync(999))
            .Should().ThrowAsync<NotFoundException>();
    }
}
