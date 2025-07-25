#!/usr/bin/env python3
"""
WSGI configuration for CraveBreaker Bot production deployment
This file provides the WSGI application object for production servers
"""

import os
from app import app, start_bot_in_thread

# Start the Telegram bot when the WSGI app is loaded
start_bot_in_thread()

# WSGI application object
application = app

if __name__ == "__main__":
    # For direct execution
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    app.run(host=host, port=port, debug=False, threaded=True)