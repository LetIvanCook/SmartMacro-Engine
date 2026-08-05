using System;
using System.Collections.Generic;

namespace SmartMacro.Api.Models;

public partial class UserTrainingSchedule
{
    public long ScheduleId { get; set; }

    public long UserId { get; set; }

    public DateOnly ScheduleDate { get; set; }

    public byte CycleTypeId { get; set; }

    public bool IsCompleted { get; set; }

    public virtual TrainingCycleType CycleType { get; set; } = null!;

    public virtual User User { get; set; } = null!;
}
