import { useLogs } from '@/hooks/useLogs';
import { useEffect, useRef } from 'react';

export default function LogViewer() {
  const { logs, isLoading, refreshLogs, setLogLines, currentLines } = useLogs();
  const logContainerRef = useRef<HTMLDivElement>(null);

  // 로그가 업데이트되면 스크롤을 맨 아래로
  useEffect(() => {
    if (logContainerRef.current && logs?.logs) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs]);

  const getLogColor = (log: string) => {
    if (log.includes('ERROR')) return 'text-red-400';
    if (log.includes('WARNING')) return 'text-yellow-400';
    if (log.includes('INFO')) return 'text-blue-400';
    return 'text-gray-300';
  };

  const handleLinesChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setLogLines(parseInt(e.target.value));
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg mt-8">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-semibold">📋 시스템 로그</h3>
        <div className="flex items-center space-x-2">
          <select 
            value={currentLines}
            onChange={handleLinesChange}
            className="bg-gray-700 text-white px-3 py-1 rounded"
          >
            <option value={50}>최근 50줄</option>
            <option value={100}>최근 100줄</option>
            <option value={200}>최근 200줄</option>
          </select>
          <button 
            onClick={refreshLogs}
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-3 py-1 rounded text-sm transition-colors"
          >
            {isLoading ? '🔄 로딩...' : '🔄 새로고침'}
          </button>
        </div>
      </div>
      
      <div 
        ref={logContainerRef}
        className="bg-gray-900 p-4 rounded-lg h-64 overflow-y-auto font-mono text-sm"
      >
        {isLoading ? (
          <div className="text-gray-500">로그를 불러오는 중...</div>
        ) : logs && logs.logs.length > 0 ? (
          logs.logs.map((log, index) => (
            <div key={index} className={getLogColor(log)}>
              {log}
            </div>
          ))
        ) : (
          <div className="text-gray-500">로그가 없습니다.</div>
        )}
      </div>
      
      {logs && (
        <div className="mt-2 text-sm text-gray-400">
          총 {logs.total_lines}줄 중 최근 {logs.shown_lines}줄 표시
        </div>
      )}
    </div>
  );
}
