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
/// Unit tests cho <see cref="FoodCategoryService"/>.
/// Sử dụng EF Core InMemory Database + real AutoMapper configuration.
/// </summary>
public class FoodCategoryServiceTests : IDisposable
{
    private readonly SmartMacroDbContext _db;
    private readonly IMapper _mapper;
    private readonly FoodCategoryService _sut;

    public FoodCategoryServiceTests()
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

        _sut = new FoodCategoryService(_db, _mapper);
    }

    public void Dispose()
    {
        _db.Database.EnsureDeleted();
        _db.Dispose();
    }

    [Fact]
    public async Task GetAllCategoriesAsync_ReturnsAllCategories_OrderedByName()
    {
        // Arrange
        _db.FoodCategories.Add(new FoodCategory { CategoryId = 1, CategoryName = "Protein" });
        _db.FoodCategories.Add(new FoodCategory { CategoryId = 2, CategoryName = "Carbs" });
        _db.FoodCategories.Add(new FoodCategory { CategoryId = 3, CategoryName = "Fat" });
        await _db.SaveChangesAsync();

        // Act
        var result = await _sut.GetAllCategoriesAsync();

        // Assert
        result.Should().HaveCount(3);
        result[0].CategoryName.Should().Be("Carbs", "vì danh sách được sắp xếp theo tên");
        result[1].CategoryName.Should().Be("Fat");
        result[2].CategoryName.Should().Be("Protein");
    }

    [Fact]
    public async Task GetAllCategoriesAsync_EmptyDb_ReturnsEmptyList()
    {
        // Act
        var result = await _sut.GetAllCategoriesAsync();

        // Assert
        result.Should().BeEmpty();
    }

    [Fact]
    public async Task CreateCategoryAsync_ValidData_ReturnsCategoryDto()
    {
        // Arrange
        var request = new CreateFoodCategoryRequestDto
        {
            CategoryName = "Protein"
        };

        // Act
        var result = await _sut.CreateCategoryAsync(request);

        // Assert
        result.Should().NotBeNull();
        result.CategoryId.Should().BeGreaterThan(0);
        result.CategoryName.Should().Be("Protein");

        // Verify entity đã được lưu vào DB
        var inDb = await _db.FoodCategories.FindAsync(result.CategoryId);
        inDb.Should().NotBeNull();
        inDb!.CategoryName.Should().Be("Protein");
    }

    [Fact]
    public async Task CreateCategoryAsync_DuplicateName_ThrowsConflictException()
    {
        // Arrange — seed category "Protein" trước
        _db.FoodCategories.Add(new FoodCategory { CategoryId = 1, CategoryName = "Protein" });
        await _db.SaveChangesAsync();

        var request = new CreateFoodCategoryRequestDto
        {
            CategoryName = "Protein"
        };

        // Act & Assert
        await _sut.Invoking(s => s.CreateCategoryAsync(request))
            .Should().ThrowAsync<ConflictException>()
            .WithMessage("*Protein*đã tồn tại*");
    }
}
