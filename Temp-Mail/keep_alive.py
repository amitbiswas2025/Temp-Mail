# Keep Alive Server for Smart TempMail Bot
# Copyright @ISmartCoder
# Updates Channel https://t.me/abirxdhackz

from flask import Flask, jsonify
from threading import Thread
import logging
import os
import time
from datetime import datetime
import socket

# Suppress Flask's default logging to reduce noise
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# Create Flask app with error handling
app = Flask(__name__)
app.config['ENV'] = 'production'

# Global variables for server management
server_thread = None
start_time = datetime.now()

def get_local_ip():
    """Get local IP address"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

def is_port_available(port):
    """Check if port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', port))
            return True
    except OSError:
        return False

@app.route('/')
def index():
    """Main keep-alive endpoint"""
    uptime = datetime.now() - start_time
    return jsonify({
        "status": "alive",
        "message": "Smart TempMail Keep-Alive Server",
        "uptime": str(uptime).split('.')[0],  # Remove microseconds
        "timestamp": datetime.now().isoformat(),
        "local_ip": get_local_ip(),
        "developer": "@ISmartCoder"
    })

@app.route('/health')
def health():
    """Detailed health check endpoint"""
    uptime = datetime.now() - start_time
    uptime_seconds = int(uptime.total_seconds())
    
    return jsonify({
        "status": "healthy",
        "service": "Smart TempMail Keep-Alive",
        "uptime": {
            "human": str(uptime).split('.')[0],
            "seconds": uptime_seconds,
            "started_at": start_time.isoformat()
        },
        "system": {
            "local_ip": get_local_ip(),
            "port": int(os.getenv('KEEP_ALIVE_PORT', 8080)),
            "environment": app.config.get('ENV', 'unknown')
        },
        "api": {
            "developer": "@ISmartCoder",
            "updates_channel": "@WeSmartDevelopers",
            "version": "2.0.0"
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/ping')
def ping():
    """Simple ping endpoint for monitoring"""
    return jsonify({
        "response": "pong",
        "timestamp": datetime.now().isoformat(),
        "status": "ok"
    })

@app.route('/stats')
def stats():
    """Server statistics endpoint"""
    uptime = datetime.now() - start_time
    return jsonify({
        "server": "Smart TempMail Keep-Alive",
        "stats": {
            "uptime_seconds": int(uptime.total_seconds()),
            "uptime_human": str(uptime).split('.')[0],
            "started_at": start_time.isoformat(),
            "current_time": datetime.now().isoformat(),
            "local_ip": get_local_ip(),
            "port": int(os.getenv('KEEP_ALIVE_PORT', 8080))
        },
        "endpoints": [
            {"path": "/", "description": "Main keep-alive check"},
            {"path": "/health", "description": "Detailed health information"},
            {"path": "/ping", "description": "Simple ping response"},
            {"path": "/stats", "description": "Server statistics"}
        ],
        "developer": "@ISmartCoder"
    })

@app.errorhandler(404)
def not_found(error):
    """Custom 404 handler"""
    return jsonify({
        "error": "Not Found",
        "message": "The requested endpoint does not exist",
        "available_endpoints": ["/", "/health", "/ping", "/stats"],
        "developer": "@ISmartCoder"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 handler"""
    return jsonify({
        "error": "Internal Server Error",
        "message": "Something went wrong on our end",
        "timestamp": datetime.now().isoformat(),
        "developer": "@ISmartCoder"
    }), 500

def run_server():
    """Run the Flask server with error handling"""
    try:
        port = int(os.getenv('KEEP_ALIVE_PORT', 8080))
        host = os.getenv('KEEP_ALIVE_HOST', '0.0.0.0')
        
        # Check if port is available
        if not is_port_available(port):
            print(f"⚠️  Warning: Port {port} is already in use, trying alternative ports...")
            for alt_port in range(port + 1, port + 10):
                if is_port_available(alt_port):
                    port = alt_port
                    print(f"✅ Using alternative port: {port}")
                    break
            else:
                print(f"❌ No available ports found in range {port}-{port+9}")
                return
        
        print(f"🚀 Keep-Alive Server starting...")
        print(f"🌐 Local URL: http://{get_local_ip()}:{port}")
        print(f"🔗 Health Check: http://{get_local_ip()}:{port}/health")
        print(f"📊 Statistics: http://{get_local_ip()}:{port}/stats")
        print(f"👨‍💻 Developer: @ISmartCoder")
        
        app.run(
            host=host,
            port=port,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except Exception as e:
        print(f"❌ Error starting keep-alive server: {str(e)}")
        logging.error(f"Keep-alive server error: {str(e)}")

def keep_alive():
    """Start the keep-alive server in a daemon thread"""
    global server_thread
    
    try:
        # Check if thread is already running
        if server_thread and server_thread.is_alive():
            print("⚠️  Keep-alive server is already running")
            return server_thread
        
        # Create and start daemon thread
        server_thread = Thread(target=run_server, daemon=True, name="KeepAliveServer")
        server_thread.start()
        
        # Give server time to start
        time.sleep(2)
        
        if server_thread.is_alive():
            print("✅ Keep-alive server started successfully")
        else:
            print("❌ Failed to start keep-alive server")
            
        return server_thread
        
    except Exception as e:
        print(f"❌ Error in keep_alive(): {str(e)}")
        logging.error(f"Keep-alive initialization error: {str(e)}")
        return None

def stop_keep_alive():
    """Stop the keep-alive server (graceful shutdown)"""
    global server_thread
    
    if server_thread and server_thread.is_alive():
        print("🛑 Stopping keep-alive server...")
        # Note: Flask development server doesn't support graceful shutdown
        # In production, you would implement proper shutdown mechanisms
        print("⚠️  Note: Manual server termination required")
        return True
    else:
        print("ℹ️  Keep-alive server is not running")
        return False

def get_server_status():
    """Get current server status"""
    global server_thread
    
    if server_thread and server_thread.is_alive():
        uptime = datetime.now() - start_time
        return {
            "running": True,
            "thread_alive": True,
            "uptime": str(uptime).split('.')[0],
            "started_at": start_time.isoformat(),
            "port": int(os.getenv('KEEP_ALIVE_PORT', 8080))
        }
    else:
        return {
            "running": False,
            "thread_alive": False,
            "uptime": "0:00:00",
            "started_at": None,
            "port": None
        }

# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Keep-Alive Server...")
    
    # Start server
    thread = keep_alive()
    
    if thread:
        print("✅ Server started in background")
        print("📋 Server Status:", get_server_status())
        
        # Keep main thread alive for testing
        try:
            while True:
                time.sleep(10)
                status = get_server_status()
                if status["running"]:
                    print(f"✅ Server running - Uptime: {status['uptime']}")
                else:
                    print("❌ Server stopped")
                    break
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            stop_keep_alive()
    else:
        print("❌ Failed to start server")