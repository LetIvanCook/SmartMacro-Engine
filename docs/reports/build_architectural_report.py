# -*- coding: utf-8 -*-
"""
SmartMacro Engine - Báo cáo Phân tích & Thiết kế Hệ thống (Buổi 4/10 - Thực tập Chuyên ngành)
Biên dịch nội dung HTML học thuật (vừa sức sinh viên CNTT năm 4) sang PDF chuẩn A4.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time


def build_report_html():
    return """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Báo cáo Thực tập Chuyên ngành (Buổi 4/10) - SmartMacro Engine</title>
<style>
    @page {
        size: A4 portrait;
        margin: 14mm 14mm 14mm 14mm;
    }

    * {
        box-sizing: border-box;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }

    body {
        font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
        color: #1e293b;
        background-color: #ffffff;
        line-height: 1.5;
        font-size: 9.5pt;
        margin: 0;
        padding: 0;
    }

    .page-break {
        page-break-before: always;
        break-before: page;
    }

    .no-break {
        page-break-inside: avoid;
        break-inside: avoid;
    }

    h1, h2, h3, h4 {
        color: #0f172a;
        font-weight: 700;
        margin-top: 0.9em;
        margin-bottom: 0.4em;
        line-height: 1.3;
    }

    h1 {
        font-size: 16pt;
        color: #0f172a;
        border-bottom: 2.5px solid #059669;
        padding-bottom: 5px;
        margin-top: 0;
        text-transform: uppercase;
    }

    h2 {
        font-size: 12.5pt;
        color: #065f46;
        border-bottom: 1px solid #a7f3d0;
        padding-bottom: 3px;
        margin-top: 1em;
    }

    h3 {
        font-size: 10.5pt;
        color: #1e40af;
        margin-top: 0.8em;
    }

    p {
        margin-top: 0;
        margin-bottom: 0.6em;
        text-align: justify;
    }

    ul, ol {
        margin-top: 0.2em;
        margin-bottom: 0.6em;
        padding-left: 20px;
    }

    li {
        margin-bottom: 0.25em;
    }

    /* Cover Page */
    .cover-page {
        min-height: 258mm;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 16mm 12mm;
        border: 2px solid #cbd5e1;
        border-radius: 8px;
        background: linear-gradient(180deg, #f8fafc 0%, #f0fdf4 100%);
    }

    .cover-school {
        text-align: center;
        border-bottom: 2px solid #059669;
        padding-bottom: 12px;
    }

    .cover-school-title {
        font-size: 11pt;
        font-weight: 700;
        color: #334155;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    .cover-subject {
        display: inline-block;
        margin-top: 8px;
        background: #059669;
        color: #ffffff;
        padding: 4px 14px;
        border-radius: 4px;
        font-size: 9.5pt;
        font-weight: 700;
        text-transform: uppercase;
    }

    .cover-main {
        text-align: center;
        margin: 24px 0;
    }

    .cover-label {
        font-size: 11pt;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .cover-title {
        font-size: 21pt;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.25;
        margin: 10px 0 12px 0;
    }

    .cover-subtitle {
        font-size: 11pt;
        color: #334155;
        font-weight: 500;
        max-width: 90%;
        margin: 0 auto;
        line-height: 1.45;
    }

    .cover-meta {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 16px 20px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }

    .meta-item {
        font-size: 9.2pt;
    }

    .meta-label {
        color: #64748b;
        font-size: 8pt;
        font-weight: 600;
        text-transform: uppercase;
    }

    .meta-val {
        color: #0f172a;
        font-weight: 700;
        margin-top: 2px;
    }

    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 8px 0 12px 0;
        font-size: 8.6pt;
        background: #ffffff;
    }

    th, td {
        border: 1px solid #cbd5e1;
        padding: 6px 8px;
        vertical-align: top;
        text-align: left;
    }

    th {
        background-color: #0f172a;
        color: #ffffff;
        font-weight: 600;
    }

    tr:nth-child(even) {
        background-color: #f8fafc;
    }

    /* Callouts */
    .qa-box {
        border: 1px solid #cbd5e1;
        border-left: 4px solid #059669;
        border-radius: 6px;
        background: #f8fafc;
        padding: 8px 12px;
        margin-bottom: 9px;
    }

    .qa-question {
        font-weight: 700;
        color: #065f46;
        font-size: 9.6pt;
        margin-bottom: 4px;
    }

    .callout {
        border-left: 4px solid #2563eb;
        background-color: #eff6ff;
        border-top: 1px solid #bfdbfe;
        border-right: 1px solid #bfdbfe;
        border-bottom: 1px solid #bfdbfe;
        padding: 8px 12px;
        border-radius: 0 6px 6px 0;
        margin: 8px 0;
    }

    .callout-green {
        border-left-color: #059669;
        background-color: #ecfdf5;
        border-color: #a7f3d0;
    }

    .pill {
        display: inline-block;
        padding: 1px 7px;
        border-radius: 10px;
        font-size: 7.6pt;
        font-weight: 600;
    }

    .pill-green { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
    .pill-blue { background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }
    .pill-amber { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
    .pill-red { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }

    code {
        font-family: Consolas, 'Courier New', monospace;
        background: #f1f5f9;
        color: #be185d;
        padding: 1px 4px;
        border-radius: 3px;
        font-size: 8.4pt;
    }

    pre {
        font-family: Consolas, 'Courier New', monospace;
        background: #0f172a;
        color: #f8fafc;
        padding: 8px 10px;
        border-radius: 6px;
        font-size: 8pt;
        line-height: 1.4;
        margin: 6px 0;
        overflow-x: auto;
    }

    /* Diagram Containers */
    .diagram-box {
        border: 1.5px solid #94a3b8;
        border-radius: 8px;
        padding: 10px;
        background: #ffffff;
        margin: 8px 0 12px 0;
        text-align: center;
    }

    .diagram-caption {
        font-size: 8.5pt;
        font-weight: 600;
        color: #475569;
        margin-top: 6px;
        text-align: center;
        font-style: italic;
    }

    /* 3-Tier Visual */
    .tier-grid {
        display: grid;
        grid-template-columns: 1fr 30px 1fr 30px 1fr;
        align-items: center;
        gap: 4px;
        margin: 10px 0;
    }

    .tier-card {
        border: 1.5px solid #cbd5e1;
        border-radius: 6px;
        padding: 8px;
        background: #f8fafc;
        text-align: left;
        height: 100%;
    }

    .tier-title {
        font-weight: 700;
        font-size: 9pt;
        padding-bottom: 4px;
        margin-bottom: 5px;
        border-bottom: 1px solid #cbd5e1;
    }

    .tier-arrow {
        text-align: center;
        font-weight: 800;
        color: #059669;
        font-size: 13pt;
    }
</style>
</head>
<body>

<!-- ====================================================================== -->
<!-- TRANG BÌA                                                              -->
<!-- ====================================================================== -->
<div class="cover-page">
    <div class="cover-school">
        <div class="cover-school-title">KHOA CÔNG NGHỆ THÔNG TIN — BÁO CÁO ĐỒ ÁN CÁ NHÂN</div>
        <div class="cover-subject">HỌC PHẦN: THỰC TẬP CHUYÊN NGÀNH (BUỔI 4 / 10)</div>
    </div>

    <div class="cover-main">
        <div class="cover-label">ĐỀ TÀI THỰC TẬP CHUYÊN NGÀNH</div>
        <div class="cover-title">XÂY DỰNG HỆ THỐNG QUẢN LÝ DINH DƯỠNG VÀ GỢI Ý KHẨU PHẦN ĂN TỐI ƯU TỪ NGUYÊN LIỆU SẴN CÓ (SMARTMACRO ENGINE)</div>
        <div class="cover-subtitle">
            Giải pháp ứng dụng Web theo mô hình 3 lớp (React TypeScript — ASP.NET Core 8 Web API — SQL Server) kết hợp giải thuật Quy hoạch Tuyến tính (Google OR-Tools) hỗ trợ tính toán thực đơn theo mục tiêu Macro
        </div>
    </div>

    <div>
        <div class="cover-meta">
            <div class="meta-item">
                <div class="meta-label">Đối tượng thực hiện</div>
                <div class="meta-val">Sinh viên CNTT Năm 4 (Đồ án cá nhân)</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">Tiến độ báo cáo</div>
                <div class="meta-val">Buổi 4/10: Hoàn thiện trả lời 12 câu hỏi &amp; 3 sơ đồ thiết kế (BFD, Use Case, ERD)</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">Công nghệ sử dụng</div>
                <div class="meta-val">React + TypeScript, ASP.NET Core 8, EF Core 8 (Code-First), Google OR-Tools, SQL Server</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">Phạm vi &amp; Quy mô áp dụng</div>
                <div class="meta-val">Cá nhân tập thể hình / ăn kiêng &amp; Phòng Gym / CLB Thể hình quy mô vừa và nhỏ</div>
            </div>
        </div>

        <div style="margin-top: 14px; padding: 10px 14px; background: #ffffff; border: 1px solid #a7f3d0; border-radius: 6px; font-size: 8.8pt;">
            <strong>Mục lục nội dung báo cáo Buổi 4/10:</strong>
            <ol style="margin: 4px 0 0 0; padding-left: 18px;">
                <li><strong>Phần 1:</strong> Trả lời trực diện 12 câu hỏi định hướng đề tài của Buổi 3/10 (Mục tiêu, Phạm vi, Khảo sát, Phân quyền 2 vai trò, Kiến trúc 3 tầng).</li>
                <li><strong>Phần 2:</strong> Thiết kế hệ thống qua 3 Sơ đồ bắt buộc của Buổi 4/10: Sơ đồ Phân rã Chức năng (BFD), Sơ đồ Use Case &amp; Đặc tả, Sơ đồ Quan hệ Thực thể (ERD).</li>
                <li><strong>Phần 3:</strong> Giải thích chi tiết giải thuật Quy hoạch Tuyến tính (OR-Tools) và Kết quả xây dựng giao diện Web thực tế để Demo.</li>
            </ol>
        </div>
    </div>

    <div style="border-top: 1px solid #cbd5e1; padding-top: 8px; display: flex; justify-content: space-between; font-size: 8pt; color: #64748b;">
        <span>Đồ án Thực tập Chuyên ngành Công nghệ Thông tin</span>
        <span>Năm học 2026</span>
    </div>
</div>

<!-- ====================================================================== -->
<!-- PHẦN 1: TRẢ LỜI TRỰC DIỆN 12 CÂU HỎI CỦA BUỔI 3/10                     -->
<!-- ====================================================================== -->
<div class="page-break"></div>

<h1>PHẦN 1: TRẢ LỜI TRỰC DIỆN 12 CÂU HỎI ĐỊNH HƯỚNG ĐỀ TÀI (BUỔI 3/10)</h1>
<p>
    Dưới đây là phần tổng hợp và trả lời trực diện 12 câu hỏi cốt lõi về mục tiêu, phạm vi, phân quyền và kiến trúc kỹ thuật của đề tài <strong>SmartMacro Engine</strong>, được điều chỉnh vừa sức với phạm vi đồ án cá nhân của sinh viên CNTT năm 4:
</p>

<h2>1. Nhóm câu hỏi về Mục tiêu, Phạm vi &amp; Khảo sát thực tế (Câu 1 &rarr; Câu 6)</h2>

<div class="qa-box no-break">
    <div class="qa-question">Câu 1: Tên đề tài là gì? Xuất phát từ bài toán thực tế nào?</div>
    <p style="margin-bottom: 0;">
        <strong>Trả lời:</strong> Tên đề tài là <em>"Xây dựng hệ thống quản lý dinh dưỡng và gợi ý khẩu phần ăn tối ưu từ nguyên liệu sẵn có (SmartMacro Engine)"</em>. Đề tài xuất phát từ khó khăn thực tế của người tập thể hình (Gym) và người ăn kiêng: mỗi ngày họ cần ăn đúng chỉ số dinh dưỡng (Calo, Protein, Tinh bột - Carb, Chất béo - Fat). Tuy nhiên, khi mở tủ lạnh ra chỉ có sẵn một số nguyên liệu (ví dụ: ức gà, trứng, cơm trắng, khoai lang), việc tự bấm máy tính nhẩm xem cần lấy mỗi món bao nhiêu gram để vừa đủ chất vừa không vượt quá lượng thức ăn đang có là rất mất thời gian và dễ sai lệch.
    </p>
</div>

<div class="qa-box no-break">
    <div class="qa-question">Câu 2: Mục tiêu cụ thể mà hệ thống cần giải quyết là gì?</div>
    <p style="margin-bottom: 0;">
        <strong>Trả lời:</strong> Hệ thống giải quyết 3 mục tiêu cụ thể: (1) Số hóa danh mục thực phẩm kèm chỉ số dinh dưỡng trên mỗi 100g và quản lý số lượng thực phẩm tồn trong tủ lạnh cá nhân (kèm ngày hết hạn); (2) Cho phép người dùng thiết lập mục tiêu dinh dưỡng hàng ngày (Calo, Protein, Carb, Fat); (3) Tự động giải bài toán tìm số gram cần ăn cho từng món trong kho sao cho tổng Protein, Carb, Fat nằm trong sai số cho phép (&plusmn;5%) và tổng Calo sát với mục tiêu nhất.
    </p>
</div>

<div class="qa-box no-break">
    <div class="qa-question">Câu 3: Phạm vi ứng dụng và quy mô triển khai của đề tài hướng tới đâu?</div>
    <p style="margin-bottom: 0;">
        <strong>Trả lời:</strong> Hệ thống được xây dựng dưới dạng <strong>ứng dụng Web cá nhân</strong> dành cho người tự tập luyện ăn kiêng tại nhà, đồng thời rất phù hợp áp dụng cho các <strong>Phòng Gym / CLB Thể hình quy mô vừa và nhỏ</strong>. Tại các phòng tập này, Huấn luyện viên cá nhân (PT) hoặc hội viên có thể nhập danh sách thực phẩm sẵn có của hội viên để lập thực đơn định lượng theo gram nhanh chóng mà không cần tính tay thủ công.
    </p>
</div>

<div class="qa-box no-break">
    <div class="qa-question">Câu 4: Đối tượng người dùng trực tiếp của hệ thống gồm những ai?</div>
    <p style="margin-bottom: 0;">
        <strong>Trả lời:</strong> Gồm 2 nhóm đối tượng trực tiếp: (1) <strong>Người dùng / Hội viên (User/Member)</strong>: sinh viên, người tập thể hình, người giảm cân/tăng cơ hoặc PT sử dụng hệ thống để quản lý tủ lạnh và tính khẩu phần ăn hàng ngày; (2) <strong>Quản trị viên (Admin)</strong>: người quản lý hệ thống tại CLB hoặc chủ ứng dụng, chịu trách nhiệm cập nhật danh mục nhóm thực phẩm, kiểm duyệt chỉ số dinh dưỡng các món ăn chuẩn và quản lý tài khoản người dùng.
    </p>
</div>

<div class="qa-box no-break">
    <div class="qa-question">Câu 5: Khảo sát các phần mềm tương tự trên thị trường và điểm khác biệt của đề tài là gì?</div>
    <p style="margin-bottom: 0;">
        <strong>Trả lời:</strong> Các ứng dụng nổi tiếng hiện nay như <em>MyFitnessPal, FatSecret, Cronometer</em> chủ yếu hoạt động theo hướng <strong>ghi nhật ký thụ động</strong> (người dùng tự cân đồ ăn rồi nhập vào để phần mềm cộng tổng Calo). Một số trang gợi ý thực đơn như <em>Spoonacular</em> lại gợi ý theo công thức nấu ăn cố định (bắt người dùng phải đi chợ mua thêm nguyên liệu). Điểm khác biệt của <strong>SmartMacro Engine</strong> là giải bài toán theo chiều ngược lại: <strong>dựa hoàn toàn vào những món đang có sẵn trong tủ lạnh của người dùng</strong>, áp dụng thư viện quy hoạch tuyến tính <code>Google.OrTools</code> để tính ra số gram chính xác của từng món cần lấy.
    </p>
</div>

<div class="qa-box no-break">
    <div class="qa-question">Câu 6: Hệ thống gồm những nhóm chức năng nghiệp vụ nào? (Sơ đồ BFD)</div>
    <p style="margin-bottom: 0;">
        <strong>Trả lời:</strong> Theo sơ đồ phân rã chức năng BFD (được trình bày chi tiết tại Mục 1 - Phần 2 của báo cáo), hệ thống gồm <strong>6 nhóm chức năng chính</strong>: (1) Quản lý tài khoản &amp; xác thực; (2) Quản lý danh mục &amp; thực phẩm; (3) Quản lý kho thực phẩm cá nhân (tủ lạnh); (4) Thiết lập mục tiêu dinh dưỡng &amp; lịch tập; (5) Tính toán thực đơn tối ưu (Meal Optimizer); (6) Tổng hợp &amp; thống kê báo cáo (Dashboard).
    </p>
</div>

<h2>2. Nhóm câu hỏi về Phân quyền &amp; Bảo mật vừa sức (Câu 7 &amp; Câu 8)</h2>

<div class="qa-box no-break">
    <div class="qa-question">Câu 7: Hệ thống phân quyền gồm mấy vai trò (Role)? Tại sao chọn cách phân quyền này?</div>
    <p style="margin-bottom: 4px;">
        <strong>Trả lời:</strong> Để phù hợp với phạm vi đồ án cá nhân của sinh viên năm 4 và đảm bảo tính trực quan, dễ kiểm chứng, hệ thống tinh giản thành <strong>2 vai trò cốt lõi</strong>:
    </p>
    <ul style="margin-bottom: 0;">
        <li><strong>Vai trò 1 — <code>Admin</code> (Quản trị viên):</strong> Quản lý danh mục nhóm thực phẩm (<code>FoodCategories</code>: Thịt/Cá, Tinh bột, Rau củ...), quản lý dữ liệu dinh dưỡng món ăn hệ thống (<code>Foods</code>: Calo, Protein, Carb, Fat trên 100g) và quản lý thông tin người dùng (<code>Users</code>).</li>
        <li><strong>Vai trò 2 — <code>User / Member</code> (Người dùng / Hội viên):</strong> Đăng ký/đăng nhập, quản lý hồ sơ cá nhân, thiết lập mục tiêu Macro hàng ngày (<code>DailyTargets</code>), thêm/sửa/xóa nguyên liệu trong kho tủ lạnh cá nhân (<code>Inventory</code>), bấm nút tính toán thực đơn tối ưu (<code>Optimizations</code>) và xem trang tổng quan (<code>Dashboard</code>).</li>
    </ul>
</div>

<div class="qa-box no-break">
    <div class="qa-question">Câu 8: Cơ chế đăng nhập, xác thực và bảo vệ API được cài đặt trong code như thế nào?</div>
    <p style="margin-bottom: 4px;">
        <strong>Trả lời:</strong> Hệ thống cài đặt cơ chế xác thực tại <code>AuthController.cs</code> và <code>AuthService.cs</code> dựa trên chuẩn <strong>JWT (JSON Web Token)</strong> kết hợp <strong>Refresh Token</strong> lưu trong SQL Server:
    </p>
    <ul style="margin-bottom: 0;">
        <li><strong>Mã hóa mật khẩu:</strong> Khi đăng ký (<code>POST /api/auth/register</code>), mật khẩu không lưu dạng chữ thuần mà được băm một chiều bằng thư viện <code>BCrypt.Net-Next</code> trước khi lưu vào cột <code>password_hash</code> của bảng <code>users</code>.</li>
        <li><strong>Cấp phát JWT Access Token:</strong> Khi đăng nhập đúng email và mật khẩu (<code>POST /api/auth/login</code>), Backend tạo ra một <code>AccessToken</code> chuẩn JWT có thời hạn <strong>15 phút</strong>. Bên trong payload của Token chứa thông tin định danh người dùng (<code>ClaimTypes.NameIdentifier</code> lưu <code>UserId</code> và <code>Email</code>), được ký bằng khóa bí mật HMAC-SHA256.</li>
        <li><strong>Lưu Refresh Token trong bảng <code>RefreshTokens</code>:</strong> Đi kèm Access Token là một chuỗi <code>RefreshToken</code> có hạn <strong>7 ngày</strong>. Để an toàn, hệ thống băm SHA-256 chuỗi này rồi lưu vào bảng <code>refresh_tokens</code> trong SQL Server (gồm các cột: <code>id</code>, <code>user_id</code>, <code>token</code>, <code>expires_at</code>, <code>revoked_at</code>). Khi Access Token hết hạn 15 phút, Frontend tự động gọi <code>POST /api/auth/refresh</code> để lấy cặp token mới mà không bắt người dùng đăng nhập lại. Khi đăng xuất (<code>POST /api/auth/logout</code>), hệ thống cập nhật cột <code>revoked_at</code> để vô hiệu hóa token.</li>
        <li><strong>Kiểm tra quyền trên các API:</strong> Các Controller nghiệp vụ được gắn thuộc tính <code>[Authorize]</code>. Mỗi khi người dùng thao tác trên Kho thực phẩm (<code>InventoryController</code>) hay Mục tiêu ngày (<code>DailyTargetsController</code>), hàm <code>GetUserId()</code> đọc trực tiếp <code>UserId</code> từ JWT Token để đảm bảo người dùng nào chỉ xem và sửa được dữ liệu của chính người dùng đó.</li>
    </ul>
</div>

<table>
    <thead>
        <tr>
            <th style="width: 24%;">Chức năng / Module</th>
            <th style="width: 28%;">Endpoint API tương ứng</th>
            <th style="width: 24%;">Admin (Quản trị viên)</th>
            <th style="width: 24%;">User / Member (Hội viên)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Đăng ký, Đăng nhập, Làm mới Token</strong></td>
            <td><code>POST /api/auth/register, login, refresh, logout</code></td>
            <td><span class="pill pill-green">✔ Được phép</span></td>
            <td><span class="pill pill-green">✔ Được phép</span></td>
        </tr>
        <tr>
            <td><strong>Quản lý Danh mục nhóm thực phẩm</strong></td>
            <td><code>GET, POST, PUT, DELETE /api/food-categories</code></td>
            <td><span class="pill pill-green">✔ Toàn quyền thêm/sửa/xóa</span></td>
            <td><span class="pill pill-blue">👁 Xem danh mục</span></td>
        </tr>
        <tr>
            <td><strong>Quản lý Dữ liệu Món ăn hệ thống</strong></td>
            <td><code>GET, POST, PUT, DELETE /api/foods</code></td>
            <td><span class="pill pill-green">✔ Toàn quyền quản trị món</span></td>
            <td><span class="pill pill-blue">👁 Tra cứu &amp; đóng góp món</span></td>
        </tr>
        <tr>
            <td><strong>Quản lý Kho tủ lạnh cá nhân</strong></td>
            <td><code>GET, POST, PUT, DELETE /api/inventory</code></td>
            <td><span class="pill pill-blue">Chỉ kho của mình</span></td>
            <td><span class="pill pill-green">✔ Toàn quyền kho cá nhân</span></td>
        </tr>
        <tr>
            <td><strong>Thiết lập Mục tiêu Macro ngày</strong></td>
            <td><code>GET, POST, PUT, DELETE /api/daily-targets</code></td>
            <td><span class="pill pill-blue">Chỉ mục tiêu của mình</span></td>
            <td><span class="pill pill-green">✔ Thiết lập &amp; cập nhật</span></td>
        </tr>
        <tr>
            <td><strong>Tính toán Thực đơn tối ưu (OR-Tools)</strong></td>
            <td><code>POST /api/optimizations/generate-plan</code></td>
            <td><span class="pill pill-green">✔ Kiểm thử thuật toán</span></td>
            <td><span class="pill pill-green">✔ Tính khẩu phần ăn tối ưu</span></td>
        </tr>
        <tr>
            <td><strong>Xem Tổng quan Dashboard</strong></td>
            <td><code>GET /api/dashboard/summary</code></td>
            <td><span class="pill pill-green">✔ Xem tổng quan</span></td>
            <td><span class="pill pill-green">✔ Xem tổng quan cá nhân</span></td>
        </tr>
    </tbody>
</table>

<!-- ====================================================================== -->
<!-- CÂU 9, 10, 11, 12: CÔNG NGHỆ & LIÊN KẾT 3 TẦNG                         -->
<!-- ====================================================================== -->
<div class="page-break"></div>

<h2>3. Nhóm câu hỏi về Công nghệ &amp; Liên kết Kiến trúc 3 Tầng (Câu 9 &rarr; Câu 12)</h2>

<div class="qa-box no-break">
    <div class="qa-question">Câu 9: Hệ thống được thiết kế theo mô hình kiến trúc nào?</div>
    <p style="margin-bottom: 0;">
        <strong>Trả lời:</strong> Hệ thống được xây dựng theo mô hình <strong>Client - Server 3 tầng (3-Tier Architecture)</strong> tách biệt rõ ràng:
        (1) <strong>Tầng Giao diện (Front-end / Presentation Layer)</strong> là ứng dụng Web SPA viết bằng React + TypeScript chạy trên trình duyệt của người dùng;
        (2) <strong>Tầng Xử lý nghiệp vụ (Back-end / Business Logic Layer)</strong> là Web API viết bằng ASP.NET Core 8 (chia rõ thành các lớp <code>Controllers</code> &rarr; <code>Services</code> &rarr; <code>Engines</code>);
        (3) <strong>Tầng Cơ sở dữ liệu (Data Layer)</strong> sử dụng hệ quản trị CSDL quan hệ Microsoft SQL Server kết nối qua Entity Framework Core 8.
    </p>
</div>

<div class="qa-box no-break">
    <div class="qa-question">Câu 10: Tại sao lại chọn bộ công nghệ React + TypeScript ở Front-end và ASP.NET Core 8 + OR-Tools ở Back-end?</div>
    <p style="margin-bottom: 0;">
        <strong>Trả lời:</strong>
        <br/>• <strong>Ở tầng Front-end (React + TypeScript + Tailwind CSS):</strong> React giúp chia giao diện thành các thành phần (Component) trực quan, cập nhật dữ liệu tức thì trên một trang duy nhất (SPA) mà không cần tải lại trang khi bấm tính toán thực đơn. TypeScript giúp định nghĩa kiểu dữ liệu (Interface) khớp chính xác với các lớp DTO của C#, hạn chế lỗi sai tên biến khi gọi API. Tailwind CSS giúp trình bày bố cục bảng biểu và thẻ chỉ số dinh dưỡng gọn gàng, dễ đọc.
        <br/>• <strong>Ở tầng Back-end (ASP.NET Core 8 Web API + EF Core 8 + Google OR-Tools):</strong> C# và .NET là nền tảng vững chắc, quen thuộc trong chương trình học đại học, hỗ trợ Dependency Injection và kiểm tra kiểu dữ liệu chặt chẽ. Đặc biệt, hệ sinh thái .NET tích hợp rất tốt gói thư viện toán học <code>Google.OrTools</code> (bộ giải GLOP), cho phép biểu diễn bài toán tìm số gram thức ăn thành các biến và phương trình tuyến tính ngay trong class <code>MacroOptimizationEngine.cs</code>.
    </p>
</div>

<div class="qa-box no-break">
    <div class="qa-question">Câu 11: Tại sao chọn Hệ quản trị CSDL Microsoft SQL Server và phương pháp EF Core Code-First?</div>
    <p style="margin-bottom: 0;">
        <strong>Trả lời:</strong> <strong>Microsoft SQL Server</strong> là hệ quản trị CSDL quan hệ phổ biến và gần gũi nhất với sinh viên CNTT, đảm bảo tính toàn vẹn dữ liệu thông qua khóa chính (PK), khóa ngoại (FK), ràng buộc duy nhất (Unique Index như một người dùng chỉ có 1 mục tiêu trên 1 ngày) và kiểu dữ liệu số thập phân chính xác <code>decimal(6,2)</code> cho các chỉ số dinh dưỡng. Kết hợp với phương pháp <strong>Entity Framework Core Code-First</strong>, sinh viên định nghĩa các lớp Model C# và cấu hình quan hệ trong <code>SmartMacroDbContext.cs</code>, sau đó sử dụng công cụ Migrations để tự động tạo bảng trên SQL Server, giúp đồng bộ 100% giữa code C# và CSDL.
    </p>
</div>

<div class="qa-box no-break">
    <div class="qa-question">Câu 12: Ba tầng Front-end, Back-end và Database liên kết và truyền dữ liệu với nhau như thế nào?</div>
    <p style="margin-bottom: 0;">
        <strong>Trả lời:</strong> Toàn bộ quy trình liên kết giữa 3 tầng diễn ra theo một vòng đời khép kín (Request - Response Lifecycle):
        <br/><strong>Bước 1 (Front-end &rarr; Back-end):</strong> Khi người dùng thao tác trên giao diện React (ví dụ bấm nút <em>"Tính toán khẩu phần ăn tối ưu"</em>), thư viện <strong>Axios</strong> (`apiClient`) sẽ đóng gói dữ liệu thành định dạng <strong>JSON</strong>, tự động đính kèm <code>Authorization: Bearer &lt;JWT_Token&gt;</code> vào HTTP Header và gửi request <code>POST /api/optimizations/generate-plan</code> tới cổng của ASP.NET Core API.
        <br/><strong>Bước 2 (Back-end xử lý &amp; gọi Database):</strong> Middleware của ASP.NET Core kiểm tra tính hợp lệ của JWT Token, trích xuất <code>UserId</code> và chuyển vào <code>OptimizationsController</code> &rarr; gọi <code>OptimizationService</code>. Tại đây, Service sử dụng <code>SmartMacroDbContext</code> (EF Core LINQ) dịch các truy vấn C# sang câu lệnh <strong>SQL</strong> để lấy mục tiêu hôm nay từ bảng <code>daily_targets</code> và danh sách nguyên liệu còn hàng từ bảng <code>user_food_inventory</code> (kết nối bảng <code>foods</code>) trong <strong>SQL Server</strong>.
        <br/><strong>Bước 3 (Giải toán &amp; Trả kết quả về Giao diện):</strong> Dữ liệu lấy từ SQL Server được nạp vào <code>MacroOptimizationEngine</code> (Google OR-Tools) để giải tìm số gram tối ưu cho từng món. Kết quả được đóng gói vào đối tượng <code>OptimizationResultDto</code>, trả về HTTP Status <code>200 OK</code> dưới dạng chuỗi JSON để React cập nhật ngay lên bảng kết quả trên màn hình.
    </p>
</div>

<div class="tier-grid no-break">
    <div class="tier-card">
        <div class="tier-title" style="color: #0369a1;">TẦNG 1: FRONT-END (CLIENT)</div>
        <div style="font-size: 8.2pt;">
            • <strong>Công nghệ:</strong> React 19, TypeScript, Vite, Tailwind CSS.<br/>
            • <strong>Quản lý trạng thái:</strong> Zustand (lưu thông tin User &amp; Token).<br/>
            • <strong>Giao tiếp mạng:</strong> Axios Client có Interceptor tự động gắn Bearer Token &amp; làm mới Token.<br/>
            • <strong>Màn hình chính:</strong> Tổng quan &amp; Mục tiêu, Kho tủ lạnh, Gợi ý thực đơn.
        </div>
    </div>
    <div class="tier-arrow">&harr;<div style="font-size: 7pt; font-weight: 600; color: #475569;">HTTP JSON<br/>REST API</div></div>
    <div class="tier-card">
        <div class="tier-title" style="color: #065f46;">TẦNG 2: BACK-END (WEB API)</div>
        <div style="font-size: 8.2pt;">
            • <strong>Nền tảng:</strong> ASP.NET Core 8 Web API.<br/>
            • <strong>Cấu trúc lớp:</strong> Controllers &rarr; Services &rarr; Engines.<br/>
            • <strong>Thuật toán:</strong> Google OR-Tools (GLOP Linear Solver) tính số gram thức ăn.<br/>
            • <strong>Ánh xạ dữ liệu:</strong> AutoMapper + DTOs.<br/>
            • <strong>ORM:</strong> Entity Framework Core 8.
        </div>
    </div>
    <div class="tier-arrow">&harr;<div style="font-size: 7pt; font-weight: 600; color: #475569;">EF Core<br/>LINQ / SQL</div></div>
    <div class="tier-card">
        <div class="tier-title" style="color: #92400e;">TẦNG 3: DATABASE (CSDL)</div>
        <div style="font-size: 8.2pt;">
            • <strong>Hệ quản trị:</strong> Microsoft SQL Server.<br/>
            • <strong>Bảng cốt lõi:</strong> <code>users</code>, <code>refresh_tokens</code>, <code>food_categories</code>, <code>foods</code>, <code>user_food_inventory</code>, <code>daily_targets</code>...<br/>
            • <strong>Ràng buộc:</strong> Khóa chính (PK), Khóa ngoại (FK 1-N), Unique Index chống trùng lặp.
        </div>
    </div>
</div>

<!-- ====================================================================== -->
<!-- PHẦN 2: 3 SƠ ĐỒ BẮT BUỘC CỦA BUỔI 4/10 (BFD, USE CASE, ERD)            -->
<!-- ====================================================================== -->
<div class="page-break"></div>

<h1>PHẦN 2: BA SƠ ĐỒ PHÂN TÍCH &amp; THIẾT KẾ HỆ THỐNG (BUỔI 4/10)</h1>

<h2>1. Sơ Đồ BFD (Business Function Diagram — Sơ Đồ Phân Rã Chức Năng)</h2>

<div class="callout callout-green">
    <strong>Định nghĩa Sơ đồ BFD (Business Function Diagram):</strong>
    Sơ đồ phân rã chức năng (BFD) là công cụ biểu diễn các chức năng nghiệp vụ của hệ thống theo cấu trúc hình cây phân cấp từ tổng quát đến chi tiết (Top-Down). Sơ đồ BFD giúp trả lời câu hỏi <em>"Hệ thống cần làm những công việc gì?"</em> một cách trực quan, làm cơ sở để xác định phạm vi phần mềm trước khi đi vào thiết kế cơ sở dữ liệu và giao diện.
</div>

<div class="diagram-box no-break">
    <svg viewBox="0 0 920 350" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
        <!-- Styles -->
        <defs>
            <style>
                .root-box { fill: #0f172a; stroke: #0f172a; stroke-width: 1.5; rx: 6; }
                .root-text { fill: #ffffff; font-size: 12px; font-weight: bold; text-anchor: middle; }
                .lvl1-box { fill: #059669; stroke: #047857; stroke-width: 1.5; rx: 5; }
                .lvl1-text { fill: #ffffff; font-size: 10px; font-weight: bold; text-anchor: middle; }
                .leaf-box { fill: #f8fafc; stroke: #94a3b8; stroke-width: 1.2; rx: 4; }
                .leaf-text { fill: #1e293b; font-size: 9.2px; font-weight: 600; text-anchor: middle; }
                .tree-line { stroke: #475569; stroke-width: 1.5; fill: none; }
            </style>
        </defs>

        <!-- Root Node -->
        <rect x="260" y="10" width="400" height="36" class="root-box"/>
        <text x="460" y="32" class="root-text">HỆ THỐNG QUẢN LÝ &amp; TỐI ƯU DINH DƯỠNG SMARTMACRO ENGINE</text>

        <!-- Trunk & Horizontal Connector -->
        <line x1="460" y1="46" x2="460" y2="68" class="tree-line"/>
        <line x1="78" y1="68" x2="842" y2="68" class="tree-line"/>

        <!-- Vertical drops to 6 Level-1 nodes -->
        <line x1="78" y1="68" x2="78" y2="88" class="tree-line"/>
        <line x1="231" y1="68" x2="231" y2="88" class="tree-line"/>
        <line x1="384" y1="68" x2="384" y2="88" class="tree-line"/>
        <line x1="537" y1="68" x2="537" y2="88" class="tree-line"/>
        <line x1="690" y1="68" x2="690" y2="88" class="tree-line"/>
        <line x1="842" y1="68" x2="842" y2="88" class="tree-line"/>

        <!-- Level 1 Nodes (6 Groups) -->
        <!-- Group 1 -->
        <rect x="10" y="88" width="136" height="40" class="lvl1-box"/>
        <text x="78" y="105" class="lvl1-text">1. Quản lý</text>
        <text x="78" y="119" class="lvl1-text">Tài khoản</text>
        <line x1="78" y1="128" x2="78" y2="305" class="tree-line"/>
        <rect x="14" y="145" width="128" height="32" class="leaf-box"/>
        <text x="78" y="165" class="leaf-text">1.1. Đăng ký tài khoản</text>
        <rect x="14" y="190" width="128" height="32" class="leaf-box"/>
        <text x="78" y="210" class="leaf-text">1.2. Đăng nhập / Xuất</text>
        <rect x="14" y="235" width="128" height="32" class="leaf-box"/>
        <text x="78" y="255" class="leaf-text">1.3. Cấp mới JWT Token</text>
        <rect x="14" y="280" width="128" height="32" class="leaf-box"/>
        <text x="78" y="300" class="leaf-text">1.4. Quản lý hồ sơ User</text>

        <!-- Group 2 -->
        <rect x="163" y="88" width="136" height="40" class="lvl1-box"/>
        <text x="231" y="105" class="lvl1-text">2. Quản lý Danh mục</text>
        <text x="231" y="119" class="lvl1-text">&amp; Thực phẩm</text>
        <line x1="231" y1="128" x2="231" y2="305" class="tree-line"/>
        <rect x="167" y="145" width="128" height="32" class="leaf-box"/>
        <text x="231" y="165" class="leaf-text">2.1. Quản lý nhóm món</text>
        <rect x="167" y="190" width="128" height="32" class="leaf-box"/>
        <text x="231" y="210" class="leaf-text">2.2. Thêm/Sửa/Xóa món</text>
        <rect x="167" y="235" width="128" height="32" class="leaf-box"/>
        <text x="231" y="255" class="leaf-text">2.3. Tra cứu &amp; Lọc món</text>
        <rect x="167" y="280" width="128" height="32" class="leaf-box"/>
        <text x="231" y="300" class="leaf-text">2.4. Chỉ số Macro/100g</text>

        <!-- Group 3 -->
        <rect x="316" y="88" width="136" height="40" class="lvl1-box"/>
        <text x="384" y="105" class="lvl1-text">3. Quản lý Kho</text>
        <text x="384" y="119" class="lvl1-text">Cá nhân (Tủ lạnh)</text>
        <line x1="384" y1="128" x2="384" y2="305" class="tree-line"/>
        <rect x="320" y="145" width="128" height="32" class="leaf-box"/>
        <text x="384" y="165" class="leaf-text">3.1. Xem tồn kho hiện tại</text>
        <rect x="320" y="190" width="128" height="32" class="leaf-box"/>
        <text x="384" y="210" class="leaf-text">3.2. Nhập món vào kho</text>
        <rect x="320" y="235" width="128" height="32" class="leaf-box"/>
        <text x="384" y="255" class="leaf-text">3.3. Cập nhật số gram</text>
        <rect x="320" y="280" width="128" height="32" class="leaf-box"/>
        <text x="384" y="300" class="leaf-text">3.4. Theo dõi hạn dùng</text>

        <!-- Group 4 -->
        <rect x="469" y="88" width="136" height="40" class="lvl1-box"/>
        <text x="537" y="105" class="lvl1-text">4. Thiết lập Mục tiêu</text>
        <text x="537" y="119" class="lvl1-text">&amp; Lịch tập</text>
        <line x1="537" y1="128" x2="537" y2="305" class="tree-line"/>
        <rect x="473" y="145" width="128" height="32" class="leaf-box"/>
        <text x="537" y="165" class="leaf-text">4.1. Đặt mục tiêu ngày</text>
        <rect x="473" y="190" width="128" height="32" class="leaf-box"/>
        <text x="537" y="210" class="leaf-text">4.2. Cập nhật P / C / F</text>
        <rect x="473" y="235" width="128" height="32" class="leaf-box"/>
        <text x="537" y="255" class="leaf-text">4.3. Quản lý chu kỳ tập</text>
        <rect x="473" y="280" width="128" height="32" class="leaf-box"/>
        <text x="537" y="300" class="leaf-text">4.4. Quy tắc chỉnh Macro</text>

        <!-- Group 5 -->
        <rect x="622" y="88" width="136" height="40" class="lvl1-box"/>
        <text x="690" y="105" class="lvl1-text">5. Tính toán</text>
        <text x="690" y="119" class="lvl1-text">Thực đơn tối ưu</text>
        <line x1="690" y1="128" x2="690" y2="305" class="tree-line"/>
        <rect x="626" y="145" width="128" height="32" class="leaf-box"/>
        <text x="690" y="165" class="leaf-text">5.1. Đọc mục tiêu &amp; kho</text>
        <rect x="626" y="190" width="128" height="32" class="leaf-box"/>
        <text x="690" y="210" class="leaf-text">5.2. Lập ràng buộc ±5%</text>
        <rect x="626" y="235" width="128" height="32" class="leaf-box"/>
        <text x="690" y="255" class="leaf-text">5.3. Giải bằng OR-Tools</text>
        <rect x="626" y="280" width="128" height="32" class="leaf-box"/>
        <text x="690" y="300" class="leaf-text">5.4. Xuất gram từng món</text>

        <!-- Group 6 -->
        <rect x="774" y="88" width="136" height="40" class="lvl1-box"/>
        <text x="842" y="105" class="lvl1-text">6. Thống kê</text>
        <text x="842" y="119" class="lvl1-text">&amp; Báo cáo</text>
        <line x1="842" y1="128" x2="842" y2="305" class="tree-line"/>
        <rect x="778" y="145" width="128" height="32" class="leaf-box"/>
        <text x="842" y="165" class="leaf-text">6.1. Tổng hợp Dashboard</text>
        <rect x="778" y="190" width="128" height="32" class="leaf-box"/>
        <text x="842" y="210" class="leaf-text">6.2. Đối chiếu đạt được</text>
        <rect x="778" y="235" width="128" height="32" class="leaf-box"/>
        <text x="842" y="255" class="leaf-text">6.3. Lịch sử mục tiêu</text>
        <rect x="778" y="280" width="128" height="32" class="leaf-box"/>
        <text x="842" y="300" class="leaf-text">6.4. Nhật ký bữa ăn</text>
    </svg>
    <div class="diagram-caption">Hình 2.1: Sơ đồ hình cây phân rã chức năng hệ thống (Business Function Diagram - BFD)</div>
</div>

<!-- ====================================================================== -->
<!-- SƠ ĐỒ 2: SƠ ĐỒ USE CASE & BẢNG ĐẶC TẢ                                  -->
<!-- ====================================================================== -->
<div class="page-break"></div>

<h2>2. Sơ Đồ Use Case Tổng Quát &amp; Bảng Đặc Tả Ca Sử Dụng</h2>
<p>
    Sơ đồ Use Case mô tả sự tương tác giữa <strong>2 tác nhân chính</strong> (<code>Admin</code> và <code>User / Member</code>) với các chức năng bên trong hệ thống <strong>SmartMacro Engine</strong>, bao gồm các quan hệ <code>&lt;&lt;include&gt;&gt;</code> (bắt buộc thực hiện kèm) và <code>&lt;&lt;extend&gt;&gt;</code> (mở rộng tùy chọn):
</p>

<div class="diagram-box no-break">
    <svg viewBox="0 0 880 430" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
        <defs>
            <marker id="arrow-open" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
                <path d="M0,1 L7,4 L0,7" fill="none" stroke="#1e40af" stroke-width="1.4"/>
            </marker>
            <style>
                .sys-boundary { fill: #f8fafc; stroke: #334155; stroke-width: 2; rx: 8; }
                .uc-ellipse { fill: #ffffff; stroke: #059669; stroke-width: 1.6; }
                .uc-ellipse-sub { fill: #eff6ff; stroke: #2563eb; stroke-width: 1.4; }
                .uc-text { fill: #0f172a; font-size: 10px; font-weight: 600; text-anchor: middle; }
                .actor-line { stroke: #0f172a; stroke-width: 2; fill: none; }
                .assoc-line { stroke: #334155; stroke-width: 1.4; fill: none; }
                .rel-line { stroke: #1e40af; stroke-width: 1.3; stroke-dasharray: 4,3; fill: none; marker-end: url(#arrow-open); }
                .rel-label { fill: #1e40af; font-size: 8.8px; font-weight: 700; text-anchor: middle; }
            </style>
        </defs>

        <!-- System Boundary -->
        <rect x="155" y="12" width="695" height="405" class="sys-boundary"/>
        <text x="502" y="34" font-size="12" font-weight="bold" fill="#0f172a" text-anchor="middle">HỆ THỐNG QUẢN LÝ &amp; TỐI ƯU DINH DƯỠNG SMARTMACRO ENGINE</text>

        <!-- Actor 1: User / Member (Top Left) -->
        <circle cx="65" cy="145" r="14" class="actor-line"/>
        <line x1="65" y1="159" x2="65" y2="200" class="actor-line"/>
        <line x1="40" y1="172" x2="90" y2="172" class="actor-line"/>
        <line x1="65" y1="200" x2="45" y2="230" class="actor-line"/>
        <line x1="65" y1="200" x2="85" y2="230" class="actor-line"/>
        <text x="65" y="248" font-size="11" font-weight="bold" fill="#065f46" text-anchor="middle">User / Member</text>
        <text x="65" y="262" font-size="9" fill="#475569" text-anchor="middle">(Người dùng / Hội viên)</text>

        <!-- Actor 2: Admin (Bottom Left) -->
        <circle cx="65" cy="315" r="14" class="actor-line"/>
        <line x1="65" y1="329" x2="65" y2="370" class="actor-line"/>
        <line x1="40" y1="342" x2="90" y2="342" class="actor-line"/>
        <line x1="65" y1="370" x2="45" y2="400" class="actor-line"/>
        <line x1="65" y1="370" x2="85" y2="400" class="actor-line"/>
        <text x="65" y="416" font-size="11" font-weight="bold" fill="#1e40af" text-anchor="middle">Admin (Quản trị viên)</text>

        <!-- Primary Use Cases (Column 1 inside boundary) -->
        <!-- UC1: Đăng ký / Đăng nhập -->
        <ellipse cx="320" cy="70" rx="115" ry="22" class="uc-ellipse"/>
        <text x="320" y="74" class="uc-text">UC01: Đăng ký &amp; Đăng nhập</text>

        <!-- UC2: Xem Dashboard & Thiết lập mục tiêu Macro -->
        <ellipse cx="320" cy="130" rx="125" ry="22" class="uc-ellipse"/>
        <text x="320" y="134" class="uc-text">UC02: Xem Dashboard &amp; Đặt mục tiêu</text>

        <!-- UC3: Quản lý Kho thực phẩm tủ lạnh -->
        <ellipse cx="320" cy="195" rx="125" ry="22" class="uc-ellipse"/>
        <text x="320" y="199" class="uc-text">UC03: Quản lý Kho tủ lạnh (Inventory)</text>

        <!-- UC4: Tính toán Thực đơn tối ưu -->
        <ellipse cx="320" cy="260" rx="125" ry="22" class="uc-ellipse"/>
        <text x="320" y="264" class="uc-text">UC04: Tính toán Thực đơn tối ưu</text>

        <!-- UC5: Quản lý Danh mục & Món ăn hệ thống -->
        <ellipse cx="320" cy="330" rx="125" ry="22" class="uc-ellipse"/>
        <text x="320" y="334" class="uc-text">UC05: Quản lý Danh mục &amp; Món ăn</text>

        <!-- UC6: Quản lý Người dùng -->
        <ellipse cx="320" cy="385" rx="115" ry="20" class="uc-ellipse"/>
        <text x="320" y="389" class="uc-text">UC06: Quản lý Tài khoản User</text>

        <!-- Included / Extended Sub Use Cases (Column 2 inside boundary) -->
        <!-- Sub 1: Xác thực JWT & Lưu Refresh Token -->
        <ellipse cx="690" cy="70" rx="125" ry="22" class="uc-ellipse-sub"/>
        <text x="690" y="74" class="uc-text">Cấp JWT &amp; Lưu Refresh Token</text>

        <!-- Sub 2: Tra cứu danh sách món ăn -->
        <ellipse cx="690" cy="180" rx="120" ry="22" class="uc-ellipse-sub"/>
        <text x="690" y="184" class="uc-text">Tra cứu món ăn (/api/foods)</text>

        <!-- Sub 3: Giải quy hoạch tuyến tính OR-Tools -->
        <ellipse cx="690" cy="245" rx="130" ry="22" class="uc-ellipse-sub"/>
        <text x="690" y="249" class="uc-text">Chạy bộ giải GLOP (OR-Tools)</text>

        <!-- Sub 4: Cảnh báo khi kho không đủ chất (Extend) -->
        <ellipse cx="690" cy="315" rx="130" ry="22" class="uc-ellipse-sub"/>
        <text x="690" y="319" class="uc-text">Báo lỗi Infeasible (Kho thiếu chất)</text>

        <!-- Associations from Actors -->
        <line x1="95" y1="160" x2="205" y2="70" class="assoc-line"/>
        <line x1="95" y1="165" x2="195" y2="130" class="assoc-line"/>
        <line x1="95" y1="175" x2="195" y2="195" class="assoc-line"/>
        <line x1="95" y1="185" x2="195" y2="260" class="assoc-line"/>

        <line x1="95" y1="330" x2="205" y2="75" class="assoc-line"/>
        <line x1="95" y1="340" x2="195" y2="330" class="assoc-line"/>
        <line x1="95" y1="355" x2="205" y2="385" class="assoc-line"/>

        <!-- <<include>> and <<extend>> relationships -->
        <!-- UC01 includes Cấp JWT -->
        <line x1="435" y1="70" x2="558" y2="70" class="rel-line"/>
        <text x="496" y="63" class="rel-label">&lt;&lt;include&gt;&gt;</text>

        <!-- UC03 includes Tra cứu món ăn -->
        <line x1="445" y1="192" x2="564" y2="182" class="rel-line"/>
        <text x="504" y="180" class="rel-label">&lt;&lt;include&gt;&gt;</text>

        <!-- UC04 includes Chạy bộ giải GLOP -->
        <line x1="445" y1="256" x2="554" y2="248" class="rel-line"/>
        <text x="500" y="245" class="rel-label">&lt;&lt;include&gt;&gt;</text>

        <!-- Báo lỗi Infeasible extends UC04 -->
        <line x1="560" y1="310" x2="438" y2="270" class="rel-line"/>
        <text x="505" y="302" class="rel-label">&lt;&lt;extend&gt;&gt;</text>
    </svg>
    <div class="diagram-caption">Hình 2.2: Sơ đồ Use Case tổng quát của hệ thống SmartMacro Engine</div>
</div>

<h3>Bảng Đặc Tả Ngắn Gọn 3 Use Case Chính Của Hệ Thống</h3>

<table class="no-break">
    <thead>
        <tr>
            <th style="width: 22%;">Thuộc tính</th>
            <th style="width: 78%;">Nội dung đặc tả — UC01: Đăng nhập hệ thống (Authentication)</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><strong>Tác nhân (Actor)</strong></td><td><code>User / Member</code> và <code>Admin</code></td></tr>
        <tr><td><strong>Điều kiện tiên quyết</strong></td><td>Người dùng đã có tài khoản trong bảng <code>users</code> (mật khẩu đã mã hóa BCrypt).</td></tr>
        <tr><td><strong>Luồng sự kiện chính</strong></td><td>1. Người dùng nhập Email và Mật khẩu trên trang <code>LoginPage</code> rồi bấm "Đăng nhập".<br/>2. Frontend gọi <code>POST /api/auth/login</code>.<br/>3. <code>AuthService</code> kiểm tra Email trong bảng <code>users</code> và đối chiếu mật khẩu bằng <code>BCrypt.Verify()</code>.<br/>4. Hệ thống sinh <code>AccessToken</code> (JWT 15 phút) và <code>RefreshToken</code> (7 ngày, lưu mã băm SHA-256 vào bảng <code>refresh_tokens</code>), trả về cho trình duyệt chuyển hướng vào trang <code>/dashboard</code>.</td></tr>
        <tr><td><strong>Luồng ngoại lệ</strong></td><td>Nếu sai Email hoặc Mật khẩu: Trả về mã lỗi <code>401 Unauthorized</code> và hiển thị thông báo trên form.</td></tr>
    </tbody>
</table>

<table class="no-break">
    <thead>
        <tr>
            <th style="width: 22%;">Thuộc tính</th>
            <th style="width: 78%;">Nội dung đặc tả — UC03: Quản lý kho thực phẩm cá nhân (Inventory Management)</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><strong>Tác nhân (Actor)</strong></td><td><code>User / Member</code> (Đã đăng nhập có JWT Token hợp lệ)</td></tr>
        <tr><td><strong>Điều kiện tiên quyết</strong></td><td>Danh mục món ăn hệ thống (<code>foods</code>) đã có dữ liệu thực phẩm.</td></tr>
        <tr><td><strong>Luồng sự kiện chính</strong></td><td>1. Người dùng mở tab "Thực phẩm &amp; Kho tủ lạnh", hệ thống gọi <code>GET /api/inventory</code> và <code>GET /api/foods</code>.<br/>2. Người dùng chọn một món ăn từ danh sách, nhập khối lượng hiện có (ví dụ: 500 gram) và ngày hết hạn, bấm "Thêm vào tủ lạnh".<br/>3. Hệ thống gọi <code>POST /api/inventory</code>. Nếu món ăn cùng hạn sử dụng đã có trong bảng <code>user_food_inventory</code> thì cộng dồn số gram; nếu chưa có thì thêm dòng mới.<br/>4. Người dùng có thể cập nhật số gram hoặc xóa món đã hết khỏi tủ lạnh (<code>PUT / DELETE /api/inventory/{id}</code>).</td></tr>
        <tr><td><strong>Luồng ngoại lệ</strong></td><td>Số lượng gram &le; 0 hoặc ngày hết hạn ở trong quá khứ: Hệ thống báo lỗi <code>400 Bad Request</code>.</td></tr>
    </tbody>
</table>

<table class="no-break">
    <thead>
        <tr>
            <th style="width: 22%;">Thuộc tính</th>
            <th style="width: 78%;">Nội dung đặc tả — UC04: Tính toán &amp; Gợi ý thực đơn tối ưu (Meal Optimization)</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><strong>Tác nhân (Actor)</strong></td><td><code>User / Member</code></td></tr>
        <tr><td><strong>Điều kiện tiên quyết</strong></td><td>Người dùng đã thiết lập mục tiêu hôm nay (<code>daily_targets</code>) và có ít nhất 1 thực phẩm còn hàng (&gt; 0g) trong <code>user_food_inventory</code>.</td></tr>
        <tr><td><strong>Luồng sự kiện chính</strong></td><td>1. Người dùng bấm nút <em>"Tính toán khẩu phần ăn tối ưu"</em> trên giao diện.<br/>2. Frontend gửi <code>POST /api/optimizations/generate-plan</code>.<br/>3. <code>OptimizationService</code> đọc mục tiêu hôm nay (Calo, P, C, F) và danh sách tồn kho thực tế của User.<br/>4. <code>MacroOptimizationEngine</code> khởi tạo bộ giải <code>GLOP</code> của Google OR-Tools, giải hệ phương trình tuyến tính tìm số gram mỗi món.<br/>5. Trả về danh sách các món cần lấy kèm số gram cụ thể và bảng đối chiếu Tổng đạt được so với Mục tiêu.</td></tr>
        <tr><td><strong>Luồng ngoại lệ (Extend)</strong></td><td>Nếu kho trống (<code>EmptyInventoryException</code>) hoặc tổng thực phẩm trong kho không thể ghép đủ chỉ số Protein/Carb/Fat trong biên độ &plusmn;5%: Trả về trạng thái <code>INFEASIBLE</code> nhắc người dùng bổ sung thêm thức ăn vào tủ lạnh.</td></tr>
    </tbody>
</table>

<!-- ====================================================================== -->
<!-- SƠ ĐỒ 3: SƠ ĐỒ ERD (ENTITY RELATIONSHIP DIAGRAM)                       -->
<!-- ====================================================================== -->
<div class="page-break"></div>

<h2>3. Sơ Đồ ERD (Entity Relationship Diagram — Sơ Đồ Quan Hệ Thực Thể)</h2>
<p>
    Sơ đồ ERD dưới đây được trích xuất chính xác 100% từ cấu hình Fluent API trong file <code>SmartMacro.Api/Models/SmartMacroDbContext.cs</code>. Tất cả khóa chính (<code>PK</code>), khóa ngoại (<code>FK</code>) và mối quan hệ <strong>Một - Nhiều (1 - N)</strong> đều được ký hiệu tường minh để dễ dàng giải thích khi vấn đáp:
</p>

<div class="diagram-box no-break">
    <svg viewBox="0 0 920 560" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" font-family="Consolas, 'Segoe UI', sans-serif">
        <defs>
            <style>
                .tbl-box { fill: #ffffff; stroke: #334155; stroke-width: 1.5; rx: 4; }
                .tbl-head { fill: #0f172a; }
                .tbl-head-core { fill: #065f46; }
                .tbl-title { fill: #ffffff; font-size: 10.5px; font-weight: bold; text-anchor: middle; font-family: 'Segoe UI', sans-serif; }
                .col-text { fill: #1e293b; font-size: 8.8px; }
                .pk-badge { fill: #b45309; font-weight: bold; font-size: 8.5px; }
                .fk-badge { fill: #1d4ed8; font-weight: bold; font-size: 8.5px; }
                .er-line { stroke: #475569; stroke-width: 1.4; fill: none; }
                .er-card { fill: #dc2626; font-size: 9.5px; font-weight: bold; font-family: 'Segoe UI', sans-serif; }
            </style>
        </defs>

        <!-- ================= COLUMN 1 (LEFT) ================= -->
        <!-- Table: refresh_tokens -->
        <rect x="15" y="15" width="235" height="108" class="tbl-box"/>
        <rect x="15" y="15" width="235" height="22" class="tbl-head"/>
        <text x="132" y="30" class="tbl-title">refresh_tokens (RefreshTokens)</text>
        <text x="23" y="50" class="col-text"><tspan class="pk-badge">PK</tspan> id : int</text>
        <text x="23" y="64" class="col-text"><tspan class="fk-badge">FK</tspan> user_id : bigint</text>
        <text x="23" y="78" class="col-text">   token (TokenHash) : varchar(128)</text>
        <text x="23" y="92" class="col-text">   expires_at : datetime2(3)</text>
        <text x="23" y="106" class="col-text">   revoked_at : datetime2(3) NULL</text>

        <!-- Table: food_categories -->
        <rect x="15" y="150" width="235" height="72" class="tbl-box"/>
        <rect x="15" y="150" width="235" height="22" class="tbl-head"/>
        <text x="132" y="165" class="tbl-title">food_categories (FoodCategories)</text>
        <text x="23" y="186" class="col-text"><tspan class="pk-badge">PK</tspan> category_id : smallint</text>
        <text x="23" y="202" class="col-text">   category_name : varchar(100) UQ</text>

        <!-- Table: foods -->
        <rect x="15" y="255" width="235" height="150" class="tbl-box"/>
        <rect x="15" y="255" width="235" height="22" class="tbl-head-core"/>
        <text x="132" y="270" class="tbl-title">foods (Foods)</text>
        <text x="23" y="290" class="col-text"><tspan class="pk-badge">PK</tspan> food_id : bigint</text>
        <text x="23" y="304" class="col-text"><tspan class="fk-badge">FK</tspan> category_id : smallint NULL</text>
        <text x="23" y="318" class="col-text"><tspan class="fk-badge">FK</tspan> created_by : bigint NULL</text>
        <text x="23" y="332" class="col-text">   food_name : varchar(200)</text>
        <text x="23" y="346" class="col-text">   kcal_per_100g : decimal(6,2)</text>
        <text x="23" y="360" class="col-text">   protein_g_per_100g : decimal(6,2)</text>
        <text x="23" y="374" class="col-text">   carbs_g_per_100g : decimal(6,2)</text>
        <text x="23" y="388" class="col-text">   fat_g_per_100g : decimal(6,2)</text>

        <!-- Table: user_body_metrics & activity_logs -->
        <rect x="15" y="430" width="235" height="115" class="tbl-box"/>
        <rect x="15" y="430" width="235" height="22" class="tbl-head"/>
        <text x="132" y="445" class="tbl-title">user_body_metrics &amp; activity_logs</text>
        <text x="23" y="465" class="col-text"><tspan class="pk-badge">PK</tspan> metric_id / activity_log_id : bigint</text>
        <text x="23" y="479" class="col-text"><tspan class="fk-badge">FK</tspan> user_id : bigint</text>
        <text x="23" y="493" class="col-text">   weight_kg, height_cm, bmr_kcal</text>
        <text x="23" y="507" class="col-text">   activity_name, duration_minutes</text>
        <text x="23" y="521" class="col-text">   kcal_burned : decimal(6,2)</text>

        <!-- ================= COLUMN 2 (CENTER CORE) ================= -->
        <!-- Table: users (Central Entity) -->
        <rect x="335" y="15" width="250" height="165" class="tbl-box"/>
        <rect x="335" y="15" width="250" height="22" class="tbl-head-core"/>
        <text x="460" y="30" class="tbl-title">users (Users — Bảng trung tâm)</text>
        <text x="343" y="50" class="col-text"><tspan class="pk-badge">PK</tspan> user_id : bigint</text>
        <text x="343" y="64" class="col-text">   email : varchar(255) UQ</text>
        <text x="343" y="78" class="col-text">   password_hash : char(60)</text>
        <text x="343" y="92" class="col-text">   full_name : varchar(150)</text>
        <text x="343" y="106" class="col-text">   date_of_birth : date</text>
        <text x="343" y="120" class="col-text">   biological_sex : varchar(10)</text>
        <text x="343" y="134" class="col-text">   activity_level : varchar(20)</text>
        <text x="343" y="148" class="col-text">   goal_type : varchar(20)</text>
        <text x="343" y="162" class="col-text">   status : varchar(20)</text>

        <!-- Table: user_food_inventory -->
        <rect x="335" y="235" width="250" height="130" class="tbl-box"/>
        <rect x="335" y="235" width="250" height="22" class="tbl-head-core"/>
        <text x="460" y="250" class="tbl-title">user_food_inventory (Kho Tủ Lạnh)</text>
        <text x="343" y="270" class="col-text"><tspan class="pk-badge">PK</tspan> inventory_id : bigint</text>
        <text x="343" y="284" class="col-text"><tspan class="fk-badge">FK</tspan> user_id : bigint</text>
        <text x="343" y="298" class="col-text"><tspan class="fk-badge">FK</tspan> food_id : bigint</text>
        <text x="343" y="312" class="col-text">   quantity_grams : decimal(8,2)</text>
        <text x="343" y="326" class="col-text">   expiry_date : date NULL</text>
        <text x="343" y="340" class="col-text">   unit_note : varchar(50) NULL</text>
        <text x="343" y="354" class="col-text">   updated_at : datetime2(3)</text>

        <!-- Table: meal_logs -->
        <rect x="335" y="405" width="250" height="140" class="tbl-box"/>
        <rect x="335" y="405" width="250" height="22" class="tbl-head"/>
        <text x="460" y="420" class="tbl-title">meal_logs (MealLogs)</text>
        <text x="343" y="440" class="col-text"><tspan class="pk-badge">PK</tspan> log_id : bigint</text>
        <text x="343" y="454" class="col-text"><tspan class="fk-badge">FK</tspan> user_id : bigint</text>
        <text x="343" y="468" class="col-text"><tspan class="fk-badge">FK</tspan> food_id : bigint</text>
        <text x="343" y="482" class="col-text"><tspan class="fk-badge">FK</tspan> inventory_id : bigint NULL</text>
        <text x="343" y="496" class="col-text">   log_date : date, meal_slot : varchar(20)</text>
        <text x="343" y="510" class="col-text">   consumed_grams : decimal(8,2)</text>
        <text x="343" y="524" class="col-text">   kcal/protein/carbs/fat_snapshot</text>

        <!-- ================= COLUMN 3 (RIGHT) ================= -->
        <!-- Table: daily_targets -->
        <rect x="660" y="15" width="245" height="145" class="tbl-box"/>
        <rect x="660" y="15" width="245" height="22" class="tbl-head-core"/>
        <text x="782" y="30" class="tbl-title">daily_targets (Mục tiêu Ngày)</text>
        <text x="668" y="50" class="col-text"><tspan class="pk-badge">PK</tspan> target_id : bigint</text>
        <text x="668" y="64" class="col-text"><tspan class="fk-badge">FK</tspan> user_id : bigint</text>
        <text x="668" y="78" class="col-text"><tspan class="fk-badge">FK</tspan> computed_from_rule_id : bigint NULL</text>
        <text x="668" y="92" class="col-text">   target_date : date (UQ với user_id)</text>
        <text x="668" y="106" class="col-text">   target_kcal : decimal(7,2)</text>
        <text x="668" y="120" class="col-text">   target_protein_g : decimal(6,2)</text>
        <text x="668" y="134" class="col-text">   target_carbs_g : decimal(6,2)</text>
        <text x="668" y="148" class="col-text">   target_fat_g : decimal(6,2)</text>

        <!-- Table: macro_adjustment_rules -->
        <rect x="660" y="200" width="245" height="130" class="tbl-box"/>
        <rect x="660" y="200" width="245" height="22" class="tbl-head"/>
        <text x="782" y="215" class="tbl-title">macro_adjustment_rules</text>
        <text x="668" y="235" class="col-text"><tspan class="pk-badge">PK</tspan> rule_id : bigint</text>
        <text x="668" y="249" class="col-text"><tspan class="fk-badge">FK</tspan> user_id : bigint</text>
        <text x="668" y="263" class="col-text"><tspan class="fk-badge">FK</tspan> cycle_type_id : smallint</text>
        <text x="668" y="277" class="col-text">   kcal_multiplier : decimal(4,3)</text>
        <text x="668" y="291" class="col-text">   protein_g_per_kg_bw : decimal(4,2)</text>
        <text x="668" y="305" class="col-text">   carb_ratio, fat_ratio : decimal(4,3)</text>

        <!-- Table: training_cycle_types -->
        <rect x="660" y="360" width="245" height="75" class="tbl-box"/>
        <rect x="660" y="360" width="245" height="22" class="tbl-head"/>
        <text x="782" y="375" class="tbl-title">training_cycle_types</text>
        <text x="668" y="395" class="col-text"><tspan class="pk-badge">PK</tspan> cycle_type_id : smallint</text>
        <text x="668" y="409" class="col-text">   type_code : varchar(20) UQ</text>
        <text x="668" y="423" class="col-text">   display_name : varchar(50)</text>

        <!-- Table: user_training_schedule -->
        <rect x="660" y="460" width="245" height="85" class="tbl-box"/>
        <rect x="660" y="460" width="245" height="22" class="tbl-head"/>
        <text x="782" y="475" class="tbl-title">user_training_schedule</text>
        <text x="668" y="495" class="col-text"><tspan class="pk-badge">PK</tspan> schedule_id : bigint</text>
        <text x="668" y="509" class="col-text"><tspan class="fk-badge">FK</tspan> user_id : bigint, <tspan class="fk-badge">FK</tspan> cycle_type_id : smallint</text>
        <text x="668" y="523" class="col-text">   schedule_date : date, is_completed : bit</text>

        <!-- ================= RELATIONSHIPS (1 - N LINES) ================= -->
        <!-- users (1) -> (N) refresh_tokens -->
        <line x1="335" y1="60" x2="250" y2="60" class="er-line"/>
        <text x="323" y="55" class="er-card">1</text>
        <text x="256" y="55" class="er-card">N</text>

        <!-- food_categories (1) -> (N) foods -->
        <line x1="132" y1="222" x2="132" y2="255" class="er-line"/>
        <text x="138" y="234" class="er-card">1</text>
        <text x="138" y="251" class="er-card">N</text>

        <!-- foods (1) -> (N) user_food_inventory -->
        <line x1="250" y1="300" x2="335" y2="300" class="er-line"/>
        <text x="256" y="295" class="er-card">1</text>
        <text x="322" y="295" class="er-card">N</text>

        <!-- users (1) -> (N) user_food_inventory -->
        <line x1="460" y1="180" x2="460" y2="235" class="er-line"/>
        <text x="466" y="193" class="er-card">1</text>
        <text x="466" y="230" class="er-card">N</text>

        <!-- user_food_inventory (1) -> (N) meal_logs -->
        <line x1="460" y1="365" x2="460" y2="405" class="er-line"/>
        <text x="466" y="378" class="er-card">1</text>
        <text x="466" y="401" class="er-card">N</text>

        <!-- foods (1) -> (N) meal_logs -->
        <polyline points="250,365 290,365 290,468 335,468" class="er-line"/>
        <text x="256" y="360" class="er-card">1</text>
        <text x="322" y="463" class="er-card">N</text>

        <!-- users (1) -> (N) daily_targets -->
        <line x1="585" y1="60" x2="660" y2="60" class="er-line"/>
        <text x="592" y="55" class="er-card">1</text>
        <text x="647" y="55" class="er-card">N</text>

        <!-- macro_adjustment_rules (1) -> (N) daily_targets -->
        <line x1="782" y1="200" x2="782" y2="160" class="er-line"/>
        <text x="788" y="195" class="er-card">1</text>
        <text x="788" y="172" class="er-card">N</text>

        <!-- users (1) -> (N) macro_adjustment_rules -->
        <polyline points="585,130 625,130 625,245 660,245" class="er-line"/>
        <text x="592" y="125" class="er-card">1</text>
        <text x="647" y="240" class="er-card">N</text>

        <!-- training_cycle_types (1) -> (N) macro_adjustment_rules -->
        <line x1="782" y1="360" x2="782" y2="330" class="er-line"/>
        <text x="788" y="355" class="er-card">1</text>
        <text x="788" y="342" class="er-card">N</text>

        <!-- training_cycle_types (1) -> (N) user_training_schedule -->
        <line x1="782" y1="435" x2="782" y2="460" class="er-line"/>
        <text x="788" y="446" class="er-card">1</text>
        <text x="788" y="457" class="er-card">N</text>

        <!-- users (1) -> (N) user_body_metrics / activity_logs -->
        <polyline points="335,140 295,140 295,480 250,480" class="er-line"/>
        <text x="323" y="135" class="er-card">1</text>
        <text x="256" y="475" class="er-card">N</text>
    </svg>
    <div class="diagram-caption">Hình 2.3: Sơ đồ Quan hệ Thực thể (ERD) trích xuất từ SmartMacroDbContext.cs</div>
</div>

<h3>Giải Thích Nhanh Các Quan Hệ Khóa Ngoại (1 - N) Để Trả Lời Vấn Đáp</h3>
<ul>
    <li><strong><code>users (1) &mdash; (N) refresh_tokens</code>:</strong> Một người dùng có thể đăng nhập trên nhiều phiên/thiết bị; khi xóa user sẽ tự động xóa (Cascade) các Refresh Token của user đó.</li>
    <li><strong><code>food_categories (1) &mdash; (N) foods</code>:</strong> Một nhóm thực phẩm (VD: "Thịt &amp; Hải sản") chứa nhiều món ăn (Ức gà, Thịt bò, Cá hồi...). Khóa ngoại <code>category_id</code> đặt chế độ <code>SetNull</code> khi xóa danh mục để không làm mất dữ liệu món ăn.</li>
    <li><strong><code>users (1) &mdash; (N) user_food_inventory</code> và <code>foods (1) &mdash; (N) user_food_inventory</code>:</strong> Bảng <code>user_food_inventory</code> là bảng trung gian lưu trữ kho tủ lạnh của từng người dùng. Cặp khóa <code>(user_id, food_id, expiry_date)</code> được đánh Unique Index để nếu người dùng nhập trùng món ăn có cùng ngày hết hạn thì hệ thống tự cộng dồn số gram.</li>
    <li><strong><code>users (1) &mdash; (N) daily_targets</code>:</strong> Mỗi ngày một người dùng có đúng 1 bản ghi mục tiêu dinh dưỡng nhờ ràng buộc duy nhất <code>UQ_target_user_date (user_id, target_date)</code>.</li>
    <li><strong><code>training_cycle_types (1) &mdash; (N) user_training_schedule / macro_adjustment_rules</code>:</strong> Cho phép mở rộng bài toán theo lịch tập (Push, Pull, Legs, Rest Day) để điều chỉnh hệ số Calo và tỷ lệ Macro tương ứng.</li>
</ul>

<!-- ====================================================================== -->
<!-- PHẦN 3: GIẢI THUẬT OR-TOOLS & GIAO DIỆN WEB DEMO                       -->
<!-- ====================================================================== -->
<div class="page-break"></div>

<h1>PHẦN 3: GIẢI THÍCH THUẬT TOÁN QUY HOẠCH TUYẾN TÍNH &amp; GIAO DIỆN WEB DEMO</h1>

<h2>1. Giải Thích Giải Thuật Quy Hoạch Tuyến Tính (Google OR-Tools) Trong Code</h2>
<p>
    Trái tim của hệ thống nằm ở file <code>SmartMacro.Api/Engines/MacroOptimizationEngine.cs</code>. Thay vì dùng vòng lặp thử-sai ngẫu nhiên, hệ thống mô hình hóa bài toán tính khẩu phần ăn thành hệ phương trình <strong>Quy hoạch Tuyến tính (Linear Programming - LP)</strong> và giải bằng bộ giải <code>GLOP</code> của Google OR-Tools qua 4 bước rất dễ hiểu:
</p>

<table>
    <thead>
        <tr>
            <th style="width: 20%;">Bước xử lý</th>
            <th style="width: 38%;">Công thức toán học</th>
            <th style="width: 42%;">Giải thích gắn với dòng code C# thực tế</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Bước 1: Gọi biến quyết định</strong></td>
            <td>\(0 \le \text{grams}_i \le \text{QuantityGrams}_i\)<br/>(với \(i = 1 \dots n\) món trong tủ lạnh)</td>
            <td>Mỗi món ăn thứ \(i\) trong kho được tạo một biến liên tục bằng hàm <code>solver.MakeNumVar(0.0, inventory[i].QuantityGrams)</code>. Nghĩa là số gram lấy ra không thể âm và không được vượt quá số gram đang có trong tủ lạnh.</td>
        </tr>
        <tr>
            <td><strong>Bước 2: Ràng buộc 3 chất P, C, F (&plusmn;5%)</strong></td>
            <td>\(0.95 \cdot T \le \sum_{i=1}^{n} \text{grams}_i \cdot \frac{\text{MacroPer100g}_i}{100} \le 1.05 \cdot T\)</td>
            <td>Hàm <code>AddMacroConstraint()</code> thiết lập ngưỡng dưới (<code>target * 0.95</code>) và ngưỡng trên (<code>target * 1.05</code>) cho cả 3 chất: <strong>Protein, Carbs, Fat</strong>. Ví dụ mục tiêu là 160g Protein thì tổng Protein của các món cộng lại bắt buộc nằm từ 152g đến 168g.</td>
        </tr>
        <tr>
            <td><strong>Bước 3: Hàm mục tiêu (Giảm lệch Calo)</strong></td>
            <td>\(\text{Minimize } \text{deviation}\)<br/>sao cho \(\text{deviation} \ge |\text{TotalKcal} - \text{TargetKcal}|\)</td>
            <td>Ta muốn tổng Calo thực tế sát với Calo mục tiêu nhất. Vì Quy hoạch tuyến tính không dùng trực tiếp dấu giá trị tuyệt đối \(|x|\), code dùng 1 biến phụ <code>deviation &ge; 0</code> với 2 ràng buộc kẹp trên và kẹp dưới (<code>kcalUpperDev</code> và <code>kcalLowerDev</code>) rồi gọi <code>objective.SetMinimization()</code>.</td>
        </tr>
        <tr>
            <td><strong>Bước 4: Giải &amp; Lọc kết quả</strong></td>
            <td><code>status = solver.Solve()</code><br/>Loại bỏ nhiễu số học <code>&lt; 0.5g</code></td>
            <td>Nếu <code>status == OPTIMAL</code> hoặc <code>FEASIBLE</code>, hệ thống lấy <code>grams[i].SolutionValue()</code> (làm tròn 2 chữ số thập phân) trả về cho người dùng. Các món có nghiệm &lt; 0.5g sẽ được bỏ qua để thực đơn gọn gàng.</td>
        </tr>
    </tbody>
</table>

<h2>2. Thiết Kế Giao Diện Sản Phẩm Thực Tế (`SmartMacro.Web`) Phục Vụ Demo</h2>
<p>
    Giao diện Front-end tại <code>SmartMacro.Web</code> được tinh gọn, tập trung vào <strong>3 màn hình cốt lõi nhất</strong> cùng nút <strong>"Nạp dữ liệu mẫu (Demo Seed)"</strong> để quá trình báo cáo và demo trực tiếp trước giảng viên diễn ra mạch lạc:
</p>

<div class="callout">
    <strong>1. Màn hình 1 — Tổng quan &amp; Mục tiêu (Dashboard &amp; Daily Target):</strong>
    Hiển thị 4 thẻ chỉ số mục tiêu hôm nay (Calo, Protein, Carbs, Fat) thông qua API <code>GET /api/daily-targets/today</code> và <code>GET /api/dashboard/summary</code>. Tích hợp sẵn biểu mẫu (Form) cho phép người dùng nhập mới hoặc cập nhật nhanh mục tiêu dinh dưỡng trong ngày (<code>POST / PUT /api/daily-targets</code>).
</div>

<div class="callout">
    <strong>2. Màn hình 2 — Thực phẩm &amp; Kho tủ lạnh (Foods &amp; Inventory):</strong>
    Hiển thị bảng danh sách các thực phẩm đang có trong tủ lạnh cá nhân (<code>GET /api/inventory</code>) kèm khối lượng tồn (gram), chỉ số dinh dưỡng trên 100g và ngày hết hạn. Đi kèm form chọn món ăn từ danh mục hệ thống (<code>GET /api/foods</code>) hoặc tạo món mới để thêm nhanh vào tủ lạnh.
</div>

<div class="callout">
    <strong>3. Màn hình 3 — Gợi ý Thực đơn Tối ưu (Meal Optimizer):</strong>
    Cung cấp nút bấm <em>"Tính toán khẩu phần ăn tối ưu"</em> gọi trực tiếp tới <code>POST /api/optimizations/generate-plan</code>. Kết quả trả về hiển thị trực quan: Trạng thái bộ giải (<code>OPTIMAL</code>), bảng đối chiếu Mục tiêu vs. Đạt được (kèm % hoàn thành), và danh sách cụ thể cần lấy món nào trong tủ lạnh với bao nhiêu gram.
</div>

<div class="callout callout-green">
    <strong>4. Nút "Nạp dữ liệu mẫu (Demo Seed)" trên góc giao diện:</strong>
    Khi bấm vào nút này, hệ thống tự động khởi tạo 5 món ăn quen thuộc với sinh viên và người tập Gym Việt Nam (<strong>Ức gà phi lê, Cơm trắng, Trứng gà nguyên quả, Khoai lang luộc, Bông cải xanh</strong>), nạp sẵn số lượng vào kho tủ lạnh cá nhân và đặt mục tiêu mẫu (<strong>2200 kcal, 160g Protein, 250g Carbs, 60g Fat</strong>) để có thể bấm chạy thuật toán tối ưu ra kết quả ngay lập tức khi lên bảng bảo vệ.
</div>

</body>
</html>
"""


def main():
    print("================================================================")
    print("SmartMacro Engine - Building Academic Report (Buoi 4/10)...")
    print("================================================================")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    report_pdf_path = os.path.join(script_dir, "SmartMacro_Architectural_Report.pdf")
    root_pdf_path = os.path.join(repo_root, "SmartMacro_Architectural_Report.pdf")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as tmp_html:
        html_path = tmp_html.name
        html_content = build_report_html()
        tmp_html.write(html_content)

    print(f"[1/3] Generated temporary HTML at: {html_path} ({len(html_content):,} bytes)")

    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    ]
    browser_exe = None
    for p in chrome_paths:
        if os.path.exists(p):
            browser_exe = p
            break

    if not browser_exe:
        print("[ERROR] Neither Chrome nor Edge executable was found.")
        sys.exit(1)

    print(f"[2/3] Compiling PDF via headless browser: {browser_exe}...")
    file_url = "file:///" + html_path.replace("\\", "/")

    if os.path.exists(report_pdf_path):
        os.remove(report_pdf_path)

    cmd = [
        browser_exe,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={report_pdf_path}",
        file_url
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[WARNING] Browser command returned code {result.returncode}: {result.stderr}")

    success = False
    for _ in range(15):
        if os.path.exists(report_pdf_path) and os.path.getsize(report_pdf_path) > 1000:
            success = True
            break
        time.sleep(1)

    # Clean up temporary HTML file so repo stays clean
    if os.path.exists(html_path):
        os.remove(html_path)

    if success:
        shutil.copy2(report_pdf_path, root_pdf_path)
        pdf_size = os.path.getsize(report_pdf_path)
        print(f"[3/3] PDF compilation SUCCEEDED!")
        print(f" -> Report path: {report_pdf_path}")
        print(f" -> Copied to root: {root_pdf_path}")
        print(f" -> Size: {pdf_size:,} bytes ({pdf_size / 1024:.1f} KB)")
    else:
        print(f"[ERROR] PDF generation failed or timed out. Output: {result.stdout} / {result.stderr}")
        sys.exit(1)


if __name__ == "__main__":
    main()
