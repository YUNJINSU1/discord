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

# 포트 기본값 (Railway에서 자동으로 덮어씀)
ENV PORT=8080

# 헬스체크 - Railway가 시작 시간을 더 주도록 수정
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# 백엔드 실행 - Railway의 startCommand가 이것을 덮어씀
CMD ["python", "main.py", "--mode", "both", "--web-port", "8080"]
