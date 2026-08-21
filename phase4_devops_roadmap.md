# Phase 4 Roadmap — SmartMacro Engine
## Integration & Hardening (DevOps Focus)

**Chuẩn bị bởi:** Senior .NET DevOps Engineer (review độc lập)
**Ngày:** 11/08/2026
**Input:** Audit Report v2 (Giai đoạn 3 Done, hiện đang ở Giai đoạn 4 ~75-80%)

---

## 1. Bối Cảnh & Mục Tiêu Phase 4

Phase 3 (Core Feature) đã hoàn thành: LP Solver, Macro logic, 115 unit/integration tests pass, build xanh 0 warning. Phase 4 tập trung vào 4 trụ cột kỹ thuật để đưa hệ thống từ "code chạy được" sang "code sẵn sàng vận hành":

| Trụ cột | Tình trạng hiện tại | Mục tiêu Phase 4 |
|---|---|---|
| CI/CD Pipeline | Build + Test + Coverage + Docker push (đơn giản) | Multi-stage pipeline: build → test → security scan → image scan → push GHCR → deploy staging |
| Container Security | Docker push cơ bản | Multi-stage Dockerfile, non-root user, Trivy scan, digest-pinned tags |
| Structured Logging | Chưa rõ (không thấy trong audit) | Serilog structured logging + request correlation |
| Git Branching | `main`, `develop` (chưa có convention rõ) | GitFlow rút gọn + branch protection + semantic release |

---

## 2. Trụ Cột 1 — CI/CD Pipeline (GitHub Actions)

### Thiết kế pipeline đề xuất (`dotnet-ci-cd.yml`)

```
push/PR → build-and-test → security-scan (CodeQL) → docker-build-push (GHCR) → deploy-staging
```

**Các cải tiến chính so với pipeline hiện tại:**

1. **NuGet caching** (`actions/cache@v4`) — giảm thời gian restore từ ~30-60s xuống gần 0 khi cache hit.
2. **CodeQL security scan** chạy song song sau build, chặn merge nếu phát hiện lỗ hổng nghiêm trọng.
3. **Docker metadata action** (`docker/metadata-action@v5`) — tự động tag image theo `sha-<short-sha>`, semver (`vX.Y.Z` khi push tag), và `latest` chỉ khi ở default branch. Tránh tình trạng tag `latest` bị ghi đè bừa bãi.
4. **GHCR authentication** dùng `secrets.GITHUB_TOKEN` mặc định (không cần tạo PAT thủ công) — cần đảm bảo repo có `permissions: packages: write`.
5. **Docker layer caching qua GitHub Actions cache** (`cache-from/to: type=gha`) — build lần 2 trở đi nhanh hơn đáng kể.
6. **Trivy image scan** sau khi push — quét CVE mức CRITICAL/HIGH, kết quả đẩy lên tab Security của GitHub (SARIF format).
7. **Deploy stage tách riêng**, dùng GitHub Environments (`environment: staging`) — cho phép gắn required reviewers hoặc secrets riêng cho từng môi trường.
8. **Job `docker-build-push` chỉ chạy khi push vào `main` hoặc tag `v*.*.*`** — tránh build/push image không cần thiết từ PR hoặc branch `develop`.

File mẫu đầy đủ: `dotnet-ci-cd.yml` (đính kèm).

### Cách đã verify YAML (vì không thể chạy thật 100% trên GitHub)

Vì pipeline có bước gọi tới GHCR, CodeQL, Trivy — không thể "chạy thử" toàn bộ ở local một cách trung thực (cần push thật lên GitHub để test auth, permissions thực tế). Tuy nhiên, mình đã verify logic YAML bằng 3 lớp kiểm tra độc lập, **chạy thật trên container này** (không phải chỉ đọc mắt):

| Công cụ | Loại kiểm tra | Kết quả |
|---|---|---|
| `yamllint` (v1.38.0) | Cú pháp YAML thuần (indentation, key trùng, kiểu dữ liệu) | Pass — chỉ có 1 warning stylistic (thiếu `---` đầu file, không bắt buộc với GitHub Actions) |
| `actionlint` (v1.7.7, binary chính thức từ `rhysd/actionlint`) | Semantic check dành riêng cho GitHub Actions: validate cú pháp `${{ }}` expressions, kiểm tra `needs:` references có tồn tại job hay không, kiểm tra input schema của các action phổ biến (`actions/checkout`, `docker/*`, `github/codeql-action/*`), lint shell script trong các bước `run:` | Pass — **0 lỗi, 0 cảnh báo** (exit code 0) |
| Review thủ công theo docs chính thức | Đối chiếu `permissions:` scope (`contents`, `packages`, `security-events`) với yêu cầu thực tế của từng action (GHCR push cần `packages: write`, SARIF upload cần `security-events: write`); đối chiếu context `github.ref`/`github.event_name` với [GitHub Actions context docs](https://docs.github.com/actions) | Khớp — không có action nào thiếu quyền cần thiết |

**Giới hạn cần lưu ý:** `actionlint` không thể verify được: (a) secrets có tồn tại/đúng giá trị hay không (`GITHUB_TOKEN` là built-in nên OK, nhưng nếu thêm secret custom cần tự tạo trong repo settings), (b) hành vi runtime thực tế của action bên thứ ba (`aquasecurity/trivy-action`) nếu version bị thay đổi breaking, (c) network/registry availability. Khuyến nghị: chạy thử lần đầu trên một **branch test riêng** với `workflow_dispatch` trigger trước khi merge vào `main`, theo dõi tab Actions để xác nhận từng job pass trước khi tin tưởng pipeline.

---

## 3. Trụ Cột 2 — Docker & Container Hardening

Đề xuất Dockerfile multi-stage (nếu chưa có dạng này):

```dockerfile
# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY *.csproj .
RUN dotnet restore
COPY . .
RUN dotnet publish -c Release -o /app/publish --no-restore

# Runtime stage — minimal, non-root
FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS runtime
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=build /app/publish .
USER appuser
HEALTHCHECK --interval=30s --timeout=5s CMD wget -q --spider http://localhost:8080/health || exit 1
ENTRYPOINT ["dotnet", "SmartMacroEngine.dll"]
```

Điểm quan trọng:
- **Alpine base** → giảm attack surface + image size (~90MB thay vì ~200MB+).
- **Non-root user** (`appuser`) → giảm rủi ro nếu container bị compromise.
- **HEALTHCHECK** → cần thêm endpoint `/health` (dùng `AddHealthChecks()` của ASP.NET Core) để orchestrator (Docker/K8s) biết khi nào container sẵn sàng.
- Image được scan bởi Trivy ngay trong CI (xem mục 2) trước khi coi là "sẵn sàng deploy".

---

## 4. Trụ Cột 3 — Serilog Structured Logging

Hiện audit không đề cập đến logging strategy — đây là khoảng trống cần lấp trước khi vào giai đoạn UAT (khó debug production nếu chỉ có `Console.WriteLine` hoặc logging mặc định của ASP.NET Core).

**Cấu hình đề xuất (`Program.cs`):**

```csharp
using Serilog;

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog((context, services, configuration) => configuration
    .ReadFrom.Configuration(context.Configuration)
    .ReadFrom.Services(services)
    .Enrich.FromLogContext()
    .Enrich.WithMachineName()
    .Enrich.WithEnvironmentName()
    .Enrich.WithProperty("Application", "SmartMacroEngine")
    .WriteTo.Console(new Serilog.Formatting.Json.JsonFormatter())
    .WriteTo.File(
        path: "logs/smartmacro-.log",
        rollingInterval: RollingInterval.Day,
        retainedFileCountLimit: 14));

var app = builder.Build();

app.UseSerilogRequestLogging(options =>
{
    options.MessageTemplate = "HTTP {RequestMethod} {RequestPath} responded {StatusCode} in {Elapsed:0.0000} ms";
    options.EnrichDiagnosticContext = (diagnosticContext, httpContext) =>
    {
        diagnosticContext.Set("CorrelationId", httpContext.TraceIdentifier);
    };
});

app.UseExceptionHandler(); // middleware global đã có sẵn theo audit
```

Lý do chọn hướng này:
- **JSON console sink** → log ra stdout dạng JSON, tương thích trực tiếp với Docker log driver và các hệ thống log tập trung (Loki, ELK, CloudWatch, Azure Log Analytics) mà không cần parse thêm.
- **`UseSerilogRequestLogging`** thay thế logging mặc định của ASP.NET Core → mỗi request chỉ ra 1 dòng log tổng hợp (thay vì 5-10 dòng rời rạc), dễ query.
- **CorrelationId** gắn vào mọi log trong 1 request → truy vết được toàn bộ luồng xử lý của 1 request cụ thể, rất quan trọng khi debug lỗi ở LP Solver (vốn có thể chạy lâu/tốn CPU theo audit).
- **Global Exception Middleware hiện có** (theo audit, `app.UseExceptionHandler()`) nên được cấu hình để log exception qua Serilog kèm `CorrelationId`, tránh mất context khi lỗi xảy ra.

Gói NuGet cần thêm: `Serilog.AspNetCore`, `Serilog.Sinks.Console`, `Serilog.Sinks.File`, `Serilog.Enrichers.Environment`.

---

## 5. Trụ Cột 4 — Git Branching Strategy

Hiện tại chỉ có `main` và `develop`, chưa có convention cho feature/release/hotfix → dễ dẫn đến xung đột khi có nhiều người cùng làm Phase 4-5 song song (load testing, security hardening, Terraform).

**Đề xuất: GitFlow rút gọn (không dùng đầy đủ GitFlow gốc vì team nhỏ, tốc độ release chưa cao):**

```
main        ●───────●───────●──────  (production-ready, tag v1.0.0, v1.1.0...)
             \       \       \
release/*     ●───●   ●───●   ●──●   (staging prep, version bump, changelog)
               \   \   \   \
develop       ●──●──●──●──●──●───●  (integration branch)
              /  /  /  /
feature/*  ●──● ●──● ●──●          (short-lived, 1 task/branch)

hotfix/*  từ main → merge lại vào cả main và develop
```

**Quy tắc branch protection đề xuất (GitHub Settings → Branches):**

| Branch | Yêu cầu |
|---|---|
| `main` | Require PR + 1 review, required status checks (`build-and-test`, `security-scan`), require branches up to date, no force-push |
| `develop` | Require PR, required status check `build-and-test`, cho phép merge sau review nhẹ hơn |
| `feature/*`, `release/*`, `hotfix/*` | Không cần protect, nhưng nên theo naming convention để CI filter đúng |

**Versioning:** Áp dụng [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `chore:`...) trên `develop`/`release/*`, kết hợp tag `v*.*.*` trên `main` để pipeline tự tag Docker image theo semver (đã cấu hình sẵn trong workflow mẫu ở mục 2).

---

## 6. Các Hạng Mục Bảo Mật Cần Xử Lý Song Song (từ Audit v2)

Audit đã chỉ ra 2 rủi ro còn tồn đọng, nên đưa vào Phase 4 luôn thay vì để riêng:

**Rate Limiting** (chống bruteforce `/auth/login`, `/auth/refresh`):
```csharp
builder.Services.AddRateLimiter(options =>
{
    options.AddFixedWindowLimiter("AuthPolicy", opt =>
    {
        opt.PermitLimit = 5;
        opt.Window = TimeSpan.FromMinutes(1);
        opt.QueueLimit = 0;
    });
    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;
});
// app.UseRateLimiter();
// [EnableRateLimiting("AuthPolicy")] trên AuthController
```

**CORS chặt chẽ** (thay cho `AllowedHosts: "*"`):
```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("ProductionCors", policy =>
    {
        policy.WithOrigins("https://app.smartmacro.example.com") // domain thật
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});
```

---

## 7. Thứ Tự Ưu Tiên & Ước Tính Thời Gian

| # | Hạng mục | Ưu tiên | Ước tính |
|---|---|---|---|
| 1 | Nâng cấp GitHub Actions pipeline (mục 2) | Cao | 0.5-1 ngày |
| 2 | Serilog structured logging (mục 4) | Cao | 0.5 ngày |
| 3 | Rate Limiting + CORS (mục 6) | Cao | 0.5 ngày |
| 4 | Dockerfile hardening + Trivy scan (mục 3) | Trung bình | 0.5-1 ngày |
| 5 | Git branch protection rules + convention (mục 5) | Trung bình | 0.5 ngày (chủ yếu là config + thống nhất team) |
| 6 | Load testing (k6) — theo đề xuất Audit v2 | Trung bình | 1-2 ngày |
| 7 | Refactor AutoMapper (Users.Update) | Thấp | vài giờ |

**Tổng ước tính Phase 4 (DevOps scope):** ~4-6 ngày làm việc, có thể chạy song song với phần load testing/pen-test do người khác đảm nhiệm.

---

## 8. Rủi Ro & Lưu Ý Khi Triển Khai

- **`docker/build-push-action` + Trivy scan bằng digest**: workflow mẫu dùng `steps.build.outputs.digest` để scan đúng image vừa build (tránh race condition nếu có build song song). Cần `docker/build-push-action@v5` trở lên để có output này.
- **`GITHUB_TOKEN` mặc định chỉ có quyền trong phạm vi repo hiện tại** — nếu sau này cần push image sang registry khác hoặc gọi API cross-repo, phải tạo PAT/Deploy key riêng và lưu vào GitHub Secrets, không hardcode.
- **CodeQL job tốn thời gian hơn build-and-test** (thường 3-8 phút cho project .NET cỡ vừa) — nếu muốn pipeline nhanh hơn cho PR, có thể tách CodeQL chạy theo lịch (`schedule:`) thay vì mọi PR, và chỉ chặn merge vào `main`.
- Trước khi merge workflow mới vào `main`, nên test trên 1 PR thật với `workflow_dispatch` để xác nhận từng job pass trên GitHub thật (không chỉ actionlint local).
