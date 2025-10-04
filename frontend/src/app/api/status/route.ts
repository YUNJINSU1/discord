import { NextRequest, NextResponse } from 'next/server';

// 기존 Flask 서버로 프록시하는 함수
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
    
    // 모킹 데이터 (Flask 서버가 없을 때만 사용)
    const mockStatus = {
      is_running: false,
      is_connected: false,
      is_enabled: true,
      next_send_time: null,
      current_time: new Date().toISOString(),
      error: 'Flask server not available'
    };
    
    return NextResponse.json(mockStatus, { status: 503 });
  }
}

export async function GET(request: NextRequest) {
  return proxyToFlaskServer(request, '/api/status');
}
