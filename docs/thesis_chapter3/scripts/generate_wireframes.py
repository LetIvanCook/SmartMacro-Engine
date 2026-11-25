# -*- coding: utf-8 -*-
"""
SmartMacro Engine - Sinh bộ giao diện Wireframe chuẩn Figma (Figma-Ready SVG)
Định dạng SVG vector độ phân giải 1440x900 chuẩn Khoa CNTT - STU:
- fig_3_8_wireframe_auth.svg: Màn hình Đăng nhập & Đăng ký tài khoản
- fig_3_9_wireframe_dashboard.svg: Màn hình Tổng quan dinh dưỡng & Thiết lập DailyTargets
- fig_3_10_wireframe_inventory.svg: Màn hình Quản lý Kho thực phẩm tủ lạnh cá nhân & Cảnh báo hạn dùng
- fig_3_11_wireframe_optimizer.svg: Màn hình Tối ưu hóa khẩu phần ăn thông minh với Google OR-Tools
"""

import os
import html

WIREFRAMES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "wireframes"))
os.makedirs(WIREFRAMES_DIR, exist_ok=True)

# Common SVG Defs for Wireframes
WF_DEFS = """
  <defs>
    <!-- Drop shadows -->
    <filter id="wf-shadow" x="-3%" y="-3%" width="106%" height="108%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.08" />
    </filter>
    <filter id="modal-shadow" x="-10%" y="-10%" width="120%" height="120%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="-4" dy="4" stdDeviation="12" flood-color="#000000" flood-opacity="0.18" />
    </filter>
    <filter id="callout-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#000000" flood-opacity="0.3" />
    </filter>
  </defs>
"""

def draw_callout(cx, cy, number):
    """Draws a numbered callout marker (1), (2), (3)..."""
    return f"""
    <g id="callout-{number}" filter="url(#callout-glow)">
      <circle cx="{cx}" cy="{cy}" r="15" fill="#E11D48" stroke="#FFFFFF" stroke-width="2.5" />
      <text x="{cx}" y="{cy+5}" font-family="Arial, sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#FFFFFF">{number}</text>
    </g>
    """

# ==============================================================================
# 1. FIG 3.8: WIREFRAME AUTH (LOGIN & REGISTER)
# ==============================================================================
def generate_wireframe_auth():
    w, h = 1440, 900
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        f'  <title>Hình 3-8: Wireframe Màn hình Đăng nhập &amp; Đăng ký — SmartMacro Engine</title>',
        WF_DEFS,
        f'  <rect width="{w}" height="{h}" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2" />',

        # --- LEFT BRAND HERO PANEL (x: 0, w: 580, h: 900) ---
        f'  <g id="hero-brand-panel">',
        f'    <rect x="0" y="0" width="580" height="{h}" fill="#0F172A" />',
        # Subtle decor shapes
        f'    <circle cx="120" cy="180" r="280" fill="#1E293B" fill-opacity="0.4" />',
        f'    <circle cx="500" cy="750" r="220" fill="#1E293B" fill-opacity="0.4" />',

        # Brand Logo & Title
        f'    <rect x="70" y="80" width="46" height="46" rx="10" fill="#10B981" />',
        f'    <text x="93" y="110" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle" fill="#FFFFFF">⚡</text>',
        f'    <text x="130" y="105" font-family="Times New Roman, Arial" font-size="26" font-weight="bold" fill="#FFFFFF">SmartMacro Engine</text>',
        f'    <text x="132" y="125" font-family="Arial, sans-serif" font-size="12" fill="#94A3B8" letter-spacing="1">NUTRITION &amp; INVENTORY OPTIMIZER</text>',

        # Headline
        f'    <text x="70" y="210" font-family="Times New Roman, Arial" font-size="28" font-weight="bold" fill="#F8FAFC">Tối ưu hóa Khẩu phần ăn</text>',
        f'    <text x="70" y="246" font-family="Times New Roman, Arial" font-size="28" font-weight="bold" fill="#34D399">Theo Chu kỳ Tập luyện</text>',
        f'    <text x="70" y="285" font-family="Times New Roman, Arial" font-size="14" fill="#94A3B8">Ứng dụng giải thuật Quy hoạch tuyến tính (Google OR-Tools GLOP)</text>',
        f'    <text x="70" y="305" font-family="Times New Roman, Arial" font-size="14" fill="#94A3B8">kết hợp quản lý kho thực phẩm tủ lạnh cá nhân chống lãng phí.</text>',

        # Feature Highlights Cards
        # Feature 1
        f'    <rect x="70" y="350" width="440" height="90" rx="8" fill="#1E293B" stroke="#334155" stroke-width="1.2" />',
        f'    <circle cx="105" cy="395" r="20" fill="#047857" />',
        f'    <text x="105" y="401" font-family="Arial" font-size="16" text-anchor="middle" fill="#FFFFFF">🎯</text>',
        f'    <text x="140" y="385" font-family="Times New Roman, Arial" font-size="15" font-weight="bold" fill="#FFFFFF">Tính toán Macro chính xác đến từng gram</text>',
        f'    <text x="140" y="408" font-family="Times New Roman, Arial" font-size="12.5" fill="#94A3B8">Giải bài toán LP đa ràng buộc Protein, Carbs, Fat (±5%)</text>',
        f'    <text x="140" y="425" font-family="Times New Roman, Arial" font-size="12.5" fill="#94A3B8">và tối thiểu hóa sai lệch Calo mục tiêu.</text>',

        # Feature 2
        f'    <rect x="70" y="460" width="440" height="90" rx="8" fill="#1E293B" stroke="#334155" stroke-width="1.2" />',
        f'    <circle cx="105" cy="505" r="20" fill="#0369A1" />',
        f'    <text x="105" y="511" font-family="Arial" font-size="16" text-anchor="middle" fill="#FFFFFF">🥦</text>',
        f'    <text x="140" y="495" font-family="Times New Roman, Arial" font-size="15" font-weight="bold" fill="#FFFFFF">Tủ lạnh thông minh &amp; Cảnh báo hạn dùng</text>',
        f'    <text x="140" y="518" font-family="Times New Roman, Arial" font-size="12.5" fill="#94A3B8">Theo dõi chính xác hạn sử dụng của từng thực phẩm,</text>',
        f'    <text x="140" y="535" font-family="Times New Roman, Arial" font-size="12.5" fill="#94A3B8">ưu tiên đưa nguyên liệu sắp hết hạn vào thực đơn nấu.</text>',

        # Feature 3
        f'    <rect x="70" y="570" width="440" height="90" rx="8" fill="#1E293B" stroke="#334155" stroke-width="1.2" />',
        f'    <circle cx="105" cy="615" r="20" fill="#7C3AED" />',
        f'    <text x="105" y="621" font-family="Arial" font-size="16" text-anchor="middle" fill="#FFFFFF">🔒</text>',
        f'    <text x="140" y="605" font-family="Times New Roman, Arial" font-size="15" font-weight="bold" fill="#FFFFFF">Bảo mật chuẩn JWT &amp; Refresh Token Rotation</text>',
        f'    <text x="140" y="628" font-family="Times New Roman, Arial" font-size="12.5" fill="#94A3B8">Mã hóa mật khẩu BCrypt, phòng chống tấn công dò quét</text>',
        f'    <text x="140" y="645" font-family="Times New Roman, Arial" font-size="12.5" fill="#94A3B8">bằng chính sách Rate Limiting tại tầng API Middleware.</text>',

        # Academic Footer in Hero
        f'    <text x="70" y="820" font-family="Times New Roman, Arial" font-size="12" fill="#64748B">ĐỒ ÁN TỐT NGHIỆP / THỰC TẬP CHUYÊN NGÀNH CNTT</text>',
        f'    <text x="70" y="840" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#94A3B8">TRƯỜNG ĐẠI HỌC CÔNG NGHỆ SÀI GÒN (STU) — KHOA CNTT</text>',
        f'  </g>',

        # --- RIGHT AUTH FORM AREA (x: 580 -> 1440) ---
        f'  <g id="auth-form-container">',
        # Centered Card (w: 520, h: 760, centered at x: 980)
        f'    <rect x="730" y="70" width="540" height="760" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#wf-shadow)" />',

        # Tab Switcher: [ Đăng nhập ] [ Đăng ký ]
        f'    <g id="tab-switcher">',
        f'      <rect x="760" y="105" width="480" height="46" rx="8" fill="#F1F5F9" />',
        # Tab Active (Đăng nhập)
        f'      <rect x="764" y="109" width="236" height="38" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" filter="url(#wf-shadow)" />',
        f'      <text x="882" y="133" font-family="Times New Roman, Arial" font-size="14.5" font-weight="bold" text-anchor="middle" fill="#0F172A">Đăng nhập tài khoản</text>',
        # Tab Inactive (Đăng ký)
        f'      <text x="1122" y="133" font-family="Times New Roman, Arial" font-size="14.5" font-weight="normal" text-anchor="middle" fill="#64748B">Đăng ký thành viên</text>',
        f'    </g>',

        # Welcome text
        f'    <text x="760" y="185" font-family="Times New Roman, Arial" font-size="18" font-weight="bold" fill="#0F172A">Chào mừng quay trở lại!</text>',
        f'    <text x="760" y="208" font-family="Times New Roman, Arial" font-size="13" fill="#64748B">Vui lòng nhập email và mật khẩu của bạn để truy cập hệ thống.</text>',

        # Field 1: Email
        f'    <g id="field-email">',
        f'      <text x="760" y="248" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#334155">Địa chỉ Email <tspan fill="#DC2626">*</tspan></text>',
        f'      <rect x="760" y="258" width="480" height="44" rx="6" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.2" />',
        f'      <text x="775" y="285" font-family="Arial, sans-serif" font-size="13.5" fill="#0F172A">nguyen.van.an@smartmacro.vn</text>',
        f'      <circle cx="1215" cy="280" r="9" fill="#10B981" />',
        f'      <text x="1215" y="284" font-family="Arial" font-size="10" font-weight="bold" text-anchor="middle" fill="#FFFFFF">✓</text>',
        f'    </g>',

        # Field 2: Password
        f'    <g id="field-password">',
        f'      <text x="760" y="332" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#334155">Mật khẩu <tspan fill="#DC2626">*</tspan></text>',
        f'      <rect x="760" y="342" width="480" height="44" rx="6" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.2" />',
        f'      <text x="775" y="370" font-family="Arial, sans-serif" font-size="16" fill="#0F172A">••••••••••••••••</text>',
        f'      <text x="1215" y="369" font-family="Arial" font-size="14" text-anchor="middle" fill="#64748B">👁</text>',
        f'    </g>',

        # Remember & Forgot Password
        f'    <g id="options-row">',
        f'      <rect x="760" y="405" width="16" height="16" rx="3" fill="#2563EB" />',
        f'      <text x="768" y="417" font-family="Arial" font-size="11" font-weight="bold" text-anchor="middle" fill="#FFFFFF">✓</text>',
        f'      <text x="785" y="418" font-family="Times New Roman, Arial" font-size="13" fill="#334155">Duy trì đăng nhập (Refresh Token 7 ngày)</text>',
        f'      <text x="1240" y="418" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" text-anchor="end" fill="#2563EB">Quên mật khẩu?</text>',
        f'    </g>',

        # Primary Action Button
        f'    <g id="btn-login-submit">',
        f'      <rect x="760" y="445" width="480" height="48" rx="6" fill="#1E293B" stroke="#0F172A" stroke-width="1" filter="url(#wf-shadow)" />',
        f'      <text x="1000" y="475" font-family="Times New Roman, Arial" font-size="15" font-weight="bold" text-anchor="middle" fill="#FFFFFF">ĐĂNG NHẬP VÀO HỆ THỐNG</text>',
        f'    </g>',

        # Divider
        f'    <line x1="760" y1="520" x2="1240" y2="520" stroke="#E2E8F0" stroke-width="1" />',
        f'    <rect x="910" y="511" width="180" height="18" fill="#FFFFFF" />',
        f'    <text x="1000" y="524" font-family="Times New Roman, Arial" font-size="12" text-anchor="middle" fill="#94A3B8">HOẶC THÔNG TIN ĐĂNG KÝ MỚI</text>',

        # Mini Register Fields Preview (Sub-form in same wireframe to demonstrate UC02 & UC03)
        f'    <g id="register-fields-preview">',
        f'      <rect x="760" y="545" width="480" height="215" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1" />',
        f'      <text x="775" y="568" font-family="Times New Roman, Arial" font-size="12.5" font-weight="bold" fill="#475569">Thông số nhân trắc học khởi tạo (Dành cho thành viên mới):</text>',

        # Row 1: FullName & BiologicalSex
        f'      <text x="775" y="595" font-family="Times New Roman, Arial" font-size="11.5" fill="#64748B">Họ và tên:</text>',
        f'      <rect x="775" y="602" width="220" height="32" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />',
        f'      <text x="785" y="623" font-family="Arial" font-size="12" fill="#0F172A">Nguyễn Văn An</text>',

        f'      <text x="1015" y="595" font-family="Times New Roman, Arial" font-size="11.5" fill="#64748B">Giới tính sinh học:</text>',
        f'      <rect x="1015" y="602" width="210" height="32" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />',
        f'      <text x="1025" y="623" font-family="Arial" font-size="12" fill="#0F172A">Nam (Male) ▾</text>',

        # Row 2: ActivityLevel & GoalType
        f'      <text x="775" y="655" font-family="Times New Roman, Arial" font-size="11.5" fill="#64748B">Mức độ vận động (Activity Level):</text>',
        f'      <rect x="775" y="662" width="220" height="32" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />',
        f'      <text x="785" y="683" font-family="Arial" font-size="12" fill="#0F172A">Moderate (3-5 buổi/tuần) ▾</text>',

        f'      <text x="1015" y="655" font-family="Times New Roman, Arial" font-size="11.5" fill="#64748B">Mục tiêu thể hình (Goal Type):</text>',
        f'      <rect x="1015" y="662" width="210" height="32" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />',
        f'      <text x="1025" y="683" font-family="Arial" font-size="12" fill="#0F172A">Tăng cơ (Hypertrophy) ▾</text>',

        # Register Action Button
        f'      <rect x="775" y="710" width="450" height="36" rx="5" fill="#FFFFFF" stroke="#2563EB" stroke-width="1.5" />',
        f'      <text x="1000" y="733" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" text-anchor="middle" fill="#2563EB">+ ĐĂNG KÝ TÀI KHOẢN MỚI &amp; THIẾT LẬP HỒ SƠ</text>',
        f'    </g>',

        # Security footer notice
        f'    <text x="1000" y="795" font-family="Times New Roman, Arial" font-size="11" text-anchor="middle" fill="#94A3B8">Hệ thống áp dụng chính sách Rate Limit 5 req/phút tại /api/auth/login để ngăn chặn Brute-force.</text>',
        f'  </g>',

        # --- CALLOUT MARKERS ---
        draw_callout(290, 115, 1),
        draw_callout(882, 110, 2),
        draw_callout(1215, 275, 3),
        draw_callout(770, 415, 4),
        draw_callout(1000, 465, 5),
        draw_callout(1210, 615, 6),

        f'</svg>'
    ]

    out_path = os.path.join(WIREFRAMES_DIR, "fig_3_8_wireframe_auth.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated Wireframe: {out_path}")

# ==============================================================================
# 2. FIG 3.9: WIREFRAME DASHBOARD & DAILY TARGETS
# ==============================================================================
def generate_wireframe_dashboard():
    w, h = 1440, 900
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        f'  <title>Hình 3-9: Wireframe Màn hình Tổng quan Dinh dưỡng (Dashboard) — SmartMacro Engine</title>',
        WF_DEFS,
        f'  <rect width="{w}" height="{h}" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2" />',

        # --- SIDEBAR (w: 240, h: 900, bg: #0F172A) ---
        f'  <g id="sidebar">',
        f'    <rect x="0" y="0" width="240" height="{h}" fill="#0F172A" />',
        # Logo
        f'    <rect x="24" y="24" width="36" height="36" rx="8" fill="#10B981" />',
        f'    <text x="42" y="48" font-family="Arial" font-size="20" font-weight="bold" text-anchor="middle" fill="#FFFFFF">⚡</text>',
        f'    <text x="70" y="42" font-family="Times New Roman, Arial" font-size="18" font-weight="bold" fill="#FFFFFF">SmartMacro</text>',
        f'    <text x="72" y="56" font-family="Arial" font-size="10" fill="#94A3B8" letter-spacing="1">ENGINE v1.0</text>',
        f'    <line x1="24" y1="80" x2="216" y2="80" stroke="#1E293B" stroke-width="1" />',

        # Nav items
        # 1. Dashboard (Active)
        f'    <rect x="16" y="100" width="208" height="42" rx="6" fill="#1E293B" stroke="#334155" stroke-width="1" />',
        f'    <text x="36" y="126" font-family="Arial" font-size="14" fill="#10B981">📊</text>',
        f'    <text x="64" y="126" font-family="Times New Roman, Arial" font-size="14" font-weight="bold" fill="#FFFFFF">Tổng quan dinh dưỡng</text>',

        # 2. Inventory
        f'    <rect x="16" y="152" width="208" height="42" rx="6" fill="transparent" />',
        f'    <text x="36" y="178" font-family="Arial" font-size="14" fill="#94A3B8">🥦</text>',
        f'    <text x="64" y="178" font-family="Times New Roman, Arial" font-size="14" fill="#94A3B8">Tủ lạnh cá nhân</text>',

        # 3. Optimizer
        f'    <rect x="16" y="204" width="208" height="42" rx="6" fill="transparent" />',
        f'    <text x="36" y="230" font-family="Arial" font-size="14" fill="#94A3B8">⚡</text>',
        f'    <text x="64" y="230" font-family="Times New Roman, Arial" font-size="14" fill="#94A3B8">Tối ưu hóa thực đơn</text>',

        # 4. Meal Log
        f'    <rect x="16" y="256" width="208" height="42" rx="6" fill="transparent" />',
        f'    <text x="36" y="282" font-family="Arial" font-size="14" fill="#94A3B8">📖</text>',
        f'    <text x="64" y="282" font-family="Times New Roman, Arial" font-size="14" fill="#94A3B8">Nhật ký bữa ăn</text>',

        # 5. Training Schedule
        f'    <rect x="16" y="308" width="208" height="42" rx="6" fill="transparent" />',
        f'    <text x="36" y="334" font-family="Arial" font-size="14" fill="#94A3B8">🏋️</text>',
        f'    <text x="64" y="334" font-family="Times New Roman, Arial" font-size="14" fill="#94A3B8">Lịch chu kỳ tập</text>',

        # 6. Settings
        f'    <rect x="16" y="360" width="208" height="42" rx="6" fill="transparent" />',
        f'    <text x="36" y="386" font-family="Arial" font-size="14" fill="#94A3B8">⚙️</text>',
        f'    <text x="64" y="386" font-family="Times New Roman, Arial" font-size="14" fill="#94A3B8">Hồ sơ &amp; Cài đặt</text>',

        # User Profile Box bottom
        f'    <rect x="16" y="810" width="208" height="66" rx="8" fill="#1E293B" />',
        f'    <circle cx="45" cy="843" r="18" fill="#3B82F6" />',
        f'    <text x="45" y="848" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#FFFFFF">AN</text>',
        f'    <text x="75" y="838" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#FFFFFF">Nguyễn Văn An</text>',
        f'    <text x="75" y="854" font-family="Arial" font-size="11" fill="#10B981">● Online (User)</text>',
        f'  </g>',

        # --- TOPBAR (x: 240, y: 0, w: 1200, h: 64) ---
        f'  <g id="topbar">',
        f'    <rect x="240" y="0" width="1200" height="64" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1" />',
        f'    <text x="270" y="36" font-family="Times New Roman, Arial" font-size="15" font-weight="bold" fill="#0F172A">Bảng điều khiển Dinh dưỡng (Nutrition Dashboard)</text>',
        # Date selector
        f'    <rect x="680" y="14" width="260" height="36" rx="6" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1" />',
        f'    <text x="700" y="37" font-family="Arial" font-size="13" fill="#334155">◀</text>',
        f'    <text x="810" y="36" font-family="Times New Roman, Arial" font-size="13.5" font-weight="bold" text-anchor="middle" fill="#0F172A">Hôm nay: 07/11/2026</text>',
        f'    <text x="920" y="37" font-family="Arial" font-size="13" fill="#334155">▶</text>',

        # Training Cycle Badge
        f'    <rect x="960" y="14" width="220" height="36" rx="18" fill="#FEF3C7" stroke="#F59E0B" stroke-width="1.2" />',
        f'    <text x="1070" y="36" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" text-anchor="middle" fill="#B45309">🏋️ Hypertrophy (+15% Kcal)</text>',

        # Fridge alert button
        f'    <circle cx="1215" cy="32" r="16" fill="#FEE2E2" />',
        f'    <text x="1215" y="37" font-family="Arial" font-size="13" text-anchor="middle" fill="#DC2626">🔔</text>',
        f'    <circle cx="1225" cy="22" r="7" fill="#DC2626" />',
        f'    <text x="1225" y="26" font-family="Arial" font-size="9" font-weight="bold" text-anchor="middle" fill="#FFFFFF">2</text>',
        f'  </g>',

        # --- MAIN CONTENT AREA (x: 240, y: 64, w: 1200, h: 836) ---
        # ROW 1: 4 KPI CARDS (Kcal, Protein, Carbs, Fat)
        # Card 1: Kcal
        f'  <g id="kpi-kcal">',
        f'    <rect x="270" y="85" width="265" height="110" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#wf-shadow)" />',
        f'    <text x="290" y="112" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#64748B">TỔNG NĂNG LƯỢNG (KCAL)</text>',
        f'    <text x="290" y="145" font-family="Times New Roman, Arial" font-size="24" font-weight="bold" fill="#0F172A">2,196 <tspan font-size="14" font-weight="normal" fill="#64748B">/ 2,200 kcal</tspan></text>',
        f'    <rect x="290" y="165" width="225" height="8" rx="4" fill="#E2E8F0" />',
        f'    <rect x="290" y="165" width="224" height="8" rx="4" fill="#10B981" />',
        f'    <text x="495" y="158" font-family="Arial" font-size="11" font-weight="bold" fill="#10B981">99.8%</text>',
        f'  </g>',

        # Card 2: Protein
        f'  <g id="kpi-protein">',
        f'    <rect x="555" y="85" width="265" height="110" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#wf-shadow)" />',
        f'    <text x="575" y="112" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#64748B">CHẤT ĐẠM (PROTEIN)</text>',
        f'    <text x="575" y="145" font-family="Times New Roman, Arial" font-size="24" font-weight="bold" fill="#0F172A">148.5 <tspan font-size="14" font-weight="normal" fill="#64748B">/ 150.0 g</tspan></text>',
        f'    <rect x="575" y="165" width="225" height="8" rx="4" fill="#E2E8F0" />',
        f'    <rect x="575" y="165" width="222" height="8" rx="4" fill="#2563EB" />',
        f'    <text x="780" y="158" font-family="Arial" font-size="11" font-weight="bold" fill="#2563EB">99.0%</text>',
        f'  </g>',

        # Card 3: Carbs
        f'  <g id="kpi-carbs">',
        f'    <rect x="840" y="85" width="265" height="110" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#wf-shadow)" />',
        f'    <text x="860" y="112" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#64748B">TINH BỘT (CARBOHYDRATES)</text>',
        f'    <text x="860" y="145" font-family="Times New Roman, Arial" font-size="24" font-weight="bold" fill="#0F172A">222.0 <tspan font-size="14" font-weight="normal" fill="#64748B">/ 220.0 g</tspan></text>',
        f'    <rect x="860" y="165" width="225" height="8" rx="4" fill="#E2E8F0" />',
        f'    <rect x="860" y="165" width="227" height="8" rx="4" fill="#F59E0B" />',
        f'    <text x="1060" y="158" font-family="Arial" font-size="11" font-weight="bold" fill="#F59E0B">100.9%</text>',
        f'  </g>',

        # Card 4: Fat
        f'  <g id="kpi-fat">',
        f'    <rect x="1125" y="85" width="265" height="110" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#wf-shadow)" />',
        f'    <text x="1145" y="112" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#64748B">CHẤT BÉO (FAT)</text>',
        f'    <text x="1145" y="145" font-family="Times New Roman, Arial" font-size="24" font-weight="bold" fill="#0F172A">54.2 <tspan font-size="14" font-weight="normal" fill="#64748B">/ 55.0 g</tspan></text>',
        f'    <rect x="1145" y="165" width="225" height="8" rx="4" fill="#E2E8F0" />',
        f'    <rect x="1145" y="165" width="221" height="8" rx="4" fill="#EC4899" />',
        f'    <text x="1345" y="158" font-family="Arial" font-size="11" font-weight="bold" fill="#EC4899">98.5%</text>',
        f'  </g>',

        # ROW 2: TWO MAIN PANELS
        # LEFT PANEL: DAILY TARGETS FORM & MEAL LOGS (w: 700)
        # Box 1: Thiết lập mục tiêu ngày
        f'  <g id="card-daily-targets-setting">',
        f'    <rect x="270" y="215" width="690" height="310" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#wf-shadow)" />',
        f'    <text x="295" y="245" font-family="Times New Roman, Arial" font-size="16" font-weight="bold" fill="#0F172A">Thiết lập Mục tiêu Macro Ngày (DailyTargets)</text>',
        f'    <text x="295" y="266" font-family="Times New Roman, Arial" font-size="12.5" fill="#64748B">Áp dụng công thức tính tự động từ Chu kỳ tập luyện và Chỉ số BMR / TDEE cơ thể.</text>',

        # Cycle Selection Pills
        f'    <text x="295" y="298" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#334155">Chọn chu kỳ tập ngày hôm nay:</text>',
        f'    <rect x="295" y="308" width="130" height="32" rx="6" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1" />',
        f'    <text x="360" y="328" font-family="Times New Roman, Arial" font-size="12" text-anchor="middle" fill="#64748B">Cardio (-10%)</text>',

        f'    <rect x="435" y="308" width="160" height="32" rx="6" fill="#1E293B" stroke="#0F172A" stroke-width="1" />',
        f'    <text x="515" y="328" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#FFFFFF">✓ Hypertrophy (+15%)</text>',

        f'    <rect x="605" y="308" width="130" height="32" rx="6" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1" />',
        f'    <text x="670" y="328" font-family="Times New Roman, Arial" font-size="12" text-anchor="middle" fill="#64748B">Rest Day (-20%)</text>',

        # Inputs Grid
        f'    <text x="295" y="370" font-family="Times New Roman, Arial" font-size="12" fill="#475569">Target Kcal:</text>',
        f'    <rect x="295" y="378" width="150" height="36" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />',
        f'    <text x="310" y="401" font-family="Arial" font-size="13" font-weight="bold" fill="#0F172A">2,200 kcal</text>',

        f'    <text x="465" y="370" font-family="Times New Roman, Arial" font-size="12" fill="#475569">Target Protein (g):</text>',
        f'    <rect x="465" y="378" width="150" height="36" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />',
        f'    <text x="480" y="401" font-family="Arial" font-size="13" font-weight="bold" fill="#0F172A">150.0 g (2.2g/kg)</text>',

        f'    <text x="635" y="370" font-family="Times New Roman, Arial" font-size="12" fill="#475569">Target Carbs (g):</text>',
        f'    <rect x="635" y="378" width="150" height="36" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />',
        f'    <text x="650" y="401" font-family="Arial" font-size="13" font-weight="bold" fill="#0F172A">220.0 g (45%)</text>',

        f'    <text x="805" y="370" font-family="Times New Roman, Arial" font-size="12" fill="#475569">Target Fat (g):</text>',
        f'    <rect x="805" y="378" width="135" height="36" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />',
        f'    <text x="820" y="401" font-family="Arial" font-size="13" font-weight="bold" fill="#0F172A">55.0 g (25%)</text>',

        # Action Buttons in Card
        f'    <rect x="295" y="450" width="220" height="42" rx="6" fill="#1E293B" />',
        f'    <text x="405" y="476" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" text-anchor="middle" fill="#FFFFFF">💾 Lưu Cấu hình Mục tiêu</text>',

        f'    <rect x="530" y="450" width="260" height="42" rx="6" fill="#10B981" />',
        f'    <text x="660" y="476" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" text-anchor="middle" fill="#FFFFFF">⚡ TỐI ƯU THỰC ĐƠN TỪ KHO</text>',
        f'  </g>',

        # Box 2: Recent Meal Logs (y: 545, h: 320)
        f'  <g id="card-recent-meals">',
        f'    <rect x="270" y="545" width="690" height="320" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#wf-shadow)" />',
        f'    <text x="295" y="575" font-family="Times New Roman, Arial" font-size="15" font-weight="bold" fill="#0F172A">Nhật ký Bữa ăn trong ngày (Meal Logs Snapshot)</text>',

        # Table Header
        f'    <rect x="295" y="590" width="640" height="30" fill="#F1F5F9" />',
        f'    <text x="310" y="610" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">BỮA ĂN</text>',
        f'    <text x="420" y="610" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">THỰC PHẨM &amp; ĐỊNH LƯỢNG</text>',
        f'    <text x="670" y="610" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">KCAL</text>',
        f'    <text x="760" y="610" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">P / C / F (g)</text>',
        f'    <text x="880" y="610" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">NGUỒN</text>',

        # Row 1: Sáng
        f'    <line x1="295" y1="655" x2="935" y2="655" stroke="#E2E8F0" stroke-width="1" />',
        f'    <text x="310" y="642" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#0F172A">Bữa sáng</text>',
        f'    <text x="420" y="642" font-family="Arial" font-size="12.5" fill="#334155">Trứng gà ta (150g) + Dầu ô liu (6g)</text>',
        f'    <text x="670" y="642" font-family="Arial" font-size="12.5" fill="#334155">268 kcal</text>',
        f'    <text x="760" y="642" font-family="Arial" font-size="12.5" fill="#334155">18.9 / 1.2 / 20.3</text>',
        f'    <text x="880" y="642" font-family="Arial" font-size="11" fill="#10B981">● Auto-LP</text>',

        # Row 2: Trưa
        f'    <line x1="295" y1="710" x2="935" y2="710" stroke="#E2E8F0" stroke-width="1" />',
        f'    <text x="310" y="688" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#0F172A">Bữa trưa</text>',
        f'    <text x="420" y="688" font-family="Arial" font-size="12.5" fill="#334155">Ức gà (200g) + Gạo lứt (150g) + Súp lơ (120g)</text>',
        f'    <text x="670" y="688" font-family="Arial" font-size="12.5" fill="#334155">890 kcal</text>',
        f'    <text x="760" y="688" font-family="Arial" font-size="12.5" fill="#334155">76.2 / 125.4 / 11.2</text>',
        f'    <text x="880" y="688" font-family="Arial" font-size="11" fill="#10B981">● Auto-LP</text>',

        # Row 3: Tối
        f'    <line x1="295" y1="765" x2="935" y2="765" stroke="#E2E8F0" stroke-width="1" />',
        f'    <text x="310" y="740" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#0F172A">Bữa tối</text>',
        f'    <text x="420" y="740" font-family="Arial" font-size="12.5" fill="#334155">Ức gà (120g) + Gạo lứt (100g) + Súp lơ (80g)</text>',
        f'    <text x="670" y="740" font-family="Arial" font-size="12.5" fill="#334155">638 kcal</text>',
        f'    <text x="760" y="740" font-family="Arial" font-size="12.5" fill="#334155">45.4 / 85.4 / 8.2</text>',
        f'    <text x="880" y="740" font-family="Arial" font-size="11" fill="#10B981">● Auto-LP</text>',

        # Bottom actions
        f'    <rect x="295" y="800" width="180" height="34" rx="4" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1" />',
        f'    <text x="385" y="822" font-family="Times New Roman, Arial" font-size="12" text-anchor="middle" fill="#334155">+ Ghi món ăn thủ công</text>',
        f'  </g>',

        # RIGHT PANEL: MACRO SPLIT CHART & FRIDGE SUMMARY (w: 410)
        # Card 1: Biểu đồ Donut Macro Ratio
        f'  <g id="card-macro-chart">',
        f'    <rect x="980" y="215" width="410" height="350" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#wf-shadow)" />',
        f'    <text x="1005" y="245" font-family="Times New Roman, Arial" font-size="15" font-weight="bold" fill="#0F172A">Phân bổ Năng lượng (Macro Ratio)</text>',

        # SVG Donut Chart Mock
        f'    <circle cx="1185" cy="355" r="70" fill="none" stroke="#E2E8F0" stroke-width="26" />',
        f'    <circle cx="1185" cy="355" r="70" fill="none" stroke="#2563EB" stroke-width="26" stroke-dasharray="120 440" stroke-dashoffset="0" />',
        f'    <circle cx="1185" cy="355" r="70" fill="none" stroke="#F59E0B" stroke-width="26" stroke-dasharray="175 440" stroke-dashoffset="-120" />',
        f'    <circle cx="1185" cy="355" r="70" fill="none" stroke="#EC4899" stroke-width="26" stroke-dasharray="145 440" stroke-dashoffset="-295" />',
        f'    <text x="1185" y="352" font-family="Times New Roman, Arial" font-size="20" font-weight="bold" text-anchor="middle" fill="#0F172A">2,196</text>',
        f'    <text x="1185" y="370" font-family="Arial" font-size="11" text-anchor="middle" fill="#64748B">KCAL</text>',

        # Chart Legend
        f'    <circle cx="1025" cy="465" r="6" fill="#2563EB" />',
        f'    <text x="1040" y="470" font-family="Times New Roman, Arial" font-size="12" fill="#334155">Protein: 148.5g (27.1%)</text>',

        f'    <circle cx="1025" cy="495" r="6" fill="#F59E0B" />',
        f'    <text x="1040" y="500" font-family="Times New Roman, Arial" font-size="12" fill="#334155">Carbohydrates: 222.0g (40.4%)</text>',

        f'    <circle cx="1025" cy="525" r="6" fill="#EC4899" />',
        f'    <text x="1040" y="530" font-family="Times New Roman, Arial" font-size="12" fill="#334155">Fat: 54.2g (32.5%)</text>',
        f'  </g>',

        # Card 2: Fridge Overview Box
        f'  <g id="card-fridge-preview">',
        f'    <rect x="980" y="580" width="410" height="285" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#wf-shadow)" />',
        f'    <text x="1005" y="610" font-family="Times New Roman, Arial" font-size="15" font-weight="bold" fill="#0F172A">Kho Tủ lạnh Cá nhân (Tồn kho)</text>',
        f'    <text x="1005" y="630" font-family="Times New Roman, Arial" font-size="12" fill="#64748B">7 mặt hàng sẵn sàng cho giải thuật tối ưu:</text>',

        # Items Preview
        f'    <rect x="1005" y="645" width="360" height="36" rx="4" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1" />',
        f'    <text x="1020" y="668" font-family="Arial" font-size="12.5" font-weight="bold" fill="#0F172A">Ức gà phi lê</text>',
        f'    <text x="1230" y="668" font-family="Arial" font-size="12" fill="#64748B">650g</text>',
        f'    <text x="1350" y="668" font-family="Arial" font-size="11" text-anchor="end" fill="#10B981">Hạn: 5 ngày</text>',

        f'    <rect x="1005" y="690" width="360" height="36" rx="4" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1" />',
        f'    <text x="1020" y="713" font-family="Arial" font-size="12.5" font-weight="bold" fill="#991B1B">Súp lơ xanh</text>',
        f'    <text x="1230" y="713" font-family="Arial" font-size="12" fill="#991B1B">250g</text>',
        f'    <text x="1350" y="713" font-family="Arial" font-size="11" font-weight="bold" text-anchor="end" fill="#DC2626">⚠️ Hạn hôm nay!</text>',

        f'    <rect x="1005" y="735" width="360" height="36" rx="4" fill="#FEF3C7" stroke="#FCD34D" stroke-width="1" />',
        f'    <text x="1020" y="758" font-family="Arial" font-size="12.5" font-weight="bold" fill="#92400E">Thịt bò nạc</text>',
        f'    <text x="1230" y="758" font-family="Arial" font-size="12" fill="#92400E">300g</text>',
        f'    <text x="1350" y="758" font-family="Arial" font-size="11" font-weight="bold" text-anchor="end" fill="#D97706">⚠️ Còn 1 ngày</text>',

        # Action to open fridge
        f'    <rect x="1005" y="795" width="360" height="42" rx="6" fill="#1E293B" />',
        f'    <text x="1185" y="821" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" text-anchor="middle" fill="#FFFFFF">🥦 QUẢN LÝ TỦ LẠNH CHI TIẾT</text>',
        f'  </g>',

        # --- CALLOUT MARKERS ---
        draw_callout(120, 120, 1),
        draw_callout(1070, 32, 2),
        draw_callout(420, 140, 3),
        draw_callout(660, 470, 4),
        draw_callout(1185, 355, 5),
        draw_callout(1185, 715, 6),

        f'</svg>'
    ]

    out_path = os.path.join(WIREFRAMES_DIR, "fig_3_9_wireframe_dashboard.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated Wireframe: {out_path}")

# ==============================================================================
# 3. FIG 3.10: WIREFRAME INVENTORY & EXPIRY WARNING
# ==============================================================================
def generate_wireframe_inventory():
    w, h = 1440, 900
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        f'  <title>Hình 3-10: Wireframe Màn hình Kho Thực phẩm Tủ lạnh Cá nhân — SmartMacro Engine</title>',
        WF_DEFS,
        f'  <rect width="{w}" height="{h}" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2" />',

        # --- SIDEBAR (w: 240, h: 900) ---
        f'  <g id="sidebar">',
        f'    <rect x="0" y="0" width="240" height="{h}" fill="#0F172A" />',
        f'    <rect x="24" y="24" width="36" height="36" rx="8" fill="#10B981" />',
        f'    <text x="42" y="48" font-family="Arial" font-size="20" font-weight="bold" text-anchor="middle" fill="#FFFFFF">⚡</text>',
        f'    <text x="70" y="42" font-family="Times New Roman, Arial" font-size="18" font-weight="bold" fill="#FFFFFF">SmartMacro</text>',
        f'    <text x="72" y="56" font-family="Arial" font-size="10" fill="#94A3B8" letter-spacing="1">ENGINE v1.0</text>',
        f'    <line x1="24" y1="80" x2="216" y2="80" stroke="#1E293B" stroke-width="1" />',

        f'    <rect x="16" y="100" width="208" height="42" rx="6" fill="transparent" />',
        f'    <text x="36" y="126" font-family="Arial" font-size="14" fill="#94A3B8">📊</text>',
        f'    <text x="64" y="126" font-family="Times New Roman, Arial" font-size="14" fill="#94A3B8">Tổng quan dinh dưỡng</text>',

        # Inventory (ACTIVE)
        f'    <rect x="16" y="152" width="208" height="42" rx="6" fill="#1E293B" stroke="#334155" stroke-width="1" />',
        f'    <text x="36" y="178" font-family="Arial" font-size="14" fill="#10B981">🥦</text>',
        f'    <text x="64" y="178" font-family="Times New Roman, Arial" font-size="14" font-weight="bold" fill="#FFFFFF">Tủ lạnh cá nhân</text>',

        f'    <rect x="16" y="204" width="208" height="42" rx="6" fill="transparent" />',
        f'    <text x="36" y="230" font-family="Arial" font-size="14" fill="#94A3B8">⚡</text>',
        f'    <text x="64" y="230" font-family="Times New Roman, Arial" font-size="14" fill="#94A3B8">Tối ưu hóa thực đơn</text>',

        f'    <rect x="16" y="256" width="208" height="42" rx="6" fill="transparent" />',
        f'    <text x="36" y="282" font-family="Arial" font-size="14" fill="#94A3B8">📖</text>',
        f'    <text x="64" y="282" font-family="Times New Roman, Arial" font-size="14" fill="#94A3B8">Nhật ký bữa ăn</text>',

        f'    <rect x="16" y="810" width="208" height="66" rx="8" fill="#1E293B" />',
        f'    <circle cx="45" cy="843" r="18" fill="#3B82F6" />',
        f'    <text x="45" y="848" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#FFFFFF">AN</text>',
        f'    <text x="75" y="838" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#FFFFFF">Nguyễn Văn An</text>',
        f'    <text x="75" y="854" font-family="Arial" font-size="11" fill="#10B981">● Online (User)</text>',
        f'  </g>',

        # --- TOPBAR (x: 240, y: 0, w: 1200, h: 64) ---
        f'  <g id="topbar">',
        f'    <rect x="240" y="0" width="1200" height="64" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1" />',
        f'    <text x="270" y="36" font-family="Times New Roman, Arial" font-size="16" font-weight="bold" fill="#0F172A">Kho Thực phẩm Tủ lạnh Cá nhân (UserFoodInventories)</text>',
        f'    <rect x="940" y="14" width="240" height="36" rx="6" fill="#10B981" />',
        f'    <text x="1060" y="37" font-family="Times New Roman, Arial" font-size="13.5" font-weight="bold" text-anchor="middle" fill="#FFFFFF">+ THÊM THỰC PHẨM VÀO KHO</text>',
        f'  </g>',

        # --- INVENTORY CONTENT AREA (Left Table: w: 790, Right Drawer: w: 370) ---
        # Search & Filter Row
        f'  <g id="filter-bar">',
        f'    <rect x="270" y="85" width="260" height="38" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />',
        f'    <text x="285" y="108" font-family="Arial" font-size="13" fill="#64748B">🔍 Tìm tên món (ức gà, gạo...)</text>',

        # Category pills
        f'    <rect x="545" y="85" width="90" height="38" rx="6" fill="#1E293B" />',
        f'    <text x="590" y="108" font-family="Times New Roman, Arial" font-size="12.5" font-weight="bold" text-anchor="middle" fill="#FFFFFF">Tất cả (7)</text>',

        f'    <rect x="645" y="85" width="105" height="38" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />',
        f'    <text x="697" y="108" font-family="Times New Roman, Arial" font-size="12.5" text-anchor="middle" fill="#334155">Thịt &amp; Cá (2)</text>',

        f'    <rect x="760" y="85" width="105" height="38" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />',
        f'    <text x="812" y="108" font-family="Times New Roman, Arial" font-size="12.5" text-anchor="middle" fill="#334155">Tinh bột (2)</text>',

        f'    <rect x="875" y="85" width="95" height="38" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />',
        f'    <text x="922" y="108" font-family="Times New Roman, Arial" font-size="12.5" text-anchor="middle" fill="#334155">Rau củ (1)</text>',

        f'    <rect x="980" y="85" width="90" height="38" rx="6" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1" />',
        f'    <text x="1025" y="108" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#DC2626">⚠️ Sắp hết hạn (2)</text>',
        f'  </g>',

        # Inventory Table Container (w: 790, y: 140, h: 720)
        f'  <g id="inventory-table-container">',
        f'    <rect x="270" y="140" width="800" height="720" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#wf-shadow)" />',

        # Table Header
        f'    <rect x="270" y="140" width="800" height="42" rx="8" fill="#F1F5F9" />',
        f'    <rect x="270" y="160" width="800" height="22" fill="#F1F5F9" />',
        f'    <line x1="270" y1="182" x2="1070" y2="182" stroke="#CBD5E1" stroke-width="1" />',

        f'    <text x="290" y="166" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">MÓN ĂN &amp; PHÂN LOẠI</text>',
        f'    <text x="490" y="166" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">TỒN KHO (g)</text>',
        f'    <text x="600" y="166" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">KCAL/P/C/F (100g)</text>',
        f'    <text x="760" y="166" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">HẠN DÙNG</text>',
        f'    <text x="890" y="166" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">TRẠNG THÁI</text>',
        f'    <text x="1010" y="166" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">THAO TÁC</text>',

        # Row 1: Ức gà (Good)
        f'    <g id="row-1">',
        f'      <line x1="270" y1="245" x2="1070" y2="245" stroke="#E2E8F0" stroke-width="1" />',
        f'      <text x="290" y="208" font-family="Times New Roman, Arial" font-size="14" font-weight="bold" fill="#0F172A">Ức gà phi lê không da</text>',
        f'      <text x="290" y="226" font-family="Arial" font-size="11.5" fill="#64748B">Thịt &amp; Gia cầm · Ngăn đông</text>',
        f'      <text x="490" y="215" font-family="Arial" font-size="14" font-weight="bold" fill="#0F172A">650 <tspan font-size="11" fill="#64748B">gam</tspan></text>',
        f'      <text x="600" y="215" font-family="Arial" font-size="12" fill="#334155">165 / 31.0 / 0.0 / 3.6</text>',
        f'      <text x="760" y="215" font-family="Arial" font-size="12" fill="#334155">12/11/2026</text>',
        f'      <rect x="880" y="202" width="90" height="24" rx="12" fill="#DCFCE7" />',
        f'      <text x="925" y="218" font-family="Times New Roman, Arial" font-size="11" font-weight="bold" text-anchor="middle" fill="#166534">Còn 5 ngày</text>',
        f'      <text x="1005" y="217" font-family="Arial" font-size="13" fill="#2563EB">✏️</text>',
        f'      <text x="1035" y="217" font-family="Arial" font-size="13" fill="#DC2626">🗑️</text>',
        f'    </g>',

        # Row 2: Súp lơ xanh (Critical Expiry Today!)
        f'    <g id="row-2">',
        f'      <rect x="271" y="246" width="798" height="62" fill="#FEF2F2" fill-opacity="0.6" />',
        f'      <line x1="270" y1="308" x2="1070" y2="308" stroke="#E2E8F0" stroke-width="1" />',
        f'      <text x="290" y="271" font-family="Times New Roman, Arial" font-size="14" font-weight="bold" fill="#991B1B">Súp lơ xanh (Broccoli)</text>',
        f'      <text x="290" y="289" font-family="Arial" font-size="11.5" fill="#991B1B">Rau củ · Ngăn mát 1</text>',
        f'      <text x="490" y="278" font-family="Arial" font-size="14" font-weight="bold" fill="#991B1B">250 <tspan font-size="11">gam</tspan></text>',
        f'      <text x="600" y="278" font-family="Arial" font-size="12" fill="#7F1D1D">34 / 2.8 / 7.0 / 0.4</text>',
        f'      <text x="760" y="278" font-family="Arial" font-size="12" font-weight="bold" fill="#DC2626">07/11/2026</text>',
        f'      <rect x="880" y="265" width="105" height="24" rx="12" fill="#FEE2E2" stroke="#DC2626" stroke-width="1" />',
        f'      <text x="932" y="281" font-family="Times New Roman, Arial" font-size="11" font-weight="bold" text-anchor="middle" fill="#DC2626">⚠️ HẾT HẠN HÔM NAY</text>',
        f'      <text x="1005" y="280" font-family="Arial" font-size="13" fill="#2563EB">✏️</text>',
        f'      <text x="1035" y="280" font-family="Arial" font-size="13" fill="#DC2626">🗑️</text>',
        f'    </g>',

        # Row 3: Thịt bò nạc (Expires tomorrow!)
        f'    <g id="row-3">',
        f'      <line x1="270" y1="370" x2="1070" y2="370" stroke="#E2E8F0" stroke-width="1" />',
        f'      <text x="290" y="333" font-family="Times New Roman, Arial" font-size="14" font-weight="bold" fill="#92400E">Thịt thăn bò Úc</text>',
        f'      <text x="290" y="351" font-family="Arial" font-size="11.5" fill="#64748B">Thịt &amp; Hải sản · Ngăn mát 2</text>',
        f'      <text x="490" y="340" font-family="Arial" font-size="14" font-weight="bold" fill="#0F172A">300 <tspan font-size="11" fill="#64748B">gam</tspan></text>',
        f'      <text x="600" y="340" font-family="Arial" font-size="12" fill="#334155">250 / 26.0 / 0.0 / 15.0</text>',
        f'      <text x="760" y="340" font-family="Arial" font-size="12" fill="#D97706">08/11/2026</text>',
        f'      <rect x="880" y="327" width="95" height="24" rx="12" fill="#FEF3C7" stroke="#D97706" stroke-width="1" />',
        f'      <text x="927" y="343" font-family="Times New Roman, Arial" font-size="11" font-weight="bold" text-anchor="middle" fill="#92400E">Còn 1 ngày</text>',
        f'      <text x="1005" y="342" font-family="Arial" font-size="13" fill="#2563EB">✏️</text>',
        f'      <text x="1035" y="342" font-family="Arial" font-size="13" fill="#DC2626">🗑️</text>',
        f'    </g>',

        # Row 4: Gạo lứt (Good)
        f'    <g id="row-4">',
        f'      <line x1="270" y1="432" x2="1070" y2="432" stroke="#E2E8F0" stroke-width="1" />',
        f'      <text x="290" y="395" font-family="Times New Roman, Arial" font-size="14" font-weight="bold" fill="#0F172A">Gạo lứt đỏ Điện Biên</text>',
        f'      <text x="290" y="413" font-family="Arial" font-size="11.5" fill="#64748B">Tinh bột ngũ cốc · Tủ khô</text>',
        f'      <text x="490" y="402" font-family="Arial" font-size="14" font-weight="bold" fill="#0F172A">1,200 <tspan font-size="11" fill="#64748B">gam</tspan></text>',
        f'      <text x="600" y="402" font-family="Arial" font-size="12" fill="#334155">354 / 7.2 / 78.0 / 2.8</text>',
        f'      <text x="760" y="402" font-family="Arial" font-size="12" fill="#334155">30/12/2026</text>',
        f'      <rect x="880" y="389" width="90" height="24" rx="12" fill="#DCFCE7" />',
        f'      <text x="925" y="405" font-family="Times New Roman, Arial" font-size="11" font-weight="bold" text-anchor="middle" fill="#166534">Còn 53 ngày</text>',
        f'      <text x="1005" y="404" font-family="Arial" font-size="13" fill="#2563EB">✏️</text>',
        f'      <text x="1035" y="404" font-family="Arial" font-size="13" fill="#DC2626">🗑️</text>',
        f'    </g>',

        # Row 5: Trứng gà ta
        f'    <g id="row-5">',
        f'      <line x1="270" y1="495" x2="1070" y2="495" stroke="#E2E8F0" stroke-width="1" />',
        f'      <text x="290" y="458" font-family="Times New Roman, Arial" font-size="14" font-weight="bold" fill="#0F172A">Trứng gà ta (cả quả)</text>',
        f'      <text x="290" y="476" font-family="Arial" font-size="11.5" fill="#64748B">Trứng &amp; Sữa · Khay cánh tủ</text>',
        f'      <text x="490" y="465" font-family="Arial" font-size="14" font-weight="bold" fill="#0F172A">320 <tspan font-size="11" fill="#64748B">gam (~6 quả)</tspan></text>',
        f'      <text x="600" y="465" font-family="Arial" font-size="12" fill="#334155">143 / 12.6 / 0.8 / 9.5</text>',
        f'      <text x="760" y="465" font-family="Arial" font-size="12" fill="#334155">20/11/2026</text>',
        f'      <rect x="880" y="452" width="90" height="24" rx="12" fill="#DCFCE7" />',
        f'      <text x="925" y="468" font-family="Times New Roman, Arial" font-size="11" font-weight="bold" text-anchor="middle" fill="#166534">Còn 13 ngày</text>',
        f'      <text x="1005" y="467" font-family="Arial" font-size="13" fill="#2563EB">✏️</text>',
        f'      <text x="1035" y="467" font-family="Arial" font-size="13" fill="#DC2626">🗑️</text>',
        f'    </g>',

        # Row 6: Dầu ô liu
        f'    <g id="row-6">',
        f'      <line x1="270" y1="557" x2="1070" y2="557" stroke="#E2E8F0" stroke-width="1" />',
        f'      <text x="290" y="520" font-family="Times New Roman, Arial" font-size="14" font-weight="bold" fill="#0F172A">Dầu ô liu nguyên chất Extra Virgin</text>',
        f'      <text x="290" y="538" font-family="Arial" font-size="11.5" fill="#64748B">Dầu &amp; Chất béo tốt · Kệ gia vị</text>',
        f'      <text x="490" y="527" font-family="Arial" font-size="14" font-weight="bold" fill="#0F172A">200 <tspan font-size="11" fill="#64748B">gam</tspan></text>',
        f'      <text x="600" y="527" font-family="Arial" font-size="12" fill="#334155">884 / 0.0 / 0.0 / 100.0</text>',
        f'      <text x="760" y="527" font-family="Arial" font-size="12" fill="#334155">15/06/2027</text>',
        f'      <rect x="880" y="514" width="90" height="24" rx="12" fill="#DCFCE7" />',
        f'      <text x="925" y="530" font-family="Times New Roman, Arial" font-size="11" font-weight="bold" text-anchor="middle" fill="#166534">Còn 220 ngày</text>',
        f'      <text x="1005" y="529" font-family="Arial" font-size="13" fill="#2563EB">✏️</text>',
        f'      <text x="1035" y="529" font-family="Arial" font-size="13" fill="#DC2626">🗑️</text>',
        f'    </g>',

        # Table Pagination bottom
        f'    <text x="290" y="835" font-family="Times New Roman, Arial" font-size="12" fill="#64748B">Hiển thị 1 - 6 của 7 thực phẩm</text>',
        f'    <rect x="940" y="818" width="110" height="30" rx="4" fill="#F1F5F9" />',
        f'    <text x="995" y="838" font-family="Arial" font-size="12" text-anchor="middle" fill="#334155">Trang 1 / 1</text>',
        f'  </g>',

        # --- RIGHT SIDEBAR / ADD ITEM DRAWER (w: 320, x: 1090) ---
        f'  <g id="add-item-drawer">',
        f'    <rect x="1090" y="85" width="325" height="775" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#modal-shadow)" />',
        f'    <rect x="1090" y="85" width="325" height="48" rx="8" fill="#1E293B" />',
        f'    <rect x="1090" y="110" width="325" height="23" fill="#1E293B" />',
        f'    <text x="1110" y="115" font-family="Times New Roman, Arial" font-size="14.5" font-weight="bold" fill="#FFFFFF">Thêm Món vào Tủ lạnh Cá nhân</text>',

        # Form fields
        f'    <text x="1110" y="160" font-family="Times New Roman, Arial" font-size="12.5" font-weight="bold" fill="#334155">1. Tra cứu Ngân hàng Thực phẩm (Foods):</text>',
        f'    <rect x="1110" y="170" width="285" height="38" rx="5" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1" />',
        f'    <text x="1125" y="194" font-family="Arial" font-size="13" fill="#0F172A">Ức gà phi lê không da ▾</text>',

        f'    <text x="1110" y="235" font-family="Times New Roman, Arial" font-size="12.5" font-weight="bold" fill="#334155">2. Khối lượng mua về (Gam) <tspan fill="#DC2626">*</tspan>:</text>',
        f'    <rect x="1110" y="245" width="285" height="38" rx="5" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1" />',
        f'    <text x="1125" y="269" font-family="Arial" font-size="13" font-weight="bold" fill="#0F172A">500</text>',
        f'    <text x="1375" y="269" font-family="Arial" font-size="12" text-anchor="end" fill="#64748B">gam</text>',

        f'    <text x="1110" y="310" font-family="Times New Roman, Arial" font-size="12.5" font-weight="bold" fill="#334155">3. Hạn sử dụng (Expiry Date) <tspan fill="#DC2626">*</tspan>:</text>',
        f'    <rect x="1110" y="320" width="285" height="38" rx="5" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1" />',
        f'    <text x="1125" y="344" font-family="Arial" font-size="13" fill="#0F172A">15/11/2026</text>',
        f'    <text x="1375" y="344" font-family="Arial" font-size="14" text-anchor="end" fill="#64748B">📅</text>',

        f'    <text x="1110" y="385" font-family="Times New Roman, Arial" font-size="12.5" font-weight="bold" fill="#334155">4. Ghi chú vị trí lưu trữ (Unit Note):</text>',
        f'    <rect x="1110" y="395" width="285" height="38" rx="5" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />',
        f'    <text x="1125" y="419" font-family="Arial" font-size="12.5" fill="#64748B">Khay đông số 2, túi zip hút chân không</text>',

        # Nutritional preview box
        f'    <rect x="1110" y="455" width="285" height="115" rx="6" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1" />',
        f'    <text x="1125" y="478" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#166534">Giá trị dinh dưỡng tích lũy (500g):</text>',
        f'    <text x="1125" y="502" font-family="Arial" font-size="13" font-weight="bold" fill="#0F172A">Năng lượng: 825.0 kcal</text>',
        f'    <text x="1125" y="524" font-family="Arial" font-size="12" fill="#334155">Protein: 155.0g · Fat: 18.0g · Carbs: 0g</text>',
        f'    <text x="1125" y="546" font-family="Times New Roman, Arial" font-size="11" font-style="italic" fill="#059669">✓ Đủ cho 1 ngày luyện tập cường độ cao</text>',

        # Submit button
        f'    <rect x="1110" y="590" width="285" height="44" rx="6" fill="#10B981" />',
        f'    <text x="1252" y="617" font-family="Times New Roman, Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="#FFFFFF">💾 LƯU VÀO TỦ LẠNH</text>',

        # Quick LP run button
        f'    <rect x="1110" y="645" width="285" height="44" rx="6" fill="#1E293B" />',
        f'    <text x="1252" y="672" font-family="Times New Roman, Arial" font-size="13.5" font-weight="bold" text-anchor="middle" fill="#FFFFFF">⚡ CHUYỂN SANG TỐI ƯU HÓA</text>',
        f'  </g>',

        # --- CALLOUT MARKERS ---
        draw_callout(400, 105, 1),
        draw_callout(1025, 105, 2),
        draw_callout(490, 215, 3),
        draw_callout(932, 275, 4),
        draw_callout(1252, 190, 5),
        draw_callout(1252, 665, 6),

        f'</svg>'
    ]

    out_path = os.path.join(WIREFRAMES_DIR, "fig_3_10_wireframe_inventory.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated Wireframe: {out_path}")

# ==============================================================================
# 4. FIG 3.11: WIREFRAME OPTIMIZER (OR-TOOLS LP MEAL SOLVER)
# ==============================================================================
def generate_wireframe_optimizer():
    w, h = 1440, 900
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        f'  <title>Hình 3-11: Wireframe Màn hình Tối ưu hóa Khẩu phần ăn thông minh với OR-Tools — SmartMacro Engine</title>',
        WF_DEFS,
        f'  <rect width="{w}" height="{h}" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2" />',

        # --- SIDEBAR (w: 240, h: 900) ---
        f'  <g id="sidebar">',
        f'    <rect x="0" y="0" width="240" height="{h}" fill="#0F172A" />',
        f'    <rect x="24" y="24" width="36" height="36" rx="8" fill="#10B981" />',
        f'    <text x="42" y="48" font-family="Arial" font-size="20" font-weight="bold" text-anchor="middle" fill="#FFFFFF">⚡</text>',
        f'    <text x="70" y="42" font-family="Times New Roman, Arial" font-size="18" font-weight="bold" fill="#FFFFFF">SmartMacro</text>',
        f'    <text x="72" y="56" font-family="Arial" font-size="10" fill="#94A3B8" letter-spacing="1">ENGINE v1.0</text>',
        f'    <line x1="24" y1="80" x2="216" y2="80" stroke="#1E293B" stroke-width="1" />',

        f'    <rect x="16" y="100" width="208" height="42" rx="6" fill="transparent" />',
        f'    <text x="36" y="126" font-family="Arial" font-size="14" fill="#94A3B8">📊</text>',
        f'    <text x="64" y="126" font-family="Times New Roman, Arial" font-size="14" fill="#94A3B8">Tổng quan dinh dưỡng</text>',

        f'    <rect x="16" y="152" width="208" height="42" rx="6" fill="transparent" />',
        f'    <text x="36" y="178" font-family="Arial" font-size="14" fill="#94A3B8">🥦</text>',
        f'    <text x="64" y="178" font-family="Times New Roman, Arial" font-size="14" fill="#94A3B8">Tủ lạnh cá nhân</text>',

        # Optimizer (ACTIVE)
        f'    <rect x="16" y="204" width="208" height="42" rx="6" fill="#1E293B" stroke="#334155" stroke-width="1" />',
        f'    <text x="36" y="230" font-family="Arial" font-size="14" fill="#10B981">⚡</text>',
        f'    <text x="64" y="230" font-family="Times New Roman, Arial" font-size="14" font-weight="bold" fill="#FFFFFF">Tối ưu hóa thực đơn</text>',

        f'    <rect x="16" y="256" width="208" height="42" rx="6" fill="transparent" />',
        f'    <text x="36" y="282" font-family="Arial" font-size="14" fill="#94A3B8">📖</text>',
        f'    <text x="64" y="282" font-family="Times New Roman, Arial" font-size="14" fill="#94A3B8">Nhật ký bữa ăn</text>',

        f'    <rect x="16" y="810" width="208" height="66" rx="8" fill="#1E293B" />',
        f'    <circle cx="45" cy="843" r="18" fill="#3B82F6" />',
        f'    <text x="45" y="848" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#FFFFFF">AN</text>',
        f'    <text x="75" y="838" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#FFFFFF">Nguyễn Văn An</text>',
        f'    <text x="75" y="854" font-family="Arial" font-size="11" fill="#10B981">● Online (User)</text>',
        f'  </g>',

        # --- TOPBAR (x: 240, y: 0, w: 1200, h: 64) ---
        f'  <g id="topbar">',
        f'    <rect x="240" y="0" width="1200" height="64" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1" />',
        f'    <text x="270" y="36" font-family="Times New Roman, Arial" font-size="16" font-weight="bold" fill="#0F172A">Bộ máy Tối ưu hóa Khẩu phần ăn Thông minh (Google OR-Tools GLOP Solver)</text>',
        f'    <rect x="1080" y="14" width="135" height="36" rx="18" fill="#DCFCE7" stroke="#16A34A" stroke-width="1" />',
        f'    <text x="1147" y="36" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#166534">● GLOP Ready</text>',
        f'  </g>',

        # --- TWO COLUMN OPTIMIZATION WORKSPACE ---
        # LEFT PANEL: INPUT CONFIG & CONSTRAINTS (x: 270, w: 460)
        f'  <g id="left-config-panel">',
        # Card 1: Daily Target Specs
        f'    <rect x="270" y="85" width="460" height="190" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#wf-shadow)" />',
        f'    <text x="290" y="112" font-family="Times New Roman, Arial" font-size="14.5" font-weight="bold" fill="#0F172A">1. Mục tiêu Macro Cần Giải Quyết (Daily Targets)</text>',
        f'    <text x="290" y="130" font-family="Times New Roman, Arial" font-size="12" fill="#64748B">Ngày: 07/11/2026 · Chu kỳ: Hypertrophy · Biên độ: ±5%</text>',

        # 4 Mini badges for Target
        f'    <rect x="290" y="145" width="100" height="50" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1" />',
        f'    <text x="340" y="165" font-family="Arial" font-size="10.5" text-anchor="middle" fill="#64748B">KCAL MỤC TIÊU</text>',
        f'    <text x="340" y="185" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="#0F172A">2,200</text>',

        f'    <rect x="398" y="145" width="100" height="50" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1" />',
        f'    <text x="448" y="165" font-family="Arial" font-size="10.5" text-anchor="middle" fill="#2563EB">PROTEIN (±5%)</text>',
        f'    <text x="448" y="185" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="#2563EB">150.0 g</text>',

        f'    <rect x="506" y="145" width="100" height="50" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1" />',
        f'    <text x="556" y="165" font-family="Arial" font-size="10.5" text-anchor="middle" fill="#F59E0B">CARBS (±5%)</text>',
        f'    <text x="556" y="185" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="#F59E0B">220.0 g</text>',

        f'    <rect x="614" y="145" width="100" height="50" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1" />',
        f'    <text x="664" y="165" font-family="Arial" font-size="10.5" text-anchor="middle" fill="#EC4899">FAT (±5%)</text>',
        f'    <text x="664" y="185" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="#EC4899">55.0 g</text>',

        f'    <text x="290" y="222" font-family="Times New Roman, Arial" font-size="11.5" font-style="italic" fill="#059669">Hệ ràng buộc: 142.5g ≤ Protein ≤ 157.5g | 209g ≤ Carbs ≤ 231g | 52.2g ≤ Fat ≤ 57.8g</text>',
        f'    <text x="290" y="240" font-family="Times New Roman, Arial" font-size="11.5" font-style="italic" fill="#059669">Hàm mục tiêu: Minimize |TotalKcal - 2200| thông qua biến phụ tuyến tính.</text>',

        # Card 2: Inventory Selection Checkbox (y: 290, h: 420)
        f'    <rect x="270" y="290" width="460" height="440" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#wf-shadow)" />',
        f'    <text x="290" y="318" font-family="Times New Roman, Arial" font-size="14.5" font-weight="bold" fill="#0F172A">2. Chọn Nguyên liệu Tủ lạnh Tham gia Tối ưu</text>',
        f'    <text x="290" y="336" font-family="Times New Roman, Arial" font-size="12" fill="#64748B">Thuật toán sẽ phân bổ số gam (0 ≤ x_i ≤ Tồn kho) từ các món sau:</text>',

        # Checkbox Items
        # Item 1
        f'    <rect x="290" y="352" width="420" height="50" rx="6" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1" />',
        f'    <rect x="305" y="369" width="16" height="16" rx="3" fill="#10B981" />',
        f'    <text x="313" y="381" font-family="Arial" font-size="11" font-weight="bold" text-anchor="middle" fill="#FFFFFF">✓</text>',
        f'    <text x="335" y="375" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#0F172A">Ức gà phi lê không da</text>',
        f'    <text x="335" y="392" font-family="Arial" font-size="11" fill="#059669">Tồn: 650g · Giàu đạm (31g/100g) · Hạn: 5 ngày</text>',

        # Item 2
        f'    <rect x="290" y="410" width="420" height="50" rx="6" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1" />',
        f'    <rect x="305" y="427" width="16" height="16" rx="3" fill="#10B981" />',
        f'    <text x="313" y="439" font-family="Arial" font-size="11" font-weight="bold" text-anchor="middle" fill="#FFFFFF">✓</text>',
        f'    <text x="335" y="433" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#0F172A">Gạo lứt đỏ Điện Biên</text>',
        f'    <text x="335" y="450" font-family="Arial" font-size="11" fill="#059669">Tồn: 1,200g · Tinh bột hấp thu chậm (78g/100g)</text>',

        # Item 3
        f'    <rect x="290" y="468" width="420" height="50" rx="6" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1" />',
        f'    <rect x="305" y="485" width="16" height="16" rx="3" fill="#DC2626" />',
        f'    <text x="313" y="497" font-family="Arial" font-size="11" font-weight="bold" text-anchor="middle" fill="#FFFFFF">✓</text>',
        f'    <text x="335" y="491" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#991B1B">Súp lơ xanh (Ưu tiên dùng - Hạn hôm nay!)</text>',
        f'    <text x="335" y="508" font-family="Arial" font-size="11" fill="#DC2626">Tồn: 250g · Chất xơ &amp; Vi chất</text>',

        # Item 4
        f'    <rect x="290" y="526" width="420" height="50" rx="6" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1" />',
        f'    <rect x="305" y="543" width="16" height="16" rx="3" fill="#10B981" />',
        f'    <text x="313" y="555" font-family="Arial" font-size="11" font-weight="bold" text-anchor="middle" fill="#FFFFFF">✓</text>',
        f'    <text x="335" y="549" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#0F172A">Trứng gà ta (cả quả)</text>',
        f'    <text x="335" y="566" font-family="Arial" font-size="11" fill="#059669">Tồn: 320g · Đạm &amp; Chất béo tốt</text>',

        # Item 5
        f'    <rect x="290" y="584" width="420" height="50" rx="6" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1" />',
        f'    <rect x="305" y="601" width="16" height="16" rx="3" fill="#10B981" />',
        f'    <text x="313" y="613" font-family="Arial" font-size="11" font-weight="bold" text-anchor="middle" fill="#FFFFFF">✓</text>',
        f'    <text x="335" y="607" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#0F172A">Dầu ô liu nguyên chất Extra Virgin</text>',
        f'    <text x="335" y="624" font-family="Arial" font-size="11" fill="#059669">Tồn: 200g · 100% Chất béo chưa bão hòa</text>',

        # Item 6 (Unchecked)
        f'    <rect x="290" y="642" width="420" height="42" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1" />',
        f'    <rect x="305" y="655" width="16" height="16" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />',
        f'    <text x="335" y="667" font-family="Times New Roman, Arial" font-size="12.5" fill="#64748B">Thịt thăn bò Úc (300g) — Không chọn</text>',

        # Big Button Solve
        f'    <rect x="270" y="750" width="460" height="52" rx="8" fill="#10B981" stroke="#059669" stroke-width="1.5" filter="url(#wf-shadow)" />',
        f'    <text x="500" y="782" font-family="Times New Roman, Arial" font-size="16" font-weight="bold" text-anchor="middle" fill="#FFFFFF">⚡ CHẠY THUẬT TOÁN TỐI ƯU HÓA (OR-TOOLS)</text>',
        f'    <text x="500" y="820" font-family="Arial" font-size="11.5" text-anchor="middle" fill="#64748B">Thời gian thực thi trung bình: ~15ms trên máy chủ ASP.NET Core</text>',
        f'  </g>',

        # RIGHT PANEL: SOLVER OUTPUT & ALLOCATED MEAL PLAN (x: 750, w: 660)
        f'  <g id="right-results-panel">',
        # Status Banner
        f'    <rect x="750" y="85" width="660" height="65" rx="8" fill="#ECFDF5" stroke="#10B981" stroke-width="1.5" filter="url(#wf-shadow)" />',
        f'    <circle cx="780" cy="117" r="14" fill="#10B981" />',
        f'    <text x="780" y="122" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="#FFFFFF">✓</text>',
        f'    <text x="805" y="110" font-family="Times New Roman, Arial" font-size="15" font-weight="bold" fill="#065F46">THUẬT TOÁN ĐÃ TÌM THẤY NGHIỆM TỐI ƯU (STATUS: OPTIMAL)</text>',
        f'    <text x="805" y="130" font-family="Arial" font-size="12" fill="#047857">Thời gian giải: 14.8 ms · Google Linear Solver GLOP · Đạt 100% ràng buộc dinh dưỡng</text>',

        # Macro Comparison Card
        f'    <rect x="750" y="165" width="660" height="195" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#wf-shadow)" />',
        f'    <text x="775" y="195" font-family="Times New Roman, Arial" font-size="15" font-weight="bold" fill="#0F172A">Đối chiếu Kết quả Dinh dưỡng Đạt được vs Mục tiêu:</text>',

        # Progress 1: Kcal
        f'    <text x="775" y="222" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#0F172A">Năng lượng (Kcal):</text>',
        f'    <text x="1000" y="222" font-family="Arial" font-size="12.5" fill="#334155">2,196.6 / 2,200.0 kcal (Sai lệch: -3.4 kcal · 0.15%)</text>',
        f'    <text x="1380" y="222" font-family="Arial" font-size="12" font-weight="bold" text-anchor="end" fill="#10B981">TỐI ƯU</text>',
        f'    <rect x="775" y="230" width="610" height="8" rx="4" fill="#E2E8F0" />',
        f'    <rect x="775" y="230" width="608" height="8" rx="4" fill="#10B981" />',

        # Progress 2: Protein
        f'    <text x="775" y="260" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#2563EB">Chất đạm (Protein):</text>',
        f'    <text x="1000" y="260" font-family="Arial" font-size="12.5" fill="#334155">148.5 / 150.0 g (Dung sai cho phép: 142.5 - 157.5g)</text>',
        f'    <text x="1380" y="260" font-family="Arial" font-size="12" font-weight="bold" text-anchor="end" fill="#2563EB">99.0% (ĐẠT)</text>',
        f'    <rect x="775" y="268" width="610" height="8" rx="4" fill="#E2E8F0" />',
        f'    <rect x="775" y="268" width="604" height="8" rx="4" fill="#2563EB" />',

        # Progress 3: Carbs
        f'    <text x="775" y="298" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#F59E0B">Tinh bột (Carbs):</text>',
        f'    <text x="1000" y="298" font-family="Arial" font-size="12.5" fill="#334155">222.0 / 220.0 g (Dung sai cho phép: 209.0 - 231.0g)</text>',
        f'    <text x="1380" y="298" font-family="Arial" font-size="12" font-weight="bold" text-anchor="end" fill="#F59E0B">100.9% (ĐẠT)</text>',
        f'    <rect x="775" y="306" width="610" height="8" rx="4" fill="#E2E8F0" />',
        f'    <rect x="775" y="306" width="610" height="8" rx="4" fill="#F59E0B" />',

        # Progress 4: Fat
        f'    <text x="775" y="336" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#EC4899">Chất béo (Fat):</text>',
        f'    <text x="1000" y="336" font-family="Arial" font-size="12.5" fill="#334155">54.2 / 55.0 g (Dung sai cho phép: 52.2 - 57.8g)</text>',
        f'    <text x="1380" y="336" font-family="Arial" font-size="12" font-weight="bold" text-anchor="end" fill="#EC4899">98.5% (ĐẠT)</text>',
        f'    <rect x="775" y="344" width="610" height="8" rx="4" fill="#E2E8F0" />',
        f'    <rect x="775" y="344" width="601" height="8" rx="4" fill="#EC4899" />',

        # Allocated Food Items Table (y: 375, h: 425)
        f'    <rect x="750" y="375" width="660" height="425" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#wf-shadow)" />',
        f'    <text x="775" y="405" font-family="Times New Roman, Arial" font-size="15" font-weight="bold" fill="#0F172A">Bảng Định lượng Số Gram Tối ưu Cần lấy từ Tủ lạnh (AllocatedItems):</text>',

        # Table Header
        f'    <rect x="775" y="420" width="610" height="32" rx="4" fill="#F1F5F9" />',
        f'    <text x="790" y="441" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">THỰC PHẨM ĐƯỢC CHỌN</text>',
        f'    <text x="990" y="441" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">SỐ GAM (x_i)</text>',
        f'    <text x="1100" y="441" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">KCAL</text>',
        f'    <text x="1180" y="441" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">PROTEIN</text>',
        f'    <text x="1270" y="441" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">CARBS</text>',
        f'    <text x="1340" y="441" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#475569">FAT</text>',

        # Rows
        # 1. Ức gà
        f'    <line x1="775" y1="485" x2="1385" y2="485" stroke="#E2E8F0" stroke-width="1" />',
        f'    <text x="790" y="472" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#0F172A">Ức gà phi lê không da</text>',
        f'    <text x="990" y="472" font-family="Arial" font-size="14" font-weight="bold" fill="#10B981">320.0 g</text>',
        f'    <text x="1100" y="472" font-family="Arial" font-size="12.5" fill="#334155">528.0</text>',
        f'    <text x="1180" y="472" font-family="Arial" font-size="12.5" fill="#334155">99.2 g</text>',
        f'    <text x="1270" y="472" font-family="Arial" font-size="12.5" fill="#334155">0.0 g</text>',
        f'    <text x="1340" y="472" font-family="Arial" font-size="12.5" fill="#334155">11.5 g</text>',

        # 2. Gạo lứt
        f'    <line x1="775" y1="525" x2="1385" y2="525" stroke="#E2E8F0" stroke-width="1" />',
        f'    <text x="790" y="512" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#0F172A">Gạo lứt đỏ Điện Biên</text>',
        f'    <text x="990" y="512" font-family="Arial" font-size="14" font-weight="bold" fill="#10B981">250.0 g</text>',
        f'    <text x="1100" y="512" font-family="Arial" font-size="12.5" fill="#334155">885.0</text>',
        f'    <text x="1180" y="512" font-family="Arial" font-size="12.5" fill="#334155">18.0 g</text>',
        f'    <text x="1270" y="512" font-family="Arial" font-size="12.5" fill="#334155">195.0 g</text>',
        f'    <text x="1340" y="512" font-family="Arial" font-size="12.5" fill="#334155">7.0 g</text>',

        # 3. Súp lơ xanh
        f'    <line x1="775" y1="565" x2="1385" y2="565" stroke="#E2E8F0" stroke-width="1" />',
        f'    <text x="790" y="552" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#991B1B">Súp lơ xanh (Ưu tiên giải quyết)</text>',
        f'    <text x="990" y="552" font-family="Arial" font-size="14" font-weight="bold" fill="#DC2626">200.0 g</text>',
        f'    <text x="1100" y="552" font-family="Arial" font-size="12.5" fill="#334155">68.0</text>',
        f'    <text x="1180" y="552" font-family="Arial" font-size="12.5" fill="#334155">5.6 g</text>',
        f'    <text x="1270" y="552" font-family="Arial" font-size="12.5" fill="#334155">14.0 g</text>',
        f'    <text x="1340" y="552" font-family="Arial" font-size="12.5" fill="#334155">0.8 g</text>',

        # 4. Trứng gà ta
        f'    <line x1="775" y1="605" x2="1385" y2="605" stroke="#E2E8F0" stroke-width="1" />',
        f'    <text x="790" y="592" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#0F172A">Trứng gà ta (cả quả ~3 quả)</text>',
        f'    <text x="990" y="592" font-family="Arial" font-size="14" font-weight="bold" fill="#10B981">150.0 g</text>',
        f'    <text x="1100" y="592" font-family="Arial" font-size="12.5" fill="#334155">214.5</text>',
        f'    <text x="1180" y="592" font-family="Arial" font-size="12.5" fill="#334155">18.9 g</text>',
        f'    <text x="1270" y="592" font-family="Arial" font-size="12.5" fill="#334155">1.2 g</text>',
        f'    <text x="1340" y="592" font-family="Arial" font-size="12.5" fill="#334155">14.3 g</text>',

        # 5. Dầu ô liu
        f'    <line x1="775" y1="645" x2="1385" y2="645" stroke="#E2E8F0" stroke-width="1" />',
        f'    <text x="790" y="632" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#0F172A">Dầu ô liu nguyên chất</text>',
        f'    <text x="990" y="632" font-family="Arial" font-size="14" font-weight="bold" fill="#10B981">18.0 g</text>',
        f'    <text x="1100" y="632" font-family="Arial" font-size="12.5" fill="#334155">159.1</text>',
        f'    <text x="1180" y="632" font-family="Arial" font-size="12.5" fill="#334155">0.0 g</text>',
        f'    <text x="1270" y="632" font-family="Arial" font-size="12.5" fill="#334155">0.0 g</text>',
        f'    <text x="1340" y="632" font-family="Arial" font-size="12.5" fill="#334155">18.0 g</text>',

        # Total Row
        f'    <rect x="775" y="650" width="610" height="36" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1" />',
        f'    <text x="790" y="673" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#0F172A">TỔNG CỘNG KHẨU PHẦN:</text>',
        f'    <text x="990" y="673" font-family="Arial" font-size="13" font-weight="bold" fill="#0F172A">938.0 g</text>',
        f'    <text x="1100" y="673" font-family="Arial" font-size="13" font-weight="bold" fill="#10B981">2,196.6</text>',
        f'    <text x="1180" y="673" font-family="Arial" font-size="13" font-weight="bold" fill="#2563EB">148.5g</text>',
        f'    <text x="1270" y="673" font-family="Arial" font-size="13" font-weight="bold" fill="#F59E0B">222.0g</text>',
        f'    <text x="1340" y="673" font-family="Arial" font-size="13" font-weight="bold" fill="#EC4899">54.2g</text>',

        # Action Buttons Bottom
        f'    <rect x="775" y="720" width="370" height="46" rx="6" fill="#1E293B" />',
        f'    <text x="960" y="748" font-family="Times New Roman, Arial" font-size="13.5" font-weight="bold" text-anchor="middle" fill="#FFFFFF">✅ XÁC NHẬN VÀ LƯU VÀO NHẬT KÝ BỮA ĂN</text>',

        f'    <rect x="1165" y="720" width="220" height="46" rx="6" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.5" />',
        f'    <text x="1275" y="748" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" text-anchor="middle" fill="#334155">🖨️ Xuất Thực đơn (PDF)</text>',
        f'  </g>',

        # --- CALLOUT MARKERS ---
        draw_callout(448, 145, 1),
        draw_callout(313, 370, 2),
        draw_callout(500, 750, 3),
        draw_callout(805, 110, 4),
        draw_callout(1380, 260, 5),
        draw_callout(990, 472, 6),
        draw_callout(960, 720, 7),

        f'</svg>'
    ]

    out_path = os.path.join(WIREFRAMES_DIR, "fig_3_11_wireframe_optimizer.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated Wireframe: {out_path}")

def main():
    print("Generating Figma-ready Wireframes for Thesis Chapter 3...")
    generate_wireframe_auth()
    generate_wireframe_dashboard()
    generate_wireframe_inventory()
    generate_wireframe_optimizer()
    print("Done generating all 4 wireframes.")

if __name__ == "__main__":
    main()
