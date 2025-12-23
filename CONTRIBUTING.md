# Contributing to SK Scanner Fast

Cảm ơn bạn đã quan tâm đến việc đóng góp cho dự án! 🎉

## 🤝 Cách đóng góp

### Báo cáo lỗi (Bug Reports)

Nếu bạn tìm thấy lỗi, vui lòng tạo issue với thông tin:

1. **Mô tả lỗi**: Giải thích rõ ràng lỗi là gì
2. **Cách tái hiện**: Các bước để tái hiện lỗi
3. **Kết quả mong đợi**: Bạn mong đợi điều gì xảy ra
4. **Kết quả thực tế**: Điều gì đã xảy ra
5. **Môi trường**:
   - OS: (Windows/Linux/Mac)
   - Python version: (3.7/3.8/3.9/...)
   - Tool version: (2.0.0)
6. **Screenshots/Logs**: Nếu có

### Đề xuất tính năng (Feature Requests)

Để đề xuất tính năng mới:

1. **Mô tả tính năng**: Giải thích chi tiết tính năng
2. **Use case**: Tại sao tính năng này hữu ích
3. **Giải pháp đề xuất**: Bạn nghĩ nên implement như thế nào
4. **Alternatives**: Các giải pháp thay thế (nếu có)

### Pull Requests

1. **Fork** repo
2. **Clone** fork của bạn:
   ```bash
   git clone https://github.com/your-username/sk-scanner-fast.git
   ```
3. **Tạo branch** mới:
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **Commit** changes:
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push** lên branch:
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Tạo Pull Request**

## 📝 Code Style

### Python

- Tuân thủ **PEP 8**
- Sử dụng **type hints** khi có thể
- Viết **docstrings** cho functions/classes
- Giữ functions ngắn gọn và tập trung
- Sử dụng **async/await** cho I/O operations

### Ví dụ:

```python
async def scan_url(self, url: str, session: aiohttp.ClientSession) -> bool:
    """
    Scan a single URL for vulnerabilities.
    
    Args:
        url: Target URL to scan
        session: Aiohttp client session
        
    Returns:
        True if vulnerability found, False otherwise
    """
    try:
        # Implementation
        pass
    except Exception as e:
        # Error handling
        pass
```

## 🧪 Testing

Trước khi submit PR:

1. **Test thủ công**:
   ```bash
   python scanner_fast.py
   ```

2. **Test với file URLs nhỏ** (10-100 URLs)

3. **Kiểm tra**:
   - Tool chạy không lỗi
   - Output files được tạo đúng
   - Progress bar hiển thị chính xác
   - Telegram notifications hoạt động (nếu có)

## 📋 Commit Messages

Format:
```
<type>: <subject>

<body>
```

**Types:**
- `feat`: Tính năng mới
- `fix`: Sửa lỗi
- `perf`: Cải thiện performance
- `docs`: Cập nhật documentation
- `style`: Code formatting
- `refactor`: Refactor code
- `test`: Thêm tests
- `chore`: Maintenance tasks

**Ví dụ:**
```
feat: add proxy support

- Add SOCKS5 proxy configuration
- Support proxy rotation
- Update documentation
```

## 🎯 Ưu tiên

Các đóng góp được ưu tiên:

1. **Bug fixes** - Luôn được chào đón
2. **Performance improvements** - Tối ưu tốc độ/RAM
3. **Documentation** - Cải thiện docs
4. **New features** - Tính năng hữu ích

## ❌ Không chấp nhận

- Code không tuân thủ PEP 8
- Breaking changes không có lý do chính đáng
- Features làm giảm performance đáng kể
- Code có security issues
- Malicious code

## 📞 Liên hệ

Nếu có câu hỏi, liên hệ:
- Telegram: [@hiamhuy](https://t.me/hiamhuy)
- GitHub Issues: [Create new issue](https://github.com/yourusername/sk-scanner-fast/issues)

## 📜 License

Bằng việc đóng góp, bạn đồng ý rằng contributions của bạn sẽ được license dưới MIT License.

---

**Cảm ơn bạn đã đóng góp! 🙏**
