import type { User } from '../types';
import { axiosInstance } from '../utils/axios';

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

  async loginOAuth(auth_provider: string, code: string): Promise<LoginResponse> {
    const response = await axiosInstance.post('/auth/login/oauth', {
      provider_id: code,
      auth_provider: auth_provider,
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