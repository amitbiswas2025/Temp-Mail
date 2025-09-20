#!/bin/bash
# Quick Replit deployment script
# Copyright @ISmartCoder

echo "🌟 Smart TempMail - Replit Quick Deploy"
echo "======================================"

# Check if we're in Replit environment
if [ -n "$REPL_SLUG" ]; then
    echo "✅ Replit environment detected"
    echo "📝 Repl: $REPL_SLUG"
    echo "👤 Owner: $REPL_OWNER"
else
    echo "⚠️  Not running in Replit environment"
fi

# Set environment variables for Replit
export ENABLE_API=true
export ENABLE_BOT=true
export ENABLE_KEEP_ALIVE=true
export PORT=8000
export KEEP_ALIVE_PORT=8080
export PYTHONUNBUFFERED=1

echo "🔧 Environment configured for Replit"

# Check for bot token
if [ -z "$BOT_TOKEN" ]; then
    echo "❌ BOT_TOKEN not found!"
    echo "Please add your bot token to Replit Secrets:"
    echo "1. Click 'Secrets' tab"
    echo "2. Key: BOT_TOKEN"
    echo "3. Value: your_telegram_bot_token"
    exit 1
fi

echo "✅ BOT_TOKEN found"

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Start the application
echo "🚀 Starting Smart TempMail services..."
python replit_main.py