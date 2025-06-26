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
    parser.add_argument('--config', default='config/bot_config.json',
                      help='설정 파일 경로')
    parser.add_argument('--web-port', type=int, default=8080,
                      help='웹 인터페이스 포트')
    parser.add_argument('--debug', action='store_true',
                      help='디버그 모드')
    
    args = parser.parse_args()
    
    # 로깅 설정
    setup_logging(logging.DEBUG if args.debug else logging.INFO)
    logger = logging.getLogger(__name__)
    
    # 설정 파일 로드
    config = BotConfig.from_file(args.config)
    if not config.validate():
        logger.error("설정이 유효하지 않습니다. 설정을 확인해주세요.")
        return 1
    
    try:
        if args.mode == 'web':
            # 웹 인터페이스만 실행
            logger.info("웹 인터페이스 모드로 시작합니다")
            web = WebInterface(args.config)
            web.run(port=args.web_port, debug=args.debug)
        
        elif args.mode == 'bot':
            # 봇만 실행
            logger.info("봇 전용 모드로 시작합니다")
            bot = DiscordAutoBot(config)
            bot.run(config.user_token)
        
        else:  # both
            # 웹 인터페이스 + 봇 (기본값)
            logger.info("통합 모드로 시작합니다 (웹 + 봇)")
            web = WebInterface(args.config)
            web.run(port=args.web_port, debug=args.debug)
    
    except KeyboardInterrupt:
        logger.info("사용자에 의해 프로그램이 종료되었습니다")
        return 0
    except Exception as e:
        logger.error(f"오류가 발생했습니다: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
