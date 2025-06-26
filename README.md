# Discord Self-Bot 자동 메시지 전송

Discord 사용자 계정을 이용한 자동 메시지 전송 스크립트입니다.

## ⚠️ 중요한 경고

- **이 스크립트는 Discord의 이용약관에 위반될 수 있습니다.**
- **Self-bot 사용은 계정 정지의 위험이 있습니다.**
- **교육 목적으로만 사용하고, 실제 운영 환경에서는 공식 Bot API를 사용하세요.**
- **사용자 토큰을 절대 공유하지 마세요.**

## 파일 구조

```
discord/
├── main.py           # 메인 스크립트
├── requirements.txt  # 의존성 패키지
├── .env             # 환경 변수 (토큰, 설정)
└── README.md        # 이 파일
```

## 설치 및 실행

### 1. 의존성 설치

```powershell
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 열고 다음 정보를 입력하세요:

- `USER_TOKEN`: Discord 사용자 계정 토큰
- `CHANNEL_ID`: 메시지를 보낼 채널 ID
- `MESSAGE_CONTENT`: 전송할 메시지 내용
- `SEND_INTERVAL`: 전송 간격 (초 단위)

### 3. 사용자 토큰 얻기

1. Discord 웹 버전 접속 (discord.com)
2. F12로 개발자 도구 열기
3. Network 탭 이동
4. 아무 채널에 메시지 입력
5. API 요청에서 Authorization 헤더 값 복사

### 4. 채널 ID 얻기

1. Discord에서 개발자 모드 활성화 (설정 > 고급 > 개발자 모드)
2. 채널 우클릭 > "ID 복사"

### 5. 실행

```powershell
# 테스트 실행 (포그라운드)
python main.py

# 백그라운드 실행 (Windows)
start /B python main.py
```

## 기능

- 지정된 간격으로 자동 메시지 전송
- 오류 처리 및 재연결
- 실시간 로깅
- 수동 제어 명령어:
  - `>stop_auto_message`: 자동 전송 중단
  - `>start_auto_message`: 자동 전송 시작

## 주의사항

1. **Discord 이용약관 준수**: Self-bot은 공식적으로 금지되어 있습니다.
2. **API 제한**: 너무 빈번한 요청은 Rate Limit에 걸릴 수 있습니다.
3. **토큰 보안**: `.env` 파일을 Git에 업로드하지 마세요.
4. **계정 안전**: 메인 계정보다는 테스트 계정 사용을 권장합니다.

## 대안

실제 서비스에서는 다음을 사용하세요:

1. **Discord Bot API**: 공식 봇 토큰 사용
2. **Discord Webhooks**: 간단한 메시지 전송용
3. **Scheduled Tasks**: OS 레벨에서 스케줄링

## 문제 해결

### 로그인 실패
- 토큰이 올바른지 확인
- 계정이 정지되지 않았는지 확인

### 메시지 전송 실패
- 채널 ID가 올바른지 확인
- 해당 채널에 메시지 전송 권한이 있는지 확인

### 봇이 응답하지 않음
- 인터넷 연결 상태 확인
- Discord 서버 상태 확인
