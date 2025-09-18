import { axiosInstance } from '../utils/axios';
import type { User } from '../types';

interface LoginResponse {
  user: User;
  access_token: string;
}

export const authAPI = {
  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await axiosInstance.post('/auth/login/email', {
      email,
      password,
    });
    return response.data;
  },

  async loginOAuth(auth_provider: string, provider_id: string): Promise<LoginResponse> {
    const response = await axiosInstance.post('/auth/login/oauth', {
      auth_provider,
      provider_id,
    });
    return response.data;
  },

  async register(email: string, password: string, name: string): Promise<LoginResponse> {
    const response = await axiosInstance.post('/auth/register/email', {
      email,
      password,
      name,
    });
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await axiosInstance.get('/users/me');
    return response.data;
  },
};