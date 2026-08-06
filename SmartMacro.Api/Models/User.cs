using System;
using System.Collections.Generic;

namespace SmartMacro.Api.Models;

public partial class User
{
    public long UserId { get; set; }

    public string Email { get; set; } = null!;

    public string PasswordHash { get; set; } = null!;

    public string? FullName { get; set; }

    public DateOnly DateOfBirth { get; set; }

    public string BiologicalSex { get; set; } = null!;

    public string ActivityLevel { get; set; } = null!;

    public string GoalType { get; set; } = null!;

    public string Status { get; set; } = null!;

    public DateTime CreatedAt { get; set; }

    public DateTime UpdatedAt { get; set; }

    public virtual ICollection<ActivityLog> ActivityLogs { get; set; } = new List<ActivityLog>();

    public virtual ICollection<DailyTarget> DailyTargets { get; set; } = new List<DailyTarget>();

    public virtual ICollection<Food> Foods { get; set; } = new List<Food>();

    public virtual ICollection<MacroAdjustmentRule> MacroAdjustmentRules { get; set; } = new List<MacroAdjustmentRule>();

    public virtual ICollection<MealLog> MealLogs { get; set; } = new List<MealLog>();

    public virtual ICollection<UserBodyMetric> UserBodyMetrics { get; set; } = new List<UserBodyMetric>();

    public virtual ICollection<UserFoodInventory> UserFoodInventories { get; set; } = new List<UserFoodInventory>();

    public virtual ICollection<UserTrainingSchedule> UserTrainingSchedules { get; set; } = new List<UserTrainingSchedule>();
}
