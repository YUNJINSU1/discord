#!/usr/bin/env python3
"""수정사항 테스트 스크립트"""

import os
import shutil

def move_log_file():
    """bot.log를 logs 폴더로 이동"""
    if os.path.exists("bot.log"):
        os.makedirs("logs", exist_ok=True)
        if os.path.exists("logs/bot.log"):
            # 기존 파일이 있으면 백업
            shutil.move("logs/bot.log", "logs/bot.log.backup")
        shutil.move("bot.log", "logs/bot.log")
        print("✅ bot.log를 logs/bot.log로 이동완료")
    else:
        print("❌ bot.log 파일이 없습니다")

def check_images():
    """이미지 파일 확인"""
    images_dir = "assets/images"
    if os.path.exists(images_dir):
        files = os.listdir(images_dir)
        print(f"📁 이미지 파일 목록: {files}")
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                file_path = os.path.join(images_dir, file)
                size = os.path.getsize(file_path)
                print(f"  📷 {file}: {size} bytes")
    else:
        print("❌ assets/images 폴더가 없습니다")

if __name__ == "__main__":
    print("🔧 수정사항 적용 중...")
    move_log_file()
    check_images()
    print("✅ 완료!")
