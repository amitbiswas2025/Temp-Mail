#!/usr/bin/env python3
"""
Replit-optimized startup script for Smart TempMail
Copyright @ISmartCoder
Updates Channel https://t.me/abirxdhackz
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_replit_environment():
    """Configure environment for Replit hosting"""
    
    # Set default values for Replit
    os.environ.setdefault('ENABLE_API', 'true')
    os.environ.setdefault('ENABLE_BOT', 'true') 
    os.environ.setdefault('ENABLE_KEEP_ALIVE', 'true')  # Always enable on Replit
    os.environ.setdefault('PORT', '8000')
    os.environ.setdefault('KEEP_ALIVE_PORT', '8080')
    os.environ.setdefault('KEEP_ALIVE_HOST', '0.0.0.0')
    
    # Replit-specific optimizations
    os.environ.setdefault('PYTHONUNBUFFERED', '1')
    os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')
    
    print("🔧 Replit environment configured")
    print(f"📡 API Port: {os.getenv('PORT')}")
    print(f"❤️  Keep-Alive Port: {os.getenv('KEEP_ALIVE_PORT')}")
    
    # Check for required bot token
    if not os.getenv('BOT_TOKEN'):
        print("⚠️  Warning: BOT_TOKEN not found in environment")
        print("   Please add your Telegram bot token to Replit Secrets:")
        print("   1. Go to Secrets tab in Replit")
        print("   2. Add key: BOT_TOKEN")
        print("   3. Add value: your_telegram_bot_token")
        return False
    
    return True

async def start_services():
    """Start all services for Replit"""
    print("🌟 Smart TempMail - Replit Edition")
    print("=" * 50)
    
    if not setup_replit_environment():
        print("❌ Environment setup failed")
        return
    
    # Import and start keep-alive first (required for Replit)
    try:
        from keep_alive import keep_alive
        keep_alive_thread = keep_alive()
        print("✅ Keep-alive server started")
    except Exception as e:
        print(f"❌ Failed to start keep-alive: {e}")
        return
    
    # Start API server
    api_enabled = os.getenv('ENABLE_API', 'true').lower() == 'true'
    if api_enabled:
        try:
            from main import app
            import uvicorn
            
            # Start API in background thread
            import threading
            
            def run_api():
                port = int(os.getenv('PORT', 8000))
                uvicorn.run(
                    app,
                    host="0.0.0.0",
                    port=port,
                    reload=False,
                    access_log=False
                )
            
            api_thread = threading.Thread(target=run_api, daemon=True)
            api_thread.start()
            print("✅ API server started")
            
            # Give API time to start
            await asyncio.sleep(3)
            
        except Exception as e:
            print(f"❌ Failed to start API: {e}")
    
    # Start Telegram bot
    bot_enabled = os.getenv('ENABLE_BOT', 'true').lower() == 'true'
    if bot_enabled:
        try:
            from bot import TempMailBot
            
            print("🤖 Starting Telegram bot...")
            bot = TempMailBot()
            
            # Set API URL to local Replit instance
            replit_url = f"https://{os.getenv('REPL_SLUG', 'smart-tempmail')}.{os.getenv('REPL_OWNER', 'user')}.repl.co"
            bot.api_url = os.getenv('API_URL', replit_url)
            
            print(f"🔗 Bot will connect to API at: {bot.api_url}")
            print("✅ Bot started successfully!")
            print("\n🎉 All services are running!")
            print(f"🌐 Web Interface: {replit_url}")
            print(f"❤️  Keep-Alive: {replit_url.replace('8000', '8080')}")
            print("🤖 Your Telegram bot is now live!")
            
            # Run bot (this will block)
            bot.run_bot()
            
        except Exception as e:
            print(f"❌ Failed to start bot: {e}")
            print("Check your BOT_TOKEN in Replit Secrets")
    else:
        print("🤖 Bot disabled, running API only")
        # Keep the script running for API
        try:
            while True:
                await asyncio.sleep(60)
                print("📊 Services running... (API + Keep-Alive)")
        except KeyboardInterrupt:
            print("🛑 Shutting down...")

if __name__ == "__main__":
    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested")
    except Exception as e:
        print(f"❌ Startup error: {e}")
        sys.exit(1)