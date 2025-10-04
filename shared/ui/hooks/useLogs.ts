import { useState, useCallback } from 'react';
import useSWR from 'swr';
import { LogData } from '@/types/bot';
import { botApi } from '@/lib/api';

export function useLogs() {
  const [lines, setLines] = useState(100);
  
  const { data, error, mutate, isLoading } = useSWR<LogData>(
    ['logs', lines],
    () => botApi.getLogs(lines),
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: false,
      refreshInterval: 0, // 수동으로만 새로고침
    }
  );

  const refreshLogs = useCallback(() => {
    mutate();
  }, [mutate]);

  const setLogLines = useCallback((newLines: number) => {
    setLines(newLines);
  }, []);

  return {
    logs: data,
    isLoading,
    error,
    refreshLogs,
    setLogLines,
    currentLines: lines,
  };
}
