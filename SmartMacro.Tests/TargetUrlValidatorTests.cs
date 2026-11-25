using System.Net;
using FluentAssertions;
using Microsoft.Extensions.Options;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Options;
using SmartMacro.Api.Services;

namespace SmartMacro.Tests;

public class TargetUrlValidatorTests
{
    private readonly TargetUrlValidator _validator;

    public TargetUrlValidatorTests()
    {
        var options = Microsoft.Extensions.Options.Options.Create(new ResearchOptions
        {
            AllowedHosts = ["macrofactor.com", "cronometer.com", "myfitnesspal.com", "eatthismuch.com"]
        });
        _validator = new TargetUrlValidator(options);
    }

    [Theory]
    [InlineData("http://cronometer.com/")]
    [InlineData("http://macrofactor.com/")]
    [InlineData("ftp://cronometer.com/")]
    public async Task ValidateAsync_WhenNotHttps_ThrowsInvalidResearchTargetException(string url)
    {
        var act = () => _validator.ValidateAsync(url);
        await act.Should().ThrowAsync<InvalidResearchTargetException>()
            .WithMessage("*Only HTTPS*");
    }

    [Theory]
    [InlineData("https://evil-competitor.com/")]
    [InlineData("https://google.com/")]
    [InlineData("https://attacker.net/payload")]
    [InlineData("https://cronometer.com.evil.com/")]
    public async Task ValidateAsync_WhenHostNotInAllowlist_ThrowsInvalidResearchTargetException(string url)
    {
        var act = () => _validator.ValidateAsync(url);
        await act.Should().ThrowAsync<InvalidResearchTargetException>()
            .WithMessage("*not in the allowed research hosts list*");
    }

    [Theory]
    [InlineData("cronometer.com", true)]
    [InlineData("app.cronometer.com", true)]
    [InlineData("blog.macrofactor.com", true)]
    [InlineData("myfitnesspal.com", true)]
    [InlineData("www.eatthismuch.com", true)]
    [InlineData("sub.domain.cronometer.com", true)]
    [InlineData("evilcronometer.com", false)]
    [InlineData("cronometer.com.attacker.com", false)]
    [InlineData("otherdomain.org", false)]
    public void IsHostAllowed_ValidatesHostsCorrectly(string host, bool expected)
    {
        var result = _validator.IsHostAllowed(host);
        result.Should().Be(expected);
    }

    [Theory]
    [InlineData("127.0.0.1", true)]
    [InlineData("127.0.0.2", true)]
    [InlineData("169.254.169.254", true)]
    [InlineData("169.254.0.1", true)]
    [InlineData("10.0.0.1", true)]
    [InlineData("10.255.255.255", true)]
    [InlineData("172.16.0.1", true)]
    [InlineData("172.24.1.1", true)]
    [InlineData("172.31.255.255", true)]
    [InlineData("192.168.0.1", true)]
    [InlineData("192.168.1.100", true)]
    [InlineData("0.0.0.0", true)]
    [InlineData("::1", true)]
    [InlineData("fe80::1", true)]
    [InlineData("fe80::215:5dff:fe00:1", true)]
    [InlineData("fc00::1", true)]
    [InlineData("fd12:3456:789a:1::1", true)]
    [InlineData("8.8.8.8", false)]
    [InlineData("1.1.1.1", false)]
    [InlineData("104.26.10.228", false)]
    [InlineData("2606:4700:20::681a:ae6", false)]
    public void IsDisallowedIpAddress_CorrectlyIdentifiesPrivateAndLoopbackIps(string ipString, bool expectedDisallowed)
    {
        var ip = IPAddress.Parse(ipString);
        var isDisallowed = TargetUrlValidator.IsDisallowedIpAddress(ip);
        isDisallowed.Should().Be(expectedDisallowed);
    }
}
