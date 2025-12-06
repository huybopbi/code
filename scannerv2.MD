# SK Scanner - Công Cụ Quét Bảo Mật Nâng Cao

Công cụ quét bảo mật mạnh mẽ được viết bằng Python, chuyên phát hiện file `.env` bị lộ và lỗ hổng debug mode trên quy mô lớn. Chuyên tìm kiếm Stripe API keys và thông tin nhạy cảm.

## 🚀 Tính Năng

### Hai Chế Độ Quét
- **ENV Mode**: Quét file `.env` bị public (HTTP/HTTPS)
- **Debug Mode**: Khai thác lỗ hổng debug mode để lấy dữ liệu nhạy cảm

### Khả Năng Chính
- ✅ **Hỗ trợ Multi-thread & Async**: Hai phiên bản cho các trường hợp khác nhau
- ✅ **Phát hiện Stripe Key**: Tự động trích xuất và lưu key `sk_live_*`
- ✅ **Thông báo Telegram**: Cảnh báo real-time khi tìm thấy key
- ✅ **Theo dõi tiến độ**: Lưu/Tiếp tục scan khi bị gián đoạn
- ✅ **Xoay vòng User-Agent**: Bypass phát hiện bot cơ bản
- ✅ **Progress Bar Real-time**: Hiển thị trực quan với thống kê
- ✅ **Tùy chỉnh Concurrency**: Tối ưu theo phần cứng

### Phát Hiện Dữ Liệu Nhạy Cảm
- Stripe API Keys (`sk_live_*`)
- Thông tin database (`DB_HOST`, `DB_CONNECTION`)
- Cấu hình mail server (`MAIL_HOST`, `MAIL_USERNAME`)
- Application secrets (`APP_ENV`, `APP_DEBUG`)

## 📦 Cài Đặt

### Yêu Cầu
```bash
# Cho scanner.py (Phiên bản Threading)
pip install requests urllib3

# Cho scanner_async.py (Phiên bản Async - KHUYẾN NGHỊ)
pip install aiohttp aiofiles requests urllib3
```

### Phiên Bản Python
- Python 3.7+

## 🎯 Sử Dụng

### Bắt Đầu Nhanh

**Phiên Bản Threading (List Nhỏ đến Trung Bình):**
```bash
python scanner.py
```

**Phiên Bản Async (List Lớn - KHUYẾN NGHỊ):**
```bash
python scanner_async.py
```

### Các Bước Cấu Hình

1. **Chọn Mode**
   - `1` - Debug Mode Scanner
   - `2` - ENV File Scanner

2. **Cài Đặt Telegram (Tùy chọn)**
   - Lần đầu: Nhập Bot Token và Chat ID
   - Lần sau: Tự động load từ `config.json`

3. **Đặt Concurrency**
   - Threading: Khuyến nghị 50-100 threads
   - Async: Khuyến nghị 200-500 concurrency

4. **Cung Cấp Danh Sách URL**
   - File text với mỗi dòng 1 IP/domain
   - Ví dụ: `ips.txt`

### Ví Dụ Sử Dụng
```
[MODE] : 2
[CONCURRENCY] : 400
[URLS PATH] : ips.txt

[████████████████░░░░░░░░░░░░░░] 53.2% | Scanned: 532/1000 | Found: 5 | Failed: 527
```

## 📊 So Sánh Hiệu Suất

| Phiên Bản | Concurrency | Tốc Độ | 1 Triệu IPs | RAM |
|-----------|-------------|--------|-------------|-----|
| scanner.py | 50-100 threads | ~50-100 URLs/s | 3-5 giờ | ~100MB |
| scanner_async.py | 200-500 | ~200-500 URLs/s | 30-90 phút | ~200-300MB |

### Cài Đặt Khuyến Nghị (RAM 16GB)
- **scanner.py**: 100 threads
- **scanner_async.py**: 400 concurrency

## 📁 Cấu Trúc Output

```
├── ENVS/                    # Kết quả ENV scan
│   └── domain.com_env.txt
├── DEBUG/                   # Kết quả Debug scan
│   └── domain.com_debug.htm
├── SK/                      # Phát hiện Stripe key
│   └── domain.com_*.htm
├── SK_ENV.TXT              # Danh sách URL có Stripe key
├── SK_LIVE.TXT             # Chỉ chứa Stripe keys
├── config.json             # Cấu hình Telegram
└── progress_*.txt          # Tiến độ scan (hỗ trợ resume)
```

## 🔧 Tính Năng Nâng Cao

### Chức Năng Lưu/Tiếp Tục
- Tự động lưu tiến độ sau mỗi lần scan
- Tiếp tục scan bị gián đoạn mà không mất tiến độ
- File tiến độ: `progress_env_*.txt` hoặc `progress_debug_*.txt`

### Tích Hợp Telegram
1. Tạo bot qua [@BotFather](https://t.me/BotFather)
2. Lấy Bot Token
3. Lấy Chat ID từ `https://api.telegram.org/bot<TOKEN>/getUpdates`
4. Nhập lần đầu - tự động lưu

### Xoay Vòng User-Agent
- 8 User-Agent trình duyệt khác nhau
- Random mỗi request
- Bao gồm Chrome, Firefox, Safari, Edge
- Bypass phát hiện bot cơ bản

## 🎨 Chi Tiết Tính Năng

### ENV Mode
- Quét endpoint `/.env` trên cả HTTP và HTTPS
- Phát hiện các pattern biến môi trường phổ biến
- Tự động trích xuất Stripe keys
- Lưu toàn bộ nội dung file `.env`

### Debug Mode
- Gửi POST request với parameter `debug=true`
- Khai thác debug mode cấu hình sai
- Capture error pages có dữ liệu nhạy cảm
- Lưu toàn bộ HTML response

## 📈 Hiển Thị Thống Kê

Sau khi scan hoàn thành:
```
============================================================
[SCAN COMPLETED]
============================================================
Total URLs: 1000000
Scanned: 1000000
Found: 42
Failed: 999958
Time: 3245.67s
Speed: 308.2 URLs/s
============================================================
```

## ⚠️ Tuyên Bố Pháp Lý

**CHỈ DÀNH CHO MỤC ĐÍCH GIÁO DỤC VÀ KIỂM THỬ CÓ PHÉP**

Công cụ này được thiết kế cho:
- Nhà nghiên cứu bảo mật
- Penetration tester có ủy quyền hợp lệ
- Bug bounty hunter trên các chương trình được phép
- Quản trị viên hệ thống kiểm tra hạ tầng của mình

**Quét trái phép là bất hợp pháp.** Luôn xin phép trước khi quét bất kỳ hệ thống nào bạn không sở hữu.

## 🛡️ Hướng Dẫn Sử Dụng Đạo Đức

- ✅ Chỉ quét hệ thống bạn sở hữu hoặc có giấy phép bằng văn bản
- ✅ Sử dụng cho đánh giá bảo mật được ủy quyền
- ✅ Báo cáo phát hiện một cách có trách nhiệm
- ❌ Không sử dụng cho mục đích xấu
- ❌ Không quét mà không có phép
- ❌ Không khai thác phát hiện bất hợp pháp

## 🔍 Cách Hoạt Động

### ENV Scanner
1. Thử HTTP request đến `http://target/.env`
2. Nếu thất bại, thử HTTPS request đến `https://target/.env`
3. Kiểm tra response có pattern nhạy cảm
4. Trích xuất và lưu Stripe keys nếu tìm thấy
5. Gửi thông báo Telegram

### Debug Scanner
1. Gửi POST request với parameter `debug=true`
2. Phân tích response tìm thông tin debug
3. Phát hiện biến môi trường trong error pages
4. Trích xuất Stripe keys từ debug output
5. Lưu toàn bộ HTML response

## 🚀 Mẹo Tối Ưu

### Cho List IP Lớn (1 Triệu+)
1. Dùng `scanner_async.py`
2. Đặt concurrency 300-500
3. Dùng SSD cho I/O nhanh hơn
4. Theo dõi RAM và điều chỉnh

### Để Kết Quả Tốt Hơn
1. Dùng masscan tìm port 80/443 mở trước
2. Lọc IP có web server đang chạy
3. Chạy ENV mode trước (tỷ lệ thành công cao hơn)
4. Dùng Debug mode cho các target còn lại

### Tích Hợp Masscan
```bash
# Quét web servers
masscan 0.0.0.0/0 -p80,443 --rate=10000 -oL results.txt

# Trích xuất IP duy nhất
awk '{print $4}' results.txt | sort -u > ips.txt

# Chạy scanner
python scanner_async.py
```

## 🐛 Xử Lý Sự Cố

### Vấn Đề Thường Gặp

**Lỗi "Module not found":**
```bash
pip install aiohttp aiofiles requests urllib3
```

**Tốc độ quét chậm:**
- Tăng concurrency (phiên bản async)
- Kiểm tra băng thông mạng
- Xác minh cài đặt timeout

**RAM sử dụng cao:**
- Giảm concurrency
- Dùng phiên bản threading cho RAM hạn chế

**Tiến độ không lưu:**
- Kiểm tra quyền ghi file
- Đảm bảo có dung lượng đĩa

## 📝 File Cấu Hình

Cấu trúc `config.json`:
```json
{
  "telegram_bot_token": "123456:ABC-DEF...",
  "telegram_chat_id": "123456789"
}
```

## 🔄 Lịch Sử Phiên Bản

### v2.0 (Async)
- Thêm hỗ trợ asyncio cho khả năng mở rộng lớn
- Cải thiện hiệu suất 5-10 lần
- Hỗ trợ 500+ kết nối đồng thời

### v1.0 (Threading)
- Phát hành đầu tiên
- Quét hai chế độ (ENV/Debug)
- Thông báo Telegram
- Theo dõi tiến độ
- Xoay vòng User-Agent

## 💡 Câu Hỏi Thường Gặp

**Q: Nên dùng phiên bản nào?**
A: Dùng `scanner_async.py` cho list > 100k IPs, `scanner.py` cho list nhỏ hơn.

**Q: Concurrency bao nhiêu là tối ưu?**
A: 
- RAM 8GB: 200 concurrency
- RAM 16GB: 400 concurrency
- RAM 32GB: 500-800 concurrency

**Q: Tại sao không tìm thấy gì?**
A: 
- Kiểm tra IP có web server chạy không
- Thử cả 2 mode (ENV và Debug)
- Đảm bảo mạng ổn định

**Q: Tool có hợp pháp không?**
A: Hợp pháp nếu bạn có phép quét. Trái phép là vi phạm pháp luật.

**Q: Làm sao lấy Telegram Bot Token?**
A:
1. Nhắn `/start` cho @BotFather
2. Gửi `/newbot` và làm theo hướng dẫn
3. Copy Bot Token nhận được

**Q: Làm sao lấy Chat ID?**
A:
1. Nhắn tin cho bot của bạn
2. Truy cập: `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Tìm `"chat":{"id":123456789}`

## 📊 Benchmark Thực Tế

**Máy test: Intel i7, 16GB RAM, 100Mbps**

| List Size | scanner.py (100 threads) | scanner_async.py (400) |
|-----------|--------------------------|------------------------|
| 10,000 | 3 phút | 45 giây |
| 100,000 | 30 phút | 6 phút |
| 1,000,000 | 5 giờ | 55 phút |

## 🎓 Học Thêm

### Tài Nguyên Hữu Ích
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Bug Bounty Platforms](https://www.bugcrowd.com/)
- [Responsible Disclosure](https://en.wikipedia.org/wiki/Responsible_disclosure)

### Kỹ Thuật Liên Quan
- Port scanning với masscan/nmap
- Subdomain enumeration
- Web application fingerprinting
- API security testing

## 🤝 Đóng Góp

Nếu bạn muốn cải thiện tool:
1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push và tạo Pull Request

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra phần Xử Lý Sự Cố
2. Đảm bảo đã cài đủ dependencies
3. Kiểm tra phiên bản Python (3.7+)

## ⚡ Pro Tips

1. **Tốc độ tối đa**: Dùng `scanner_async.py` với concurrency 400-500
2. **Tiết kiệm RAM**: Giảm concurrency xuống 200-300
3. **Tỷ lệ thành công cao**: Chạy ENV mode trước
4. **Tránh bị block**: Dùng proxy hoặc VPN
5. **List lớn**: Chia nhỏ thành nhiều file và chạy song song

## 🎯 Use Cases

### Security Researcher
- Tìm lỗ hổng trên quy mô lớn
- Thu thập dữ liệu cho nghiên cứu
- Phân tích xu hướng bảo mật

### Penetration Tester
- Đánh giá bảo mật hạ tầng
- Tìm điểm yếu trong hệ thống
- Báo cáo cho khách hàng

### Bug Bounty Hunter
- Quét các chương trình được phép
- Tìm lỗ hổng high/critical
- Tối đa hóa thu nhập

### System Administrator
- Kiểm tra hệ thống của mình
- Phát hiện misconfiguration
- Cải thiện bảo mật

---

**⚡ Lời Khuyên Cuối**: Với hàng triệu IPs, dùng `scanner_async.py` với concurrency 400 trên máy 16GB+ RAM để đạt hiệu suất tối ưu (~300-500 URLs/giây).

**🔒 Nhớ**: Luôn sử dụng có trách nhiệm và hợp pháp!
