namespace SmartMacro.Api.DTOs;

public class UserDto
{
    public long UserId { get; set; }
    public string Email { get; set; } = null!;
    public string? FullName { get; set; }
    public DateOnly DateOfBirth { get; set; }
    public string BiologicalSex { get; set; } = null!;
    public string ActivityLevel { get; set; } = null!;
    public string GoalType { get; set; } = null!;
    public string Status { get; set; } = null!;
    public DateTime CreatedAt { get; set; }
}

public class UpdateUserRequestDto
{
    public string? FullName { get; set; }
    public DateOnly? DateOfBirth { get; set; }
    public string? BiologicalSex { get; set; }
    public string? ActivityLevel { get; set; }
    public string? GoalType { get; set; }
}
