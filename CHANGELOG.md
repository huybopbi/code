# Changelog

All notable changes to SK Scanner Fast will be documented in this file.

## [2.0.0] - 2024-12-23

### Added
- ✨ Loại bỏ hoàn toàn database tracking để tối ưu tốc độ
- ✨ Thêm pyfiglet ASCII art banner
- ✨ Thêm system monitoring (CPU & RAM usage)
- ✨ Thêm admin Telegram notification (hidden)
- ✨ Cache system stats (update mỗi 5s)
- ✨ Tree-style menu với box-drawing characters

### Changed
- ⚡ Tăng chunk size từ 5,000 lên 10,000 URLs
- ⚡ Tối ưu progress update (mỗi 200 URLs thay vì 100)
- ⚡ Tăng limit_per_host từ 50 lên 100
- ⚡ Enable DNS caching 300 seconds
- ⚡ Enable connection reuse
- 🎨 Cải thiện giao diện progress bar
- 🎨 Đổi màu SK valid keys từ pink sang green
- 🎨 Compact progress format (loại bỏ "ETA:")

### Fixed
- 🐛 Sửa lỗi hiển thị RAM có nhiều dấu %
- 🐛 Sửa lỗi thiếu SK counter trên progress bar
- 🐛 Sửa lỗi pyfiglet không được require

### Performance
- 🚀 Tốc độ tăng từ 300-500 URLs/s lên 500-1000+ URLs/s
- 💚 RAM usage giảm xuống ~200MB
- ⚡ Giảm overhead từ database operations

## [1.0.0] - 2024-12-09

### Added
- 🎉 Initial release
- ⚡ Async/concurrent scanning
- 🔍 ENV file scanner
- 🐛 Debug mode scanner
- 💳 Stripe key detection
- ✅ Auto-check Stripe keys via API
- 📱 Telegram notifications
- 🎨 Colored progress bar
- 📊 Real-time statistics

### Features
- Dual scan mode (ENV & Debug)
- Configurable concurrency
- Random user agents
- Timeout handling
- Error recovery
- Output to organized folders

---

## Version Format

Format: `[MAJOR.MINOR.PATCH]`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

## Emoji Legend

- ✨ New feature
- ⚡ Performance improvement
- 🐛 Bug fix
- 🎨 UI/UX improvement
- 📝 Documentation
- 🔒 Security
- 🚀 Speed optimization
- 💚 Memory optimization
