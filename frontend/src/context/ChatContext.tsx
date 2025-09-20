import React, { createContext, useContext, useReducer } from 'react';
import type { Chat, ChatAction, ChatState, Message } from '../types';

const initialState: ChatState = {
  chats: [],
  currentChatId: null,
  messages: {},
  isLoading: false,
};

const chatReducer = (state: ChatState, action: ChatAction): ChatState => {
  switch (action.type) {
    case 'SET_CHATS':
      return {
        ...state,
        chats: action.payload,
      };
    case 'SET_CURRENT_CHAT':
      return {
        ...state,
        currentChatId: action.payload,
      };
    case 'ADD_MESSAGE':
      const message = action.payload;
      return {
        ...state,
        messages: {
          ...state.messages,
          [message.chat_id]: [
            ...(state.messages[message.chat_id] || []),
            message,
          ],
        },
      };
    case 'UPDATE_MESSAGE':
      const updatedMessage = action.payload;
      return {
        ...state,
        messages: {
          ...state.messages,
          [updatedMessage.chat_id]: state.messages[updatedMessage.chat_id]?.map(msg =>
            msg.id === updatedMessage.id ? updatedMessage : msg
          ) || [],
        },
      };
    case 'DELETE_MESSAGE':
      const { chatId, messageId } = action.payload;
      return {
        ...state,
        messages: {
          ...state.messages,
          [chatId]: state.messages[chatId]?.filter(msg => msg.id !== messageId) || [],
        },
      };
    case 'SET_MESSAGES':
      return {
        ...state,
        messages: {
          ...state.messages,
          [action.payload.chatId]: action.payload.messages,
        },
      };
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload,
      };
    default:
      return state;
  }
};

interface ChatContextType {
  state: ChatState;
  dispatch: React.Dispatch<ChatAction>;
  getCurrentChat: () => Chat | null;
  getCurrentMessages: () => Message[];
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  const getCurrentChat = () => {
    if (!state.currentChatId) return null;
    return state.chats.find(chat => chat.id === state.currentChatId) || null;
  };

  const getCurrentMessages = () => {
    if (!state.currentChatId) return [];
    return state.messages[state.currentChatId] || [];
  };
  
  return (
    <ChatContext.Provider value={{ state, dispatch, getCurrentChat, getCurrentMessages }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};