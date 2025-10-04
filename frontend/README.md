# 🚀 Discord Bot Dashboard (Next.js)

이 프로젝트는 바닐라 JavaScript에서 **Next.js + TypeScript + SWR**로 마이그레이션된 Discord 봇 대시보드입니다.

## ✨ 주요 개선사항

### 🎯 **성능 최적화**
- **95-97% API 호출 감소** (기존 매초 → 30-60초 간격)
- **SWR 자동 캐싱** 및 중복 제거
- **적응형 새로고침** (봇 상태에 따라 간격 조정)
- **페이지 가시성 감지** (백그라운드에서 자동 중지)

### 🛠️ **개발 경험 향상**
- **TypeScript** 완전 지원으로 타입 안전성
- **React Hooks** 기반 상태 관리
- **재사용 가능한 컴포넌트** 구조
- **자동 에러 처리** 및 재시도

### 🎨 **사용자 경험 개선**
- **SSR (Server-Side Rendering)** 지원
- **실시간 카운트다운** (서버 동기화)
- **낙관적 업데이트** (즉시 UI 반영)
- **로딩 상태** 및 에러 핸들링

## 🚀 실행 방법

### 1. 의존성 설치
```bash
cd discord-bot-dashboard
npm install
```

### 2. 환경 변수 설정
`.env.local` 파일에서 Flask 서버 URL 설정:
```env
FLASK_SERVER_URL=http://localhost:5000
NEXT_PUBLIC_API_URL=http://localhost:3000
```

### 3. 개발 서버 실행
```bash
npm run dev
```

🌐 **브라우저에서 [http://localhost:3000](http://localhost:3000) 접속**
