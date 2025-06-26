# 멀티스테이지 빌드로 최적화된 Dockerfile
FROM python:3.12-slim as builder

# 의존성 설치 (빌드 단계)
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 런타임 스테이지
FROM python:3.12-slim

# 사용자 생성 (보안)
RUN useradd --create-home --shell /bin/bash bot

# Python 패키지 복사
COPY --from=builder /root/.local /home/bot/.local
ENV PATH=/home/bot/.local/bin:$PATH

# 작업 디렉토리 설정
WORKDIR /app

# 소스 코드 복사
COPY src/ src/
COPY web/ web/
COPY config/ config/
COPY assets/ assets/

# 권한 설정
RUN chown -R bot:bot /app
USER bot

# 포트 노출 (웹 인터페이스용)
EXPOSE 8080

# 헬스체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/api/status || exit 1

# 애플리케이션 실행
CMD ["python", "-m", "src.main"]
