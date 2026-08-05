using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

namespace SmartMacro.Api.Models;

public partial class SmartMacroDbContext : DbContext
{
    public SmartMacroDbContext()
    {
    }

    public SmartMacroDbContext(DbContextOptions<SmartMacroDbContext> options)
        : base(options)
    {
    }

    public virtual DbSet<ActivityLog> ActivityLogs { get; set; }

    public virtual DbSet<DailyTarget> DailyTargets { get; set; }

    public virtual DbSet<Food> Foods { get; set; }

    public virtual DbSet<FoodCategory> FoodCategories { get; set; }

    public virtual DbSet<MacroAdjustmentRule> MacroAdjustmentRules { get; set; }

    public virtual DbSet<MealLog> MealLogs { get; set; }

    public virtual DbSet<TrainingCycleType> TrainingCycleTypes { get; set; }

    public virtual DbSet<User> Users { get; set; }

    public virtual DbSet<UserBodyMetric> UserBodyMetrics { get; set; }

    public virtual DbSet<UserFoodInventory> UserFoodInventories { get; set; }

    public virtual DbSet<UserTrainingSchedule> UserTrainingSchedules { get; set; }

    //protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    //    => optionsBuilder.UseSqlServer("Name=ConnectionStrings:DefaultConnection");

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<ActivityLog>(entity =>
        {
            entity.ToTable("activity_logs");

            entity.HasIndex(e => new { e.UserId, e.LogDate }, "IX_activity_user_date");

            entity.Property(e => e.ActivityLogId).HasColumnName("activity_log_id");
            entity.Property(e => e.ActivityName)
                .HasMaxLength(150)
                .IsUnicode(false)
                .HasColumnName("activity_name");
            entity.Property(e => e.CreatedAt)
                .HasPrecision(3)
                .HasDefaultValueSql("(sysdatetime())")
                .HasColumnName("created_at");
            entity.Property(e => e.DurationMinutes).HasColumnName("duration_minutes");
            entity.Property(e => e.KcalBurned)
                .HasColumnType("decimal(6, 2)")
                .HasColumnName("kcal_burned");
            entity.Property(e => e.LogDate).HasColumnName("log_date");
            entity.Property(e => e.UserId).HasColumnName("user_id");

            entity.HasOne(d => d.User).WithMany(p => p.ActivityLogs)
                .HasForeignKey(d => d.UserId)
                .HasConstraintName("FK_activity_user");
        });

        modelBuilder.Entity<DailyTarget>(entity =>
        {
            entity.HasKey(e => e.TargetId);

            entity.ToTable("daily_targets");

            entity.HasIndex(e => new { e.UserId, e.TargetDate }, "UQ_target_user_date").IsUnique();

            entity.Property(e => e.TargetId).HasColumnName("target_id");
            entity.Property(e => e.ComputedFromRuleId).HasColumnName("computed_from_rule_id");
            entity.Property(e => e.CreatedAt)
                .HasPrecision(3)
                .HasDefaultValueSql("(sysdatetime())")
                .HasColumnName("created_at");
            entity.Property(e => e.TargetCarbsG)
                .HasColumnType("decimal(6, 2)")
                .HasColumnName("target_carbs_g");
            entity.Property(e => e.TargetDate).HasColumnName("target_date");
            entity.Property(e => e.TargetFatG)
                .HasColumnType("decimal(6, 2)")
                .HasColumnName("target_fat_g");
            entity.Property(e => e.TargetKcal)
                .HasColumnType("decimal(7, 2)")
                .HasColumnName("target_kcal");
            entity.Property(e => e.TargetProteinG)
                .HasColumnType("decimal(6, 2)")
                .HasColumnName("target_protein_g");
            entity.Property(e => e.UserId).HasColumnName("user_id");

            entity.HasOne(d => d.ComputedFromRule).WithMany(p => p.DailyTargets)
                .HasForeignKey(d => d.ComputedFromRuleId)
                .HasConstraintName("FK_target_rule");

            entity.HasOne(d => d.User).WithMany(p => p.DailyTargets)
                .HasForeignKey(d => d.UserId)
                .HasConstraintName("FK_target_user");
        });

        modelBuilder.Entity<Food>(entity =>
        {
            entity.ToTable("foods");

            entity.HasIndex(e => new { e.KcalPer100g, e.ProteinGPer100g, e.CarbsGPer100g, e.FatGPer100g }, "IX_foods_macro");

            entity.HasIndex(e => e.Barcode, "UQ_foods_barcode")
                .IsUnique()
                .HasFilter("([barcode] IS NOT NULL)");

            entity.Property(e => e.FoodId).HasColumnName("food_id");
            entity.Property(e => e.Barcode)
                .HasMaxLength(64)
                .IsUnicode(false)
                .HasColumnName("barcode");
            entity.Property(e => e.CarbsGPer100g)
                .HasColumnType("decimal(6, 2)")
                .HasColumnName("carbs_g_per_100g");
            entity.Property(e => e.CategoryId).HasColumnName("category_id");
            entity.Property(e => e.CreatedAt)
                .HasPrecision(3)
                .HasDefaultValueSql("(sysdatetime())")
                .HasColumnName("created_at");
            entity.Property(e => e.CreatedBy).HasColumnName("created_by");
            entity.Property(e => e.FatGPer100g)
                .HasColumnType("decimal(6, 2)")
                .HasColumnName("fat_g_per_100g");
            entity.Property(e => e.FiberGPer100g)
                .HasColumnType("decimal(6, 2)")
                .HasColumnName("fiber_g_per_100g");
            entity.Property(e => e.FoodName)
                .HasMaxLength(200)
                .IsUnicode(false)
                .HasColumnName("food_name");
            entity.Property(e => e.IsVerified).HasColumnName("is_verified");
            entity.Property(e => e.KcalPer100g)
                .HasColumnType("decimal(6, 2)")
                .HasColumnName("kcal_per_100g");
            entity.Property(e => e.ProteinGPer100g)
                .HasColumnType("decimal(6, 2)")
                .HasColumnName("protein_g_per_100g");
            entity.Property(e => e.Source)
                .HasMaxLength(20)
                .IsUnicode(false)
                .HasDefaultValue("user_submitted")
                .HasColumnName("source");

            entity.HasOne(d => d.Category).WithMany(p => p.Foods)
                .HasForeignKey(d => d.CategoryId)
                .OnDelete(DeleteBehavior.SetNull)
                .HasConstraintName("FK_foods_category");

            entity.HasOne(d => d.CreatedByNavigation).WithMany(p => p.Foods)
                .HasForeignKey(d => d.CreatedBy)
                .OnDelete(DeleteBehavior.SetNull)
                .HasConstraintName("FK_foods_created_by");
        });

        modelBuilder.Entity<FoodCategory>(entity =>
        {
            entity.HasKey(e => e.CategoryId);

            entity.ToTable("food_categories");

            entity.HasIndex(e => e.CategoryName, "UQ_food_categories_name").IsUnique();

            entity.Property(e => e.CategoryId).HasColumnName("category_id");
            entity.Property(e => e.CategoryName)
                .HasMaxLength(100)
                .IsUnicode(false)
                .HasColumnName("category_name");
        });

        modelBuilder.Entity<MacroAdjustmentRule>(entity =>
        {
            entity.HasKey(e => e.RuleId);

            entity.ToTable("macro_adjustment_rules", tb =>
                {
                    tb.HasTrigger("TRG_rules_after_delete_nullify_targets");
                    tb.HasTrigger("TRG_rules_updated_at");
                });

            entity.HasIndex(e => new { e.UserId, e.CycleTypeId }, "UQ_rules_user_cycletype").IsUnique();

            entity.Property(e => e.RuleId).HasColumnName("rule_id");
            entity.Property(e => e.CarbRatio)
                .HasColumnType("decimal(4, 3)")
                .HasColumnName("carb_ratio");
            entity.Property(e => e.CycleTypeId).HasColumnName("cycle_type_id");
            entity.Property(e => e.FatRatio)
                .HasColumnType("decimal(4, 3)")
                .HasColumnName("fat_ratio");
            entity.Property(e => e.KcalMultiplier)
                .HasDefaultValue(1.000m)
                .HasColumnType("decimal(4, 3)")
                .HasColumnName("kcal_multiplier");
            entity.Property(e => e.ProteinGPerKgBw)
                .HasColumnType("decimal(4, 2)")
                .HasColumnName("protein_g_per_kg_bw");
            entity.Property(e => e.UpdatedAt)
                .HasPrecision(3)
                .HasDefaultValueSql("(sysdatetime())")
                .HasColumnName("updated_at");
            entity.Property(e => e.UserId).HasColumnName("user_id");

            entity.HasOne(d => d.CycleType).WithMany(p => p.MacroAdjustmentRules)
                .HasForeignKey(d => d.CycleTypeId)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("FK_rules_cycle_type");

            entity.HasOne(d => d.User).WithMany(p => p.MacroAdjustmentRules)
                .HasForeignKey(d => d.UserId)
                .HasConstraintName("FK_rules_user");
        });

        modelBuilder.Entity<MealLog>(entity =>
        {
            entity.HasKey(e => e.LogId);

            entity.ToTable("meal_logs");

            entity.HasIndex(e => new { e.UserId, e.LogDate }, "IX_meallog_user_date");

            entity.Property(e => e.LogId).HasColumnName("log_id");
            entity.Property(e => e.CarbsGSnapshot)
                .HasColumnType("decimal(6, 2)")
                .HasColumnName("carbs_g_snapshot");
            entity.Property(e => e.ConsumedGrams)
                .HasColumnType("decimal(8, 2)")
                .HasColumnName("consumed_grams");
            entity.Property(e => e.CreatedAt)
                .HasPrecision(3)
                .HasDefaultValueSql("(sysdatetime())")
                .HasColumnName("created_at");
            entity.Property(e => e.FatGSnapshot)
                .HasColumnType("decimal(6, 2)")
                .HasColumnName("fat_g_snapshot");
            entity.Property(e => e.FoodId).HasColumnName("food_id");
            entity.Property(e => e.InventoryId).HasColumnName("inventory_id");
            entity.Property(e => e.IsAutoGenerated)
                .HasDefaultValue(true)
                .HasColumnName("is_auto_generated");
            entity.Property(e => e.KcalSnapshot)
                .HasColumnType("decimal(7, 2)")
                .HasColumnName("kcal_snapshot");
            entity.Property(e => e.LogDate).HasColumnName("log_date");
            entity.Property(e => e.MealSlot)
                .HasMaxLength(20)
                .IsUnicode(false)
                .HasColumnName("meal_slot");
            entity.Property(e => e.ProteinGSnapshot)
                .HasColumnType("decimal(6, 2)")
                .HasColumnName("protein_g_snapshot");
            entity.Property(e => e.UserId).HasColumnName("user_id");

            entity.HasOne(d => d.Food).WithMany(p => p.MealLogs)
                .HasForeignKey(d => d.FoodId)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("FK_meallog_food");

            entity.HasOne(d => d.Inventory).WithMany(p => p.MealLogs)
                .HasForeignKey(d => d.InventoryId)
                .HasConstraintName("FK_meallog_inventory");

            entity.HasOne(d => d.User).WithMany(p => p.MealLogs)
                .HasForeignKey(d => d.UserId)
                .HasConstraintName("FK_meallog_user");
        });

        modelBuilder.Entity<TrainingCycleType>(entity =>
        {
            entity.HasKey(e => e.CycleTypeId);

            entity.ToTable("training_cycle_types");

            entity.HasIndex(e => e.TypeCode, "UQ_training_cycle_types_code").IsUnique();

            entity.Property(e => e.CycleTypeId)
                .ValueGeneratedOnAdd()
                .HasColumnName("cycle_type_id");
            entity.Property(e => e.DisplayName)
                .HasMaxLength(50)
                .IsUnicode(false)
                .HasColumnName("display_name");
            entity.Property(e => e.TypeCode)
                .HasMaxLength(20)
                .IsUnicode(false)
                .HasColumnName("type_code");
        });

        modelBuilder.Entity<User>(entity =>
        {
            entity.ToTable("users", tb => tb.HasTrigger("TRG_users_updated_at"));

            entity.HasIndex(e => e.Email, "UQ_users_email").IsUnique();

            entity.Property(e => e.UserId).HasColumnName("user_id");
            entity.Property(e => e.ActivityLevel)
                .HasMaxLength(20)
                .IsUnicode(false)
                .HasDefaultValue("moderate")
                .HasColumnName("activity_level");
            entity.Property(e => e.BiologicalSex)
                .HasMaxLength(10)
                .IsUnicode(false)
                .HasColumnName("biological_sex");
            entity.Property(e => e.CreatedAt)
                .HasPrecision(3)
                .HasDefaultValueSql("(sysdatetime())")
                .HasColumnName("created_at");
            entity.Property(e => e.DateOfBirth).HasColumnName("date_of_birth");
            entity.Property(e => e.Email)
                .HasMaxLength(255)
                .IsUnicode(false)
                .HasColumnName("email");
            entity.Property(e => e.FullName)
                .HasMaxLength(150)
                .IsUnicode(false)
                .HasColumnName("full_name");
            entity.Property(e => e.GoalType)
                .HasMaxLength(20)
                .IsUnicode(false)
                .HasColumnName("goal_type");
            entity.Property(e => e.PasswordHash)
                .HasMaxLength(60)
                .IsUnicode(false)
                .IsFixedLength()
                .HasColumnName("password_hash");
            entity.Property(e => e.Status)
                .HasMaxLength(20)
                .IsUnicode(false)
                .HasDefaultValue("active")
                .HasColumnName("status");
            entity.Property(e => e.UpdatedAt)
                .HasPrecision(3)
                .HasDefaultValueSql("(sysdatetime())")
                .HasColumnName("updated_at");
        });

        modelBuilder.Entity<UserBodyMetric>(entity =>
        {
            entity.HasKey(e => e.MetricId);

            entity.ToTable("user_body_metrics");

            entity.HasIndex(e => new { e.UserId, e.RecordedDate }, "IX_metrics_user_date_desc").IsDescending(false, true);

            entity.HasIndex(e => new { e.UserId, e.RecordedDate }, "UQ_metrics_user_date").IsUnique();

            entity.Property(e => e.MetricId).HasColumnName("metric_id");
            entity.Property(e => e.BmrKcal)
                .HasColumnType("decimal(6, 2)")
                .HasColumnName("bmr_kcal");
            entity.Property(e => e.BodyFatPercent)
                .HasColumnType("decimal(4, 2)")
                .HasColumnName("body_fat_percent");
            entity.Property(e => e.CreatedAt)
                .HasPrecision(3)
                .HasDefaultValueSql("(sysdatetime())")
                .HasColumnName("created_at");
            entity.Property(e => e.HeightCm)
                .HasColumnType("decimal(5, 2)")
                .HasColumnName("height_cm");
            entity.Property(e => e.RecordedDate).HasColumnName("recorded_date");
            entity.Property(e => e.UserId).HasColumnName("user_id");
            entity.Property(e => e.WeightKg)
                .HasColumnType("decimal(5, 2)")
                .HasColumnName("weight_kg");

            entity.HasOne(d => d.User).WithMany(p => p.UserBodyMetrics)
                .HasForeignKey(d => d.UserId)
                .HasConstraintName("FK_metrics_user");
        });

        modelBuilder.Entity<UserFoodInventory>(entity =>
        {
            entity.HasKey(e => e.InventoryId);

            entity.ToTable("user_food_inventory", tb =>
                {
                    tb.HasTrigger("TRG_inventory_after_delete_nullify_meallogs");
                    tb.HasTrigger("TRG_inventory_updated_at");
                });

            entity.HasIndex(e => new { e.UserId, e.ExpiryDate }, "IX_inventory_user_expiry");

            entity.HasIndex(e => new { e.UserId, e.QuantityGrams }, "IX_inventory_user_qty");

            entity.HasIndex(e => new { e.UserId, e.FoodId, e.ExpiryDate }, "UQ_inventory_user_food_expiry").IsUnique();

            entity.Property(e => e.InventoryId).HasColumnName("inventory_id");
            entity.Property(e => e.ExpiryDate).HasColumnName("expiry_date");
            entity.Property(e => e.FoodId).HasColumnName("food_id");
            entity.Property(e => e.QuantityGrams)
                .HasColumnType("decimal(8, 2)")
                .HasColumnName("quantity_grams");
            entity.Property(e => e.UnitNote)
                .HasMaxLength(50)
                .IsUnicode(false)
                .HasColumnName("unit_note");
            entity.Property(e => e.UpdatedAt)
                .HasPrecision(3)
                .HasDefaultValueSql("(sysdatetime())")
                .HasColumnName("updated_at");
            entity.Property(e => e.UserId).HasColumnName("user_id");

            entity.HasOne(d => d.Food).WithMany(p => p.UserFoodInventories)
                .HasForeignKey(d => d.FoodId)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("FK_inventory_food");

            entity.HasOne(d => d.User).WithMany(p => p.UserFoodInventories)
                .HasForeignKey(d => d.UserId)
                .HasConstraintName("FK_inventory_user");
        });

        modelBuilder.Entity<UserTrainingSchedule>(entity =>
        {
            entity.HasKey(e => e.ScheduleId);

            entity.ToTable("user_training_schedule");

            entity.HasIndex(e => new { e.UserId, e.ScheduleDate }, "UQ_schedule_user_date").IsUnique();

            entity.Property(e => e.ScheduleId).HasColumnName("schedule_id");
            entity.Property(e => e.CycleTypeId).HasColumnName("cycle_type_id");
            entity.Property(e => e.IsCompleted).HasColumnName("is_completed");
            entity.Property(e => e.ScheduleDate).HasColumnName("schedule_date");
            entity.Property(e => e.UserId).HasColumnName("user_id");

            entity.HasOne(d => d.CycleType).WithMany(p => p.UserTrainingSchedules)
                .HasForeignKey(d => d.CycleTypeId)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("FK_schedule_cycle_type");

            entity.HasOne(d => d.User).WithMany(p => p.UserTrainingSchedules)
                .HasForeignKey(d => d.UserId)
                .HasConstraintName("FK_schedule_user");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
