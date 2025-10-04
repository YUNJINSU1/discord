'use client';

import { useBotStatus } from '../../../shared/ui/hooks/useBotStatus';
import StatusCards from '../../../shared/ui/components/StatusCards';
import ControlButtons from '../../../shared/ui/components/ControlButtons';
import ConfigDisplay from '../../../shared/ui/components/ConfigDisplay';
import MessagePreview from '../../../shared/ui/components/MessagePreview';
import LogViewer from '../../../shared/ui/components/LogViewer';
import useSWR from 'swr';
import { BotConfig } from '../../../shared/ui/types/bot';
import { botApi } from '../../../shared/ui/lib/api';

export default function Dashboard() {
  const { status, isLoading, controlBot } = useBotStatus();
  
  // 봇 설정 조회
  const { data: config } = useSWR<BotConfig>(
    'config',
    () => botApi.getConfig(),
    {
      revalidateOnFocus: false,
      refreshInterval: 0, // 설정은 수동으로만 새로고침
    }
  );

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto p-6">
        <h1 className="text-3xl font-bold mb-8 text-center">🤖 Discord Auto Bot</h1>
        
        {/* 상태 카드 */}
        <StatusCards status={status} isLoading={isLoading} />
        
        {/* 제어 버튼 */}
        <ControlButtons onControlBot={controlBot} disabled={isLoading} />
        
        {/* 현재 설정 */}
        <ConfigDisplay config={config} />
        
        {/* 메시지 미리보기 */}
        <MessagePreview config={config} />
        
        {/* 로그 뷰어 */}
        <LogViewer />
      </div>
    </div>
  );
}
