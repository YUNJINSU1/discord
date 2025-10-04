# Multi-stage build for optimized image
FROM node:18-alpine AS frontend-builder

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./frontend/
COPY discord-bot-dashboard/package*.json ./discord-bot-dashboard/

# Install dependencies
RUN cd frontend && npm ci --only=production && cd ../discord-bot-dashboard && npm ci --only=production

# Copy source and build
COPY frontend/ ./frontend/
COPY discord-bot-dashboard/ ./discord-bot-dashboard/
COPY shared/ ./shared/

RUN cd frontend && npm run build && cd ../discord-bot-dashboard && npm run build

# Python backend stage
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies minimally
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./

# Copy built frontend assets
COPY --from=frontend-builder /app/frontend/out ./frontend/out
COPY --from=frontend-builder /app/discord-bot-dashboard/out ./discord-bot-dashboard/out

# Copy shared assets
COPY shared/ ./shared/

# Create necessary directories
RUN mkdir -p shared/assets/images

# Expose port
EXPOSE 8080

# Set environment
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# Start backend (which can serve frontend static files)
CMD python main.py --mode web --web-port ${PORT}
COPY shared/ ./shared/

# shared assets 디렉토리 생성
RUN mkdir -p shared/assets/images

# 포트 노출 (Railway 동적 할당)
EXPOSE 8080

# 환경 변수 설정
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# 헬스체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# 백엔드 실행 (Railway PORT 환경변수 사용)
CMD python main.py --mode web --web-port ${PORT}
