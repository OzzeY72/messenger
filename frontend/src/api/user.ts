import type { User } from '../types';
import { axiosInstance } from '../utils/axios';

export const userAPI = {
  async getMe(): Promise<User> {
    const response = await axiosInstance.get('/users/me');
    return response.data;
  },

  async getUserById(userId: string): Promise<User> {
    const response = await axiosInstance.get(`/users/${userId}`);
    return response.data;
  },

  async searchUsers(query: string): Promise<User[]> {
    const response = await axiosInstance.get('/users/', {
      params: { q: query },
    });
    return response.data;
  },
};
