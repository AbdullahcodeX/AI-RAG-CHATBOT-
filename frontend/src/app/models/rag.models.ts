export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  sources?: string[];
}

export interface UploadResult {
  session_id: string;
  filename: string;
  chunks_indexed: number;
  message: string;
}

export interface ChatResult {
  answer: string;
  sources: string[];
}

export interface SessionStatus {
  session_id: string;
  document_count: number;
  chunk_count: number;
  filenames: string[];
}
