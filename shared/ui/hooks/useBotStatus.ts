import { useState, useEffect, useCallback } from 'react';
import useSWR from 'swr';
import { BotStatus, BotAction } from '@/types/bot';
import { botApi } from '@/lib/api';

export function useBotStatus() {
  const { data, error, mutate, isLoading } = useSWR<BotStatus>(
    '/api/status',
    () => botApi.getStatus(),
    {
      refreshInterval: (data) => {
        // 적응형 새로고침: 봇이 실행 중이면 30초, 아니면 60초
        return data?.is_running ? 30000 : 60000;
      },
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
      dedupingInterval: 10000, // 10초 내 중복 요청 방지
      errorRetryCount: 3,
      errorRetryInterval: 5000,
    }
  );

  const controlBot = useCallback(async (action: BotAction) => {
    try {
      const result = await botApi.controlBot(action);
      // 성공 시 1초 후 상태 새로고침
      setTimeout(() => mutate(), 1000);
      return result;
    } catch (error) {
      // 실패 시에도 상태 새로고침
      setTimeout(() => mutate(), 1000);
      throw error;
    }
  }, [mutate]);

  return {
    status: data,
    isLoading,
    error,
    mutate,
    controlBot,
  };
}

export function useCountdown(nextSendTime?: string, serverTime?: string) {
  const [timeLeft, setTimeLeft] = useState<{
    hours: number;
    minutes: number;
    seconds: number;
    totalSeconds: number;
  } | null>(null);

  useEffect(() => {
    if (!nextSendTime || !serverTime) {
      setTimeLeft(null);
      return;
    }

    // 서버 시간과 로컬 시간의 차이 계산
    const serverTimestamp = new Date(serverTime).getTime();
    const localTimestamp = Date.now();
    const timeOffset = serverTimestamp - localTimestamp;

    const updateCountdown = () => {
      const now = Date.now() + timeOffset;
      const target = new Date(nextSendTime).getTime();
      const diff = Math.max(0, Math.floor((target - now) / 1000));

      if (diff > 0) {
        const hours = Math.floor(diff / 3600);
        const minutes = Math.floor((diff % 3600) / 60);
        const seconds = diff % 60;

        setTimeLeft({
          hours,
          minutes,
          seconds,
          totalSeconds: diff,
        });
      } else {
        setTimeLeft({
          hours: 0,
          minutes: 0,
          seconds: 0,
          totalSeconds: 0,
        });
      }
    };

    // 즉시 업데이트
    updateCountdown();

    // 1초마다 업데이트
    const interval = setInterval(updateCountdown, 1000);

    return () => clearInterval(interval);
  }, [nextSendTime, serverTime]);

  return timeLeft;
}
