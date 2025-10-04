export interface BotStatus {
  is_running: boolean;
  is_connected: boolean;
  is_enabled: boolean;
  next_send_time?: string;
  current_time: string;
}

export interface BotConfig {
  channel_id: string;
  send_interval: number;
  message_content: string;
  send_with_image: boolean;
  image_path?: string;
}

export interface LogData {
  logs: string[];
  total_lines: number;
  shown_lines: number;
}

export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
}

export type BotAction = 'start' | 'stop' | 'send_now';
