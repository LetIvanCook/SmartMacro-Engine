# Contributing to SmartMacro Engine

## Git Branching Strategy (GitFlow rút gọn)

Dự án dùng **GitFlow rút gọn** phù hợp với team nhỏ và release cycle chưa cao.

```
main        ●───────────●────────●──────  (production-ready, tag v1.0.0, v1.1.0...)
             \           \        \
release/*     ●───●        ●───●   ●──●   (staging prep, version bump, changelog)
               \   \        \   \
develop       ●──●──●──●──●──●──●──●──●  (integration branch)
              /  /  /  /
feature/*  ●──● ●──● ●──●               (short-lived, 1 task/branch)

hotfix/*  từ main → merge lại vào cả main và develop
```

### 5 loại branch

| Branch | Tạo từ | Merge vào | Mục đích |
|---|---|---|---|
| `main` | — | — | Production-ready. Chỉ nhận merge từ `release/*` hoặc `hotfix/*`. Mỗi merge phải được tag version. |
| `develop` | `main` | — | Integration branch. Tổng hợp tất cả tính năng đã hoàn thiện, chuẩn bị cho release tiếp theo. |
| `feature/<mô-tả-ngắn>` | `develop` | `develop` | 1 task / 1 branch. Merge vào `develop` qua PR (squash merge). |
| `release/<version>` | `develop` | `main` + `develop` | Chuẩn bị release: bump version, viết changelog, sửa lỗi nhỏ. |
| `hotfix/<mô-tả-ngắn>` | `main` | `main` + `develop` | Sửa lỗi nghiêm trọng trên production, không thể chờ release cycle. |

### Naming convention

```bash
# Feature — mô tả ngắn, kebab-case
feature/add-food-category-filter
feature/optimize-lp-solver-timeout

# Release — theo Semantic Versioning
release/1.1.0

# Hotfix
hotfix/fix-jwt-expiry-null-ref
```

> **Ghi chú về Phase 4 legacy:** Các branch `feature/phase4-p<N>-<slug>` (ví dụ:
> `feature/phase4-p1-cicd-pineline`) là naming convention nội bộ dùng trong Phase 4
> để phân biệt từng prompt. Các branch mới tạo sau thời điểm Prompt 5 merge sẽ theo
> convention `feature/<mô-tả-ngắn>` như bảng trên.

---

## Quy Ước Commit Message — Conventional Commits

Dự án áp dụng [Conventional Commits](https://www.conventionalcommits.org/) từ thời điểm
**Prompt 5 (18/08/2026)** trở đi.

> **Quan trọng:** Lịch sử commit trước thời điểm này (Prompt 1–4) **KHÔNG bị rewrite**.
> Convention áp dụng cho tất cả commit mới và PR title từ bây giờ.

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Các `type` được phép

| Type | Khi nào dùng |
|---|---|
| `feat` | Thêm tính năng mới |
| `fix` | Sửa bug |
| `chore` | Thay đổi không ảnh hưởng code (dependency update, config, v.v.) |
| `docs` | Thay đổi chỉ về documentation |
| `refactor` | Refactor code (không thêm tính năng, không sửa bug) |
| `test` | Thêm hoặc sửa tests |
| `ci` | Thay đổi CI/CD pipeline, GitHub Actions |
| `perf` | Cải thiện hiệu năng |
| `build` | Thay đổi build system (Dockerfile, csproj, v.v.) |
| `revert` | Revert commit trước |

### Ví dụ thực tế từ dự án này

```bash
# Từ Prompt 2 (Serilog) — đây là ví dụ commit message tốt
feat(logging): configure Serilog structured logging with JSON formatter and correlation ID

# Từ Prompt 3 (Security)
feat(security): implement rate limiting and CORS policy hardening

# Từ Prompt 4 (Docker)
feat(docker): implement hardened multi-stage dockerfile with non-root user and healthchecks

# Từ Prompt 5 (Git Branching) — convention đang áp dụng
ci: add PR title lint job and branch protection rules
docs: add CONTRIBUTING.md with GitFlow and Conventional Commits guide
```

### Scope (optional nhưng khuyến khích)

Scope giúp xác định phần nào của codebase bị ảnh hưởng:

```
feat(auth): add OAuth2 Google provider
fix(solver): handle INFEASIBLE result gracefully
refactor(dashboard): extract parallel query logic to service
test(macro-engine): add boundary value tests for LP constraints
ci(docker): pin base image to digest for reproducibility
```

---

## Quy Trình Mở PR

### Feature branch → develop

```bash
# 1. Tạo branch từ develop (đã up-to-date)
git checkout develop
git pull origin develop
git checkout -b feature/my-feature-description

# 2. Làm việc, commit theo Conventional Commits
git add .
git commit -m "feat(scope): description of change"

# 3. Push và mở PR
git push origin feature/my-feature-description
# → Mở PR trên GitHub với title theo Conventional Commits
# → PR title = commit message sau khi squash merge
```

### Yêu cầu PR

- **PR title** phải theo Conventional Commits (tự động kiểm tra bởi CI job `Lint PR Title`).
- PR vào `develop`: Require CI pass (`Build & Test (.NET 8)` + `Lint PR Title`).
- PR vào `main`: Require CI pass + CodeQL pass + tối thiểu 1 review approved.
- **Merge strategy:** Squash merge — mỗi PR = 1 commit trên develop.
- Branch sau khi merge nên được xóa khỏi remote (GitHub tự động hỏi).

### Release

```bash
# 1. Tạo release branch từ develop
git checkout develop
git pull origin develop
git checkout -b release/1.1.0

# 2. Bump version, update changelog
# 3. PR vào main
# 4. Sau khi merge vào main, tag version
git tag v1.1.0
git push origin v1.1.0

# 5. Merge release branch ngược lại vào develop
```

### Hotfix

```bash
# 1. Tạo hotfix từ main
git checkout main
git pull origin main
git checkout -b hotfix/fix-critical-bug

# 2. Sửa bug, commit
# 3. PR vào main (bypass qua PR + review)
# 4. Tag hotfix version (ví dụ: v1.0.1)
# 5. Merge vào develop để giữ đồng bộ
```

---

## Branch Protection Rules

### `main`
- ✅ Require PR trước khi merge (no direct push)
- ✅ Minimum 1 review approved
- ✅ Required status checks: `Build & Test (.NET 8)`, `CodeQL Security Scan`, `Lint PR Title`
- ✅ Require branches up to date before merging
- ✅ No force push, no bypass

### `develop`
- ✅ Require PR trước khi merge
- ✅ Required status checks: `Build & Test (.NET 8)`, `Lint PR Title`
- ⚠️ Force push được phép khi cần rebase

---

## Versioning

Áp dụng [Semantic Versioning](https://semver.org/): `vMAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (đổi API contract, xóa endpoint)
- **MINOR**: Tính năng mới tương thích ngược (`feat:`)
- **PATCH**: Bug fix (`fix:`, `hotfix/*`)

Docker image sẽ tự động được tag theo version khi push git tag `v*.*.*` lên `main`
(xem `dotnet-ci.yml` — `docker-build-push` job).
