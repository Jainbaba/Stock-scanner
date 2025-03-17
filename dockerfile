# Dockerfile for combined Stock Scanner application
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies, Node.js and npm
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy and install backend dependencies
COPY stock-scanner-backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt gunicorn

# Copy backend code
COPY stock-scanner-backend/ ./backend/

# Set up frontend
WORKDIR /app/frontend

# Copy frontend code
COPY stock-scanner-frontend/ ./

# Use a compatible npm version
RUN npm install -g npm@10.8.2

# Install specific dependencies that were missing in the error message
RUN npm install tailwindcss postcss autoprefixer --save-dev

# Make sure all dependencies are installed properly
RUN npm install

# Set environment variables
ENV NODE_ENV=production
ENV NEXT_PUBLIC_API_URL=/api

# Build the frontend
RUN npm run build

# Set up nginx configuration
WORKDIR /app
RUN echo 'server { \
    listen 80; \
    \
    location / { \
        proxy_pass http://localhost:3000; \
        proxy_http_version 1.1; \
        proxy_set_header Upgrade $http_upgrade; \
        proxy_set_header Connection "upgrade"; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
        proxy_set_header X-Forwarded-Proto $scheme; \
    } \
    \
    location /api/ { \
        proxy_pass http://localhost:5000/api/; \
        proxy_http_version 1.1; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
        proxy_set_header X-Forwarded-Proto $scheme; \
    } \
    \
    location /health { \
        proxy_pass http://localhost:5000/health; \
    } \
}' > /etc/nginx/sites-available/default

# Create startup script
RUN echo '#!/bin/bash' > /app/start.sh && \
    echo 'set -e' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo '# Start nginx' >> /app/start.sh && \
    echo 'service nginx start' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo '# Start backend in background' >> /app/start.sh && \
    echo 'cd /app/backend && gunicorn --bind 0.0.0.0:5000 app:app &' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo '# Start frontend and wait for it' >> /app/start.sh && \
    echo 'cd /app/frontend && npm start' >> /app/start.sh && \
    chmod +x /app/start.sh

# Environment variables
ENV PORT=8000
ENV FLASK_ENV=production
ENV CORS_ORIGIN=http://localhost

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/health || exit 1

# Start all services
CMD ["/app/start.sh"]