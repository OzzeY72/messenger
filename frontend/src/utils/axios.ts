import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Перехватчик для добавления токена авторизации
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Перехватчик для обработки ответов
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);