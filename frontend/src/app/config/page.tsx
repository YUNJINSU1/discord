'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import useSWR from 'swr';
import { BotConfig } from '@/types/bot';
import { botApi } from '@/lib/api';

export default function ConfigPage() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const { data: config, mutate } = useSWR<BotConfig>(
    'config',
    () => botApi.getConfig()
  );

  const [formData, setFormData] = useState<Partial<BotConfig>>({});

  // 설정이 로드되면 폼 데이터 초기화
  useEffect(() => {
    if (config) {
      setFormData(config);
    }
  }, [config]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseInt(value) || 0 : value
    }));
  };

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, checked } = e.target;
    
    setFormData(prev => ({
      ...prev,
      [name]: checked
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (isSubmitting) return;
    
    try {
      setIsSubmitting(true);
      const result = await botApi.updateConfig(formData);
      
      if (result.success) {
        alert('설정이 저장되었습니다!');
        mutate(); // 설정 데이터 새로고침
        router.push('/'); // 대시보드로 이동
      } else {
        alert(`설정 저장 실패: ${result.message}`);
      }
    } catch (error: any) {
      alert(`오류가 발생했습니다: ${error.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!config) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-xl">설정을 불러오는 중...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto p-6 max-w-2xl">
        <div className="flex items-center mb-8">
          <button
            onClick={() => router.push('/')}
            className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded-lg mr-4"
          >
            ← 대시보드로
          </button>
          <h1 className="text-3xl font-bold">⚙️ 봇 설정</h1>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* 디스코드 설정 */}
          <div className="bg-gray-800 p-6 rounded-lg">
            <h2 className="text-xl font-semibold mb-4">디스코드 설정</h2>
            
            <div className="space-y-4">
              <div>
                <label htmlFor="channel_id" className="block text-sm font-medium text-gray-300 mb-2">
                  채널 ID
                </label>
                <input
                  type="text"
                  id="channel_id"
                  name="channel_id"
                  value={formData.channel_id || ''}
                  onChange={handleInputChange}
                  className="w-full bg-gray-700 text-white px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="예: 1234567890123456789"
                  required
                />
              </div>
            </div>
          </div>

          {/* 전송 설정 */}
          <div className="bg-gray-800 p-6 rounded-lg">
            <h2 className="text-xl font-semibold mb-4">전송 설정</h2>
            
            <div className="space-y-4">
              <div>
                <label htmlFor="send_interval" className="block text-sm font-medium text-gray-300 mb-2">
                  전송 간격 (초)
                </label>
                <input
                  type="number"
                  id="send_interval"
                  name="send_interval"
                  value={formData.send_interval || 0}
                  onChange={handleInputChange}
                  min="60"
                  className="w-full bg-gray-700 text-white px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
                <p className="text-sm text-gray-400 mt-1">
                  최소 60초 (1분) 이상 설정해주세요
                </p>
              </div>

              <div>
                <label htmlFor="message_content" className="block text-sm font-medium text-gray-300 mb-2">
                  메시지 내용
                </label>
                <textarea
                  id="message_content"
                  name="message_content"
                  value={formData.message_content || ''}
                  onChange={handleInputChange}
                  rows={5}
                  className="w-full bg-gray-700 text-white px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="전송할 메시지를 입력하세요..."
                  required
                />
                <p className="text-sm text-gray-400 mt-1">
                  현재 길이: {formData.message_content?.length || 0}자
                </p>
              </div>
            </div>
          </div>

          {/* 이미지 설정 */}
          <div className="bg-gray-800 p-6 rounded-lg">
            <h2 className="text-xl font-semibold mb-4">이미지 설정</h2>
            
            <div className="space-y-4">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="send_with_image"
                  name="send_with_image"
                  checked={formData.send_with_image || false}
                  onChange={handleCheckboxChange}
                  className="w-4 h-4 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"
                />
                <label htmlFor="send_with_image" className="ml-2 text-sm font-medium text-gray-300">
                  이미지와 함께 전송
                </label>
              </div>

              {formData.send_with_image && (
                <div>
                  <label htmlFor="image_path" className="block text-sm font-medium text-gray-300 mb-2">
                    이미지 파일 경로
                  </label>
                  <input
                    type="text"
                    id="image_path"
                    name="image_path"
                    value={formData.image_path || ''}
                    onChange={handleInputChange}
                    className="w-full bg-gray-700 text-white px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="예: /path/to/image.png"
                  />
                </div>
              )}
            </div>
          </div>

          {/* 버튼 */}
          <div className="flex gap-4">
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed px-6 py-3 rounded-lg font-medium transition-colors"
            >
              {isSubmitting ? '저장 중...' : '💾 설정 저장'}
            </button>
            
            <button
              type="button"
              onClick={() => router.push('/')}
              className="px-6 py-3 bg-gray-600 hover:bg-gray-700 rounded-lg font-medium transition-colors"
            >
              취소
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
