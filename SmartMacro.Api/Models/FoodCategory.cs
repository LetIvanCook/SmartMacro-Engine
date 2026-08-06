using System;
using System.Collections.Generic;

namespace SmartMacro.Api.Models;

public partial class FoodCategory
{
    public short CategoryId { get; set; }

    public string CategoryName { get; set; } = null!;

    public virtual ICollection<Food> Foods { get; set; } = new List<Food>();
}
