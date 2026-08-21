using FluentAssertions;
using Microsoft.AspNetCore.DataProtection;
using Microsoft.Extensions.DependencyInjection;

namespace SmartMacro.Tests.IntegrationTests;

public class DataProtectionConfigurationTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly CustomWebApplicationFactory _factory;

    public DataProtectionConfigurationTests(CustomWebApplicationFactory factory)
    {
        _factory = factory;
    }

    [Fact]
    public void DataProtection_ProviderIsRegisteredAndCanProtectUnprotectData()
    {
        // Arrange
        using var scope = _factory.Services.CreateScope();
        var dpProvider = scope.ServiceProvider.GetService<IDataProtectionProvider>();

        // Assert
        dpProvider.Should().NotBeNull("IDataProtectionProvider must be registered in the DI container");

        var protector = dpProvider!.CreateProtector("SmartMacro.TestPurpose");
        protector.Should().NotBeNull();

        const string plaintext = "SuperSensitiveRefreshTokenPayload123!";
        var protectedData = protector.Protect(plaintext);

        protectedData.Should().NotBeNullOrEmpty();
        protectedData.Should().NotBe(plaintext);

        var roundtripped = protector.Unprotect(protectedData);
        roundtripped.Should().Be(plaintext);
    }
}
