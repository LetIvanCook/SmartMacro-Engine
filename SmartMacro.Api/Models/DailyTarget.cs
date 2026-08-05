using System;
using System.Collections.Generic;

namespace SmartMacro.Api.Models;

public partial class DailyTarget
{
    public long TargetId { get; set; }

    public long UserId { get; set; }

    public DateOnly TargetDate { get; set; }

    public decimal TargetKcal { get; set; }

    public decimal TargetProteinG { get; set; }

    public decimal TargetCarbsG { get; set; }

    public decimal TargetFatG { get; set; }

    public long? ComputedFromRuleId { get; set; }

    public DateTime CreatedAt { get; set; }

    public virtual MacroAdjustmentRule? ComputedFromRule { get; set; }

    public virtual User User { get; set; } = null!;
}
