using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using FluentAssertions;
using SmartMacro.Api.DTOs;

namespace SmartMacro.Tests.IntegrationTests;

public class DailyTargetIntegrationTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly HttpClient _client;
    private string? _token;

    public DailyTargetIntegrationTests(CustomWebApplicationFactory factory)
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

        var email = $"targettest{Guid.NewGuid()}@example.com";
        var request = new RegisterRequestDto
        {
            Email = email,
            Password = "Password123!",
            FullName = "Target Test User",
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
    public async Task Create_ValidData_ReturnsCreatedAndTarget()
    {
        await AuthenticateAsync();

        var request = new CreateDailyTargetRequestDto
        {
            Date = DateOnly.FromDateTime(DateTime.Now.AddDays(Random.Shared.Next(10, 1000))),
            TargetKcal = 2200,
            TargetProteinG = 160,
            TargetCarbsG = 220,
            TargetFatG = 70
        };

        var response = await _client.PostAsJsonAsync("/api/daily-targets", request);

        response.StatusCode.Should().Be(HttpStatusCode.Created);
        var target = await response.Content.ReadFromJsonAsync<DailyTargetResponseDto>();
        target.Should().NotBeNull();
        target!.TargetKcal.Should().Be(2200);
    }

    [Fact]
    public async Task GetAll_ReturnsOkAndList()
    {
        await AuthenticateAsync();

        var request = new CreateDailyTargetRequestDto
        {
            Date = DateOnly.FromDateTime(DateTime.Now.AddDays(Random.Shared.Next(10, 1000))),
            TargetKcal = 2000,
            TargetProteinG = 150,
            TargetCarbsG = 200,
            TargetFatG = 65
        };
        var createResp = await _client.PostAsJsonAsync("/api/daily-targets", request);
        var created = await createResp.Content.ReadFromJsonAsync<DailyTargetResponseDto>();

        var response = await _client.GetAsync("/api/daily-targets");

        response.StatusCode.Should().Be(HttpStatusCode.OK);
        var targets = await response.Content.ReadFromJsonAsync<List<DailyTargetResponseDto>>();
        targets.Should().NotBeNull();
        targets.Should().Contain(t => t.Id == created!.Id);
    }

    [Fact]
    public async Task Update_ValidData_ReturnsOk()
    {
        await AuthenticateAsync();

        var createReq = new CreateDailyTargetRequestDto
        {
            Date = DateOnly.FromDateTime(DateTime.Now.AddDays(Random.Shared.Next(10, 1000))),
            TargetKcal = 1800,
            TargetProteinG = 140,
            TargetCarbsG = 180,
            TargetFatG = 50
        };
        var createResp = await _client.PostAsJsonAsync("/api/daily-targets", createReq);
        var created = await createResp.Content.ReadFromJsonAsync<DailyTargetResponseDto>();

        var updateReq = new UpdateDailyTargetRequestDto
        {
            TargetKcal = 2500,
            TargetProteinG = 180,
            TargetCarbsG = 250,
            TargetFatG = 80
        };

        var response = await _client.PutAsJsonAsync($"/api/daily-targets/{created!.Id}", updateReq);

        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var getResp = await _client.GetAsync("/api/daily-targets");
        var targets = await getResp.Content.ReadFromJsonAsync<List<DailyTargetResponseDto>>();
        targets!.First(t => t.Id == created.Id).TargetKcal.Should().Be(2500);
    }

    [Fact]
    public async Task Update_NonExistentId_ReturnsNotFound()
    {
        await AuthenticateAsync();

        var updateReq = new UpdateDailyTargetRequestDto
        {
            TargetKcal = 2000,
            TargetProteinG = 150,
            TargetCarbsG = 200,
            TargetFatG = 60
        };

        var response = await _client.PutAsJsonAsync("/api/daily-targets/999999", updateReq);

        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task Delete_ExistingId_ReturnsNoContent()
    {
        await AuthenticateAsync();

        var createReq = new CreateDailyTargetRequestDto
        {
            Date = DateOnly.FromDateTime(DateTime.Now.AddDays(Random.Shared.Next(10, 1000))),
            TargetKcal = 2000,
            TargetProteinG = 150,
            TargetCarbsG = 200,
            TargetFatG = 60
        };
        var createResp = await _client.PostAsJsonAsync("/api/daily-targets", createReq);
        var created = await createResp.Content.ReadFromJsonAsync<DailyTargetResponseDto>();

        var response = await _client.DeleteAsync($"/api/daily-targets/{created!.Id}");

        response.StatusCode.Should().Be(HttpStatusCode.NoContent);
    }

    [Fact]
    public async Task Delete_NonExistentId_ReturnsNotFound()
    {
        await AuthenticateAsync();

        var response = await _client.DeleteAsync("/api/daily-targets/999999");

        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }
}
