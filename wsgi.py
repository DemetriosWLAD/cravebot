#!/usr/bin/env python3
"""
WSGI entry point for production deployment
Compatible with Gunicorn and other WSGI servers
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from main import app, start_bot_in_thread

# Start the Telegram bot when the WSGI application loads
start_bot_in_thread()

# WSGI callable
application = app

if __name__ == "__main__":
    application.run()