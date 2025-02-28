# gunicorn.conf.py
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '3000')}"
backlog = 2048

# Worker processes
workers = 1  # For most cases 1 worker is enough
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'stock-scanner'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None

# Server hooks
def on_starting(server):
    """Log when server starts."""
    server.log.info("Starting server...")

def on_exit(server):
    """Log when server exits."""
    server.log.info("Shutting down...")