#!/bin/bash

# AWS ECS 배포 스크립트
# 사용법: ./deploy-aws.sh

set -e

# 설정
CLUSTER_NAME="discord-bot-cluster"
SERVICE_NAME="discord-auto-bot"
TASK_DEFINITION="discord-bot-task"
REGION="ap-northeast-2"  # 서울 리전
IMAGE_URI="your-account-id.dkr.ecr.ap-northeast-2.amazonaws.com/discord-bot:latest"

echo "🚀 Discord Bot을 AWS ECS에 배포합니다..."

# AWS CLI 설정 확인
if ! aws sts get-caller-identity >/dev/null 2>&1; then
    echo "❌ AWS CLI가 설정되지 않았습니다."
    echo "💡 'aws configure' 명령으로 AWS 자격 증명을 설정해주세요."
    exit 1
fi

# ECR에 이미지 푸시
echo "📦 ECR에 이미지 푸시 중..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $IMAGE_URI

docker build -f ../docker/Dockerfile -t discord-bot ..
docker tag discord-bot:latest $IMAGE_URI
docker push $IMAGE_URI

# ECS 클러스터 생성 (없는 경우)
if ! aws ecs describe-clusters --clusters $CLUSTER_NAME --region $REGION >/dev/null 2>&1; then
    echo "🏗️ ECS 클러스터 생성 중..."
    aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $REGION
fi

# 태스크 정의 등록
echo "📋 태스크 정의 등록 중..."
aws ecs register-task-definition \
  --region $REGION \
  --cli-input-json file://deploy/ecs-task-definition.json

# 서비스 업데이트 또는 생성
if aws ecs describe-services --cluster $CLUSTER_NAME --services $SERVICE_NAME --region $REGION >/dev/null 2>&1; then
    echo "🔄 서비스 업데이트 중..."
    aws ecs update-service \
      --cluster $CLUSTER_NAME \
      --service $SERVICE_NAME \
      --task-definition $TASK_DEFINITION \
      --region $REGION
else
    echo "🆕 서비스 생성 중..."
    aws ecs create-service \
      --cluster $CLUSTER_NAME \
      --service-name $SERVICE_NAME \
      --task-definition $TASK_DEFINITION \
      --desired-count 1 \
      --region $REGION
fi

echo "✅ AWS ECS 배포 완료!"
echo "📊 상태 확인: aws ecs describe-services --cluster $CLUSTER_NAME --services $SERVICE_NAME --region $REGION"
