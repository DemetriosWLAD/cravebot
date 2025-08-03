# Gunicorn configuration for production deployment
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
backlog = 2048

# Worker processes - Keep at 1 for Telegram bots to avoid conflicts
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Restart workers after this many requests
max_requests = 1000
max_requests_jitter = 50

# Logging
loglevel = "info"
accesslog = "-"
errorlog = "-"
capture_output = True

# Process naming
proc_name = "cravebreaker-bot"

# Server mechanics
preload_app = True
timeout = 120
graceful_timeout = 30

# Application module
wsgi_module = "wsgi:application"