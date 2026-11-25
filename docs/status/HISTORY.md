### 2026-10-31T18:13:00+07:00 | d23b1ec | health: YELLOW
- Lần chạy khảo sát toàn diện đầu tiên: Backend (.NET 8) build xanh và vượt qua 201/201 unit/integration tests; Frontend (`SmartMacro.Web`) pass `oxlint` và `tsc` với 0 lỗi.
- Nhánh hiện tại `feature/scheduled-competitor-research` đã hoàn tất tính năng lập lịch AI Competitor Research (vượt trước `develop` 8 commits, dừng 4 ngày từ 2026-10-27) và có 5 file tạo báo cáo PDF đang untracked ở thư mục gốc.
- Phát hiện 5 lỗ hổng mức HIGH trong npm packages của `SmartMacro.Web` (`axios`, `zod`, `vite`, `follow-redirects`, `source-map-js`) và lỗ hổng HIGH ở gói NuGet transitive `System.Formats.Asn1` (`5.0.0`) trong `SmartMacro.Api`.
- Việc ưu tiên cao nhất hiện tại: Vá các lỗ hổng bảo mật mức HIGH trong dependencies của Frontend (`npm`) và Backend (`NuGet`).


### 2026-10-31T18:41:18+07:00 | d23b1ec | health: YELLOW
- Không có thay đổi kể từ lần chạy trước (`HEAD` giữ nguyên tại `d23b1ec`, toàn bộ rủi ro bảo mật dependency và 5 file untracked vẫn giữ nguyên trạng thái `[VẪN TỒN TẠI]`).
- Việc ưu tiên cao nhất hiện tại: Vá các lỗ hổng bảo mật mức HIGH trong dependencies của Frontend (`npm`) và Backend (`NuGet`).


### 2026-11-25T11:03:00+07:00 | fix/research-background-service-shutdown | FIX-01
- Khắc phục race condition khi dừng `CompetitorResearchBackgroundService` (thay `CancellationToken.None` bằng `stoppingToken` và kiểm tra `stoppingToken.IsCancellationRequested` ngay sau `Task.WhenAny`).
- Bổ sung test tái hiện `BackgroundService_StopAsync_WhenWaitingOnIntervalOrTrigger_StopsPromptly` (202/202 tests pass 10/10 lần chạy liên tiếp) và thêm `--blame-hang-timeout 60s` vào `.github/workflows/dotnet-ci.yml`.


### 2026-11-25T12:03:00+07:00 | fix/ef-unicode-migration | FIX-02
- Bổ sung EF Core Migration `SupportUnicodeVietnameseColumns` đồng bộ thay đổi `varchar` -> `nvarchar` cho 3 cột `users.full_name` (`nvarchar(150)`), `foods.food_name` (`nvarchar(200)`), `food_categories.category_name` (`nvarchar(100)`) từ commit `1a175f9`.
- Vượt qua kiểm tra `dotnet-ef migrations has-pending-model-changes` (exit code 0), `dotnet build` và `201/201` tests.


### 2026-11-25T14:30:00+07:00 | feature/p0-00-sync-state | P0-00
- Nâng `AutoMapper` từ `15.1.1` lên `15.1.4` trong `SmartMacro.Api.csproj` để xử lý dứt điểm cảnh báo bảo mật `NU1903` (`GHSA-6vhm-j9h7-f9gh`, `GHSA-gpwp-5797-mjff`), giúp `dotnet build` đạt `0 Warning(s)`.
- Đưa `AGENTS.md` (kèm quy tắc EF migration và Git/PR mới) và `audit_report.md` vào quản lý phiên bản; giải quyết xung đột và đồng bộ `docs/status/PROJECT_STATUS.md` cùng `docs/status/HISTORY.md` sau khi merge PR #25 (`FIX-02`) và PR #24 (`FIX-01`).
