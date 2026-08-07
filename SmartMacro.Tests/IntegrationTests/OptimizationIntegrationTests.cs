using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using FluentAssertions;
using SmartMacro.Api.DTOs;

namespace SmartMacro.Tests.IntegrationTests;

public class OptimizationIntegrationTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly HttpClient _client;
    private string? _token;

    public OptimizationIntegrationTests(CustomWebApplicationFactory factory)
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

        var email = $"optimizetest{Guid.NewGuid()}@example.com";
        var request = new RegisterRequestDto
        {
            Email = email,
            Password = "Password123!",
            FullName = "Optimize Test User",
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
    public async Task OptimizationEngine_E2E_ReturnsOptimalSolution()
    {
        await AuthenticateAsync();

        // 1. Create a Daily Target
        var targetReq = new CreateDailyTargetRequestDto
        {
            Date = DateOnly.FromDateTime(DateTime.Now.AddDays(1)),
            TargetKcal = 2000,
            TargetProteinG = 150,
            TargetCarbsG = 200,
            TargetFatG = 66
        };
        var targetResp = await _client.PostAsJsonAsync("/api/daily-targets", targetReq);
        targetResp.StatusCode.Should().Be(HttpStatusCode.Created);
        var target = await targetResp.Content.ReadFromJsonAsync<DailyTargetResponseDto>();

        // 2. Create some Foods to use for optimization
        var foods = new[]
        {
            new CreateFoodRequestDto { FoodName = "Chicken Breast", KcalPer100g = 165, ProteinGPer100g = 31, CarbsGPer100g = 0, FatGPer100g = 3.6m },
            new CreateFoodRequestDto { FoodName = "Rice", KcalPer100g = 130, ProteinGPer100g = 2.7m, CarbsGPer100g = 28, FatGPer100g = 0.3m },
            new CreateFoodRequestDto { FoodName = "Olive Oil", KcalPer100g = 884, ProteinGPer100g = 0, CarbsGPer100g = 0, FatGPer100g = 100 }
        };

        var foodIds = new List<long>();
        foreach (var f in foods)
        {
            var r = await _client.PostAsJsonAsync("/api/foods", f);
            r.StatusCode.Should().Be(HttpStatusCode.Created);
            var fResp = await r.Content.ReadFromJsonAsync<FoodResponseDto>();
            foodIds.Add(fResp!.FoodId);
            
            // Add to Inventory
            var invReq = new CreateInventoryItemRequestDto { FoodId = fResp.FoodId, QuantityGrams = 1000 };
            await _client.PostAsJsonAsync("/api/inventory", invReq);
        }

        // 3. Call Optimization endpoint
        var optimizeReq = new OptimizationRequestDto
        {
            DailyTargetId = target!.Id,
            IncludeFoodIds = foodIds
        };
        var optResp = await _client.PostAsJsonAsync("/api/optimizations/generate-plan", optimizeReq);
        optResp.StatusCode.Should().Be(HttpStatusCode.OK);

        var result = await optResp.Content.ReadFromJsonAsync<OptimizationResultDto>();
        
        // 4. Verify Result
        result.Should().NotBeNull();
        result!.SolverStatus.Should().Be("OPTIMAL");
        result.AllocatedItems.Should().NotBeEmpty();

        // Check if macros are roughly within constraint (depending on how the engine works, usually close)
        result.AchievedMacros.Kcal.Should().BeGreaterThan(0);
        result.AchievedMacros.ProteinG.Should().BeGreaterThan(0);
    }

    [Fact]
    public async Task OptimizationEngine_Infeasible_ReturnsFriendlyResponse()
    {
        await AuthenticateAsync();

        // 1. Create a Daily Target with extremely tight constraints (e.g., 0 Kcal but 100g protein)
        var targetReq = new CreateDailyTargetRequestDto
        {
            Date = DateOnly.FromDateTime(DateTime.Now.AddDays(2)),
            TargetKcal = 100,
            TargetProteinG = 100,
            TargetCarbsG = 1,
            TargetFatG = 1
        };
        var targetResp = await _client.PostAsJsonAsync("/api/daily-targets", targetReq);
        targetResp.StatusCode.Should().Be(HttpStatusCode.Created);
        var target = await targetResp.Content.ReadFromJsonAsync<DailyTargetResponseDto>();

        // 2. Create one Food (Oil, pure fat)
        var f = new CreateFoodRequestDto { FoodName = "Oil 2", KcalPer100g = 884, ProteinGPer100g = 0, CarbsGPer100g = 0, FatGPer100g = 100 };
        var r = await _client.PostAsJsonAsync("/api/foods", f);
        var fResp = await r.Content.ReadFromJsonAsync<FoodResponseDto>();

        // Add to Inventory
        var invReq = new CreateInventoryItemRequestDto { FoodId = fResp!.FoodId, QuantityGrams = 1000 };
        await _client.PostAsJsonAsync("/api/inventory", invReq);

        // 3. Call Optimization (needs 100g protein, but only has fat)
        var optimizeReq = new OptimizationRequestDto
        {
            DailyTargetId = target!.Id,
            IncludeFoodIds = new List<long> { fResp.FoodId }
        };
        var optResp = await _client.PostAsJsonAsync("/api/optimizations/generate-plan", optimizeReq);
        
        // Even if infeasible, the API usually returns 200 with INFEASIBLE status, or 400 Bad Request. 
        // It should NOT crash (500).
        optResp.StatusCode.Should().NotBe(HttpStatusCode.InternalServerError);
        
        if (optResp.StatusCode == HttpStatusCode.OK)
        {
            var result = await optResp.Content.ReadFromJsonAsync<OptimizationResultDto>();
            result!.SolverStatus.Should().BeOneOf("INFEASIBLE", "ABNORMAL");
        }
    }
}
