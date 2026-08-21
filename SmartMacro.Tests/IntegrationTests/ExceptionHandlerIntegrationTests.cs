using System.Net;
using System.Net.Http.Json;
using FluentAssertions;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.DependencyInjection;
using SmartMacro.Api.Exceptions;

namespace SmartMacro.Tests.IntegrationTests;

public class ExceptionHandlerIntegrationTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly CustomWebApplicationFactory _factory;

    public ExceptionHandlerIntegrationTests(CustomWebApplicationFactory factory)
    {
        _factory = factory;
    }

    [Fact]
    public async Task UnhandledException_ReturnsHttp500WithProblemDetailsJson()
    {
        // Arrange: create client with a test endpoint that throws an unhandled exception
        var client = _factory.WithWebHostBuilder(builder =>
        {
            builder.Configure(app =>
            {
                app.UseExceptionHandler();
                app.UseRouting();
                app.UseEndpoints(endpoints =>
                {
                    endpoints.MapGet("/api/test-unhandled-exception", (Func<IResult>)(() =>
                        throw new InvalidOperationException("Unexpected fatal crash")));
                });
            });
        }).CreateClient();

        // Act
        var response = await client.GetAsync("/api/test-unhandled-exception");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.InternalServerError);
        response.Content.Headers.ContentType?.MediaType.Should().BeOneOf("application/problem+json", "application/json");

        var problemDetails = await response.Content.ReadFromJsonAsync<ProblemDetails>();
        problemDetails.Should().NotBeNull();
        problemDetails!.Status.Should().Be(500);
        problemDetails.Title.Should().Be("Internal Server Error");
        problemDetails.Detail.Should().Be("An unexpected error occurred.");
    }

    [Fact]
    public async Task NotFoundException_ReturnsHttp404WithProblemDetailsJson()
    {
        // Arrange
        var client = _factory.WithWebHostBuilder(builder =>
        {
            builder.Configure(app =>
            {
                app.UseExceptionHandler();
                app.UseRouting();
                app.UseEndpoints(endpoints =>
                {
                    endpoints.MapGet("/api/test-not-found-exception", (Func<IResult>)(() =>
                        throw new NotFoundException("Specific resource was not found")));
                });
            });
        }).CreateClient();

        // Act
        var response = await client.GetAsync("/api/test-not-found-exception");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
        var problemDetails = await response.Content.ReadFromJsonAsync<ProblemDetails>();
        problemDetails.Should().NotBeNull();
        problemDetails!.Status.Should().Be(404);
        problemDetails.Title.Should().Be("Resource Not Found");
        problemDetails.Detail.Should().Be("Specific resource was not found");
    }
}
