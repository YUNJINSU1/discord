# Discord Auto Bot

Discord에서 자동으로 메시지와 이미지를 전송하는 봇입니다.

## 🚀 주요 기능

- 📨 자동 메시지 전송 (설정 가능한 간격)
- 🖼️ 이미지와 텍스트 동시 전송
- 🌐 웹 관리 인터페이스
- ⚙️ 실시간 설정 변경
- 🎛️ 봇 제어 (시작/중지/즉시전송)
- ☁️ 클라우드 배포 지원

## 📁 프로젝트 구조

```
discord-bot/
├── src/                    # 소스 코드
│   ├── bot/               # 봇 핵심 로직
│   ├── config/            # 설정 관리
│   ├── web_interface.py   # 웹 인터페이스
│   └── main.py           # 메인 실행 파일
├── web/                   # 웹 관리 인터페이스
│   └── templates/         # HTML 템플릿
├── docker/                # Docker 설정
│   ├── Dockerfile        # 컨테이너 빌드 파일
│   └── .dockerignore     # Docker 무시 파일
├── deploy/                # 클라우드 배포
│   ├── deploy-cloudrun.sh # Google Cloud Run
│   ├── deploy-aws.sh     # AWS ECS
│   ├── cloudbuild.yaml   # Cloud Build 설정
│   └── docker-compose.yml # Docker Compose
├── config/                # 설정 파일들
│   ├── bot_config.json   # 봇 설정
│   └── .env.example      # 환경 변수 예시
├── assets/                # 리소스 파일들
│   └── images/           # 이미지 파일들
├── logs/                  # 로그 파일들
├── .env                   # 환경 변수 (실제 설정)
├── .gitignore            # Git 무시 파일
├── requirements.txt       # Python 의존성
└── README.md             # 이 파일
```

## 🛠️ 설치 및 실행

### 로컬 실행

1. **의존성 설치**
```bash
pip install -r requirements.txt
```

2. **설정 파일 준비**
```bash
cp config/.env.example .env
# .env 파일을 편집하여 토큰 등 설정
```

3. **실행**
```bash
# 통합 모드 (웹 + 봇)
python src/main.py

# 웹 인터페이스만
python src/main.py --mode web

# 봇만
python src/main.py --mode bot
```

### Docker 실행

```bash
# Docker Compose 사용
cd deploy
docker-compose up -d
```

### 클라우드 배포

#### Google Cloud Run
```bash
# 환경 변수 설정
export USER_TOKEN="your_discord_token"
export CHANNEL_ID="your_channel_id"

# 배포
./deploy/deploy-cloudrun.sh your-project-id
```

#### AWS ECS
```bash
./deploy/deploy-aws.sh
```

## 🌐 웹 인터페이스

봇이 실행되면 `http://localhost:8080`에서 웹 관리 인터페이스에 접속할 수 있습니다.

### 주요 기능
- 📊 실시간 대시보드
- ⚙️ 설정 변경 (메시지, 이미지, 간격, 채널)
- 🎛️ 봇 제어 (시작/중지/즉시전송)
- 📱 메시지 미리보기

## 🤖 Discord 명령어

채널에서 다음 명령어를 사용할 수 있습니다:

- `>bot_status` - 봇 상태 확인
- `>bot_stop` - 자동 메시지 중지
- `>bot_start` - 자동 메시지 시작
- `>bot_send_now` - 즉시 메시지 전송

## ⚙️ 설정

### 환경 변수
- `USER_TOKEN` - Discord 사용자 토큰
- `CHANNEL_ID` - 메시지를 보낼 채널 ID
- `SEND_INTERVAL` - 전송 간격 (초)
- `WEB_PORT` - 웹 인터페이스 포트

### 설정 파일
`config/bot_config.json`에서 상세 설정을 관리할 수 있습니다.
