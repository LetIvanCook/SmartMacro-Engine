using System;
using System.Collections.Generic;

namespace SmartMacro.Api.Models;

public partial class UserBodyMetric
{
    public long MetricId { get; set; }

    public long UserId { get; set; }

    public DateOnly RecordedDate { get; set; }

    public decimal WeightKg { get; set; }

    public decimal? HeightCm { get; set; }

    public decimal? BodyFatPercent { get; set; }

    public decimal? BmrKcal { get; set; }

    public DateTime CreatedAt { get; set; }

    public virtual User User { get; set; } = null!;
}
