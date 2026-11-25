using System.Net;
using System.Net.Sockets;
using Microsoft.Extensions.Options;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Options;

namespace SmartMacro.Api.Services;

public class TargetUrlValidator : ITargetUrlValidator
{
    private readonly ResearchOptions _options;

    public TargetUrlValidator(IOptions<ResearchOptions> options)
    {
        _options = options.Value;
    }

    public bool IsHostAllowed(string host)
    {
        if (string.IsNullOrWhiteSpace(host))
        {
            return false;
        }

        var normalizedHost = host.Trim().ToLowerInvariant();

        foreach (var allowedHost in _options.AllowedHosts)
        {
            var normalizedAllowed = allowedHost.Trim().ToLowerInvariant();
            if (normalizedHost == normalizedAllowed || normalizedHost.EndsWith("." + normalizedAllowed, StringComparison.OrdinalIgnoreCase))
            {
                return true;
            }
        }

        return false;
    }

    public async Task ValidateAsync(string url, CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(url))
        {
            throw new InvalidResearchTargetException("Target URL cannot be empty.");
        }

        if (!Uri.TryCreate(url, UriKind.Absolute, out var uri))
        {
            throw new InvalidResearchTargetException("Target URL is not a valid absolute URI.");
        }

        if (!string.Equals(uri.Scheme, Uri.UriSchemeHttps, StringComparison.OrdinalIgnoreCase))
        {
            throw new InvalidResearchTargetException("Only HTTPS protocol is permitted for research targets.");
        }

        if (!IsHostAllowed(uri.Host))
        {
            throw new InvalidResearchTargetException($"Host '{uri.Host}' is not in the allowed research hosts list.");
        }

        IPAddress[] addresses;
        try
        {
            addresses = await Dns.GetHostAddressesAsync(uri.DnsSafeHost, cancellationToken);
        }
        catch (Exception ex)
        {
            throw new InvalidResearchTargetException($"Failed to resolve host '{uri.Host}': {ex.Message}");
        }

        if (addresses.Length == 0)
        {
            throw new InvalidResearchTargetException($"Could not resolve any IP address for host '{uri.Host}'.");
        }

        foreach (var ip in addresses)
        {
            if (IsDisallowedIpAddress(ip))
            {
                throw new InvalidResearchTargetException(
                    $"Resolved IP '{ip}' for host '{uri.Host}' is restricted (private, loopback, or link-local address).");
            }
        }
    }

    public static bool IsDisallowedIpAddress(IPAddress address)
    {
        if (address.IsIPv4MappedToIPv6)
        {
            address = address.MapToIPv4();
        }

        if (IPAddress.IsLoopback(address))
        {
            return true;
        }

        if (address.Equals(IPAddress.Any) || address.Equals(IPAddress.IPv6Any) || address.Equals(IPAddress.None))
        {
            return true;
        }

        var bytes = address.GetAddressBytes();

        if (address.AddressFamily == AddressFamily.InterNetwork)
        {
            // 10.0.0.0/8
            if (bytes[0] == 10)
            {
                return true;
            }

            // 172.16.0.0/12 (172.16.0.0 - 172.31.255.255)
            if (bytes[0] == 172 && bytes[1] >= 16 && bytes[1] <= 31)
            {
                return true;
            }

            // 192.168.0.0/16
            if (bytes[0] == 192 && bytes[1] == 168)
            {
                return true;
            }

            // 169.254.0.0/16 (Link-local / Cloud metadata)
            if (bytes[0] == 169 && bytes[1] == 254)
            {
                return true;
            }

            // 127.0.0.0/8
            if (bytes[0] == 127)
            {
                return true;
            }

            // 0.0.0.0/8
            if (bytes[0] == 0)
            {
                return true;
            }
        }
        else if (address.AddressFamily == AddressFamily.InterNetworkV6)
        {
            // ::1 (Loopback)
            if (address.Equals(IPAddress.IPv6Loopback))
            {
                return true;
            }

            // fc00::/7 (Unique Local Address)
            if ((bytes[0] & 0xFE) == 0xFC)
            {
                return true;
            }

            // fe80::/10 (Link-Local)
            if (bytes[0] == 0xFE && (bytes[1] & 0xC0) == 0x80)
            {
                return true;
            }
        }

        return false;
    }
}
