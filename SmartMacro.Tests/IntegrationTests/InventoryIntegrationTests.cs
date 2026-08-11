using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using FluentAssertions;
using SmartMacro.Api.DTOs;

namespace SmartMacro.Tests.IntegrationTests;

public class InventoryIntegrationTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly HttpClient _client;
    private string? _token;

    public InventoryIntegrationTests(CustomWebApplicationFactory factory)
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

        var email = $"inventorytest{Guid.NewGuid()}@example.com";
        var request = new RegisterRequestDto
        {
            Email = email,
            Password = "Password123!",
            FullName = "Inventory Test User",
            DateOfBirth = new DateOnly(1990, 1, 1),
            BiologicalSex = "male",
            ActivityLevel = "active",
            GoalType = "cutting"
        };
        var response = await _client.PostAsJsonAsync("/api/auth/register", request);
        var authData = await response.Content.ReadFromJsonAsync<AuthResponseDto>();
        _token = authData!.AccessToken;
        _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", _token);
    }

    private async Task<FoodResponseDto> CreateFoodAsync()
    {
        var foodReq = new CreateFoodRequestDto
        {
            FoodName = $"InvFood_{Guid.NewGuid()}",
            KcalPer100g = 150,
            ProteinGPer100g = 15,
            CarbsGPer100g = 20,
            FatGPer100g = 5
        };
        var resp = await _client.PostAsJsonAsync("/api/foods", foodReq);
        return (await resp.Content.ReadFromJsonAsync<FoodResponseDto>())!;
    }

    [Fact]
    public async Task Create_ValidData_ReturnsCreatedAndItem()
    {
        await AuthenticateAsync();
        var food = await CreateFoodAsync();

        var request = new CreateInventoryItemRequestDto
        {
            FoodId = food.FoodId,
            QuantityGrams = 500,
            ExpiryDate = DateOnly.FromDateTime(DateTime.Today.AddDays(10))
        };

        var response = await _client.PostAsJsonAsync("/api/inventory", request);

        response.StatusCode.Should().Be(HttpStatusCode.Created);
        var item = await response.Content.ReadFromJsonAsync<InventoryItemResponseDto>();
        item.Should().NotBeNull();
        item!.FoodId.Should().Be(food.FoodId);
        item.QuantityGrams.Should().Be(500);
    }

    [Fact]
    public async Task Create_NonExistentFood_ReturnsNotFound()
    {
        await AuthenticateAsync();

        var request = new CreateInventoryItemRequestDto
        {
            FoodId = 999999,
            QuantityGrams = 500
        };

        var response = await _client.PostAsJsonAsync("/api/inventory", request);

        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task GetMyInventory_ReturnsOkAndList()
    {
        await AuthenticateAsync();
        var food = await CreateFoodAsync();

        var createReq = new CreateInventoryItemRequestDto
        {
            FoodId = food.FoodId,
            QuantityGrams = 300
        };
        var createResp = await _client.PostAsJsonAsync("/api/inventory", createReq);
        var created = await createResp.Content.ReadFromJsonAsync<InventoryItemResponseDto>();

        var response = await _client.GetAsync("/api/inventory");

        response.StatusCode.Should().Be(HttpStatusCode.OK);
        var items = await response.Content.ReadFromJsonAsync<List<InventoryItemResponseDto>>();
        items.Should().NotBeNull();
        items.Should().Contain(i => i.InventoryId == created!.InventoryId);
    }

    [Fact]
    public async Task Update_ValidData_ReturnsOk()
    {
        await AuthenticateAsync();
        var food = await CreateFoodAsync();

        var createReq = new CreateInventoryItemRequestDto
        {
            FoodId = food.FoodId,
            QuantityGrams = 200
        };
        var createResp = await _client.PostAsJsonAsync("/api/inventory", createReq);
        var created = await createResp.Content.ReadFromJsonAsync<InventoryItemResponseDto>();

        var updateReq = new UpdateInventoryItemRequestDto
        {
            QuantityGrams = 750,
            ExpiryDate = DateOnly.FromDateTime(DateTime.Today.AddDays(15))
        };

        var response = await _client.PutAsJsonAsync($"/api/inventory/{created!.InventoryId}", updateReq);

        response.StatusCode.Should().Be(HttpStatusCode.OK);
        var updated = await response.Content.ReadFromJsonAsync<InventoryItemResponseDto>();
        updated!.QuantityGrams.Should().Be(750);
    }

    [Fact]
    public async Task Update_NonExistentId_ReturnsNotFound()
    {
        await AuthenticateAsync();

        var updateReq = new UpdateInventoryItemRequestDto
        {
            QuantityGrams = 500
        };

        var response = await _client.PutAsJsonAsync("/api/inventory/999999", updateReq);

        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task Delete_ExistingId_ReturnsNoContent()
    {
        await AuthenticateAsync();
        var food = await CreateFoodAsync();

        var createReq = new CreateInventoryItemRequestDto
        {
            FoodId = food.FoodId,
            QuantityGrams = 400
        };
        var createResp = await _client.PostAsJsonAsync("/api/inventory", createReq);
        var created = await createResp.Content.ReadFromJsonAsync<InventoryItemResponseDto>();

        var response = await _client.DeleteAsync($"/api/inventory/{created!.InventoryId}");

        response.StatusCode.Should().Be(HttpStatusCode.NoContent);
    }

    [Fact]
    public async Task Delete_NonExistentId_ReturnsNotFound()
    {
        await AuthenticateAsync();

        var response = await _client.DeleteAsync("/api/inventory/999999");

        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }
}
