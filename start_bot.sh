#!/bin/bash

# University Course Registration Bot Startup Script

echo "🎓 Starting University Course Registration Bot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "✅ Activating virtual environment..."
    source venv/bin/activate
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found! Please create it with your bot token."
    exit 1
fi

# Check if bot token is set
if ! grep -q "TELEGRAM_BOT_TOKEN=" .env; then
    echo "❌ TELEGRAM_BOT_TOKEN not found in .env file!"
    exit 1
fi

echo "🚀 Starting bot..."
python main.py