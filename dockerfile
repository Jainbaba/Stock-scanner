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

# Copy frontend code
COPY stock-scanner-frontend/ ./frontend/

# Install frontend dependencies and build
WORKDIR /app/frontend
ENV NODE_ENV=production
ENV NEXT_PUBLIC_API_URL=/api
RUN npm install
RUN npm run build

# Set up nginx configuration
WORKDIR /app
RUN echo ' \
server { \
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
} \
' > /etc/nginx/sites-available/default

# Create startup script
RUN echo '#!/bin/bash \
set -e \
\
# Start nginx \
service nginx start \
\
# Start backend in background \
cd /app/backend && gunicorn --bind 0.0.0.0:5000 app:app & \
\
# Start frontend and wait for it \
cd /app/frontend && npm start \
' > /app/start.sh && chmod +x /app/start.sh

# Environment variables
ENV PORT=80
ENV FLASK_ENV=production
ENV MONGODB_URI=mongodb+srv://jainbaba:svQK5gZah6fCF7pW@stock-scanner.usflx.mongodb.net/?retryWrites=true&w=majority&appName=stock-scanner
ENV CORS_ORIGIN=http://localhost

# Expose port
EXPOSE 80

# Start all services
CMD ["/app/start.sh"]