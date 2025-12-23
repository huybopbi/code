# 🚀 SK Scanner - Fast Mode

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Speed](https://img.shields.io/badge/speed-500--1000%20URLs%2Fs-brightgreen.svg)](README.md)

**Maximum Speed Edition** - Scanner tốc độ cao để tìm file .env bị lộ và Stripe keys

![SK Scanner Screenshot](scanner-fast.png)

## 📖 Giới thiệu

SK Scanner Fast là công cụ quét bảo mật tốc độ cao, được tối ưu hóa để phát hiện:
- 🔍 File `.env` bị lộ
- 🐛 Debug mode exposure
- 💳 Stripe API keys (`sk_live_*`)

Với tốc độ **500-1000+ URLs/giây**, tool này loại bỏ hoàn toàn database tracking để đạt hiệu suất tối đa.

## ✨ Tính năng chính

- ⚡ **Tốc độ cực cao**: 500-1000+ URLs/s
- 🚫 **Không database**: Zero overhead, maximum speed
- 💳 **Stripe checker**: Auto-check keys qua API
- 📱 **Telegram alerts**: Thông báo real-time
- 🎨 **Giao diện đẹp**: ASCII art + progress bar
- 📊 **System monitor**: CPU & RAM tracking
- 🔄 **Async/Concurrent**: Xử lý hàng nghìn requests đồng thời

## 🚀 Quick Start

### 1. Cài đặt

```bash
# Clone repo
git clone https://github.com/yourusername/sk-scanner-fast.git
cd sk-scanner-fast

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Chuẩn bị file URLs

Tạo file `urls.txt`:
```
example.com
test.com
demo.com
```

### 3. Chạy scanner

```bash
python scanner_fast.py
```

## 📦 Requirements

- Python 3.7+
- aiohttp
- aiofiles
- urllib3
- pyfiglet
- psutil

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

```
ENVS/           # File .env tìm được
DEBUG/          # Debug mode responses
SK_LIVE.TXT     # Tất cả Stripe keys
SK_VALID.TXT    # Valid Stripe keys (nếu bật auto-check)
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
