from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
import os
import json
import asyncio
import threading
import logging
from datetime import datetime
from werkzeug.utils import secure_filename
import mimetypes
import ipaddress
from functools import wraps
from flask import Response
from src.config import BotConfig
from src.bot import DiscordAutoBot

# Flask 로깅 필터 설정
class HealthCheckFilter(logging.Filter):
    """헬스체크 요청을 로그에서 제외하는 필터"""
    def filter(self, record):
        # /api/status, /api/logs 요청은 로그에서 제외
        if hasattr(record, 'getMessage'):
            message = record.getMessage()
            if any(endpoint in message for endpoint in ['/api/status', '/api/logs']):
                return False
        return True

# 보안 관련 함수들
def get_client_ip():
    """클라이언트 IP 주소 가져오기 (프록시 고려)"""
    if request.headers.get('X-Forwarded-For'):
        # 프록시를 통한 접근 시 (Google Cloud Load Balancer 등)
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr

def is_ip_allowed(client_ip):
    """IP 화이트리스트 체크"""
    allowed_ips = os.getenv('ALLOWED_IPS', '').split(',')
    
    # 빈 설정이면 모든 IP 허용 (개발 모드)
    if not allowed_ips or allowed_ips == ['']:
        return True
    
    for allowed_ip in allowed_ips:
        allowed_ip = allowed_ip.strip()
        if not allowed_ip:
            continue
            
        try:
            # CIDR 표기법 지원 (예: 192.168.1.0/24)
            if '/' in allowed_ip:
                if ipaddress.ip_address(client_ip) in ipaddress.ip_network(allowed_ip, strict=False):
                    return True
            # 정확한 IP 매치
            elif client_ip == allowed_ip:
                return True
        except ValueError:
            # IP 형식이 잘못된 경우 무시
            continue
    
    return False

def check_basic_auth():
    """Basic Auth 체크"""
    auth = request.authorization
    username = os.getenv('ADMIN_USERNAME', 'admin')
    password = os.getenv('ADMIN_PASSWORD', 'password')
    
    if auth and auth.username == username and auth.password == password:
        return True
    return False

def require_auth(f):
    """인증 데코레이터"""
    @wraps(f)
    def decorated(*args, **kwargs):
        client_ip = get_client_ip()
        
        # 1단계: IP 화이트리스트 체크
        if not is_ip_allowed(client_ip):
            # 보안 로그 기록
            logging.warning(f"❌ 차단된 IP 접근 시도: {client_ip} - {request.endpoint}")
            return Response(
                '🚫 접근이 거부되었습니다.\n허용되지 않은 IP 주소입니다.',
                401,
                {'Content-Type': 'text/plain; charset=utf-8'}
            )
        
        # 2단계: Basic Auth 체크
        if not check_basic_auth():
            # 성공한 IP 로그 (첫 로그인 시에만)
            if 'logged_ips' not in globals():
                globals()['logged_ips'] = set()
            
            if client_ip not in globals()['logged_ips']:
                logging.info(f"✅ 허용된 IP 접근: {client_ip}")
                globals()['logged_ips'].add(client_ip)
            
            return Response(
                '🔐 인증이 필요합니다',
                401,
                {
                    'WWW-Authenticate': 'Basic realm="Discord Bot Admin"',
                    'Content-Type': 'text/plain; charset=utf-8'
                }
            )
        
        # 인증 성공 로그 (세션당 1회)
        auth = request.authorization
        session_key = f"{client_ip}_{auth.username}" if auth else client_ip
        if 'auth_sessions' not in globals():
            globals()['auth_sessions'] = set()
            
        if session_key not in globals()['auth_sessions']:
            username = auth.username if auth else 'unknown'
            logging.info(f"🎉 로그인 성공: {username}@{client_ip}")
            globals()['auth_sessions'].add(session_key)
        
        return f(*args, **kwargs)
    return decorated

class WebInterface:
    """웹 관리 인터페이스"""
    
    def __init__(self, config: BotConfig = None):
        # 현재 파일 위치에서 프로젝트 루트 찾기
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        template_dir = os.path.join(project_root, 'web', 'templates')
        static_dir = os.path.join(project_root, 'web', 'static')
        
        print(f"Templates directory: {template_dir}")  # 디버깅용
        print(f"Templates exist: {os.path.exists(template_dir)}")
        
        self.app = Flask(__name__, 
                        template_folder=template_dir,
                        static_folder=static_dir)
        
        # Flask의 werkzeug 로거에 필터 추가
        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.addFilter(HealthCheckFilter())
        
        # 설정 로드 - 전달받은 config 우선, 없으면 새로 로드
        self.config = config if config else BotConfig.load()
        self.bot = None
        self.bot_thread = None
        
        self._setup_routes()
    
    def _setup_routes(self):
        """라우트 설정"""
        
        @self.app.route('/')
        @require_auth
        def dashboard():
            """대시보드 페이지"""
            status = {
                'is_running': self.bot is not None and self.bot.is_running,
                'is_enabled': self.config.is_enabled,
                'next_send_time': getattr(self.bot, 'next_send_time', None),
                'config': self.config
            }
            return render_template('dashboard.html', **status)
        
        @self.app.route('/config', methods=['GET', 'POST'])
        @require_auth
        def config_page():
            """설정 페이지 - PostgreSQL 기반"""
            if request.method == 'POST':
                # 설정 업데이트
                data = request.form.to_dict()
                
                # 숫자 타입 변환
                if 'send_interval' in data:
                    data['send_interval'] = int(data['send_interval'])
                
                # 체크박스 처리
                data['is_enabled'] = 'is_enabled' in data
                
                # 이미지 경로 처리 - 빈 문자열이면 None으로 설정
                if 'image_path' in data and data['image_path'].strip() == '':
                    data['image_path'] = None
                
                # PostgreSQL에 설정 저장
                success = self.config.update(**data)
                
                if success:
                    logging.info("설정이 데이터베이스에 저장되었습니다.")
                    
                    # 실행 중인 봇에 설정 적용
                    if self.bot and hasattr(self.bot, '_loop') and self.bot._loop:
                        try:
                            future = asyncio.run_coroutine_threadsafe(
                                self.bot.update_config(**data),
                                self.bot._loop
                            )
                            future.result(timeout=5)  # 5초 타임아웃
                        except Exception as e:
                            logging.error(f"봇 설정 업데이트 오류: {e}")
                else:
                    logging.error("설정 저장에 실패했습니다.")
                
                return redirect(url_for('dashboard'))
            
            return render_template('config.html', config=self.config)
        
        @self.app.route('/api/bot/<action>', methods=['POST'])
        @require_auth
        def bot_control(action):
            """봇 제어 API"""
            try:
                if action == 'start':
                    if not self.bot or not self.bot.is_running:
                        self._start_bot()
                    return jsonify({'success': True, 'message': '봇이 시작되었습니다'})
                
                elif action == 'stop':
                    if self.bot:
                        self._stop_bot()
                    return jsonify({'success': True, 'message': '봇이 중지되었습니다'})
                
                elif action == 'send_now':
                    if self.bot:
                        future = asyncio.run_coroutine_threadsafe(
                            self.bot.send_auto_message(),
                            self.bot.loop
                        )
                        success = future.result(timeout=10)
                        message = '메시지가 전송되었습니다' if success else '메시지 전송에 실패했습니다'
                        return jsonify({'success': success, 'message': message})
                    else:
                        return jsonify({'success': False, 'message': '봇이 실행 중이 아닙니다'})
                
                else:
                    return jsonify({'success': False, 'message': '알 수 없는 명령입니다'})
                    
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)})
        
        @self.app.route('/api/status')
        @require_auth
        def bot_status():
            """봇 상태 API"""
            # 봇 실행 상태 정확히 체크
            is_bot_connected = (self.bot is not None and 
                               hasattr(self.bot, 'is_ready') and 
                               self.bot.is_ready() and
                               not self.bot.is_closed())
            
            is_scheduler_running = (self.bot is not None and 
                                  hasattr(self.bot, 'is_running') and 
                                  self.bot.is_running)
            
            next_time = None
            if self.bot and hasattr(self.bot, 'next_send_time') and self.bot.next_send_time:
                # ISO 형식으로 변환
                next_time = self.bot.next_send_time.isoformat()
            
            status = {
                'is_running': is_scheduler_running,
                'is_connected': is_bot_connected,
                'is_enabled': self.config.is_enabled,
                'next_send_time': next_time,
                'current_time': datetime.now().isoformat(),
                'bot_user': str(self.bot.user) if is_bot_connected else None
            }
            return jsonify(status)
        
        @self.app.route('/api/logs')
        @require_auth
        def get_logs():
            """로그 조회 API"""
            try:
                lines = int(request.args.get('lines', 50))  # 기본 50줄
                log_file = "logs/bot.log"
                
                if not os.path.exists(log_file):
                    return jsonify({'logs': [], 'message': '로그 파일이 없습니다'})
                
                with open(log_file, 'r', encoding='utf-8') as f:
                    all_lines = f.readlines()
                    recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
                    
                return jsonify({
                    'logs': [line.strip() for line in recent_lines],
                    'total_lines': len(all_lines),
                    'shown_lines': len(recent_lines)
                })
            except Exception as e:
                return jsonify({'logs': [], 'error': str(e)})
        
        @self.app.route('/api/images')
        @require_auth
        def list_images():
            """이미지 목록 조회 API"""
            try:
                images_dir = "assets/images"
                if not os.path.exists(images_dir):
                    os.makedirs(images_dir, exist_ok=True)
                    return jsonify({'images': []})
                
                image_files = []
                allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
                
                for filename in os.listdir(images_dir):
                    file_path = os.path.join(images_dir, filename)
                    if os.path.isfile(file_path):
                        _, ext = os.path.splitext(filename.lower())
                        if ext in allowed_extensions:
                            file_size = os.path.getsize(file_path)
                            image_files.append({
                                'filename': filename,
                                'size': file_size,
                                'size_mb': round(file_size / 1024 / 1024, 2)
                            })
                
                return jsonify({'images': image_files})
            except Exception as e:
                return jsonify({'images': [], 'error': str(e)})
        
        @self.app.route('/api/images/upload', methods=['POST'])
        @require_auth
        def upload_image():
            """이미지 업로드 API"""
            try:
                if 'file' not in request.files:
                    return jsonify({'success': False, 'message': '파일이 선택되지 않았습니다'})
                
                file = request.files['file']
                if file.filename == '':
                    return jsonify({'success': False, 'message': '파일이 선택되지 않았습니다'})
                
                # 파일 확장자 검사
                allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
                filename = secure_filename(file.filename)
                _, ext = os.path.splitext(filename.lower())
                
                if ext not in allowed_extensions:
                    return jsonify({'success': False, 'message': f'지원하지 않는 파일 형식입니다. 지원 형식: {", ".join(allowed_extensions)}'})
                
                # 파일 크기 검사 (10MB 제한)
                file.seek(0, 2)  # 파일 끝으로 이동
                file_size = file.tell()
                file.seek(0)  # 파일 시작으로 돌아가기
                
                if file_size > 10 * 1024 * 1024:  # 10MB
                    return jsonify({'success': False, 'message': '파일 크기가 10MB를 초과했습니다'})
                
                # 이미지 저장
                images_dir = "assets/images"
                os.makedirs(images_dir, exist_ok=True)
                
                file_path = os.path.join(images_dir, filename)
                
                # 파일명 중복 처리
                counter = 1
                base_name, ext = os.path.splitext(filename)
                while os.path.exists(file_path):
                    filename = f"{base_name}_{counter}{ext}"
                    file_path = os.path.join(images_dir, filename)
                    counter += 1
                
                file.save(file_path)
                
                return jsonify({
                    'success': True, 
                    'message': '이미지가 업로드되었습니다',
                    'filename': filename,
                    'size_mb': round(file_size / 1024 / 1024, 2)
                })
                
            except Exception as e:
                return jsonify({'success': False, 'message': f'업로드 실패: {str(e)}'})
        
        @self.app.route('/api/images/<filename>')
        @require_auth
        def serve_image(filename):
            """이미지 파일 서빙"""
            try:
                # 파일명에서 경로 조작 방지
                filename = secure_filename(filename)
                images_dir = os.path.abspath("assets/images")
                file_path = os.path.join(images_dir, filename)
                
                # 보안: 디렉토리 외부 접근 방지
                if not file_path.startswith(images_dir):
                    return jsonify({'error': '잘못된 파일 경로입니다'}), 400
                
                if not os.path.exists(file_path):
                    return jsonify({'error': '파일을 찾을 수 없습니다'}), 404
                
                # MIME 타입 추론
                mime_type, _ = mimetypes.guess_type(file_path)
                if not mime_type or not mime_type.startswith('image/'):
                    return jsonify({'error': '이미지 파일이 아닙니다'}), 400
                
                return send_file(file_path, mimetype=mime_type)
                
            except Exception as e:
                print(f"이미지 서빙 오류: {e}")  # 디버깅용
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/images/<filename>/delete', methods=['DELETE'])
        @require_auth
        def delete_image(filename):
            """이미지 삭제 API"""
            try:
                images_dir = "assets/images"
                file_path = os.path.join(images_dir, filename)
                
                if not os.path.exists(file_path):
                    return jsonify({'success': False, 'message': '파일을 찾을 수 없습니다'})
                
                os.remove(file_path)
                
                return jsonify({
                    'success': True,
                    'message': '이미지가 삭제되었습니다'
                })
                
            except Exception as e:
                return jsonify({'success': False, 'message': f'삭제 실패: {str(e)}'})
    
    
    def _start_bot(self):
        """봇 시작"""
        if self.bot_thread and self.bot_thread.is_alive():
            return
        
        def run_bot():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                self.bot = DiscordAutoBot(self.config)
                # 봇에 루프 설정
                self.bot._loop = loop
                
                loop.run_until_complete(self.bot.start(self.config.user_token))
            except Exception as e:
                print(f"봇 실행 오류: {e}")
            finally:
                if self.bot:
                    self.bot.is_running = False
                loop.close()
        
        self.bot_thread = threading.Thread(target=run_bot, daemon=True)
        self.bot_thread.start()
    
    def _stop_bot(self):
        """봇 중지"""
        if self.bot:
            try:
                # 스케줄러 먼저 중지
                if hasattr(self.bot, '_loop') and self.bot._loop and not self.bot._loop.is_closed():
                    try:
                        future = asyncio.run_coroutine_threadsafe(
                            self.bot.stop_scheduler(),
                            self.bot._loop
                        )
                        future.result(timeout=5)  # 5초 타임아웃
                    except (asyncio.TimeoutError, RuntimeError):
                        pass  # 타임아웃이나 루프 종료는 무시
                
                # 봇 연결 종료
                if hasattr(self.bot, '_loop') and self.bot._loop and not self.bot._loop.is_closed():
                    try:
                        future = asyncio.run_coroutine_threadsafe(
                            self.bot.close(),
                            self.bot._loop
                        )
                        future.result(timeout=5)  # 5초 타임아웃
                    except (asyncio.TimeoutError, RuntimeError):
                        pass  # 타임아웃이나 루프 종료는 무시
                        
            except Exception as e:
                # 조용히 처리 (로그만 출력하지 않음)
                pass
            finally:
                self.bot = None
    
    def run(self, host='0.0.0.0', port=8080, debug=False):
        """웹 서버 실행"""
        self.app.run(host=host, port=port, debug=debug)
