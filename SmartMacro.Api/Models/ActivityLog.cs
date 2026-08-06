using System;
using System.Collections.Generic;

namespace SmartMacro.Api.Models;

public partial class ActivityLog
{
    public long ActivityLogId { get; set; }

    public long UserId { get; set; }

    public DateOnly LogDate { get; set; }

    public string ActivityName { get; set; } = null!;

    public short DurationMinutes { get; set; }

    public decimal KcalBurned { get; set; }

    public DateTime CreatedAt { get; set; }

    public virtual User User { get; set; } = null!;
}
