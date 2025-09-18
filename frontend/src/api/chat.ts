import { axiosInstance } from '../utils/axios';
import type { Chat } from '../types';

export const chatAPI = {
  async fetchChats(): Promise<Chat[]> {
    const response = await axiosInstance.get('/chats');
    return response.data;
  },

  async createChat(userIds: string[]): Promise<Chat> {
    const response = await axiosInstance.post('/chats', {
      participant_ids: userIds,
    });
    return response.data;
  },

  async getChatById(chatId: string): Promise<Chat> {
    const response = await axiosInstance.get(`/chats/${chatId}`);
    return response.data;
  },

  async searchUsers(query: string): Promise<any[]> {
    const response = await axiosInstance.get(`/users/search?q=${query}`);
    return response.data;
  },
};