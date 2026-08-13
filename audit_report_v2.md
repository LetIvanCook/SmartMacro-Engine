# Technical Audit Report v2 — SmartMacro Engine

## 1. Tổng Quan Dữ Liệu Thu Thập

| Metric | Giá trị (Audit v2) | Nguồn/Lệnh thực tế |
|---|---|---|
| **Tổng số Commit** | 32 | `git log --oneline \| wc -l` |
| **Branch** | `main`, `develop` | `git branch -a` |
| **Commit gần nhất** | 11/08/2026 | `git log -1 --format=%cd` |
| **Source Files (.cs)** | 78 | `find . -name "*.cs" -not -path ...` |
| **Unit/Integration Tests** | 115 Passed | `dotnet test` (Passed: 115, Failed: 0, Skipped: 0) |
| **CI/CD** | GitHub Actions | `dotnet-ci.yml` (Build, Test, Coverage, Docker push) |

## 2. Chẩn Đoán Giai Đoạn (So Sánh Before/After)

* **Giai đoạn trước (Audit v1)**: Giai đoạn 3/6 — Core Feature Development (~55-60%).
* **Giai đoạn hiện tại (Audit v2)**: **Giai đoạn 4/6 — Integration & Hardening**.
* **Mức độ hoàn thiện ước tính**: **~75-80%** (Tăng 20% so với Audit v1).

**Vòng Đời Phát Triển (Updated):**
```text
[1] Ý tưởng & Setup (Done)
[2] Data Layer & Auth Cơ Bản (Done)
[3] Core Feature (LP Solver, Macro logic) (Done)
[4] Integration & Hardening (Tests, Docker, Security, CI/CD) (In Progress - ~80%)  <-- Current Stage
[5] UAT & Tối ưu hóa (Pending)
[6] Production Release (Pending)
```

## 3. Đối Chiếu Từng Vấn Đề Trong Audit Gốc

| # | Vấn đề (Audit gốc) | Trạng thái | Bằng chứng (file/dòng cụ thể) |
|---|---|---|---|
| 1 | Controller Exception Handling không nhất quán | ✅ | `AuthController.cs` không còn `try-catch` thủ công, sử dụng Global Exception Middleware (khai báo trong `Program.cs`: `app.UseExceptionHandler()`). |
| 2 | Manual DTO Mapping trong UsersController | ⚠️ | `UsersController.cs`: Phương thức `GetUser` (dòng 33) đã sử dụng `_mapper.Map<UserDto>(user)`. Tuy nhiên, phương thức `UpdateUser` (dòng 47-51) vẫn đang map thủ công từng field (`user.FullName = request.FullName;`, v.v.). Mặc dù điều này phổ biến với Partial Update, nhưng không hoàn toàn tận dụng AutoMapper. |
| 3 | FoodCategories CRUD thiếu Update/Delete | ✅ | `FoodCategoriesController.cs`: Đã có đầy đủ `[HttpPut("{id}")]` (dòng 34) và `[HttpDelete("{id}")]` (dòng 41). |
| 4 | JWT 30-day token không có Refresh | ✅ | `appsettings.json` (dòng 24): `ExpireMinutes: 15`. `AuthController.cs`: Có `[HttpPost("refresh")]` (dòng 32, không cần Auth) và `[HttpPost("logout")]` (dòng 40, cần Auth). |
| 5 | README mâu thuẫn nội bộ | ✅ | `README.md` (dòng 28): Đã sửa "Entity Framework Core 8 (Code-First Migrations)". Dòng 60-69 giải thích rõ cách tạo DB bằng `dotnet ef database update`. |
| 6 | JWT secret hardcode | ✅ | `appsettings.json` (dòng 21): Token key là placeholder `YOUR_JWT_SECRET_KEY_MUST_BE_AT_LEAST_32_BYTES_LONG`. Không có hardcoded secrets trong repo. Tìm kiếm `.json` regex `password\|secretkey\|connectionstring` không ra kết quả hardcode thật. Lệnh `docker-compose.yml` có dùng `${JWT_SECRET}`. |

*Thêm xác minh về bảo mật Refresh Token (Task 4):* 
- `RefreshToken.cs` (dòng 13) sử dụng property `TokenHash`.
- `AuthService.cs` (dòng 221) có hàm `HashToken()` sử dụng `SHA256` để băm token trước khi lưu xuống Database và đối chiếu. Việc này làm đúng và an toàn. 

## 4. Vấn Đề Mới Phát Hiện (Regression Check)

Qua quá trình kiểm tra code độc lập (`grep`, đọc source, build project), phát hiện một số điểm:
- **Tình trạng Build**: Chạy `dotnet build` trả về **0 Warning(s), 0 Error(s)**. Rất tốt!
- **Code Consistency (UsersController Update)**: Như đã đề cập ở bảng đối chiếu, update thủ công cho `User` trong `UsersController.cs` (dòng 47-51) chưa tận dụng được `AutoMapper`. Có thể dùng `.ForAllMembers(opts => opts.Condition((src, dest, srcMember) => srcMember != null))` trong Profile của AutoMapper để giải quyết triệt để.

## 5. Next Steps — Đề Xuất Giai Đoạn Tiếp Theo

Với việc 5 task Remediation đã được xác nhận hoàn thành, dự án đã có nền tảng vững chắc (Tests, Security, CI/CD, Containerization). Hướng đi tiếp theo tập trung vào giai đoạn **Tích Hợp & Kiểm Thử Nâng Cao (Stage 4/5)**:

1. **Load Testing & Performance Tuning**: Thuật toán LP Solver (Google OR-Tools) có thể tốn CPU khi scale. Cần setup các bài test tải (ví dụ: dùng k6 hoặc JMeter) để xem endpoint `/dashboard` chịu tải được bao nhiêu RPS.
2. **Security Hardening (Pen-test)**:
   - Áp dụng Rate Limiting cho các endpoint nhạy cảm (`/auth/login`, `/auth/refresh`).
   - Cấu hình CORS policy chặt chẽ thay vì `AllowedHosts: "*"`.
3. **Refactor AutoMapper cho Update**: Xử lý nốt DTO mapping thủ công trong `UsersController.Update` để code hoàn toàn DRY.
4. **Chuẩn Bị Môi Trường Staging/Production**: Bổ sung Terraform/Bicep hoặc scripts deploy thực tế lên AWS/Azure/GCP.

## 6. Executive Summary

| Hạng mục | Đánh giá |
|---|---|
| **Giai đoạn Dự án** | **Giai đoạn 4/6 (Integration & Hardening)** |
| **Tiến độ** | ~75-80% (Core features, Security, và DevOps đã ổn định). |
| **Điểm sáng nhất** | - Build xanh (0 warnings).<br>- Test suite lớn (115 passing tests) cover tốt.<br>- Refresh Token được hash chuẩn mực bằng SHA256 thay vì lưu plaintext. |
| **Rủi ro còn tồn đọng** | - API chưa có Rate Limiting (dễ bị bruteforce login hoặc dDoS solver endpoint).<br>- Cập nhật partial DTO (Users) chưa tự động hóa hoàn toàn. |
| **Ước tính** | 2-3 tuần để hoàn thiện performance tuning, security configs và chuẩn bị cho UAT/Staging. |
