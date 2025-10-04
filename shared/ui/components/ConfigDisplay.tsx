import { BotConfig } from '@/types/bot';

interface ConfigDisplayProps {
  config?: BotConfig;
}

export default function ConfigDisplay({ config }: ConfigDisplayProps) {
  if (!config) {
    return (
      <div className="bg-gray-800 p-6 rounded-lg mb-8">
        <h3 className="text-xl font-semibold mb-4">현재 설정</h3>
        <div className="text-gray-400">설정을 불러오는 중...</div>
      </div>
    );
  }

  return (
    <div className="bg-gray-800 p-6 rounded-lg mb-8">
      <h3 className="text-xl font-semibold mb-4">현재 설정</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <p className="text-gray-400">채널 ID:</p>
          <p className="font-mono">{config.channel_id}</p>
        </div>
        <div>
          <p className="text-gray-400">전송 간격:</p>
          <p>{config.send_interval}초 ({Math.floor(config.send_interval / 60)}분)</p>
        </div>
        <div>
          <p className="text-gray-400">이미지 설정:</p>
          <p>
            {config.send_with_image ? (
              config.image_path ? (
                '🖼️ 이미지와 함께 전송'
              ) : (
                '⚠️ 이미지 없음 (설정 필요)'
              )
            ) : (
              '📝 텍스트만 전송'
            )}
          </p>
        </div>
        <div>
          <p className="text-gray-400">메시지 길이:</p>
          <p>{config.message_content.length}자</p>
        </div>
      </div>
    </div>
  );
}
