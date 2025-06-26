import os
import discord
import asyncio
import logging
from typing import Optional
from datetime import datetime, timedelta

from src.config import BotConfig

# 로그 설정
def setup_logging():
    """로그 설정"""
    # logs 디렉토리 생성
    os.makedirs("logs", exist_ok=True)
    
    # 로거 설정
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 기존 핸들러 제거
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 파일 핸들러 (logs/bot.log)
    file_handler = logging.FileHandler("logs/bot.log", encoding="utf-8")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

# 로그 설정 초기화
setup_logging()

class DiscordAutoBot(discord.Client):
    """Discord 자동 메시지 봇"""
    
    def __init__(self, config: BotConfig, loop=None):
        # discord.py-self에서는 loop 매개변수가 중복될 수 있으므로 제거
        super().__init__(self_bot=True)
        self.config = config
        self.is_running = False
        self.scheduler_task: Optional[asyncio.Task] = None
        self.next_send_time: Optional[datetime] = None
        self._loop = loop or asyncio.get_event_loop()
        
    async def on_ready(self):
        """봇이 준비되었을 때 실행"""
        logging.info(f'✅ 로그인 성공: {self.user} (ID: {self.user.id})')
        logging.info(f'📅 계정 생성일: {self.user.created_at}')
        
        # 채널 확인
        channel = self.get_channel(int(self.config.channel_id))
        if not channel:
            logging.error(f"❌ 채널 ID {self.config.channel_id}를 찾을 수 없습니다.")
            await self.close()
            return
        
        logging.info(f"📨 전송 채널: #{channel.name} (서버: {channel.guild.name})")
        logging.info(f"⏰ 전송 간격: {self.config.send_interval}초 ({self.config.send_interval//60}분)")
        logging.info(f"🎛️ 봇 상태: {'활성화' if self.config.is_enabled else '비활성화'}")
        
        # 자동 전송 시작
        if self.config.is_enabled:
            await self.start_scheduler()
    
    async def start_scheduler(self):
        """스케줄러 시작"""
        if self.is_running:
            return
            
        self.is_running = True
        logging.info("🚀 메시지 스케줄러 시작")
        
        # 첫 메시지 즉시 전송
        await self.send_auto_message()
        
        # 스케줄러 태스크 시작
        self.scheduler_task = asyncio.create_task(self._scheduler_loop())
    
    async def stop_scheduler(self):
        """스케줄러 중지"""
        self.is_running = False
        if self.scheduler_task:
            self.scheduler_task.cancel()
            try:
                await self.scheduler_task
            except asyncio.CancelledError:
                pass
        logging.info("⏸️ 메시지 스케줄러 중지")
    
    async def _scheduler_loop(self):
        """스케줄러 메인 루프"""
        while self.is_running:
            try:
                # 다음 전송 시간 계산
                self.next_send_time = datetime.now() + timedelta(seconds=self.config.send_interval)
                logging.info(f"⏰ 다음 전송 시간: {self.next_send_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # 대기
                await asyncio.sleep(self.config.send_interval)
                
                # 메시지 전송
                if self.is_running and self.config.is_enabled:
                    await self.send_auto_message()
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"❌ 스케줄러 오류: {e}")
                await asyncio.sleep(60)  # 오류 시 1분 대기
    
    async def send_auto_message(self) -> bool:
        """자동 메시지 전송"""
        try:
            channel = self.get_channel(int(self.config.channel_id))
            if not channel:
                logging.error(f"❌ 채널을 찾을 수 없습니다: {self.config.channel_id}")
                return False
            
            # 이미지 파일 확인
            file_to_send = None
            if self.config.image_path and os.path.exists(self.config.image_path):
                file_to_send = discord.File(self.config.image_path)
                logging.info(f"🖼️ 이미지 준비: {self.config.image_path}")
            elif self.config.image_path:
                logging.warning(f"⚠️ 이미지 파일 없음: {self.config.image_path}")
            
            # 메시지 전송
            if file_to_send:
                await channel.send(content=self.config.message_content, file=file_to_send)
                logging.info(f"📨 메시지+이미지 전송 완료: #{channel.name}")
            else:
                await channel.send(self.config.message_content)
                logging.info(f"📨 메시지 전송 완료: #{channel.name}")
            
            return True
            
        except discord.HTTPException as e:
            logging.error(f"❌ HTTP 오류: {e}")
            return False
        except discord.Forbidden:
            logging.error("❌ 권한 없음: 메시지 전송 권한이 필요합니다")
            return False
        except Exception as e:
            logging.error(f"❌ 전송 오류: {e}")
            return False
    
    async def update_config(self, **kwargs):
        """설정 업데이트"""
        old_enabled = self.config.is_enabled
        self.config.update(**kwargs)
        
        # 활성화 상태 변경 처리
        if 'is_enabled' in kwargs:
            if self.config.is_enabled and not old_enabled:
                await self.start_scheduler()
            elif not self.config.is_enabled and old_enabled:
                await self.stop_scheduler()
        
        # 전송 간격 변경 시 스케줄러 재시작
        if 'send_interval' in kwargs and self.is_running:
            await self.stop_scheduler()
            await self.start_scheduler()
    
    async def on_message(self, message):
        """메시지 이벤트 핸들러"""
        if message.author != self.user:
            return
        
        # 봇 제어 명령어
        if message.content == '>bot_status':
            status = "🟢 활성화" if self.config.is_enabled else "🔴 비활성화"
            next_time = self.next_send_time.strftime('%H:%M:%S') if self.next_send_time else "없음"
            await message.channel.send(f"**봇 상태**: {status}\n**다음 전송**: {next_time}")
        
        elif message.content == '>bot_stop':
            await self.update_config(is_enabled=False)
            await message.channel.send("🔴 자동 메시지 비활성화")
        
        elif message.content == '>bot_start':
            await self.update_config(is_enabled=True)
            await message.channel.send("🟢 자동 메시지 활성화")
        
        elif message.content == '>bot_send_now':
            success = await self.send_auto_message()
            emoji = "✅" if success else "❌"
            await message.channel.send(f"{emoji} 즉시 전송 {'완료' if success else '실패'}")
    
    async def on_error(self, event, *args, **kwargs):
        """오류 이벤트 핸들러"""
        logging.error(f"❌ Discord 이벤트 오류: {event}", exc_info=True)
