#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CraveBreaker Telegram Bot - Cloud Run Main Entry Point
This is the primary entry point for Cloud Run deployment
"""

import os
import sys

# Ensure the current directory is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point for the CraveBreaker Bot"""
    from app import app, start_bot_in_thread
    
    # Start the Telegram bot in a separate thread
    start_bot_in_thread()
    
    # Start Flask server for health checks
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    
    print(f"🚀 Starting CraveBreaker Bot on {host}:{port}")
    app.run(host=host, port=port, debug=False, threaded=True)

# Import and run the application
if __name__ == "__main__":
    main()