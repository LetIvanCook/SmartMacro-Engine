# HƯỚNG DẪN DEMO 5 PHÚT & CẨM NANG VẤN ĐÁP BUỔI 4/10 (CHEAT SHEET)

> **Dành cho:** Sinh viên CNTT Năm 4 — Học phần Thực tập Chuyên ngành (Buổi 4/10)  
> **Đề tài:** Xây dựng hệ thống quản lý dinh dưỡng và gợi ý khẩu phần ăn tối ưu từ nguyên liệu sẵn có (**SmartMacro Engine**)  
> **Tài liệu PDF đính kèm:** `SmartMacro_Architectural_Report.pdf` (có sẵn ở thư mục gốc và `docs/reports/`)

---

## PHẦN 1: LỆNH BẬT HỆ THỐNG & KỊCH BẢN CLICK CHUỘT DEMO TRONG 5 PHÚT

### 1. Cách khởi động Backend & Frontend trước giờ lên bảng

Mở **2 cửa sổ Terminal (PowerShell)** tại thư mục gốc `c:\Projects\SmartMacro-Engine`:

#### Cửa sổ Terminal 1 — Bật Backend API (ASP.NET Core 8 + SQL Server)
```powershell
# (Nếu lần đầu chạy trên máy mới, cập nhật bảng vào SQL Server):
dotnet tool run dotnet-ef database update --project SmartMacro.Api --startup-project SmartMacro.Api

# Chạy Backend Web API (mặc định lắng nghe tại http://localhost:5000):
dotnet run --project SmartMacro.Api
```
* **Ghi chú:** Khi thấy dòng `Now listening on: http://localhost:5000`, bạn có thể mở thêm tab `http://localhost:5000/swagger` để sẵn sàng khoe danh sách API nếu giảng viên muốn xem.

#### Cửa sổ Terminal 2 — Bật Giao diện Web (React + TypeScript + Vite)
```powershell
cd SmartMacro.Web
npm run dev
```
* Mở trình duyệt truy cập: **`http://localhost:5173`**

---

### 2. Kịch bản Click chuột Demo trực tiếp trong 5 phút (Mượt, không sợ lỗi dữ liệu)

* **Phút 1 — Đăng ký / Đăng nhập (Chứng minh JWT + BCrypt):**
  1. Tại màn hình `/login`, bấm **"Đăng ký ngay"** (hoặc đăng nhập tài khoản đã có).
  2. Nhập nhanh: Họ tên, Email (`sinhvien@smartmacro.vn`), Mật khẩu (`Password123!`), Ngày sinh, Giới tính, Chế độ (`Cutting` / `Maintenance`) $\rightarrow$ Bấm **Đăng ký**.
  3. Hệ thống tự động cấp `AccessToken` (JWT 15 phút) + `RefreshToken` (lưu bảng `refresh_tokens`) và chuyển thẳng vào giao diện chính `/dashboard`.

* **Phút 2 — Bấm nút "Nạp dữ liệu mẫu (Demo Seed)" (Điểm ăn tiền khi Demo):**
  1. Chỉ cho giảng viên thấy nút màu vàng cam **"Nạp dữ liệu mẫu (Demo Seed)"** ở góc trên bên phải thanh Header và bấm vào đó.
  2. Giải thích ngắn gọn: *"Thưa thầy/cô, để tiết kiệm thời gian nhập tay khi demo, nút này gọi API tạo sẵn 5 món ăn quen thuộc (Ức gà, Cơm trắng, Trứng gà, Khoai lang, Bông cải xanh), nạp vào kho tủ lạnh cá nhân và đặt mục tiêu mẫu hôm nay là 2200 kcal (160g Protein, 250g Carbs, 60g Fat)."*

* **Phút 3 — Trình diễn Màn hình 1 (Tổng quan & Mục tiêu) và Màn hình 2 (Kho tủ lạnh):**
  1. Tại **Tab 1 (Tổng quan & Mục tiêu)**: Chỉ vào 4 ô hiển thị Mục tiêu hôm nay (`2200 kcal`, `160g Đạm`, `250g Tinh bột`, `60g Chất béo`). Có thể sửa thử số Calo trên form rồi bấm **"Cập nhật mục tiêu hôm nay"** để chứng minh API `PUT /api/daily-targets/{id}` chạy thật.
  2. Chuyển sang **Tab 2 (Thực phẩm & Kho tủ lạnh)**: Chỉ vào bảng danh sách nguyên liệu đang có trong tủ lạnh (`600g Ức gà`, `800g Cơm trắng`, `500g Trứng gà`, `600g Khoai lang`, `400g Bông cải xanh`) kèm hạn sử dụng. Thử chọn thêm 1 món ở cột trái bấm **"Thêm vào Kho tủ lạnh"** để chứng minh chức năng cộng dồn số gram tồn kho.

* **Phút 4 & 5 — Trình diễn Màn hình 3 (Gợi ý Thực đơn Tối ưu bằng Google OR-Tools):**
  1. Chuyển sang **Tab 3 (Gợi ý Thực đơn Tối ưu)** $\rightarrow$ Bấm nút lớn màu xanh **"Tính toán khẩu phần ăn tối ưu"**.
  2. Chỉ vào bảng kết quả hiện ra ngay lập tức:
     * **Trạng thái bộ giải:** `OPTIMAL` (Tìm được nghiệm tối ưu).
     * **Đối chiếu chỉ số:** Tổng Protein, Carbs, Fat đạt được đều nằm khít trong khoảng $\pm 5\%$ so với mục tiêu (`160g P`, `250g C`, `60g F`), và tổng Calo sát mức `2200 kcal`.
     * **Bảng định lượng chi tiết:** Hệ thống chỉ rõ cần lấy bao nhiêu gram **Ức gà**, bao nhiêu gram **Cơm trắng**, **Trứng gà**, **Khoai lang** từ trong tủ lạnh.

---

## PHẦN 2: CẨM NANG VẤN ĐÁP (ĐỌC 10 PHÚT NẮM VỮNG 100%)

### A. Tóm tắt trả lời nhanh 12 câu hỏi của Buổi 3/10 (Ngắn gọn, đúng trọng tâm)

1. **Câu 1 (Tên đề tài & Bài toán thực tế):**
   * *Trả lời:* Đề tài là **Hệ thống quản lý dinh dưỡng và gợi ý khẩu phần ăn tối ưu từ nguyên liệu sẵn có (SmartMacro Engine)**. Giải quyết bài toán thực tế: người tập thể hình/ăn kiêng có sẵn đồ ăn trong tủ lạnh nhưng không biết lấy mỗi món bao nhiêu gram để khớp chỉ số Calo, Protein, Carb, Fat trong ngày.
2. **Câu 2 (Mục tiêu hệ thống):**
   * *Trả lời:* Quản lý danh mục món ăn, quản lý tồn kho tủ lạnh cá nhân (số gram, hạn dùng), đặt mục tiêu Macro theo ngày và tự động tính số gram thức ăn tối ưu bằng thuật toán.
3. **Câu 3 (Phạm vi & Quy mô áp dụng):**
   * *Trả lời:* Ứng dụng Web cá nhân cho người tự tập luyện/ăn kiêng tại nhà, hoặc áp dụng cho các **Phòng Gym / CLB Thể hình quy mô vừa và nhỏ** để PT và hội viên lên thực đơn định lượng nhanh.
4. **Câu 4 (Đối tượng sử dụng):**
   * *Trả lời:* Người tập thể hình, người ăn kiêng theo chế độ Macro, Huấn luyện viên cá nhân (PT) và Quản trị viên hệ thống.
5. **Câu 5 (Khảo sát hệ thống tương tự & Điểm khác biệt):**
   * *Trả lời:* Các app như *MyFitnessPal, FatSecret* chỉ là sổ tay cộng dồn (ăn gì tự gõ vào), còn *Spoonacular* gợi ý công thức cố định bắt phải đi mua thêm đồ. Điểm khác biệt của em là **giải bài toán ngược**: tủ lạnh đang có gì thì dùng thuật toán tính số gram từ chính những món đó.
6. **Câu 6 (Sơ đồ BFD là gì & gồm mấy nhánh?):**
   * *Trả lời:* **BFD (Business Function Diagram)** là sơ đồ hình cây phân rã chức năng hệ thống từ tổng quát đến chi tiết. Hệ thống của em chia làm **6 nhánh chức năng**: (1) Quản lý tài khoản, (2) Quản lý danh mục & thực phẩm, (3) Quản lý kho cá nhân, (4) Thiết lập mục tiêu & lịch tập, (5) Tính toán thực đơn tối ưu, (6) Thống kê báo cáo.
7. **Câu 7 (Phân quyền gồm mấy vai trò?):**
   * *Trả lời:* Em thiết kế **2 vai trò cốt lõi** vừa sức với đồ án cá nhân:
     * **`Admin (Quản trị viên)`**: Quản lý danh mục nhóm thực phẩm (`FoodCategories`), quản lý dữ liệu món ăn chuẩn hệ thống (`Foods`), quản lý người dùng (`Users`).
     * **`User / Member (Người dùng)`**: Quản lý hồ sơ, đặt mục tiêu ngày (`DailyTargets`), quản lý tủ lạnh cá nhân (`Inventory`), chạy công cụ tối ưu thực đơn (`Optimizations`) và xem tổng quan (`Dashboard`).
8. **Câu 8 (Cơ chế đăng nhập & bảo mật API hoạt động ra sao?):**
   * *Trả lời:* Mật khẩu được băm bằng **BCrypt** lưu trong bảng `users`. Khi đăng nhập đúng, Backend trả về **JWT Access Token** (hạn 15 phút, chứa `UserId` trong Claim) và **Refresh Token** (hạn 7 ngày, được băm SHA-256 lưu vào bảng `refresh_tokens` trong SQL Server). Khi gọi API có gắn `[Authorize]`, Backend đọc `UserId` từ JWT Token để đảm bảo tài khoản nào chỉ truy cập được kho và mục tiêu của tài khoản đó.
9. **Câu 9 (Mô hình kiến trúc hệ thống):**
   * *Trả lời:* Mô hình **Client - Server 3 lớp (3-Tier Architecture)**:
     * **Front-end:** React + TypeScript + Tailwind CSS.
     * **Back-end:** ASP.NET Core 8 Web API + Entity Framework Core 8 + Google OR-Tools.
     * **Database:** Microsoft SQL Server.
10. **Câu 10 (Tại sao chọn các công nghệ này?):**
    * *Trả lời:* React + TypeScript giúp làm giao diện SPA mượt, bắt lỗi kiểu dữ liệu khớp với DTO của Backend. ASP.NET Core 8 (C#) là ngôn ngữ hướng đối tượng mạnh mẽ được học ở trường, cấu trúc `Controller -> Service` rõ ràng và hỗ trợ thư viện toán học `Google.OrTools` rất tốt.
11. **Câu 11 (Tại sao chọn SQL Server & EF Core Code-First?):**
    * *Trả lời:* SQL Server quen thuộc, quản lý khóa chính (PK), khóa ngoại (FK 1-N) và kiểu số `decimal` rất chặt chẽ. Dùng **EF Core Code-First** giúp viết class C# trong thư mục `Models` và `SmartMacroDbContext.cs` rồi chạy lệnh Migration để tự động sinh bảng SQL Server, không sợ lệch code với DB.
12. **Câu 12 (3 tầng liên kết với nhau như thế nào?):**
    * *Trả lời:* Trên trình duyệt React, khi bấm nút $\rightarrow$ **Axios** gửi HTTP Request (JSON kèm Header `Authorization: Bearer <token>`) $\rightarrow$ **Controller** ở ASP.NET Core nhận request $\rightarrow$ gọi **Service** xử lý nghiệp vụ $\rightarrow$ gọi **EF Core (`SmartMacroDbContext`)** sinh câu lệnh SQL truy vấn xuống **SQL Server** $\rightarrow$ trả DTO về dạng JSON để React vẽ lên màn hình.

---

### B. Cách giải thích Thuật toán Quy hoạch Tuyến tính (OR-Tools) bằng ngôn ngữ bình dân nhất

Khi giảng viên hỏi: *"Em tính số gram thức ăn bằng cách nào? Code nằm ở đâu?"*, bạn trả lời theo đúng 4 ý sau (nằm trong file `SmartMacro.Api/Engines/MacroOptimizationEngine.cs`):

1. **Bài toán giống như giải hệ phương trình cấp 3:**
   * Giả sử trong tủ lạnh có $n$ món ăn. Em gọi biến cần tìm là `grams[i]` — tức là **số gram cần lấy của món thứ `i`**.
2. **Điều kiện 1 — Không lấy lố số lượng trong tủ lạnh (Dòng 94–101):**
   * Mỗi biến `grams[i]` phải lớn hơn hoặc bằng `0` và nhỏ hơn hoặc bằng số gram đang có trong kho (`0 <= grams[i] <= QuantityGrams[i]`).
3. **Điều kiện 2 — Tổng Đạm, Tinh bột, Chất béo phải đạt mục tiêu $\pm 5\%$ (Dòng 107–130):**
   * Trong bảng `foods`, chỉ số dinh dưỡng được tính trên `100g`, nên `1g` thức ăn sẽ có `MacroPer100g / 100`.
   * Em cộng tổng lượng Protein của tất cả các món lại: $\sum (\text{grams}[i] \times \text{Protein}[i] / 100)$ và ép nó phải nằm trong khoảng từ **95% đến 105%** mục tiêu Protein hôm nay. Làm y hệt cho **Carbs** và **Fat**.
4. **Mục tiêu tối ưu — Tổng Calo sát mục tiêu nhất (Dòng 141–172):**
   * Sau khi thỏa mãn đủ 3 chất Đạm, Bột, Béo, có thể có nhiều cách kết hợp món ăn. Em đặt hàm mục tiêu là **Minimizing (cực tiểu hóa) độ lệch giữa Tổng Calo thực tế và Calo mục tiêu** (`|TotalKcal - TargetKcal|`).
   * Bộ giải `GLOP` của thư viện `Google.OrTools` sẽ giải hệ bất phương trình này trong vài mili-giây và trả về số gram chính xác của từng món (`grams[i].SolutionValue()`). Món nào dưới `0.5g` thì em lọc bỏ cho thực đơn gọn gàng.

---

### C. Cách chỉ tay giải thích Sơ đồ ERD (Bảng CSDL trong `SmartMacroDbContext.cs`)

Khi giảng viên mở trang Sơ đồ ERD trong file PDF và hỏi về CSDL, bạn chỉ cần lấy bảng **`users`** làm trung tâm rồi tỏa ra 3 nhánh:

1. **Nhánh 1 — Xác thực & Bảo mật (`users` 1 $\rightarrow$ N `refresh_tokens`):**
   * Bảng `users` lưu thông tin tài khoản (`user_id` là khóa chính PK, `email` là duy nhất, `password_hash` lưu mật khẩu băm BCrypt).
   * Nối `1 - N` sang bảng `refresh_tokens` qua khóa ngoại `user_id` để quản lý các phiên đăng nhập và thu hồi token khi đăng xuất.
2. **Nhánh 2 — Thực phẩm & Kho tủ lạnh (`food_categories` 1 $\rightarrow$ N `foods` 1 $\rightarrow$ N `user_food_inventory`):**
   * Bảng `food_categories` lưu nhóm thực phẩm (Thịt cá, Tinh bột, Rau củ...).
   * Một nhóm có nhiều món trong bảng `foods` (lưu `kcal_per_100g`, `protein_g_per_100g`, `carbs_g_per_100g`, `fat_g_per_100g`).
   * Bảng `user_food_inventory` là **kho tủ lạnh cá nhân**, nối khóa ngoại `user_id` (của ai) và `food_id` (món gì), lưu cột `quantity_grams` (còn bao nhiêu gram) và `expiry_date` (ngày hết hạn).
3. **Nhánh 3 — Mục tiêu dinh dưỡng & Lịch tập (`users` 1 $\rightarrow$ N `daily_targets`):**
   * Bảng `daily_targets` lưu mục tiêu từng ngày của người dùng (`target_date`, `target_kcal`, `target_protein_g`, `target_carbs_g`, `target_fat_g`). Cặp `(user_id, target_date)` được đặt **Unique Index** để mỗi ngày 1 người chỉ có 1 mục tiêu duy nhất.
   * Ngoài ra hệ thống có các bảng mở rộng cho lịch tập (`training_cycle_types`, `user_training_schedule`, `macro_adjustment_rules`) và nhật ký bữa ăn (`meal_logs`) để sẵn sàng mở rộng ở các buổi thực tập tiếp theo.
