import { BotConfig } from '@/types/bot';
import Image from 'next/image';

interface MessagePreviewProps {
  config?: BotConfig;
}

export default function MessagePreview({ config }: MessagePreviewProps) {
  if (!config) {
    return (
      <div className="bg-gray-800 p-6 rounded-lg">
        <h3 className="text-xl font-semibold mb-4">📱 현재 메시지 미리보기</h3>
        <div className="text-gray-400">설정을 불러오는 중...</div>
      </div>
    );
  }

  return (
    <div className="bg-gray-800 p-6 rounded-lg">
      <h3 className="text-xl font-semibold mb-4">📱 현재 메시지 미리보기</h3>
      <div className="bg-gray-700 p-4 rounded-lg">
        <div className="flex items-start space-x-3">
          <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
            🤖
          </div>
          <div className="flex-1">
            <div className="font-semibold mb-1">Discord Bot</div>
            <div className="whitespace-pre-wrap text-sm">{config.message_content}</div>
            {config.send_with_image && config.image_path && (
              <div className="mt-2">
                <div className="text-sm text-gray-400 mb-1">📷 첨부된 이미지:</div>
                <div className="relative">
                  <Image
                    src={`/api/images/${config.image_path.split('/').pop()}`}
                    alt="봇 이미지"
                    width={300}
                    height={200}
                    className="max-w-xs max-h-48 rounded object-cover"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.style.display = 'none';
                      const errorDiv = target.nextElementSibling as HTMLElement;
                      if (errorDiv) {
                        errorDiv.style.display = 'block';
                      }
                    }}
                  />
                  <div 
                    className="text-sm text-gray-400 hidden"
                    style={{ display: 'none' }}
                  >
                    이미지 로드 실패: {config.image_path}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
