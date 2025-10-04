import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

@dataclass
class BotConfig:
    """봇 설정을 관리하는 데이터 클래스 - 경량화된 JSON 파일 기반"""
    user_token: str
    channel_id: str
    message_content: str
    send_interval: int = 1800  # 30분
    image_path: Optional[str] = None
    send_with_image: bool = True  # 이미지와 함께 보내기 여부
    is_enabled: bool = True
    admin_username: str = "admin"
    admin_password: str = "admin123"
    web_port: int = 8080
    
    @classmethod
    def load(cls) -> 'BotConfig':
        """설정 로드 - 환경변수 우선, JSON 파일 보조"""
        return cls.from_env()
    
    @classmethod
    def from_env(cls) -> 'BotConfig':
        """환경 변수에서 설정 로드"""
        load_dotenv()
        
        # JSON 파일에서 사용자 설정 로드 시도
        config_path = "config.json"
        saved_config = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
            except:
                pass
        
        # 기본 안내 메시지
        default_message = """
🤖 Discord 자동 메시지 봇이 실행 중입니다!

✅ 경량화된 버전으로 동작합니다
⚙️ 웹 인터페이스에서 모든 설정을 변경할 수 있습니다
🔧 환경변수 설정이 필요합니다:

1. USER_TOKEN = Discord 사용자 토큰
2. CHANNEL_ID = 메시지를 보낼 채널 ID

웹 관리 페이지에서 설정을 변경하세요!
        """.strip()
        
        return cls(
            user_token=os.getenv("USER_TOKEN", ""),
            channel_id=saved_config.get("channel_id", os.getenv("CHANNEL_ID", "")),
            message_content=saved_config.get("message_content", os.getenv("MESSAGE_CONTENT", default_message)),
            send_interval=saved_config.get("send_interval", int(os.getenv("SEND_INTERVAL", "1800"))),
            image_path=saved_config.get("image_path", os.getenv("IMAGE_PATH")),
            send_with_image=saved_config.get("send_with_image", True),
            is_enabled=saved_config.get("is_enabled", os.getenv("IS_ENABLED", "true").lower() == "true"),
            admin_username=os.getenv("ADMIN_USERNAME", "admin"),
            admin_password=os.getenv("ADMIN_PASSWORD", "admin123"),
            web_port=int(os.getenv("PORT", "8080"))
        )
    
    def save(self) -> bool:
        """사용자 설정을 JSON 파일에 저장 (보안 정보 제외)"""
        try:
            # 보안 정보를 제외한 사용자 설정만 저장
            user_settings = {
                'channel_id': self.channel_id,
                'message_content': self.message_content,
                'send_interval': self.send_interval,
                'is_enabled': self.is_enabled,
                'image_path': self.image_path,
                'send_with_image': self.send_with_image,
                'web_port': self.web_port
            }
            
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(user_settings, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"설정 저장 오류: {e}")
            return False
    
    def update(self, **kwargs) -> bool:
        """설정 업데이트 및 파일 동기화"""
        updated = False
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                updated = True
        
        if updated:
            return self.save()
        return True
    
    def validate(self) -> bool:
        """설정 유효성 검사"""
        missing_settings = []
        
        if not self.user_token or self.user_token == "":
            missing_settings.append("USER_TOKEN (Discord 사용자 토큰)")
            
        if not self.channel_id or self.channel_id == "":
            missing_settings.append("CHANNEL_ID (메시지를 보낼 채널 ID)")
                
        # 토큰 기본값 체크
        if self.user_token in ["YOUR_DISCORD_BOT_TOKEN_HERE", "***"]:
            missing_settings.append("USER_TOKEN (유효한 Discord 토큰)")
        
        if missing_settings:
            print("🚨 필수 환경변수가 설정되지 않았습니다:")
            for setting in missing_settings:
                print(f"   ❌ {setting}")
            print("")
            print("📋 설정 가이드:")
            print("1. 환경변수 설정:")
            print("   USER_TOKEN=your_discord_user_token")
            print("   CHANNEL_ID=your_channel_id")
            print("2. 또는 웹 인터페이스에서 설정하세요")
            return False
            
        if not self.message_content:
            print("메시지 내용이 없습니다. 기본 메시지를 사용합니다.")
            self.message_content = "🤖 자동 메시지입니다."
            
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """설정을 딕셔너리로 변환 (민감 정보 제외)"""
        data = asdict(self)
        # 보안상 민감한 정보는 마스킹
        if data.get('user_token'):
            data['user_token'] = '***'
        if data.get('admin_password'):
            data['admin_password'] = '***'
        return data
