import { chatAPI } from '../api/chat';
import { messageAPI } from '../api/message';
import { useChat as useChatContext } from '../context/ChatContext';

export const useChat = () => {
  const { state, dispatch, getCurrentChat, getCurrentMessages } = useChatContext();

  const loadChats = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const chats = await chatAPI.fetchChats();
      dispatch({ type: 'SET_CHATS', payload: chats });
    } catch (error) {
      console.error('Error loading chats:', error);
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const loadMessages = async (chatId: string) => {
    try {
      const messages = await messageAPI.fetchMessages(chatId);
      dispatch({ type: 'SET_MESSAGES', payload: { chatId, messages } });
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const sendMessage = async (content: string, files?: File[]) => {
    if (!state.currentChatId) return;

    try {
      // const message = await messageAPI.sendMessage(state.currentChatId, content, files);
      await messageAPI.sendMessage(state.currentChatId, content, files);
      //dispatch({ type: 'ADD_MESSAGE', payload: message });
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  };

  const updateMessage = async (messageId: string, content: string) => {
    try {
      // const updatedMessage = await messageAPI.updateMessage(messageId, content);
      await messageAPI.updateMessage(messageId, content);
      //dispatch({ type: 'UPDATE_MESSAGE', payload: updatedMessage });
    } catch (error) {
      console.error('Error updating message:', error);
      throw error;
    }
  };

  const deleteMessage = async (messageId: string, chatId: string) => {
    try {
      await messageAPI.deleteMessage(messageId);
      console.log(chatId);
      //dispatch({ type: 'DELETE_MESSAGE', payload: { chatId, messageId } });
    } catch (error) {
      console.error('Error deleting message:', error);
      throw error;
    }
  };

  const selectChat = (chatId: string | null) => {
    dispatch({ type: 'SET_CURRENT_CHAT', payload: chatId });
    if (chatId) {
      loadMessages(chatId);
    }
  };

  return {
    ...state,
    getCurrentChat,
    getCurrentMessages,
    loadChats,
    loadMessages,
    sendMessage,
    updateMessage,
    deleteMessage,
    selectChat,
  };
};