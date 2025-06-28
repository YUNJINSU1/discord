# Railway 최적화된 Dockerfile
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY src/ src/
COPY web/ web/
COPY config/ config/
COPY assets/ assets/

# 포트 노출
EXPOSE $PORT

# 환경 변수 설정
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Railway 헬스체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# 애플리케이션 실행 (Railway에서 PORT 환경변수 제공)
CMD ["python", "-m", "src.main"]
