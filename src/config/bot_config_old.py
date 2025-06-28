import os
import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

@dataclass
class BotConfig:
    """봇 설정을 관리하는 데이터 클래스"""
    user_token: str
    channel_id: str
    message_content: str
    send_interval: int = 1800  # 30분
    image_path: Optional[str] = None
    is_enabled: bool = True
    
    @classmethod
    def from_env(cls) -> 'BotConfig':
        """환경 변수에서 설정 로드"""
        load_dotenv()
        
        # 기본 메시지 설정
        default_message = "🤖 자동 메시지입니다. Railway에서 환경 변수를 설정해주세요!"
        
        return cls(
            user_token=os.getenv("USER_TOKEN", ""),
            channel_id=os.getenv("CHANNEL_ID", ""),
            message_content=os.getenv("MESSAGE_CONTENT", default_message),
            send_interval=int(os.getenv("SEND_INTERVAL", "1800")),
            image_path=os.getenv("IMAGE_PATH"),
            is_enabled=os.getenv("IS_ENABLED", "true").lower() == "true"
        )
    
    @classmethod
    def from_file(cls, file_path: str) -> 'BotConfig':
        """JSON 파일에서 설정 로드, 토큰은 환경 변수에서 가져옴"""
        try:
            # 먼저 환경 변수 로드
            load_dotenv()
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 환경 변수에서 토큰 가져오기 (우선순위)
            token_from_env = os.getenv("USER_TOKEN")
            if token_from_env and token_from_env != "YOUR_ACTUAL_DISCORD_TOKEN_HERE":
                data['user_token'] = token_from_env
                logging.info("환경 변수에서 토큰을 로드했습니다")
            elif data.get('user_token') == "***" or not data.get('user_token'):
                logging.error("유효한 토큰이 설정되지 않았습니다. .env 파일의 USER_TOKEN을 확인하세요")
                
            return cls(**data)
        except FileNotFoundError:
            logging.warning(f"설정 파일을 찾을 수 없습니다: {file_path}")
            return cls.from_env()
        except Exception as e:
            logging.error(f"설정 파일 로드 오류: {e}")
            return cls.from_env()
    
    def save_to_file(self, file_path: str) -> None:
        """설정을 JSON 파일로 저장"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                # 토큰은 보안상 저장하지 않음
                data = asdict(self)
                data['user_token'] = "***"
                json.dump(data, f, indent=2, ensure_ascii=False)
            logging.info(f"설정이 저장되었습니다: {file_path}")
        except Exception as e:
            logging.error(f"설정 저장 오류: {e}")
    
    def update(self, **kwargs) -> None:
        """설정 업데이트"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                logging.info(f"설정 업데이트: {key} = {value}")
    
    def validate(self) -> bool:
        """설정 유효성 검사"""
        if not self.user_token:
            logging.error("필수 설정이 없습니다: user_token")
            logging.error("Railway 대시보드에서 USER_TOKEN 환경 변수를 설정해주세요!")
            return False
            
        if not self.channel_id:
            logging.error("필수 설정이 없습니다: channel_id") 
            logging.error("Railway 대시보드에서 CHANNEL_ID 환경 변수를 설정해주세요!")
            return False
            
        if not self.message_content:
            logging.warning("메시지 내용이 없습니다. 기본 메시지를 사용합니다.")
            self.message_content = "🤖 자동 메시지입니다."
            
        return True
