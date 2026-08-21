using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace SmartMacro.Api.Migrations
{
    /// <inheritdoc />
    public partial class AddRefreshTokens : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_schedule_cycle_type",
                table: "user_training_schedule");

            migrationBuilder.DropForeignKey(
                name: "FK_rules_cycle_type",
                table: "macro_adjustment_rules");

            migrationBuilder.AlterColumn<short>(
                name: "cycle_type_id",
                table: "user_training_schedule",
                type: "smallint",
                nullable: false,
                oldClrType: typeof(byte),
                oldType: "tinyint");

            migrationBuilder.DropPrimaryKey(
                name: "PK_training_cycle_types",
                table: "training_cycle_types");

            migrationBuilder.AlterColumn<short>(
                name: "cycle_type_id",
                table: "training_cycle_types",
                type: "smallint",
                nullable: false,
                oldClrType: typeof(byte),
                oldType: "tinyint")
                .Annotation("SqlServer:Identity", "1, 1")
                .OldAnnotation("SqlServer:Identity", "1, 1");

            migrationBuilder.AddPrimaryKey(
                name: "PK_training_cycle_types",
                table: "training_cycle_types",
                column: "cycle_type_id");

            migrationBuilder.AlterColumn<short>(
                name: "cycle_type_id",
                table: "macro_adjustment_rules",
                type: "smallint",
                nullable: false,
                oldClrType: typeof(byte),
                oldType: "tinyint");

            migrationBuilder.AddForeignKey(
                name: "FK_schedule_cycle_type",
                table: "user_training_schedule",
                column: "cycle_type_id",
                principalTable: "training_cycle_types",
                principalColumn: "cycle_type_id");

            migrationBuilder.AddForeignKey(
                name: "FK_rules_cycle_type",
                table: "macro_adjustment_rules",
                column: "cycle_type_id",
                principalTable: "training_cycle_types",
                principalColumn: "cycle_type_id");

            migrationBuilder.CreateTable(
                name: "refresh_tokens",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    token = table.Column<string>(type: "varchar(128)", unicode: false, maxLength: 128, nullable: false),
                    user_id = table.Column<long>(type: "bigint", nullable: false),
                    created_at = table.Column<DateTime>(type: "datetime2(3)", precision: 3, nullable: false, defaultValueSql: "(sysdatetime())"),
                    expires_at = table.Column<DateTime>(type: "datetime2(3)", precision: 3, nullable: false),
                    revoked_at = table.Column<DateTime>(type: "datetime2(3)", precision: 3, nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_refresh_tokens", x => x.id);
                    table.ForeignKey(
                        name: "FK_refresh_tokens_user",
                        column: x => x.user_id,
                        principalTable: "users",
                        principalColumn: "user_id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_refresh_tokens_user_id",
                table: "refresh_tokens",
                column: "user_id");

            migrationBuilder.CreateIndex(
                name: "UQ_refresh_tokens_token",
                table: "refresh_tokens",
                column: "token",
                unique: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "refresh_tokens");

            migrationBuilder.DropForeignKey(
                name: "FK_schedule_cycle_type",
                table: "user_training_schedule");

            migrationBuilder.DropForeignKey(
                name: "FK_rules_cycle_type",
                table: "macro_adjustment_rules");

            migrationBuilder.AlterColumn<byte>(
                name: "cycle_type_id",
                table: "user_training_schedule",
                type: "tinyint",
                nullable: false,
                oldClrType: typeof(short),
                oldType: "smallint");

            migrationBuilder.DropPrimaryKey(
                name: "PK_training_cycle_types",
                table: "training_cycle_types");

            migrationBuilder.AlterColumn<byte>(
                name: "cycle_type_id",
                table: "training_cycle_types",
                type: "tinyint",
                nullable: false,
                oldClrType: typeof(short),
                oldType: "smallint")
                .Annotation("SqlServer:Identity", "1, 1")
                .OldAnnotation("SqlServer:Identity", "1, 1");

            migrationBuilder.AddPrimaryKey(
                name: "PK_training_cycle_types",
                table: "training_cycle_types",
                column: "cycle_type_id");

            migrationBuilder.AlterColumn<byte>(
                name: "cycle_type_id",
                table: "macro_adjustment_rules",
                type: "tinyint",
                nullable: false,
                oldClrType: typeof(short),
                oldType: "smallint");

            migrationBuilder.AddForeignKey(
                name: "FK_schedule_cycle_type",
                table: "user_training_schedule",
                column: "cycle_type_id",
                principalTable: "training_cycle_types",
                principalColumn: "cycle_type_id");

            migrationBuilder.AddForeignKey(
                name: "FK_rules_cycle_type",
                table: "macro_adjustment_rules",
                column: "cycle_type_id",
                principalTable: "training_cycle_types",
                principalColumn: "cycle_type_id");
        }
    }
}
