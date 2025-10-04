import { BotStatus } from '@/types/bot';
import { useCountdown } from '@/hooks/useBotStatus';

interface StatusCardsProps {
  status?: BotStatus;
  isLoading: boolean;
}

export default function StatusCards({ status, isLoading }: StatusCardsProps) {
  const countdown = useCountdown(
    status?.next_send_time,
    status?.current_time
  );

  const getBotStatusDisplay = () => {
    if (isLoading) return { text: '🔄 확인 중...', color: 'text-blue-400' };
    if (!status) return { text: '❌ 연결 실패', color: 'text-red-400' };
    
    if (status.is_connected && status.is_running) {
      return { text: '🟢 실행 중', color: 'text-green-400' };
    } else if (status.is_connected) {
      return { text: '🟡 연결됨', color: 'text-yellow-400' };
    } else {
      return { text: '🔴 중지됨', color: 'text-red-400' };
    }
  };

  const getAutoStatusDisplay = () => {
    if (!status) return { text: '❌ 알 수 없음', color: 'text-red-400' };
    
    return status.is_enabled 
      ? { text: '✅ 활성화', color: 'text-green-400' }
      : { text: '❌ 비활성화', color: 'text-red-400' };
  };

  const getNextSendDisplay = () => {
    if (!status || !status.is_running || !status.is_enabled) {
      return { text: '없음', color: 'text-gray-400' };
    }

    if (!countdown) {
      return { text: '계산 중...', color: 'text-blue-400' };
    }

    if (countdown.totalSeconds === 0) {
      return { text: '곧 전송', color: 'text-green-400' };
    }

    const timeText = countdown.hours > 0 
      ? `${countdown.hours}시간 ${countdown.minutes}분 ${countdown.seconds}초 후`
      : `${countdown.minutes}분 ${countdown.seconds}초 후`;

    return { text: timeText, color: 'text-blue-400' };
  };

  const botStatus = getBotStatusDisplay();
  const autoStatus = getAutoStatusDisplay();
  const nextSend = getNextSendDisplay();

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div className="bg-gray-800 p-6 rounded-lg">
        <h3 className="text-lg font-semibold mb-2">봇 상태</h3>
        <p className={`text-2xl ${botStatus.color}`}>
          {botStatus.text}
        </p>
      </div>
      
      <div className="bg-gray-800 p-6 rounded-lg">
        <h3 className="text-lg font-semibold mb-2">자동 전송</h3>
        <p className={`text-2xl ${autoStatus.color}`}>
          {autoStatus.text}
        </p>
      </div>
      
      <div className="bg-gray-800 p-6 rounded-lg">
        <h3 className="text-lg font-semibold mb-2">다음 전송</h3>
        <p className={`text-xl ${nextSend.color}`}>
          {nextSend.text}
        </p>
      </div>
    </div>
  );
}
