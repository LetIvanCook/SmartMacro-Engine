# -*- coding: utf-8 -*-
"""
SmartMacro Engine - Sinh bộ sơ đồ UML Chương 3
Định dạng SVG độ nét cao chuẩn Khoa CNTT - STU:
- fig_3_3_usecase_detailed.svg: Sơ đồ Use Case chi tiết (Admin & User, include/extend)
- fig_3_4_class_diagram.svg: Sơ đồ lớp (Class Diagram) 3 tầng .NET 8 + OR-Tools + EF Core
- fig_3_5_sequence_login_and_inventory.svg: Sơ đồ tuần tự Đăng nhập & Quản lý kho
- fig_3_6_sequence_optimization.svg: Sơ đồ tuần tự Tối ưu hóa thực đơn Google OR-Tools
- fig_3_7_activity_optimization.svg: Sơ đồ hoạt động (Activity Diagram) giải thuật LP
"""

import os
import html

DIAGRAMS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "diagrams"))
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

COMMON_DEFS = """
  <defs>
    <!-- Arrow Markers -->
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1E293B" />
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563EB" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669" />
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#DC2626" />
    </marker>
    <marker id="open-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="#475569" stroke-width="1.6" stroke-linecap="round" />
    </marker>
    <marker id="open-arrow-dashed" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="#2563EB" stroke-width="1.6" stroke-linecap="round" />
    </marker>
    <!-- Realization hollow triangle -->
    <marker id="triangle-hollow" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="11" markerHeight="11" orient="auto-start-reverse">
      <polygon points="1 1, 13 7, 1 13" fill="#FFFFFF" stroke="#2563EB" stroke-width="1.6" />
    </marker>
    <!-- Filter for subtle drop-shadow -->
    <filter id="card-shadow" x="-3%" y="-3%" width="108%" height="108%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.08" />
    </filter>
    <filter id="callout-shadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#000000" flood-opacity="0.25" />
    </filter>
  </defs>
"""

# ==============================================================================
# 1. FIG 3.3: USE CASE CHI TIẾT (ADMIN & USER)
# ==============================================================================
def generate_usecase_diagram():
    w, h = 1700, 1150
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        f'  <title>Hình 3-3: Sơ đồ Use Case chi tiết — SmartMacro Engine</title>',
        COMMON_DEFS,
        f'  <rect width="{w}" height="{h}" fill="#F8FAFC" />',
        
        # Tiêu đề biểu đồ
        f'  <text x="{w/2}" y="42" font-family="Times New Roman, Arial" font-size="22" font-weight="bold" text-anchor="middle" fill="#0F172A">SƠ ĐỒ USE CASE CHI TIẾT HỆ THỐNG SMARTMACRO ENGINE</text>',
        f'  <text x="{w/2}" y="68" font-family="Times New Roman, Arial" font-size="13" font-style="italic" text-anchor="middle" fill="#475569">Phân quyền 2 tác nhân chính (User &amp; Admin) với quan hệ liên kết «include» và mở rộng «extend» theo chuẩn UML</text>',

        # System Boundary Box
        f'  <g id="system-boundary">',
        f'    <rect x="280" y="95" width="1140" height="1025" rx="16" fill="#FFFFFF" stroke="#334155" stroke-width="2.5" filter="url(#card-shadow)" />',
        f'    <rect x="280" y="95" width="1140" height="42" rx="16" fill="#1E293B" />',
        f'    <rect x="280" y="115" width="1140" height="22" fill="#1E293B" />',
        f'    <text x="310" y="122" font-family="Times New Roman, Arial" font-size="16" font-weight="bold" fill="#F8FAFC">Ranh giới Hệ thống: SMARTMACRO ENGINE CORE SERVICES</text>',
        f'  </g>',

        # Package Sub-areas inside boundary
        f'  <g id="packages">',
        # Package 1: Auth & User Profile (Top Left)
        f'    <rect x="305" y="150" width="530" height="270" rx="8" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1.2" stroke-dasharray="4,4" />',
        f'    <text x="325" y="172" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#334155">Phân hệ 1: Xác thực &amp; Hồ sơ cá nhân</text>',

        # Package 2: Food & Inventory (Bottom Left)
        f'    <rect x="305" y="440" width="530" height="330" rx="8" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1.2" stroke-dasharray="4,4" />',
        f'    <text x="325" y="462" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#334155">Phân hệ 2: Quản lý Kho thực phẩm &amp; Dinh dưỡng</text>',

        # Package 3: Optimization Engine (Bottom/Center)
        f'    <rect x="305" y="790" width="1090" height="310" rx="8" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1.5" />',
        f'    <text x="325" y="814" font-family="Times New Roman, Arial" font-size="14" font-weight="bold" fill="#166534">Phân hệ 3: Tối ưu hóa Khẩu phần ăn Thông minh (Google OR-Tools GLOP Engine)</text>',

        # Package 4: Admin Management (Top/Mid Right)
        f'    <rect x="860" y="150" width="535" height="620" rx="8" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1.5" />',
        f'    <text x="880" y="172" font-family="Times New Roman, Arial" font-size="14" font-weight="bold" fill="#991B1B">Phân hệ 4: Quản trị Hệ thống (Admin Management)</text>',
        f'  </g>',
    ]

    # Helper: draw stickman actor
    def draw_actor(x, y, label, role_tag="Actor", color="#1E293B"):
        return f"""
        <g id="actor-{label.replace(' ', '_')}">
          <!-- Head -->
          <circle cx="{x}" cy="{y}" r="22" fill="#FFFFFF" stroke="{color}" stroke-width="2.5" />
          <!-- Body -->
          <line x1="{x}" y1="{y+22}" x2="{x}" y2="{y+75}" stroke="{color}" stroke-width="2.5" />
          <!-- Arms -->
          <line x1="{x-32}" y1="{y+42}" x2="{x+32}" y2="{y+42}" stroke="{color}" stroke-width="2.5" />
          <!-- Left Leg -->
          <line x1="{x}" y1="{y+75}" x2="{x-26}" y2="{y+130}" stroke="{color}" stroke-width="2.5" />
          <!-- Right Leg -->
          <line x1="{x}" y1="{y+75}" x2="{x+26}" y2="{y+130}" stroke="{color}" stroke-width="2.5" />
          <!-- Labels -->
          <text x="{x}" y="{y+152}" font-family="Times New Roman, Arial" font-size="16" font-weight="bold" text-anchor="middle" fill="{color}">{label}</text>
          <text x="{x}" y="{y+170}" font-family="Times New Roman, Arial" font-size="12" font-style="italic" text-anchor="middle" fill="#64748B">&lt;&lt;{role_tag}&gt;&gt;</text>
        </g>
        """

    # Actor 1: User (Left) at (130, 420)
    svg.append(draw_actor(130, 430, "Người dùng", "End User", "#2563EB"))
    # Actor 2: Admin (Right) at (1570, 360)
    svg.append(draw_actor(1570, 370, "Quản trị viên", "System Admin", "#DC2626"))

    # Helper: draw use case oval
    def draw_uc(cx, cy, rx, ry, ucid, title, subtitle="", fill="#EFF6FF", stroke="#2563EB"):
        t1_y = cy - 7 if subtitle else cy + 4
        sub_svg = f'<text x="{cx}" y="{cy+13}" font-family="Times New Roman, Arial" font-size="11" text-anchor="middle" fill="#475569">{subtitle}</text>' if subtitle else ""
        return f"""
        <g id="uc-{ucid}">
          <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="1.8" filter="url(#card-shadow)" />
          <text x="{cx}" y="{t1_y}" font-family="Times New Roman, Arial" font-size="12.5" font-weight="bold" text-anchor="middle" fill="#0F172A">{title}</text>
          {sub_svg}
        </g>
        """

    # --- Use cases list ---
    # Phân hệ 1
    svg.append(draw_uc(430, 215, 105, 26, "UC01", "UC01: Đăng nhập", "(Email / Password)"))
    svg.append(draw_uc(710, 215, 105, 26, "UC02", "UC02: Cấp Access JWT", "(&amp; Rotation RefreshToken)"))
    svg.append(draw_uc(430, 290, 105, 26, "UC03", "UC03: Đăng ký tài khoản", "(Tạo tài khoản mới)"))
    svg.append(draw_uc(430, 370, 105, 26, "UC04", "UC04: Quản lý hồ sơ", "(Chỉ số UserBodyMetrics)"))
    svg.append(draw_uc(710, 290, 105, 26, "UC05", "UC05: Đăng xuất hệ thống", "(Thu hồi RefreshToken)"))

    # Phân hệ 2
    svg.append(draw_uc(435, 510, 115, 28, "UC06", "UC06: Quản lý kho thực phẩm", "(UserFoodInventories CRUD)"))
    svg.append(draw_uc(715, 510, 105, 26, "UC07", "UC07: Cảnh báo hạn dùng", "(Lọc thực phẩm sắp hết hạn)"))
    svg.append(draw_uc(435, 600, 115, 28, "UC08", "UC08: Thiết lập mục tiêu ngày", "(DailyTargets Kcal &amp; Macros)"))
    svg.append(draw_uc(715, 600, 105, 26, "UC09", "UC09: Tính macro theo chu kỳ", "(Áp dụng Adjustment Rule)"))
    svg.append(draw_uc(435, 690, 115, 28, "UC10", "UC10: Xem Dashboard Macro", "(Tổng quan Kcal / Carbs / Fat)"))

    # Phân hệ 3 (Optimization)
    svg.append(draw_uc(540, 885, 145, 34, "UC11", "UC11: Tối ưu hóa khẩu phần ăn", "(Google OR-Tools GLOP Solver)", "#DCFCE7", "#16A34A"))
    svg.append(draw_uc(940, 850, 130, 28, "UC12", "UC12: Đọc Daily Target ngày", "(Mục tiêu Kcal &amp; Macro)", "#FFFFFF", "#059669"))
    svg.append(draw_uc(940, 925, 130, 28, "UC13", "UC13: Lọc kho thực phẩm còn tồn", "(QuantityGrams &gt; 0)", "#FFFFFF", "#059669"))
    svg.append(draw_uc(940, 1005, 130, 28, "UC14", "UC14: Lưu vào MealLog", "(Ghi nhận lịch sử bữa ăn)", "#FEF9C3", "#D97706"))

    # Phân hệ 4 (Admin)
    svg.append(draw_uc(1020, 220, 130, 28, "UC15", "UC15: Quản lý danh mục món", "(FoodCategories CRUD)", "#FEE2E2", "#DC2626"))
    svg.append(draw_uc(1020, 310, 130, 28, "UC16", "UC16: Quản trị dữ liệu Foods", "(Cơ sở dữ liệu thực phẩm)", "#FEE2E2", "#DC2626"))
    svg.append(draw_uc(1250, 310, 105, 26, "UC17", "UC17: Duyệt thực phẩm", "(Set is_verified = true)", "#FFFFFF", "#B91C1C"))
    svg.append(draw_uc(1020, 420, 130, 28, "UC18", "UC18: Quản lý người dùng", "(Khóa / Mở tài khoản Users)", "#FEE2E2", "#DC2626"))
    svg.append(draw_uc(1020, 530, 135, 28, "UC19", "UC19: Cấu hình quy tắc Macro", "(MacroAdjustmentRules CRUD)", "#FEE2E2", "#DC2626"))
    svg.append(draw_uc(1020, 640, 135, 28, "UC20", "UC20: Quản lý loại chu kỳ tập", "(TrainingCycleTypes CRUD)", "#FEE2E2", "#DC2626"))

    # Associations & Relations
    svg.append('  <!-- Association Lines -->')
    # User associations
    user_links = [
        (130, 420, 330, 220), # to UC01
        (130, 420, 330, 290), # to UC03
        (130, 440, 330, 370), # to UC04
        (130, 450, 320, 510), # to UC06
        (130, 460, 320, 600), # to UC08
        (130, 480, 320, 690), # to UC10
        (130, 500, 395, 885), # to UC11
    ]
    for x1, y1, x2, y2 in user_links:
        svg.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#2563EB" stroke-width="1.6" />')

    # Admin associations
    admin_links = [
        (1570, 350, 1150, 220), # to UC15
        (1570, 370, 1150, 310), # to UC16
        (1570, 390, 1150, 420), # to UC18
        (1570, 410, 1155, 530), # to UC19
        (1570, 430, 1155, 640), # to UC20
        (1570, 330, 815, 220),  # admin also logs in
    ]
    for x1, y1, x2, y2 in admin_links:
        svg.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#DC2626" stroke-width="1.6" />')

    # Helper: draw stereotyped arrow (include / extend)
    def draw_relation(x1, y1, x2, y2, stereotype="include", label_offset=(0, -10)):
        lx = (x1 + x2) / 2 + label_offset[0]
        ly = (y1 + y2) / 2 + label_offset[1]
        color = "#2563EB" if stereotype == "include" else "#D97706"
        return f"""
        <g>
          <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.5" stroke-dasharray="5,4" marker-end="url(#open-arrow-dashed)" />
          <rect x="{lx-36}" y="{ly-10}" width="72" height="18" rx="3" fill="#FFFFFF" fill-opacity="0.9" />
          <text x="{lx}" y="{ly+3}" font-family="Times New Roman, Arial" font-size="11.5" font-weight="bold" font-style="italic" text-anchor="middle" fill="{color}">«{stereotype}»</text>
        </g>
        """

    # Include / Extend links
    # UC01 -> UC02 (include token generation)
    svg.append(draw_relation(535, 215, 605, 215, "include", (0, -10)))
    # UC01 -> UC05 (extend logout)
    svg.append(draw_relation(535, 225, 615, 280, "extend", (0, -10)))
    # UC06 -> UC07 (extend expiry warning)
    svg.append(draw_relation(550, 510, 610, 510, "extend", (0, -10)))
    # UC08 -> UC09 (include compute from rule)
    svg.append(draw_relation(550, 600, 610, 600, "include", (0, -10)))
    # UC16 -> UC17 (extend verify food)
    svg.append(draw_relation(1150, 310, 1145, 310, "extend", (0, -10)))
    # UC11 -> UC12 (include Read Daily Target)
    svg.append(draw_relation(685, 875, 810, 855, "include", (-10, -12)))
    # UC11 -> UC13 (include Query Available Inventory)
    svg.append(draw_relation(685, 895, 810, 920, "include", (-10, 12)))
    # UC11 -> UC14 (extend Save to MealLog)
    svg.append(draw_relation(665, 915, 815, 995, "extend", (-15, 12)))

    # Legend box
    svg.append(f"""
    <g id="legend" transform="translate(30, 990)">
      <rect width="230" height="130" rx="8" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.2" filter="url(#card-shadow)" />
      <text x="15" y="24" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#0F172A">CHÚ GIẢI KÝ HIỆU UML:</text>
      <line x1="15" y1="46" x2="65" y2="46" stroke="#2563EB" stroke-width="1.6" />
      <text x="75" y="50" font-family="Times New Roman, Arial" font-size="11" fill="#334155">Liên kết tác nhân (Association)</text>
      <line x1="15" y1="72" x2="65" y2="72" stroke="#2563EB" stroke-width="1.5" stroke-dasharray="5,4" />
      <text x="75" y="76" font-family="Times New Roman, Arial" font-size="11" fill="#2563EB">&#171;include&#187; (Quan hệ bắt buộc)</text>
      <line x1="15" y1="98" x2="65" y2="98" stroke="#D97706" stroke-width="1.5" stroke-dasharray="5,4" />
      <text x="75" y="102" font-family="Times New Roman, Arial" font-size="11" fill="#D97706">&#171;extend&#187; (Quan hệ mở rộng)</text>
    </g>
    """)

    svg.append('</svg>')
    out_path = os.path.join(DIAGRAMS_DIR, "fig_3_3_usecase_detailed.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated: {out_path}")

# ==============================================================================
# 2. FIG 3.4: SƠ ĐỒ LỚP (CLASS DIAGRAM 3 TẦNG)
# ==============================================================================
def generate_class_diagram():
    w, h = 1800, 1300
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        f'  <title>Hình 3-4: Sơ đồ lớp (Class Diagram) 3 tầng — SmartMacro Engine</title>',
        COMMON_DEFS,
        f'  <rect width="{w}" height="{h}" fill="#F8FAFC" />',

        # Tiêu đề
        f'  <text x="{w/2}" y="40" font-family="Times New Roman, Arial" font-size="22" font-weight="bold" text-anchor="middle" fill="#0F172A">SƠ ĐỒ LỚP KIẾN TRÚC 3 TẦNG (THREE-TIER CLASS DIAGRAM) — SMARTMACRO ENGINE</text>',
        f'  <text x="{w/2}" y="66" font-family="Times New Roman, Arial" font-size="13" font-style="italic" text-anchor="middle" fill="#475569">Tuân thủ nguyên lý Dependency Inversion: Controller → Service Interface/Impl → Optimization Engine (OR-Tools) → EF Core DbContext</text>',

        # 4 Tiers Containers
        # Tier 1: Presentation Layer / Controllers
        f'  <rect x="40" y="90" width="1720" height="240" rx="10" fill="#FFFBEB" stroke="#FDE68A" stroke-width="1.5" />',
        f'  <text x="60" y="115" font-family="Times New Roman, Arial" font-size="14" font-weight="bold" fill="#92400E">TẦNG 1: PRESENTATION / API CONTROLLERS (ASP.NET Core Web API 8.0 - RESTful endpoints)</text>',

        # Tier 2: Business Logic / Service Layer
        f'  <rect x="40" y="355" width="1720" height="340" rx="10" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1.5" />',
        f'  <text x="60" y="380" font-family="Times New Roman, Arial" font-size="14" font-weight="bold" fill="#1E40AF">TẦNG 2: BUSINESS LOGIC / SERVICE ABSTRACTION &amp; IMPLEMENTATION (DTO Mapping &amp; Business Rules)</text>',

        # Tier 3: Optimization Algorithmic Engine (OR-Tools)
        f'  <rect x="40" y="720" width="860" height="540" rx="10" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1.5" />',
        f'  <text x="60" y="745" font-family="Times New Roman, Arial" font-size="14" font-weight="bold" fill="#166534">TẦNG 3A: ALGORITHMIC OPTIMIZATION ENGINE (Google OR-Tools GLOP Linear Solver)</text>',

        # Tier 4: Data Access / Persistence Layer (EF Core & Entities)
        f'  <rect x="920" y="720" width="840" height="540" rx="10" fill="#FAF5FF" stroke="#E9D5FF" stroke-width="1.5" />',
        f'  <text x="940" y="745" font-family="Times New Roman, Arial" font-size="14" font-weight="bold" fill="#6B21A8">TẦNG 3B: DATA ACCESS LAYER (Entity Framework Core 8.0 &amp; SQL Server Persistence)</text>',
    ]

    # Helper: draw UML Class Box
    def draw_uml_class(x, y, w, header_h, title, stereotype="", attributes=[], methods=[], header_bg="#1E293B", header_fg="#FFFFFF", box_bg="#FFFFFF", border_color="#334155"):
        attr_h = len(attributes) * 17 + (10 if attributes else 0)
        meth_h = len(methods) * 17 + (10 if methods else 0)
        total_h = header_h + attr_h + meth_h + 10

        c_svg = [
            f'<g id="class-{title.replace(" ", "_").replace("<", "").replace(">", "")}">',
            f'  <rect x="{x}" y="{y}" width="{w}" height="{total_h}" rx="6" fill="{box_bg}" stroke="{border_color}" stroke-width="1.5" filter="url(#card-shadow)" />',
            # Header rect
            f'  <path d="M{x},{y+header_h} L{x},{y+6} Q{x},{y} {x+6},{y} L{x+w-6},{y} Q{x+w},{y} {x+w},{y+6} L{x+w},{y+header_h} Z" fill="{header_bg}" />',
        ]
        if stereotype:
            c_svg.append(f'  <text x="{x+w/2}" y="{y+15}" font-family="Times New Roman, Arial" font-size="11" font-style="italic" text-anchor="middle" fill="{header_fg}" fill-opacity="0.85">&lt;&lt;{stereotype}&gt;&gt;</text>')
            c_svg.append(f'  <text x="{x+w/2}" y="{y+32}" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" text-anchor="middle" fill="{header_fg}">{title}</text>')
        else:
            c_svg.append(f'  <text x="{x+w/2}" y="{y+24}" font-family="Times New Roman, Arial" font-size="13.5" font-weight="bold" text-anchor="middle" fill="{header_fg}">{title}</text>')

        # Attributes
        cur_y = y + header_h + 15
        if attributes:
            for attr in attributes:
                c_svg.append(f'  <text x="{x+10}" y="{cur_y}" font-family="Consolas, Courier, monospace" font-size="11" fill="#1E293B">{html.escape(attr)}</text>')
                cur_y += 17
            c_svg.append(f'  <line x1="{x}" y1="{cur_y-5}" x2="{x+w}" y2="{cur_y-5}" stroke="{border_color}" stroke-width="1" />')
            cur_y += 8

        # Methods
        if methods:
            for meth in methods:
                c_svg.append(f'  <text x="{x+10}" y="{cur_y}" font-family="Consolas, Courier, monospace" font-size="11" fill="#1E293B">{html.escape(meth)}</text>')
                cur_y += 17

        c_svg.append('</g>')
        return "\n".join(c_svg), total_h

    # --- TIER 1: CONTROLLERS ---
    # AuthController
    box, _ = draw_uml_class(60, 135, 300, 42, "AuthController", "Controller",
        ["- _authService : IAuthService"],
        ["+ Register(req) : Task<ActionResult>", "+ Login(req) : Task<ActionResult>", "+ Refresh(req) : Task<ActionResult>", "+ Logout(req) : Task<IActionResult>"],
        header_bg="#B45309", border_color="#B45309")
    svg.append(box)

    # InventoryController
    box, _ = draw_uml_class(390, 135, 310, 42, "InventoryController", "Controller",
        ["- _inventoryService : IInventoryService"],
        ["+ GetMyInventory() : Task<ActionResult>", "+ AddItem(req) : Task<ActionResult>", "+ UpdateItem(id, req) : Task<ActionResult>", "+ DeleteItem(id) : Task<IActionResult>"],
        header_bg="#B45309", border_color="#B45309")
    svg.append(box)

    # OptimizationsController (Highlight)
    box, _ = draw_uml_class(730, 135, 330, 42, "OptimizationsController", "Controller",
        ["- _optimizationService : IOptimizationService"],
        ["+ GeneratePlan(req) : Task<ActionResult<OptimizationResultDto>>"],
        header_bg="#047857", border_color="#047857")
    svg.append(box)

    # DailyTargetsController
    box, _ = draw_uml_class(1090, 135, 320, 42, "DailyTargetsController", "Controller",
        ["- _dailyTargetService : IDailyTargetService"],
        ["+ GetMyTargets() : Task<ActionResult>", "+ GetTodayTarget() : Task<ActionResult>", "+ CreateTarget(req) : Task<ActionResult>", "+ UpdateTarget(id, req) : Task<ActionResult>"],
        header_bg="#B45309", border_color="#B45309")
    svg.append(box)

    # FoodsController
    box, _ = draw_uml_class(1440, 135, 300, 42, "FoodsController", "Controller",
        ["- _foodService : IFoodService"],
        ["+ Search(req) : Task<ActionResult>", "+ GetById(id) : Task<ActionResult>", "+ Create(req) : Task<ActionResult>", "+ Update(id, req) : Task<ActionResult>", "+ Delete(id) : Task<IActionResult>"],
        header_bg="#B45309", border_color="#B45309")
    svg.append(box)

    # --- TIER 2: SERVICE INTERFACES & IMPLEMENTATIONS ---
    # IAuthService & AuthService
    box, _ = draw_uml_class(60, 400, 300, 42, "IAuthService", "interface",
        [],
        ["+ RegisterAsync(req) : Task<AuthResponseDto>", "+ LoginAsync(req) : Task<AuthResponseDto>", "+ RefreshTokenAsync(token) : Task<AuthResponseDto>", "+ RevokeTokenAsync(token, userId) : Task"],
        header_bg="#1D4ED8", border_color="#1D4ED8")
    svg.append(box)
    box, _ = draw_uml_class(60, 530, 300, 38, "AuthService", "class",
        ["- _userService : IUserService", "- _dbContext : SmartMacroDbContext"],
        ["+ RegisterAsync(...) : Task", "+ LoginAsync(...) : Task", "+ GenerateJwtToken(...) : (string, DateTime)", "+ HashToken(token) : string"],
        header_bg="#3B82F6", border_color="#3B82F6")
    svg.append(box)

    # IInventoryService & InventoryService
    box, _ = draw_uml_class(390, 400, 310, 42, "IInventoryService", "interface",
        [],
        ["+ GetMyInventoryAsync(userId) : Task<List>", "+ AddItemAsync(userId, req) : Task<ItemDto>", "+ UpdateItemAsync(userId, id, req) : Task", "+ DeleteItemAsync(userId, id) : Task"],
        header_bg="#1D4ED8", border_color="#1D4ED8")
    svg.append(box)
    box, _ = draw_uml_class(390, 530, 310, 38, "InventoryService", "class",
        ["- _db : SmartMacroDbContext", "- _mapper : IMapper"],
        ["+ GetMyInventoryAsync(...) : Task", "+ AddItemAsync(...) : Task", "+ UpdateItemAsync(...) : Task", "+ DeleteItemAsync(...) : Task"],
        header_bg="#3B82F6", border_color="#3B82F6")
    svg.append(box)

    # IOptimizationService & OptimizationService (Centerpiece)
    box, _ = draw_uml_class(730, 400, 330, 42, "IOptimizationService", "interface",
        [],
        ["+ GenerateMealPlanAsync(userId, req) : Task<OptimizationResultDto>"],
        header_bg="#047857", border_color="#047857")
    svg.append(box)
    box, _ = draw_uml_class(730, 515, 330, 38, "OptimizationService", "class",
        ["- _db : SmartMacroDbContext", "- _mapper : IMapper", "- _engine : IMacroOptimizationEngine"],
        ["+ GenerateMealPlanAsync(userId, req) : Task<OptimizationResultDto>"],
        header_bg="#10B981", border_color="#047857")
    svg.append(box)

    # IDailyTargetService & DailyTargetService
    box, _ = draw_uml_class(1090, 400, 320, 42, "IDailyTargetService", "interface",
        [],
        ["+ GetMyTargetsAsync(userId) : Task<List>", "+ GetTodayTargetAsync(userId) : Task<TargetDto>", "+ CreateTargetAsync(userId, req) : Task", "+ UpdateTargetAsync(userId, id, req) : Task"],
        header_bg="#1D4ED8", border_color="#1D4ED8")
    svg.append(box)
    box, _ = draw_uml_class(1090, 530, 320, 38, "DailyTargetService", "class",
        ["- _db : SmartMacroDbContext", "- _mapper : IMapper"],
        ["+ GetMyTargetsAsync(...) : Task", "+ GetTodayTargetAsync(...) : Task", "+ CreateTargetAsync(...) : Task", "+ UpdateTargetAsync(...) : Task"],
        header_bg="#3B82F6", border_color="#3B82F6")
    svg.append(box)

    # IFoodService & FoodService
    box, _ = draw_uml_class(1440, 400, 300, 42, "IFoodService", "interface",
        [],
        ["+ SearchFoodsAsync(req) : Task<PagedResult>", "+ GetFoodByIdAsync(id) : Task<FoodDto>", "+ CreateFoodAsync(req) : Task<FoodDto>", "+ UpdateFoodAsync(id, req) : Task", "+ DeleteFoodAsync(id) : Task"],
        header_bg="#1D4ED8", border_color="#1D4ED8")
    svg.append(box)
    box, _ = draw_uml_class(1440, 545, 300, 38, "FoodService", "class",
        ["- _db : SmartMacroDbContext", "- _mapper : IMapper"],
        ["+ SearchFoodsAsync(...) : Task", "+ GetFoodByIdAsync(...) : Task", "+ CreateFoodAsync(...) : Task"],
        header_bg="#3B82F6", border_color="#3B82F6")
    svg.append(box)

    # --- TIER 3A: CORE OPTIMIZATION ENGINE ---
    # IMacroOptimizationEngine
    box, _ = draw_uml_class(60, 770, 380, 42, "IMacroOptimizationEngine", "interface",
        [],
        ["+ CalculateOptimalMeal(target, inventory) : OptimizationResult"],
        header_bg="#065F46", border_color="#065F46")
    svg.append(box)

    # MacroOptimizationEngine
    box, _ = draw_uml_class(60, 890, 380, 38, "MacroOptimizationEngine", "class",
        ["- const Tolerance : double = 0.05", "- const MinGramsThreshold : double = 0.5"],
        [
            "+ CalculateOptimalMeal(target, inventory) : OptimizationResult",
            "- SolveLinearProgram(target, inventory) : OptimizationResult",
            "- AddMacroConstraint(solver, grams, inv, selector, target, name)",
            "- Fail(message : string) : OptimizationResult"
        ],
        header_bg="#059669", border_color="#059669")
    svg.append(box)

    # Google OR-Tools Solver (External Library Abstraction)
    box, _ = draw_uml_class(60, 1080, 380, 42, "Google.OrTools.LinearSolver.Solver", "external library",
        ["+ CreateSolver(solverType : string) : Solver"],
        [
            "+ MakeNumVar(lb, ub, name) : Variable",
            "+ MakeConstraint(lb, ub, name) : Constraint",
            "+ Objective() : Objective",
            "+ Solve() : ResultStatus"
        ],
        header_bg="#0F766E", border_color="#0F766E")
    svg.append(box)

    # Optimization Result Models
    box, _ = draw_uml_class(480, 770, 390, 38, "OptimizationResult", "class",
        [
            "+ IsSuccessful : bool",
            "+ Message : string",
            "+ TotalKcal : decimal",
            "+ TotalProtein : decimal",
            "+ TotalCarbs : decimal",
            "+ TotalFat : decimal",
            "+ Items : List<OptimizedFoodItem>"
        ],
        [],
        header_bg="#15803D", border_color="#15803D")
    svg.append(box)

    box, _ = draw_uml_class(480, 980, 390, 38, "OptimizedFoodItem", "class",
        [
            "+ FoodId : long",
            "+ FoodName : string",
            "+ CalculatedGrams : decimal"
        ],
        [],
        header_bg="#15803D", border_color="#15803D")
    svg.append(box)

    # --- TIER 3B: DATA ACCESS LAYER (EF CORE) ---
    # SmartMacroDbContext
    box, _ = draw_uml_class(940, 770, 430, 42, "SmartMacroDbContext", "DbContext",
        [
            "+ Users : DbSet<User>",
            "+ RefreshTokens : DbSet<RefreshToken>",
            "+ Foods : DbSet<Food>",
            "+ FoodCategories : DbSet<FoodCategory>",
            "+ UserFoodInventories : DbSet<UserFoodInventory>",
            "+ DailyTargets : DbSet<DailyTarget>",
            "+ MacroAdjustmentRules : DbSet<MacroAdjustmentRule>",
            "+ TrainingCycleTypes : DbSet<TrainingCycleType>",
            "+ UserTrainingSchedules : DbSet<UserTrainingSchedule>"
        ],
        [
            "+ OnModelCreating(modelBuilder : ModelBuilder) : void",
            "+ SaveChangesAsync(cancellationToken) : Task<int>"
        ],
        header_bg="#6B21A8", border_color="#6B21A8")
    svg.append(box)

    # Key Entities in DAL
    box, _ = draw_uml_class(1410, 770, 330, 38, "UserFoodInventory", "entity",
        [
            "+ InventoryId : long  {PK}",
            "+ UserId : long  {FK}",
            "+ FoodId : long  {FK}",
            "+ QuantityGrams : decimal(8,2)",
            "+ ExpiryDate : DateOnly",
            "+ UnitNote : string"
        ],
        [],
        header_bg="#7E22CE", border_color="#7E22CE")
    svg.append(box)

    box, _ = draw_uml_class(1410, 960, 330, 38, "DailyTarget", "entity",
        [
            "+ TargetId : long  {PK}",
            "+ UserId : long  {FK}",
            "+ TargetDate : DateOnly",
            "+ TargetKcal : decimal(7,2)",
            "+ TargetProteinG : decimal(6,2)",
            "+ TargetCarbsG : decimal(6,2)",
            "+ TargetFatG : decimal(6,2)",
            "+ ComputedFromRuleId : short?  {FK}"
        ],
        [],
        header_bg="#7E22CE", border_color="#7E22CE")
    svg.append(box)

    box, _ = draw_uml_class(1410, 1145, 330, 38, "Food", "entity",
        [
            "+ FoodId : long  {PK}",
            "+ FoodName : string",
            "+ CategoryId : short?  {FK}",
            "+ KcalPer100g : decimal(6,2)",
            "+ ProteinGPer100g : decimal(6,2)",
            "+ CarbsGPer100g : decimal(6,2)",
            "+ FatGPer100g : decimal(6,2)"
        ],
        [],
        header_bg="#7E22CE", border_color="#7E22CE")
    svg.append(box)

    # --- CONNECTORS ---
    svg.append('  <!-- UML Dependency & Realization Connectors -->')
    # Realizations (Service -> Interface): dashed line with hollow triangle marker
    realizations = [
        (210, 530, 210, 485),   # AuthService -> IAuthService
        (545, 530, 545, 485),   # InventoryService -> IInventoryService
        (895, 515, 895, 465),   # OptimizationService -> IOptimizationService
        (1250, 530, 1250, 485), # DailyTargetService -> IDailyTargetService
        (1590, 545, 1590, 485), # FoodService -> IFoodService
        (250, 890, 250, 835),   # MacroOptimizationEngine -> IMacroOptimizationEngine
    ]
    for x1, y1, x2, y2 in realizations:
        svg.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#2563EB" stroke-width="1.8" stroke-dasharray="6,4" marker-end="url(#triangle-hollow)" />')

    # Controller -> Service Interface Dependencies
    dependencies = [
        (210, 260, 210, 400),
        (545, 260, 545, 400),
        (895, 220, 895, 400),
        (1250, 260, 1250, 400),
        (1590, 260, 1590, 400),
    ]
    for x1, y1, x2, y2 in dependencies:
        svg.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#B45309" stroke-width="1.6" stroke-dasharray="5,4" marker-end="url(#open-arrow)" />')

    # OptimizationService -> IMacroOptimizationEngine
    svg.append(f'  <path d="M 730 560 L 250 560 L 250 770" fill="none" stroke="#047857" stroke-width="1.8" stroke-dasharray="6,4" marker-end="url(#open-arrow)" />')
    svg.append(f'  <text x="360" y="552" font-family="Times New Roman, Arial" font-size="11" font-weight="bold" fill="#047857">&#171;uses engine&#187;</text>')

    # OptimizationService -> SmartMacroDbContext
    svg.append(f'  <path d="M 1060 560 L 1150 560 L 1150 770" fill="none" stroke="#6B21A8" stroke-width="1.8" stroke-dasharray="6,4" marker-end="url(#open-arrow)" />')
    svg.append(f'  <text x="1160" y="650" font-family="Times New Roman, Arial" font-size="11" font-weight="bold" fill="#6B21A8">&#171;injects context&#187;</text>')

    # MacroOptimizationEngine -> OR-Tools Solver
    svg.append(f'  <line x1="250" y1="1025" x2="250" y2="1080" stroke="#059669" stroke-width="1.8" stroke-dasharray="5,4" marker-end="url(#open-arrow)" />')

    # MacroOptimizationEngine -> OptimizationResult
    svg.append(f'  <line x1="440" y1="920" x2="480" y2="920" stroke="#15803D" stroke-width="1.6" marker-end="url(#arrow-green)" />')
    svg.append(f'  <text x="445" y="910" font-family="Times New Roman, Arial" font-size="10.5" fill="#15803D">returns</text>')

    # OptimizationResult -> OptimizedFoodItem (Composition)
    svg.append(f'  <line x1="675" y1="920" x2="675" y2="980" stroke="#15803D" stroke-width="1.6" marker-end="url(#arrow-green)" />')
    svg.append(f'  <text x="685" y="955" font-family="Times New Roman, Arial" font-size="11" font-weight="bold" fill="#15803D">1..*</text>')

    # SmartMacroDbContext -> Entities
    svg.append(f'  <line x1="1370" y1="840" x2="1410" y2="840" stroke="#6B21A8" stroke-width="1.6" marker-end="url(#arrow)" />')
    svg.append(f'  <line x1="1370" y1="980" x2="1410" y2="980" stroke="#6B21A8" stroke-width="1.6" marker-end="url(#arrow)" />')

    svg.append('</svg>')
    out_path = os.path.join(DIAGRAMS_DIR, "fig_3_4_class_diagram.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated: {out_path}")

# ==============================================================================
# 3. FIG 3.5: SEQUENCE DIAGRAM (LOGIN & INVENTORY MANAGEMENT)
# ==============================================================================
def generate_sequence_login_and_inventory():
    w, h = 1650, 1180
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        f'  <title>Hình 3-5: Sơ đồ tuần tự Đăng nhập &amp; Quản lý kho thực phẩm — SmartMacro Engine</title>',
        COMMON_DEFS,
        f'  <rect width="{w}" height="{h}" fill="#F8FAFC" />',

        # Title
        f'  <text x="{w/2}" y="38" font-family="Times New Roman, Arial" font-size="21" font-weight="bold" text-anchor="middle" fill="#0F172A">SƠ ĐỒ TUẦN TỰ: ĐĂNG NHẬP, CẤP JWT TOKEN &amp; QUẢN LÝ KHO THỰC PHẨM CÁ NHÂN</text>',
        f'  <text x="{w/2}" y="62" font-family="Times New Roman, Arial" font-size="13" font-style="italic" text-anchor="middle" fill="#475569">Mô hình tuần tự tương tác từ Client SPA → Auth/Inventory Controllers → Services → SQL Server DbContext</text>',
    ]

    # Lifelines columns:
    # 1. Actor User: x = 120
    # 2. WebClient (SPA/React): x = 320
    # 3. AuthController: x = 540
    # 4. AuthService: x = 760
    # 5. InventoryController: x = 990
    # 6. InventoryService: x = 1230
    # 7. SmartMacroDbContext (DB): x = 1490
    lifelines = [
        ("User", 120, "Người dùng\n(User)", "#1E293B"),
        ("WebClient", 320, "Web Browser\n(SPA Client)", "#2563EB"),
        ("AuthController", 540, "AuthController\n(API Controller)", "#B45309"),
        ("AuthService", 760, "AuthService\n(Business Service)", "#047857"),
        ("InventoryController", 1010, "InventoryController\n(API Controller)", "#B45309"),
        ("InventoryService", 1260, "InventoryService\n(Business Service)", "#047857"),
        ("DbContext", 1510, "SmartMacroDbContext\n(SQL Server DB)", "#6B21A8"),
    ]

    top_y = 100
    bottom_y = 1110

    # Draw Lifeline Headers & Vertical Dashed Lines
    for code, x, label, color in lifelines:
        lines = label.split("\n")
        svg.append(f"""
        <g id="lifeline-{code}">
          <rect x="{x-70}" y="{top_y}" width="140" height="50" rx="6" fill="#FFFFFF" stroke="{color}" stroke-width="2" filter="url(#card-shadow)" />
          <text x="{x}" y="{top_y+20}" font-family="Times New Roman, Arial" font-size="12.5" font-weight="bold" text-anchor="middle" fill="{color}">{lines[0]}</text>
          <text x="{x}" y="{top_y+36}" font-family="Times New Roman, Arial" font-size="11" text-anchor="middle" fill="#64748B">{lines[1]}</text>
          <line x1="{x}" y1="{top_y+50}" x2="{x}" y2="{bottom_y}" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="6,4" />
        </g>
        """)

    # Section Headers (Dividers)
    # Phase 1: Authentication & Token Issuance (y: 170 -> 560)
    svg.append(f"""
    <g id="phase-1-login">
      <rect x="50" y="170" width="1550" height="400" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" />
      <rect x="50" y="170" width="480" height="28" rx="8" fill="#1E3A8A" />
      <text x="65" y="189" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#FFFFFF">GIAI ĐOẠN 1: ĐĂNG NHẬP &amp; CẤP PHÁT CẶP ACCESS / REFRESH TOKEN</text>
    </g>
    """)

    # Phase 2: Inventory Management with Bearer Token (y: 600 -> 1080)
    svg.append(f"""
    <g id="phase-2-inventory">
      <rect x="50" y="590" width="1550" height="500" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" />
      <rect x="50" y="590" width="480" height="28" rx="8" fill="#065F46" />
      <text x="65" y="609" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" fill="#FFFFFF">GIAI ĐOẠN 2: QUẢN LÝ KHO THỰC PHẨM TỦ LẠNH VỚI BEARER JWT</text>
    </g>
    """)

    # Helper: message arrow
    def draw_msg(x1, y1, x2, y2, text, is_return=False, color="#1E293B"):
        dash = ' stroke-dasharray="5,4"' if is_return else ""
        marker = 'url(#arrow)' if not is_return else 'url(#open-arrow)'
        mid_x = (x1 + x2) / 2
        return f"""
        <g>
          <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.5"{dash} marker-end="{marker}" />
          <text x="{mid_x}" y="{y1-6}" font-family="Consolas, 'Times New Roman', monospace" font-size="11.5" text-anchor="middle" fill="{color}">{html.escape(text)}</text>
        </g>
        """

    # Helper: activation box
    def draw_activation(x, y, h, color="#2563EB"):
        return f'<rect x="{x-7}" y="{y}" width="14" height="{h}" rx="2" fill="#E2E8F0" stroke="{color}" stroke-width="1.5" />'

    # --- Phase 1 Messages ---
    svg.append(draw_activation(120, 215, 330, "#1E293B"))
    svg.append(draw_activation(320, 225, 310, "#2563EB"))
    svg.append(draw_activation(540, 245, 270, "#B45309"))
    svg.append(draw_activation(760, 260, 240, "#047857"))
    svg.append(draw_activation(1510, 280, 50, "#6B21A8"))
    svg.append(draw_activation(1510, 430, 45, "#6B21A8"))

    svg.append(draw_msg(120, 225, 320, 225, "1: Nhập email & password, bấm 'Đăng nhập'"))
    svg.append(draw_msg(320, 245, 540, 245, "2: POST /api/auth/login (LoginRequestDto)"))
    svg.append(draw_msg(540, 260, 760, 260, "3: LoginAsync(request)"))
    svg.append(draw_msg(760, 280, 1510, 280, "4: Users.FirstOrDefaultAsync(u => u.Email == email)"))
    svg.append(draw_msg(1510, 315, 760, 315, "5: return User (kèm PasswordHash)", is_return=True))

    # Self call in AuthService: BCrypt.Verify
    svg.append(f"""
    <g>
      <path d="M 767 340 L 820 340 L 820 365 L 767 365" fill="none" stroke="#047857" stroke-width="1.5" marker-end="url(#arrow)" />
      <text x="828" y="357" font-family="Consolas, monospace" font-size="11" fill="#047857">6: BCrypt.Verify(password, hash)</text>
    </g>
    """)

    # Self call in AuthService: Generate Tokens
    svg.append(f"""
    <g>
      <path d="M 767 385 L 830 385 L 830 410 L 767 410" fill="none" stroke="#047857" stroke-width="1.5" marker-end="url(#arrow)" />
      <text x="838" y="402" font-family="Consolas, monospace" font-size="11" fill="#047857">7: GenerateJwtToken() &amp; GenerateRefreshToken()</text>
    </g>
    """)

    svg.append(draw_msg(760, 435, 1510, 435, "8: RefreshTokens.Add(TokenHash, ExpiresAt) & SaveChangesAsync()"))
    svg.append(draw_msg(1510, 470, 760, 470, "9: DB Commit Success", is_return=True))
    svg.append(draw_msg(760, 495, 540, 495, "10: return AuthResponseDto(AccessToken, RefreshToken)", is_return=True))
    svg.append(draw_msg(540, 520, 320, 520, "11: HTTP 200 OK (Tokens, UserId, FullName)", is_return=True, color="#059669"))
    svg.append(draw_msg(320, 545, 120, 545, "12: Hiển thị Dashboard & lưu Token vào authStore", is_return=True))

    # --- Phase 2 Messages ---
    svg.append(draw_activation(120, 640, 420, "#1E293B"))
    svg.append(draw_activation(320, 650, 400, "#2563EB"))
    svg.append(draw_activation(1010, 670, 350, "#B45309"))
    svg.append(draw_activation(1260, 695, 310, "#047857"))
    svg.append(draw_activation(1510, 750, 40, "#6B21A8"))
    svg.append(draw_activation(1510, 830, 40, "#6B21A8"))
    svg.append(draw_activation(1510, 915, 45, "#6B21A8"))

    svg.append(draw_msg(120, 650, 320, 650, "13: Thêm 500g Ức gà (Hạn: 15/11) vào tủ lạnh"))
    svg.append(draw_msg(320, 670, 1010, 670, "14: POST /api/inventory [Bearer JWT] (CreateInventoryItemRequestDto)"))

    # Controller extracts claims
    svg.append(f"""
    <g>
      <path d="M 1017 685 L 1080 685 L 1080 705 L 1017 705" fill="none" stroke="#B45309" stroke-width="1.5" marker-end="url(#arrow)" />
      <text x="1088" y="700" font-family="Consolas, monospace" font-size="11" fill="#B45309">15: Extract userId từ Claims (Sub)</text>
    </g>
    """)

    svg.append(draw_msg(1010, 720, 1260, 720, "16: AddItemAsync(userId, requestDto)"))
    svg.append(draw_msg(1260, 750, 1510, 750, "17: Foods.FindAsync(request.FoodId) [Validate thực phẩm]"))
    svg.append(draw_msg(1510, 785, 1260, 785, "18: return Food entity (Hợp lệ)", is_return=True))

    svg.append(draw_msg(1260, 830, 1510, 830, "19: UserFoodInventories.FirstOrDefaultAsync(u, f, expiry) [Check trùng]"))
    svg.append(draw_msg(1510, 865, 1260, 865, "20: return null (Món mới chưa có trong kho)", is_return=True))

    svg.append(draw_msg(1260, 915, 1510, 915, "21: UserFoodInventories.Add(new Item) & SaveChangesAsync()"))
    svg.append(draw_msg(1510, 955, 1260, 955, "22: Commit DB thành công (Tạo InventoryId mới)", is_return=True))

    svg.append(draw_msg(1260, 985, 1010, 985, "23: return InventoryItemResponseDto (AutoMapper)", is_return=True))
    svg.append(draw_msg(1010, 1015, 320, 1015, "24: HTTP 201 CreatedAtAction (InventoryItemResponseDto)", is_return=True, color="#059669"))
    svg.append(draw_msg(320, 1045, 120, 1045, "25: Cập nhật giao diện Tủ lạnh cá nhân & hiển thị Badge hạn dùng", is_return=True))

    svg.append('</svg>')
    out_path = os.path.join(DIAGRAMS_DIR, "fig_3_5_sequence_login_and_inventory.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated: {out_path}")

# ==============================================================================
# 4. FIG 3.6: SEQUENCE DIAGRAM (OPTIMIZATION WITH GOOGLE OR-TOOLS)
# ==============================================================================
def generate_sequence_optimization():
    w, h = 1750, 1250
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        f'  <title>Hình 3-6: Sơ đồ tuần tự Tối ưu hóa thực đơn với Google OR-Tools — SmartMacro Engine</title>',
        COMMON_DEFS,
        f'  <rect width="{w}" height="{h}" fill="#F8FAFC" />',

        # Tiêu đề
        f'  <text x="{w/2}" y="38" font-family="Times New Roman, Arial" font-size="21" font-weight="bold" text-anchor="middle" fill="#0F172A">SƠ ĐỒ TUẦN TỰ: GIẢI BÀI TOÁN TỐI ƯU HÓA KHẨU PHẦN ĂN VỚI GOOGLE OR-TOOLS</text>',
        f'  <text x="{w/2}" y="62" font-family="Times New Roman, Arial" font-size="13" font-style="italic" text-anchor="middle" fill="#475569">Mô hình tuần tự chi tiết luồng xử lý từ Client → OptimizationsController → OptimizationService → OR-Tools GLOP Solver</text>',
    ]

    # Lifelines columns:
    # 1. User: 110
    # 2. WebClient: 290
    # 3. OptimizationsController: 520
    # 4. OptimizationService: 770
    # 5. SmartMacroDbContext: 1040
    # 6. MacroOptimizationEngine: 1330
    # 7. GLOP Solver: 1610
    lifelines = [
        ("User", 110, "Người dùng\n(User)", "#1E293B"),
        ("WebClient", 290, "Web Browser\n(SPA React)", "#2563EB"),
        ("OptController", 520, "OptimizationsController\n(API Controller)", "#047857"),
        ("OptService", 770, "OptimizationService\n(Business Service)", "#047857"),
        ("DbContext", 1040, "SmartMacroDbContext\n(SQL Server)", "#6B21A8"),
        ("Engine", 1330, "MacroOptimizationEngine\n(Core LP Engine)", "#059669"),
        ("GLOPSolver", 1610, "Google.OrTools\n(GLOP Linear Solver)", "#0F766E"),
    ]

    top_y = 95
    bottom_y = 1180

    for code, x, label, color in lifelines:
        lines = label.split("\n")
        svg.append(f"""
        <g id="lifeline-{code}">
          <rect x="{x-75}" y="{top_y}" width="150" height="50" rx="6" fill="#FFFFFF" stroke="{color}" stroke-width="2" filter="url(#card-shadow)" />
          <text x="{x}" y="{top_y+20}" font-family="Times New Roman, Arial" font-size="12.5" font-weight="bold" text-anchor="middle" fill="{color}">{lines[0]}</text>
          <text x="{x}" y="{top_y+36}" font-family="Times New Roman, Arial" font-size="11" text-anchor="middle" fill="#64748B">{lines[1]}</text>
          <line x1="{x}" y1="{top_y+50}" x2="{x}" y2="{bottom_y}" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="6,4" />
        </g>
        """)

    # Helper: message arrow
    def draw_msg(x1, y1, x2, y2, text, is_return=False, color="#1E293B"):
        dash = ' stroke-dasharray="5,4"' if is_return else ""
        marker = 'url(#arrow)' if not is_return else 'url(#open-arrow)'
        mid_x = (x1 + x2) / 2
        return f"""
        <g>
          <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.5"{dash} marker-end="{marker}" />
          <text x="{mid_x}" y="{y1-6}" font-family="Consolas, 'Times New Roman', monospace" font-size="11.5" text-anchor="middle" fill="{color}">{html.escape(text)}</text>
        </g>
        """

    def draw_activation(x, y, h, color="#047857"):
        return f'<rect x="{x-7}" y="{y}" width="14" height="{h}" rx="2" fill="#E2E8F0" stroke="{color}" stroke-width="1.5" />'

    # Activations
    svg.append(draw_activation(110, 170, 950, "#1E293B"))
    svg.append(draw_activation(290, 185, 920, "#2563EB"))
    svg.append(draw_activation(520, 205, 875, "#047857"))
    svg.append(draw_activation(770, 230, 835, "#047857"))
    svg.append(draw_activation(1040, 260, 50, "#6B21A8"))
    svg.append(draw_activation(1040, 360, 50, "#6B21A8"))
    svg.append(draw_activation(1330, 480, 480, "#059669"))
    svg.append(draw_activation(1610, 520, 370, "#0F766E"))

    # Sequence Messages
    svg.append(draw_msg(110, 185, 290, 185, "1: Chọn mục tiêu & thực phẩm kho, bấm 'Tối ưu hóa khẩu phần'"))
    svg.append(draw_msg(290, 205, 520, 205, "2: POST /api/optimizations/generate-plan (DailyTargetId, IncludeFoodIds)"))

    # Controller extracts claims
    svg.append(f"""
    <g>
      <path d="M 527 215 L 590 215 L 590 235 L 527 235" fill="none" stroke="#047857" stroke-width="1.5" marker-end="url(#arrow)" />
      <text x="598" y="230" font-family="Consolas, monospace" font-size="11" fill="#047857">3: userId = User.FindFirstValue(Sub)</text>
    </g>
    """)

    svg.append(draw_msg(520, 245, 770, 245, "4: GenerateMealPlanAsync(userId, request)"))

    # 1. Query DailyTargets
    svg.append(draw_msg(770, 265, 1040, 265, "5: DailyTargets.Where(u => u.UserId == userId &amp;&amp; TargetDate == today)"))
    svg.append(draw_msg(1040, 305, 770, 305, "6: return DailyTargetDto (Kcal: 2200, P: 150g, C: 220g, F: 55g)", is_return=True))

    # 2. Query UserFoodInventories
    svg.append(draw_msg(770, 360, 1040, 360, "7: UserFoodInventories.Where(QuantityGrams > 0).ProjectTo<InventoryItemDto>()"))
    svg.append(draw_msg(1040, 405, 770, 405, "8: return List<InventoryItemResponseDto> (Danh sách nguyên liệu tồn kho)", is_return=True))

    # Guard check note
    svg.append(f"""
    <g id="note-guard" transform="translate(680, 420)">
      <rect width="250" height="34" rx="4" fill="#FEF3C7" stroke="#D97706" stroke-width="1.2" />
      <text x="125" y="16" font-family="Times New Roman, Arial" font-size="11" font-weight="bold" text-anchor="middle" fill="#92400E">Kiểm tra điều kiện biên (Guards):</text>
      <text x="125" y="28" font-family="Times New Roman, Arial" font-size="10.5" text-anchor="middle" fill="#78350F">Target != null &amp;&amp; Inventory.Count &gt; 0</text>
    </g>
    """)

    # 3. Call Optimization Engine
    svg.append(draw_msg(770, 485, 1330, 485, "9: CalculateOptimalMeal(targetDto, availableInventory)"))

    # Engine creates GLOP solver
    svg.append(draw_msg(1330, 520, 1610, 520, "10: Solver.CreateSolver('GLOP')"))
    svg.append(draw_msg(1610, 550, 1330, 550, "11: return Solver instance", is_return=True))

    # Engine defines variables & constraints
    svg.append(draw_msg(1330, 580, 1610, 580, "12: MakeNumVar(0.0, QuantityGrams[i], 'grams_i') cho n thực phẩm"))
    svg.append(draw_msg(1330, 620, 1610, 620, "13: AddMacroConstraint(Protein, Carbs, Fat) với Tolerance ±5%"))
    svg.append(draw_msg(1330, 660, 1610, 660, "14: MakeNumVar(0, +Inf, 'deviation') &amp; Tuyến tính hóa sai lệch Kcal"))
    svg.append(draw_msg(1330, 700, 1610, 700, "15: Objective.SetMinimization() sai lệch Kcal"))

    # Solve
    svg.append(draw_msg(1330, 745, 1610, 745, "16: Solve() [Thực thi thuật toán Simplex / Interior Point]"))
    svg.append(draw_msg(1610, 790, 1330, 790, "17: return Solver.ResultStatus.OPTIMAL", is_return=True, color="#059669"))

    # Extract solution
    svg.append(f"""
    <g>
      <path d="M 1337 810 L 1420 810 L 1420 840 L 1337 840" fill="none" stroke="#059669" stroke-width="1.5" marker-end="url(#arrow)" />
      <text x="1430" y="825" font-family="Consolas, monospace" font-size="10.5" fill="#059669">18: Lọc grams[i] &gt;= 0.5g,</text>
      <text x="1430" y="838" font-family="Consolas, monospace" font-size="10.5" fill="#059669">    tính Total Kcal/P/C/F</text>
    </g>
    """)

    svg.append(draw_msg(1330, 870, 770, 870, "19: return OptimizationResult(IsSuccessful=true, TotalMacros, Items)", is_return=True))

    # Service maps to DTO
    svg.append(f"""
    <g>
      <path d="M 777 890 L 860 890 L 860 920 L 777 920" fill="none" stroke="#047857" stroke-width="1.5" marker-end="url(#arrow)" />
      <text x="870" y="905" font-family="Consolas, monospace" font-size="10.5" fill="#047857">20: Map DTO: SolverStatus='OPTIMAL',</text>
      <text x="870" y="918" font-family="Consolas, monospace" font-size="10.5" fill="#047857">    Target vs Achieved Macro, Items</text>
    </g>
    """)

    svg.append(draw_msg(770, 950, 520, 950, "21: return OptimizationResultDto", is_return=True))
    svg.append(draw_msg(520, 985, 290, 985, "22: HTTP 200 OK (OptimizationResultDto JSON)", is_return=True, color="#059669"))
    svg.append(draw_msg(290, 1025, 110, 1025, "23: Render bảng định lượng gam thực phẩm & Biểu đồ tiến độ Macro", is_return=True))

    # Notes about Infeasible branch
    svg.append(f"""
    <g id="alt-infeasible" transform="translate(110, 1075)">
      <rect width="1580" height="75" rx="6" fill="#FEF2F2" stroke="#DC2626" stroke-width="1.2" stroke-dasharray="4,4" />
      <text x="20" y="24" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#991B1B">NHÁNH RẼ THẤT BẠI (INFEASIBLE BRANCH):</text>
      <text x="20" y="44" font-family="Times New Roman, Arial" font-size="11.5" fill="#7F1D1D">Nếu kho thực phẩm không đủ nguyên liệu đáp ứng đồng thời cả 3 ràng buộc Protein, Carbs, Fat trong ngưỡng ±5%:</text>
      <text x="20" y="62" font-family="Consolas, monospace" font-size="11" fill="#991B1B">→ SolverStatus = 'INFEASIBLE' | Message = 'Kho thực phẩm hiện tại không đủ để đáp ứng mục tiêu' | HTTP 200 kèm khuyến nghị bổ sung nguyên liệu.</text>
    </g>
    """)

    svg.append('</svg>')
    out_path = os.path.join(DIAGRAMS_DIR, "fig_3_6_sequence_optimization.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated: {out_path}")

# ==============================================================================
# 5. FIG 3.7: ACTIVITY DIAGRAM (OPTIMIZATION ALGORITHM & INFEASIBLE HANDLING)
# ==============================================================================
def generate_activity_optimization():
    w, h = 1350, 1500
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        f'  <title>Hình 3-7: Sơ đồ hoạt động (Activity Diagram) giải thuật tối ưu hóa khẩu phần — SmartMacro Engine</title>',
        COMMON_DEFS,
        f'  <rect width="{w}" height="{h}" fill="#F8FAFC" />',

        # Tiêu đề
        f'  <text x="{w/2}" y="38" font-family="Times New Roman, Arial" font-size="21" font-weight="bold" text-anchor="middle" fill="#0F172A">SƠ ĐỒ HOẠT ĐỘNG: GIẢI THUẬT QUY HOẠCH TUYẾN TÍNH &amp; XỬ LÝ NGHIỆM TỐI ƯU</text>',
        f'  <text x="{w/2}" y="62" font-family="Times New Roman, Arial" font-size="13" font-style="italic" text-anchor="middle" fill="#475569">Mô hình hoạt động (Activity Diagram) thể hiện tiền điều kiện, khởi tạo solver, thiết lập ràng buộc và phân nhánh OPTIMAL / INFEASIBLE</text>',
    ]

    # Helper: draw start node (solid circle)
    def draw_start_node(cx, cy):
        return f'<circle cx="{cx}" cy="{cy}" r="14" fill="#0F172A" stroke="#334155" stroke-width="2" />'

    # Helper: draw end node (bullseye)
    def draw_end_node(cx, cy):
        return f"""
        <g>
          <circle cx="{cx}" cy="{cy}" r="16" fill="#FFFFFF" stroke="#0F172A" stroke-width="2" />
          <circle cx="{cx}" cy="{cy}" r="10" fill="#0F172A" />
        </g>
        """

    # Helper: draw action state (rounded rectangle)
    def draw_action(cx, cy, w, h, text1, text2="", fill="#F0FDF4", stroke="#16A34A"):
        t1_y = cy - 7 if text2 else cy + 4
        sub = f'<text x="{cx}" y="{cy+13}" font-family="Times New Roman, Arial" font-size="11.5" text-anchor="middle" fill="#475569">{text2}</text>' if text2 else ""
        return f"""
        <g id="action-{text1.replace(' ', '_')}">
          <rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.6" filter="url(#card-shadow)" />
          <text x="{cx}" y="{t1_y}" font-family="Times New Roman, Arial" font-size="13" font-weight="bold" text-anchor="middle" fill="#0F172A">{text1}</text>
          {sub}
        </g>
        """

    # Helper: draw decision diamond
    def draw_decision(cx, cy, rx, ry, question):
        return f"""
        <g id="decision-{question.replace(' ', '_')}">
          <polygon points="{cx},{cy-ry} {cx+rx},{cy} {cx},{cy+ry} {cx-rx},{cy}" fill="#FEF9C3" stroke="#CA8A04" stroke-width="1.8" filter="url(#card-shadow)" />
          <text x="{cx}" y="{cy+4}" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#713F12">{question}</text>
        </g>
        """

    # Helper: draw vertical arrow
    def draw_arrow(x1, y1, x2, y2, label=""):
        lbl_svg = ""
        if label:
            mid_y = (y1 + y2) / 2
            lbl_svg = f'<text x="{x1+10}" y="{mid_y}" font-family="Times New Roman, Arial" font-size="11.5" font-weight="bold" fill="#1E293B">{label}</text>'
        return f"""
        <g>
          <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#1E293B" stroke-width="1.6" marker-end="url(#arrow)" />
          {lbl_svg}
        </g>
        """

    # Main Center Column at cx = 675
    cx = 675

    # 1. Start Node
    svg.append(draw_start_node(cx, 105))
    svg.append(draw_arrow(cx, 119, cx, 150))

    # 2. Action: Nhận yêu cầu tối ưu hóa
    svg.append(draw_action(cx, 175, 420, 50, "Tiếp nhận yêu cầu tối ưu hóa", "POST /api/optimizations/generate-plan (userId, request)"))
    svg.append(draw_arrow(cx, 200, cx, 235))

    # 3. Action: Query DailyTargets
    svg.append(draw_action(cx, 260, 420, 50, "Truy vấn mục tiêu dinh dưỡng ngày", "Đọc DailyTargets theo userId và TargetDate (hôm nay)"))
    svg.append(draw_arrow(cx, 285, cx, 320))

    # 4. Decision: Tìm thấy DailyTarget?
    svg.append(draw_decision(cx, 350, 120, 30, "Tìm thấy mục tiêu?"))

    # Branch: Không -> Ném ngoại lệ NotFoundException (Side right)
    svg.append(f"""
    <g>
      <line x1="{cx+120}" y1="350" x2="1050" y2="350" stroke="#DC2626" stroke-width="1.6" marker-end="url(#arrow-red)" />
      <text x="750" y="342" font-family="Times New Roman, Arial" font-size="11.5" font-weight="bold" fill="#DC2626">[Không]</text>
    </g>
    """)
    svg.append(draw_action(1150, 350, 200, 46, "NotFoundException", "Trả về mã HTTP 404", fill="#FEF2F2", stroke="#DC2626"))
    svg.append(f'<line x1="1250" y1="350" x2="1290" y2="350" stroke="#DC2626" stroke-width="1.6" marker-end="url(#arrow-red)" />')
    svg.append(draw_end_node(1310, 350))

    # Branch: Có -> Tiếp tục
    svg.append(draw_arrow(cx, 380, cx, 420, "[Có]"))

    # 5. Action: Query UserFoodInventories
    svg.append(draw_action(cx, 445, 420, 50, "Truy vấn kho thực phẩm khả dụng", "Lọc UserFoodInventories có QuantityGrams &gt; 0"))
    svg.append(draw_arrow(cx, 470, cx, 505))

    # 6. Decision: Kho có thực phẩm?
    svg.append(draw_decision(cx, 535, 120, 30, "Kho có thực phẩm?"))

    # Branch: Không -> Ném EmptyInventoryException
    svg.append(f"""
    <g>
      <line x1="{cx+120}" y1="535" x2="1050" y2="535" stroke="#DC2626" stroke-width="1.6" marker-end="url(#arrow-red)" />
      <text x="750" y="527" font-family="Times New Roman, Arial" font-size="11.5" font-weight="bold" fill="#DC2626">[Không - Kho rỗng]</text>
    </g>
    """)
    svg.append(draw_action(1150, 535, 200, 46, "EmptyInventoryException", "Trả về mã HTTP 400", fill="#FEF2F2", stroke="#DC2626"))
    svg.append(f'<line x1="1250" y1="535" x2="1290" y2="535" stroke="#DC2626" stroke-width="1.6" marker-end="url(#arrow-red)" />')
    svg.append(draw_end_node(1310, 535))

    # Branch: Có -> Khởi tạo OR-Tools
    svg.append(draw_arrow(cx, 565, cx, 605, "[Có nguyên liệu]"))

    # 7. Action: Khởi tạo GLOP
    svg.append(draw_action(cx, 630, 460, 50, "Khởi tạo Google OR-Tools Solver", "Solver.CreateSolver('GLOP') chuyên giải LP liên tục", fill="#E0F2FE", stroke="#0284C7"))
    svg.append(draw_arrow(cx, 655, cx, 690))

    # 8. Action: Định nghĩa biến quyết định
    svg.append(draw_action(cx, 715, 460, 50, "Định nghĩa Biến quyết định (Decision Variables)", "grams[i] ∈ [0.0, QuantityGrams[i]] cho từng món i trong kho", fill="#E0F2FE", stroke="#0284C7"))
    svg.append(draw_arrow(cx, 740, cx, 775))

    # 9. Action: Thiết lập ràng buộc Macro
    svg.append(draw_action(cx, 805, 520, 60, "Thiết lập hệ ràng buộc Macro (Tolerance ±5%)", "0.95 × Target ≤ Σ (grams[i] × Macro[i] / 100) ≤ 1.05 × Target\n(Áp dụng cho 3 phương trình: Protein, Carbs, Fat)", fill="#E0F2FE", stroke="#0284C7"))
    svg.append(draw_arrow(cx, 835, cx, 875))

    # 10. Action: Tuyến tính hóa hàm mục tiêu
    svg.append(draw_action(cx, 905, 520, 60, "Tuyến tính hóa sai lệch Kcal &amp; Hàm mục tiêu", "Biến phụ deviation ≥ |TotalKcal - TargetKcal|\nHàm mục tiêu: Minimize (deviation)", fill="#E0F2FE", stroke="#0284C7"))
    svg.append(draw_arrow(cx, 935, cx, 975))

    # 11. Action: Thực thi Solver
    svg.append(draw_action(cx, 1005, 460, 60, "Thực thi giải bài toán: solver.Solve()", "Sử dụng thuật toán Primal/Dual Simplex", fill="#FEF3C7", stroke="#D97706"))
    svg.append(draw_arrow(cx, 1035, cx, 1075))

    # 12. Decision: Kiểm tra trạng thái nghiệm Solver
    svg.append(draw_decision(cx, 1110, 140, 35, "Kiểm tra Solver Status?"))

    # Branch Left: INFEASIBLE (Không tìm thấy nghiệm)
    svg.append(f"""
    <g>
      <polyline points="{cx-140},1110 320,1110 320,1160" fill="none" stroke="#DC2626" stroke-width="1.6" marker-end="url(#arrow-red)" />
      <text x="420" y="1102" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#DC2626">[INFEASIBLE / Không khả thi]</text>
    </g>
    """)

    svg.append(draw_action(320, 1200, 340, 65, "Xử lý trạng thái Không khả thi", "Gán SolverStatus = 'INFEASIBLE'\nItems = [] (Kho không đủ nguyên liệu đáp ứng ±5%)\nKhuyến nghị bổ sung nguyên liệu protein/carbs", fill="#FEF2F2", stroke="#DC2626"))

    # Branch Down/Right: OPTIMAL or FEASIBLE
    svg.append(f"""
    <g>
      <polyline points="{cx+140},1110 1020,1110 1020,1160" fill="none" stroke="#16A34A" stroke-width="1.6" marker-end="url(#arrow-green)" />
      <text x="910" y="1102" font-family="Times New Roman, Arial" font-size="12" font-weight="bold" fill="#16A34A">[OPTIMAL / FEASIBLE]</text>
    </g>
    """)

    svg.append(draw_action(1020, 1200, 380, 65, "Xử lý nghiệm Tối ưu / Khả thi", "Lọc biến: grams[i] ≥ 0.5g (loại bỏ nhiễu số học)\nLàm tròn 2 chữ số thập phân\nTính tổng macro và Kcal thực tế đạt được", fill="#DCFCE7", stroke="#16A34A"))

    # Merge Node (horizontal bar)
    merge_y = 1320
    svg.append(f"""
    <g id="merge-node">
      <polyline points="320,1233 320,1320 550,1320" fill="none" stroke="#1E293B" stroke-width="1.6" />
      <polyline points="1020,1233 1020,1320 800,1320" fill="none" stroke="#1E293B" stroke-width="1.6" />
      <rect x="550" y="1317" width="250" height="6" rx="3" fill="#1E293B" />
    </g>
    """)
    svg.append(draw_arrow(cx, merge_y+3, cx, 1365))

    # 13. Action: Đóng gói và trả kết quả
    svg.append(draw_action(cx, 1395, 460, 60, "Đóng gói OptimizationResultDto", "Bao gồm SolverStatus, TargetMacros, AchievedMacros, AllocatedItems\nTrả về HTTP 200 OK cho Client", fill="#F8FAFC", stroke="#334155"))
    svg.append(draw_arrow(cx, 1425, cx, 1465))

    # 14. Final End Node
    svg.append(draw_end_node(cx, 1480))

    svg.append('</svg>')
    out_path = os.path.join(DIAGRAMS_DIR, "fig_3_7_activity_optimization.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated: {out_path}")


def main():
    print("Generating UML Diagrams for Thesis Chapter 3...")
    generate_usecase_diagram()
    generate_class_diagram()
    generate_sequence_login_and_inventory()
    generate_sequence_optimization()
    generate_activity_optimization()
    print("Done generating all 5 UML diagrams.")

if __name__ == "__main__":
    main()
