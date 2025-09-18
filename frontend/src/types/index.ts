export interface User {
  id: string;
  email: string;
  name: string;
}

export interface Chat {
  id: string;
  members: User[];
  created_at: string;
  last_message?: Message;
}

export interface Message {
  id: string;
  chat_id: string;
  sender_id: string;
  content: string;
  attachments: Attachment[];
  created_at: string;
  updated_at: string;
  edited: boolean;
}

export interface Attachment {
  id: string;
  message_id: string;
  file_path: string;
  file_type: string;
  file_size: number;
  url: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface ChatState {
  chats: Chat[];
  currentChatId: string | null;
  messages: Record<string, Message[]>;
  isLoading: boolean;
}

export type AuthAction =
  | { type: 'SET_USER'; payload: { user: User; token: string } }
  | { type: 'LOGOUT' }
  | { type: 'SET_LOADING'; payload: boolean };

export type ChatAction =
  | { type: 'SET_CHATS'; payload: Chat[] }
  | { type: 'SET_CURRENT_CHAT'; payload: string | null }
  | { type: 'ADD_MESSAGE'; payload: Message }
  | { type: 'UPDATE_MESSAGE'; payload: Message }
  | { type: 'DELETE_MESSAGE'; payload: { chatId: string; messageId: string } }
  | { type: 'SET_MESSAGES'; payload: { chatId: string; messages: Message[] } }
  | { type: 'SET_LOADING'; payload: boolean };