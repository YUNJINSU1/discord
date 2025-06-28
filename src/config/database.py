"""
PostgreSQL 기반 설정 관리 시스템
"""
import os
import logging
from typing import Dict, Any, Optional
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class BotSettings(Base):
    """봇 설정 테이블"""
    __tablename__ = 'bot_settings'
    
    key = Column(String(50), primary_key=True)
    value = Column(Text)
    value_type = Column(String(20))  # str, int, bool
    description = Column(String(200))
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class DatabaseManager:
    """데이터베이스 연결 및 설정 관리"""
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            # Railway PostgreSQL은 보통 DATABASE_URL로 제공됨
            logging.error("DATABASE_URL 환경변수가 설정되지 않았습니다!")
            return
        
        logging.info(f"DATABASE_URL 환경변수가 설정되어 있습니다.")
            
        # SQLAlchemy 엔진 생성
        try:
            self.engine = create_engine(self.database_url)
            self.SessionLocal = sessionmaker(bind=self.engine)
            
            # 테이블 생성
            self.init_database()
            
            # 기본 설정 값들 초기화
            self.init_default_settings()
            
            logging.info("PostgreSQL 데이터베이스 연결 성공!")
        except Exception as e:
            logging.error(f"데이터베이스 연결 실패: {e}")
            self.database_url = None  # 연결 실패시 None으로 설정
    
    def init_database(self):
        """데이터베이스 및 테이블 초기화"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logging.info("데이터베이스 테이블이 생성되었습니다.")
        except Exception as e:
            logging.error(f"데이터베이스 초기화 오류: {e}")
    
    def init_default_settings(self):
        """기본 설정값들 초기화 - 보안에 민감하지 않은 설정만 DB에 저장"""
        default_settings = {
            # 사용자 설정 (DB 관리)
            'channel_id': {
                'value': os.getenv('CHANNEL_ID', '1191577280095461388'),
                'type': 'str', 
                'description': '메시지를 보낼 채널 ID'
            },
            'message_content': {
                'value': os.getenv('MESSAGE_CONTENT', '🚀 PostgreSQL로 관리되는 Discord 봇 메시지입니다!'),
                'type': 'str',
                'description': '전송할 메시지 내용'
            },
            'send_interval': {
                'value': os.getenv('SEND_INTERVAL', '1800'),
                'type': 'int',
                'description': '메시지 전송 간격 (초)'
            },
            'is_enabled': {
                'value': os.getenv('IS_ENABLED', 'true'),
                'type': 'bool',
                'description': '봇 활성화 여부'
            },
            'image_path': {
                'value': os.getenv('IMAGE_PATH', 'assets/images/sell.png'),
                'type': 'str',
                'description': '첨부할 이미지 파일 경로'
            },
            'web_port': {
                'value': os.getenv('PORT', '8080'),
                'type': 'int',
                'description': '웹 인터페이스 포트'
            }
            # 보안 민감 정보는 환경변수로만 관리:
            # USER_TOKEN, ADMIN_USERNAME, ADMIN_PASSWORD
        }
        
        with self.SessionLocal() as session:
            for key, config in default_settings.items():
                existing = session.query(BotSettings).filter_by(key=key).first()
                if not existing:
                    setting = BotSettings(
                        key=key,
                        value=config['value'],
                        value_type=config['type'],
                        description=config['description']
                    )
                    session.add(setting)
            session.commit()
            logging.info("기본 설정값들이 데이터베이스에 저장되었습니다.")
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """설정값 가져오기"""
        try:
            with self.SessionLocal() as session:
                setting = session.query(BotSettings).filter_by(key=key).first()
                if setting:
                    # 타입에 따라 변환
                    if setting.value_type == 'int':
                        return int(setting.value)
                    elif setting.value_type == 'bool':
                        return setting.value.lower() == 'true'
                    else:
                        return setting.value
                return default
        except Exception as e:
            logging.error(f"설정 조회 오류 ({key}): {e}")
            return default
    
    def set_setting(self, key: str, value: Any, description: str = None) -> bool:
        """설정값 저장/업데이트"""
        try:
            with self.SessionLocal() as session:
                setting = session.query(BotSettings).filter_by(key=key).first()
                
                # 타입 자동 감지
                if isinstance(value, bool):
                    value_type = 'bool'
                    value_str = str(value).lower()
                elif isinstance(value, int):
                    value_type = 'int'
                    value_str = str(value)
                else:
                    value_type = 'str'
                    value_str = str(value)
                
                if setting:
                    # 기존 설정 업데이트
                    setting.value = value_str
                    setting.value_type = value_type
                    if description:
                        setting.description = description
                    setting.updated_at = datetime.now()
                else:
                    # 새 설정 생성
                    setting = BotSettings(
                        key=key,
                        value=value_str,
                        value_type=value_type,
                        description=description or f'{key} 설정'
                    )
                    session.add(setting)
                
                session.commit()
                logging.info(f"설정 저장됨: {key} = {value}")
                return True
        except Exception as e:
            logging.error(f"설정 저장 오류 ({key}): {e}")
            return False
    
    def get_all_settings(self) -> Dict[str, Any]:
        """모든 설정값 가져오기"""
        settings = {}
        try:
            with self.SessionLocal() as session:
                all_settings = session.query(BotSettings).all()
                for setting in all_settings:
                    if setting.value_type == 'int':
                        settings[setting.key] = int(setting.value)
                    elif setting.value_type == 'bool':
                        settings[setting.key] = setting.value.lower() == 'true'
                    else:
                        settings[setting.key] = setting.value
        except Exception as e:
            logging.error(f"전체 설정 조회 오류: {e}")
        
        return settings
    
    def delete_setting(self, key: str) -> bool:
        """설정값 삭제"""
        try:
            with self.SessionLocal() as session:
                setting = session.query(BotSettings).filter_by(key=key).first()
                if setting:
                    session.delete(setting)
                    session.commit()
                    logging.info(f"설정 삭제됨: {key}")
                    return True
                return False
        except Exception as e:
            logging.error(f"설정 삭제 오류 ({key}): {e}")
            return False

# 전역 데이터베이스 매니저 인스턴스
db_manager = None

def get_db_manager() -> DatabaseManager:
    """데이터베이스 매니저 싱글톤 인스턴스 반환"""
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager()
    return db_manager
