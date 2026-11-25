# AGENTS.md — SmartMacro Engine

> File quy tắc cho AI agent làm việc trong repo này. Đọc toàn bộ trước khi bắt đầu bất kỳ task nào.

## 1. Bối cảnh dự án

SmartMacro Engine là ứng dụng web theo dõi bữa ăn, tối ưu dinh dưỡng (quy hoạch tuyến tính, Google OR-Tools GLOP) và đề xuất luyện tập.
Đây là **đồ án môn học đồng thời là nền tảng cho luận văn tốt nghiệp** của chủ dự án.

Ưu tiên theo thứ tự: **đúng > dễ giải thích > có test > có tài liệu > gọn đẹp**.
Chủ dự án phải hiểu và bảo vệ được từng quyết định, nên tránh over-engineering và "phép màu" khó giải thích.

## 2. Stack

- Backend: .NET 8, EF Core 8, SQL Server, Google OR-Tools (GLOP), JWT + Refresh Token
- AI module: Playwright + Anthropic Claude API (module phụ, mặc định tắt)
- Frontend: React 19 + TypeScript + Vite (`SmartMacro.Web`), Zustand, Axios, oxlint
- Test: xUnit (`SmartMacro.Tests`)
- CI: GitHub Actions (`.github/workflows/`)

## 3. Tài liệu trạng thái (đọc đầu task, cập nhật cuối task)

- `docs/status/PROJECT_STATUS.md`: trạng thái hiện tại
- `docs/status/HISTORY.md`: nhật ký thay đổi
- `audit_report.md`: báo cáo khảo sát gần nhất
- `docs/decisions/`: ADR (quyết định kiến trúc). Tạo thư mục nếu chưa có.

## 4. Quy tắc Git (agent được tự commit và push)

1. Luôn làm trên nhánh `feature/<tên-task>` tách từ `develop`. Nếu đang đứng ở `develop` hoặc `main`, tạo nhánh mới trước khi commit.
2. **Được phép:** commit và push nhánh `feature/*`, mở Pull Request vào `develop`.
3. **Cấm:**
   - commit hoặc push trực tiếp vào `develop` hoặc `main`
   - `--force`, `--force-with-lease`, `reset --hard`, `rebase` trên nhánh chung
   - xóa nhánh, sửa lịch sử đã push
   - tự merge PR (chủ dự án sẽ merge)
4. **Không dùng** `git add -A` hoặc `git add .`. Chỉ add từng file thuộc phạm vi task. Trước mỗi commit phải chạy `git status` và `git diff --staged --stat`, đối chiếu với phạm vi task và báo danh sách file cho chủ dự án.
5. **Không bao giờ stage:** `.env`, `appsettings.Development.json`, file có tiền tố `secrets`, `logs/`, `bin/`, `obj/`, `node_modules/`, `dist/`.
6. Commit theo Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`, `ci:`). Mỗi commit một ý, không gom nhiều việc vào một commit.
7. Chỉ commit khi build, test, lint đã pass. Nếu push bị từ chối hoặc có xung đột, dừng lại và báo, **không tự xử lý bằng force**.
8. Dùng skill `git-guardrails-claude-code` và `resolving-merge-conflicts` trong `.agents/skills` khi phù hợp.
9. Khi tạo PR bằng `gh`, viết mô tả vào file tạm rồi dùng `--body-file`; không đưa backtick vào chuỗi truyền qua PowerShell.
10. Trước khi bắt đầu nhánh feature, đảm bảo `develop` local đã được push và đồng bộ với `origin/develop`, để PR chỉ chứa commit của chính task.

## 5. Quy trình làm việc cho mỗi task

1. Đọc `AGENTS.md`, `PROJECT_STATUS.md` và phần liên quan của code.
2. Viết **kế hoạch ngắn** (file sẽ đổi, cách làm, rủi ro) và **chờ chủ dự án xác nhận** trước khi sửa code.
3. Thực hiện trên nhánh feature, theo từng bước nhỏ. Với logic nghiệp vụ, ưu tiên viết test trước (skill `tdd`).
4. Chạy kiểm tra (mục 8) và báo kết quả thật.
5. Cập nhật `PROJECT_STATUS.md`, `HISTORY.md`.
6. Commit, push, mở PR vào `develop` kèm tóm tắt: thay đổi gì, vì sao, cách kiểm tra lại.
7. Dừng lại chờ chủ dự án duyệt. Không tự bắt đầu task kế tiếp.

## 6. Quy tắc xử lý secret và cấu hình (mức tối thiểu, phù hợp đồ án)

Đây là dự án cá nhân, không cần quy trình bảo mật như production, nhưng phải giữ mức tối thiểu sau:

1. **Không đọc, không in, không sửa** nội dung `.env`, `appsettings.Development.json` và user-secrets.
2. **Không hardcode** mật khẩu, JWT secret, API key trong code, compose, test hay tài liệu. File mẫu (`.env.example`, `*.example.json`) chỉ chứa placeholder rõ ràng như `CHANGE_ME_...`.
3. Khi phát hiện chuỗi giống secret (ví dụ API key Anthropic bắt đầu bằng `sk-ant-`) trong file được Git theo dõi, chỉ báo **tên file và số dòng**, không in giá trị.
4. Không thêm công cụ bảo mật nặng (Key Vault, lịch xoay khóa, viết lại lịch sử Git) trừ khi chủ dự án yêu cầu.

## 7. Quy tắc kiến trúc và code

**Backend**
- Giữ logic nghiệp vụ ngoài Controller. Controller chỉ nhận request, gọi service, trả response.
- Solver tối ưu phải đứng sau interface (ví dụ `IDietOptimizer`), thuần hàm, không phụ thuộc EF Core, để dễ test và dễ so sánh thuật toán.
- Mọi lỗi trả về `ProblemDetails` thống nhất. Không nuốt exception.
- Thay đổi schema phải đi kèm EF migration. **Không chạy** `dotnet ef database update` trên DB của chủ dự án nếu chưa được xác nhận.
- Mọi thay đổi trong `Models/` hoặc `SmartMacroDbContext.cs` PHẢI đi kèm EF migration trong CÙNG nhánh và CÙNG task. Trước khi commit, chạy `dotnet tool run dotnet-ef migrations has-pending-model-changes` (phải sạch) và đọc file migration sinh ra để chắc không có lệnh `Drop` ngoài ý muốn.
- Không thêm NuGet/npm package mới nếu chưa nêu lý do và được chấp thuận.
- Tên model Anthropic phải nằm trong config, không hardcode trong code. Mọi lỗi từ API Claude (model không tồn tại, hết quota, timeout) phải được xử lý và trả lỗi rõ ràng.

**Frontend**
- Không thêm logic vào `DashboardPlaceholderPage.tsx`. Khi chạm vào nó, ưu tiên tách vào `components/dashboard`, `inventory`, `optimization`, `targets`, `layout`.
- Gọi API qua Axios client sẵn có, state xác thực qua Zustand store sẵn có.
- Component mới có test (Vitest + React Testing Library khi đã cài đặt).

**Dữ liệu và khoa học (quan trọng cho luận văn)**
- Công thức dinh dưỡng, giá trị MET, bảng thành phần thực phẩm phải ghi rõ **nguồn** trong code (comment) và trong ADR.
- **Tuyệt đối không bịa** số liệu, kết quả thí nghiệm, kết quả khảo sát hay trích dẫn học thuật. Thiếu dữ liệu thì dừng lại và hỏi.
- Script benchmark chỉ được tạo để chủ dự án tự chạy. Không tự điền kết quả.
- Kiểm tra giấy phép và nguồn gốc của mọi bộ dữ liệu trước khi import.

## 8. Kiểm tra bắt buộc trước khi báo "xong"

```bash
dotnet build SmartMacroEngine.slnx --configuration Release     # 0 warning, 0 error
dotnet test  SmartMacroEngine.slnx --configuration Release     # tất cả pass
cd SmartMacro.Web
npm run lint                                                   # 0 lỗi
npx tsc -b --noEmit                                            # 0 lỗi
npm run build                                                  # thành công
npm test                                                       # khi đã có script test
```

Nếu một lệnh không chạy được (thiếu môi trường, bị chặn), phải nói rõ, không được ghi "pass" khi chưa chạy.

## 9. Định nghĩa "xong"

Code + test + tài liệu trạng thái + CI xanh + PR kèm tóm tắt (file nào đổi, vì sao, cách kiểm tra).
Với quyết định thiết kế đáng kể, thêm một ADR ngắn vào `docs/decisions/` (bối cảnh, các phương án, lý do chọn, hệ quả).

## 10. Khi nào phải dừng lại và hỏi

- Quyết định kiến trúc lớn hoặc đề bài mơ hồ: nêu 2–3 phương án kèm đánh đổi, chờ chủ dự án chọn.
- Task cần chạm vào thứ nằm ngoài phạm vi đã nêu.
- Cần dữ liệu, tài khoản, khóa hoặc quyền mà agent không có.
- Test hiện có fail vì lý do không liên quan task.
- Lệnh sắp chạy có thể mất dữ liệu hoặc không thể hoàn tác.

## 11. Phạm vi sản phẩm (để không lạc đề)

Trọng tâm luận văn, theo thứ tự ưu tiên:
1. Tối ưu khẩu phần (diet problem, LP) với ràng buộc macro, tồn kho, ngân sách
2. Nhật ký bữa ăn (meal log) và so sánh với mục tiêu
3. Đề xuất luyện tập (BMR/TDEE, MET, luật theo mục tiêu)
4. Đánh giá thực nghiệm (so sánh với baseline, khảo sát người dùng)

AI Competitor Research là module phụ: không mở rộng thêm nếu chưa được yêu cầu.