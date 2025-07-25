#!/usr/bin/env python3
"""
Startup script for CraveBreaker Bot Cloud Run deployment
This ensures the application starts correctly in the cloud environment
"""

import os
import sys

# Set environment variables for Cloud Run
os.environ.setdefault('PORT', '5000')
os.environ.setdefault('HOST', '0.0.0.0')

# Import and run the main application
if __name__ == "__main__":
    from app import app, start_bot_in_thread
    
    # Start the Telegram bot in a separate thread
    start_bot_in_thread()
    
    # Start Flask server for health checks
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    
    print(f"Starting CraveBreaker on {host}:{port}")
    app.run(host=host, port=port, debug=False, threaded=True)