# 🔑 Stripe Key Scanner

A powerful multithreaded Python tool for scanning websites to find exposed `.env` files containing Stripe API keys and secrets.

## ✨ Features

- 🚀 **Multithreaded scanning** - Fast concurrent processing (default: 10 threads)
- 🎯 **Smart detection** - Scans 40+ common `.env` file paths
- 📦 **Extended path list** - Optional 500+ path file for comprehensive scanning
- 📱 **Telegram notifications** - Get instant alerts when Stripe keys are found
- 📊 **Progress tracking** - Real-time progress with processed/found counters
- 💾 **Session management** - Resume interrupted scans
- 📝 **Detailed logging** - File and console logging with timestamps
- 🔄 **Retry mechanism** - Automatic retries with exponential backoff
- 🛡️ **Memory protection** - Response size limits to prevent memory issues
- 📤 **Multiple output formats** - Text files and optional JSON output

## 📋 Requirements

- Python 3.6+
- Required packages:
  ```bash
  pip install requests urllib3 colorama
  ```

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/huybopbi/code.git
   cd code
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create your URL list file (one URL per line):
   ```bash
   echo "http://example.com" > urls.txt
   echo "http://example2.com" >> urls.txt
   ```

## ⚙️ Configuration

### Telegram Notifications (Optional)

Configure Telegram notifications directly in `code.py` (lines 42-43):

```python
TELEGRAM_BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
TELEGRAM_CHAT_ID = "123456789"
```

**How to get Telegram credentials:**

1. Create a bot via [@BotFather](https://t.me/BotFather)
   - Send `/newbot` and follow instructions
   - Save the bot token

2. Get your Chat ID:
   - Send a message to your bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find `"chat":{"id":123456789}`

## 📖 Usage

### Basic Usage

```bash
# Interactive mode (will prompt for URL list)
python code.py

# With URL list file
python code.py --list urls.txt

# With custom threads
python code.py --list urls.txt --threads 20

# With Telegram notifications
python code.py --list urls.txt \
  --telegram-bot-token "YOUR_TOKEN" \
  --telegram-chat-id "YOUR_CHAT_ID"
```

### Advanced Options

```bash
# Use 500+ path file for comprehensive scanning
python code.py --list urls.txt --path-file path.txt

# Custom timeout and retries
python code.py --list urls.txt --timeout 10 --retries 3

# Disable TLS verification (for testing)
python code.py --list urls.txt --insecure

# Follow redirects
python code.py --list urls.txt --redirects

# Add rate limiting (0.5 seconds between requests)
python code.py --list urls.txt --rate 0.5

# JSON output
python code.py --list urls.txt --json-out results.json

# Custom paths (override defaults)
python code.py --list urls.txt --paths /.env /api/.env /admin/.env
```

## 🎛️ Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--list` | Path to file containing URLs (one per line) | Interactive prompt |
| `--threads` | Number of concurrent threads | 10 |
| `--timeout` | Request timeout in seconds | 5.0 |
| `--retries` | Max retries per request | 2 |
| `--insecure` | Disable TLS verification | False |
| `--redirects` | Allow following redirects | False |
| `--paths` | Custom .env paths to try | 40 built-in paths |
| `--path-file` | File with custom paths (500+) | None |
| `--rate` | Sleep seconds between requests | 0.0 |
| `--json-out` | Write JSONL output to file | None |
| `--telegram-bot-token` | Telegram bot token | From config |
| `--telegram-chat-id` | Telegram chat ID | From config |

## 📁 Output Files

All results are saved in the `Results/` directory:

### Main Output Files

- **`Results/STRIPE.txt`** - Found Stripe keys with details
  ```
  URL: http://example.com
  METHOD: .env
  STRIPE_KEY: sk_live_xxxxx
  STRIPE_SECRET: rk_live_xxxxx
  ```

- **`Results/scan.log`** - Detailed scan log with timestamps

### Log Files (in `Results/logsites/`)

- **`vulnerable.txt`** - URLs with accessible .env files
- **`stripesite.txt`** - URLs with Stripe keys found
- **`not_vulnerable.txt`** - URLs without .env files
- **`exception_sites.txt`** - URLs that caused errors

### Session Files

- **`.nero_swallowtail`** - Session restore data (auto-created on interrupt)

## 📱 Telegram Notification Format

When Stripe keys are found, you'll receive a formatted message:

```
🔑 STRIPE KEY FOUND!

URL: http://example.com
METHOD: .env
STRIPE_KEY: sk_live_xxxxxxxxxxxxx
STRIPE_SECRET: rk_live_xxxxxxxxxxxxx
```

## 🗂️ Path Files

### Default Paths (40 paths)

The tool includes 40 commonly used `.env` paths:
- `/.env`
- `/.env.local`
- `/.env.production`
- `/api/.env`
- `/backend/.env`
- And 35+ more...

### Extended Path File (500+ paths)

Use `path.txt` for comprehensive scanning:

```bash
python code.py --list urls.txt --path-file path.txt
```

This includes paths like:
- Framework-specific paths (Laravel, Django, React, etc.)
- Environment-specific paths (dev, staging, production)
- Common directory structures
- Legacy paths

## 🎯 Detection Methods

The tool uses two methods to find Stripe keys:

1. **`.env` file scanning** - Direct access to .env files
   - Searches for `STRIPE_KEY=` and `STRIPE_SECRET=`
   - Supports quoted and unquoted values

2. **Debug page detection** - Laravel debug pages
   - Searches for `<td>STRIPE_KEY</td>` and `<td>STRIPE_SECRET</td>`
   - Extracts values from HTML tables

## ⚡ Performance Tips

- **Default (Fast):** Use built-in 40 paths for quick scans
- **Comprehensive (Slow):** Use `--path-file path.txt` for thorough scanning
- **Rate Limiting:** Add `--rate 0.5` to avoid overwhelming targets
- **Threading:** Increase `--threads 20` for faster scans (use responsibly)
- **Timeout:** Adjust `--timeout 10` for slow targets

## 🔄 Session Management

The tool supports session resumption:

1. **During scan:** Press `Ctrl+C` to interrupt
2. **On restart:** The tool will ask if you want to restore the session
3. **Choose:**
   - `Y` - Resume from where you left off
   - `n` - Start a new scan

## 📊 Progress Monitoring

During scanning, you'll see:

```bash
2025-01-15 10:30:00 - INFO - Starting scan: 1000 URLs, 10 threads
# http://example1.com | Can't get everything
# http://example2.com | STRIPE
# http://example3.com | Can't access sites
[100/1000] Found: 5
[200/1000] Found: 12
...
============================================================
Scan completed!
Processed: 1000/1000
Found Stripe keys: 25
============================================================
```

## ⚠️ Legal Disclaimer

**This tool is for educational and authorized security testing purposes only.**

- ✅ Use only on systems you own or have explicit permission to test
- ✅ Obtain proper authorization before scanning
- ✅ Comply with all applicable laws and regulations
- ❌ Do not use for malicious purposes
- ❌ Do not use for unauthorized access
- ❌ Do not use for illegal activities

The authors are not responsible for misuse of this tool.

## 🛠️ Troubleshooting

### Common Issues

**"Wrong input or list not found!"**
- Ensure your URL list file exists
- Check the file path is correct

**"Response too large"**
- Normal behavior, the tool skips files > 10MB to prevent memory issues

**Telegram notifications not working**
- Verify bot token and chat ID are correct
- Ensure you've sent at least one message to the bot
- Check `Results/scan.log` for error messages

**Too many timeouts**
- Increase `--timeout` value
- Reduce `--threads` to avoid overwhelming the network
- Add `--rate 0.5` for rate limiting

## 📝 Example Workflow

```bash
# 1. Create URL list
cat > targets.txt << EOF
http://example1.com
http://example2.com
http://example3.com
EOF

# 2. Quick scan with defaults
python code.py --list targets.txt

# 3. Comprehensive scan with Telegram
python code.py --list targets.txt \
  --path-file path.txt \
  --threads 15 \
  --telegram-bot-token "123456:ABC..." \
  --telegram-chat-id "123456789" \
  --json-out results.json

# 4. Check results
cat Results/STRIPE.txt
cat Results/scan.log
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📜 License

This project is provided as-is for educational purposes.

## 🔗 Links

- **Repository:** https://github.com/huybopbi/code
- **Issues:** https://github.com/huybopbi/code/issues

## 👨‍💻 Author

Created by [@huybopbi](https://github.com/huybopbi)

---

**Remember:** Always obtain proper authorization before scanning any systems you don't own. Use responsibly! 🛡️
