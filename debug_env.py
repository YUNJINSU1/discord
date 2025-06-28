#!/usr/bin/env python3
"""
환경변수 디버깅 도구 - Railway 배포 문제 해결용
"""
import os

def check_environment():
    """현재 환경변수 상태를 확인"""
    print("🔍 환경변수 체크:")
    print("=" * 50)
    
    # 필수 환경변수
    required_vars = ['USER_TOKEN', 'DATABASE_URL', 'PORT']
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if var == 'USER_TOKEN':
                print(f"✅ {var}: {'*' * 20} (설정됨)")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: 설정되지 않음")
    
    print()
    print("📋 선택적 환경변수:")
    optional_vars = ['CHANNEL_ID', 'ADMIN_USERNAME', 'ADMIN_PASSWORD']
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            if 'PASSWORD' in var:
                print(f"✅ {var}: {'*' * 10} (설정됨)")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"⚠️ {var}: 설정되지 않음 (웹에서 설정 가능)")
    
    print()
    print("🌐 Railway 환경변수:")
    railway_vars = [k for k in os.environ.keys() if k.startswith('RAILWAY')]
    if railway_vars:
        for var in railway_vars[:3]:  # 처음 3개만 표시
            print(f"ℹ️ {var}: {os.getenv(var)}")
        if len(railway_vars) > 3:
            print(f"   ... 및 {len(railway_vars)-3}개 더")
    else:
        print("ℹ️ Railway 관련 환경변수 없음")
    
    print("=" * 50)

if __name__ == "__main__":
    check_environment()
