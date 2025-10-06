# 경량화된 Python 이미지 - Frontend 제거 버전
FROM python:3.12-slim

WORKDIR /app

# 시스템 의존성 최소 설치
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Python 의존성 복사 및 설치
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 백엔드 소스 복사
COPY backend/ ./

# Flask 템플릿 및 정적 파일 복사
COPY web/ ./web/

# 이미지 저장 디렉토리 생성
RUN mkdir -p assets/images

# 포트 노출
EXPOSE 8080

# 환경 변수 설정
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# 헬스체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# 백엔드 실행
CMD python main.py --mode web --web-port ${PORT}
