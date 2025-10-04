import axios from 'axios';
import { BotStatus, BotConfig, LogData, ApiResponse, BotAction } from '@/types/bot';

// API 베이스 URL 설정 (개발환경과 프로덕션 환경 구분)
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? ''  // 프로덕션에서는 상대 경로 (같은 도메인)
  : 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// API 함수들
export const botApi = {
  // 봇 상태 조회
  getStatus: async (): Promise<BotStatus> => {
    const response = await api.get<BotStatus>('/api/status');
    return response.data;
  },

  // 봇 제어 (시작/중지/즉시전송)
  controlBot: async (action: BotAction): Promise<ApiResponse> => {
    const response = await api.post<ApiResponse>(`/api/bot/${action}`);
    return response.data;
  },

  // 봇 설정 조회
  getConfig: async (): Promise<BotConfig> => {
    const response = await api.get<BotConfig>('/api/config');
    return response.data;
  },

  // 봇 설정 업데이트
  updateConfig: async (config: Partial<BotConfig>): Promise<ApiResponse> => {
    const response = await api.post<ApiResponse>('/api/config', config);
    return response.data;
  },

  // 로그 조회
  getLogs: async (lines: number = 100): Promise<LogData> => {
    const response = await api.get<LogData>(`/api/logs?lines=${lines}`);
    return response.data;
  },
};

// SWR용 fetcher 함수
export const fetcher = (url: string) => api.get(url).then(res => res.data);

export default api;
