#!/usr/bin/env python3
"""
Smart TempMail - Unified Startup Script
Copyright @ISmartCoder
Updates Channel https://t.me/abirxdhackz

This script starts both the API server and Telegram bot with keep-alive functionality.
"""

import os
import sys
import time
import signal
import subprocess
from threading import Thread
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ServiceManager:
    def __init__(self):
        self.processes = {}
        self.running = True
        
    def start_service(self, name, command, shell=False):
        """Start a service in a subprocess"""
        try:
            print(f"🚀 Starting {name}...")
            process = subprocess.Popen(
                command,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            self.processes[name] = process
            print(f"✅ {name} started with PID: {process.pid}")
            return process
        except Exception as e:
            print(f"❌ Failed to start {name}: {e}")
            return None
    
    def monitor_process(self, name, process):
        """Monitor a process and log its output"""
        try:
            for line in iter(process.stdout.readline, ''):
                if line.strip():
                    print(f"[{name}] {line.strip()}")
                    
            process.wait()
            print(f"⚠️  {name} process ended with code: {process.returncode}")
        except Exception as e:
            print(f"❌ Error monitoring {name}: {e}")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🛑 Received signal {signum}. Shutting down services...")
        self.shutdown()
        sys.exit(0)
    
    def shutdown(self):
        """Shutdown all services"""
        self.running = False
        print("🛑 Shutting down all services...")
        
        for name, process in self.processes.items():
            try:
                print(f"🛑 Stopping {name}...")
                process.terminate()
                
                # Wait for graceful shutdown
                try:
                    process.wait(timeout=10)
                    print(f"✅ {name} stopped gracefully")
                except subprocess.TimeoutExpired:
                    print(f"⚠️  Force killing {name}...")
                    process.kill()
                    process.wait()
                    print(f"✅ {name} force killed")
            except Exception as e:
                print(f"❌ Error stopping {name}: {e}")
    
    def run_all_services(self):
        """Start and monitor all services"""
        # Register signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Configuration
        api_enabled = os.getenv('ENABLE_API', 'true').lower() == 'true'
        bot_enabled = os.getenv('ENABLE_BOT', 'true').lower() == 'true'
        keep_alive_enabled = os.getenv('ENABLE_KEEP_ALIVE', 'false').lower() == 'true'
        
        print("🌟 Smart TempMail - Service Manager")
        print("=" * 50)
        print(f"📡 API Server: {'Enabled' if api_enabled else 'Disabled'}")
        print(f"🤖 Telegram Bot: {'Enabled' if bot_enabled else 'Disabled'}")
        print(f"❤️  Keep-Alive: {'Enabled' if keep_alive_enabled else 'Disabled'}")
        print("=" * 50)
        
        # Start services
        threads = []
        
        if api_enabled:
            api_process = self.start_service("API", [sys.executable, "main.py"])
            if api_process:
                thread = Thread(target=self.monitor_process, args=("API", api_process), daemon=True)
                thread.start()
                threads.append(thread)
        
        if bot_enabled:
            # Set keep-alive environment variable for bot
            if keep_alive_enabled:
                os.environ['ENABLE_KEEP_ALIVE'] = 'true'
            
            bot_process = self.start_service("BOT", [sys.executable, "bot.py"])
            if bot_process:
                thread = Thread(target=self.monitor_process, args=("BOT", bot_process), daemon=True)
                thread.start()
                threads.append(thread)
        
        if not self.processes:
            print("❌ No services started. Check your configuration.")
            return
        
        print("\n✅ All services started successfully!")
        print("🔗 Access URLs:")
        
        if api_enabled:
            port = os.getenv('PORT', '8000')
            print(f"   📡 API: http://localhost:{port}")
            print(f"   📚 Docs: http://localhost:{port}/docs")
        
        if keep_alive_enabled:
            keep_port = os.getenv('KEEP_ALIVE_PORT', '8080')
            print(f"   ❤️  Keep-Alive: http://localhost:{keep_port}")
        
        print("\n⌨️  Press Ctrl+C to stop all services")
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
                
                # Check if any process died
                for name, process in list(self.processes.items()):
                    if process.poll() is not None:
                        print(f"⚠️  {name} process died unexpectedly!")
                        del self.processes[name]
                
                # If all processes are dead, exit
                if not self.processes:
                    print("❌ All services have stopped")
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Keyboard interrupt received")
        finally:
            self.shutdown()

def show_help():
    """Show help message"""
    help_text = """
🌟 Smart TempMail Service Manager

Usage: python start.py [options]

Options:
  --help, -h     Show this help message
  --api-only     Run only the API server
  --bot-only     Run only the Telegram bot
  --with-keepalive  Enable keep-alive server (for hosting platforms)

Environment Variables:
  ENABLE_API=true/false        Enable/disable API server (default: true)
  ENABLE_BOT=true/false        Enable/disable Telegram bot (default: true)  
  ENABLE_KEEP_ALIVE=true/false Enable/disable keep-alive server (default: false)
  BOT_TOKEN=your_token         Your Telegram bot token
  API_URL=http://localhost:8000 API URL for bot to connect to
  PORT=8000                    API server port
  KEEP_ALIVE_PORT=8080         Keep-alive server port

Examples:
  python start.py                    # Run both API and bot
  python start.py --api-only         # Run only API server
  python start.py --bot-only         # Run only Telegram bot
  python start.py --with-keepalive   # Run with keep-alive server

Developer: @ISmartCoder
Updates: @WeSmartDevelopers
    """
    print(help_text)

if __name__ == "__main__":
    # Parse command line arguments
    args = sys.argv[1:]
    
    if '--help' in args or '-h' in args:
        show_help()
        sys.exit(0)
    
    # Set environment variables based on arguments
    if '--api-only' in args:
        os.environ['ENABLE_API'] = 'true'
        os.environ['ENABLE_BOT'] = 'false'
    elif '--bot-only' in args:
        os.environ['ENABLE_API'] = 'false'
        os.environ['ENABLE_BOT'] = 'true'
    
    if '--with-keepalive' in args:
        os.environ['ENABLE_KEEP_ALIVE'] = 'true'
    
    # Check if required environment variables are set
    if os.getenv('ENABLE_BOT', 'true').lower() == 'true' and not os.getenv('BOT_TOKEN'):
        print("❌ BOT_TOKEN environment variable is required when bot is enabled")
        print("   Get your token from @BotFather and set it in .env file")
        sys.exit(1)
    
    # Start service manager
    try:
        manager = ServiceManager()
        manager.run_all_services()
    except Exception as e:
        print(f"❌ Service manager error: {e}")
        sys.exit(1)