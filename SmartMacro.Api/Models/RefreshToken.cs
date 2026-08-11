using System;

namespace SmartMacro.Api.Models;

public class RefreshToken
{
    public int Id { get; set; }
    
    /// <summary>
    /// SHA256 hash of the cryptographically secure refresh token value.
    /// The raw token is only returned to the client and never stored.
    /// </summary>
    public string TokenHash { get; set; } = null!;
    
    public long UserId { get; set; }
    
    public virtual User User { get; set; } = null!;
    
    public DateTime CreatedAt { get; set; }
    
    public DateTime ExpiresAt { get; set; }
    
    public DateTime? RevokedAt { get; set; }
    
    public bool IsRevoked => RevokedAt.HasValue;
    
    public bool IsExpired => DateTime.UtcNow >= ExpiresAt;
    
    public bool IsActive => !IsRevoked && !IsExpired;
}
