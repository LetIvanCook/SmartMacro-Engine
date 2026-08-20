# SmartMacro Engine — Load Testing Suite (k6)

Bộ công cụ kiểm thử hiệu năng và khả năng chịu tải (Load Testing) cho SmartMacro Engine sử dụng **[k6](https://k6.io/)** by Grafana Labs.

---

## 1. Tổng quan & Kiến trúc k6 Test

### 1.1 Endpoint mục tiêu
- **LP Solver (Chính):** `POST /api/optimizations/generate-plan`
  - Đây là endpoint cốt lõi tính toán dinh dưỡng sử dụng Google OR-Tools (GLOP Linear Programming Solver). Tác vụ này là **CPU-bound**, cần được đo đạc kỹ lưỡng về độ trễ (latency) và giới hạn RPS.
- **Dashboard (Tùy chọn):** `GET /api/dashboard/{userId}/dashboard`
  - Endpoint Chunky API tổng hợp dữ liệu vĩ mô của người dùng.

### 1.2 Chiến lược xử lý Rate Limiting
- Hệ thống áp dụng `[EnableRateLimiting("AuthPolicy")]` với hạn mức **5 requests / phút** cho các endpoint xác thực (`/api/auth/login`, `/api/auth/refresh`).
- Script k6 gom toàn bộ bước xác thực vào hàm **`setup()`** (chạy đúng 1 lần duy nhất trước khi các Virtual Users bắt đầu).
- Token JWT được trích xuất từ `setup()` và chia sẻ cho toàn bộ VUs xuyên suốt quá trình test, **tuyệt đối không gây nghẽn hay kích hoạt HTTP 429 Too Many Requests**.

---

## 2. Cài đặt k6

### Windows
```powershell
# Sử dụng Windows Package Manager (khuyến nghị)
winget install k6 --source winget

# Hoặc qua Chocolatey
choco install k6
```

### macOS
```bash
brew install k6
```

### Linux (Debian / Ubuntu)
```bash
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

### Sử dụng Docker (Không cần cài đặt binary vào máy)
```bash
docker pull grafana/k6:latest
```

---

## 3. Hướng dẫn chạy Load Test

> [!WARNING]
> **Bảo mật thông tin đăng nhập:**
> Tuyệt đối KHÔNG hardcode tài khoản thật hoặc production credentials vào script. Toàn bộ thông tin đăng nhập và URL cấu hình đều được đọc qua **biến môi trường** (`__ENV`).

### 3.1 Chạy qua k6 CLI trực tiếp

#### Bước 1: Chuẩn bị tài khoản test trên môi trường mục tiêu
Đảm bảo tài khoản test đã được đăng ký trên hệ thống (ví dụ: `testuser@smartmacro.local` / `Test@123456`).

#### Bước 2: Chạy Smoke Test (Xác minh nhanh 1-2 VUs)
```powershell
k6 run `
  -e BASE_URL="http://localhost:8080" `
  -e TEST_USER_EMAIL="testuser@smartmacro.local" `
  -e TEST_USER_PASSWORD="TestPassword123!" `
  -e PROFILE="smoke" `
  load-tests/dashboard-load-test.js
```

#### Bước 3: Chạy Standard Load Test (Ramping 0 -> 20 -> 50 VUs trong 2 phút)
```powershell
k6 run `
  -e BASE_URL="http://localhost:8080" `
  -e TEST_USER_EMAIL="testuser@smartmacro.local" `
  -e TEST_USER_PASSWORD="TestPassword123!" `
  -e PROFILE="standard" `
  load-tests/dashboard-load-test.js
```

#### Bước 4: Chạy Stress Test (Ramping lên 100 VUs)
```powershell
k6 run `
  -e BASE_URL="http://localhost:8080" `
  -e TEST_USER_EMAIL="testuser@smartmacro.local" `
  -e TEST_USER_PASSWORD="TestPassword123!" `
  -e PROFILE="stress" `
  -e P95_THRESHOLD="1200" `
  load-tests/dashboard-load-test.js
```

---

### 3.2 Chạy qua Docker Container

Nếu chạy API trên host (`localhost:8080`) và k6 trong Docker:

```powershell
# Trên Windows PowerShell (dùng host.docker.internal để trỏ về API trên host)
docker run --rm -i `
  -v "${PWD}/load-tests:/load-tests" `
  grafana/k6 run `
  -e BASE_URL="http://host.docker.internal:8080" `
  -e TEST_USER_EMAIL="testuser@smartmacro.local" `
  -e TEST_USER_PASSWORD="TestPassword123!" `
  -e PROFILE="standard" `
  /load-tests/dashboard-load-test.js
```

---

## 4. Các biến môi trường tùy biến (Environment Variables)

| Biến môi trường | Mặc định | Ý nghĩa |
|---|---|---|
| `BASE_URL` | `http://localhost:8080` | URL gốc của API (không có dấu gạch chéo cuối). |
| `TEST_USER_EMAIL` | *(Bắt buộc)* | Email tài khoản test đã tồn tại trong DB. |
| `TEST_USER_PASSWORD` | *(Bắt buộc)* | Mật khẩu tài khoản test. |
| `TARGET_ENDPOINT` | `/api/optimizations/generate-plan` | Endpoint cần load test (`/api/optimizations/generate-plan` hoặc `/api/dashboard/{userId}/dashboard`). |
| `PROFILE` | `standard` | Hồ sơ tải (`smoke`, `standard`, `stress`). |
| `P95_THRESHOLD` | `800` | Ngưỡng thời gian phản hồi p95 tối đa cho phép (ms). |
| `P99_THRESHOLD` | `1500` | Ngưỡng thời gian phản hồi p99 tối đa cho phép (ms). |
| `MAX_ERROR_RATE` | `0.01` | Tỷ lệ lỗi tối đa cho phép (0.01 = 1%). |

---

## 5. Đọc và Phân tích kết quả k6

Khi k6 kết thúc một phiên chạy, bảng thống kê tổng hợp sẽ hiển thị trên terminal:

```text
✓ setup: login succeeded (status 200)
✓ setup: access token returned
✓ status is 200
✓ response time within p95 threshold
✓ solver result valid

checks.........................: 100.00% ✓ 450      ✗ 0
data_received..................: 1.2 MB  10 kB/s
data_sent......................: 150 kB  1.2 kB/s
http_req_blocked...............: avg=21.4µs   min=1µs     med=3µs    max=1.2ms    p(90)=8µs    p(95)=12µs
http_req_connecting............: avg=1.2µs    min=0s      med=0s     max=300µs    p(90)=0s     p(95)=0s
http_req_duration..............: avg=42.15ms  min=12.4ms  med=38.2ms max=312.4ms  p(90)=65.4ms p(95)=88.2ms p(99)=194.5ms
{ expected_response:true }...: avg=42.15ms  min=12.4ms  med=38.2ms max=312.4ms  p(90)=65.4ms p(95)=88.2ms p(99)=194.5ms
http_req_failed................: 0.00%   ✓ 0        ✗ 150
http_reqs......................: 150     1.25/s
iteration_duration.............: avg=1.04s    min=1.01s   med=1.03s  max=1.31s    p(90)=1.06s  p(95)=1.09s
iterations.....................: 150     1.25/s
vus............................: 1       min=0      max=50
vus_max........................: 50      min=50     max=50
```

### Các chỉ số quan trọng cần lưu ý:
1. **`http_req_duration p(95)` & `p(99)`**:
   - 95% và 99% số lượng request hoàn thành trong khoảng thời gian này.
   - Nếu `p(95) < 800ms`: Đạt chuẩn SLA của hệ thống.
2. **`http_reqs` (RPS)**:
   - Số lượng request xử lý thành công trên mỗi giây.
3. **`http_req_failed`**:
   - Tỷ lệ phần trăm request lỗi (HTTP 4xx, 5xx, timeout). Bắt buộc phải `< 1%`.
4. **`checks`**:
   - Đảm bảo 100% assertions về status code và định dạng response body pass.

---

## 6. Lưu ý đặc thù về Môi trường Local / Dev

- **Bản chất CPU-bound của LP Solver:**
  Google OR-Tools GLOP solver thực hiện các phép toán ma trận đại số tuyến tính trên CPU. Khi chạy trên môi trường máy Dev/Local đơn máy (single-node) cùng lúc với cơ sở dữ liệu SQL Server, mức chiếm dụng CPU sẽ tăng tỉ lệ thuận với số lượng VUs.
- **Giới hạn đo đạc Local:**
  Kết quả RPS đo trên máy local phản ánh năng lực xử lý của máy trạm cá nhân, không đại diện cho năng lực mở rộng ngang (horizontal autoscaling trên Kubernetes / Container Apps) ở môi trường Staging/Production thực tế.
- **Khuyến nghị Staging:**
  Khi triển khai lên Staging có multi-instance và load balancer, hãy chạy lại load test với profile `stress` để xác định chính xác điểm bão hòa (saturation point) và cấu hình HPA (Horizontal Pod Autoscaler) phù hợp.

---

## 7. Tích hợp CI/CD (GitHub Actions)

Bộ k6 test được tích hợp trong workflow `.github/workflows/load-test.yml`.
Workflow này được cấu hình **chỉ chạy thủ công (`workflow_dispatch`)**, cho phép:
- Chọn target URL (mặc định trỏ Staging/Dev).
- Lựa chọn profile tải (`smoke`, `standard`, `stress`).
- Điều chỉnh ngưỡng p95 threshold.
- Tự động đính kèm kết quả k6 vào GitHub Actions Job Summary.
