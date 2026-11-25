# Báo cáo Tình trạng Dự án — SmartMacro Engine

- **Ngày giờ tạo:** 2026-11-25 10:20:00 +07:00
- **Commit hash HEAD:** `d5cdfe4eb3fa11827df7f7e0796edce609897fed` (`chore: save current progress before running Cline agent`)
- **Nhánh hiện tại:** `develop`
- **Tổng kết sức khỏe:** **YELLOW** — Toàn bộ build, lint, typecheck và 201/201 backend tests đều PASS với 0 lỗ hổng bảo mật mức HIGH trên NuGet/npm, nhưng vẫn còn rủi ro mức CAO về secret/mật khẩu mẫu bị commit trong repo, 3 file đang sửa chưa commit, thiếu test và CI cho Frontend (`SmartMacro.Web`), và nhánh `develop` chưa được đồng bộ/phát hành lên `main`.

---

## 1. Tóm tắt

SmartMacro Engine gồm Backend API (.NET 8, EF Core 8, SQL Server, Google OR-Tools GLOP Solver), module AI Competitor Research (Playwright + Anthropic Claude API) và Frontend React 19 + TypeScript (`SmartMacro.Web`) `[ĐÃ XÁC MINH: README.md:1-36, SmartMacroEngine.slnx:1-4, SmartMacro.Web/package.json:1-40]`.
Backend hiện biên dịch sạch (0 warnings, 0 errors), vượt qua 201/201 unit & integration tests, và không phát hiện lỗ hổng NuGet hoặc npm mức high `[ĐÃ XÁC MINH: dotnet build, dotnet test, dotnet list package, npm audit]`.
Frontend (`SmartMacro.Web`) vượt qua `oxlint` và `tsc -b --noEmit`, đã có giao diện 3 tab (`dashboard`, `inventory`, `optimizer`) kèm Demo Seed trong `DashboardPlaceholderPage.tsx`, nhưng chưa có automated tests và chưa được đưa vào CI `[ĐÃ XÁC MINH: npm run lint, npx tsc -b --noEmit, SmartMacro.Web/src/pages/DashboardPlaceholderPage.tsx:28,515-541]`.
Working tree hiện có 3 file đang sửa chưa commit (`SmartMacro.Api.csproj`, `docs/status/HISTORY.md`, `docs/status/PROJECT_STATUS.md`) và `develop` đang đi trước `main` 20 commits `[ĐÃ XÁC MINH: git status --short, git log main..develop --oneline]`.
Rủi ro lớn nhất cần xử lý ngay là loại bỏ mật khẩu/JWT secret mẫu có giá trị cụ thể khỏi các file cấu hình đã track trong Git, đồng thời bổ sung CI cho Frontend và dọn dẹp trạng thái Git `[ĐÃ XÁC MINH: git ls-files, .env.example:5-6, docker-compose.yml:9,34]`.

---

## 2. Bảng sức khỏe kỹ thuật

| Hạng mục | Trạng thái | Kết quả | Lệnh đã chạy |
|---|---|---|---|
| Build Backend (.NET 8) | PASS | Thành công: `0 Warning(s)`, `0 Error(s)` (7.90s) | `dotnet build SmartMacroEngine.slnx --configuration Release` |
| Test Backend (xUnit) | PASS | `Passed: 201, Failed: 0, Skipped: 0, Total: 201` (6s) | `dotnet test SmartMacroEngine.slnx --configuration Release` |
| NuGet Vulnerabilities (`SmartMacro.Api`) | PASS | `has no vulnerable packages given the current sources` | `dotnet list SmartMacro.Api/SmartMacro.Api.csproj package --vulnerable --include-transitive` |
| NuGet Vulnerabilities (`SmartMacro.Tests`) | PASS | `has no vulnerable packages given the current sources` | `dotnet list SmartMacro.Tests/SmartMacro.Tests.csproj package --vulnerable --include-transitive` |
| Lint Frontend (`SmartMacro.Web`) | PASS | `Found 0 warnings and 0 errors` trên 20 files (116 rules, 78ms) | `npm run lint` (`oxlint`) |
| Typecheck Frontend (`SmartMacro.Web`) | PASS | Thành công, exit code 0, 0 lỗi | `npx tsc -b --noEmit` |
| npm Audit (`SmartMacro.Web`) | PASS | `found 0 vulnerabilities` | `npm audit --audit-level=high` |
| npm Outdated (`SmartMacro.Web`) | WARN | 21 gói có phiên bản mới hơn (command exit code 1 theo chuẩn `npm outdated`) | `npm outdated` |
| Test Frontend (`SmartMacro.Web`) | CHƯA CÓ | Không có script `test` trong `SmartMacro.Web/package.json:6-11` | Kiểm tra `SmartMacro.Web/package.json` |
| Quét TODO / FIXME / HACK / XXX / NotImplementedException | CLEAN | 0 kết quả trên toàn bộ `*.cs`, `*.ts`, `*.tsx` (loại trừ `bin`, `obj`, `node_modules`) | PowerShell `Select-String` trên `*.cs, *.ts, *.tsx` |

---

## 3. Tiến độ

### Đã xong
- **Core Backend API & Thuật toán tối ưu (Phases 1–4):**
  - 9 Controllers (`Auth`, `DailyTargets`, `Dashboard`, `FoodCategories`, `Foods`, `Inventory`, `Optimizations`, `Research`, `Users`) và 14 Services tương ứng `[ĐÃ XÁC MINH: SmartMacro.Api/Controllers/, SmartMacro.Api/Services/]`.
  - Bộ giải quy hoạch tuyến tính Google OR-Tools GLOP, xác thực JWT + Refresh Token, EF Core 8 SQL Server và bộ 201 unit/integration tests pass 100% `[ĐÃ XÁC MINH: SmartMacro.Api/SmartMacro.Api.csproj:13-25, dotnet test]`.
- **AI Competitor Research & Lập lịch tự động:**
  - `IClaudeService`, `TargetUrlValidator`, `PlaywrightPageContentFetcher`, `CompetitorResearchService`, `CompetitorResearchBackgroundService`, `CompetitorResearchHistoryStore` và `ResearchController` (`/api/research/analyze`, `/reports`, `/status`, `/trigger`) `[ĐÃ XÁC MINH: SmartMacro.Api/Controllers/ResearchController.cs:37-126, commits 9759bbd..d23b1ec]`.
  - Cấu hình `AnthropicOptions.Model` đã cập nhật thành `claude-3-5-sonnet-20241022` `[ĐÃ XÁC MINH: SmartMacro.Api/Options/AnthropicOptions.cs:16, SmartMacro.Api/appsettings.json:37, commit 30c55ae]`.
- **CI/CD Backend & Security Hardening:**
  - Pipeline GitHub Actions 4 stages (`pr-lint`, `build-and-test`, `security-scan` CodeQL, `docker-build-push` + Trivy) và workflow k6 load test thủ công `[ĐÃ XÁC MINH: .github/workflows/dotnet-ci.yml:1-200, .github/workflows/load-test.yml:1-80]`.
- **Frontend Auth & Giao diện 3 màn hình (`SmartMacro.Web`):**
  - Đã dựng `LoginPage.tsx`, `RegisterPage.tsx`, `ProtectedRoute.tsx`, Axios client + Zustand auth store, và giao diện 3 tab (`dashboard`, `inventory`, `optimizer`) kèm Demo Seed `[ĐÃ XÁC MINH: SmartMacro.Web/src/routes/AppRoutes.tsx:14-30, SmartMacro.Web/src/pages/DashboardPlaceholderPage.tsx:28-60,515-541, commits 9e2b8b6, 93963b2, 1a175f9]`.

### Đang dở
- **Tái cấu trúc & Kiểm thử Frontend (`SmartMacro.Web`):**
  - Toàn bộ UI 3 tab hiện nằm trong một file `DashboardPlaceholderPage.tsx` (1.215 dòng) dù đã tạo sẵn các thư mục `components/dashboard`, `components/inventory`, `components/optimization`, `components/targets`, `components/layout`; chưa có unit/integration test cho Frontend `[ĐÃ XÁC MINH: SmartMacro.Web/src/pages/DashboardPlaceholderPage.tsx, SmartMacro.Web/package.json:6-11]`.
- **Tích hợp CI/CD & Docker cho Frontend + Staging:**
  - `.github/workflows/dotnet-ci.yml` chưa có job build/lint cho `SmartMacro.Web`; `deploy-staging` vẫn là placeholder; `docker-compose.yml` chưa có service cho `SmartMacro.Web` `[ĐÃ XÁC MINH: .github/workflows/dotnet-ci.yml, docker-compose.yml:3-42]`.
- **Đồng bộ tài liệu & nhánh Git:**
  - `README.md` chưa cập nhật danh sách đầy đủ các controller/endpoint mới (`Foods`, `Inventory`, `DailyTargets`, `Optimizations`, `Research`) và `SmartMacro.Web` `[ĐÃ XÁC MINH: README.md:130-177,246-258]`.
  - Working tree còn 3 file modified chưa commit (`SmartMacro.Api/SmartMacro.Api.csproj`, `docs/status/HISTORY.md`, `docs/status/PROJECT_STATUS.md`) `[ĐÃ XÁC MINH: git status --short, git diff --stat]`.
  - Nhánh `develop` (`d5cdfe4`) đang vượt trước `main` (`a2bfc8b`) 20 commits; `main` local chậm hơn `origin/main` (`63123c9`) 1 commit `[ĐÃ XÁC MINH: git log main..develop --oneline, git log -1 origin/main]`.

### Bị hỏng
- Không ghi nhận hạng mục nào bị hỏng khi chạy build, lint, typecheck hoặc test backend ở thời điểm khảo sát `[ĐÃ XÁC MINH]`.

---

## 4. Rủi ro

### CAO
1. **Lộ thông tin nhạy cảm / mật khẩu mẫu có giá trị cụ thể trong Git:**
   - `.env.example` (dòng 5–6) chứa giá trị mật khẩu `SA_PASSWORD` và `JWT_SECRET` cụ thể thay vì chuỗi placeholder rỗng/mẫu an toàn `[ĐÃ XÁC MINH: .env.example:5-6]`.
   - `docker-compose.yml` (dòng 9, 34) chứa giá trị fallback cho `SA_PASSWORD` và `JWT_SECRET` `[ĐÃ XÁC MINH: docker-compose.yml:9,34]`.
   - `SmartMacro.Api/appsettings.Development.json` đang được Git theo dõi (`git ls-files` xác nhận), dù `.gitignore:59` đã khai báo ignore file này `[ĐÃ XÁC MINH: git ls-files SmartMacro.Api/appsettings*.json .env*, .gitignore:59]`. Nếu các giá trị này bị tái sử dụng ở môi trường thật sẽ gây rủi ro chiếm quyền DB hoặc giả mạo JWT `[SUY ĐOÁN]`.

### TRUNG BÌNH
1. **Thiếu kiểm thử tự động và CI cho Frontend (`SmartMacro.Web`):**
   - `SmartMacro.Web/package.json:6-11` không có script test và `.github/workflows/dotnet-ci.yml` không chạy `npm run lint` / `tsc` / `vite build`, khiến lỗi hồi quy UI hoặc lỗi TypeScript có thể lọt qua PR `[ĐÃ XÁC MINH: .github/workflows/dotnet-ci.yml, SmartMacro.Web/package.json:6-11]`.
2. **Thay đổi chưa commit trong Working Tree:**
   - `SmartMacro.Api/SmartMacro.Api.csproj` nâng `AutoMapper` từ `15.1.1` lên `15.1.4`, kèm thay đổi ở `docs/status/HISTORY.md` và `docs/status/PROJECT_STATUS.md` chưa được commit (`git diff --stat`) `[ĐÃ XÁC MINH: git status --short, git diff -- SmartMacro.Api/SmartMacro.Api.csproj]`.
3. **Độ trễ đồng bộ nhánh và thiếu triển khai Staging:**
   - `develop` cách `main` 20 commits; `main` local lệch `origin/main` 1 commit (`63123c9`); job `deploy-staging` trong CI mới là placeholder `[ĐÃ XÁC MINH: git log main..develop --oneline, .github/workflows/dotnet-ci.yml]`.
4. **Hạn chế khi chạy AI Research trong Docker:**
   - `Dockerfile:15-21` chỉ cài `wget` trên `aspnet:8.0-bookworm-slim`, chưa cài Chromium/thư viện hệ thống cho Playwright, nên nếu bật `Research:Enabled=true` trong container sẽ lỗi khi khởi chạy trình duyệt `[ĐÃ XÁC MINH: Dockerfile:15-21]`, `[SUY ĐOÁN]`. Ngoài ra `CompetitorResearchHistoryStore` lưu kết quả trong RAM nên mất dữ liệu khi restart `[ĐÃ XÁC MINH: docs/status/PROJECT_STATUS.md:72]`.

### THẤP
1. **21 gói npm có phiên bản mới hơn (`npm outdated`):**
   - Bao gồm `@hookform/resolvers`, `@types/node`, `react`, `react-dom`, `typescript` (6.0.3 -> 7.0.2), `vite` (8.3.5 -> 8.3.8) `[ĐÃ XÁC MINH: npm outdated]`.
2. **Tài liệu `README.md` chưa phản ánh đầy đủ phạm vi hiện tại:**
   - Chưa liệt kê `SmartMacro.Web` và các API endpoints mới ngoài `Auth`, `Dashboard`, `Users` `[ĐÃ XÁC MINH: README.md:130-177,246-258]`.
3. **Code organization ở Frontend:**
   - `DashboardPlaceholderPage.tsx` dài 1.215 dòng và vẫn giữ tên "Placeholder" trong khi các thư mục `components/dashboard`, `inventory`, `optimization`, `targets`, `layout` đang tồn tại `[ĐÃ XÁC MINH: SmartMacro.Web/src/pages/DashboardPlaceholderPage.tsx]`.

---

## 5. Các bước tiếp theo

1. **[P0] Loại bỏ mật khẩu/JWT secret mẫu có giá trị cụ thể khỏi các file tracked và untrack `appsettings.Development.json`**
   - **Lý do:** Giảm rủi ro lộ/tái sử dụng credential trong `.env.example`, `docker-compose.yml` và `SmartMacro.Api/appsettings.Development.json` `[ĐÃ XÁC MINH]`.
   - **Tiêu chí hoàn thành:** `.env.example` và `docker-compose.yml` chỉ dùng placeholder rõ ràng (không chứa mật khẩu/key mẫu cố định); `git ls-files` không còn `SmartMacro.Api/appsettings.Development.json`.

2. **[P1] Xử lý và commit/hoàn tác 3 file đang sửa dở trong working tree**
   - **Lý do:** Đảm bảo trạng thái Git sạch và đồng bộ nâng cấp `AutoMapper 15.1.4` trước khi tạo PR `[ĐÃ XÁC MINH]`.
   - **Tiêu chí hoàn thành:** `git status --short` không còn file modified ngoài ý muốn (trừ `audit_report.md` nếu chưa commit).

3. **[P1] Bổ sung job CI cho Frontend (`SmartMacro.Web`) vào `.github/workflows/dotnet-ci.yml`**
   - **Lý do:** Hiện CI chỉ kiểm tra `.NET 8`, bỏ sót hoàn toàn `oxlint`, `tsc -b --noEmit` và `vite build` `[ĐÃ XÁC MINH]`.
   - **Tiêu chí hoàn thành:** Mỗi PR vào `develop`/`main` tự động chạy `npm ci`, `npm run lint`, `npx tsc -b --noEmit` và `npm run build` thành công.

4. **[P2] Tách `DashboardPlaceholderPage.tsx` (1.215 dòng) vào các component con và thêm Frontend tests**
   - **Lý do:** Giảm độ phức tạp bảo trì và bù đắp khoảng trống chưa có test tự động cho Frontend `[ĐÃ XÁC MINH]`.
   - **Tiêu chí hoàn thành:** Đổi tên trang chính khỏi `Placeholder`, tách logic vào `components/dashboard`, `inventory`, `optimization`, `targets`, và có tối thiểu smoke/unit tests chạy qua script `npm test`.

5. **[P2] Đồng bộ `main` với `origin/main` và mở PR phát hành `develop` -> `main` sau khi ổn định**
   - **Lý do:** `develop` đang đi trước `main` 20 commits và `main` local chậm hơn `origin/main` 1 commit `[ĐÃ XÁC MINH]`.
   - **Tiêu chí hoàn thành:** `main` cập nhật đủ các thay đổi đã kiểm thử và CI trên `main` chạy xanh.

6. **[P3] Cập nhật `README.md` và bổ sung `SmartMacro.Web` vào `docker-compose.yml` (nếu cần chạy full-stack container)**
   - **Lý do:** Đồng bộ tài liệu kiến trúc/API Surface với code thực tế và hỗ trợ chạy toàn hệ thống bằng Docker `[ĐÃ XÁC MINH]`.
   - **Tiêu chí hoàn thành:** `README.md` mô tả đủ 9 controllers và `SmartMacro.Web`; `docker compose up` khởi chạy được cả API và Web.

---

## 6. Câu hỏi cần chủ dự án trả lời

1. **Về 3 file đang sửa chưa commit** (`SmartMacro.Api/SmartMacro.Api.csproj`, `docs/status/HISTORY.md`, `docs/status/PROJECT_STATUS.md`): Bạn muốn giữ nâng cấp `AutoMapper 15.1.4` và commit cả 3 file này vào `develop`, hay giữ nguyên bản cũ?
2. **Về `SmartMacro.Api/appsettings.Development.json` đang bị Git theo dõi:** Bạn có đồng ý `git rm --cached` file này để `.gitignore` có hiệu lực và chuyển cấu hình dev nhạy cảm sang `dotnet user-secrets`?
3. **Về nhánh `feature/ai-competitor-research` và `feature/scheduled-competitor-research`:** Cả hai nhánh hiện đã được hợp nhất vào `develop` (0 commit vượt trước `develop`), bạn có muốn xóa hai nhánh này để dọn repo không?
4. **Về `SmartMacro.Web`:** Bạn muốn ưu tiên tách nhỏ `DashboardPlaceholderPage.tsx` + viết test cho Frontend trước, hay ưu tiên tích hợp UI cho tính năng AI Competitor Research?
5. **Về triển khai thực tế:** Job `deploy-staging` trong `.github/workflows/dotnet-ci.yml` hiện vẫn là placeholder — bạn dự định triển khai lên môi trường nào (Azure, VPS Docker, hay chỉ chạy local phục vụ đồ án)?

---

## 7. Hạn chế của lần khảo sát này

- **Không chạy `npm run build` (`vite build`):** Bỏ qua theo ràng buộc chỉ đọc (tránh ghi bundle `dist/` ra đĩa); đã thay thế bằng `npx tsc -b --noEmit` và `npm run lint`.
- **Không chạy `dotnet ef database update` và `k6` load test (`load-tests/dashboard-load-test.js`):** Bỏ qua để tránh tác dụng phụ ghi vào SQL Server hoặc tạo tải mạng.
- **Không đọc nội dung `.env` và `SmartMacro.Api/appsettings.Development.json`:** Tuân thủ ràng buộc không đọc/in giá trị khóa, mật khẩu, token; chỉ kiểm tra trạng thái theo dõi Git qua `git ls-files`.
- **Không kiểm tra GitHub Issues/PRs trực tiếp qua `gh` CLI:** Chỉ phân tích dựa trên lịch sử Git local và các file trong workspace.
