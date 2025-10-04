import { useState } from 'react';
import Link from 'next/link';
import { BotAction } from '@/types/bot';

interface ControlButtonsProps {
  onControlBot: (action: BotAction) => Promise<any>;
  disabled?: boolean;
}

export default function ControlButtons({ onControlBot, disabled = false }: ControlButtonsProps) {
  const [loading, setLoading] = useState<BotAction | null>(null);

  const handleControl = async (action: BotAction) => {
    if (disabled || loading) return;
    
    try {
      setLoading(action);
      const result = await onControlBot(action);
      
      // 성공/실패 메시지 표시
      if (result.success) {
        alert(result.message);
      } else {
        alert(`오류: ${result.message}`);
      }
    } catch (error: any) {
      alert(`오류가 발생했습니다: ${error.message}`);
    } finally {
      setLoading(null);
    }
  };

  const getButtonText = (action: BotAction) => {
    if (loading === action) {
      switch (action) {
        case 'start': return '🔄 시작 중...';
        case 'stop': return '🔄 중지 중...';
        case 'send_now': return '🔄 전송 중...';
      }
    }
    
    switch (action) {
      case 'start': return '🚀 봇 시작';
      case 'stop': return '⏹️ 봇 중지';
      case 'send_now': return '📨 즉시 전송';
    }
  };

  const isDisabled = disabled || loading !== null;

  return (
    <div className="flex flex-wrap gap-4 mb-8 justify-center">
      <button
        onClick={() => handleControl('start')}
        disabled={isDisabled}
        className="bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed px-6 py-3 rounded-lg transition-colors"
      >
        {getButtonText('start')}
      </button>
      
      <button
        onClick={() => handleControl('stop')}
        disabled={isDisabled}
        className="bg-red-600 hover:bg-red-700 disabled:bg-gray-600 disabled:cursor-not-allowed px-6 py-3 rounded-lg transition-colors"
      >
        {getButtonText('stop')}
      </button>
      
      <button
        onClick={() => handleControl('send_now')}
        disabled={isDisabled}
        className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed px-6 py-3 rounded-lg transition-colors"
      >
        {getButtonText('send_now')}
      </button>
      
      <Link
        href="/config"
        className="bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg inline-block transition-colors"
      >
        ⚙️ 설정
      </Link>
    </div>
  );
}
