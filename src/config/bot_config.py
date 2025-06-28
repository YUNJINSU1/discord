import os
import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

# PostgreSQL 설정 관리 시스템 import (실패시 fallback)
try:
    from .database import get_db_manager
    USE_DATABASE = True
except ImportError:
    USE_DATABASE = False
    logging.warning("PostgreSQL 의존성이 없습니다. 환경변수 방식을 사용합니다.")

@dataclass
class BotConfig:
    """봇 설정을 관리하는 데이터 클래스 - PostgreSQL 기반"""
    user_token: str
    channel_id: str
    message_content: str
    send_interval: int = 1800  # 30분
    image_path: Optional[str] = None
    is_enabled: bool = True
    admin_username: str = "admin"
    admin_password: str = "admin123"
    web_port: int = 8080
    
    @classmethod
    def load(cls) -> 'BotConfig':
        """설정 로드 - PostgreSQL 우선, 실패시 환경변수"""
        if USE_DATABASE:
            return cls.from_database()
        else:
            return cls.from_env()
    
    @classmethod
    def from_database(cls) -> 'BotConfig':
        """PostgreSQL 데이터베이스에서 설정 로드"""
        try:
            db = get_db_manager()
            if not db.database_url:
                logging.warning("DATABASE_URL이 없습니다. 환경변수 방식으로 fallback")
                return cls.from_env()
            
            return cls(
                user_token=db.get_setting('user_token', ''),
                channel_id=db.get_setting('channel_id', ''),
                message_content=db.get_setting('message_content', '🤖 PostgreSQL 관리 메시지'),
                send_interval=db.get_setting('send_interval', 1800),
                is_enabled=db.get_setting('is_enabled', True),
                admin_username=db.get_setting('admin_username', 'admin'),
                admin_password=db.get_setting('admin_password', 'admin123'),
                web_port=db.get_setting('web_port', 8080),
                image_path=db.get_setting('image_path', None)
            )
        except Exception as e:
            logging.error(f"데이터베이스 설정 로드 실패: {e}")
            return cls.from_env()
    
    @classmethod
    def from_env(cls) -> 'BotConfig':
        """환경 변수에서 설정 로드 (fallback)"""
        load_dotenv()
        
        return cls(
            user_token=os.getenv("USER_TOKEN", ""),
            channel_id=os.getenv("CHANNEL_ID", ""),
            message_content=os.getenv("MESSAGE_CONTENT", "🤖 환경변수 기반 메시지입니다!"),
            send_interval=int(os.getenv("SEND_INTERVAL", "1800")),
            image_path=os.getenv("IMAGE_PATH"),
            is_enabled=os.getenv("IS_ENABLED", "true").lower() == "true",
            admin_username=os.getenv("ADMIN_USERNAME", "admin"),
            admin_password=os.getenv("ADMIN_PASSWORD", "admin123"),
            web_port=int(os.getenv("PORT", "8080"))
        )
    
    def save(self) -> bool:
        """설정을 데이터베이스에 저장"""
        if not USE_DATABASE:
            logging.warning("PostgreSQL을 사용할 수 없습니다. 설정 저장 실패")
            return False
            
        try:
            db = get_db_manager()
            success = True
            
            # 모든 설정값을 데이터베이스에 저장
            settings = {
                'user_token': self.user_token,
                'channel_id': self.channel_id,
                'message_content': self.message_content,
                'send_interval': self.send_interval,
                'is_enabled': self.is_enabled,
                'admin_username': self.admin_username,
                'admin_password': self.admin_password,
                'web_port': self.web_port,
                'image_path': self.image_path
            }
            
            for key, value in settings.items():
                if value is not None:  # None 값은 저장하지 않음
                    if not db.set_setting(key, value):
                        success = False
            
            return success
        except Exception as e:
            logging.error(f"설정 저장 오류: {e}")
            return False
    
    def update(self, **kwargs) -> bool:
        """설정 업데이트 및 데이터베이스 동기화"""
        updated = False
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                logging.info(f"설정 업데이트: {key} = {value}")
                updated = True
        
        if updated:
            return self.save()
        return True
    
    def validate(self) -> bool:
        """설정 유효성 검사"""
        if not self.user_token or self.user_token == "":
            logging.error("필수 설정이 없습니다: user_token")
            logging.error("Railway 대시보드에서 USER_TOKEN 환경 변수를 설정해주세요!")
            return False
            
        if not self.channel_id or self.channel_id == "":
            logging.error("필수 설정이 없습니다: channel_id") 
            logging.error("Railway 대시보드에서 CHANNEL_ID 환경 변수를 설정해주세요!")
            return False
                
        # 토큰 기본값 체크
        if self.user_token in ["YOUR_DISCORD_BOT_TOKEN_HERE", "***"]:
            logging.error("유효한 Discord 토큰이 설정되지 않았습니다.")
            return False
            
        if not self.message_content:
            logging.warning("메시지 내용이 없습니다. 기본 메시지를 사용합니다.")
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

    # Backward compatibility methods
    @classmethod
    def from_env_legacy(cls) -> 'BotConfig':
        """레거시 호환성을 위한 메서드"""
        return cls.from_env()
        
    @classmethod
    def from_file(cls, file_path: str) -> 'BotConfig':
        """레거시 호환성: 파일에서 로드 (실제로는 새 시스템 사용)"""
        logging.warning("from_file은 더 이상 사용되지 않습니다. load() 메서드를 사용하세요.")
        return cls.load()
        
    def save_to_file(self, file_path: str) -> None:
        """레거시 호환성: 파일 저장 (실제로는 DB 저장)"""
        logging.warning("save_to_file은 더 이상 사용되지 않습니다. save() 메서드를 사용하세요.")
        self.save()
