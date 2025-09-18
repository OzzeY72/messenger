import { axiosInstance } from '../utils/axios';
import type { Message } from '../types';

export const messageAPI = {
  async fetchMessages(chatId: string): Promise<Message[]> {
    const response = await axiosInstance.get(`/messages/chat/${chatId}/`);
    return response.data;
  },

  async sendMessage(chatId: string, content: string, files?: File[]): Promise<Message> {
    const formData = new FormData();
    formData.append('content', content);
    formData.append('chat_id', chatId);

    if (files) {
      files.forEach((file) => {
        formData.append('files', file);
      });
    }

    const response = await axiosInstance.post('/messages', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async updateMessage(messageId: string, content: string): Promise<Message> {
    const response = await axiosInstance.put(`/messages/${messageId}`, {
      content,
    });
    return response.data;
  },

  async deleteMessage(messageId: string): Promise<void> {
    await axiosInstance.delete(`/messages/${messageId}`);
  },
};