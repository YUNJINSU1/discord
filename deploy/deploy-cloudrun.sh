#!/bin/bash

# Google Cloud Run 배포 스크립트
# 사용법: ./deploy-cloudrun.sh [PROJECT_ID]

set -e

# 설정
PROJECT_ID=${1:-"your-project-id"}
SERVICE_NAME="discord-auto-bot"
REGION="asia-northeast3"  # 서울 리전
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Discord Bot을 Google Cloud Run에 배포합니다..."
echo "📋 프로젝트: $PROJECT_ID"
echo "🌍 리전: $REGION"
echo "🏷️ 이미지: $IMAGE_NAME"

# 환경 변수 확인
if [ -z "$USER_TOKEN" ]; then
    echo "❌ ERROR: USER_TOKEN 환경 변수가 설정되지 않았습니다."
    echo "💡 사용법: USER_TOKEN=your_token ./deploy-cloudrun.sh"
    exit 1
fi

# Google Cloud 프로젝트 설정
echo "⚙️ Google Cloud 프로젝트 설정 중..."
gcloud config set project $PROJECT_ID

# Docker 이미지 빌드 및 푸시
echo "📦 Docker 이미지 빌드 중..."
gcloud builds submit --config=deploy/cloudbuild.yaml --substitutions=_IMAGE_NAME=$IMAGE_NAME .

# Cloud Run에 배포
echo "☁️ Cloud Run에 배포 중..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --concurrency 1 \
  --max-instances 1 \
  --min-instances 0 \
  --timeout 3600 \
  --set-env-vars "USER_TOKEN=$USER_TOKEN" \
  --set-env-vars "CHANNEL_ID=${CHANNEL_ID:-1191577280095461388}" \
  --set-env-vars "SEND_INTERVAL=${SEND_INTERVAL:-1800}" \
  --set-env-vars "WEB_PORT=8080"

# 서비스 URL 가져오기
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')

echo "✅ 배포 완료!"
echo "🌐 웹 인터페이스: $SERVICE_URL"
echo "📊 대시보드: $SERVICE_URL/"
echo "⚙️ 설정: $SERVICE_URL/config"

# 로그 확인 방법 안내
echo ""
echo "📝 로그 확인:"
echo "   gcloud logs tail $SERVICE_NAME --region=$REGION"
