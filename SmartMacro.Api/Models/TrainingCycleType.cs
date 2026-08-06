using System;
using System.Collections.Generic;

namespace SmartMacro.Api.Models;

public partial class TrainingCycleType
{
    public byte CycleTypeId { get; set; }

    public string TypeCode { get; set; } = null!;

    public string DisplayName { get; set; } = null!;

    public virtual ICollection<MacroAdjustmentRule> MacroAdjustmentRules { get; set; } = new List<MacroAdjustmentRule>();

    public virtual ICollection<UserTrainingSchedule> UserTrainingSchedules { get; set; } = new List<UserTrainingSchedule>();
}
