using System;
using System.Collections.Generic;

namespace SmartMacro.Api.Models;

public partial class MacroAdjustmentRule
{
    public long RuleId { get; set; }

    public long UserId { get; set; }

    public short CycleTypeId { get; set; }

    public decimal KcalMultiplier { get; set; }

    public decimal ProteinGPerKgBw { get; set; }

    public decimal CarbRatio { get; set; }

    public decimal FatRatio { get; set; }

    public DateTime UpdatedAt { get; set; }

    public virtual TrainingCycleType CycleType { get; set; } = null!;

    public virtual ICollection<DailyTarget> DailyTargets { get; set; } = new List<DailyTarget>();

    public virtual User User { get; set; } = null!;
}
