# 🚀 SK Scanner FAST v1.0

**Maximum Speed Edition** - Phiên bản tối ưu tốc độ tối đa cho việc quét .env files và debug mode.

---

## ✨ Tính năng

- ⚡ **Tốc độ cực nhanh**: 500-1000+ URLs/giây
- 🎯 **Không tracking**: Scan tất cả URLs, không bỏ qua
- 🔍 **Tìm Stripe Keys**: Tự động phát hiện `sk_live_*` keys
- ✅ **Check Stripe Keys**: Tùy chọn kiểm tra key có valid không
- 📱 **Telegram Alert**: Thông báo ngay khi tìm thấy key valid
- 🌐 **2 chế độ scan**: ENV file scanner & Debug mode scanner
- 💪 **Async/Concurrent**: Xử lý hàng nghìn requests đồng thời

---

## 📋 Yêu cầu hệ thống

- **Python**: 3.7+
- **RAM**: Tối thiểu 2GB
- **Network**: Kết nối internet ổn định

---

## 🔧 Cài đặt

### Windows

```cmd
# 1. Cài đặt Python dependencies
pip install aiohttp aiofiles urllib3

# 2. Chạy scanner
python scanner_fast.py
```

### Linux/Mac

```bash
# 1. Cài đặt Python dependencies
pip3 install aiohttp aiofiles urllib3

# 2. Chạy scanner
python3 scanner_fast.py
```

---

## 🎮 Hướng dẫn sử dụng

### Bước 1: Chuẩn bị file URLs

Tạo file text chứa danh sách URLs (mỗi dòng 1 URL):

```
example.com
test.com:8080
192.168.1.1
subdomain.example.com
```

**Lưu ý**: Không cần thêm `http://` hoặc `https://`, tool sẽ tự động thử cả hai.

### Bước 2: Chạy scanner

```cmd
python scanner_fast.py
```

### Bước 3: Chọn chế độ scan

```
[1] Debug Mode Scanner    - Scan debug mode exposure
[2] ENV File Scanner      - Scan .env files
```

### Bước 4: Cấu hình Telegram (tùy chọn)

Nếu muốn nhận thông báo qua Telegram:

1. Tạo bot với [@BotFather](https://t.me/BotFather)
2. Lấy Bot Token
3. Lấy Chat ID (dùng [@userinfobot](https://t.me/userinfobot))
4. Nhập vào khi tool hỏi

### Bước 5: Cấu hình Auto-check Stripe Keys (tùy chọn)

- **Yes (y)**: Tool sẽ tự động check key có valid không
- **No (n)**: Chỉ lưu key vào file, không check

### Bước 6: Chọn Concurrency

Số lượng requests đồng thời:
- **500-1000**: Phù hợp cho máy thường
- **1000-2000**: Máy mạnh, mạng tốt
- **2000+**: Máy rất mạnh, cần test

### Bước 7: Nhập đường dẫn file URLs

```
[URLS PATH] : urls.txt
```

Tool sẽ bắt đầu scan!

---

## 📊 Kết quả

### Trong quá trình scan

```
[████████████░░░░░░░░] 60.5% | 12,345/20,000 | ✓156 ✗11,189 | 850/s | ETA: 0h2m | SK: 3/5
```

- **Progress bar**: Tiến độ scan
- **✓**: Số URLs tìm thấy .env/debug
- **✗**: Số URLs không tìm thấy
- **Speed**: URLs/giây
- **ETA**: Thời gian còn lại
- **SK**: Valid keys / Total keys checked

### Khi hoàn thành

```
======================================================================
                    SCAN COMPLETED
======================================================================
  Total URLs: 20,000
  Scanned: 20,000
  Found: 156 | Failed: 19,844
  Time: 0.65h | Speed: 856.3 URLs/s

[STRIPE CHECKER]
  Checked: 5
  Valid: 3 | Invalid: 2
  Valid keys saved to: SK_VALID.TXT
======================================================================
```

---

## 📁 File kết quả

### ENVS/
Chứa các file .env đã tìm thấy:
```
ENVS/example.com_env.txt
ENVS/test.com_8080_env.txt
```

### DEBUG/
Chứa các file debug response:
```
DEBUG/example.com_debug.htm
```

### SK_LIVE.TXT
Danh sách tất cả Stripe keys tìm thấy:
```
sk_live_xxx
sk_live_...
```

### SK_VALID.TXT
Chi tiết các Stripe keys VALID (nếu bật auto-check):
```
============================================================
KEY: sk_live_xx
SOURCE: https://example.com/.env
ACCOUNT: acct_1234567890
EMAIL: admin@example.com
COUNTRY: US | CURRENCY: usd
AVAILABLE: $1,234.56
PENDING: $0.00
CHARGES: True | PAYOUTS: True
CHECKED: 2025-12-09 17:30:45
============================================================
```

### SK_ENV.TXT
Mapping giữa URL và Stripe key:
```
ENV : https://example.com/.env
DEBUG : https://test.com
```

---

## ⚙️ Tùy chỉnh nâng cao

### Thay đổi Concurrency

Mở file `scanner_fast.py`, tìm dòng:
```python
limit=concurrency,
limit_per_host=100,
```

Tăng `limit_per_host` nếu muốn nhiều requests hơn đến cùng 1 host.

### Thay đổi Timeout

Tìm dòng:
```python
timeout=aiohttp.ClientTimeout(total=8, connect=4),
```

- `total=8`: Timeout tổng (giây)
- `connect=4`: Timeout kết nối (giây)

### Thay đổi Chunk Size

Tìm dòng:
```python
chunk_size = 5000
```

Tăng để xử lý nhiều URLs cùng lúc (cần RAM nhiều hơn).

---

## 🆚 So sánh các phiên bản

| Tính năng | scanner_fast.py | scannerv43.py | scanner_cloud.py |
|-----------|----------------|---------------|------------------|
| Tốc độ | ⚡⚡⚡ Cực nhanh | ⚡⚡ Trung bình | ⚡ Chậm |
| Tracking | ❌ Không | ✅ Local DB | ✅ Cloud DB |
| Skip duplicate | ❌ | ✅ | ✅ |
| Phù hợp cho | Scan nhanh, test | Scan thường xuyên | Multi-user, team |
| RAM usage | Thấp | Trung bình | Thấp |
| Setup | Đơn giản | Đơn giản | Phức tạp |

---

## 💡 Tips & Tricks

### 1. Tối ưu tốc độ
- Dùng concurrency cao (1500-2000)
- Tắt auto-check Stripe keys nếu không cần
- Dùng SSD để ghi file nhanh hơn

### 2. Tránh bị block
- Không dùng concurrency quá cao (>3000)
- Scan từng batch nhỏ thay vì 1 file lớn
- Dùng proxy/VPN nếu cần

### 3. Quản lý kết quả
- Backup folder ENVS/ thường xuyên
- Xóa file cũ trước khi scan mới
- Dùng timestamp trong tên file

### 4. Test trước khi scan thật
```cmd
# Tạo file test nhỏ
echo localhost:8080 > test_urls.txt

# Chạy test server
python test_server.py

# Scan test
python scanner_fast.py
```

---

## 🐛 Xử lý lỗi

### Lỗi: "ModuleNotFoundError: No module named 'aiohttp'"
```cmd
pip install aiohttp aiofiles urllib3
```

### Lỗi: "Too many open files"
**Windows**: Tăng limit trong Registry  
**Linux**: 
```bash
ulimit -n 10000
```

### Lỗi: "Connection timeout"
- Giảm concurrency
- Tăng timeout trong code
- Kiểm tra kết nối mạng

### Scan chậm hơn mong đợi
- Giảm concurrency (có thể bị rate limit)
- Kiểm tra tốc độ mạng
- Tắt auto-check Stripe keys

---

## 📞 Hỗ trợ

- **Tác giả**: Phạm Quang Huy (@hiamhuy)
- **Version**: 1.0
- **License**: MIT

---

## 🔄 Changelog

### v1.0 (2025-12-09)
- ✨ Release đầu tiên
- ⚡ Tối ưu tốc độ tối đa
- 🎯 Loại bỏ hoàn toàn database
- 📱 Tích hợp Telegram notifications
- ✅ Auto-check Stripe keys

---

## ⚠️ Lưu ý quan trọng

1. **Chỉ sử dụng cho mục đích hợp pháp**: Không scan các website mà bạn không có quyền
2. **Tuân thủ luật pháp**: Việc truy cập trái phép vào hệ thống là vi phạm pháp luật
3. **Bảo mật thông tin**: Không chia sẻ Stripe keys hoặc thông tin nhạy cảm tìm được
4. **Sử dụng có trách nhiệm**: Tool này chỉ dành cho security testing và research

---

**Happy Scanning! 🚀**
