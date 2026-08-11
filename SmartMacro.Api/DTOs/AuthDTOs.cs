namespace SmartMacro.Api.DTOs;

public class RegisterRequestDto
{
    public string Email { get; set; } = null!;
    public string Password { get; set; } = null!;
    public string FullName { get; set; } = null!;
    public DateOnly DateOfBirth { get; set; }
    public string BiologicalSex { get; set; } = null!;
    public string ActivityLevel { get; set; } = "moderate";
    public string GoalType { get; set; } = "maintenance";
}

public class LoginRequestDto
{
    public string Email { get; set; } = null!;
    public string Password { get; set; } = null!;
}

public class AuthResponseDto
{
    public string AccessToken { get; set; } = null!;
    public string RefreshToken { get; set; } = null!;
    public DateTime AccessTokenExpiry { get; set; }
    public long UserId { get; set; }
    public string Email { get; set; } = null!;
    public string? FullName { get; set; }
}

public class RefreshTokenRequestDto
{
    public string RefreshToken { get; set; } = null!;
}
