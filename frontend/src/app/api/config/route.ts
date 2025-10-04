import { NextRequest, NextResponse } from 'next/server';

async function proxyToFlaskServer(request: NextRequest, endpoint: string) {
  const flaskUrl = process.env.FLASK_SERVER_URL || 'http://localhost:5000';
  
  try {
    const response = await fetch(`${flaskUrl}${endpoint}`, {
      method: request.method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': request.headers.get('Authorization') || '',
      },
      body: request.body,
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Flask server connection failed:', error);
    
    if (request.method === 'GET') {
      // 모킹 설정 데이터
      const mockConfig = {
        channel_id: "1234567890123456789",
        send_interval: 300,
        message_content: "🚀 Flask 서버에 연결할 수 없습니다.\n\n📅 모킹 데이터입니다.",
        send_with_image: false,
        image_path: null,
        error: 'Flask server not available'
      };
      return NextResponse.json(mockConfig, { status: 503 });
    } else {
      // POST 요청 (설정 업데이트)
      return NextResponse.json({
        success: false,
        message: 'Flask 서버에 연결할 수 없습니다.'
      }, { status: 503 });
    }
  }
}

export async function GET(request: NextRequest) {
  return proxyToFlaskServer(request, '/api/config');
}

export async function POST(request: NextRequest) {
  return proxyToFlaskServer(request, '/api/config');
}
