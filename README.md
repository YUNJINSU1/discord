# 🤖 Discord Auto Bot - 모노레포

Discord 자동 메시지 봇과 웹 대시보드가 통합된 모노레포입니다.

## 📁 프로젝트 구조

```
discord-auto-bot/
├── backend/                    # Flask 백엔드 (Python)
│   ├── src/
│   │   ├── bot/               # Discord 봇 로직
│   │   ├── config/            # 설정 관리
│   │   └── web_interface.py   # Flask API 서버
│   ├── requirements.txt
│   └── main.py
├── frontend/                   # Next.js 프론트엔드 (TypeScript)
│   ├── src/
│   │   ├── app/               # Next.js App Router
│   │   ├── components/        # React 컴포넌트
│   │   ├── hooks/             # 커스텀 훅
│   │   └── lib/               # 유틸리티
│   └── package.json
├── shared/                     # 공유 설정 및 에셋
│   ├── assets/
│   └── config.json
├── docker-compose.yml          # 개발/테스트용
├── Dockerfile                 # Railway 프로덕션 배포용
└── README.md
```

## 🚀 빠른 시작

### 1. 저장소 클론 및 설정

```bash
git clone <repository-url>
cd discord-auto-bot

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 Discord 토큰 등을 설정
```

### 2. 개발 모드 (로컬)

**옵션 A: 개별 실행**
```bash
# 터미널 1: Flask 백엔드
cd backend
pip install -r requirements.txt
python main.py --mode web --web-port 5000

# 터미널 2: Next.js 프론트엔드  
cd frontend
npm install
npm run dev
```

**옵션 B: Docker Compose 사용**
```bash
docker-compose up --build
```

### 3. 접속
- **프론트엔드 대시보드**: http://localhost:3000
- **백엔드 API**: http://localhost:5000
- **헬스체크**: http://localhost:5000/health

## 🔧 개발 스크립트

루트 디렉토리에서 사용할 수 있는 편의 스크립트들:

```bash
# 백엔드 개발 서버
npm run dev:backend

# 프론트엔드 개발 서버  
npm run dev:frontend

# 전체 개발 환경
npm run dev

# 빌드
npm run build

# 프로덕션 시작
npm run start
```

## 🌐 배포

### Railway 배포
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 연결
railway link

# 환경 변수 설정
railway variables set USER_TOKEN=your_token
railway variables set CHANNEL_ID=your_channel_id

# 배포
railway up
```

### Docker 배포
```bash
# 프로덕션 빌드
docker build -t discord-bot .

# 실행
docker run -p 8080:8080 \
  -e USER_TOKEN=your_token \
  -e CHANNEL_ID=your_channel_id \
  discord-bot
```

## 🔗 아키텍처

### API 통신
- **Frontend (Next.js)** ↔ **Backend (Flask)**
- RESTful API + JSON
- 실시간 상태 업데이트 (SWR 폴링)

### 주요 API 엔드포인트
- `GET /api/status` - 봇 상태 조회
- `POST /api/bot/start` - 봇 시작
- `POST /api/bot/stop` - 봇 중지
- `POST /api/bot/send_now` - 즉시 메시지 전송
- `GET /api/images` - 이미지 목록
- `POST /api/images/upload` - 이미지 업로드

## ⚙️ 환경 변수

```bash
# Discord Bot (필수)
USER_TOKEN=your_discord_user_token
CHANNEL_ID=your_target_channel_id

# 서버 설정 (선택)
FLASK_PORT=5000
NEXT_PORT=3000

# 웹 인증 (선택)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=password

# 개발 환경 (선택)
NODE_ENV=development
FLASK_ENV=development
```

## 🛠️ 기술 스택

### 백엔드
- **Flask** - 웹 API 서버
- **discord.py** - Discord 봇 라이브러리
- **APScheduler** - 자동 메시지 스케줄링
- **Python 3.12+**

### 프론트엔드
- **Next.js 15** - React 프레임워크
- **TypeScript** - 정적 타입 검사
- **Tailwind CSS** - 스타일링
- **SWR** - 데이터 패칭 및 캐싱
- **Axios** - HTTP 클라이언트

### 인프라
- **Docker** - 컨테이너화
- **Railway** - 클라우드 배포
- **GitHub Actions** - CI/CD (선택)

## 📝 개발 가이드

### 새 기능 추가
1. **백엔드**: `backend/src/web_interface.py`에 API 엔드포인트 추가
2. **프론트엔드**: `frontend/src/lib/api.ts`에 API 함수 추가
3. **UI**: `frontend/src/components/`에 컴포넌트 작성

### 디버깅
```bash
# 백엔드 로그
cd backend && python main.py --mode web --web-port 5000

# 프론트엔드 개발 도구
cd frontend && npm run dev
# → 브라우저에서 F12 개발자 도구 사용
```

---

🎯 **모던 웹 대시보드 + 안정적인 Flask 백엔드**의 조합으로 최적의 성능과 개발 경험을 제공합니다!
