using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using FluentAssertions;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.TestHost;
using Microsoft.Extensions.DependencyInjection;
using Moq;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Engines;
using SmartMacro.Api.Exceptions;

namespace SmartMacro.Tests.IntegrationTests;

public class OptimizationErrorHandlingIntegrationTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly CustomWebApplicationFactory _factory;

    public OptimizationErrorHandlingIntegrationTests(CustomWebApplicationFactory factory)
    {
        _factory = factory;
    }

    private async Task<(HttpClient Client, long TargetId, long FoodId)> SetupUserAndDataAsync(HttpClient client)
    {
        var email = $"solverterror{Guid.NewGuid()}@example.com";
        var request = new RegisterRequestDto
        {
            Email = email,
            Password = "Password123!",
            FullName = "Solver Error Test User",
            DateOfBirth = new DateOnly(1990, 1, 1),
            BiologicalSex = "male",
            ActivityLevel = "active",
            GoalType = "cutting"
        };
        var response = await client.PostAsJsonAsync("/api/auth/register", request);
        var authData = await response.Content.ReadFromJsonAsync<AuthResponseDto>();
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", authData!.AccessToken);

        // Create target
        var targetReq = new CreateDailyTargetRequestDto
        {
            Date = DateOnly.FromDateTime(DateTime.Now.AddDays(3)),
            TargetKcal = 2000,
            TargetProteinG = 150,
            TargetCarbsG = 200,
            TargetFatG = 66
        };
        var targetResp = await client.PostAsJsonAsync("/api/daily-targets", targetReq);
        var target = await targetResp.Content.ReadFromJsonAsync<DailyTargetResponseDto>();

        // Create food
        var fReq = new CreateFoodRequestDto
        {
            FoodName = "Chicken Breast",
            KcalPer100g = 165,
            ProteinGPer100g = 31,
            CarbsGPer100g = 0,
            FatGPer100g = 3.6m
        };
        var fResp = await client.PostAsJsonAsync("/api/foods", fReq);
        var food = await fResp.Content.ReadFromJsonAsync<FoodResponseDto>();

        // Add inventory
        var invReq = new CreateInventoryItemRequestDto { FoodId = food!.FoodId, QuantityGrams = 1000 };
        await client.PostAsJsonAsync("/api/inventory", invReq);

        return (client, target!.Id, food.FoodId);
    }

    [Fact]
    public async Task OptimizationEngine_WhenSolverUnavailable_Returns503ServiceUnavailable()
    {
        var mockEngine = new Mock<IMacroOptimizationEngine>();
        mockEngine.Setup(e => e.CalculateOptimalMeal(It.IsAny<DailyTargetDto>(), It.IsAny<List<InventoryItemResponseDto>>()))
            .Throws(new SolverUnavailableException("Native OR-Tools GLOP solver library could not be loaded."));

        var client = _factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureTestServices(services =>
            {
                services.AddScoped<IMacroOptimizationEngine>(_ => mockEngine.Object);
            });
        }).CreateClient();

        var (_, targetId, foodId) = await SetupUserAndDataAsync(client);

        var optimizeReq = new OptimizationRequestDto
        {
            DailyTargetId = targetId,
            IncludeFoodIds = new List<long> { foodId }
        };

        // Act
        var response = await client.PostAsJsonAsync("/api/optimizations/generate-plan", optimizeReq);

        // Assert: MUST return 503 Service Unavailable, NOT 200 INFEASIBLE
        response.StatusCode.Should().Be(HttpStatusCode.ServiceUnavailable);
        var problemDetails = await response.Content.ReadFromJsonAsync<ProblemDetails>();
        problemDetails.Should().NotBeNull();
        problemDetails!.Status.Should().Be(503);
        problemDetails.Title.Should().Be("Service Unavailable");
        problemDetails.Detail.Should().Contain("Native OR-Tools GLOP solver library could not be loaded.");
    }
}
