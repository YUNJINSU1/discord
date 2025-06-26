import os
import discord
import asyncio
import logging
import time
from dotenv import load_dotenv

# --- 기본 설정 ---
# 로그 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수 읽기
USER_TOKEN = os.getenv("USER_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
MESSAGE_CONTENT = os.getenv("MESSAGE_CONTENT")
SEND_INTERVAL = int(os.getenv("SEND_INTERVAL", "1800"))  # 기본값: 30분(1800초)

# --- 유효성 검사 ---
if not all([USER_TOKEN, CHANNEL_ID, MESSAGE_CONTENT]):
    logging.critical("오류: 필수 환경 변수(USER_TOKEN, CHANNEL_ID, MESSAGE_CONTENT)가 설정되지 않았습니다.")
    exit(1)

class DiscordSelfBot(discord.Client):
    def __init__(self):
        super().__init__(self_bot=True)
        self.channel_id = int(CHANNEL_ID)
        self.message_content = MESSAGE_CONTENT
        self.send_interval = SEND_INTERVAL
        self.is_running = False

    async def on_ready(self):
        logging.info(f'로그인 성공: {self.user} (ID: {self.user.id})')
        
        # 채널 확인
        channel = self.get_channel(self.channel_id)
        if not channel:
            logging.error(f"채널 ID {self.channel_id}를 찾을 수 없습니다.")
            await self.close()
            return
        
        logging.info(f"메시지를 전송할 채널: #{channel.name} (서버: {channel.guild.name})")
        logging.info(f"메시지 전송 간격: {self.send_interval}초 ({self.send_interval//60}분)")
        
        # 스케줄러 시작
        if not self.is_running:
            self.is_running = True
            asyncio.create_task(self.message_scheduler())

    async def send_message_to_channel(self):
        """지정된 채널에 메시지를 전송하는 함수"""
        try:
            channel = self.get_channel(self.channel_id)
            if not channel:
                logging.error(f"채널 ID {self.channel_id}를 찾을 수 없습니다.")
                return False

            # 메시지 전송
            await channel.send(self.message_content)
            logging.info(f"메시지 전송 성공: #{channel.name}")
            return True

        except discord.HTTPException as e:
            logging.error(f"메시지 전송 실패 (HTTP 오류): {e}")
            return False
        except discord.Forbidden:
            logging.error("메시지 전송 권한이 없습니다.")
            return False
        except Exception as e:
            logging.error(f"예상치 못한 오류 발생: {e}")
            return False

    async def message_scheduler(self):
        """정해진 간격으로 메시지를 전송하는 스케줄러"""
        logging.info("메시지 스케줄러가 시작되었습니다.")
        
        # 시작 시 즉시 1회 실행 (테스트용)
        logging.info("시작 즉시 첫 번째 메시지를 전송합니다.")
        await self.send_message_to_channel()
        
        while self.is_running:
            try:
                # 지정된 간격만큼 대기
                await asyncio.sleep(self.send_interval)
                
                # 메시지 전송
                if self.is_running:  # 종료 신호 확인
                    await self.send_message_to_channel()
                    
            except asyncio.CancelledError:
                logging.info("스케줄러가 중단되었습니다.")
                break
            except Exception as e:
                logging.error(f"스케줄러 오류: {e}")
                await asyncio.sleep(60)  # 오류 발생 시 1분 대기 후 재시도

    async def on_message(self, message):
        """메시지 이벤트 핸들러 (필요시 추가 기능 구현)"""
        # 자신의 메시지만 처리하고 싶은 경우
        if message.author != self.user:
            return
        
        # 특정 명령어 처리 예시 (선택사항)
        if message.content == '>stop_auto_message':
            self.is_running = False
            await message.channel.send("자동 메시지 전송을 중단합니다.")
            logging.info("사용자 명령으로 자동 메시지 전송이 중단되었습니다.")
        
        elif message.content == '>start_auto_message':
            if not self.is_running:
                self.is_running = True
                asyncio.create_task(self.message_scheduler())
                await message.channel.send("자동 메시지 전송을 시작합니다.")
                logging.info("사용자 명령으로 자동 메시지 전송이 시작되었습니다.")

    async def on_error(self, event, *args, **kwargs):
        logging.error(f"Discord 이벤트 오류 발생: {event}")

def main():
    """메인 실행 함수"""
    try:
        client = DiscordSelfBot()
        
        # 봇 실행
        logging.info("Discord 클라이언트를 시작합니다...")
        client.run(USER_TOKEN)
        
    except discord.LoginFailure:
        logging.critical("로그인 실패: 토큰이 유효하지 않습니다.")
    except KeyboardInterrupt:
        logging.info("사용자에 의해 프로그램이 종료되었습니다.")
    except Exception as e:
        logging.critical(f"치명적 오류: {e}")

if __name__ == "__main__":
    main()
