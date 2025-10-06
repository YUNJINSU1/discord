# 🤖 Discord 자동 메시지 봇 - Railway 배포 가이드

> **코딩 몰라도 OK!** 이 가이드를 따라하면 누구나 Discord 봇을 만들 수 있습니다!

[![Railway 배포](https://railway.app/button.svg)](https://railway.app/template/your-template)

## 🎯 이 프로젝트로 할 수 있는 것

- ⏰ **자동 메시지 전송**: 설정한 시간마다 Discord 채널에 메시지 자동 전송
- 🖼️ **이미지 첨부**: 메시지와 함께 사진도 보낼 수 있어요
- 🌐 **웹 관리**: 인터넷 브라우저로 봇 설정하고 상태 확인 가능
- 📱 **실시간 모니터링**: 언제 메시지가 전송되는지 실시간으로 확인
- 🔒 **보안**: 비밀번호로 보호된 관리자 페이지

## 📋 준비물 (꼭 있어야 해요!)

### 1. Discord 계정
- [Discord 앱 다운로드](https://discord.com/download) (없으시면 설치하세요)

### 2. GitHub 계정
- [GitHub 가입](https://github.com) (코드 저장소, 무료예요)

### 3. Railway 계정
- [Railway 가입](https://railway.app) (배포 플랫폼, 무료 플랜 있어요)

---

## 🚀 5단계로 끝나는 배포 가이드

### 단계 1: Discord 봇 만들기 (10분 소요)

#### 1-1. Discord 개발자 포털 접속
1. 인터넷 브라우저에서 [https://discord.com/developers/applications](https://discord.com/developers/applications) 열기
2. **"New Application"** 버튼 클릭
3. 봇 이름 입력 (예: "내 자동 메시지 봇")
4. **"Create"** 버튼 클릭

#### 1-2. 봇 토큰 발급받기
1. 왼쪽 메뉴에서 **"Bot"** 클릭
2. **"Reset Token"** 버튼 클릭
3. **"Yes, do it"** 확인
4. **토큰 복사** (노란색 박스 안의 텍스트) - **중요: 이 토큰은 절대 다른 사람에게 보여주지 마세요!**
5. 아래 설정들을 모두 **ON**으로 변경:
   - ✅ **PRESENCE INTENT**
   - ✅ **SERVER MEMBERS INTENT**
   - ✅ **MESSAGE CONTENT INTENT**

#### 1-3. 봇을 서버에 초대하기
1. 왼쪽 메뉴에서 **"OAuth2"** → **"URL Generator"** 클릭
2. **SCOPES**에서 **"bot"** 체크
3. **BOT PERMISSIONS**에서 다음 권한들 체크:
   - ✅ **Send Messages** (메시지 전송)
   - ✅ **Attach Files** (파일/이미지 첨부)
   - ✅ **Read Message History** (메시지 기록 읽기)
   - ✅ **Use External Emojis** (외부 이모지 사용, 선택사항)
4. 아래에 생성된 **URL 복사**
5. 새 탭에서 그 URL 열기
6. 초대할 서버 선택 후 **"승인"** 클릭

#### 1-4. Discord 개발자 모드 켜기
1. Discord 앱 열기
2. 왼쪽 하단 **⚙️ 톱니바퀴(설정)** 아이콘 클릭
3. 왼쪽 메뉴에서 **"앱 설정"** → **"고급"** 클릭
4. **"개발자 모드"** 스위치를 **ON**으로 변경
5. 설정 창 닫기

#### 1-5. 채널 ID 확인하기
1. Discord에서 메시지를 보낼 채널 우클릭
2. **"ID 복사"** 클릭
3. 이 ID를 메모장에 저장해두세요 (예: `1191577280095461388`)

---

### 단계 2: 코드 GitHub에 올리기 (5분 소요)

#### 2-1. GitHub에 새 저장소 만들기
1. [GitHub.com](https://github.com) 접속
2. 우측 상단 **"+" 버튼** → **"New repository"** 클릭
3. **Repository name** 입력 (예: `discord-auto-bot`)
4. **"Create repository"** 버튼 클릭
5. **HTTPS URL 복사** (예: `https://github.com/yourname/discord-auto-bot.git`)

#### 2-2. 코드 업로드 (코딩 몰라도 OK!)

**방법 1: GitHub 웹에서 직접 업로드 (추천!)**
1. 이 프로젝트 폴더를 **ZIP 파일로 압축**
2. 방금 만든 GitHub 저장소 페이지로 이동
3. **"uploading an existing file"** 링크 클릭
4. ZIP 파일을 드래그 앤 드롭
5. 아래 **"Commit changes"** 버튼 클릭

**방법 2: GitHub Desktop 사용**
1. [GitHub Desktop 다운로드](https://desktop.github.com/)
2. 설치 후 GitHub 계정으로 로그인
3. **File → Add Local Repository** 클릭
4. 프로젝트 폴더 선택
5. **Publish repository** 버튼 클릭

**방법 3: Git 명령어 사용 (개발자용)**
```bash
git clone https://github.com/YOUR_USERNAME/discord-auto-bot.git
cd discord-auto-bot
# 프로젝트 파일들을 이 폴더에 복사
git add .
git commit -m "Initial commit"
git push origin main
```

---

### 단계 3: Railway에 배포하기 (10분 소요)

#### 3-1. Railway 프로젝트 생성
1. [Railway.app](https://railway.app) 접속 및 로그인
2. **"New Project"** 버튼 클릭
3. **"Deploy from GitHub repo"** 선택
4. **"Configure GitHub App"** 버튼 클릭 (GitHub 연동)
5. **"Authorize Railway"** 허용
6. 방금 만든 **discord-auto-bot** 저장소 선택
7. **"Deploy"** 버튼 클릭

#### 3-2. 환경 변수 설정 (중요! 꼭 모두 입력하세요)
1. Railway 대시보드에서 프로젝트 클릭
2. **"Variables"** 탭 클릭
3. **"New Variable"** 버튼을 눌러서 아래 **6개 변수를 모두** 추가:

| 변수 이름 | 값 예시 | 설명 |
|-----------|----|------|
| `USER_TOKEN` | `ODc0NzUxMz...` | Discord 봇 토큰 (1단계에서 복사한 것) ⚠️ 필수 |
| `CHANNEL_ID` | `1191577280095461388` | 메시지 보낼 채널 ID (1단계에서 복사한 것) ⚠️ 필수 |
| `ADMIN_USERNAME` | `admin` | 관리자 아이디 |
| `ADMIN_PASSWORD` | `mysecret123!` | 관리자 비밀번호 (강력한 걸로 바꾸세요!) |
| `SEND_INTERVAL` | `1800` | 메시지 전송 간격 (초 단위, 1800 = 30분) |
| `MESSAGE_CONTENT` | `🚀 자동 메시지!` | 전송할 메시지 내용 |

4. 모든 변수 입력 후 자동 저장됨

#### 3-3. 배포 완료 대기
1. **"Deployments"** 탭 클릭
2. 빌드가 완료될 때까지 기다리기 (약 5-10분)
3. **"Active"** 상태가 되면 성공!
4. 상단에 **생성된 URL** 복사 (예: `https://discord-bot.up.railway.app`)

---

### 단계 4: 관리자 페이지 접속 및 확인 (5분 소요)

#### 4-1. 배포 URL 확인
1. Railway 대시보드에서 **"Settings"** 탭 클릭
2. **"Domains"** 섹션에서 **"Generate Domain"** 버튼 클릭
3. 생성된 URL 복사 (예: `https://discord-bot-production.up.railway.app`)

#### 4-2. 관리자 페이지 접속
1. 복사한 URL을 브라우저에서 열기
2. 로그인 화면에서:
   - **아이디**: 3단계에서 설정한 `ADMIN_USERNAME`
   - **비밀번호**: 3단계에서 설정한 `ADMIN_PASSWORD`
3. **"로그인"** 버튼 클릭

#### 4-3. 봇 자동 시작 확인
1. 대시보드 메인 화면에서 봇 상태 확인
2. **"🟢 실행 중"** 상태인지 확인
3. **다음 전송 시간**이 표시되는지 확인
4. Discord 채널로 가서 설정한 시간 후 메시지가 오는지 확인!

> 💡 **참고**: Railway에서 환경 변수에 `CHANNEL_ID`와 `MESSAGE_CONTENT`를 설정했기 때문에 봇이 자동으로 시작됩니다!

#### 4-4. 설정 변경 (필요시)
1. 우측 상단 **"⚙️ 설정"** 버튼 클릭
2. 다음 정보들을 변경할 수 있습니다:
   - **채널 ID**: 다른 채널로 변경
   - **전송 간격**: 시간 조정 (초 단위)
   - **메시지 내용**: 내용 수정
   - **자동 전송 활성화**: 켜기/끄기
3. **"💾 설정 저장"** 버튼 클릭

---

### 단계 5: 이미지 추가하기 (선택사항)

#### 5-1. 설정 페이지에서 이미지 업로드
1. **"⚙️ 설정"** 페이지로 이동
2. 아래 **"🖼️ 이미지 관리"** 섹션에서
3. **"📤 업로드"** 버튼 클릭
4. 이미지 파일 선택 (JPG, PNG, GIF, WEBP 지원, 최대 10MB)
5. **업로드 완료** 메시지 확인

#### 5-2. 이미지 미리보기
1. 설정 페이지에서 현재 이미지가 보이는지 확인
2. 대시보드 메인에서도 메시지 미리보기에 이미지가 표시되는지 확인

---

## 🎉 배포 완료! 이제 뭐 할 수 있나요?

### ✅ 기본 기능 사용하기
- **실시간 모니터링**: 언제 다음 메시지가 전송되는지 확인
- **즉시 전송**: "📨 즉시 전송" 버튼으로 바로 메시지 보내기
- **설정 변경**: 전송 간격, 메시지 내용 등 실시간으로 수정
- **봇 제어**: 시작/중지 버튼으로 봇 켜고 끄기

### ✅ 고급 기능
- **로그 확인**: 시스템 로그로 봇 상태 확인
- **이미지 관리**: 메시지에 사진 첨부
- **자동 재시작**: Railway가 알아서 서버 재시작 해줌

---

## 🔧 문제 해결 가이드

### Q: "Railway에서 배포가 실패해요"
**해결**:
1. Railway **"Deployments"** → **"View Logs"** 클릭해서 오류 확인
2. 모든 환경 변수가 설정되어 있는지 확인 (특히 `USER_TOKEN`, `CHANNEL_ID`)
3. GitHub 저장소에 모든 파일이 올라갔는지 확인

### Q: "봇이 시작되지 않아요"
**해결**:
1. Railway **Variables**에서 `USER_TOKEN`이 올바른지 확인
2. Discord Developer Portal에서 토큰이 만료되지 않았는지 확인
3. 봇의 **INTENT** 권한들이 모두 켜져 있는지 확인

### Q: "메시지가 안 보내져요"
**해결**:
1. `CHANNEL_ID`가 올바른지 확인 (Discord에서 다시 복사)
2. 봇이 해당 서버에 초대되어 있는지 확인
3. 봇에게 **"Send Messages"**와 **"Attach Files"** 권한이 있는지 확인
4. 채널이 비공개 채널인 경우, 봇을 채널에 추가했는지 확인

### Q: "로그인할 수 없어요"
**해결**: Railway Variables에서 `ADMIN_USERNAME`과 `ADMIN_PASSWORD` 확인

### Q: "이미지가 안 보여요"
**해결**: 이미지 파일이 10MB 이하이고 지원되는 형식인지 확인

---

## 💰 비용은 얼마나 들까요?

### 무료 플랜 (Trial)
- **월 $5 무료 크레딧** 제공
- **최소 사양으로 충분**: 이 봇은 약 100MB 메모리만 사용
- **예상 비용**: 월 $3-5 정도 (무료 크레딧으로 충당 가능)
- **시간 제한 없음**: 24시간 계속 실행

> 💡 **팁**: Railway는 사용한 만큼만 과금됩니다. 이 봇은 리소스를 적게 사용하도록 최적화되어 있어 무료 크레딧 안에서 충분히 사용 가능합니다!

### 유료 플랜 (필요시)
- **Hobby**: 월 $5 (추가 크레딧)
- **Pro**: 월 $20 (더 많은 리소스)

### 💡 절약 팁
1. 메시지 전송 간격을 길게 설정 (예: 1시간)
2. 이미지 크기를 1MB 이하로 최적화
3. 불필요할 때는 봇 중지하기

---

## 📞 도움이 필요하세요?

### 📧 문의 방법
1. **GitHub Issues**: 버그 신고나 질문
2. **Discord**: [지원 서버 링크] (준비중)

### 🆘 긴급 상황
- Railway 대시보드 → "Deployments" → 로그 확인
- 봇 토큰이 만료되지 않았는지 확인
- 인터넷 연결 상태 확인

---

## 🎊 성공 사례들

- ✅ **카페 홍보 봇**: 1시간마다 메뉴 안내 메시지 전송
- ✅ **스터디 리마인더**: 30분마다 공부 시간 알림
- ✅ **서버 공지 봇**: 중요한 공지사항 자동 전송
- ✅ **이벤트 알림 봇**: 이벤트 시작 1시간 전 알림

---

## 🚀 다음 단계 (고급 사용자용)

### 커스터마이징
- 메시지 내용 변경
- 전송 시간 조정
- 여러 채널에 동시에 전송
- 웹훅 연동

### 모니터링
- Railway 메트릭스로 성능 확인
- 로그 분석으로 문제 해결
- 자동 알림 설정

---

**🎉 축하합니다! 이제 당신만의 Discord 자동 메시지 봇이 완성되었습니다!**

질문 있으시면 언제든 물어보세요 😊

---

*Made with ❤️ for Discord community*</content>
<parameter name="filePath">c:\Users\yunjinsu\discord\README.md