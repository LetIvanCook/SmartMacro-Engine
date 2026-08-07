using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using FluentAssertions;
using SmartMacro.Api.DTOs;

namespace SmartMacro.Tests.IntegrationTests;

public class FoodCategoryIntegrationTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly HttpClient _client;
    private string? _token;

    public FoodCategoryIntegrationTests(CustomWebApplicationFactory factory)
    {
        _client = factory.CreateClient();
    }

    private async Task AuthenticateAsync()
    {
        if (_token != null)
        {
            _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", _token);
            return;
        }

        var email = $"categorytest{Guid.NewGuid()}@example.com";
        var request = new RegisterRequestDto
        {
            Email = email,
            Password = "Password123!",
            FullName = "Category Test User",
            DateOfBirth = new DateOnly(1990, 1, 1),
            BiologicalSex = "male",
            ActivityLevel = "active",
            GoalType = "cutting"
        };
        var response = await _client.PostAsJsonAsync("/api/auth/register", request);
        var authData = await response.Content.ReadFromJsonAsync<AuthResponseDto>();
        _token = authData!.Token;
        _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", _token);
    }

    [Fact]
    public async Task Create_ValidData_ReturnsCreatedAndCategory()
    {
        await AuthenticateAsync();

        var createRequest = new CreateFoodCategoryRequestDto { CategoryName = $"Cat_{Guid.NewGuid()}" };
        var response = await _client.PostAsJsonAsync("/api/food-categories", createRequest);

        response.StatusCode.Should().Be(HttpStatusCode.Created);
        var category = await response.Content.ReadFromJsonAsync<FoodCategoryResponseDto>();
        category.Should().NotBeNull();
        category!.CategoryName.Should().Be(createRequest.CategoryName);
    }

    [Fact]
    public async Task GetAll_ReturnsOkAndList()
    {
        await AuthenticateAsync();

        var createRequest = new CreateFoodCategoryRequestDto { CategoryName = $"Cat_{Guid.NewGuid()}" };
        var createResp = await _client.PostAsJsonAsync("/api/food-categories", createRequest);
        var created = await createResp.Content.ReadFromJsonAsync<FoodCategoryResponseDto>();

        var response = await _client.GetAsync("/api/food-categories");

        response.StatusCode.Should().Be(HttpStatusCode.OK);
        var categories = await response.Content.ReadFromJsonAsync<List<FoodCategoryResponseDto>>();
        categories.Should().NotBeNull();
        categories.Should().Contain(c => c.CategoryId == created!.CategoryId);
    }

    [Fact]
    public async Task Update_ValidData_ReturnsOk()
    {
        await AuthenticateAsync();

        var createRequest = new CreateFoodCategoryRequestDto { CategoryName = $"Cat_{Guid.NewGuid()}" };
        var createResp = await _client.PostAsJsonAsync("/api/food-categories", createRequest);
        var created = await createResp.Content.ReadFromJsonAsync<FoodCategoryResponseDto>();

        var updateRequest = new UpdateFoodCategoryRequestDto { CategoryName = $"Updated_{Guid.NewGuid()}" };
        var response = await _client.PutAsJsonAsync($"/api/food-categories/{created!.CategoryId}", updateRequest);

        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var getResp = await _client.GetAsync("/api/food-categories");
        var categories = await getResp.Content.ReadFromJsonAsync<List<FoodCategoryResponseDto>>();
        categories!.First(c => c.CategoryId == created.CategoryId).CategoryName.Should().Be(updateRequest.CategoryName);
    }

    [Fact]
    public async Task Update_NonExistentId_ReturnsNotFound()
    {
        await AuthenticateAsync();

        var updateRequest = new UpdateFoodCategoryRequestDto { CategoryName = "NonExistent" };
        var response = await _client.PutAsJsonAsync("/api/food-categories/32000", updateRequest);

        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task Delete_ExistingId_ReturnsNoContent()
    {
        await AuthenticateAsync();

        var createRequest = new CreateFoodCategoryRequestDto { CategoryName = $"Cat_{Guid.NewGuid()}" };
        var createResp = await _client.PostAsJsonAsync("/api/food-categories", createRequest);
        var created = await createResp.Content.ReadFromJsonAsync<FoodCategoryResponseDto>();

        var response = await _client.DeleteAsync($"/api/food-categories/{created!.CategoryId}");

        response.StatusCode.Should().Be(HttpStatusCode.NoContent);
    }

    [Fact]
    public async Task Delete_NonExistentId_ReturnsNotFound()
    {
        await AuthenticateAsync();

        var response = await _client.DeleteAsync("/api/food-categories/32000");

        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task Delete_CategoryWithLinkedFood_ReturnsConflict()
    {
        await AuthenticateAsync();

        // 1. Create Category
        var createCatReq = new CreateFoodCategoryRequestDto { CategoryName = $"LinkedCat_{Guid.NewGuid()}" };
        var createCatResp = await _client.PostAsJsonAsync("/api/food-categories", createCatReq);
        var category = await createCatResp.Content.ReadFromJsonAsync<FoodCategoryResponseDto>();

        // 2. Create Food referencing Category
        var createFoodReq = new CreateFoodRequestDto
        {
            FoodName = $"LinkedFood_{Guid.NewGuid()}",
            CategoryId = category!.CategoryId,
            KcalPer100g = 100,
            ProteinGPer100g = 10,
            CarbsGPer100g = 10,
            FatGPer100g = 10
        };
        var createFoodResp = await _client.PostAsJsonAsync("/api/foods", createFoodReq);
        createFoodResp.StatusCode.Should().Be(HttpStatusCode.Created);

        // 3. Try to delete Category -> Conflict
        var deleteResp = await _client.DeleteAsync($"/api/food-categories/{category.CategoryId}");
        deleteResp.StatusCode.Should().Be(HttpStatusCode.Conflict);
    }
}
