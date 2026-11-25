# KẾ HOẠCH SỬ DỤNG AI TRONG QUÁ TRÌNH THỰC HIỆN ĐỀ TÀI

**Đề tài:** Xây dựng ứng dụng web quản lý dinh dưỡng và tối ưu hóa bữa ăn thông minh (*SmartMacro Engine*)  
**Sinh viên thực hiện:** Lư Vĩnh An — Sinh viên năm 4, Ngành Công nghệ Thông tin  
**Đơn vị đào tạo:** Khoa Công nghệ Thông tin — Trường Đại học Công nghệ Sài Gòn (STU)  
**Repository dự án:** `SmartMacro-Engine` (`.NET 8 Web API` + `React 19 / TypeScript` + `Google OR-Tools`)  

---

## LỜI MỞ ĐẦU & TƯ DUY CỐT LÕI (HUMAN-IN-THE-LOOP)

Trong bối cảnh công nghệ phát triển nhanh, việc ứng dụng Trí tuệ nhân tạo (AI) vào quy trình phát triển phần mềm giúp rút ngắn đáng kể thời gian lặp lại các tác vụ thủ công. Tuy nhiên, đối với một sinh viên năm 4 thực hiện đồ án/luận văn tốt nghiệp, AI **không phải là công cụ "làm thay"** mà là một **trợ lý kỹ thuật tăng tốc**. Toàn bộ dự án *SmartMacro Engine* được triển khai theo nguyên tắc **Human-in-the-loop (Con người làm trung tâm kiểm soát)**:

- **Sinh viên (Người chủ trì):** Thiết kế kiến trúc 3 tầng, chốt mô hình dữ liệu và nghiệp vụ dinh dưỡng, kiểm soát phạm vi đề tài theo chuẩn Khoa CNTT (STU), đọc hiểu từng dòng mã trước khi hợp nhất, trực tiếp chạy kiểm thử (`dotnet test`, `npm run lint`, `npx tsc -b --noEmit`) và chịu trách nhiệm cuối cùng về chất lượng sản phẩm.
- **AI (Công cụ hỗ trợ):** Sinh mã khung (*boilerplate*), đề xuất phương án tối ưu, hỗ trợ viết test case biên, rà soát tài liệu kỹ thuật và tích hợp như một module tính năng có kiểm soát trong sản phẩm.

---

## MỤC 1: CÁC CÔNG CỤ AI LỰA CHỌN SỬ DỤNG & LÝ DO LỰA CHỌN

Để tránh phụ thuộc vào một công cụ duy nhất, dự án kết hợp **4 nhóm công cụ AI** theo đúng thế mạnh của từng nhóm:

| STT | Nhóm công cụ AI | Công cụ cụ thể | Lý do lựa chọn trong dự án SmartMacro Engine |
| :-: | :--- | :--- | :--- |
| **1** | **AI Coding Agent tự chủ** | **Google Antigravity / Claude Code CLI** | Có khả năng đọc ngữ cảnh đa tệp (*multi-file context*) trên toàn bộ cây thư mục `SmartMacro.Api/`, `SmartMacro.Web/`, `SmartMacro.Tests/`. Có thể thao tác trực tiếp terminal để chạy `dotnet build`, `dotnet test`, kiểm tra migration EF Core và sinh bộ kiểm thử tự động theo chuẩn xUnit. |
| **2** | **Trợ lý gợi ý code tại chỗ** | **GitHub Copilot** (Visual Studio / VS Code) | Phản hồi tức thì theo từng dòng gõ (*inline completion*). Phù hợp để tăng tốc viết mã lặp lại (*boilerplate*) như DTOs, AutoMapper Profiles, Data Annotations validation và các class tiện ích Tailwind CSS v4. |
| **3** | **LLM tư duy & nghiên cứu** | **Gemini / ChatGPT** | Mạnh ở khả năng tổng hợp thông tin, phân tích nghiệp vụ và chuẩn hóa văn phong học thuật. Dùng để khảo sát và so sánh các API dinh dưỡng (FatSecret, Edamam, Spoonacular, USDA), lên cấu trúc sơ đồ BFD/Use Case/ERD/UML và rà soát bố cục báo cáo theo đúng quy định của Khoa CNTT (STU). |
| **4** | **AI tích hợp trực tiếp vào sản phẩm** | **Anthropic Claude API + Playwright .NET** | Được tích hợp thành một module nghiệp vụ thực thụ ở Backend (`CompetitorResearchService`), kết hợp `Microsoft.Playwright` (`1.64.1`) để thu thập nội dung trang đối thủ và gọi Claude API (`AnthropicOptions`) để phân tích tính năng tự động có kiểm soát bảo mật. |

---

## MỤC 2: PHÂN BỔ VAI TRÒ CỦA AI THEO TỪNG GIAI ĐOẠN PHÁT TRIỂN ĐỀ TÀI

Bảng ma trận dưới đây phân định rạch ròi trách nhiệm giữa **Sinh viên (Người chủ trì)** và **Các công cụ AI** xuyên suốt 5 giai đoạn thực hiện đề tài:

| Giai đoạn | Hạng mục công việc | Vai trò của Sinh viên (Người chủ trì) | Vai trò của AI (Hỗ trợ) | Đầu ra thực tế được kiểm duyệt |
| :--- | :--- | :--- | :--- | :--- |
| **1. Khảo sát & Phân tích yêu cầu** | Khảo sát bài toán, API dinh dưỡng, xác định tác nhân và phạm vi chức năng | Xác định bài toán cốt lõi (quản lý kho thực phẩm cá nhân + tối ưu hóa Macro), giới hạn phạm vi 2 vai trò (`Admin`, `User`), chốt đặc tả nghiệp vụ. | Tổng hợp bảng so sánh FatSecret / Edamam / USDA; gợi ý cây phân rã chức năng (BFD) và kịch bản Use Case ban đầu. | Tài liệu đặc tả yêu cầu, sơ đồ Use Case (`<<include>>`, `<<extend>>`) đúng chuẩn STU. |
| **2. Thiết kế hệ thống & Giao diện** | Thiết kế CSDL 3 mức, sơ đồ lớp, tuần tự, hoạt động và Wireframe UI | Thiết kế chuẩn hóa 9 bảng dữ liệu (`Users`, `RefreshTokens`, `FoodCategories`, `Foods`, `UserFoodInventories`, `DailyTargets`, `TrainingCycleTypes`, `MacroAdjustmentRules`, `UserTrainingSchedules`), duyệt bố cục Wireframe. | Chuyển đổi mô tả cấu trúc thành sơ đồ SVG độ phân giải cao (ERD, Class Diagram, Sequence Diagram, Wireframe Figma-ready 1440×900). | Bộ 11 sơ đồ kỹ thuật & Wireframe chuẩn xác 100% với code thực tế trong `docs/thesis_chapter3/`. |
| **3. Lập trình Backend & Frontend** | Xây dựng `.NET 8 Web API`, EF Core 8, JWT Auth, `Google.OrTools` GLOP & `React 19` + `Tailwind CSS` | Thiết kế kiến trúc 3 tầng (`Controllers` → `Services` → `Engines` → `DbContext`), kiểm soát logic thuật toán quy hoạch tuyến tính (`MacroOptimizationEngine`), xử lý ngoại lệ và cấu hình bảo mật. | Copilot gợi ý DTOs, AutoMapper, Tailwind classes; Coding Agent hỗ trợ sinh khung CRUD, cấu hình `AnthropicOptions`, `CompetitorResearchService` và trang giao diện. | Hệ thống Backend `.NET 8` + Frontend `React 19 / TypeScript 6 / Vite 8 / Zustand 5` biên dịch sạch. |
| **4. Kiểm thử & Bảo mật** | Viết Unit/Integration Test, rà soát lỗ hổng thư viện và cấu hình | Xác định các ca biên quan trọng (hạn dùng thực phẩm, nghiệm `OPTIMAL`/`INFEASIBLE`, lỗi native OR-Tools, SSRF URL), chạy `dotnet test`, `npm audit`, `dotnet list package --vulnerable` và tự sửa các lỗ hổng phát hiện. | Hỗ trợ sinh khung test xUnit + SQLite In-Memory + FluentAssertions + Moq cho các kịch bản lặp lại; gợi ý cấu trúc test tích hợp với `WebApplicationFactory`. | **201/201 tests** vượt qua (`SmartMacro.Tests`), khóa phiên bản các gói transitive CVE trong `.csproj`. |
| **5. Báo cáo & Chuẩn bị bảo vệ** | Biên soạn tài liệu kỹ thuật, báo cáo tiến độ, slide và phản biện | Kiểm chứng mọi số liệu từ repository (`PROJECT_STATUS.md`, git history), tự nắm vững giải thích toán học GLOP và kiến trúc hệ thống để trả lời hội đồng. | Hỗ trợ chuẩn hóa văn phong học thuật, kiểm tra lỗi chính tả, xuất tài liệu Markdown/HTML sang định dạng PDF in ấn chuẩn A4. | Báo cáo Chương 3, Kế hoạch sử dụng AI (`KE_HOACH_SU_DUNG_AI_SMARTMACRO.pdf`), sẵn sàng bảo vệ. |

---

## MỤC 3: ĐÁNH GIÁ NĂNG LỰC, ĐIỂM MẠNH VÀ HẠN CHẾ CỦA TỪNG CÔNG CỤ AI

Qua quá trình áp dụng thực tế trên mã nguồn *SmartMacro Engine*, mỗi công cụ đều bộc lộ rõ ưu điểm và giới hạn cần kiểm soát:

| Công cụ AI | Điểm mạnh thực tế | Hạn chế & Rủi ro gặp phải | Biện pháp khắc phục của Sinh viên |
| :--- | :--- | :--- | :--- |
| **AI Coding Agent** (Antigravity / Claude Code CLI) | Đọc hiểu tốt quan hệ giữa `Controller` – `Service` – `Engine` – `Tests`; thực thi được chuỗi lệnh build/test liên hoàn và sửa lỗi nhanh. | Dễ rơi vào **"over-engineering"** (đề xuất kiến trúc quá phức tạp vượt quy mô đồ án sinh viên) hoặc **ảo giác phiên bản thư viện/model** (ví dụ điền tên model chưa tồn tại). | Luôn đặt ràng buộc phạm vi ngay trong prompt; không cho phép tự ý đổi kiến trúc khi chưa được duyệt; đối chiếu mọi tên gói/model với tài liệu chính thức. |
| **GitHub Copilot** | Tốc độ gợi ý cực nhanh khi viết DTO, Entity property, Validation attribute, Tailwind CSS class; giảm hẳn thao tác gõ lặp lại. | Tầm nhìn ngữ cảnh hẹp (chỉ quanh file đang mở); hay gợi ý sai logic nghiệp vụ đặc thù (ví dụ nhầm đơn vị 100g dinh dưỡng với tổng gram tồn kho trong `UserFoodInventories`). | Chỉ nhấn `Tab` chấp nhận cho mã *boilerplate*; luôn tự viết hoặc kiểm tra từng dòng đối với các biểu thức tính toán Macro và ràng buộc kho thực phẩm. |
| **Gemini / ChatGPT** | Mạnh về tư duy tổng hợp, so sánh ưu/nhược điểm API dinh dưỡng, lập bảng ma trận và rà soát tính mạch lạc của văn bản học thuật. | Không nhìn thấy trực tiếp trạng thái repo hiện tại nên dễ trả lời chung chung hoặc lệch tên bảng/tên hàm thực tế. | Đính kèm file `docs/status/PROJECT_STATUS.md` và trích đoạn mã nguồn thực tế vào ngữ cảnh trước khi yêu cầu phân tích. |
| **Anthropic Claude API** (trong `CompetitorResearchService`) | Phân tích và tóm tắt cấu trúc trang web đối thủ rất linh hoạt khi kết hợp dữ liệu DOM từ Playwright. | Chi phí gọi API theo token, phụ thuộc mạng, tiềm ẩn rủi ro **Prompt Injection** từ nội dung HTML bên ngoài hoặc **SSRF** nếu người dùng nhập URL nội bộ. | Xây dựng `TargetUrlValidator` (bắt buộc HTTPS, allowlist `AllowedHosts`, chặn IP nội bộ qua DNS), bọc dữ liệu trong thẻ `<competitor_page>` và caching theo khóa SHA256. |

---

## MỤC 4: PHƯƠNG PHÁP QUẢN LÝ NGỮ CẢNH & KỸ THUẬT ĐẶT CÂU LỆNH (PROMPT ENGINEERING)

Để AI sinh ra kết quả bám sát thực tế mã nguồn và quy chuẩn học thuật của Khoa CNTT (STU), dự án áp dụng 3 kỹ thuật quản lý ngữ cảnh cốt lõi:

1. **Duy trì bộ nhớ trạng thái bằng `docs/status/PROJECT_STATUS.md`:** Trước mỗi phiên làm việc mới với AI Agent, sinh viên cập nhật và đính kèm file trạng thái dự án (ghi rõ commit hiện tại, số lượng test 201/201, các lỗ hổng bảo mật đang mở, cấu trúc thư mục thực tế). Nhờ đó AI không bị mất ngữ cảnh hoặc tự bịa lại cấu trúc cũ.
2. **Đính kèm mẫu quy chuẩn của Khoa CNTT (STU):** Khi tạo báo cáo hoặc sơ đồ Chương 3, sinh viên cung cấp trực tiếp quy định căn lề A4 (Top 2cm, Bottom 2cm, Left 3cm, Right 2cm), font chữ, quy tắc đánh số hình/bảng và ký hiệu UML (`<<include>>`, `<<extend>>`).
3. **Áp dụng công thức Prompt 4 phần:** `[Vai trò (Role)]` + `[Ngữ cảnh thực tế (Context)]` + `[Nhiệm vụ & Ràng buộc (Task & Constraints)]` + `[Định dạng đầu ra (Output Format)]`.

### Ví dụ Prompt thực tế 1 — Sinh kiểm thử tích hợp xử lý lỗi Solver OR-Tools

```text
[Role]: Bạn là Senior .NET Backend Engineer chuyên về xUnit và ASP.NET Core Integration Testing.
[Context]: Dự án SmartMacro.Api (.NET 8) sử dụng Google.OrTools (GLOP) trong MacroOptimizationEngine.cs.
Hiện tại khi thư viện native C++ của OR-Tools bị lỗi khởi tạo (DllNotFoundException), hệ thống cần
ném SolverUnavailableException và trả về HTTP 503 qua GlobalExceptionHandler thay vì trả về HTTP 200 INFEASIBLE giả.
[Task & Constraints]: Hãy viết Integration Test trong SmartMacro.Tests dùng WebApplicationFactory
và SQLite In-Memory để kiểm chứng endpoint POST /api/optimizations trả về đúng mã 503 Service Unavailable
khi IMacroOptimizationEngine ném SolverUnavailableException. Không sửa logic nghiệp vụ của Engine.
[Output Format]: Xuất mã C# hoàn chỉnh theo chuẩn FluentAssertions và Moq đang dùng trong SmartMacro.Tests.csproj.
```

### Ví dụ Prompt thực tế 2 — Rà soát bảo mật module CompetitorResearchService

```text
[Role]: Bạn là Application Security Reviewer cho ứng dụng .NET 8 tích hợp LLM.
[Context]: Module CompetitorResearchService.cs dùng Microsoft.Playwright tải trang web từ URL đầu vào
và gửi nội dung văn bản cho Anthropic Claude API phân tích tính năng đối thủ.
[Task & Constraints]: Hãy kiểm tra 2 rủi ro chính: (1) SSRF nếu người dùng truyền URL trỏ vào localhost
hoặc dải IP nội bộ; (2) Prompt Injection ẩn trong nội dung HTML của trang đối thủ. Đề xuất thiết kế lớp
kiểm tra URL và cách cô lập dữ liệu đầu vào trước khi gửi tới IClaudeService.
[Output Format]: Liệt kê lỗ hổng cụ thể, kèm giải pháp code C# ngắn gọn dễ kiểm thử đơn vị.
```

---

## MỤC 5: QUY TRÌNH LÀM VIỆC KHÉP KÍN VỚI AI (HUMAN-IN-THE-LOOP WORKFLOW)

Mọi thay đổi mã nguồn hoặc tài liệu trong *SmartMacro Engine* đều phải đi qua **quy trình 5 bước khép kín** dưới đây, tuyệt đối không sao chép thẳng đầu ra của AI vào nhánh chính:

1. **Bước 1 — Sinh viên phân tích & viết đặc tả:** Xác định rõ mục tiêu chức năng, ràng buộc nghiệp vụ (ví dụ: giới hạn gram tồn kho, công thức tính Macro) và chuẩn bị ngữ cảnh từ mã nguồn thực tế.
2. **Bước 2 — AI đề xuất giải pháp / sinh mã khung:** AI Agent hoặc Copilot sinh bản nháp code, test case hoặc sơ đồ dựa trên Prompt 4 phần.
3. **Bước 3 — Sinh viên đọc hiểu & phản biện (Code Review):** Sinh viên đọc từng dòng code do AI tạo, loại bỏ phần *over-engineering*, kiểm tra tên thư viện/model/hàm và đối chiếu với kiến trúc 3 tầng.
4. **Bước 4 — Kiểm chứng tự động tại máy cá nhân & CI:** Chạy lần lượt `dotnet build`, `dotnet test` (201/201), `npx tsc -b --noEmit`, `npm run lint`, và pipeline `.github/workflows/dotnet-ci.yml`. Nếu có lỗi, quay lại Bước 3 để tự sửa hoặc điều chỉnh yêu cầu.
5. **Bước 5 — Lưu vết kiểm soát (Git Commit):** Chỉ khi toàn bộ kiểm tra đạt 100%, sinh viên mới thực hiện `git commit` với thông điệp rõ ràng (như `fix(solver): propagate SolverUnavailableException...`).

---

## MỤC 6: QUY TRÌNH KIỂM CHỨNG, GỠ LỖI & ĐẢM BẢO AN TOÀN BẢO MẬT

AI thường tạo ra mã nguồn "trông có vẻ chạy đúng" (*plausible code*) nhưng ẩn chứa lỗi biên hoặc lỗ hổng bảo mật. Trong dự án này, sinh viên áp dụng 4 lớp kiểm chứng bắt buộc:

### 6.1. Kiểm chứng biên dịch và kiểm thử tự động
- **Backend (.NET 8):** Chạy `dotnet build` và `dotnet test` trên `SmartMacro.Tests` (sử dụng `xunit` `2.5.3`, `Microsoft.AspNetCore.Mvc.Testing` `8.0.10`, `Microsoft.EntityFrameworkCore.Sqlite` `8.0.10`, `FluentAssertions` `8.10.0`, `Moq` `4.20.72`), đảm bảo **201/201 unit & integration tests** vượt qua 100% và duy trì **0** ghi chú `TODO`/`FIXME` tồn đọng.
- **Frontend (React 19 + TypeScript 6):** Chạy `npx tsc -b --noEmit` để kiểm tra chặt chẽ kiểu dữ liệu và `npm run lint` (`oxlint` `^1.75.0`) để phát hiện lỗi cú pháp/anti-pattern trước khi build bằng Vite 8.

### 6.2. Kiểm toán bảo mật & quản lý bí mật (Secrets & CVEs)
- **Quản lý khóa bí mật:** Tuyệt đối không đưa `AnthropicOptions:ApiKey`, JWT Secret hoặc SQL Connection String vào mã nguồn hay prompt gửi lên AI; toàn bộ được tách qua `.NET User Secrets` / biến môi trường `.env` (được ignore khỏi Git).
- **Rà soát lỗ hổng thư viện (Dependency Audit):** Định kỳ chạy `npm audit` (phát hiện 5 lỗ hổng mức `HIGH` trên các gói như `axios`, `vite`, `zod`, `follow-redirects`, `source-map-js` để theo dõi nâng cấp) và `dotnet list package --vulnerable --include-transitive`. Khi phát hiện các gói transitive cũ chứa CVE (như `System.Formats.Asn1` `5.0.0`), sinh viên đã chủ động ghim phiên bản an toàn trực tiếp trong `SmartMacro.Api.csproj` và `SmartMacro.Tests.csproj` (`System.Formats.Asn1` `8.0.1`, `System.Net.Http` `4.3.4`, `System.Text.RegularExpressions` `4.3.1`, `SQLitePCLRaw.bundle_e_sqlite3` `3.0.5`).
- **Bảo mật module AI tích hợp (`CompetitorResearchService` & `TargetUrlValidator`):**
  - Chống **SSRF**: `TargetUrlValidator.ValidateAsync` bắt buộc giao thức `HTTPS`, kiểm tra `AllowedHosts` allowlist, phân giải DNS và chặn các địa chỉ IP nội bộ/loopback thông qua `IsDisallowedIpAddress`.
  - Chống **Prompt Injection**: Nội dung thu thập từ `IPageContentFetcher` được bọc cách ly trong thẻ `<competitor_page>...</competitor_page>` kết hợp chỉ thị hệ thống (*system prompt*) yêu cầu Claude bỏ qua mọi mệnh lệnh nhúng bên trong nội dung trang web.

### 6.3. Hai tình huống thực tế sinh viên phát hiện & sửa lỗi của AI (Case Studies)

1. **Case Study 1 — Phát hiện AI "ảo giác" tên phiên bản Claude Model (`AnthropicOptions.cs`):**
   - *Hiện tượng:* Khi sinh file cấu hình `SmartMacro.Api/Options/AnthropicOptions.cs`, AI đã tự động điền giá trị mặc định cho thuộc tính `Model` là `"claude-sonnet-5-5"` — một định danh model chưa hề tồn tại trên hệ thống Anthropic API, dẫn đến nguy cơ lỗi `404 Model Not Found` khi gọi thật.
   - *Xử lý của sinh viên:* Trong bước rà soát cấu hình và ghi nhận vào `PROJECT_STATUS.md`, sinh viên phát hiện sự sai lệch tên phiên bản, đối chiếu tài liệu chính thức của Anthropic và sửa lại chính xác thành `"claude-3-5-sonnet-20241022"` (với `MaxTokens = 4096`, `TimeoutSeconds = 90`).
2. **Case Study 2 — Cắt giảm tình trạng "Over-engineering" hệ thống phân quyền:**
   - *Hiện tượng:* Ở giai đoạn thiết kế ban đầu, AI đề xuất hệ thống phân quyền phức tạp gồm 4 vai trò (`SuperAdmin`, `Admin`, `Nutritionist`, `User`) kèm bảng phân quyền động (RBAC nhiều-nhiều), làm phình to số bảng CSDL và phát sinh nhiều màn hình không cần thiết cho bài toán cốt lõi.
   - *Xử lý của sinh viên:* Sinh viên đánh giá lại phạm vi đồ án tốt nghiệp tại Khoa CNTT (STU), quyết định cắt bỏ 2 vai trò dư thừa và chuẩn hóa lại hệ thống chỉ còn đúng **2 vai trò thực chất là `Admin` và `User`** gắn trực tiếp với `Users`, giúp kiến trúc gọn gàng, tập trung sâu vào bài toán tối ưu hóa thực đơn bằng OR-Tools.

---

## MỤC 7: ĐÁNH GIÁ HIỆU QUẢ ĐỊNH LƯỢNG & ĐỊNH TÍNH KHI SỬ DỤNG AI

| Tiêu chí đánh giá | Giá trị thực tế ghi nhận trên SmartMacro Engine | Tác động & Ý nghĩa đối với sinh viên năm 4 |
| :--- | :--- | :--- |
| **Tốc độ xây dựng nền tảng & CRUD** | Rút ngắn đáng kể thời gian tạo DTO, AutoMapper Profile, EF Core Migrations và cấu trúc 9 bảng dữ liệu (`SmartMacroDbContext`). | Giúp sinh viên dành phần lớn thời gian cho phần khó nhất là mô hình toán học quy hoạch tuyến tính và kiểm soát nghiệp vụ dinh dưỡng. |
| **Độ phủ kiểm thử tự động** | Đạt **201/201 tests** (`xUnit` + `SQLite In-Memory` + `WebApplicationFactory` + `FluentAssertions` + `Moq`), chạy tự động trên GitHub Actions CI. | Tạo lưới an toàn vững chắc: mọi chỉnh sửa hay tái cấu trúc (*refactor*) đều được kiểm chứng tức thì, không sợ vỡ tính năng cũ. |
| **Chất lượng mã nguồn & tài liệu** | **0 TODO/FIXME** tồn đọng; bộ 11 sơ đồ SVG Chương 3 khớp 100% tên lớp, tên bảng và chữ ký hàm trong `SmartMacro.Api/`. | Nâng tính chuyên nghiệp của luận văn và giúp sinh viên kiểm soát đồng bộ giữa code và tài liệu thiết kế. |
| **Năng lực làm chủ công nghệ** | Sinh viên tự giải thích được ma trận ràng buộc GLOP, tự phát hiện lỗi native C++ OR-Tools, lỗi ảo giác model AI và tự vá lỗ hổng transitive CVE. | Khẳng định AI chỉ là đòn bẩy năng suất; tư duy phân tích hệ thống và trách nhiệm kỹ thuật hoàn toàn thuộc về sinh viên. |

---

## MỤC 8: VÍ DỤ MINH HỌA THỰC TẾ TỪ ĐẦU ĐẾN CUỐI (END-TO-END WALKTHROUGH)

Để minh họa rõ cách phối hợp **Human-in-the-loop** trên một tính năng cốt lõi thực thụ, dưới đây là toàn bộ nhật ký thực tế khi xây dựng và gỡ lỗi luồng **Tối ưu hóa khẩu phần ăn thông minh** (`OptimizationsController` → `OptimizationService` → `MacroOptimizationEngine` sử dụng **Google OR-Tools GLOP Solver**).

### Bước 1: Sinh viên thiết kế bài toán & đặt Prompt cho AI
Sinh viên xác định bài toán Quy hoạch tuyến tính (*Linear Programming*):
- **Biến quyết định:** Lượng gram $x_i$ cần lấy cho mỗi món ăn $i$ trong kho cá nhân (`UserFoodInventories`), với $0 \le x_i \le \text{StockGrams}_i$.
- **Ràng buộc dinh dưỡng:** Tổng Calories, Protein, Carbs, Fat đạt mục tiêu ngày (`DailyTargets`) trong biên độ sai số $\pm 5\%$ (`Tolerance = 0.05`), lọc bỏ các món có lượng khuyến nghị quá nhỏ dưới `MinGramsThreshold = 0.5` gram.
- **Bộ giải:** `Solver.CreateSolver("GLOP")` thuộc gói `Google.OrTools` (`9.15.6755`).

Sinh viên gửi prompt yêu cầu AI sinh khung `MacroOptimizationEngine.cs` và `OptimizationService.cs` theo đúng giao diện đã định nghĩa.

### Bước 2: Phát hiện lỗi nghiêm trọng trong quá trình kiểm thử & rà soát mã
Khi đọc lại mã xử lý ngoại lệ của `MacroOptimizationEngine.cs`, sinh viên phát hiện một **lỗi ngụy trang trạng thái (error masking bug)** rất nguy hiểm:
- Thư viện `Google.OrTools` phụ thuộc vào tệp nhị phân native C++ (`ortools.dll` / `libortools.so`). Khi chạy trong môi trường thiếu runtime C++ hoặc sai kiến trúc CPU, lệnh `Solver.CreateSolver("GLOP")` sẽ ném ra `DllNotFoundException`, `TypeInitializationException` hoặc `BadImageFormatException` (hoặc trả về `null`).
- Nếu khối `try/catch` xử lý chung chung hoặc gán trạng thái mặc định, API `POST /api/optimizations` sẽ trả về **HTTP 200 OK kèm kết quả giả là `INFEASIBLE`** ("không tìm thấy thực đơn phù hợp"), khiến người dùng hiểu lầm rằng tủ lạnh thiếu thức ăn trong khi thực chất hệ thống tối ưu đang bị sập!

### Bước 3: Sinh viên chỉ đạo sửa lỗi kiến trúc & kiểm chứng bằng Integration Test
Sinh viên trực tiếp thiết kế lại luồng xử lý lỗi và ghi nhận tại **commit `0636fb2`** (*"fix(solver): propagate SolverUnavailableException on native OR-Tools failure instead of returning fake 200 INFEASIBLE"*), tác động đồng bộ trên **5 tệp**:
1. `SmartMacro.Api/Exceptions/SolverUnavailableException.cs`: Định nghĩa ngoại lệ miền riêng biệt cho sự cố bộ giải.
2. `SmartMacro.Api/Engines/MacroOptimizationEngine.cs`: Bắt đích danh `DllNotFoundException`, `TypeInitializationException`, `BadImageFormatException` (và trường hợp solver `null`) để ném `SolverUnavailableException` thay vì nuốt lỗi.
3. `SmartMacro.Api/Middleware/GlobalExceptionHandler.cs`: Ánh xạ `SolverUnavailableException` sang mã phản hồi chuẩn **HTTP 503 Service Unavailable**.
4. `SmartMacro.Tests/OptimizationServiceTests.cs` & `SmartMacro.Tests/Integration/OptimizationErrorHandlingIntegrationTests.cs`: Bổ sung 144 dòng test đơn vị và test tích hợp để khóa chặt hành vi HTTP 503, đảm bảo toàn bộ **201/201 tests** đều vượt qua.

---

## KẾT LUẬN

Việc kết hợp có kỷ luật giữa 4 nhóm công cụ AI (Coding Agent, GitHub Copilot, LLM nghiên cứu và Claude API tích hợp) cùng quy trình **Human-in-the-loop 5 bước** đã giúp dự án *SmartMacro Engine* đạt tiến độ nhanh nhưng vẫn giữ được độ tin cậy kỹ thuật cao (201/201 test đạt, kiến trúc 3 tầng rõ ràng, kiểm soát chặt chẽ bảo mật và SSRF). Quan trọng hơn, sinh viên luôn giữ vai trò **người kiến trúc sư và người kiểm duyệt cuối cùng**, sẵn sàng lý giải, bảo vệ và chịu trách nhiệm cho mọi dòng mã trong luận văn tốt nghiệp tại Khoa CNTT — Trường Đại học Công nghệ Sài Gòn (STU).
