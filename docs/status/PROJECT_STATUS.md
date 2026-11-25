---
last_run: 2026-10-31T18:13:00+07:00
last_commit: d23b1ec36ef2812c3309ae93ee2ba572ea339702
run_type: first
health: YELLOW
---
# Trạng thái dự án: SmartMacro Engine

## 1. Tóm tắt trong 5 dòng
SmartMacro Engine là hệ thống tối ưu hóa dinh dưỡng tự động dựa trên ràng buộc (Linear Programming với Google OR-Tools GLOP Solver), gồm Backend API (.NET 8 / EF Core 8 / SQL Server), module AI Competitor Research (Playwright + Claude API) và Frontend React 19 + TypeScript (`SmartMacro.Web`) [ĐÃ XÁC MINH: `README.md:1-36`, `SmartMacro.Api/Program.cs:132-162`, `SmartMacro.Web/package.json:1-39`].
Dự án đã hoàn tất Phase 4 (Integration & Hardening - release `v1.0.0` trên `main` ngày 2026-08-21, kèm giải quyết 4 backlog issues `#6`, `#7`, `#8`, `#9` trên `develop`), hoàn thành Sprint 1 Frontend (Auth Flow), và vừa phát triển xong tính năng AI Competitor Research tự động theo lịch trên nhánh `feature/scheduled-competitor-research` [ĐÃ XÁC MINH: `audit_report_v3.md:1-95`, commits `a2bfc8b`, `9e2b8b6`, `d23b1ec`].
Sức khỏe hiện tại đạt mức **YELLOW**: toàn bộ lệnh build, lint, typecheck và 201/201 unit/integration tests đều PASS tuyệt đối với 0 lỗi/0 cảnh báo [ĐÃ XÁC MINH: `dotnet build`, `dotnet test`, `npm run lint`].
Tuy nhiên, hệ thống đang tồn tại lỗ hổng bảo mật mức HIGH trong cả gói npm của `SmartMacro.Web` (5 gói: `axios`, `vite`, `zod`, `follow-redirects`, `source-map-js`) lẫn gói NuGet bắc cầu (transitive) của `.NET` (`System.Formats.Asn1` 5.0.0 ở `SmartMacro.Api`), cùng với 5 file tạo báo cáo PDF chưa được theo dõi (untracked) trong working tree [ĐÃ XÁC MINH: `npm audit`, `dotnet list package --vulnerable --include-transitive`, `git status`].
Việc quan trọng nhất cần làm ngay là vá các lỗ hổng dependency mức HIGH (`npm audit fix` và ghim phiên bản gói NuGet bắc cầu an toàn), dọn dẹp working tree, và mở PR hợp nhất nhánh `feature/scheduled-competitor-research` (đang vượt trước `develop` 8 commits) [ĐÃ XÁC MINH: `git log develop..HEAD --oneline`].

## 3. Sức khỏe kỹ thuật

| Hạng mục | Trạng thái | Kết quả chi tiết | Bằng chứng thực tế |
|---|---|---|---|
| **Build (Backend)** | ✅ PASS | Thành công, `0 Warning(s)`, `0 Error(s)` (10.39s) | [ĐÃ XÁC MINH] `dotnet build SmartMacroEngine.slnx --configuration Release` (exit code 0) |
| **Build / Typecheck (Frontend)** | ✅ PASS | Thành công, `0 Error(s)` | [ĐÃ XÁC MINH] `npx tsc -b --noEmit` tại `SmartMacro.Web` (exit code 0) |
| **Test (Backend)** | ✅ PASS | `201 Passed`, `0 Failed`, `0 Skipped` (2m 18s) | [ĐÃ XÁC MINH] `dotnet test SmartMacroEngine.slnx --configuration Release --no-build` |
| **Test (Frontend)** | ⚠️ N/A | Không xác định được lệnh test trong `SmartMacro.Web` | [ĐÃ XÁC MINH] `SmartMacro.Web/package.json:6-11` chỉ có `dev`, `build`, `lint`, `preview` |
| **Lint (Frontend)** | ✅ PASS | `0 warnings and 0 errors` trên 18 files (116 rules, 86ms) | [ĐÃ XÁC MINH] `npm run lint` (`oxlint`) tại `SmartMacro.Web` |
| **Dependency (Backend NuGet)** | ⚠️ WARN | **3 gói transitive có CVE ở `SmartMacro.Api`** (`System.Formats.Asn1` `5.0.0` **HIGH** `GHSA-447r-wph3-92pm`; `Azure.Identity` `1.10.3` Moderate; `Microsoft.Identity.Client` `4.56.0` Moderate/Low) và **6 gói transitive ở `SmartMacro.Tests`** (thêm `SQLitePCLRaw.lib.e_sqlite3` `2.1.6` HIGH, `System.Net.Http` `4.3.0` HIGH, `System.Text.RegularExpressions` `4.3.0` HIGH). Có 8 gói top-level có bản mới hơn (như `System.IdentityModel.Tokens.Jwt` `8.14.0` -> `8.23.0`). | [ĐÃ XÁC MINH] `dotnet list SmartMacro.Api/SmartMacro.Api.csproj package --vulnerable --include-transitive --no-restore` & `--outdated` |
| **Dependency (Frontend npm)** | ❌ HIGH VULN | **5 lỗ hổng mức HIGH** (`axios` `1.19.0`, `vite` `8.2.2`, `zod` `4.4.3`, `follow-redirects`, `source-map-js`). Có 20 gói npm có bản cập nhật mới hơn. | [ĐÃ XÁC MINH] `npm audit` (exit code 1) & `npm outdated` tại `SmartMacro.Web` |
| **TODO / FIXME / HACK / XXX** | ✅ CLEAN | **0 mục** trong mã nguồn chính (`SmartMacro.Api`, `SmartMacro.Tests`, `SmartMacro.Web/src`), **0 test bị skip** | [ĐÃ XÁC MINH] Quét regex `\b(TODO|FIXME|HACK|XXX|NotImplementedException)\b` trên toàn bộ `*.cs`, `*.ts`, `*.tsx` (loại trừ `bin/`, `obj/`, `node_modules/`) |

### Hạn chế của lần chạy này
- **Không chạy `gh` CLI (GitHub Issues/PRs)**: Bỏ qua vì ràng buộc an toàn cấm truy cập mạng ngoài việc kiểm tra dependency chuẩn.
- **Không chạy `dotnet ef database update` và `k6` load test (`load-tests/dashboard-load-test.js`)**: Bỏ qua vì rủi ro tác dụng phụ ghi vào SQL Server local hoặc khởi tạo tải mạng.
- **Không chạy `npm run build` ghi ra đĩa**: Chỉ chạy `npx tsc -b --noEmit` và `npm run lint` để đảm bảo chế độ CHỈ ĐỌC tuyệt đối với cây thư mục dự án.

## 4. Tiến độ

### Đã hoàn thành (Có bằng chứng)
- **Nền tảng Backend & Thuật toán cốt lõi (Phases 1–3)**:
  - Mô hình dữ liệu EF Core 8 Code-First với 11 thực thể và migrations đầy đủ (`InitialCreate`, `AddRefreshTokens`, `HashRefreshTokens`, `FixCycleTypeIdType`) [ĐÃ XÁC MINH: `SmartMacro.Api/Models/SmartMacroDbContext.cs`, `SmartMacro.Api/Migrations/`].
  - Bộ giải quy hoạch tuyến tính `MacroOptimizationEngine` dùng Google OR-Tools GLOP Solver, xử lý tách biệt lỗi native `SolverUnavailableException` (HTTP 503/500) thay vì trả về giả định `INFEASIBLE` [ĐÃ XÁC MINH: `SmartMacro.Api/Engines/MacroOptimizationEngine.cs`, commit `0636fb2`].
  - Xác thực JWT (15 phút) kèm Refresh Token rotation & revocation băm SHA256, BCrypt password hashing [ĐÃ XÁC MINH: `SmartMacro.Api/Services/AuthService.cs`, commit `4ab5352`].
  - Toàn bộ CRUD APIs cho `Users`, `Foods`, `FoodCategories`, `Inventory` (có `ExpiryDate`), `DailyTargets`, `Dashboard` (`Task.WhenAll`), và `Optimizations` (`generate-plan`) [ĐÃ XÁC MINH: `SmartMacro.Api/Controllers/`].
- **DevOps, Bảo mật & Hardening (Phase 4 — Release `v1.0.0`)**:
  - CI/CD GitHub Actions 4 stages (`pr-lint`, `build-and-test`, `security-scan` với CodeQL, `docker-build-push` kèm Trivy scan, `deploy-staging`) và workflow k6 load test [ĐÃ XÁC MINH: `.github/workflows/dotnet-ci.yml:1-329`, `.github/workflows/load-test.yml`].
  - Serilog structured JSON logging kèm `CorrelationId`, Rate Limiting (`AuthPolicy` và `research` — 5 req/phút), CORS tường minh, ForwardedHeaders cho Reverse Proxy, và Data Protection key persistence ra filesystem (`dp-keys`) [ĐÃ XÁC MINH: `SmartMacro.Api/Program.cs:23-240`, commits `11b3444`, `3a5ab2b`, `d64b2e7`].
  - Giải quyết xong cả 4 backlog issues từ Audit v3 (`#6`, `#7`, `#8`, `#9`) và merge vào `develop` / `main` [ĐÃ XÁC MINH: commits `d64b2e7`, `0636fb2`, `3a5ab2b`, `11b3444`, `a2bfc8b`].
- **Frontend Sprint 1 — Scaffolding & Auth Flow (`SmartMacro.Web`)**:
  - Khởi tạo ứng dụng React 19 + TypeScript + Vite + Tailwind CSS v4 + Zustand + Axios interceptor hỗ trợ Silent Token Refresh, trang `LoginPage`, `RegisterPage`, `ProtectedRoute` [ĐÃ XÁC MINH: commit `9e2b8b6`, `SmartMacro.Web/src/routes/AppRoutes.tsx:1-43`, `SmartMacro.Web/src/api/client.ts`].
- **AI Competitor Research & Scheduled Background Service (trên nhánh feature)**:
  - Xây dựng `IClaudeService` với Polly resilience retry, `TargetUrlValidator` chống SSRF (chặn IP nội bộ + allowlist domain), `PlaywrightPageContentFetcher` cào nội dung bằng headless Chromium, và `CompetitorResearchService` chống prompt injection [ĐÃ XÁC MINH: `SmartMacro.Api/Services/CompetitorResearchService.cs:40-132`, `SmartMacro.Api/Services/PlaywrightPageContentFetcher.cs:58-128`, commits `9759bbd`..`d78ff52`].
  - Xây dựng `CompetitorResearchBackgroundService` chạy định kỳ hoặc kích hoạt thủ công qua `Channel<bool>`, lưu lịch sử vào `CompetitorResearchHistoryStore`, và mở các endpoints `POST /api/research/analyze`, `GET /api/research/reports`, `GET /api/research/status`, `POST /api/research/trigger` kèm bộ 201 unit/integration tests pass 100% [ĐÃ XÁC MINH: `SmartMacro.Api/Controllers/ResearchController.cs:37-126`, `SmartMacro.Api/Services/CompetitorResearchBackgroundService.cs:11-165`, commit `d23b1ec`].

### Đang dở dang
- **Nhánh đang làm việc (`feature/scheduled-competitor-research`)**:
  - Commit cuối: `d23b1ec36ef2812c3309ae93ee2ba572ea339702` (`2026-10-27 00:20:04 +0700` — cách đây **4 ngày** không có commit mới) [ĐÃ XÁC MINH: `git log -1`].
  - Nhánh `feature/scheduled-competitor-research` (cùng nhánh tiền nhiệm `feature/ai-competitor-research` ở `7d28b33`) đang vượt trước `develop` (`97cf1b8`, commit cuối ngày `2026-08-21`) **8 commits** nhưng chưa được merge vào `develop` [ĐÃ XÁC MINH: `git log develop..HEAD --oneline`, `git branch -a -v`].
  - Nhánh `main` ở local (`a2bfc8b`) đang chậm hơn `origin/main` (`63123c9` - "Add MIT License to the project") 1 commit [ĐÃ XÁC MINH: `git branch -a -v`].
- **Thay đổi chưa commit trong Working Tree**:
  - Không có file tracked nào bị sửa (`git diff --stat` trống, `git stash list` trống), nhưng có **5 file untracked** ở thư mục gốc phục vụ việc xuất báo cáo kiến trúc PDF: `build_architectural_report.py`, `report_content.html`, `SmartMacro_Architectural_Report.pdf`, `test_chrome.pdf`, `test_render.pdf` [ĐÃ XÁC MINH: `git status`, `build_architectural_report.py:1-5`].
- **Frontend Sprints 2, 3, 4 (`SmartMacro.Web`)**:
  - Sau khi đăng nhập, route `/dashboard` hiện vẫn đang trỏ tới trang stub `DashboardPlaceholderPage.tsx` hiển thị lộ trình dự kiến cho Sprint 2 (Food Catalog & Inventory), Sprint 3 (Daily Targets & Chu kỳ tập luyện), và Sprint 4 (Flagship Optimization Dashboard) [ĐÃ XÁC MINH: `SmartMacro.Web/src/routes/AppRoutes.tsx:28-30`, `SmartMacro.Web/src/pages/DashboardPlaceholderPage.tsx:70-103`].
- **Tích hợp CI/CD & Docker cho các thành phần mới**:
  - Job `deploy-staging` trong `.github/workflows/dotnet-ci.yml:306-329` vẫn là bước placeholder (`echo "--- Replace this step with actual deploy command ---"`).
  - `SmartMacro.Web` chưa có job build/lint/test trong `.github/workflows/dotnet-ci.yml` và chưa có service trong `docker-compose.yml` [ĐÃ XÁC MINH: `.github/workflows/dotnet-ci.yml`, `docker-compose.yml:1-45`].

### Bị hỏng hoặc rủi ro
- **[RỦI RO BẢO MẬT - CAO] Lỗ hổng Dependency trên cả Frontend và Backend**:
  - `SmartMacro.Web`: 5 gói báo lỗ hổng mức **HIGH** qua `npm audit`, đáng chú ý nhất là `axios` (`1.19.0` - SSRF/Prototype Pollution/Header Injection), `zod` (`4.4.3` - DoS memory exhaustion), `vite` (`8.2.2`), `follow-redirects`, `source-map-js` [ĐÃ XÁC MINH: `npm audit`].
  - `SmartMacro.Api`: Gói transitive `System.Formats.Asn1` `5.0.0` có lỗ hổng mức **HIGH** (`GHSA-447r-wph3-92pm`), kéo theo từ `Microsoft.EntityFrameworkCore.SqlServer` `8.0.10` / `Microsoft.Data.SqlClient` [ĐÃ XÁC MINH: `dotnet list SmartMacro.Api/SmartMacro.Api.csproj package --vulnerable --include-transitive --no-restore`].
- **[RỦI RO VẬN HÀNH - TRUNG BÌNH] Cấu hình Model ID của Anthropic và Playwright trong Docker**:
  - Giá trị mặc định `AnthropicOptions.Model` đang đặt là `"claude-sonnet-5-5"` trong `SmartMacro.Api/Options/AnthropicOptions.cs:16` và `SmartMacro.Api/appsettings.json:37` [ĐÃ XÁC MINH]. Nếu tên model này không khớp với model ID hợp lệ trên Anthropic API thực tế, các lời gọi thật sẽ trả lỗi 400/404 [SUY ĐOÁN].
  - `Dockerfile` hiện dùng ảnh nền `mcr.microsoft.com/dotnet/aspnet:8.0-bookworm-slim` và chỉ cài `wget` [ĐÃ XÁC MINH: `Dockerfile:15-21`], chưa cài đặt trình duyệt Chromium và thư viện hệ thống cho Playwright. Mặc dù `Research:Enabled` đang tắt (`false`) ở Production [ĐÃ XÁC MINH: `SmartMacro.Api/appsettings.json:42`], nếu bật `Research:Enabled=true` trong container Docker thì `PlaywrightPageContentFetcher` sẽ lỗi khi khởi chạy Chromium [SUY ĐOÁN].
  - `CompetitorResearchHistoryStore` lưu kết quả hoàn toàn trên bộ nhớ RAM (`List<CompetitorAnalysisResult>`, tối đa 100 bản ghi) [ĐÃ XÁC MINH: `SmartMacro.Api/Services/CompetitorResearchHistoryStore.cs:8-10`], nên lịch sử phân tích sẽ mất khi restart container/ứng dụng.
- **[LƯU Ý BẢO MẬT CẤU HÌNH] File cấu hình môi trường phát triển trong Git**:
  - File `.env` ở thư mục gốc đang có trên ổ đĩa nhưng đã được ignore an toàn trong `.gitignore` (không bị commit) [ĐÃ XÁC MINH: `git status`, `git ls-files`].
  - Tuy nhiên, repo có commit khóa JWT mẫu dùng cho môi trường dev/local tại `SmartMacro.Api/appsettings.Development.json:22`, giá trị fallback của `JWT_SECRET` và `SA_PASSWORD` trong `docker-compose.yml:9,34`, và token mẫu trong `postman/environments/Local - Dev.environment.yaml` [ĐÃ XÁC MINH: `git ls-files`]. Cần đảm bảo tuyệt đối không dùng các giá trị fallback này ở môi trường staging/production.

## 5. Các bước tiếp theo (xếp theo ưu tiên)

| Ưu tiên | Việc cần làm | Lý do | Độ khó | File / Module liên quan | Tiêu chí hoàn thành |
|---|---|---|---|---|---|
| **P1** | Vá các lỗ hổng bảo mật mức HIGH trong dependencies của Frontend (`npm`) và Backend (`NuGet`) | `npm audit` phát hiện 5 lỗ hổng HIGH (`axios`, `zod`, `vite`...) và `dotnet list package --vulnerable` phát hiện `System.Formats.Asn1` `5.0.0` (HIGH) trong `SmartMacro.Api`. | **S** | `SmartMacro.Web/package.json`, `SmartMacro.Web/package-lock.json`, `SmartMacro.Api/SmartMacro.Api.csproj`, `SmartMacro.Tests/SmartMacro.Tests.csproj` | `npm audit` trả về 0 vulnerabilities (exit code 0); `dotnet list package --vulnerable --include-transitive` trả về 0 lỗ hổng cho cả `SmartMacro.Api` và `SmartMacro.Tests`; toàn bộ test vẫn pass. |
| **P1** | Hợp nhất (PR & Merge) nhánh `feature/scheduled-competitor-research` vào `develop` và xử lý 5 file untracked | Nhánh feature hiện đã hoàn thiện code + 201 tests pass nhưng đang nằm riêng 4 ngày qua (vượt `develop` 8 commits); working tree đang vướng 5 file tạo báo cáo PDF chưa rõ cần lưu vào `docs/` hay đưa vào `.gitignore`. | **S** | `.gitignore`, `build_architectural_report.py`, `SmartMacro_Architectural_Report.pdf`, nhánh `feature/scheduled-competitor-research` -> `develop` | `git status` sạch hoàn toàn; PR từ `feature/scheduled-competitor-research` vượt qua CI (`Build & Test`, `Lint PR Title`) và được merge vào `develop`. |
| **P1** | Kiểm tra và xác nhận cấu hình `Anthropic:Model` (`claude-sonnet-5-5`) cùng tài liệu API cho `ResearchController` | Đảm bảo model ID mặc định hoạt động đúng với Anthropic API thật và cập nhật `README.md` (mục API Surface) bổ sung 4 endpoints `/api/research/*`. | **S** | `SmartMacro.Api/Options/AnthropicOptions.cs`, `SmartMacro.Api/appsettings.json`, `README.md` | Gọi thử nghiệm thành công với API key thật (hoặc xác nhận model ID hợp lệ) và `README.md` liệt kê đầy đủ các endpoints `/api/research/analyze`, `/reports`, `/status`, `/trigger`. |
| **P2** | Bổ sung bước kiểm tra Frontend (`SmartMacro.Web`) vào CI pipeline (`.github/workflows/dotnet-ci.yml`) | Hiện tại CI chỉ kiểm tra `.NET 8`, mọi thay đổi trên `SmartMacro.Web` chưa được tự động chạy `npm ci`, `npm run lint` và `npm run build` khi mở PR. | **S** | `.github/workflows/dotnet-ci.yml`, `SmartMacro.Web/package.json` | GitHub Actions workflow có job `frontend-build-and-lint` chạy pass `npm ci && npm run lint && npm run build` trên mỗi push/PR. |
| **P2** | Triển khai các tính năng Frontend Sprints 2–4 trên `SmartMacro.Web` thay thế cho `DashboardPlaceholderPage` | Giao diện sau đăng nhập hiện chỉ là trang placeholder (`DashboardPlaceholderPage.tsx`), chưa kết nối với các API Inventory, DailyTargets, và Optimization/Dashboard đã có sẵn ở Backend. | **L** | `SmartMacro.Web/src/pages/`, `SmartMacro.Web/src/api/`, `SmartMacro.Web/src/routes/AppRoutes.tsx` | Người dùng đăng nhập trên Web có thể xem Dashboard thật (`/api/dashboard/{userId}/dashboard`), quản lý Inventory, thiết lập Daily Targets và kích hoạt tính toán thực đơn tối ưu (`generate-plan`). |
| **P3** | Hỗ trợ cài đặt Playwright Chromium tùy chọn trong `Dockerfile` hoặc tách worker cho AI Research khi chạy container | Nếu bật `Research:Enabled=true` trong môi trường Docker (`bookworm-slim`), Playwright sẽ cần trình duyệt Chromium và các gói thư viện hệ thống đi kèm. | **M** | `Dockerfile`, `docker-compose.yml` | Container chạy được kịch bản `POST /api/research/analyze` khi bật `Research:Enabled=true` mà không bị lỗi thiếu binary trình duyệt của Playwright. |

## 6. Câu hỏi cần chủ dự án trả lời
1. **Về 5 file untracked ở thư mục gốc** (`build_architectural_report.py`, `report_content.html`, `SmartMacro_Architectural_Report.pdf`, `test_chrome.pdf`, `test_render.pdf`): Bạn muốn lưu trữ báo cáo chính thức vào thư mục `docs/` rồi xóa các file nháp (`test_*.pdf`, `report_content.html`), hay thêm toàn bộ chúng vào `.gitignore`?
2. **Về mã model Anthropic mặc định (`"claude-sonnet-5-5"`)** tại `SmartMacro.Api/Options/AnthropicOptions.cs:16` và `appsettings.json:37`: Đây là model ID chủ đích của bạn hay cần điều chỉnh lại theo định danh chuẩn của Anthropic API?
3. **Về tính năng AI Competitor Research (`ResearchController`)**: Bạn có dự định lưu trữ lịch sử báo cáo phân tích đối thủ xuống cơ sở dữ liệu SQL Server (EF Core table) thay vì chỉ lưu trong RAM (`CompetitorResearchHistoryStore` tối đa 100 bản ghi, mất khi khởi động lại) trước khi merge vào `develop` không?
4. **Về trọng tâm phát triển tiếp theo sau khi merge nhánh Research**: Bạn muốn ưu tiên phát triển tiếp **Frontend Sprint 2–4** (`SmartMacro.Web` — Inventory, Daily Targets, Optimization Dashboard) hay xây dựng giao diện UI cho tính năng **Competitor Research**?

## 7. Bối cảnh để quay lại làm việc

### Cách chạy dự án & Lệnh thường dùng
- **Backend API (.NET 8)**:
  - Restore & Build: `dotnet build SmartMacroEngine.slnx --configuration Release`
  - Chạy toàn bộ 201 Unit & Integration Tests: `dotnet test SmartMacroEngine.slnx`
  - Cập nhật Database (SQL Server): `dotnet tool run dotnet-ef database update --project SmartMacro.Api --startup-project SmartMacro.Api`
  - Cấu hình API Key cho AI Research (Local User Secrets):
    `dotnet user-secrets set "Anthropic:ApiKey" "<your-api-key>" --project SmartMacro.Api`
  - Cài đặt trình duyệt Chromium cho Playwright (Local):
    `pwsh SmartMacro.Api/bin/Debug/net8.0/playwright.ps1 install chromium`
  - Chạy API: `dotnet run --project SmartMacro.Api` (Swagger UI tại `/swagger` khi chạy môi trường `Development`).
- **Frontend (`SmartMacro.Web`)**:
  - Chuyển vào thư mục: `cd SmartMacro.Web`
  - Chạy dev server (mặc định cổng `5173`, đã được cho phép trong CORS Development): `npm run dev`
  - Kiểm tra lint & kiểu dữ liệu: `npm run lint` và `npx tsc -b --noEmit`

### Quyết định kiến trúc quan trọng
- **Layered Architecture + Clean DI**: Tách biệt rõ `Controllers` -> `Services` (`Interfaces`) -> `Engines` (`IMacroOptimizationEngine` dùng Google OR-Tools GLOP) & `Models` (`SmartMacroDbContext`).
- **Bảo mật nhiều lớp**:
  - Xác thực JWT Access Token ngắn hạn (15 phút) + Refresh Token băm SHA256 lưu DB, có cơ chế tự động làm mới ngầm (Silent Refresh) ở Axios client phía Frontend (`SmartMacro.Web/src/api/client.ts`).
  - Tính năng AI Competitor Research mặc định tắt ở Production (`Research:Enabled = false`), bảo vệ chống SSRF hai lớp (trước khi mở trang qua `TargetUrlValidator` kiểm tra DNS/IP nội bộ + chặn chuyển hướng ngoài `AllowedHosts` ngay trong route interceptor của Playwright tại `PlaywrightPageContentFetcher.cs:72-105`), và bọc nội dung trang web trong thẻ `<competitor_page>` kèm chỉ thị chống Prompt Injection (`CompetitorResearchService.cs:63-90`).
  - Lập lịch tự động bằng `CompetitorResearchBackgroundService` (`BackgroundService` kết hợp `Channel<bool>` cho phép vừa chạy định kỳ theo `IntervalMinutes` vừa kích hoạt tức thời qua `POST /api/research/trigger`, dùng `SemaphoreSlim(1, 1)` chống chạy chồng chéo).
- **Quy trình GitFlow & CI**: Mọi tính năng mới đi từ nhánh `feature/*` -> mở PR vào `develop` (yêu cầu pass `Build & Test (.NET 8)` và `Lint PR Title` theo chuẩn Conventional Commits) -> từ `develop` mở PR vào `main` để phát hành.

### Nơi lần làm việc cuối dừng lại
- **Nhánh hiện tại**: `feature/scheduled-competitor-research`
- **Commit cuối cùng**: `d23b1ec` (`2026-10-27 00:20:04 +0700`) — *"feat(research): implement scheduled automated competitor research background service"*.
- **Trạng thái công việc gần nhất**: Đã hoàn thành toàn bộ phần lập lịch tự động cho Competitor Research (`CompetitorResearchBackgroundService`, `CompetitorResearchHistoryStore`, các endpoints `GET /api/research/reports`, `GET /api/research/status`, `POST /api/research/trigger`) và viết đầy đủ unit/integration tests (`CompetitorResearchScheduledTests.cs`, `ResearchIntegrationTests.cs` — tất cả 201 tests đều pass). Ngoài ra có tạo script `build_architectural_report.py` để kết xuất file `SmartMacro_Architectural_Report.pdf` (đang nằm ở dạng untracked tại thư mục gốc).
- **Cập nhật FIX-01 (`fix/research-background-service-shutdown` — PR #24 đã merge vào `develop`)**: Đã sửa race condition khi shutdown `CompetitorResearchBackgroundService` (loại bỏ `CancellationToken.None` khi chờ `_triggerChannel`, kiểm tra `stoppingToken.IsCancellationRequested` sau `Task.WhenAny`), thêm test `BackgroundService_StopAsync_WhenWaitingOnIntervalOrTrigger_StopsPromptly` (202/202 tests pass 10/10 lần liên tiếp) và thêm `--blame-hang-timeout 60s` vào `.github/workflows/dotnet-ci.yml`.
- **Cập nhật FIX-02 (`fix/ef-unicode-migration` — PR #25 đã merge vào `develop`)**: Đã bổ sung EF Core Migration `SupportUnicodeVietnameseColumns` cho 3 cột `NVARCHAR` (`users.full_name`, `foods.food_name`, `food_categories.category_name`) từ commit `1a175f9`, giúp `dotnet-ef migrations has-pending-model-changes` sạch hoàn toàn (exit code 0).
- **Cập nhật P0-00 (`feature/p0-00-sync-state`)**: Nâng `AutoMapper` từ `15.1.1` lên `15.1.4` trong `SmartMacro.Api.csproj` (xử lý dứt điểm cảnh báo `NU1903`, đạt `0 Warning(s)` khi build), bổ sung `AGENTS.md` và `audit_report.md` vào repo, đồng thời đồng bộ lại `PROJECT_STATUS.md` và `HISTORY.md`.
- **Cập nhật P0-01 (`feature/p0-01-cleanup-config`)**: Dọn cấu hình nhạy cảm theo quy tắc tối thiểu của dự án: thay mật khẩu/JWT cố định trong `.env.example` và `docker-compose.yml` bằng placeholder và cú pháp bắt buộc `${VAR:?message}`; gỡ theo dõi `SmartMacro.Api/appsettings.Development.json` khỏi Git (`git rm --cached`) và tạo `appsettings.Development.example.json`; bỏ hardcode tên model mặc định trong `AnthropicOptions.cs` để lấy hoàn toàn từ `appsettings.json` / biến môi trường `Anthropic__Model`, bổ sung xử lý lỗi rõ ràng (`502 Bad Gateway` - `"AI Model Unavailable"`) khi model không tồn tại hoặc bị gỡ kèm unit/integration tests (`205/205` tests pass), và cập nhật hướng dẫn `.env` / `dotnet user-secrets` trong `README.md`.
