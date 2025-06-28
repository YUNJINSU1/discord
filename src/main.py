#!/usr/bin/env python3
"""
Discord Auto Bot - 메인 실행 파일
"""

import os
import sys
import logging
import argparse
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import BotConfig
from src.bot import DiscordAutoBot
from src.web_interface import WebInterface

def setup_logging(level=logging.INFO):
    """로깅 설정"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('bot.log', encoding='utf-8')
        ]
    )

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='Discord Auto Bot')
    parser.add_argument('--mode', choices=['bot', 'web', 'both'], default='both',
                      help='실행 모드 선택')
    parser.add_argument('--web-port', type=int, default=8080,
                      help='웹 인터페이스 포트')
    parser.add_argument('--debug', action='store_true',
                      help='디버그 모드')
    
    args = parser.parse_args()
    
    # 로깅 설정
    setup_logging(logging.DEBUG if args.debug else logging.INFO)
    logger = logging.getLogger(__name__)
    
    # 환경변수 체크
    logger.info("환경 변수를 확인하는 중...")
    user_token = os.getenv("USER_TOKEN")
    database_url = os.getenv("DATABASE_URL")
    
    if not user_token:
        logger.error("❌ USER_TOKEN 환경변수가 설정되지 않았습니다!")
        logger.error("🔧 Railway 대시보드에서 다음 환경변수를 설정해주세요:")
        logger.error("   USER_TOKEN=your_discord_bot_token")
        logger.error("   (선택) DATABASE_URL=postgresql://... (PostgreSQL 서비스 추가시 자동생성)")
        logger.info("60초 후 재시도합니다...")
        import time
        time.sleep(60)
        return main()  # 재귀 호출로 재시도
    
    if database_url:
        logger.info("✅ DATABASE_URL이 설정되어 있습니다. PostgreSQL 모드로 동작합니다.")
    else:
        logger.warning("⚠️ DATABASE_URL이 없습니다. 환경변수 모드로 동작합니다.")
    
    # 설정 로드 - PostgreSQL 우선, 실패시 환경변수
    logger.info("설정을 로드하는 중...")
    config = BotConfig.load()
    
    # 설정 검증 - 모드에 따라 다르게 처리
    if args.mode == 'bot':
        # 봇 전용 모드: 반드시 유효한 설정 필요
        if not config.validate():
            logger.error("❌ 봇 실행을 위한 설정이 유효하지 않습니다!")
            logger.info("60초 후 재시도합니다...")
            import time
            time.sleep(60)
            return main()  # 재귀 호출로 재시도
    elif args.mode == 'web':
        # 웹 전용 모드: 설정 없어도 실행 (웹에서 설정 가능)
        logger.info("웹 전용 모드: 설정이 없어도 웹 인터페이스를 시작합니다")
    else:  # both
        # 통합 모드: 웹은 항상 시작, 봇은 설정이 있을 때만
        if not config.validate():
            logger.warning("⚠️ Discord 봇 설정이 불완전하지만 웹 인터페이스는 시작합니다")
            logger.info("웹 인터페이스에서 설정을 완료할 수 있습니다: /config")
    
    # 실행 모드별 처리
    
    try:
        if args.mode == 'web':
            # 웹 인터페이스만 실행
            logger.info("웹 인터페이스 모드로 시작합니다")
            web = WebInterface(config)
            web.run(port=args.web_port, debug=args.debug)
        
        elif args.mode == 'bot':
            # 봇만 실행  
            if config.validate():
                logger.info("봇 전용 모드로 시작합니다")
                bot = DiscordAutoBot(config)
                bot.run(config.user_token)
            else:
                logger.error("봇 설정이 유효하지 않아 시작할 수 없습니다")
                return
        
        else:  # both
            # 웹 인터페이스 + 봇 (기본값)
            logger.info("통합 모드로 시작합니다 (웹 + 봇)")
            web = WebInterface(config)
            web.run(port=args.web_port, debug=args.debug)
    
    except KeyboardInterrupt:
        logger.info("사용자에 의해 프로그램이 종료되었습니다")
        return 0
    except Exception as e:
        logger.error(f"오류가 발생했습니다: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
