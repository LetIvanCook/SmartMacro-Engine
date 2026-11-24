import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
HTML_PATH = os.path.join(BASE_DIR, "KE_HOACH_SU_DUNG_AI.html")
PDF_PATH = os.path.join(REPO_ROOT, "KE_HOACH_SU_DUNG_AI_SMARTMACRO.pdf")
CDP_SCRIPT = os.path.join(BASE_DIR, "render_pdf_cdp.js")

WORKFLOW_SVG = """
<svg viewBox="0 0 860 215" width="100%" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Segoe UI', Arial, sans-serif;">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e3a8a" />
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#b91c1c" />
    </marker>
  </defs>

  <!-- Step 1 -->
  <rect x="12" y="28" width="144" height="106" rx="8" fill="#eff6ff" stroke="#1d4ed8" stroke-width="1.6"/>
  <rect x="12" y="28" width="144" height="26" rx="8" fill="#1d4ed8"/>
  <text x="84" y="45" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="700">BƯỚC 1: SINH VIÊN</text>
  <text x="84" y="72" text-anchor="middle" fill="#0f172a" font-size="11" font-weight="700">Phân tích &amp; Đặc tả</text>
  <text x="84" y="90" text-anchor="middle" fill="#334155" font-size="10">Chốt nghiệp vụ, DTO,</text>
  <text x="84" y="104" text-anchor="middle" fill="#334155" font-size="10">ràng buộc GLOP &amp;</text>
  <text x="84" y="118" text-anchor="middle" fill="#334155" font-size="10">ngữ cảnh thực tế</text>

  <line x1="156" y1="81" x2="184" y2="81" stroke="#1e3a8a" stroke-width="1.8" marker-end="url(#arrow)"/>

  <!-- Step 2 -->
  <rect x="186" y="28" width="144" height="106" rx="8" fill="#f0fdf4" stroke="#15803d" stroke-width="1.6"/>
  <rect x="186" y="28" width="144" height="26" rx="8" fill="#15803d"/>
  <text x="258" y="45" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="700">BƯỚC 2: CÔNG CỤ AI</text>
  <text x="258" y="72" text-anchor="middle" fill="#0f172a" font-size="11" font-weight="700">Đề xuất &amp; Sinh khung</text>
  <text x="258" y="90" text-anchor="middle" fill="#334155" font-size="10">Agent / Copilot sinh</text>
  <text x="258" y="104" text-anchor="middle" fill="#334155" font-size="10">mã khung, test case</text>
  <text x="258" y="118" text-anchor="middle" fill="#334155" font-size="10">theo Prompt 4 phần</text>

  <line x1="330" y1="81" x2="358" y2="81" stroke="#1e3a8a" stroke-width="1.8" marker-end="url(#arrow)"/>

  <!-- Step 3 -->
  <rect x="360" y="28" width="144" height="106" rx="8" fill="#eff6ff" stroke="#1d4ed8" stroke-width="1.6"/>
  <rect x="360" y="28" width="144" height="26" rx="8" fill="#1d4ed8"/>
  <text x="432" y="45" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="700">BƯỚC 3: SINH VIÊN</text>
  <text x="432" y="72" text-anchor="middle" fill="#0f172a" font-size="11" font-weight="700">Đọc hiểu &amp; Phản biện</text>
  <text x="432" y="90" text-anchor="middle" fill="#334155" font-size="10">Loại over-engineering,</text>
  <text x="432" y="104" text-anchor="middle" fill="#334155" font-size="10">soi ảo giác tên model,</text>
  <text x="432" y="118" text-anchor="middle" fill="#334155" font-size="10">kiểm tra bảo mật</text>

  <line x1="504" y1="81" x2="532" y2="81" stroke="#1e3a8a" stroke-width="1.8" marker-end="url(#arrow)"/>

  <!-- Step 4 -->
  <rect x="534" y="28" width="144" height="106" rx="8" fill="#fffbeb" stroke="#b45309" stroke-width="1.6"/>
  <rect x="534" y="28" width="144" height="26" rx="8" fill="#b45309"/>
  <text x="606" y="45" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="700">BƯỚC 4: KIỂM CHỨNG</text>
  <text x="606" y="72" text-anchor="middle" fill="#0f172a" font-size="11" font-weight="700">Build, Test &amp; Audit</text>
  <text x="606" y="90" text-anchor="middle" fill="#334155" font-size="10">dotnet test (201/201),</text>
  <text x="606" y="104" text-anchor="middle" fill="#334155" font-size="10">tsc --noEmit, oxlint,</text>
  <text x="606" y="118" text-anchor="middle" fill="#334155" font-size="10">npm/dotnet CVE audit</text>

  <line x1="678" y1="81" x2="706" y2="81" stroke="#1e3a8a" stroke-width="1.8" marker-end="url(#arrow)"/>

  <!-- Step 5 -->
  <rect x="708" y="28" width="140" height="106" rx="8" fill="#f8fafc" stroke="#334155" stroke-width="1.6"/>
  <rect x="708" y="28" width="140" height="26" rx="8" fill="#334155"/>
  <text x="778" y="45" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="700">BƯỚC 5: LƯU VẾT</text>
  <text x="778" y="72" text-anchor="middle" fill="#0f172a" font-size="11" font-weight="700">Git Commit &amp; CI</text>
  <text x="778" y="90" text-anchor="middle" fill="#334155" font-size="10">Chỉ commit khi đạt</text>
  <text x="778" y="104" text-anchor="middle" fill="#334155" font-size="10">100% test &amp; đẩy lên</text>
  <text x="778" y="118" text-anchor="middle" fill="#334155" font-size="10">GitHub Actions CI</text>

  <!-- Feedback Loop -->
  <path d="M 606 134 L 606 176 L 432 176 L 432 138" fill="none" stroke="#b91c1c" stroke-width="1.5" stroke-dasharray="5,4" marker-end="url(#arrow-red)"/>
  <rect x="444" y="164" width="150" height="22" rx="4" fill="#fef2f2" stroke="#fecaca"/>
  <text x="519" y="179" text-anchor="middle" fill="#991b1b" font-size="10" font-weight="600">Lỗi / Không đạt → Sửa lại</text>
</svg>
"""

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Kế hoạch sử dụng AI — SmartMacro Engine</title>
<style>
  @page {{
    size: A4;
  }}
  * {{
    box-sizing: border-box;
  }}
  body {{
    font-family: "Times New Roman", Georgia, serif;
    font-size: 11.5pt;
    line-height: 1.48;
    color: #1e293b;
    margin: 0;
    padding: 0;
  }}
  .header-banner {{
    border: 1.5px solid #1e3a8a;
    border-radius: 6px;
    padding: 16px 20px;
    background: #f8fafc;
    margin-bottom: 18px;
  }}
  .uni-line {{
    font-size: 10.5pt;
    font-weight: bold;
    color: #1e3a8a;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    margin-bottom: 4px;
  }}
  .report-title {{
    font-size: 17pt;
    font-weight: bold;
    color: #0f172a;
    margin: 6px 0 8px 0;
    line-height: 1.25;
  }}
  .meta-grid {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 8px;
    font-size: 10.5pt;
  }}
  .meta-grid td {{
    padding: 3px 6px 3px 0;
    border: none;
    vertical-align: top;
  }}
  .meta-label {{
    font-weight: bold;
    color: #334155;
    width: 175px;
  }}
  h2 {{
    font-size: 13pt;
    font-weight: bold;
    color: #1e3a8a;
    border-bottom: 1.5px solid #cbd5e1;
    padding-bottom: 4px;
    margin: 18px 0 10px 0;
    break-after: avoid;
    page-break-after: avoid;
  }}
  h3 {{
    font-size: 11.5pt;
    font-weight: bold;
    color: #0f172a;
    margin: 12px 0 6px 0;
    break-after: avoid;
    page-break-after: avoid;
  }}
  p {{
    margin: 0 0 8px 0;
    text-align: justify;
  }}
  ul, ol {{
    margin: 0 0 10px 0;
    padding-left: 20px;
  }}
  li {{
    margin-bottom: 4px;
    text-align: justify;
  }}
  code {{
    font-family: "Consolas", "Courier New", monospace;
    font-size: 9.5pt;
    background: #f1f5f9;
    padding: 1px 4px;
    border-radius: 3px;
    color: #0f172a;
  }}
  table.data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0 14px 0;
    font-size: 10pt;
    line-height: 1.38;
  }}
  table.data-table thead {{
    display: table-header-group;
  }}
  table.data-table tr {{
    break-inside: avoid;
    page-break-inside: avoid;
  }}
  table.data-table th {{
    background: #1e3a8a;
    color: #ffffff;
    font-weight: bold;
    text-align: left;
    padding: 7px 8px;
    border: 1px solid #1e3a8a;
  }}
  table.data-table td {{
    padding: 6px 8px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
    text-align: left;
  }}
  table.data-table tbody tr:nth-child(even) {{
    background: #f8fafc;
  }}
  .callout {{
    border-left: 4px solid #1d4ed8;
    background: #eff6ff;
    padding: 10px 14px;
    margin: 10px 0 12px 0;
    border-radius: 0 6px 6px 0;
    break-inside: avoid;
    page-break-inside: avoid;
  }}
  .callout-warn {{
    border-left: 4px solid #b45309;
    background: #fffbeb;
    padding: 10px 14px;
    margin: 10px 0 12px 0;
    border-radius: 0 6px 6px 0;
    break-inside: avoid;
    page-break-inside: avoid;
  }}
  .prompt-box {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #334155;
    border-radius: 4px;
    padding: 9px 12px;
    margin: 8px 0 12px 0;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 9pt;
    line-height: 1.42;
    white-space: pre-wrap;
    color: #0f172a;
    break-inside: avoid;
    page-break-inside: avoid;
  }}
  .diagram-box {{
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 10px 12px 6px 12px;
    background: #ffffff;
    margin: 10px 0 12px 0;
    break-inside: avoid;
    page-break-inside: avoid;
  }}
  .diagram-caption {{
    text-align: center;
    font-size: 10pt;
    font-style: italic;
    color: #475569;
    margin-top: 4px;
  }}
  .center {{
    text-align: center !important;
  }}
</style>
</head>
<body>

<div class="header-banner">
  <div class="uni-line">Trường Đại học Công nghệ Sài Gòn (STU) — Khoa Công nghệ Thông tin</div>
  <div class="report-title">BÁO CÁO KẾ HOẠCH SỬ DỤNG AI TRONG QUÁ TRÌNH THỰC HIỆN ĐỀ TÀI</div>
  <table class="meta-grid">
    <tr>
      <td class="meta-label">Đề tài tốt nghiệp:</td>
      <td><strong>Xây dựng ứng dụng web quản lý dinh dưỡng và tối ưu hóa bữa ăn thông minh (SmartMacro Engine)</strong></td>
    </tr>
    <tr>
      <td class="meta-label">Sinh viên thực hiện:</td>
      <td><strong>Lư Vĩnh An</strong> — Sinh viên năm 4, Ngành Công nghệ Thông tin</td>
    </tr>
    <tr>
      <td class="meta-label">Kiến trúc thực tế:</td>
      <td><code>.NET 8 Web API</code> + <code>EF Core 8</code> + <code>Google.OrTools (GLOP)</code> + <code>React 19 / TypeScript 6 / Tailwind CSS 4</code></td>
    </tr>
    <tr>
      <td class="meta-label">Trạng thái kiểm chứng:</td>
      <td><code>201/201 tests</code> đạt (<code>SmartMacro.Tests</code> — xUnit + SQLite In-Memory) | <code>0 TODO/FIXME</code></td>
    </tr>
  </table>
</div>

<div class="callout">
  <strong>Tư duy cốt lõi (Human-in-the-loop):</strong> Trong suốt quá trình xây dựng <em>SmartMacro Engine</em>, AI được định vị là <strong>công cụ trợ lý kỹ thuật tăng tốc</strong>, tuyệt đối không làm thay vai trò tư duy của sinh viên. Sinh viên trực tiếp thiết kế kiến trúc 3 tầng, chốt mô hình dữ liệu 9 bảng, kiểm soát logic thuật toán quy hoạch tuyến tính, đọc hiểu từng dòng mã trước khi hợp nhất và chịu trách nhiệm cuối cùng về chất lượng, bảo mật cũng như tính đúng đắn của sản phẩm trước Hội đồng.
</div>

<h2>MỤC 1: CÁC CÔNG CỤ AI LỰA CHỌN SỬ DỤNG &amp; LÝ DO LỰA CHỌN</h2>
<p>Dự án kết hợp có chọn lọc <strong>4 nhóm công cụ AI</strong> bổ trợ lẫn nhau, mỗi nhóm đảm nhiệm một phân khúc công việc phù hợp với đặc thù kỹ thuật của hệ thống:</p>
<table class="data-table">
  <thead>
    <tr>
      <th style="width:5%;">STT</th>
      <th style="width:22%;">Nhóm công cụ AI</th>
      <th style="width:23%;">Công cụ cụ thể</th>
      <th style="width:50%;">Lý do lựa chọn trong dự án SmartMacro Engine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center"><strong>1</strong></td>
      <td><strong>AI Coding Agent tự chủ</strong></td>
      <td>Google Antigravity / Claude Code CLI</td>
      <td>Đọc hiểu ngữ cảnh đa tệp trên toàn bộ cây thư mục <code>SmartMacro.Api/</code>, <code>SmartMacro.Web/</code>, <code>SmartMacro.Tests/</code>; thao tác trực tiếp terminal để chạy <code>dotnet build</code>, <code>dotnet test</code>, kiểm tra migration EF Core và sinh bộ kiểm thử tự động.</td>
    </tr>
    <tr>
      <td class="center"><strong>2</strong></td>
      <td><strong>Trợ lý gợi ý code tại chỗ</strong></td>
      <td>GitHub Copilot (Visual Studio / VS Code)</td>
      <td>Gợi ý tức thì theo từng dòng gõ (<em>inline completion</em>), giúp tăng tốc viết mã lặp lại (<em>boilerplate</em>) như DTOs, AutoMapper Profiles, validation attributes và các class tiện ích Tailwind CSS v4.</td>
    </tr>
    <tr>
      <td class="center"><strong>3</strong></td>
      <td><strong>LLM tư duy &amp; nghiên cứu</strong></td>
      <td>Gemini / ChatGPT</td>
      <td>Hỗ trợ khảo sát và so sánh các API dinh dưỡng (FatSecret, Edamam, Spoonacular, USDA), phân tích nghiệp vụ, lên cấu trúc sơ đồ BFD/Use Case/ERD/UML và chuẩn hóa văn phong báo cáo theo quy định của Khoa CNTT (STU).</td>
    </tr>
    <tr>
      <td class="center"><strong>4</strong></td>
      <td><strong>AI tích hợp trực tiếp vào sản phẩm</strong></td>
      <td>Anthropic Claude API + Playwright .NET</td>
      <td>Đóng vai trò module nghiệp vụ ở Backend (<code>CompetitorResearchService</code>), kết hợp <code>Microsoft.Playwright</code> (<code>1.64.1</code>) để thu thập nội dung trang đối thủ và gọi Claude API (<code>AnthropicOptions</code>) phân tích tính năng tự động có kiểm soát bảo mật.</td>
    </tr>
  </tbody>
</table>

<h2>MỤC 2: PHÂN BỔ VAI TRÒ CỦA AI THEO TỪNG GIAI ĐOẠN PHÁT TRIỂN ĐỀ TÀI</h2>
<table class="data-table">
  <thead>
    <tr>
      <th style="width:17%;">Giai đoạn</th>
      <th style="width:28%;">Vai trò Sinh viên (Người chủ trì)</th>
      <th style="width:29%;">Vai trò Các công cụ AI (Hỗ trợ)</th>
      <th style="width:26%;">Đầu ra thực tế đã kiểm duyệt</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Khảo sát &amp; Phân tích yêu cầu</strong></td>
      <td>Xác định bài toán quản lý kho tủ lạnh + tối ưu hóa Macro; chốt phạm vi 2 vai trò (<code>Admin</code>, <code>User</code>); phê duyệt đặc tả.</td>
      <td>Tổng hợp bảng so sánh API dinh dưỡng; gợi ý cây phân rã chức năng (BFD) và kịch bản Use Case ban đầu.</td>
      <td>Đặc tả yêu cầu, sơ đồ Use Case chuẩn UML (<code>&lt;&lt;include&gt;&gt;</code>, <code>&lt;&lt;extend&gt;&gt;</code>).</td>
    </tr>
    <tr>
      <td><strong>2. Thiết kế hệ thống &amp; Giao diện</strong></td>
      <td>Thiết kế 9 bảng CSDL (<code>Users</code>, <code>Foods</code>, <code>UserFoodInventories</code>, <code>DailyTargets</code>...); duyệt bố cục màn hình.</td>
      <td>Chuyển đổi mô tả thành bộ sơ đồ kỹ thuật SVG (ERD 3 mức, Class, Sequence, Activity) và Wireframe Figma-ready 1440×900.</td>
      <td>Bộ 11 sơ đồ &amp; Wireframe chuẩn xác 100% với code trong <code>docs/thesis_chapter3/</code>.</td>
    </tr>
    <tr>
      <td><strong>3. Lập trình Backend &amp; Frontend</strong></td>
      <td>Thiết kế kiến trúc 3 tầng; tự kiểm soát logic quy hoạch tuyến tính <code>MacroOptimizationEngine</code>, JWT Auth và bảo mật.</td>
      <td>Copilot sinh DTOs, AutoMapper, Tailwind CSS; Agent hỗ trợ dựng khung CRUD, <code>CompetitorResearchService</code>, UI React 19.</td>
      <td>Backend <code>.NET 8</code> + Frontend <code>React 19 / TS 6 / Vite 8 / Zustand 5</code> biên dịch sạch.</td>
    </tr>
    <tr>
      <td><strong>4. Kiểm thử &amp; Bảo mật</strong></td>
      <td>Xác định ca biên (hạn dùng, <code>OPTIMAL</code>/<code>INFEASIBLE</code>, lỗi native OR-Tools, SSRF); chạy test và tự sửa lỗ hổng CVE.</td>
      <td>Hỗ trợ sinh khung test xUnit + SQLite In-Memory + FluentAssertions + Moq; gợi ý kịch bản test tích hợp <code>WebApplicationFactory</code>.</td>
      <td><strong>201/201 tests</strong> đạt; ghim phiên bản an toàn các gói transitive CVE trong <code>.csproj</code>.</td>
    </tr>
    <tr>
      <td><strong>5. Báo cáo &amp; Bảo vệ</strong></td>
      <td>Đối chiếu số liệu thực tế từ <code>PROJECT_STATUS.md</code> và git history; nắm vững giải thích toán học GLOP để phản biện.</td>
      <td>Chuẩn hóa văn phong học thuật, kiểm tra lỗi chính tả, xuất báo cáo Markdown/HTML sang PDF chuẩn A4.</td>
      <td>Báo cáo Chương 3, <code>KE_HOACH_SU_DUNG_AI_SMARTMACRO.pdf</code>.</td>
    </tr>
  </tbody>
</table>

<h2>MỤC 3: ĐÁNH GIÁ NĂNG LỰC, ĐIỂM MẠNH VÀ HẠN CHẾ CỦA TỪNG CÔNG CỤ AI</h2>
<table class="data-table">
  <thead>
    <tr>
      <th style="width:18%;">Công cụ AI</th>
      <th style="width:27%;">Điểm mạnh thực tế</th>
      <th style="width:28%;">Hạn chế &amp; Rủi ro gặp phải</th>
      <th style="width:27%;">Biện pháp khắc phục của Sinh viên</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>AI Coding Agent</strong><br/>(Antigravity / Claude Code)</td>
      <td>Hiểu tốt liên kết đa tệp (<code>Controller</code> → <code>Service</code> → <code>Engine</code>); chạy chuỗi lệnh build/test liên hoàn và gỡ lỗi nhanh.</td>
      <td>Dễ <em>over-engineering</em> (làm phức tạp hóa kiến trúc vượt phạm vi đồ án) hoặc ảo giác tên model/thư viện chưa tồn tại.</td>
      <td>Giới hạn phạm vi rõ trong prompt; không cho tự ý đổi kiến trúc; đối chiếu tên gói/model với tài liệu chính thức.</td>
    </tr>
    <tr>
      <td><strong>GitHub Copilot</strong></td>
      <td>Phản hồi tức thì theo dòng code; rất hiệu quả cho DTO, Validation, AutoMapper và class Tailwind CSS.</td>
      <td>Ngữ cảnh hẹp quanh file đang mở; hay gợi ý sai nghiệp vụ đặc thù (nhầm đơn vị 100g dinh dưỡng với tổng gram tồn kho).</td>
      <td>Chỉ dùng cho mã lặp lại; luôn tự kiểm tra từng biểu thức tính Macro và ràng buộc <code>UserFoodInventories</code>.</td>
    </tr>
    <tr>
      <td><strong>Gemini / ChatGPT</strong></td>
      <td>Mạnh về tổng hợp thông tin, so sánh API dinh dưỡng và rà soát tính mạch lạc của văn bản học thuật.</td>
      <td>Không tự thấy trạng thái hiện tại của repo nên dễ trả lời chung chung hoặc lệch tên hàm thực tế.</td>
      <td>Đính kèm <code>docs/status/PROJECT_STATUS.md</code> và trích đoạn mã nguồn thật trước khi hỏi.</td>
    </tr>
    <tr>
      <td><strong>Claude API</strong><br/>(trong sản phẩm)</td>
      <td>Phân tích và tóm tắt cấu trúc trang đối thủ linh hoạt khi nhận dữ liệu DOM từ Playwright.</td>
      <td>Tốn chi phí token, tiềm ẩn rủi ro <strong>Prompt Injection</strong> từ HTML lạ hoặc <strong>SSRF</strong> nếu URL trỏ vào mạng nội bộ.</td>
      <td>Chặn SSRF qua <code>TargetUrlValidator</code>, bọc dữ liệu bằng thẻ <code>&lt;competitor_page&gt;</code> và cache SHA256.</td>
    </tr>
  </tbody>
</table>

<h2>MỤC 4: PHƯƠNG PHÁP QUẢN LÝ NGỮ CẢNH &amp; KỸ THUẬT ĐẶT CÂU LỆNH</h2>
<p>Để đầu ra của AI bám sát thực tế mã nguồn và quy chuẩn Khoa CNTT (STU), sinh viên áp dụng 3 nguyên tắc quản lý ngữ cảnh và công thức <strong>Prompt 4 phần</strong> (<em>Role – Context – Task &amp; Constraints – Output Format</em>):</p>
<ul>
  <li><strong>Bộ nhớ trạng thái bằng <code>docs/status/PROJECT_STATUS.md</code>:</strong> Cập nhật định kỳ commit mới nhất, kết quả 201/201 test và danh sách lỗ hổng mở để AI Agent không bị mất ngữ cảnh giữa các phiên làm việc.</li>
  <li><strong>Đính kèm quy chuẩn Khoa CNTT (STU):</strong> Cung cấp rõ ràng quy cách lề A4, ký hiệu UML chuẩn và cấu trúc 9 bảng CSDL thực tế trước khi sinh sơ đồ hoặc báo cáo.</li>
</ul>

<h3>Ví dụ Prompt 1 — Sinh Integration Test xử lý lỗi native Solver OR-Tools</h3>
<div class="prompt-box">[Role]: Bạn là Senior .NET Backend Engineer chuyên về xUnit và ASP.NET Core Integration Testing.
[Context]: SmartMacro.Api (.NET 8) dùng Google.OrTools (GLOP) trong MacroOptimizationEngine.cs. Khi native C++ runtime bị lỗi (DllNotFoundException), hệ thống phải ném SolverUnavailableException và trả HTTP 503 qua GlobalExceptionHandler thay vì trả HTTP 200 INFEASIBLE giả.
[Task &amp; Constraints]: Viết Integration Test trong SmartMacro.Tests dùng WebApplicationFactory + SQLite In-Memory kiểm chứng POST /api/optimizations trả mã 503 khi IMacroOptimizationEngine ném SolverUnavailableException. Không sửa logic nghiệp vụ Engine.
[Output Format]: Mã C# hoàn chỉnh theo chuẩn FluentAssertions và Moq trong SmartMacro.Tests.csproj.</div>

<h3>Ví dụ Prompt 2 — Rà soát bảo mật module CompetitorResearchService</h3>
<div class="prompt-box">[Role]: Bạn là Application Security Reviewer cho ứng dụng .NET 8 tích hợp LLM.
[Context]: CompetitorResearchService.cs dùng Microsoft.Playwright tải trang từ URL người dùng nhập và gửi văn bản cho Anthropic Claude API phân tích.
[Task &amp; Constraints]: Kiểm tra 2 rủi ro: (1) SSRF nếu URL trỏ vào localhost/IP nội bộ; (2) Prompt Injection ẩn trong HTML trang đối thủ. Đề xuất lớp kiểm tra URL và cách cô lập dữ liệu trước khi gọi IClaudeService.
[Output Format]: Liệt kê lỗ hổng kèm giải pháp code C# ngắn gọn, dễ viết Unit Test.</div>

<h2>MỤC 5: QUY TRÌNH LÀM VIỆC KHÉP KÍN VỚI AI (HUMAN-IN-THE-LOOP)</h2>
<p>Mọi dòng mã và tài liệu trước khi đưa vào nhánh chính đều phải đi qua quy trình kiểm soát 5 bước khép kín sau:</p>
<div class="diagram-box">
  {WORKFLOW_SVG}
  <div class="diagram-caption">Hình 1: Quy trình làm việc khép kín 5 bước (Human-in-the-loop) áp dụng trên SmartMacro Engine.</div>
</div>

<h2>MỤC 6: QUY TRÌNH KIỂM CHỨNG, GỠ LỖI &amp; ĐẢM BẢO AN TOÀN BẢO MẬT</h2>
<h3>6.1. Bốn lớp kiểm chứng kỹ thuật bắt buộc</h3>
<ul>
  <li><strong>Kiểm thử Backend (.NET 8):</strong> Thực thi <code>dotnet build</code> và <code>dotnet test</code> trên <code>SmartMacro.Tests</code> (<code>xunit</code> <code>2.5.3</code>, <code>Microsoft.AspNetCore.Mvc.Testing</code> <code>8.0.10</code>, <code>Microsoft.EntityFrameworkCore.Sqlite</code> <code>8.0.10</code>, <code>FluentAssertions</code> <code>8.10.0</code>, <code>Moq</code> <code>4.20.72</code>), bảo đảm <strong>201/201 tests</strong> vượt qua và giữ <strong>0 TODO/FIXME</strong>.</li>
  <li><strong>Kiểm tra tĩnh Frontend (React 19 + TS 6):</strong> Chạy <code>npx tsc -b --noEmit</code> kiểm tra kiểu nghiêm ngặt và <code>npm run lint</code> (<code>oxlint</code> <code>^1.75.0</code>) trước khi đóng gói bằng Vite 8.</li>
  <li><strong>Quản lý bí mật &amp; rà soát lỗ hổng thư viện:</strong> Tách API Key qua <code>.NET User Secrets</code> / <code>.env</code>; chạy định kỳ <code>npm audit</code> (ghi nhận 5 cảnh báo HIGH trên chuỗi <code>axios</code>/<code>vite</code>/<code>zod</code>/<code>follow-redirects</code>/<code>source-map-js</code> để theo dõi nâng cấp) và <code>dotnet list package --vulnerable --include-transitive</code>. Các gói transitive chứa CVE (như <code>System.Formats.Asn1</code> <code>5.0.0</code>) đã được ghim phiên bản an toàn trong <code>.csproj</code> (<code>System.Formats.Asn1</code> <code>8.0.1</code>, <code>System.Net.Http</code> <code>4.3.4</code>, <code>System.Text.RegularExpressions</code> <code>4.3.1</code>).</li>
  <li><strong>Bảo mật module AI tích hợp:</strong> <code>TargetUrlValidator.ValidateAsync</code> ép buộc giao thức <code>HTTPS</code>, kiểm tra allowlist <code>AllowedHosts</code>, phân giải DNS và chặn IP nội bộ qua <code>IsDisallowedIpAddress</code> (chống SSRF); <code>CompetitorResearchService</code> bọc nội dung trang trong thẻ <code>&lt;competitor_page&gt;</code> kèm system prompt chống Prompt Injection và cache bằng SHA256.</li>
</ul>

<h3>6.2. Hai tình huống thực tế sinh viên phát hiện &amp; sửa lỗi của AI (Case Studies)</h3>
<div class="callout-warn">
  <strong>Case Study 1 — Phát hiện AI "ảo giác" tên Claude Model trong <code>AnthropicOptions.cs</code>:</strong> Khi sinh file <code>SmartMacro.Api/Options/AnthropicOptions.cs</code>, AI tự điền giá trị mặc định <code>Model = "claude-sonnet-5-5"</code> — một định danh chưa tồn tại trên API của Anthropic. Sinh viên đã phát hiện trong bước rà soát cấu hình (ghi nhận tại <code>PROJECT_STATUS.md</code>), đối chiếu tài liệu chính thức và sửa lại chính xác thành <code>"claude-3-5-sonnet-20241022"</code> (<code>MaxTokens = 4096</code>, <code>TimeoutSeconds = 90</code>).
</div>
<div class="callout-warn">
  <strong>Case Study 2 — Cắt giảm tình trạng Over-engineering phân quyền:</strong> AI ban đầu đề xuất mô hình 4 vai trò (<code>SuperAdmin</code>, <code>Admin</code>, <code>Nutritionist</code>, <code>User</code>) kèm bảng RBAC nhiều-nhiều gây phình CSDL. Sinh viên đã chủ động cắt bỏ 2 vai trò dư thừa, chuẩn hóa hệ thống về đúng <strong>2 vai trò thực chất là <code>Admin</code> và <code>User</code></strong> phù hợp quy mô đồ án Khoa CNTT (STU).
</div>

<h2>MỤC 7: ĐÁNH GIÁ HIỆU QUẢ ĐỊNH LƯỢNG &amp; ĐỊNH TÍNH</h2>
<table class="data-table">
  <thead>
    <tr>
      <th style="width:24%;">Tiêu chí đánh giá</th>
      <th style="width:38%;">Giá trị thực tế ghi nhận trên dự án</th>
      <th style="width:38%;">Ý nghĩa đối với sinh viên năm 4</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Tốc độ dựng nền tảng</strong></td>
      <td>Hoàn thiện nhanh bộ khung 3 tầng, 9 bảng dữ liệu EF Core 8 và giao diện React 19 / Tailwind CSS 4.</td>
      <td>Dồn được thời gian chuyên sâu vào bài toán quy hoạch tuyến tính OR-Tools và xử lý nghiệp vụ dinh dưỡng.</td>
    </tr>
    <tr>
      <td><strong>Độ phủ kiểm thử tự động</strong></td>
      <td>Đạt <strong>201/201 unit &amp; integration tests</strong> (xUnit + SQLite In-Memory), chạy tự động qua <code>.github/workflows/dotnet-ci.yml</code>.</td>
      <td>Tạo lưới an toàn vững chắc khi tái cấu trúc mã nguồn, hạn chế tối đa lỗi hồi quy (<em>regression</em>).</td>
    </tr>
    <tr>
      <td><strong>Chất lượng &amp; đồng bộ</strong></td>
      <td><strong>0 TODO/FIXME</strong> tồn đọng; bộ 11 sơ đồ Chương 3 khớp 100% tên lớp, tên bảng và chữ ký hàm thực tế.</td>
      <td>Đảm bảo tính nhất quán tuyệt đối giữa mã nguồn chạy thật và tài liệu luận văn nộp Hội đồng.</td>
    </tr>
    <tr>
      <td><strong>Làm chủ công nghệ</strong></td>
      <td>Tự phát hiện lỗi native OR-Tools, lỗi ảo giác model AI và tự xử lý bảo mật SSRF/CVE.</td>
      <td>Khẳng định tư duy kỹ sư phần mềm: AI là đòn bẩy, sinh viên là người kiểm soát chất lượng cuối cùng.</td>
    </tr>
  </tbody>
</table>

<h2>MỤC 8: VÍ DỤ MINH HỌA THỰC TẾ TỪ ĐẦU ĐẾN CUỐI (END-TO-END WALKTHROUGH)</h2>
<p>Minh họa quy trình <strong>Human-in-the-loop</strong> trọn vẹn trên luồng <strong>Tối ưu hóa khẩu phần ăn thông minh</strong> (<code>OptimizationsController</code> → <code>OptimizationService</code> → <code>MacroOptimizationEngine</code> dùng bộ giải <strong>Google OR-Tools GLOP</strong>):</p>
<ol>
  <li><strong>Thiết kế toán học &amp; đặt Prompt:</strong> Sinh viên xác định biến quyết định là số gram <code>x_i</code> của từng món trong <code>UserFoodInventories</code> (<code>0 ≤ x_i ≤ StockGrams_i</code>), ràng buộc Calories/Protein/Carbs/Fat theo <code>DailyTargets</code> với biên độ sai số <code>Tolerance = 0.05</code> (±5%) và ngưỡng lọc món nhỏ <code>MinGramsThreshold = 0.5</code>g, sử dụng <code>Solver.CreateSolver("GLOP")</code> (<code>Google.OrTools</code> <code>9.15.6755</code>).</li>
  <li><strong>Phát hiện lỗi ngụy trang trạng thái (Error Masking Bug):</strong> Khi kiểm tra mã xử lý ngoại lệ trong <code>MacroOptimizationEngine.cs</code>, sinh viên nhận ra nếu thư viện native C++ của OR-Tools lỗi tải (ném <code>DllNotFoundException</code>, <code>TypeInitializationException</code>, <code>BadImageFormatException</code> hoặc trả <code>null</code>), cách bắt lỗi chung trước đó sẽ trả về <strong>HTTP 200 OK kèm trạng thái giả <code>INFEASIBLE</code></strong> — làm người dùng tưởng tủ lạnh thiếu đồ ăn trong khi thực chất bộ giải đang sập.</li>
  <li><strong>Chỉ đạo sửa lỗi kiến trúc &amp; khóa chặt bằng Integration Test (Commit <code>0636fb2</code>):</strong> Sinh viên thiết kế lại luồng ngoại lệ trên <strong>5 tệp</strong>: tạo <code>SmartMacro.Api/Exceptions/SolverUnavailableException.cs</code>; cập nhật <code>MacroOptimizationEngine.cs</code> bắt đích danh các lỗi native để ném <code>SolverUnavailableException</code>; ánh xạ sang <strong>HTTP 503 Service Unavailable</strong> trong <code>GlobalExceptionHandler.cs</code>; bổ sung 144 dòng test trong <code>OptimizationServiceTests.cs</code> và <code>OptimizationErrorHandlingIntegrationTests.cs</code>. Toàn bộ <strong>201/201 tests</strong> đều vượt qua sau khi sửa.</li>
</ol>

<h2>KẾT LUẬN</h2>
<p>Việc kết hợp có kỷ luật 4 nhóm công cụ AI cùng quy trình kiểm soát <strong>Human-in-the-loop 5 bước</strong> giúp dự án <em>SmartMacro Engine</em> tối ưu hóa tốc độ phát triển mà vẫn bảo đảm chuẩn mực kỹ thuật (201/201 test đạt, kiến trúc 3 tầng mạch lạc, kiểm soát chặt chẽ SSRF, Prompt Injection và CVE). Sinh viên hoàn toàn làm chủ hệ thống, sẵn sàng giải trình và bảo vệ toàn bộ đề tài trước Hội đồng Khoa Công nghệ Thông tin — Trường Đại học Công nghệ Sài Gòn (STU).</p>

</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"Wrote HTML: {HTML_PATH}")
subprocess.run(["node", CDP_SCRIPT, HTML_PATH, PDF_PATH], check=True)
print(f"Generated PDF: {PDF_PATH} ({os.path.getsize(PDF_PATH)} bytes)")
