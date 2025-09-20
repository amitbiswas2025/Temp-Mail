# 🤖 Smart TempMail Telegram Bot

A powerful Telegram bot that integrates with the Smart TempMail API to provide instant temporary email generation and message checking directly through Telegram.

## 🌟 Features

- **📧 Multiple Email Types**: Generate regular, 10-minute, and .edu temporary emails
- **🔄 Real-time Message Checking**: Check incoming messages instantly
- **⚡ Lightning Fast**: Async architecture for optimal performance
- **🎯 User-Friendly Interface**: Interactive buttons and easy commands
- **📱 Mobile Optimized**: Perfect for mobile Telegram usage
- **🔒 Session Management**: Secure token-based email tracking

## 🚀 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message with quick actions |
| `/gen` | Generate regular temporary email |
| `/tenmin` | Generate 10-minute email (auto-expires) |
| `/edu` | Generate educational (.edu) email |
| `/check` | Check messages for your active emails |
| `/help` | Show help and usage instructions |

## 📋 Setup Instructions

### Prerequisites

1. **Python 3.11+** installed
2. **Telegram Bot Token** from [@BotFather](https://t.me/BotFather)
3. **Running TempMail API** (local or deployed)

### Step 1: Create Your Telegram Bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command
3. Choose a name for your bot (e.g., "Smart TempMail Bot")
4. Choose a username (e.g., "smart_tempmail_bot")
5. Copy the bot token provided

### Step 2: Configure Environment

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file and add your bot token:
   ```env
   BOT_TOKEN=your_telegram_bot_token_here
   API_URL=http://localhost:8000
   LOG_LEVEL=INFO
   PORT=8000
   ```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Services

#### Option 1: Run Both API and Bot Together
```bash
# Terminal 1 - Start the API
python main.py

# Terminal 2 - Start the Bot
python bot.py
```

#### Option 2: Run Only the Bot (if API is deployed elsewhere)
```bash
# Update API_URL in .env to your deployed API
python bot.py
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BOT_TOKEN` | Telegram bot token from BotFather | Required |
| `API_URL` | URL of your TempMail API | `http://localhost:8000` |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | `INFO` |
| `PORT` | Port for web service | `8000` |

## 📱 Bot Usage

### 1. Start the Bot
Send `/start` to get the welcome message with quick action buttons.

### 2. Generate Emails
- **Regular Email**: `/gen` or tap "📧 Generate Email"
- **10-Minute Email**: `/tenmin` or tap "⏱️ 10-Min Email"  
- **Educational Email**: `/edu` or tap "🎓 Edu Email"

### 3. Check Messages
- **All Emails**: `/check` or tap "📬 Check Messages"
- **Specific Email**: Use the "📬 Check Messages" button under each generated email

### 4. Copy Information
Tap on the generated email or token to copy it to your clipboard.

## 🚀 Deployment

### Local Development
```bash
# Start API
python main.py

# Start Bot (in another terminal)
python bot.py
```

### Replit Deployment (Easiest) 🚀

1. **Create Replit Project**:
   - Go to [replit.com](https://replit.com)
   - Click "Create Repl" → "Import from GitHub"
   - Paste your GitHub repo URL or upload files
   - Name your repl (e.g., "smart-tempmail")

2. **Configure Secrets**:
   - Click "Secrets" tab in sidebar
   - Add: `BOT_TOKEN` = your_telegram_bot_token
   - Add: `API_URL` = https://your-repl-name.your-username.repl.co

3. **Deploy**:
   ```bash
   # Just click the green "Run" button!
   # Or use: python replit_main.py
   ```

4. **Your URLs**:
   - Web: `https://your-repl.repl.co`
   - Keep-Alive: `https://your-repl.repl.co:8080`
   - Bot: Works instantly via Telegram

### Heroku Deployment

1. **Create Heroku App**:
   ```bash
   heroku create your-app-name
   ```

2. **Set Environment Variables**:
   ```bash
   heroku config:set BOT_TOKEN=your_bot_token
   heroku config:set API_URL=https://your-app-name.herokuapp.com
   ```

3. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy Smart TempMail Bot"
   git push heroku main
   ```

4. **Scale Processes**:
   ```bash
   heroku ps:scale web=1 bot=1
   ```

### Docker Deployment

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8000
   CMD ["python", "main.py"]
   ```

2. **Build and Run**:
   ```bash
   docker build -t smart-tempmail .
   docker run -p 8000:8000 -e BOT_TOKEN=your_token smart-tempmail
   ```

## 🛠️ Development

### Project Structure
```
├── main.py              # FastAPI web server
├── bot.py               # Telegram bot
├── index.html           # API documentation
├── requirements.txt     # Python dependencies
├── Procfile            # Process configuration
├── runtime.txt         # Python version
├── .env                # Environment variables
├── .env.example        # Environment template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

### Adding New Features

1. **New Commands**: Add handlers in `bot.py`
2. **New API Endpoints**: Add routes in `main.py`
3. **Enhanced UI**: Modify inline keyboards and messages

### Testing

```bash
# Test the API
curl http://localhost:8000/api/gen

# Test bot locally
python bot.py
```

## 🔍 Troubleshooting

### Common Issues

1. **Bot Not Responding**
   - Check if `BOT_TOKEN` is correct
   - Ensure bot is started with `/start` command
   - Verify API is running and accessible

2. **API Connection Errors**
   - Check `API_URL` in `.env`
   - Ensure API server is running
   - Check firewall/network settings

3. **Import Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Use virtual environment for isolation

### Debug Mode

Enable debug logging:
```env
LOG_LEVEL=DEBUG
```

## 📄 API Integration

The bot integrates with these API endpoints:

- `GET /api/gen` - Generate regular email
- `GET /api/chk?token=<token>` - Check regular email messages
- `GET /api/10min/gen` - Generate 10-minute email
- `GET /api/10min/chk?token=<token>` - Check 10-minute email messages
- `GET /api/edu/gen` - Generate educational email
- `GET /api/edu/chk?token=<token>` - Check educational email messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📞 Support

- **Developer**: [@ISmartCoder](https://t.me/ISmartCoder)
- **Updates Channel**: [@WeSmartDevelopers](https://t.me/WeSmartDevelopers)
- **Community**: [@TheSmartDev](https://t.me/TheSmartDev)

## 📜 License

This project is developed by @ISmartCoder. For commercial use or customization, contact [@ISmartCoder](https://t.me/ISmartCoder).

## 🎯 Features Overview

### ✅ Current Features
- Multiple email types (regular, 10-min, edu)
- Real-time message checking
- Interactive Telegram interface
- Session management
- Auto-expiration for 10-minute emails
- Copy-to-clipboard functionality
- Error handling and user feedback

### 🔮 Future Enhancements
- Message forwarding to Telegram
- Email notifications
- Scheduled message checking
- Advanced filtering options
- Multi-language support
- Analytics and usage stats

---

**Made with ❤️ by [@ISmartCoder](https://t.me/ISmartCoder)**