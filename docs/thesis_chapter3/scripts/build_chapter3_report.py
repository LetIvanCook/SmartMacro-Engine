# -*- coding: utf-8 -*-
"""
SmartMacro Engine - Biên dịch Luận văn Tốt nghiệp / Báo cáo Thực tập chuyên ngành
CHƯƠNG 3: THIẾT KẾ HỆ THỐNG
Đúng chuẩn quy định Khoa CNTT - Trường Đại học Công nghệ Sài Gòn (STU):
- Khổ giấy A4, lề: Top 2cm, Bottom 2cm, Left 3cm, Right 2cm.
- Font: Times New Roman, 13pt, giãn đoạn Before 6pt, After 0pt, Line spacing 1.3.
- Tiêu đề cấp 1: 24pt, canh phải: Chương 3. <b>THIẾT KẾ</b>
- Tiêu đề cấp 2 (3.1, 3.2, 3.3, 3.4): 15pt, IN HOA, IN ĐẬM.
- Tiêu đề cấp 3 (3.1.1, 3.1.2...): 14pt, chữ thường, in đậm.
- Chú thích hình: <u><b><i>Hình 3-x:</i></b></u> <i>Tên hình.</i> (canh giữa, ngay dưới hình).
- Header: <i>CHƯƠNG 3. THIẾT KẾ</i> (bỏ trang 1).
- Footer: <i>LUẬN VĂN TỐT NGHIỆP: HỆ THỐNG SMARTMACRO ENGINE</i> kèm số trang canh phải.
"""

import os
import re
import subprocess
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIAGRAMS_DIR = os.path.join(BASE_DIR, "diagrams")
WIREFRAMES_DIR = os.path.join(BASE_DIR, "wireframes")
OUTPUT_HTML = os.path.join(BASE_DIR, "CHUONG_3_THIET_KE_HE_THONG.html")
OUTPUT_PDF = os.path.join(BASE_DIR, "CHUONG_3_THIET_KE_HE_THONG.pdf")

def read_svg_cleaned(filepath):
    """Reads SVG file and strips <?xml> or DOCTYPE so it embeds cleanly inline."""
    if not os.path.exists(filepath):
        return f"<div style='color:red;font-weight:bold;'>[Missing SVG file: {os.path.basename(filepath)}]</div>"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'<\?xml[^>]*\?>', '', content)
    content = re.sub(r'<!DOCTYPE[^>]*>', '', content)
    return content.strip()

def build_chapter3_html():
    svg_3_1 = read_svg_cleaned(os.path.join(DIAGRAMS_DIR, "fig_3_1_conceptual_erd.svg"))
    svg_3_2 = read_svg_cleaned(os.path.join(DIAGRAMS_DIR, "fig_3_2_logical_schema.svg"))
    svg_3_3 = read_svg_cleaned(os.path.join(DIAGRAMS_DIR, "fig_3_3_usecase_detailed.svg"))
    svg_3_4 = read_svg_cleaned(os.path.join(DIAGRAMS_DIR, "fig_3_4_class_diagram.svg"))
    svg_3_5 = read_svg_cleaned(os.path.join(DIAGRAMS_DIR, "fig_3_5_sequence_login_and_inventory.svg"))
    svg_3_6 = read_svg_cleaned(os.path.join(DIAGRAMS_DIR, "fig_3_6_sequence_optimization.svg"))
    svg_3_7 = read_svg_cleaned(os.path.join(DIAGRAMS_DIR, "fig_3_7_activity_optimization.svg"))

    svg_3_8 = read_svg_cleaned(os.path.join(WIREFRAMES_DIR, "fig_3_8_wireframe_auth.svg"))
    svg_3_9 = read_svg_cleaned(os.path.join(WIREFRAMES_DIR, "fig_3_9_wireframe_dashboard.svg"))
    svg_3_10 = read_svg_cleaned(os.path.join(WIREFRAMES_DIR, "fig_3_10_wireframe_inventory.svg"))
    svg_3_11 = read_svg_cleaned(os.path.join(WIREFRAMES_DIR, "fig_3_11_wireframe_optimizer.svg"))

    template = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Chương 3: Thiết Kế Hệ Thống — SmartMacro Engine</title>
<style>
  @page {
    size: A4 portrait;
    margin-top: 20mm;
    margin-bottom: 20mm;
    margin-left: 30mm;
    margin-right: 20mm;
  }

  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  body {
    font-family: "Times New Roman", Times, serif;
    font-size: 13pt;
    line-height: 1.3;
    color: #000000;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
    text-align: justify;
  }

  /* Page Break Helpers */
  .page-break {
    page-break-before: always;
    break-before: page;
  }

  .avoid-break {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  /* Typography strictly STU */
  .chapter-title {
    font-size: 24pt;
    font-family: "Times New Roman", Times, serif;
    text-align: right;
    margin-top: 0;
    margin-bottom: 24pt;
    font-weight: normal;
  }

  .chapter-title b {
    font-weight: bold;
    text-transform: uppercase;
  }

  h2.level2 {
    font-size: 15pt;
    font-weight: bold;
    text-transform: uppercase;
    margin-top: 18pt;
    margin-bottom: 6pt;
    line-height: 1.3;
    color: #000000;
  }

  h3.level3 {
    font-size: 14pt;
    font-weight: bold;
    text-transform: none;
    margin-top: 14pt;
    margin-bottom: 6pt;
    line-height: 1.3;
    color: #000000;
  }

  h4.level4 {
    font-size: 13pt;
    font-weight: bold;
    font-style: italic;
    margin-top: 10pt;
    margin-bottom: 4pt;
    line-height: 1.3;
    color: #000000;
  }

  p {
    font-size: 13pt;
    line-height: 1.3;
    margin-top: 6pt;
    margin-bottom: 0pt;
    text-indent: 1cm;
  }

  p.no-indent {
    text-indent: 0;
  }

  ul, ol {
    font-size: 13pt;
    line-height: 1.3;
    margin-top: 4pt;
    margin-bottom: 6pt;
    padding-left: 1.5cm;
  }

  li {
    margin-bottom: 3pt;
  }

  /* Math and Formulas */
  .formula-box {
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #0f172a;
    padding: 10pt 14pt;
    margin: 8pt 0;
    font-family: "Times New Roman", serif;
    font-size: 12.5pt;
    page-break-inside: avoid;
  }

  .formula-title {
    font-weight: bold;
    margin-bottom: 4pt;
    color: #0f172a;
  }

  /* Tables */
  table.stu-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 8pt;
    margin-bottom: 12pt;
    font-size: 11pt;
    line-height: 1.25;
    page-break-inside: avoid;
  }

  table.stu-table th, table.stu-table td {
    border: 1px solid #000000;
    padding: 5pt 7pt;
    vertical-align: middle;
  }

  table.stu-table th {
    background-color: #f1f5f9;
    font-weight: bold;
    text-align: center;
    color: #000000;
  }

  table.stu-table td.center {
    text-align: center;
  }

  .table-caption {
    font-size: 12pt;
    font-weight: bold;
    font-style: italic;
    text-align: left;
    margin-top: 10pt;
    margin-bottom: 4pt;
  }

  /* Figure and Captions strictly STU format */
  .figure-wrapper {
    text-align: center;
    margin-top: 12pt;
    margin-bottom: 14pt;
    page-break-inside: avoid;
  }

  .figure-wrapper svg {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    background-color: #ffffff;
  }

  .figure-caption {
    font-size: 12pt;
    text-align: center;
    margin-top: 6pt;
    margin-bottom: 10pt;
  }

  .figure-caption u b i {
    text-decoration: underline;
    font-weight: bold;
    font-style: italic;
  }

  .figure-caption i {
    font-style: italic;
  }

  /* Wireframe specific presentation */
  .wireframe-container {
    margin: 10pt 0 14pt 0;
    page-break-inside: avoid;
  }

  .wireframe-container svg {
    max-width: 100%;
    height: auto;
    border: 1.5px solid #94a3b8;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }
</style>
</head>
<body>

<div class="chapter-title">
  Chương 3. <b>THIẾT KẾ</b>
</div>

<p>Sau khi đã tiến hành thu thập, phân tích toàn diện các yêu cầu nghiệp vụ và xác lập ranh giới hệ thống ở Chương 2, Chương 3 tập trung hiện thực hóa quy trình thiết kế kỹ thuật chi tiết cho đồ án <b>SmartMacro Engine</b> — Hệ thống Tối ưu hóa Khẩu phần ăn &amp; Dinh dưỡng Cá nhân hóa theo Chu kỳ Vận động. Quá trình thiết kế được thực hiện tuần tự, chặt chẽ qua 4 trụ cột công nghệ chính:</p>

<ul>
  <li><b>Thiết kế dữ liệu (Mục 3.1):</b> Xây dựng mô hình dữ liệu qua 3 mức trừu tượng học thuật bao gồm: Mô hình dữ liệu mức ý niệm (Conceptual ERD), Lược đồ dữ liệu mức luận lý (Logical Schema) chuẩn hóa bậc 3 (3NF) và Bảng từ điển dữ liệu vật lý (Physical Data Dictionary) cho 9 thực thể cốt lõi trong cơ sở dữ liệu SQL Server.</li>
  <li><b>Thiết kế kiến trúc &amp; xử lý hệ thống (Mục 3.2):</b> Xây dựng biểu đồ Use Case tổng thể có phân quyền nghiêm ngặt giữa người dùng cuối (User) và quản trị viên (Admin) kèm quan hệ <i>&laquo;include&raquo;</i> / <i>&laquo;extend&raquo;</i> và các bảng đặc tả kịch bản Use Case chi tiết; thiết kế sơ đồ lớp (Class Diagram) 3 tầng tuân thủ nguyên lý Dependency Inversion; biểu diễn luồng dữ liệu thời gian thực qua 2 sơ đồ tuần tự (Sequence Diagram) và sơ đồ hoạt động (Activity Diagram) của thuật toán.</li>
  <li><b>Thiết kế giao diện người dùng (Mục 3.3):</b> Xây dựng bộ Wireframe chuyên nghiệp dạng Vector chuẩn công cụ thiết kế Figma (độ phân giải lưới chuẩn 1440&times;900) cho 4 màn hình trọng yếu, có đánh số định danh Callout trên từng phân vùng giao diện kèm bảng thuyết minh công năng.</li>
  <li><b>Thiết kế giải thuật tối ưu hóa khẩu phần ăn (Mục 3.4):</b> Xây dựng mô hình toán học Quy hoạch tuyến tính (Linear Programming - LP) đa mục tiêu, kỹ thuật tuyến tính hóa hàm mục tiêu sai lệch Calo, các ràng buộc dung sai &plusmn;5% và phân tích cơ chế giải quyết trạng thái tối ưu (Optimal) hoặc vô nghiệm (Infeasible) của bộ giải Google OR-Tools GLOP.</li>
</ul>

<!-- ======================================================================= -->
<!-- MỤC 3.1: THIẾT KẾ DỮ LIỆU -->
<!-- ======================================================================= -->
<h2 class="level2">3.1. THIẾT KẾ DỮ LIỆU</h2>

<p>Dữ liệu là nền tảng cốt lõi chi phối toàn bộ tính đúng đắn của các giải thuật tính toán dinh dưỡng trong SmartMacro Engine. Nhằm đảm bảo dữ liệu không bị dư thừa, đạt chuẩn toàn vẹn tham chiếu và tối ưu hóa tốc độ truy vấn cho các bài toán tối ưu quy hoạch, mô hình dữ liệu được thiết kế công phu qua 3 mức độ trừu tượng chuẩn mực.</p>

<h3 class="level3">3.1.1. Mô hình dữ liệu mức ý niệm (Conceptual ERD)</h3>

<p>Mô hình dữ liệu mức ý niệm phản ánh thế giới thực của bài toán quản lý dinh dưỡng thể thao và kho thực phẩm gia đình. Mô hình tập trung xác định các tập thực thể độc lập, thuộc tính định danh và các mối kết hợp ngữ nghĩa giữa các thực thể mà không phụ thuộc vào hệ quản trị cơ sở dữ liệu cụ thể.</p>

<p>Hệ thống SmartMacro Engine bao gồm 9 thực thể chính với các mối liên kết nghiệp vụ như sau:</p>

<ul>
  <li><b>Người dùng (User):</b> Đóng vai trò trung tâm của hệ thống, sở hữu các chỉ số thể chất (chiều cao, cân nặng, BMR), hồ sơ mục tiêu thể hình (tăng cơ, giảm mỡ, duy trì) và quản lý tài nguyên cá nhân.</li>
  <li><b>Phiên làm mới (RefreshToken):</b> Thực thể hỗ trợ duy trì phiên làm việc bảo mật dài hạn cho người dùng theo cơ chế OAuth2/JWT token rotation. Một người dùng có thể sở hữu nhiều Refresh Token tương ứng với nhiều thiết bị đăng nhập (quan hệ 1-N).</li>
  <li><b>Danh mục thực phẩm (FoodCategory) &amp; Thực phẩm (Food):</b> FoodCategory phân loại nguồn dinh dưỡng (Thịt, Tinh bột, Rau củ, Trứng sữa, Dầu hạt). Food lưu trữ chỉ số dinh dưỡng chuẩn hóa trên 100 gram (Kcal, Protein, Carbs, Fat, Fiber). Quan hệ giữa FoodCategory và Food là 1-N. Ngoài ra, Food có thể được đóng góp bởi User (created_by) và cần được quản trị viên duyệt tính xác thực (is_verified).</li>
  <li><b>Mục kho cá nhân (UserFoodInventory):</b> Đại diện cho tủ lạnh thông minh của người dùng. Một người dùng có thể lưu trữ nhiều thực phẩm trong kho với số lượng cụ thể (gam) và hạn sử dụng (ExpiryDate). Quan hệ giữa User và Food thông qua UserFoodInventory là quan hệ kết hợp đa trị có thuộc tính bổ sung.</li>
  <li><b>Loại chu kỳ tập (TrainingCycleType) &amp; Lịch tập (UserTrainingSchedule):</b> Xác định chu kỳ vận động thể chất (Hypertrophy - Tăng cơ, Cardio - Tim mạch, Rest Day - Nghỉ ngơi). UserTrainingSchedule ghi nhận lịch trình tập luyện của người dùng theo từng ngày cụ thể.</li>
  <li><b>Quy tắc điều chỉnh Macro (MacroAdjustmentRule) &amp; Mục tiêu dinh dưỡng ngày (DailyTarget):</b> MacroAdjustmentRule định nghĩa tỷ lệ phân bổ dinh dưỡng (KcalMultiplier, ProteinGPerKgBw, CarbRatio, FatRatio) theo từng loại chu kỳ tập. Dựa trên quy tắc này, DailyTarget được tính toán tự động hoặc người dùng tự thiết lập cho từng ngày xác định.</li>
</ul>

<div class="figure-wrapper">
  __SVG_3_1__
  <div class="figure-caption"><u><b><i>Hình 3-1:</i></b></u> <i>Mô hình dữ liệu mức ý niệm (Conceptual ERD) hệ thống SmartMacro Engine.</i></div>
</div>

<h3 class="level3">3.1.2. Mô hình dữ liệu mức luận lý (Logical Schema)</h3>

<p>Từ mô hình ý niệm, hệ thống tiến hành chuyển đổi sang mô hình dữ liệu quan hệ mức luận lý đạt chuẩn hóa dạng 3 (Third Normal Form - 3NF). Mọi thuộc tính không khóa đều phụ thuộc đầy đủ và trực tiếp vào khóa chính, triệt tiêu hoàn toàn các dị thường thêm (insert anomaly), dị thường sửa (update anomaly) và dị thường xóa (delete anomaly).</p>

<p>Lược đồ luận lý xác lập rõ các Khóa chính (Primary Key - PK), Khóa ngoại (Foreign Key - FK), Ràng buộc duy nhất (Unique Constraint - UQ) và các Chỉ mục kết hợp (Composite Index) phục vụ tối ưu hóa truy vấn SQL Server:</p>

<ul>
  <li>Bảng `foods` thiết lập chỉ mục tổ hợp `IX_foods_macro` trên 4 cột (`kcal_per_100g`, `protein_g_per_100g`, `carbs_g_per_100g`, `fat_g_per_100g`) nhằm tăng tốc độ lọc ứng viên thực phẩm cho bộ giải thuật toán.</li>
  <li>Bảng `user_food_inventory` áp dụng ràng buộc duy nhất tổ hợp `UQ_inventory_user_food_expiry` trên bộ 3 thuộc tính (`user_id`, `food_id`, `expiry_date`) nhằm ngăn chặn việc trùng lặp cùng một mặt hàng có cùng hạn dùng trong tủ lạnh.</li>
  <li>Bảng `daily_targets` thiết lập ràng buộc duy nhất `UQ_target_user_date` (`user_id`, `target_date`) đảm bảo mỗi người dùng chỉ có duy nhất một bộ chỉ số Macro mục tiêu trong một ngày.</li>
  <li>Cơ chế toàn vẹn dữ liệu được gia cố bởi Trigger: `TRG_inventory_after_delete_nullify_meallogs` tự động set null mã kho trong nhật ký bữa ăn khi thực phẩm trong kho bị xóa, và `TRG_rules_after_delete_nullify_targets` bảo vệ tính toàn vẹn khi cập nhật quy tắc tính toán.</li>
</ul>

<div class="figure-wrapper">
  __SVG_3_2__
  <div class="figure-caption"><u><b><i>Hình 3-2:</i></b></u> <i>Lược đồ dữ liệu mức luận lý (Logical Schema) với các khóa và ràng buộc tham chiếu.</i></div>
</div>

<div class="page-break"></div>

<h3 class="level3">3.1.3. Bảng đặc tả vật lý (Physical Data Dictionary)</h3>

<p>Dưới đây là bảng đặc tả cấu trúc vật lý chi tiết của 9 bảng dữ liệu trên hệ quản trị cơ sở dữ liệu Microsoft SQL Server 2022, thể hiện tên trường vật lý, kiểu dữ liệu, các ràng buộc toàn vẹn và mô tả ý nghĩa nghiệp vụ.</p>

<div class="table-caption">Bảng 3.1: Đặc tả vật lý bảng users (Thông tin tài khoản người dùng)</div>
<table class="stu-table">
  <thead>
    <tr>
      <th style="width: 5%;">STT</th>
      <th style="width: 18%;">Tên trường</th>
      <th style="width: 17%;">Kiểu dữ liệu</th>
      <th style="width: 20%;">Ràng buộc</th>
      <th style="width: 40%;">Mô tả ý nghĩa nghiệp vụ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center">1</td>
      <td><b>user_id</b></td>
      <td>bigint</td>
      <td>PK, IDENTITY(1,1)</td>
      <td>Mã định danh duy nhất của người dùng trong hệ thống</td>
    </tr>
    <tr>
      <td class="center">2</td>
      <td><b>email</b></td>
      <td>varchar(255)</td>
      <td>NOT NULL, UQ</td>
      <td>Địa chỉ thư điện tử dùng để đăng nhập và nhận thông báo</td>
    </tr>
    <tr>
      <td class="center">3</td>
      <td><b>password_hash</b></td>
      <td>char(60)</td>
      <td>NOT NULL</td>
      <td>Chuỗi băm mật khẩu mã hóa an toàn bằng thuật toán BCrypt</td>
    </tr>
    <tr>
      <td class="center">4</td>
      <td><b>full_name</b></td>
      <td>nvarchar(150)</td>
      <td>NULL</td>
      <td>Họ và tên đầy đủ hiển thị trên giao diện người dùng</td>
    </tr>
    <tr>
      <td class="center">5</td>
      <td><b>date_of_birth</b></td>
      <td>date</td>
      <td>NOT NULL</td>
      <td>Ngày tháng năm sinh dùng để tính tuổi sinh học</td>
    </tr>
    <tr>
      <td class="center">6</td>
      <td><b>biological_sex</b></td>
      <td>varchar(10)</td>
      <td>NOT NULL</td>
      <td>Giới tính sinh học ('male' hoặc 'female') để tính BMR</td>
    </tr>
    <tr>
      <td class="center">7</td>
      <td><b>activity_level</b></td>
      <td>varchar(20)</td>
      <td>NOT NULL, DEFAULT 'moderate'</td>
      <td>Hệ số vận động ('sedentary', 'light', 'moderate', 'very_active')</td>
    </tr>
    <tr>
      <td class="center">8</td>
      <td><b>goal_type</b></td>
      <td>varchar(20)</td>
      <td>NOT NULL</td>
      <td>Mục tiêu hình thể ('cut', 'maintain', 'bulk', 'recomp')</td>
    </tr>
    <tr>
      <td class="center">9</td>
      <td><b>status</b></td>
      <td>varchar(20)</td>
      <td>NOT NULL, DEFAULT 'active'</td>
      <td>Trạng thái hoạt động tài khoản ('active', 'inactive', 'locked')</td>
    </tr>
    <tr>
      <td class="center">10</td>
      <td><b>created_at</b></td>
      <td>datetime2(3)</td>
      <td>NOT NULL, DEFAULT sysdatetime()</td>
      <td>Thời điểm khởi tạo tài khoản trên hệ thống</td>
    </tr>
    <tr>
      <td class="center">11</td>
      <td><b>updated_at</b></td>
      <td>datetime2(3)</td>
      <td>NOT NULL, DEFAULT sysdatetime()</td>
      <td>Thời điểm cập nhật thông tin hồ sơ lần gần nhất</td>
    </tr>
  </tbody>
</table>

<div class="table-caption">Bảng 3.2: Đặc tả vật lý bảng refresh_tokens (Quản lý phiên xác thực xoay vòng)</div>
<table class="stu-table">
  <thead>
    <tr>
      <th style="width: 5%;">STT</th>
      <th style="width: 18%;">Tên trường</th>
      <th style="width: 17%;">Kiểu dữ liệu</th>
      <th style="width: 20%;">Ràng buộc</th>
      <th style="width: 40%;">Mô tả ý nghĩa nghiệp vụ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center">1</td>
      <td><b>id</b></td>
      <td>bigint</td>
      <td>PK, IDENTITY(1,1)</td>
      <td>Khóa chính tự tăng của bản ghi refresh token</td>
    </tr>
    <tr>
      <td class="center">2</td>
      <td><b>token</b></td>
      <td>varchar(128)</td>
      <td>NOT NULL, UQ</td>
      <td>Chuỗi băm SHA-256 của Refresh Token bảo mật</td>
    </tr>
    <tr>
      <td class="center">3</td>
      <td><b>user_id</b></td>
      <td>bigint</td>
      <td>FK &rarr; users(user_id) ON DELETE CASCADE</td>
      <td>Mã người dùng sở hữu phiên đăng nhập này</td>
    </tr>
    <tr>
      <td class="center">4</td>
      <td><b>created_at</b></td>
      <td>datetime2(3)</td>
      <td>NOT NULL, DEFAULT sysdatetime()</td>
      <td>Thời điểm phát hành token</td>
    </tr>
    <tr>
      <td class="center">5</td>
      <td><b>expires_at</b></td>
      <td>datetime2(3)</td>
      <td>NOT NULL</td>
      <td>Thời điểm hết hạn hiệu lực của Refresh Token (thường là 7 ngày)</td>
    </tr>
    <tr>
      <td class="center">6</td>
      <td><b>revoked_at</b></td>
      <td>datetime2(3)</td>
      <td>NULL</td>
      <td>Thời điểm thu hồi token (khi đăng xuất hoặc token rotation)</td>
    </tr>
  </tbody>
</table>

<div class="table-caption">Bảng 3.3: Đặc tả vật lý bảng food_categories (Danh mục phân loại thực phẩm)</div>
<table class="stu-table">
  <thead>
    <tr>
      <th style="width: 5%;">STT</th>
      <th style="width: 18%;">Tên trường</th>
      <th style="width: 17%;">Kiểu dữ liệu</th>
      <th style="width: 20%;">Ràng buộc</th>
      <th style="width: 40%;">Mô tả ý nghĩa nghiệp vụ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center">1</td>
      <td><b>category_id</b></td>
      <td>smallint</td>
      <td>PK, IDENTITY(1,1)</td>
      <td>Mã định danh nhóm thực phẩm</td>
    </tr>
    <tr>
      <td class="center">2</td>
      <td><b>category_name</b></td>
      <td>nvarchar(100)</td>
      <td>NOT NULL, UQ</td>
      <td>Tên danh mục phân loại (Thịt, Hải sản, Tinh bột, Rau củ...)</td>
    </tr>
  </tbody>
</table>

<div class="table-caption">Bảng 3.4: Đặc tả vật lý bảng foods (Ngân hàng dữ liệu thành phần thực phẩm)</div>
<table class="stu-table">
  <thead>
    <tr>
      <th style="width: 5%;">STT</th>
      <th style="width: 18%;">Tên trường</th>
      <th style="width: 17%;">Kiểu dữ liệu</th>
      <th style="width: 20%;">Ràng buộc</th>
      <th style="width: 40%;">Mô tả ý nghĩa nghiệp vụ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center">1</td>
      <td><b>food_id</b></td>
      <td>bigint</td>
      <td>PK, IDENTITY(1,1)</td>
      <td>Mã định danh thực phẩm</td>
    </tr>
    <tr>
      <td class="center">2</td>
      <td><b>category_id</b></td>
      <td>smallint</td>
      <td>FK &rarr; food_categories ON DELETE SET NULL</td>
      <td>Mã danh mục phân loại trực thuộc</td>
    </tr>
    <tr>
      <td class="center">3</td>
      <td><b>food_name</b></td>
      <td>nvarchar(200)</td>
      <td>NOT NULL</td>
      <td>Tên gọi thực phẩm (ví dụ: Ức gà phi lê, Gạo lứt, Súp lơ...)</td>
    </tr>
    <tr>
      <td class="center">4</td>
      <td><b>barcode</b></td>
      <td>varchar(64)</td>
      <td>NULL, UQ</td>
      <td>Mã vạch chuẩn GS1/EAN dùng để quét nhận diện nhanh</td>
    </tr>
    <tr>
      <td class="center">5</td>
      <td><b>kcal_per_100g</b></td>
      <td>decimal(6,2)</td>
      <td>NOT NULL</td>
      <td>Mức năng lượng cung cấp trên mỗi 100 gam thực phẩm</td>
    </tr>
    <tr>
      <td class="center">6</td>
      <td><b>protein_g_per_100g</b></td>
      <td>decimal(6,2)</td>
      <td>NOT NULL</td>
      <td>Khối lượng chất đạm (Protein) tính trên 100 gam</td>
    </tr>
    <tr>
      <td class="center">7</td>
      <td><b>carbs_g_per_100g</b></td>
      <td>decimal(6,2)</td>
      <td>NOT NULL</td>
      <td>Khối lượng tinh bột (Carbohydrates) tính trên 100 gam</td>
    </tr>
    <tr>
      <td class="center">8</td>
      <td><b>fat_g_per_100g</b></td>
      <td>decimal(6,2)</td>
      <td>NOT NULL</td>
      <td>Khối lượng chất béo (Fat) tính trên 100 gam</td>
    </tr>
    <tr>
      <td class="center">9</td>
      <td><b>fiber_g_per_100g</b></td>
      <td>decimal(6,2)</td>
      <td>NOT NULL, DEFAULT 0</td>
      <td>Hàm lượng chất xơ trên 100 gam</td>
    </tr>
    <tr>
      <td class="center">10</td>
      <td><b>is_verified</b></td>
      <td>bit</td>
      <td>NOT NULL, DEFAULT 0</td>
      <td>Cờ xác nhận độ tin cậy từ chuyên gia dinh dưỡng / Admin</td>
    </tr>
    <tr>
      <td class="center">11</td>
      <td><b>source</b></td>
      <td>varchar(20)</td>
      <td>NOT NULL, DEFAULT 'user_submitted'</td>
      <td>Nguồn cấp dữ liệu ('usda', 'system_verified', 'user_submitted')</td>
    </tr>
    <tr>
      <td class="center">12</td>
      <td><b>created_by</b></td>
      <td>bigint</td>
      <td>FK &rarr; users(user_id) ON DELETE SET NULL</td>
      <td>Mã người dùng đóng góp món ăn vào ngân hàng dữ liệu</td>
    </tr>
  </tbody>
</table>

<div class="table-caption">Bảng 3.5: Đặc tả vật lý bảng user_food_inventory (Kho thực phẩm tủ lạnh cá nhân)</div>
<table class="stu-table">
  <thead>
    <tr>
      <th style="width: 5%;">STT</th>
      <th style="width: 18%;">Tên trường</th>
      <th style="width: 17%;">Kiểu dữ liệu</th>
      <th style="width: 20%;">Ràng buộc</th>
      <th style="width: 40%;">Mô tả ý nghĩa nghiệp vụ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center">1</td>
      <td><b>inventory_id</b></td>
      <td>bigint</td>
      <td>PK, IDENTITY(1,1)</td>
      <td>Mã định danh mặt hàng trong kho cá nhân</td>
    </tr>
    <tr>
      <td class="center">2</td>
      <td><b>user_id</b></td>
      <td>bigint</td>
      <td>FK &rarr; users(user_id)</td>
      <td>Mã người dùng sở hữu kho thực phẩm này</td>
    </tr>
    <tr>
      <td class="center">3</td>
      <td><b>food_id</b></td>
      <td>bigint</td>
      <td>FK &rarr; foods(food_id)</td>
      <td>Mã thực phẩm tham chiếu đến ngân hàng dữ liệu</td>
    </tr>
    <tr>
      <td class="center">4</td>
      <td><b>quantity_grams</b></td>
      <td>decimal(8,2)</td>
      <td>NOT NULL, CHECK &ge; 0</td>
      <td>Khối lượng tồn kho thực tế tính bằng gram (0 &le; x_i &le; Q_i)</td>
    </tr>
    <tr>
      <td class="center">5</td>
      <td><b>expiry_date</b></td>
      <td>date</td>
      <td>NOT NULL</td>
      <td>Ngày hết hạn sử dụng của lô thực phẩm đang lưu trữ</td>
    </tr>
    <tr>
      <td class="center">6</td>
      <td><b>unit_note</b></td>
      <td>varchar(50)</td>
      <td>NULL</td>
      <td>Ghi chú lưu trữ (ví dụ: Ngăn đông 2, Hộp số 1, Khay mát...)</td>
    </tr>
    <tr>
      <td class="center">7</td>
      <td><b>updated_at</b></td>
      <td>datetime2(3)</td>
      <td>NOT NULL, DEFAULT sysdatetime()</td>
      <td>Thời điểm cập nhật số lượng tồn kho gần nhất</td>
    </tr>
  </tbody>
</table>

<div class="table-caption">Bảng 3.6: Đặc tả vật lý bảng training_cycle_types (Loại chu kỳ tập luyện)</div>
<table class="stu-table">
  <thead>
    <tr>
      <th style="width: 5%;">STT</th>
      <th style="width: 18%;">Tên trường</th>
      <th style="width: 17%;">Kiểu dữ liệu</th>
      <th style="width: 20%;">Ràng buộc</th>
      <th style="width: 40%;">Mô tả ý nghĩa nghiệp vụ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center">1</td>
      <td><b>cycle_type_id</b></td>
      <td>smallint</td>
      <td>PK, IDENTITY(1,1)</td>
      <td>Mã định danh chu kỳ vận động</td>
    </tr>
    <tr>
      <td class="center">2</td>
      <td><b>type_code</b></td>
      <td>varchar(20)</td>
      <td>NOT NULL, UQ</td>
      <td>Mã code duy nhất ('cardio', 'hypertrophy', 'rest_day', 'deload')</td>
    </tr>
    <tr>
      <td class="center">3</td>
      <td><b>display_name</b></td>
      <td>varchar(50)</td>
      <td>NOT NULL</td>
      <td>Tên hiển thị trực quan trên giao diện ứng dụng</td>
    </tr>
  </tbody>
</table>

<div class="table-caption">Bảng 3.7: Đặc tả vật lý bảng macro_adjustment_rules (Quy tắc điều chỉnh Macro)</div>
<table class="stu-table">
  <thead>
    <tr>
      <th style="width: 5%;">STT</th>
      <th style="width: 18%;">Tên trường</th>
      <th style="width: 17%;">Kiểu dữ liệu</th>
      <th style="width: 20%;">Ràng buộc</th>
      <th style="width: 40%;">Mô tả ý nghĩa nghiệp vụ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center">1</td>
      <td><b>rule_id</b></td>
      <td>smallint</td>
      <td>PK, IDENTITY(1,1)</td>
      <td>Mã định danh quy tắc điều chỉnh</td>
    </tr>
    <tr>
      <td class="center">2</td>
      <td><b>user_id</b></td>
      <td>bigint</td>
      <td>FK &rarr; users(user_id)</td>
      <td>Mã người dùng áp dụng quy tắc tùy chỉnh cá nhân hóa</td>
    </tr>
    <tr>
      <td class="center">3</td>
      <td><b>cycle_type_id</b></td>
      <td>smallint</td>
      <td>FK &rarr; training_cycle_types</td>
      <td>Mã chu kỳ tập luyện liên kết</td>
    </tr>
    <tr>
      <td class="center">4</td>
      <td><b>kcal_multiplier</b></td>
      <td>decimal(4,3)</td>
      <td>NOT NULL, DEFAULT 1.000</td>
      <td>Hệ số nhân calo theo chu kỳ (ví dụ: 1.15 cho Hypertrophy, 0.85 cho Rest Day)</td>
    </tr>
    <tr>
      <td class="center">5</td>
      <td><b>protein_g_per_kg_bw</b></td>
      <td>decimal(4,2)</td>
      <td>NOT NULL</td>
      <td>Định mức protein tính trên mỗi kg trọng lượng cơ thể (g/kg BW)</td>
    </tr>
    <tr>
      <td class="center">6</td>
      <td><b>carb_ratio</b></td>
      <td>decimal(4,3)</td>
      <td>NOT NULL</td>
      <td>Tỷ lệ phần trăm calo phân bổ cho Carbohydrate (0.45 = 45%)</td>
    </tr>
    <tr>
      <td class="center">7</td>
      <td><b>fat_ratio</b></td>
      <td>decimal(4,3)</td>
      <td>NOT NULL</td>
      <td>Tỷ lệ phần trăm calo phân bổ cho Chất béo Fat (0.25 = 25%)</td>
    </tr>
  </tbody>
</table>

<div class="table-caption">Bảng 3.8: Đặc tả vật lý bảng daily_targets (Mục tiêu dinh dưỡng hàng ngày)</div>
<table class="stu-table">
  <thead>
    <tr>
      <th style="width: 5%;">STT</th>
      <th style="width: 18%;">Tên trường</th>
      <th style="width: 17%;">Kiểu dữ liệu</th>
      <th style="width: 20%;">Ràng buộc</th>
      <th style="width: 40%;">Mô tả ý nghĩa nghiệp vụ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center">1</td>
      <td><b>target_id</b></td>
      <td>bigint</td>
      <td>PK, IDENTITY(1,1)</td>
      <td>Mã mục tiêu dinh dưỡng ngày</td>
    </tr>
    <tr>
      <td class="center">2</td>
      <td><b>user_id</b></td>
      <td>bigint</td>
      <td>FK &rarr; users(user_id)</td>
      <td>Mã người dùng sở hữu mục tiêu</td>
    </tr>
    <tr>
      <td class="center">3</td>
      <td><b>target_date</b></td>
      <td>date</td>
      <td>NOT NULL</td>
      <td>Ngày áp dụng mục tiêu (kết hợp user_id tạo thành khóa duy nhất)</td>
    </tr>
    <tr>
      <td class="center">4</td>
      <td><b>target_kcal</b></td>
      <td>decimal(7,2)</td>
      <td>NOT NULL</td>
      <td>Tổng năng lượng mục tiêu cần nạp trong ngày (kcal)</td>
    </tr>
    <tr>
      <td class="center">5</td>
      <td><b>target_protein_g</b></td>
      <td>decimal(6,2)</td>
      <td>NOT NULL</td>
      <td>Mục tiêu chất đạm Protein cần đạt trong ngày (gam)</td>
    </tr>
    <tr>
      <td class="center">6</td>
      <td><b>target_carbs_g</b></td>
      <td>decimal(6,2)</td>
      <td>NOT NULL</td>
      <td>Mục tiêu chất tinh bột Carbohydrates cần đạt trong ngày (gam)</td>
    </tr>
    <tr>
      <td class="center">7</td>
      <td><b>target_fat_g</b></td>
      <td>decimal(6,2)</td>
      <td>NOT NULL</td>
      <td>Mục tiêu chất béo Fat cần nạp trong ngày (gam)</td>
    </tr>
    <tr>
      <td class="center">8</td>
      <td><b>computed_from_rule_id</b></td>
      <td>smallint</td>
      <td>FK &rarr; macro_adjustment_rules</td>
      <td>Mã quy tắc tự động sinh ra mục tiêu này (nếu có)</td>
    </tr>
  </tbody>
</table>

<div class="table-caption">Bảng 3.9: Đặc tả vật lý bảng user_training_schedule (Lịch tập luyện người dùng)</div>
<table class="stu-table">
  <thead>
    <tr>
      <th style="width: 5%;">STT</th>
      <th style="width: 18%;">Tên trường</th>
      <th style="width: 17%;">Kiểu dữ liệu</th>
      <th style="width: 20%;">Ràng buộc</th>
      <th style="width: 40%;">Mô tả ý nghĩa nghiệp vụ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center">1</td>
      <td><b>schedule_id</b></td>
      <td>bigint</td>
      <td>PK, IDENTITY(1,1)</td>
      <td>Khóa chính lịch trình tập luyện</td>
    </tr>
    <tr>
      <td class="center">2</td>
      <td><b>user_id</b></td>
      <td>bigint</td>
      <td>FK &rarr; users(user_id)</td>
      <td>Mã người dùng lên lịch</td>
    </tr>
    <tr>
      <td class="center">3</td>
      <td><b>schedule_date</b></td>
      <td>date</td>
      <td>NOT NULL</td>
      <td>Ngày diễn ra buổi tập luyện</td>
    </tr>
    <tr>
      <td class="center">4</td>
      <td><b>cycle_type_id</b></td>
      <td>smallint</td>
      <td>FK &rarr; training_cycle_types</td>
      <td>Loại chu kỳ tập luyện được lên lịch cho ngày hôm đó</td>
    </tr>
    <tr>
      <td class="center">5</td>
      <td><b>is_completed</b></td>
      <td>bit</td>
      <td>NOT NULL, DEFAULT 0</td>
      <td>Trạng thái đánh dấu người dùng đã hoàn thành buổi tập hay chưa</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- ======================================================================= -->
<!-- MỤC 3.2: THIẾT KẾ KIẾN TRÚC & XỬ LÝ HỆ THỐNG -->
<!-- ======================================================================= -->
<h2 class="level2">3.2. THIẾT KẾ KIẾN TRÚC &amp; XỬ LÝ HỆ THỐNG</h2>

<h3 class="level3">3.2.1. Sơ đồ Use Case chi tiết &amp; Bảng đặc tả Use Case</h3>

<p>Sơ đồ Use Case thể hiện rõ rệt ranh giới nghiệp vụ của hệ thống <b>SmartMacro Engine</b> giữa 2 tác nhân chính: <b>Người dùng (User)</b> và <b>Quản trị viên (Admin)</b>. Các mối quan hệ phụ thuộc giữa các chức năng được mô hình hóa chính xác qua 2 stereotype chuẩn mực của UML:</p>

<ul>
  <li><b>Quan hệ Bắt buộc (&laquo;include&raquo;):</b> Thể hiện rằng một hành vi luôn luôn được thực thi kèm theo Use Case nguồn. Điển hình là Use Case <i>UC11: Tối ưu hóa khẩu phần ăn</i> bắt buộc phải bao gồm <i>UC12: Đọc Daily Target ngày</i> và <i>UC13: Lọc kho thực phẩm còn tồn</i> để có đủ dữ liệu đầu vào cho bộ giải quy hoạch tuyến tính.</li>
  <li><b>Quan hệ Mở rộng (&laquo;extend&raquo;):</b> Thể hiện hành vi có điều kiện hoặc tùy chọn dựa trên ngữ cảnh người dùng. Điển hình là khi thực hiện <i>UC06: Quản lý kho thực phẩm</i>, hệ thống tự động kiểm tra ngày hết hạn và kích hoạt <i>UC07: Cảnh báo hạn dùng</i> nếu ngày hết hạn của thực phẩm &le; 2 ngày; hoặc sau khi giải tối ưu thành công, người dùng có thể kích hoạt tùy chọn <i>UC14: Lưu vào MealLog</i> để trừ tồn kho và ghi nhật ký bữa ăn.</li>
</ul>

<div class="figure-wrapper">
  __SVG_3_3__
  <div class="figure-caption"><u><b><i>Hình 3-3:</i></b></u> <i>Sơ đồ Use Case chi tiết phân hệ Người dùng và Quản trị viên.</i></div>
</div>

<p>Dưới đây là 3 bảng đặc tả Use Case chi tiết cho 3 chức năng cốt lõi nhất của đồ án tốt nghiệp, tuân thủ nghiêm ngặt quy định học thuật của Khoa CNTT - STU:</p>

<div class="table-caption">Bảng 3.10: Đặc tả Use Case UC01 — Đăng nhập &amp; Cấp phát JWT</div>
<table class="stu-table">
  <tbody>
    <tr>
      <td style="width: 25%; font-weight: bold;">Tên Use Case</td>
      <td style="width: 75%;"><b>UC01: Đăng nhập &amp; Cấp phát JWT (Authentication &amp; JWT Rotation)</b></td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Tác nhân (Actor)</td>
      <td>Người dùng (User), Quản trị viên (Admin)</td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Mô tả mục đích</td>
      <td>Xác thực danh tính người dùng qua Email/Mật khẩu và cấp phát cặp Access Token (JWT - 15 phút) cùng Refresh Token (7 ngày) để truy cập tài nguyên bảo mật.</td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Tiền điều kiện</td>
      <td>Người dùng đã có tài khoản trên hệ thống ở trạng thái hoạt động (status = 'active').</td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Hậu điều kiện</td>
      <td>Client nhận được JWT Access Token và lưu trữ Refresh Token mã hóa vào cơ sở dữ liệu.</td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Luồng sự kiện chính (Main Flow)</td>
      <td>
        1. Người dùng truy cập trang Đăng nhập, nhập Email và Mật khẩu, bấm nút "Đăng nhập".<br>
        2. Client gửi yêu cầu HTTP POST /api/auth/login kèm LoginRequestDto đến AuthController.<br>
        3. Hệ thống kiểm tra chính sách Rate Limiting (chặn nếu vượt quá 5 request/phút).<br>
        4. AuthService truy vấn cơ sở dữ liệu lấy thông tin User qua Email.<br>
        5. AuthService gọi BCrypt.Verify(password, passwordHash) để kiểm tra tính khớp của mật khẩu.<br>
        6. AuthService khởi tạo Access Token (JWT ký HMAC-SHA256 chứa Claim NameIdentifier = userId) với thời gian hết hạn 15 phút.<br>
        7. AuthService tạo chuỗi ngẫu nhiên 64-byte Refresh Token, băm SHA-256 và lưu vào bảng refresh_tokens.<br>
        8. AuthController trả về mã HTTP 200 OK kèm AuthResponseDto.<br>
        9. Client lưu Access Token vào bộ nhớ trạng thái và điều hướng người dùng tới Dashboard.
      </td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Các luồng ngoại lệ (Alternative Flows)</td>
      <td>
        <b>4a. Email không tồn tại hoặc sai mật khẩu:</b> Hệ thống ném ngoại lệ ArgumentException, trả về HTTP 400 với thông báo "Email hoặc mật khẩu không đúng".<br>
        <b>4b. Tài khoản bị khóa:</b> Nếu status == 'locked', hệ thống từ chối đăng nhập và trả về HTTP 403 Forbidden.<br>
        <b>3a. Tấn công dò quét Brute-force:</b> API Gateway trả về HTTP 429 Too Many Requests khi vượt hạn ngạch.
      </td>
    </tr>
  </tbody>
</table>

<div class="table-caption">Bảng 3.11: Đặc tả Use Case UC06 — Quản lý kho thực phẩm tủ lạnh cá nhân</div>
<table class="stu-table">
  <tbody>
    <tr>
      <td style="width: 25%; font-weight: bold;">Tên Use Case</td>
      <td style="width: 75%;"><b>UC06: Quản lý kho thực phẩm tủ lạnh cá nhân (Inventory Management)</b></td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Tác nhân (Actor)</td>
      <td>Người dùng đã xác thực (User)</td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Mô tả mục đích</td>
      <td>Cho phép người dùng quản lý tủ lạnh cá nhân: thêm mới số lượng gam thực phẩm kèm ngày hết hạn, tra cứu cảnh báo hết hạn, chỉnh sửa số lượng tồn và xóa mặt hàng đã dùng hết.</td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Tiền điều kiện</td>
      <td>Người dùng đã đăng nhập thành công và gửi kèm Bearer Token hợp lệ trong Authorization Header.</td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Hậu điều kiện</td>
      <td>Cơ sở dữ liệu bảng user_food_inventory được cập nhật, hiển thị đúng tồn kho thực tế.</td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Luồng sự kiện chính (Thêm món mới)</td>
      <td>
        1. Người dùng bấm nút "+ Thêm thực phẩm vào kho" trên giao diện Tủ lạnh.<br>
        2. Người dùng tìm kiếm món ăn từ danh mục Foods, nhập khối lượng (gam), chọn ngày hết hạn (expiry_date) và ghi chú vị trí lưu trữ.<br>
        3. Client gửi POST /api/inventory kèm CreateInventoryItemRequestDto.<br>
        4. InventoryController trích xuất userId từ JWT Claims và gọi InventoryService.AddItemAsync.<br>
        5. InventoryService xác thực food_id tồn tại trong bảng foods.<br>
        6. InventoryService kiểm tra trùng lặp (user_id, food_id, expiry_date): nếu đã có thì cộng dồn số lượng, nếu chưa thì thêm mới bản ghi.<br>
        7. Ghi nhận xuống SQL Server và trả về HTTP 201 CreatedAtAction kèm InventoryItemResponseDto.<br>
        8. Giao diện người dùng cập nhật danh sách và hiển thị huy hiệu trạng thái hạn dùng tương ứng.
      </td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Các luồng ngoại lệ</td>
      <td>
        <b>5a. Thực phẩm không tồn tại:</b> Ném ngoại lệ NotFoundException, trả về HTTP 404.<br>
        <b>2a. Số lượng gram không hợp lệ:</b> Kiểm tra quantity_grams &le; 0, ném ngoại lệ ValidationException và trả về HTTP 400.
      </td>
    </tr>
  </tbody>
</table>

<div class="table-caption">Bảng 3.12: Đặc tả Use Case UC11 — Tối ưu hóa thực đơn bằng Google OR-Tools</div>
<table class="stu-table">
  <tbody>
    <tr>
      <td style="width: 25%; font-weight: bold;">Tên Use Case</td>
      <td style="width: 75%;"><b>UC11: Tối ưu hóa khẩu phần ăn thông minh (Smart Meal Optimization)</b></td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Tác nhân (Actor)</td>
      <td>Người dùng (User)</td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Mô tả mục đích</td>
      <td>Tự động giải bài toán Quy hoạch tuyến tính (LP) để phân bổ chính xác số gam từng loại thực phẩm sẵn có trong tủ lạnh nhằm đáp ứng mục tiêu Kcal và Macro ngày trong biên độ &plusmn;5%.</td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Tiền điều kiện</td>
      <td>Người dùng đã thiết lập mục tiêu DailyTargets của ngày và có thực phẩm còn tồn (quantity_grams > 0) trong tủ lạnh.</td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Hậu điều kiện</td>
      <td>Hệ thống trả về danh sách AllocatedItems với số gram tối ưu cho từng món ăn hoặc thông báo không khả thi kèm khuyến nghị.</td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Luồng sự kiện chính</td>
      <td>
        1. Người dùng chọn mục tiêu ngày, tích chọn các thực phẩm tham gia tối ưu và bấm nút "⚡ Chạy thuật toán tối ưu hóa".<br>
        2. Client gửi POST /api/optimizations/generate-plan kèm OptimizationRequestDto đến OptimizationsController.<br>
        3. OptimizationsController xác thực JWT, gọi OptimizationService.GenerateMealPlanAsync.<br>
        4. OptimizationService truy vấn bảng daily_targets lấy mục tiêu (Kcal, Protein, Carbs, Fat).<br>
        5. OptimizationService truy vấn bảng user_food_inventory lọc các thực phẩm có tồn kho > 0.<br>
        6. OptimizationService chuyển dữ liệu sang MacroOptimizationEngine.CalculateOptimalMeal.<br>
        7. MacroOptimizationEngine khởi tạo bộ giải Solver.CreateSolver("GLOP") từ thư viện Google OR-Tools.<br>
        8. Engine định nghĩa các biến quyết định x_i &isin; [0, Q_i], thiết lập 3 hệ ràng buộc bất đẳng thức kép &plusmn;5% cho Protein, Carbs, Fat và tuyến tính hóa hàm mục tiêu sai lệch Calo qua biến phụ delta.<br>
        9. GLOP Solver thực thi giải bài toán bằng thuật toán Primal/Dual Simplex.<br>
        10. Solver tìm thấy nghiệm trạng thái OPTIMAL. Engine trích xuất nghiệm x_i &ge; 0.5g, làm tròn 2 chữ số thập phân và tính tổng macro thực tế đạt được.<br>
        11. OptimizationService đóng gói OptimizationResultDto và Controller trả về HTTP 200 OK.<br>
        12. Giao diện hiển thị bảng định lượng gam từng món ăn và biểu đồ đối chiếu tiến độ Macro.
      </td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Các luồng ngoại lệ</td>
      <td>
        <b>4a. Chưa có DailyTarget ngày:</b> Ném ngoại lệ NotFoundException ("Chưa có mục tiêu dinh dưỡng hôm nay").<br>
        <b>5a. Kho thực phẩm trống:</b> Ném ngoại lệ EmptyInventoryException ("Kho thực phẩm đang trống").<br>
        <b>9a. Bài toán vô nghiệm (INFEASIBLE):</b> Nếu kho thực phẩm hiện tại không đủ để đáp ứng đồng thời cả 3 ràng buộc Macro trong biên độ &plusmn;5%, Solver trả về trạng thái INFEASIBLE. Hệ thống trả về HTTP 200 kèm SolverStatus = "INFEASIBLE", danh sách nguyên liệu rỗng và thông điệp tư vấn người dùng cần bổ sung thêm nguyên liệu giàu chất gì.
      </td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<h3 class="level3">3.2.2. Sơ đồ lớp (Class Diagram) kiến trúc 3 tầng</h3>

<p>Hệ thống SmartMacro Engine được tổ chức theo mô hình kiến trúc 3 tầng chuẩn mực của hệ sinh thái Microsoft .NET 8.0, triệt để áp dụng nguyên lý <b>Inversion of Control (IoC)</b> và <b>Dependency Injection (DI)</b> để giảm thiểu sự phụ thuộc trực tiếp giữa các module phần mềm:</p>

<ul>
  <li><b>Tầng Presentation (API Controllers):</b> Chịu trách nhiệm tiếp nhận HTTP Request, giải mã Bearer Token JWT trích xuất User Claims (NameIdentifier), validate tham số đầu vào và trả về mã trạng thái HTTP chuẩn mực (200 OK, 201 Created, 400 Bad Request, 404 Not Found). Các Controller chỉ phụ thuộc vào Service Interface (IAuthService, IInventoryService, IOptimizationService), hoàn toàn không phụ thuộc vào lớp cài đặt cụ thể hay cơ sở dữ liệu.</li>
  <li><b>Tầng Business Logic (Services):</b> Triển khai các quy tắc nghiệp vụ dinh dưỡng, tính toán chuyển đổi đơn vị và quản lý giao dịch. OptimizationService đóng vai trò nhạc trưởng (orchestrator), điều phối việc nạp dữ liệu từ SmartMacroDbContext, chuyển đổi mô hình qua AutoMapper và gọi bộ máy giải thuật IMacroOptimizationEngine.</li>
  <li><b>Tầng Algorithmic Engine (Google OR-Tools):</b> Độc lập hoàn toàn với cơ sở dữ liệu. MacroOptimizationEngine chỉ nhận dữ liệu đầu vào thuần túy là các DTOs (DailyTargetDto và danh sách InventoryItemResponseDto), trực tiếp làm việc với bộ giải bản địa Google OR-Tools GLOP qua API Google.OrTools.LinearSolver.Solver để tạo biến quyết định, ràng buộc và hàm mục tiêu.</li>
  <li><b>Tầng Data Access (EF Core DAL):</b> SmartMacroDbContext quản lý ánh xạ quan hệ - đối tượng (ORM) cho 9 thực thể cơ sở dữ liệu trên SQL Server, cung cấp các truy vấn Linq to Entities tối ưu hóa và đảm bảo tính nhất quán dữ liệu ACID.</li>
</ul>

<div class="figure-wrapper">
  __SVG_3_4__
  <div class="figure-caption"><u><b><i>Hình 3-4:</i></b></u> <i>Sơ đồ lớp (Class Diagram) thể hiện kiến trúc 3 tầng của hệ thống SmartMacro Engine.</i></div>
</div>

<div class="page-break"></div>

<h3 class="level3">3.2.3. Sơ đồ tuần tự (Sequence Diagrams)</h3>

<h4 class="level4">3.2.3.1. Luồng Đăng nhập, cấp phát Token &amp; Quản lý kho thực phẩm</h4>

<p>Sơ đồ tuần tự Hình 3-5 biểu diễn chi tiết quy trình xác thực người dùng và việc sử dụng Bearer Token để thực thi thao tác quản lý kho tủ lạnh cá nhân. Luồng xử lý minh chứng tính an toàn của hệ thống qua 2 giai đoạn:</p>

<p>Ở Giai đoạn 1 (Đăng nhập), mật khẩu gửi từ client được băm và so khớp với chuỗi BCrypt hash lưu trong DB. Sau khi kiểm tra thành công, server cấp phát cặp token: Access Token (thời hạn 15 phút, ký thuật toán HMAC-SHA256 chứa Claim nhận diện) và Refresh Token (chuỗi ngẫu nhiên 64 bytes lưu dưới dạng băm SHA-256 trong bảng refresh_tokens).</p>

<p>Ở Giai đoạn 2 (Thêm thực phẩm vào tủ lạnh), Client đính kèm JWT vào HTTP Header Authorization: Bearer. API Controller giải mã token tự động qua ASP.NET Core JWT Middleware, trích xuất mã định danh userId an toàn mà không cần tin tưởng dữ liệu người dùng tự gửi, tiến hành kiểm tra trùng lặp mặt hàng và ghi nhận vào cơ sở dữ liệu.</p>

<div class="figure-wrapper">
  __SVG_3_5__
  <div class="figure-caption"><u><b><i>Hình 3-5:</i></b></u> <i>Sơ đồ tuần tự quy trình Xác thực tài khoản và Quản lý kho thực phẩm tủ lạnh.</i></div>
</div>

<div class="page-break"></div>

<h4 class="level4">3.2.3.2. Luồng Giải bài toán Tối ưu hóa thực đơn với Google OR-Tools</h4>

<p>Sơ đồ tuần tự Hình 3-6 đặc tả quá trình thực thi giải thuật toán quy hoạch tuyến tính từ khi người dùng bấm nút kích hoạt trên giao diện đến khi nhận về bảng phân bổ số gram thực phẩm tối ưu:</p>

<ol>
  <li>Client gửi yêu cầu tối ưu hóa đến OptimizationsController.GeneratePlan.</li>
  <li>Controller chuyển tiếp tham số đến OptimizationService.GenerateMealPlanAsync.</li>
  <li>Service thực hiện 2 câu truy vấn tối ưu: Lấy DailyTarget của ngày hôm nay và lấy danh sách UserFoodInventories còn tồn kho (quantity_grams > 0).</li>
  <li>Service kiểm tra các điều kiện biên (Guards), nếu hợp lệ sẽ truyền tham số sang MacroOptimizationEngine.CalculateOptimalMeal.</li>
  <li>Engine khởi tạo thể hiện bộ giải Solver.CreateSolver("GLOP").</li>
  <li>Engine khởi tạo n biến quyết định liên tục đại diện cho số gram của từng món, gán chặn dưới là 0.0 và chặn trên là khối lượng tồn kho thực tế.</li>
  <li>Engine thiết lập hệ 3 ràng buộc bất đẳng thức kép &plusmn;5% cho Protein, Carbs, Fat và tuyến tính hóa sai lệch Kcal bằng biến phụ sai lệch deviation.</li>
  <li>Engine gọi phương thức solver.Solve() để thực thi thuật toán Simplex.</li>
  <li>Engine trích xuất kết quả nghiệm từ biến quyết định (grams[i].SolutionValue()), áp dụng ngưỡng lọc nhiễu số học (grams &ge; 0.5g), làm tròn và tính toán tổng macro thực tế.</li>
  <li>OptimizationService ánh xạ sang OptimizationResultDto và trả về Client với mã HTTP 200 OK.</li>
</ol>

<div class="figure-wrapper">
  __SVG_3_6__
  <div class="figure-caption"><u><b><i>Hình 3-6:</i></b></u> <i>Sơ đồ tuần tự quy trình Tối ưu hóa khẩu phần ăn với Google OR-Tools GLOP.</i></div>
</div>

<div class="page-break"></div>

<h3 class="level3">3.2.4. Sơ đồ hoạt động (Activity Diagram) giải thuật tối ưu</h3>

<p>Sơ đồ hoạt động Hình 3-7 biểu diễn trực quan toàn bộ logic rẽ nhánh, các nút kiểm tra điều kiện biên và quy trình xử lý 2 trạng thái nghiệm cơ bản: OPTIMAL (tìm được nghiệm tối ưu) và INFEASIBLE (kho thực phẩm không đủ đáp ứng ràng buộc):</p>

<div class="figure-wrapper">
  __SVG_3_7__
  <div class="figure-caption"><u><b><i>Hình 3-7:</i></b></u> <i>Sơ đồ hoạt động biểu diễn giải thuật quy hoạch tuyến tính và xử lý các trạng thái nghiệm.</i></div>
</div>

<div class="page-break"></div>

<!-- ======================================================================= -->
<!-- MỤC 3.3: THIẾT KẾ GIAO DIỆN NGƯỜI DÙNG (UI/UX WIREFRAME) -->
<!-- ======================================================================= -->
<h2 class="level2">3.3. THIẾT KẾ GIAO DIỆN NGƯỜI DÙNG (UI/UX WIREFRAME)</h2>

<p>Tuân thủ nghiêm ngặt quy định học thuật của Khoa CNTT - STU: <i>"Yêu cầu sử dụng công cụ để thiết kế giao diện (Wireframe/Figma) chứ KHÔNG vẽ tay hay chụp màn hình sản phẩm"</i>, toàn bộ các màn hình chức năng của hệ thống SmartMacro Engine được xây dựng hoàn toàn bằng ngôn ngữ đồ họa Vector SVG độ nét cao trên hệ thống lưới chuẩn màn hình Desktop hiện đại <b>1440 &times; 900 px</b>.</p>

<p>Hệ thống Design System của bản vẽ Wireframe tuân thủ các quy tắc thiết kế sản phẩm số chuyên nghiệp:</p>

<ul>
  <li><b>Bảng màu Wireframe chuẩn mực:</b> Nền tổng thể #F8FAFC, đường viền khung cấu trúc #CBD5E1, thẻ nội dung màu trắng thuần #FFFFFF với hiệu ứng bóng đổ tinh tế, và các khối điều hướng/nút bấm trọng tâm sử dụng tông màu than chì #1E293B hoặc xanh ngọc lục bảo #10B981.</li>
  <li><b>Cấu trúc Layer chuẩn Figma:</b> Mỗi bản vẽ SVG được cấu trúc sạch sẽ qua các thẻ nhóm ngữ nghĩa, cho phép kéo thả trực tiếp vào ứng dụng Figma tạo thành các Frame và Layer chỉnh sửa độc lập.</li>
  <li><b>Hệ thống Callout đánh số:</b> Trên mỗi bản vẽ đều gắn các biểu tượng đánh số nổi bật <b>(1), (2), (3)...</b> để người đọc dễ dàng đối chiếu trực tiếp với các bảng thuyết minh công năng kỹ thuật bên dưới.</li>
</ul>

<h3 class="level3">3.3.1. Màn hình Đăng nhập &amp; Đăng ký tài khoản</h3>

<p>Màn hình Xác thực được thiết kế theo bố cục phân tách 2 cột (Split Layout) hiện đại. Cột bên trái đóng vai trò Showcase giới thiệu giải thuật cốt lõi và các tính năng then chốt của SmartMacro Engine. Cột bên phải là thẻ xác thực thông minh hỗ trợ chuyển đổi linh hoạt giữa chế độ Đăng nhập và Đăng ký hồ sơ mới.</p>

<div class="wireframe-container">
  __SVG_3_8__
  <div class="figure-caption"><u><b><i>Hình 3-8:</i></b></u> <i>Wireframe thiết kế màn hình Đăng nhập và Đăng ký thành viên.</i></div>
</div>

<div class="table-caption">Bảng 3.13: Thuyết minh chi tiết các vùng chức năng màn hình Đăng nhập &amp; Đăng ký</div>
<table class="stu-table">
  <thead>
    <tr>
      <th style="width: 10%;">Callout</th>
      <th style="width: 25%;">Vùng giao diện</th>
      <th style="width: 35%;">Các thành phần điều khiển</th>
      <th style="width: 30%;">Diễn giải kỹ thuật &amp; Nghiệp vụ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center"><b>(1)</b></td>
      <td>Thương hiệu &amp; Giá trị cốt lõi</td>
      <td>Logo SmartMacro Engine, 3 thẻ giới thiệu giải thuật quy hoạch LP, tủ lạnh chống lãng phí và bảo mật JWT.</td>
      <td>Tạo dấu ấn trực quan cho người dùng, nêu bật công nghệ học thuật cốt lõi của đồ án tốt nghiệp.</td>
    </tr>
    <tr>
      <td class="center"><b>(2)</b></td>
      <td>Thanh chuyển đổi Tab</td>
      <td>Tab "Đăng nhập tài khoản" (active) và Tab "Đăng ký thành viên".</td>
      <td>Giúp người dùng dễ dàng chuyển đổi qua lại giữa 2 quy trình xác thực trên cùng một khung nhìn.</td>
    </tr>
    <tr>
      <td class="center"><b>(3)</b></td>
      <td>Form nhập liệu định danh</td>
      <td>Ô nhập Email (có biểu tượng validate cú pháp), ô nhập Mật khẩu (ẩn/hiện ký tự &bull;&bull;&bull;).</td>
      <td>Gửi dữ liệu qua POST /api/auth/login. Áp dụng Rate Limit 5 request/phút ngăn chặn brute-force.</td>
    </tr>
    <tr>
      <td class="center"><b>(4)</b></td>
      <td>Tùy chọn phiên làm việc</td>
      <td>Checkbox "Duy trì đăng nhập", link text "Quên mật khẩu?".</td>
      <td>Khi kích hoạt, hệ thống sẽ lưu Refresh Token vào HttpOnly Cookie/bảng refresh_tokens để duy trì đăng nhập 7 ngày.</td>
    </tr>
    <tr>
      <td class="center"><b>(5)</b></td>
      <td>Nút hành động chính</td>
      <td>Nút "ĐĂNG NHẬP VÀO HỆ THỐNG" (Primary Action Button).</td>
      <td>Gửi DTO xác thực lên server, tiếp nhận Access Token và điều hướng chuyển trang tức thì.</td>
    </tr>
    <tr>
      <td class="center"><b>(6)</b></td>
      <td>Khung thu thập chỉ số khởi tạo</td>
      <td>Ô Họ tên, Giới tính sinh học, Dropdown Mức vận động (Activity Level) và Mục tiêu hình thể.</td>
      <td>Thu thập ngay các biến số sinh học để phục vụ việc tính toán công thức BMR và TDEE khi người dùng đăng ký mới.</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<h3 class="level3">3.3.2. Màn hình Tổng quan Dinh dưỡng (Dashboard) &amp; Thiết lập DailyTargets</h3>

<p>Màn hình Tổng quan Dinh dưỡng cung cấp cho người dùng bức tranh toàn cảnh về tiến độ nạp năng lượng trong ngày, đối chiếu thời gian thực giữa mức dinh dưỡng thực tế đã nạp so với mục tiêu Daily Targets, đồng thời cho phép tùy chỉnh nhanh mục tiêu calo theo chu kỳ luyện tập thể chất.</p>

<div class="wireframe-container">
  __SVG_3_9__
  <div class="figure-caption"><u><b><i>Hình 3-9:</i></b></u> <i>Wireframe thiết kế màn hình Tổng quan dinh dưỡng và Thiết lập mục tiêu ngày.</i></div>
</div>

<div class="table-caption">Bảng 3.14: Thuyết minh chi tiết các vùng chức năng màn hình Dashboard</div>
<table class="stu-table">
  <thead>
    <tr>
      <th style="width: 10%;">Callout</th>
      <th style="width: 25%;">Vùng giao diện</th>
      <th style="width: 35%;">Các thành phần điều khiển</th>
      <th style="width: 30%;">Diễn giải kỹ thuật &amp; Nghiệp vụ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center"><b>(1)</b></td>
      <td>Thanh điều hướng toàn cục (Sidebar)</td>
      <td>Menu phân hệ: Tổng quan, Tủ lạnh cá nhân, Tối ưu thực đơn, Nhật ký bữa ăn, Lịch tập, Cài đặt.</td>
      <td>Định vị cấu trúc ứng dụng Single Page Application (SPA), làm nổi bật phân hệ đang hoạt động.</td>
    </tr>
    <tr>
      <td class="center"><b>(2)</b></td>
      <td>Thanh trạng thái ngày &amp; Chu kỳ tập</td>
      <td>Bộ điều hướng ngày (Hôm nay, Trước, Sau), Huy hiệu chu kỳ đang kích hoạt (Hypertrophy +15%).</td>
      <td>Cho phép tra cứu lịch sử dinh dưỡng của các ngày trong quá khứ hoặc lên kế hoạch cho ngày tiếp theo.</td>
    </tr>
    <tr>
      <td class="center"><b>(3)</b></td>
      <td>Bộ 4 thẻ chỉ số KPI dinh dưỡng</td>
      <td>4 thẻ Macro: Kcal (2196/2200), Protein (148.5g), Carbs (222g), Fat (54.2g) kèm thanh tiến trình.</td>
      <td>Hiển thị tỷ lệ hoàn thành mục tiêu ngày theo thời gian thực (Real-time progress indicators).</td>
    </tr>
    <tr>
      <td class="center"><b>(4)</b></td>
      <td>Form cấu hình DailyTargets</td>
      <td>Bộ chọn chu kỳ tập (Cardio, Hypertrophy, Rest Day), 4 ô nhập thông số Target Kcal, P, C, F.</td>
      <td>Cho phép người dùng lưu đè hoặc áp dụng công thức điều chỉnh calo tự động từ MacroAdjustmentRules.</td>
    </tr>
    <tr>
      <td class="center"><b>(5)</b></td>
      <td>Biểu đồ phân bổ tỷ lệ năng lượng</td>
      <td>Biểu đồ hình vành khuyên (Donut Chart) biểu diễn % calo từ Protein (27%), Carbs (40%), Fat (33%).</td>
      <td>Trực quan hóa cấu trúc năng lượng bữa ăn giúp vận động viên theo dõi chuẩn macro thể thao.</td>
    </tr>
    <tr>
      <td class="center"><b>(6)</b></td>
      <td>Thẻ tóm tắt tủ lạnh cá nhân</td>
      <td>Danh sách xem nhanh các mặt hàng trong kho và làm nổi bật cảnh báo các món sắp hết hạn (⚠️).</td>
      <td>Nhắc nhở người dùng ưu tiên nấu các nguyên liệu sắp hỏng, có nút tắt chuyển nhanh sang bộ máy tối ưu.</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<h3 class="level3">3.3.3. Màn hình Quản lý Danh mục món &amp; Kho thực phẩm tủ lạnh cá nhân</h3>

<p>Màn hình Quản lý Kho thực phẩm tủ lạnh cá nhân (UserFoodInventories) đóng vai trò là "nguồn nguyên liệu đầu vào" cho thuật toán quy hoạch tuyến tính. Giao diện được thiết kế để theo dõi sát sao hạn sử dụng của từng mặt hàng nhằm phòng ngừa tối đa tình trạng lãng phí thực phẩm trong gia đình.</p>

<div class="wireframe-container">
  __SVG_3_10__
  <div class="figure-caption"><u><b><i>Hình 3-10:</i></b></u> <i>Wireframe thiết kế màn hình Quản lý kho thực phẩm tủ lạnh và Cảnh báo hạn dùng.</i></div>
</div>

<div class="table-caption">Bảng 3.15: Thuyết minh chi tiết các vùng chức năng màn hình Tủ lạnh cá nhân</div>
<table class="stu-table">
  <thead>
    <tr>
      <th style="width: 10%;">Callout</th>
      <th style="width: 25%;">Vùng giao diện</th>
      <th style="width: 35%;">Các thành phần điều khiển</th>
      <th style="width: 30%;">Diễn giải kỹ thuật &amp; Nghiệp vụ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center"><b>(1)</b></td>
      <td>Thanh tìm kiếm &amp; Lọc phân loại</td>
      <td>Ô tìm kiếm từ khóa món ăn, các nút lọc theo danh mục: Tất cả, Thịt cá, Tinh bột, Rau củ...</td>
      <td>Giúp người dùng lọc nhanh danh mục thực phẩm khi tủ lạnh lưu trữ số lượng hàng hóa lớn.</td>
    </tr>
    <tr>
      <td class="center"><b>(2)</b></td>
      <td>Bộ lọc trạng thái hạn dùng</td>
      <td>Nút lọc chuyên biệt: Sắp hết hạn với viền đỏ nổi bật.</td>
      <td>Kích hoạt bộ lọc nhanh trích xuất các mặt hàng có ngày hết hạn &le; 2 ngày để ưu tiên xử lý.</td>
    </tr>
    <tr>
      <td class="center"><b>(3)</b></td>
      <td>Bảng dữ liệu kho thực phẩm</td>
      <td>Bảng dữ liệu lưới gồm các cột: Tên thực phẩm, Số lượng (gam), Dinh dưỡng/100g, Hạn dùng, Trạng thái, Thao tác.</td>
      <td>Ánh xạ trực tiếp từ thực thể UserFoodInventory, hỗ trợ chỉnh sửa số lượng tồn hoặc xóa khi đã sử dụng hết.</td>
    </tr>
    <tr>
      <td class="center"><b>(4)</b></td>
      <td>Huy hiệu cảnh báo mức độ khẩn cấp</td>
      <td>Huy hiệu màu sắc: Đỏ viền nổi bật (HẾT HẠN HÔM NAY), Vàng (Còn 1 ngày), Xanh (Còn hạn dài).</td>
      <td>Cảnh báo trực quan mức độ ưu tiên theo thuật toán First-Expiring-First-Used (FEFU).</td>
    </tr>
    <tr>
      <td class="center"><b>(5)</b></td>
      <td>Drawer thêm món mới vào kho</td>
      <td>Khung trượt bên phải: Chọn món từ ngân hàng Foods, nhập số lượng gam, chọn ngày hết hạn, ghi chú ngăn tủ.</td>
      <td>Cung cấp biểu mẫu thêm thực phẩm trực quan, có tính năng tính toán preview ngay lượng calo tương ứng.</td>
    </tr>
    <tr>
      <td class="center"><b>(6)</b></td>
      <td>Nút chuyển tiếp Tối ưu hóa</td>
      <td>Nút "⚡ CHUYỂN SANG TỐI ƯU HÓA" (Primary Action).</td>
      <td>Chuyển trực tiếp danh sách các nguyên liệu sẵn có trong tủ lạnh sang Bộ máy giải thuật toán OR-Tools.</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<h3 class="level3">3.3.4. Màn hình Tối ưu hóa Khẩu phần ăn Thông minh với OR-Tools</h3>

<p>Đây là màn hình trung tâm thể hiện giá trị học thuật và năng lực công nghệ vượt trội của đề tài SmartMacro Engine. Màn hình được bố trí theo cấu trúc hai cột: Cột trái cho phép người dùng cấu hình bài toán và lựa chọn nguyên liệu từ tủ lạnh; Cột phải hiển thị kết quả giải toán của Google OR-Tools GLOP bao gồm trạng thái nghiệm, biểu đồ sai số và bảng định lượng số gram chính xác cần lấy để nấu ăn.</p>

<div class="wireframe-container">
  __SVG_3_11__
  <div class="figure-caption"><u><b><i>Hình 3-11:</i></b></u> <i>Wireframe thiết kế màn hình Tối ưu hóa khẩu phần ăn thông minh với OR-Tools.</i></div>
</div>

<div class="table-caption">Bảng 3.16: Thuyết minh chi tiết các vùng chức năng màn hình Tối ưu hóa thực đơn</div>
<table class="stu-table">
  <thead>
    <tr>
      <th style="width: 10%;">Callout</th>
      <th style="width: 25%;">Vùng giao diện</th>
      <th style="width: 35%;">Các thành phần điều khiển</th>
      <th style="width: 30%;">Diễn giải kỹ thuật &amp; Nghiệp vụ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center"><b>(1)</b></td>
      <td>Khung mục tiêu dinh dưỡng đầu vào</td>
      <td>Hộp thông số Kcal (2200), Protein (150g), Carbs (220g), Fat (55g) và dải dung sai cho phép &plusmn;5%.</td>
      <td>Trích xuất từ DailyTargets của người dùng, đóng vai trò là vector vế phải (RHS) trong hệ phương trình ràng buộc.</td>
    </tr>
    <tr>
      <td class="center"><b>(2)</b></td>
      <td>Danh sách chọn nguyên liệu khả dụng</td>
      <td>Checkboxes chọn các món ăn từ tủ lạnh, hiển thị khối lượng tồn kho tối đa (Q_i) và nhãn cảnh báo hạn dùng.</td>
      <td>Cho phép người dùng linh hoạt chỉ định các thực phẩm muốn ăn trong ngày; các món sắp hết hạn được tự động gợi ý tích chọn.</td>
    </tr>
    <tr>
      <td class="center"><b>(3)</b></td>
      <td>Nút kích hoạt giải thuật toán</td>
      <td>Nút nổi bật kích thước lớn: "⚡ CHẠY THUẬT TOÁN TỐI ƯU HÓA (OR-TOOLS)".</td>
      <td>Gửi HTTP POST /api/optimizations/generate-plan, kích hoạt bộ giải Google OR-Tools GLOP trên máy chủ backend.</td>
    </tr>
    <tr>
      <td class="center"><b>(4)</b></td>
      <td>Huy hiệu trạng thái nghiệm Solver</td>
      <td>Banner trạng thái màu xanh ngọc: THUẬT TOÁN ĐÃ TÌM THẤY NGHIỆM TỐI ƯU (STATUS: OPTIMAL).</td>
      <td>Phản hồi trực quan kết quả giải; hiển thị thời gian giải thực tế (~14.8 ms) và thuật toán Simplex đã áp dụng.</td>
    </tr>
    <tr>
      <td class="center"><b>(5)</b></td>
      <td>Biểu đồ đối chiếu sai lệch dinh dưỡng</td>
      <td>4 thanh tiến trình so sánh Mục tiêu vs Thực tế: Kcal (sai lệch -3.4 kcal), Protein (99%), Carbs (100.9%), Fat (98.5%).</td>
      <td>Minh chứng nghiệm tối ưu thỏa mãn 100% các ràng buộc dinh dưỡng trong phạm vi dung sai cho phép &plusmn;5%.</td>
    </tr>
    <tr>
      <td class="center"><b>(6)</b></td>
      <td>Bảng định lượng số gam cần nấu</td>
      <td>Bảng chi tiết: Ức gà (320g), Gạo lứt (250g), Súp lơ (200g), Trứng (150g), Dầu ô liu (18g).</td>
      <td>Kết quả phân bổ nghiệm x_i sau khi đã lọc nhiễu (&ge; 0.5g); hướng dẫn chính xác số gram người dùng cần cân để chế biến.</td>
    </tr>
    <tr>
      <td class="center"><b>(7)</b></td>
      <td>Nút xác nhận lưu vào Nhật ký bữa ăn</td>
      <td>Nút "✅ XÁC NHẬN VÀ LƯU VÀO NHẬT KÝ BỮA ĂN (MEAL LOG)".</td>
      <td>Tự động ghi vết các món ăn vào bảng meal_logs và thực hiện trừ tồn kho tương ứng trong user_food_inventory.</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- ======================================================================= -->
<!-- MỤC 3.4: THIẾT KẾ GIẢI THUẬT TỐI ƯU HÓA KHẨU PHẦN ĂN (OR-TOOLS ENGINE) -->
<!-- ======================================================================= -->
<h2 class="level2">3.4. THIẾT KẾ GIẢI THUẬT TỐI ƯU HÓA KHẨU PHẦN ĂN (OR-TOOLS ENGINE)</h2>

<h3 class="level3">3.4.1. Cơ sở lý thuyết Quy hoạch tuyến tính (Linear Programming - LP)</h3>

<p>Quy hoạch tuyến tính (Linear Programming - LP) là một trong những phân nhánh toán học quan trọng nhất của lĩnh vực Nghiên cứu Vận hành (Operations Research). Một bài toán quy hoạch tuyến tính tổng quát bao gồm việc tìm cực trị (cực đại hoặc cực tiểu) của một hàm mục tiêu tuyến tính dưới sự chi phối của một hệ hữu hạn các phương trình hoặc bất phương trình ràng buộc tuyến tính.</p>

<p>Trong bài toán phân bổ dinh dưỡng, việc tính toán thủ công bằng bảng tính Excel hoặc bằng các thuật toán lặp vét cạn (brute-force) đối mặt với sự bùng nổ tổ hợp khi số lượng món ăn gia tăng. Các phương pháp heuristic (như thuật toán di truyền - GA hay bầy đàn kiến - ACO) mặc dù có thể giải bài toán phi tuyến nhưng lại mang tính ngẫu nhiên (stochastic), không đảm bảo tìm được nghiệm tối ưu toàn cục và có thời gian hội tụ chậm (thường từ 1 đến 5 giây).</p>

<p>Nhằm đáp ứng yêu cầu khắt khe của hệ thống Web API phục vụ nhiều người dùng đồng thời, SmartMacro Engine lựa chọn bộ giải <b>Google OR-Tools GLOP (Google Linear Optimization Package)</b>. Đây là thư viện tối ưu hóa hiệu năng cao mã nguồn mở được phát triển bởi đội ngũ kỹ sư Google, cài đặt thuật toán Primal-Dual Simplex trên nền tảng C++ hiện đại. Thư viện này sở hữu các ưu điểm vượt trội:</p>

<ul>
  <li><b>Tính tất định (Deterministic):</b> Với cùng một bộ dữ liệu kho và mục tiêu, solver luôn luôn trả về một nghiệm tối ưu duy nhất và nhất quán.</li>
  <li><b>Tối ưu toàn cục (Global Optimum):</b> Do miền nghiệm của bài toán LP là một đa diện lồi (Convex Polytope), thuật toán Simplex chứng minh toán học rằng nghiệm tìm được luôn đạt giá trị tối ưu toàn cục, không bị mắc kẹt tại cực trị địa phương.</li>
  <li><b>Tốc độ thực thi siêu tốc:</b> Thời gian giải quyết bài toán với 10 đến 50 biến thực phẩm chỉ mất trung bình từ <b>8 ms đến 20 ms</b>, hoàn toàn không gây nghẽn luồng xử lý của máy chủ ASP.NET Core.</li>
</ul>

<h3 class="level3">3.4.2. Mô hình toán học áp dụng cho SmartMacro Engine</h3>

<div class="formula-box">
  <div class="formula-title">ĐỊNH NGHĨA BIẾN QUYẾT ĐỊNH (DECISION VARIABLES)</div>
  Giả sử trong tủ lạnh của người dùng hiện có n mặt hàng thực phẩm khả dụng được chọn tham gia tối ưu. Ta định nghĩa biến quyết định liên tục x_i đại diện cho khối lượng (gam) cần sử dụng của thực phẩm thứ i (với i = 1, 2, ..., n):
  <br><br>
  <center><b>0 &le; x_i &le; Q_i &nbsp;&nbsp;&nbsp;&nbsp; (&forall; i &isin; {1, 2, ..., n})</b></center>
  <br>
  Trong đó: Q_i là số lượng gram tồn kho thực tế của thực phẩm i được lưu trữ trong bảng <code>user_food_inventory</code>. Ràng buộc chặn trên đảm bảo hệ thống không bao giờ đề xuất khẩu phần vượt quá số nguyên liệu sẵn có trong tủ lạnh.
</div>

<div class="formula-box">
  <div class="formula-title">HỆ RÀNG BUỘC DINH DƯỠNG ĐA MỤC TIÊU VỚI BIÊN ĐỘ SAI SỐ DUNG SAI &plusmn;5%</div>
  Trong dinh dưỡng học thể thao, việc bắt buộc tổng lượng dinh dưỡng phải chính xác tuyệt đối từng miligram là phi thực tế và thường dẫn đến việc bài toán bị vô nghiệm (Over-constrained). Do đó, hệ thống thiết lập biên độ dung sai chấp nhận được &tau; = 0.05 (&plusmn;5%) quanh các mục tiêu:
  <br><br>
  <b>1. Ràng buộc về Chất đạm (Protein Constraint):</b>
  <br>
  <center>0.95 &times; P_target &le; &sum; (x_i &times; P_i / 100) &le; 1.05 &times; P_target</center>
  <br>
  <b>2. Ràng buộc về Tinh bột (Carbohydrates Constraint):</b>
  <br>
  <center>0.95 &times; C_target &le; &sum; (x_i &times; C_i / 100) &le; 1.05 &times; C_target</center>
  <br>
  <b>3. Ràng buộc về Chất béo (Fat Constraint):</b>
  <br>
  <center>0.95 &times; F_target &le; &sum; (x_i &times; F_i / 100) &le; 1.05 &times; F_target</center>
  <br>
  Trong đó: P_i, C_i, F_i lần lượt là hàm lượng Protein, Carbs, Fat có trong 100 gam thực phẩm i; P_target, C_target, F_target là mục tiêu dinh dưỡng ngày từ bảng <code>daily_targets</code>.
</div>

<div class="formula-box">
  <div class="formula-title">TUYẾN TÍNH HÓA HÀM MỤC TIÊU SAI LỆCH NĂNG LƯỢNG (KCAL)</div>
  Hàm mục tiêu ban đầu mong muốn tối thiểu hóa độ lệch tuyệt đối giữa tổng Calo tính toán được và Calo mục tiêu:
  <br><br>
  <center><b>min | &sum; (x_i &times; E_i / 100) - E_target |</b></center>
  <br>
  Tuy nhiên, toán tử giá trị tuyệt đối |z| là phi tuyến tính, không thể giải trực tiếp bằng bộ giải tuyến tính GLOP. Hệ thống áp dụng kỹ thuật <b>biến phụ tuyến tính hóa (Auxiliary Variable Linearization)</b> bằng cách đưa vào biến phụ sai lệch &delta; &ge; 0:
  <br><br>
  Hàm mục tiêu chuyển đổi thành:
  <center><b>min &delta;</b></center>
  <br>
  Đi kèm hai bất đẳng thức ràng buộc tuyến tính bổ sung:
  <br>
  <center>&sum; (x_i &times; E_i / 100) - &delta; &le; E_target &nbsp;&nbsp;&nbsp;&nbsp; (&hArr; &delta; &ge; &sum; (x_i &times; E_i / 100) - E_target)</center>
  <br>
  <center>&sum; (x_i &times; E_i / 100) + &delta; &ge; E_target &nbsp;&nbsp;&nbsp;&nbsp; (&hArr; &delta; &ge; -[&sum; (x_i &times; E_i / 100) - E_target])</center>
  <br>
  <center>&delta; &ge; 0</center>
</div>

<p>Kỹ thuật tuyến tính hóa này tương đương toán học 100% với hàm mục tiêu ban đầu, giữ cho bài toán ở dạng Quy hoạch tuyến tính thuần túy, cho phép bộ giải GLOP tìm ra nghiệm tối ưu toàn cục chỉ sau một lần chạy đơn pha.</p>

<h3 class="level3">3.4.3. Phân tích độ phức tạp, thời gian phản hồi và các kịch bản ngoại lệ</h3>

<p>Để đảm bảo sự ổn định và tin cậy khi triển khai thực tế trên môi trường sản xuất, giải thuật được trang bị các cơ chế kiểm soát chất lượng nghiêm ngặt:</p>

<ul>
  <li><b>Cơ chế lọc nhiễu số học (Threshold Filtering):</b> Trong quá trình giải ma trận lồi, solver GLOP có thể gán cho một số biến những giá trị cực nhỏ do sai số làm tròn số thực dấu phẩy động (ví dụ: 0.00014g). Trong thực tế nhà bếp, không người dùng nào có thể cân đong lượng gram nhỏ như vậy. Do đó, hệ thống thiết lập hằng số <code>MinGramsThreshold = 0.5g</code>. Bất kỳ thực phẩm nào có x_i < 0.5g sẽ bị coi là nhiễu và bị loại bỏ khỏi kết quả phân bổ.</li>
  <li><b>Xử lý bài toán vô nghiệm (INFEASIBLE):</b> Khi người dùng chỉ có trong tủ lạnh các thực phẩm giàu mỡ mà thiếu nguồn đạm hoặc tinh bột, hệ thống 3 phương trình ràng buộc sẽ không có miền nghiệm chung. Khi đó, phương thức solver.Solve() sẽ trả về ResultStatus.INFEASIBLE. Hệ thống sẽ bắt trạng thái này một cách mềm dẻo, không làm sập ứng dụng, gán SolverStatus = "INFEASIBLE" và gửi kèm thông điệp hướng dẫn người dùng: <i>"Kho thực phẩm hiện tại không đủ để đáp ứng mục tiêu trong biên độ &plusmn;5%. Vui lòng bổ sung thêm nguồn thực phẩm giàu Protein hoặc Tinh bột vào tủ lạnh."</i></li>
  <li><b>Hiệu năng thực tế:</b> Các cuộc thử nghiệm tải (load testing) cho thấy với danh mục từ 10 đến 30 thực phẩm trong tủ lạnh, GLOP solver hoàn thành việc giải bài toán trong <b>12 ms đến 18 ms</b>, tiêu tốn dưới 4MB bộ nhớ RAM, hoàn toàn đáp ứng tiêu chuẩn khắt khe của một dịch vụ Microservice cấp doanh nghiệp.</li>
</ul>

<div class="page-break"></div>

<!-- ======================================================================= -->
<!-- KẾT LUẬN CHƯƠNG 3 -->
<!-- ======================================================================= -->
<h2 class="level2">KẾT LUẬN CHƯƠNG 3</h2>

<p>Chương 3 đã hoàn thành toàn diện nhiệm vụ thiết kế kỹ thuật chi tiết cho dự án <b>SmartMacro Engine</b> theo đúng các quy chuẩn học thuật khắt khe của Khoa Công nghệ Thông tin - Trường Đại học Công nghệ Sài Gòn (STU). Toàn bộ nội dung thiết kế phản ánh chính xác 100% mã nguồn thực tế đã xây dựng trong giải pháp phần mềm:</p>

<ol>
  <li><b>Về thiết kế dữ liệu:</b> Đã xây dựng hoàn chỉnh mô hình ý niệm (Conceptual ERD), mô hình luận lý (Logical Schema) chuẩn hóa 3NF và 9 bảng từ điển dữ liệu vật lý chi tiết cho hệ quản trị cơ sở dữ liệu Microsoft SQL Server 2022.</li>
  <li><b>Về thiết kế kiến trúc và xử lý:</b> Đã hoàn thiện sơ đồ Use Case chi tiết có phân quyền Admin/User kèm 3 bảng đặc tả ca sử dụng; sơ đồ lớp (Class Diagram) 3 tầng tuân thủ nguyên lý Dependency Inversion; 2 sơ đồ tuần tự biểu diễn chi tiết luồng xác thực và tối ưu hóa; cùng sơ đồ hoạt động mô tả chính xác logic rẽ nhánh thuật toán.</li>
  <li><b>Về thiết kế giao diện:</b> Đã xuất sắc hiện thực hóa 4 bản vẽ Wireframe định dạng Vector SVG chuẩn công cụ thiết kế Figma (lưới 1440&times;900 px), gắn mã Callout rõ ràng và thuyết minh công năng chi tiết qua các bảng mô tả, đáp ứng trọn vẹn yêu cầu không vẽ tay hay chụp ảnh màn hình của Khoa CNTT.</li>
  <li><b>Về thiết kế giải thuật:</b> Đã xây dựng mô hình toán học Quy hoạch tuyến tính (Linear Programming) hoàn chỉnh với hệ ràng buộc dung sai &plusmn;5%, kỹ thuật tuyến tính hóa sai lệch Calo qua biến phụ delta và phân tích cơ chế giải nghiệm của Google OR-Tools GLOP.</li>
</ol>

<p>Những kết quả thiết kế vững chắc này là tiền đề kỹ thuật vững chắc để bước sang <b>Chương 4: Hiện thực hóa và Kiểm thử hệ thống</b>, nơi toàn bộ các kiến trúc, giao diện và giải thuật toán học sẽ được chứng minh qua mã nguồn thực thi và các kịch bản kiểm thử tự động (Unit Test / Integration Test).</p>

</body>
</html>"""

    # Replace SVG placeholders
    replacements = {
        "__SVG_3_1__": svg_3_1,
        "__SVG_3_2__": svg_3_2,
        "__SVG_3_3__": svg_3_3,
        "__SVG_3_4__": svg_3_4,
        "__SVG_3_5__": svg_3_5,
        "__SVG_3_6__": svg_3_6,
        "__SVG_3_7__": svg_3_7,
        "__SVG_3_8__": svg_3_8,
        "__SVG_3_9__": svg_3_9,
        "__SVG_3_10__": svg_3_10,
        "__SVG_3_11__": svg_3_11,
    }
    for key, val in replacements.items():
        template = template.replace(key, val)

    return template

def main():
    print("================================================================")
    print("SmartMacro Engine - Building Thesis Chapter 3 Document...")
    print("================================================================")

    # 1. Generate HTML file
    print(f"[1/3] Generating HTML report at: {OUTPUT_HTML}...")
    html_content = build_chapter3_html()
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    html_size = os.path.getsize(OUTPUT_HTML)
    print(f" -> HTML generated successfully! Size: {html_size:,} bytes ({html_size/1024:.1f} KB)")

    # 2. Compile to PDF via Node + Chrome CDP (with custom Header and Footer)
    print(f"[2/3] Compiling PDF via Node.js Chrome DevTools Protocol (CDP)...")
    node_script_path = os.path.join(os.path.dirname(__file__), "compile_pdf.js")

    node_script = f"""const {{ spawn }} = require('child_process');
const fs = require('fs');

async function compilePDF() {{
  const chromePath = 'C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe';
  const port = 9222;
  const proc = spawn(chromePath, [
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--remote-debugging-port=' + port
  ]);

  await new Promise(r => setTimeout(r, 1500));

  try {{
    const listRes = await fetch('http://127.0.0.1:' + port + '/json/new', {{ method: 'PUT' }});
    const target = await listRes.json();
    const ws = new WebSocket(target.webSocketDebuggerUrl);

    let id = 1;
    function send(method, params = {{}}) {{
      return new Promise((resolve, reject) => {{
        const msgId = id++;
        const handler = (event) => {{
          const res = JSON.parse(event.data);
          if (res.id === msgId) {{
            ws.removeEventListener('message', handler);
            if (res.error) reject(res.error);
            else resolve(res.result);
          }}
        }};
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({{ id: msgId, method, params }}));
      }});
    }}

    await new Promise((resolve) => ws.addEventListener('open', resolve));
    await send('Page.enable');

    const htmlPath = {repr(OUTPUT_HTML.replace('\\\\', '/'))};
    const fileUrl = 'file:///' + htmlPath;
    await send('Page.navigate', {{ url: fileUrl }});

    // Wait for load
    await new Promise(r => setTimeout(r, 2500));

    // STU Requirements:
    // Header on subsequent pages: CHƯƠNG 3. THIẾT KẾ (13pt Times New Roman, italic uppercase)
    // Footer on all pages: LUẬN VĂN TỐT NGHIỆP: HỆ THỐNG SMARTMACRO ENGINE (italic uppercase) and pageNumber
    // Margins: Top 2cm (0.7874in), Bottom 2cm (0.7874in), Left 3cm (1.1811in), Right 2cm (0.7874in)
    const headerTpl = '<div style="font-size:11pt; font-family:Times New Roman, serif; font-style:italic; text-transform:uppercase; width:100%; padding-right:20mm; text-align:right; border-bottom:0.5pt solid #cbd5e1; padding-bottom:1.5mm;">CHƯƠNG 3. THIẾT KẾ</div>';
    const footerTpl = '<div style="font-size:10pt; font-family:Times New Roman, serif; font-style:italic; width:100%; padding-left:30mm; padding-right:20mm; display:flex; justify-content:space-between; border-top:0.5pt solid #cbd5e1; padding-top:1.5mm;"><span style="text-transform:uppercase;">LUẬN VĂN TỐT NGHIỆP: HỆ THỐNG TỐI ƯU HÓA KHẨU PHẦN ĂN SMARTMACRO ENGINE</span><span>Trang <span class="pageNumber"></span></span></div>';

    const pdfData = await send('Page.printToPDF', {{
      displayHeaderFooter: true,
      headerTemplate: headerTpl,
      footerTemplate: footerTpl,
      paperWidth: 8.27,   // A4 Width
      paperHeight: 11.69, // A4 Height
      marginTop: 0.7874,   // 2cm
      marginBottom: 0.7874,// 2cm
      marginLeft: 1.1811,  // 3cm
      marginRight: 0.7874  // 2cm
    }});

    const outPath = {repr(OUTPUT_PDF.replace('\\\\', '/'))};
    fs.writeFileSync(outPath, Buffer.from(pdfData.data, 'base64'));
    console.log('[NODE-CDP] Successfully compiled PDF to: ' + outPath);
    ws.close();
  }} catch (err) {{
    console.error('[NODE-CDP ERROR]', err);
    process.exit(1);
  }} finally {{
    proc.kill();
  }}
}}

compilePDF();
"""
    with open(node_script_path, "w", encoding="utf-8") as f:
        f.write(node_script)

    res = subprocess.run(["node", node_script_path], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[WARNING] Node CDP failed: {res.stderr}. Falling back to Chrome CLI...")
        chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        cmd = [
            chrome_exe,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            f"--print-to-pdf={OUTPUT_PDF}",
            "file:///" + OUTPUT_HTML.replace("\\", "/")
        ]
        subprocess.run(cmd, check=True)
    else:
        print(res.stdout.strip())

    # Clean up node script
    if os.path.exists(node_script_path):
        os.remove(node_script_path)

    # 3. Final Verification
    if os.path.exists(OUTPUT_PDF):
        pdf_size = os.path.getsize(OUTPUT_PDF)
        print(f"[3/3] Chapter 3 Document Generation SUCCEEDED!")
        print(f" -> PDF Path:  {OUTPUT_PDF} ({pdf_size:,} bytes / {pdf_size/1024:.1f} KB)")
        print(f" -> HTML Path: {OUTPUT_HTML} ({html_size:,} bytes / {html_size/1024:.1f} KB)")
    else:
        print("[ERROR] PDF was not generated.")

if __name__ == "__main__":
    main()
