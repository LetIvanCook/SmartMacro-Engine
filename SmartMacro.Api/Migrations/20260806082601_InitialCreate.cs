using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace SmartMacro.Api.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "food_categories",
                columns: table => new
                {
                    category_id = table.Column<short>(type: "smallint", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    category_name = table.Column<string>(type: "varchar(100)", unicode: false, maxLength: 100, nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_food_categories", x => x.category_id);
                });

            migrationBuilder.CreateTable(
                name: "training_cycle_types",
                columns: table => new
                {
                    cycle_type_id = table.Column<byte>(type: "tinyint", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    type_code = table.Column<string>(type: "varchar(20)", unicode: false, maxLength: 20, nullable: false),
                    display_name = table.Column<string>(type: "varchar(50)", unicode: false, maxLength: 50, nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_training_cycle_types", x => x.cycle_type_id);
                });

            migrationBuilder.CreateTable(
                name: "users",
                columns: table => new
                {
                    user_id = table.Column<long>(type: "bigint", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    email = table.Column<string>(type: "varchar(255)", unicode: false, maxLength: 255, nullable: false),
                    password_hash = table.Column<string>(type: "char(60)", unicode: false, fixedLength: true, maxLength: 60, nullable: false),
                    full_name = table.Column<string>(type: "varchar(150)", unicode: false, maxLength: 150, nullable: true),
                    date_of_birth = table.Column<DateOnly>(type: "date", nullable: false),
                    biological_sex = table.Column<string>(type: "varchar(10)", unicode: false, maxLength: 10, nullable: false),
                    activity_level = table.Column<string>(type: "varchar(20)", unicode: false, maxLength: 20, nullable: false, defaultValue: "moderate"),
                    goal_type = table.Column<string>(type: "varchar(20)", unicode: false, maxLength: 20, nullable: false),
                    status = table.Column<string>(type: "varchar(20)", unicode: false, maxLength: 20, nullable: false, defaultValue: "active"),
                    created_at = table.Column<DateTime>(type: "datetime2(3)", precision: 3, nullable: false, defaultValueSql: "(sysdatetime())"),
                    updated_at = table.Column<DateTime>(type: "datetime2(3)", precision: 3, nullable: false, defaultValueSql: "(sysdatetime())")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_users", x => x.user_id);
                });

            migrationBuilder.CreateTable(
                name: "activity_logs",
                columns: table => new
                {
                    activity_log_id = table.Column<long>(type: "bigint", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    user_id = table.Column<long>(type: "bigint", nullable: false),
                    log_date = table.Column<DateOnly>(type: "date", nullable: false),
                    activity_name = table.Column<string>(type: "varchar(150)", unicode: false, maxLength: 150, nullable: false),
                    duration_minutes = table.Column<short>(type: "smallint", nullable: false),
                    kcal_burned = table.Column<decimal>(type: "decimal(6,2)", nullable: false),
                    created_at = table.Column<DateTime>(type: "datetime2(3)", precision: 3, nullable: false, defaultValueSql: "(sysdatetime())")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_activity_logs", x => x.activity_log_id);
                    table.ForeignKey(
                        name: "FK_activity_user",
                        column: x => x.user_id,
                        principalTable: "users",
                        principalColumn: "user_id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "foods",
                columns: table => new
                {
                    food_id = table.Column<long>(type: "bigint", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    category_id = table.Column<short>(type: "smallint", nullable: true),
                    food_name = table.Column<string>(type: "varchar(200)", unicode: false, maxLength: 200, nullable: false),
                    barcode = table.Column<string>(type: "varchar(64)", unicode: false, maxLength: 64, nullable: true),
                    kcal_per_100g = table.Column<decimal>(type: "decimal(6,2)", nullable: false),
                    protein_g_per_100g = table.Column<decimal>(type: "decimal(6,2)", nullable: false),
                    carbs_g_per_100g = table.Column<decimal>(type: "decimal(6,2)", nullable: false),
                    fat_g_per_100g = table.Column<decimal>(type: "decimal(6,2)", nullable: false),
                    fiber_g_per_100g = table.Column<decimal>(type: "decimal(6,2)", nullable: true),
                    is_verified = table.Column<bool>(type: "bit", nullable: false),
                    source = table.Column<string>(type: "varchar(20)", unicode: false, maxLength: 20, nullable: false, defaultValue: "user_submitted"),
                    created_by = table.Column<long>(type: "bigint", nullable: true),
                    created_at = table.Column<DateTime>(type: "datetime2(3)", precision: 3, nullable: false, defaultValueSql: "(sysdatetime())")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_foods", x => x.food_id);
                    table.ForeignKey(
                        name: "FK_foods_category",
                        column: x => x.category_id,
                        principalTable: "food_categories",
                        principalColumn: "category_id",
                        onDelete: ReferentialAction.SetNull);
                    table.ForeignKey(
                        name: "FK_foods_created_by",
                        column: x => x.created_by,
                        principalTable: "users",
                        principalColumn: "user_id",
                        onDelete: ReferentialAction.SetNull);
                });

            migrationBuilder.CreateTable(
                name: "macro_adjustment_rules",
                columns: table => new
                {
                    rule_id = table.Column<long>(type: "bigint", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    user_id = table.Column<long>(type: "bigint", nullable: false),
                    cycle_type_id = table.Column<byte>(type: "tinyint", nullable: false),
                    kcal_multiplier = table.Column<decimal>(type: "decimal(4,3)", nullable: false, defaultValue: 1.000m),
                    protein_g_per_kg_bw = table.Column<decimal>(type: "decimal(4,2)", nullable: false),
                    carb_ratio = table.Column<decimal>(type: "decimal(4,3)", nullable: false),
                    fat_ratio = table.Column<decimal>(type: "decimal(4,3)", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime2(3)", precision: 3, nullable: false, defaultValueSql: "(sysdatetime())")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_macro_adjustment_rules", x => x.rule_id);
                    table.ForeignKey(
                        name: "FK_rules_cycle_type",
                        column: x => x.cycle_type_id,
                        principalTable: "training_cycle_types",
                        principalColumn: "cycle_type_id");
                    table.ForeignKey(
                        name: "FK_rules_user",
                        column: x => x.user_id,
                        principalTable: "users",
                        principalColumn: "user_id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "user_body_metrics",
                columns: table => new
                {
                    metric_id = table.Column<long>(type: "bigint", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    user_id = table.Column<long>(type: "bigint", nullable: false),
                    recorded_date = table.Column<DateOnly>(type: "date", nullable: false),
                    weight_kg = table.Column<decimal>(type: "decimal(5,2)", nullable: false),
                    height_cm = table.Column<decimal>(type: "decimal(5,2)", nullable: true),
                    body_fat_percent = table.Column<decimal>(type: "decimal(4,2)", nullable: true),
                    bmr_kcal = table.Column<decimal>(type: "decimal(6,2)", nullable: true),
                    created_at = table.Column<DateTime>(type: "datetime2(3)", precision: 3, nullable: false, defaultValueSql: "(sysdatetime())")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_user_body_metrics", x => x.metric_id);
                    table.ForeignKey(
                        name: "FK_metrics_user",
                        column: x => x.user_id,
                        principalTable: "users",
                        principalColumn: "user_id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "user_training_schedule",
                columns: table => new
                {
                    schedule_id = table.Column<long>(type: "bigint", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    user_id = table.Column<long>(type: "bigint", nullable: false),
                    schedule_date = table.Column<DateOnly>(type: "date", nullable: false),
                    cycle_type_id = table.Column<byte>(type: "tinyint", nullable: false),
                    is_completed = table.Column<bool>(type: "bit", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_user_training_schedule", x => x.schedule_id);
                    table.ForeignKey(
                        name: "FK_schedule_cycle_type",
                        column: x => x.cycle_type_id,
                        principalTable: "training_cycle_types",
                        principalColumn: "cycle_type_id");
                    table.ForeignKey(
                        name: "FK_schedule_user",
                        column: x => x.user_id,
                        principalTable: "users",
                        principalColumn: "user_id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "user_food_inventory",
                columns: table => new
                {
                    inventory_id = table.Column<long>(type: "bigint", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    user_id = table.Column<long>(type: "bigint", nullable: false),
                    food_id = table.Column<long>(type: "bigint", nullable: false),
                    quantity_grams = table.Column<decimal>(type: "decimal(8,2)", nullable: false),
                    expiry_date = table.Column<DateOnly>(type: "date", nullable: true),
                    unit_note = table.Column<string>(type: "varchar(50)", unicode: false, maxLength: 50, nullable: true),
                    updated_at = table.Column<DateTime>(type: "datetime2(3)", precision: 3, nullable: false, defaultValueSql: "(sysdatetime())")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_user_food_inventory", x => x.inventory_id);
                    table.ForeignKey(
                        name: "FK_inventory_food",
                        column: x => x.food_id,
                        principalTable: "foods",
                        principalColumn: "food_id");
                    table.ForeignKey(
                        name: "FK_inventory_user",
                        column: x => x.user_id,
                        principalTable: "users",
                        principalColumn: "user_id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "daily_targets",
                columns: table => new
                {
                    target_id = table.Column<long>(type: "bigint", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    user_id = table.Column<long>(type: "bigint", nullable: false),
                    target_date = table.Column<DateOnly>(type: "date", nullable: false),
                    target_kcal = table.Column<decimal>(type: "decimal(7,2)", nullable: false),
                    target_protein_g = table.Column<decimal>(type: "decimal(6,2)", nullable: false),
                    target_carbs_g = table.Column<decimal>(type: "decimal(6,2)", nullable: false),
                    target_fat_g = table.Column<decimal>(type: "decimal(6,2)", nullable: false),
                    computed_from_rule_id = table.Column<long>(type: "bigint", nullable: true),
                    created_at = table.Column<DateTime>(type: "datetime2(3)", precision: 3, nullable: false, defaultValueSql: "(sysdatetime())")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_daily_targets", x => x.target_id);
                    table.ForeignKey(
                        name: "FK_target_rule",
                        column: x => x.computed_from_rule_id,
                        principalTable: "macro_adjustment_rules",
                        principalColumn: "rule_id");
                    table.ForeignKey(
                        name: "FK_target_user",
                        column: x => x.user_id,
                        principalTable: "users",
                        principalColumn: "user_id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "meal_logs",
                columns: table => new
                {
                    log_id = table.Column<long>(type: "bigint", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    user_id = table.Column<long>(type: "bigint", nullable: false),
                    food_id = table.Column<long>(type: "bigint", nullable: false),
                    inventory_id = table.Column<long>(type: "bigint", nullable: true),
                    log_date = table.Column<DateOnly>(type: "date", nullable: false),
                    meal_slot = table.Column<string>(type: "varchar(20)", unicode: false, maxLength: 20, nullable: false),
                    consumed_grams = table.Column<decimal>(type: "decimal(8,2)", nullable: false),
                    kcal_snapshot = table.Column<decimal>(type: "decimal(7,2)", nullable: false),
                    protein_g_snapshot = table.Column<decimal>(type: "decimal(6,2)", nullable: false),
                    carbs_g_snapshot = table.Column<decimal>(type: "decimal(6,2)", nullable: false),
                    fat_g_snapshot = table.Column<decimal>(type: "decimal(6,2)", nullable: false),
                    is_auto_generated = table.Column<bool>(type: "bit", nullable: false, defaultValue: true),
                    created_at = table.Column<DateTime>(type: "datetime2(3)", precision: 3, nullable: false, defaultValueSql: "(sysdatetime())")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_meal_logs", x => x.log_id);
                    table.ForeignKey(
                        name: "FK_meallog_food",
                        column: x => x.food_id,
                        principalTable: "foods",
                        principalColumn: "food_id");
                    table.ForeignKey(
                        name: "FK_meallog_inventory",
                        column: x => x.inventory_id,
                        principalTable: "user_food_inventory",
                        principalColumn: "inventory_id");
                    table.ForeignKey(
                        name: "FK_meallog_user",
                        column: x => x.user_id,
                        principalTable: "users",
                        principalColumn: "user_id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_activity_user_date",
                table: "activity_logs",
                columns: new[] { "user_id", "log_date" });

            migrationBuilder.CreateIndex(
                name: "IX_daily_targets_computed_from_rule_id",
                table: "daily_targets",
                column: "computed_from_rule_id");

            migrationBuilder.CreateIndex(
                name: "UQ_target_user_date",
                table: "daily_targets",
                columns: new[] { "user_id", "target_date" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "UQ_food_categories_name",
                table: "food_categories",
                column: "category_name",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_foods_category_id",
                table: "foods",
                column: "category_id");

            migrationBuilder.CreateIndex(
                name: "IX_foods_created_by",
                table: "foods",
                column: "created_by");

            migrationBuilder.CreateIndex(
                name: "IX_foods_macro",
                table: "foods",
                columns: new[] { "kcal_per_100g", "protein_g_per_100g", "carbs_g_per_100g", "fat_g_per_100g" });

            migrationBuilder.CreateIndex(
                name: "UQ_foods_barcode",
                table: "foods",
                column: "barcode",
                unique: true,
                filter: "([barcode] IS NOT NULL)");

            migrationBuilder.CreateIndex(
                name: "IX_macro_adjustment_rules_cycle_type_id",
                table: "macro_adjustment_rules",
                column: "cycle_type_id");

            migrationBuilder.CreateIndex(
                name: "UQ_rules_user_cycletype",
                table: "macro_adjustment_rules",
                columns: new[] { "user_id", "cycle_type_id" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_meal_logs_food_id",
                table: "meal_logs",
                column: "food_id");

            migrationBuilder.CreateIndex(
                name: "IX_meal_logs_inventory_id",
                table: "meal_logs",
                column: "inventory_id");

            migrationBuilder.CreateIndex(
                name: "IX_meallog_user_date",
                table: "meal_logs",
                columns: new[] { "user_id", "log_date" });

            migrationBuilder.CreateIndex(
                name: "UQ_training_cycle_types_code",
                table: "training_cycle_types",
                column: "type_code",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_metrics_user_date_desc",
                table: "user_body_metrics",
                columns: new[] { "user_id", "recorded_date" },
                descending: new[] { false, true });

            migrationBuilder.CreateIndex(
                name: "UQ_metrics_user_date",
                table: "user_body_metrics",
                columns: new[] { "user_id", "recorded_date" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_inventory_user_expiry",
                table: "user_food_inventory",
                columns: new[] { "user_id", "expiry_date" });

            migrationBuilder.CreateIndex(
                name: "IX_inventory_user_qty",
                table: "user_food_inventory",
                columns: new[] { "user_id", "quantity_grams" });

            migrationBuilder.CreateIndex(
                name: "IX_user_food_inventory_food_id",
                table: "user_food_inventory",
                column: "food_id");

            migrationBuilder.CreateIndex(
                name: "UQ_inventory_user_food_expiry",
                table: "user_food_inventory",
                columns: new[] { "user_id", "food_id", "expiry_date" },
                unique: true,
                filter: "[expiry_date] IS NOT NULL");

            migrationBuilder.CreateIndex(
                name: "IX_user_training_schedule_cycle_type_id",
                table: "user_training_schedule",
                column: "cycle_type_id");

            migrationBuilder.CreateIndex(
                name: "UQ_schedule_user_date",
                table: "user_training_schedule",
                columns: new[] { "user_id", "schedule_date" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "UQ_users_email",
                table: "users",
                column: "email",
                unique: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "activity_logs");

            migrationBuilder.DropTable(
                name: "daily_targets");

            migrationBuilder.DropTable(
                name: "meal_logs");

            migrationBuilder.DropTable(
                name: "user_body_metrics");

            migrationBuilder.DropTable(
                name: "user_training_schedule");

            migrationBuilder.DropTable(
                name: "macro_adjustment_rules");

            migrationBuilder.DropTable(
                name: "user_food_inventory");

            migrationBuilder.DropTable(
                name: "training_cycle_types");

            migrationBuilder.DropTable(
                name: "foods");

            migrationBuilder.DropTable(
                name: "food_categories");

            migrationBuilder.DropTable(
                name: "users");
        }
    }
}
