using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using FluentAssertions;
using SmartMacro.Api.DTOs;

namespace SmartMacro.Tests.IntegrationTests;

public class FoodIntegrationTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly HttpClient _client;
    private string? _token;

    public FoodIntegrationTests(CustomWebApplicationFactory factory)
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

        var email = $"foodtest{Guid.NewGuid()}@example.com";
        var request = new RegisterRequestDto
        {
            Email = email,
            Password = "Password123!",
            FullName = "Food Test User",
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

    [Fact]
    public async Task Create_ValidData_ReturnsCreatedAndFood()
    {
        await AuthenticateAsync();

        var request = new CreateFoodRequestDto
        {
            FoodName = $"Food_{Guid.NewGuid()}",
            KcalPer100g = 200,
            ProteinGPer100g = 20,
            CarbsGPer100g = 15,
            FatGPer100g = 5
        };

        var response = await _client.PostAsJsonAsync("/api/foods", request);

        response.StatusCode.Should().Be(HttpStatusCode.Created);
        var food = await response.Content.ReadFromJsonAsync<FoodResponseDto>();
        food.Should().NotBeNull();
        food!.FoodName.Should().Be(request.FoodName);
        food.KcalPer100g.Should().Be(200);
    }

    [Fact]
    public async Task GetById_ExistingId_ReturnsOkAndFood()
    {
        await AuthenticateAsync();

        var createReq = new CreateFoodRequestDto
        {
            FoodName = $"Food_{Guid.NewGuid()}",
            KcalPer100g = 150,
            ProteinGPer100g = 15,
            CarbsGPer100g = 10,
            FatGPer100g = 5
        };
        var createResp = await _client.PostAsJsonAsync("/api/foods", createReq);
        var created = await createResp.Content.ReadFromJsonAsync<FoodResponseDto>();

        var response = await _client.GetAsync($"/api/foods/{created!.FoodId}");

        response.StatusCode.Should().Be(HttpStatusCode.OK);
        var food = await response.Content.ReadFromJsonAsync<FoodResponseDto>();
        food.Should().NotBeNull();
        food!.FoodId.Should().Be(created.FoodId);
        food.FoodName.Should().Be(createReq.FoodName);
    }

    [Fact]
    public async Task GetById_NonExistentId_ReturnsNotFound()
    {
        await AuthenticateAsync();

        var response = await _client.GetAsync("/api/foods/999999");

        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task Update_ValidData_ReturnsOk()
    {
        await AuthenticateAsync();

        var createReq = new CreateFoodRequestDto
        {
            FoodName = $"Food_{Guid.NewGuid()}",
            KcalPer100g = 100,
            ProteinGPer100g = 10,
            CarbsGPer100g = 10,
            FatGPer100g = 2
        };
        var createResp = await _client.PostAsJsonAsync("/api/foods", createReq);
        var created = await createResp.Content.ReadFromJsonAsync<FoodResponseDto>();

        var updateReq = new UpdateFoodRequestDto
        {
            FoodName = $"Updated_{Guid.NewGuid()}",
            KcalPer100g = 250,
            ProteinGPer100g = 25,
            CarbsGPer100g = 20,
            FatGPer100g = 10
        };

        var response = await _client.PutAsJsonAsync($"/api/foods/{created!.FoodId}", updateReq);

        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var getResp = await _client.GetAsync($"/api/foods/{created.FoodId}");
        var updated = await getResp.Content.ReadFromJsonAsync<FoodResponseDto>();
        updated!.FoodName.Should().Be(updateReq.FoodName);
        updated.KcalPer100g.Should().Be(250);
    }

    [Fact]
    public async Task Update_NonExistentId_ReturnsNotFound()
    {
        await AuthenticateAsync();

        var updateReq = new UpdateFoodRequestDto
        {
            FoodName = "NonExistent",
            KcalPer100g = 100,
            ProteinGPer100g = 10,
            CarbsGPer100g = 10,
            FatGPer100g = 2
        };

        var response = await _client.PutAsJsonAsync("/api/foods/999999", updateReq);

        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task Delete_ExistingId_ReturnsNoContent()
    {
        await AuthenticateAsync();

        var createReq = new CreateFoodRequestDto
        {
            FoodName = $"Food_{Guid.NewGuid()}",
            KcalPer100g = 100,
            ProteinGPer100g = 10,
            CarbsGPer100g = 10,
            FatGPer100g = 2
        };
        var createResp = await _client.PostAsJsonAsync("/api/foods", createReq);
        var created = await createResp.Content.ReadFromJsonAsync<FoodResponseDto>();

        var response = await _client.DeleteAsync($"/api/foods/{created!.FoodId}");

        response.StatusCode.Should().Be(HttpStatusCode.NoContent);

        var getResp = await _client.GetAsync($"/api/foods/{created.FoodId}");
        getResp.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task Delete_NonExistentId_ReturnsNotFound()
    {
        await AuthenticateAsync();

        var response = await _client.DeleteAsync("/api/foods/999999");

        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }
}
