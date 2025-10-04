import { NextRequest, NextResponse } from 'next/server';

async function proxyToFlaskServer(request: NextRequest, endpoint: string) {
  const flaskUrl = process.env.FLASK_SERVER_URL || 'http://localhost:5000';
  
  try {
    const response = await fetch(`${flaskUrl}${endpoint}`, {
      method: request.method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: request.body,
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.log('Flask server not available, using mock response:', error);
    
    // 모킹 응답
    return NextResponse.json({
      success: true,
      message: '봇 제어가 실행되었습니다! (모킹 모드)'
    });
  }
}

export async function POST(
  request: NextRequest,
  { params }: { params: { action: string } }
) {
  const { action } = params;
  return proxyToFlaskServer(request, `/api/bot/${action}`);
}
