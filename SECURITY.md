# 🔐 Discord Bot 보안 설정 가이드

## 📋 필수 환경변수

### Discord Bot 설정
```bash
USER_TOKEN=your_discord_bot_token_here
CHANNEL_ID=your_discord_channel_id
MESSAGE_CONTENT="your_message_content"
SEND_INTERVAL=1800
IMAGE_PATH=assets/images/sell.png
```

### 🛡️ 보안 설정
```bash
# 관리자 계정 (Basic Auth)
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_strong_password

# IP 화이트리스트 (쉼표로 구분)
ALLOWED_IPS=your_home_ip,your_office_ip,your_mobile_ip
```

## 🌐 IP 화이트리스트 설정 방법

### 1. 현재 IP 확인
```bash
# 현재 공인 IP 확인
curl ifconfig.me
# 또는
curl ipinfo.io/ip
```

### 2. IP 설정 예시
```bash
# 단일 IP
ALLOWED_IPS=123.456.789.012

# 여러 IP (쉼표로 구분)
ALLOWED_IPS=123.456.789.012,987.654.321.098

# CIDR 표기법 (네트워크 범위)
ALLOWED_IPS=192.168.1.0/24,10.0.0.0/8

# 혼합 사용
ALLOWED_IPS=123.456.789.012,192.168.1.0/24,::1
```

### 3. Google Cloud 배포 시 설정
```bash
# Google Cloud Console에서 환경변수 설정
gcloud run services update discord-bot \
  --set-env-vars ADMIN_USERNAME=admin \
  --set-env-vars ADMIN_PASSWORD=your_secure_password \
  --set-env-vars ALLOWED_IPS=your_ip_list
```

## 🔒 보안 레벨

### 📊 보안 강도
- **Level 1**: IP 화이트리스트만 (`ALLOWED_IPS` 설정)
- **Level 2**: Basic Auth만 (`ADMIN_USERNAME`, `ADMIN_PASSWORD` 설정)  
- **Level 3**: IP + Basic Auth (추천 🌟)

### 🚨 보안 로그
```
✅ 허용된 IP 접근: 123.456.789.012
🎉 로그인 성공: admin@123.456.789.012
❌ 차단된 IP 접근 시도: 999.888.777.666 - /
```

## 🛠️ 운영 팁

### 동적 IP 대응
```bash
# 동적 IP 사용 시 넓은 범위 설정
ALLOWED_IPS=123.456.0.0/16

# 또는 DDNS 사용
# your-domain.ddns.net의 IP를 주기적으로 확인
```

### 모바일 접근
```bash
# 모바일 핫스팟 IP도 추가
ALLOWED_IPS=home_ip,office_ip,mobile_hotspot_ip
```

### 비상 접근
```bash
# Google Cloud Console SSH 접속으로 관리
gcloud compute ssh your-instance
# 환경변수 직접 수정 가능
```

## ⚠️ 주의사항

1. **패스워드 강도**: 최소 12자, 대소문자+숫자+특수문자
2. **IP 확인**: 클라우드 환경에서는 Load Balancer IP가 다를 수 있음
3. **로그 모니터링**: 의심스러운 접근 시도 확인
4. **백업 접근**: SSH나 Cloud Console로 응급 관리

## 🌍 클라우드 환경별 설정

### Google Cloud Run
```yaml
# deploy/cloudrun.yaml
env:
  - name: ADMIN_USERNAME
    value: "admin"
  - name: ADMIN_PASSWORD
    valueFrom:
      secretKeyRef:
        name: bot-password
        key: password
  - name: ALLOWED_IPS
    value: "your,ip,list"
```

### Docker Compose
```yaml
# docker-compose.yml
environment:
  - ADMIN_USERNAME=admin
  - ADMIN_PASSWORD=your_password
  - ALLOWED_IPS=your,ip,list
```

이제 보안이 완전히 설정되었습니다! 🎉
