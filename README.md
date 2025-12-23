# 🚀 SK Scanner - Fast Mode

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Speed](https://img.shields.io/badge/speed-500--1000%20URLs%2Fs-brightgreen.svg)](README.md)

**Maximum Speed Edition** - Scanner tốc độ cao để tìm file .env bị lộ và Stripe keys

![SK Scanner Screenshot](scanner-fast.png)

## 📖 Giới thiệu

Bộ công cụ bảo mật tốc độ cao gồm 2 tools:

### 🚀 SK Scanner Fast
Công cụ quét bảo mật tốc độ cao, được tối ưu hóa để phát hiện:
- 🔍 File `.env` bị lộ
- 🐛 Debug mode exposure
- 💳 Stripe API keys (`sk_live_*`)

Với tốc độ **500-1000+ URLs/giây**, tool này loại bỏ hoàn toàn database tracking để đạt hiệu suất tối đa.

### 🌐 IP Scanner
Công cụ quét IP sử dụng masscan để tìm hosts có port mở:
- ⚡ Tốc độ cao với masscan
- 🎯 Hỗ trợ quét theo file ranges hoặc toàn bộ Internet
- 📊 Giới hạn số lượng IP và timeout
- 🎨 Giao diện đẹp với màu sắc

## ✨ Tính năng chính

### SK Scanner Fast
- ⚡ **Tốc độ cực cao**: 500-1000+ URLs/s
- 🚫 **Không database**: Zero overhead, maximum speed
- 💳 **Stripe checker**: Auto-check keys qua API
- 📱 **Telegram alerts**: Thông báo real-time
- 🎨 **Giao diện đẹp**: ASCII art + progress bar
- 📊 **System monitor**: CPU & RAM tracking
- 🔄 **Async/Concurrent**: Xử lý hàng nghìn requests đồng thời

### IP Scanner
- ⚡ **Masscan integration**: Tốc độ quét cực nhanh
- 🎯 **Flexible targeting**: File ranges hoặc toàn bộ Internet (0.0.0.0/0)
- 📊 **Smart limits**: Giới hạn số IP và timeout
- 🎨 **Beautiful UI**: Giao diện màu sắc, dễ sử dụng
- 🔧 **Customizable**: Tùy chỉnh ports, rate, output
- 📈 **Real-time stats**: Hiển thị tiến độ và kết quả

## 🚀 Quick Start

### SK Scanner Fast

```bash
# 1. Clone repo
git clone https://github.com/huybopbi/code.git
cd code

# 2. Cài đặt dependencies
pip install -r requirements.txt

# 3. Tạo file URLs
echo "example.com" > urls.txt
echo "test.com" >> urls.txt

# 4. Chạy scanner
python scanner_fast.py
```

### IP Scanner

```bash
# 1. Cài đặt masscan (Linux)
sudo apt install masscan

# 2. Tạo file IP ranges (tùy chọn)
echo "1.0.0.0/8" > ranges.txt
echo "8.8.8.0/24" >> ranges.txt

# 3. Chạy scanner
sudo bash scanip.sh
```

## 📦 Requirements

### SK Scanner Fast
- Python 3.7+
- aiohttp
- aiofiles
- urllib3
- pyfiglet
- psutil

### IP Scanner
- Linux/Unix system
- masscan
- Root privileges (sudo)

## 📖 Hướng dẫn chi tiết

Xem [README_FAST.md](README_FAST.md) để biết hướng dẫn đầy đủ.

## 📊 Performance

| Metric | Value |
|--------|-------|
| Speed | 500-1000 URLs/s |
| RAM Usage | ~200MB |
| Concurrency | Up to 2000 |
| Chunk Size | 10,000 URLs |

## 🆚 So sánh

| Feature | Fast Mode | Standard Mode |
|---------|-----------|---------------|
| Speed | 🚀🚀🚀 | 🚀 |
| Database | ❌ | ✅ |
| Tracking | ❌ | ✅ |
| Resume | ❌ | ✅ |
| Use Case | Quick scans | Full tracking |

## 📁 Output

### SK Scanner Fast
```
ENVS/           # File .env tìm được
DEBUG/          # Debug mode responses
SK_LIVE.TXT     # Tất cả Stripe keys
SK_VALID.TXT    # Valid Stripe keys (nếu bật auto-check)
```

### IP Scanner
```
result.txt      # Danh sách IPs có port mở (hoặc tên tùy chỉnh)
```

## ⚠️ Disclaimer

Tool này chỉ dành cho:
- ✅ Security testing với quyền hợp pháp
- ✅ Bug bounty programs
- ✅ Educational purposes

**KHÔNG** sử dụng cho mục đích bất hợp pháp. Tác giả không chịu trách nhiệm về việc sử dụng sai mục đích.

## 👨‍💻 Tác giả

**Phạm Quang Huy** ([@hiamhuy](https://t.me/hiamhuy))

## 📝 License

MIT License - Xem [LICENSE](LICENSE) để biết chi tiết

## 🌟 Support

Nếu thấy hữu ích, hãy cho repo một ⭐!

---

**Version**: 2.0 - Maximum Speed Edition
