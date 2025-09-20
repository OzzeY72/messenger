import React, { createContext, useContext, useEffect, useReducer } from 'react';
import { authAPI } from '../api/auth';
import type { AuthAction, AuthState } from '../types';

const initialState: AuthState = {
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,
};

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'SET_USER':
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        isLoading: false,
      };
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
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

interface AuthContextType {
  state: AuthState;
  login: (email: string, password: string) => Promise<void>;
  loginOAuth: (provider: string, token: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      authAPI
        .getCurrentUser()
        .then((user) => {
          dispatch({ type: 'SET_USER', payload: { user, token } });
        })
        .catch(() => {
          localStorage.removeItem('authToken');
          dispatch({ type: 'SET_LOADING', payload: false });
        });
    } else {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await authAPI.login(email, password);
      localStorage.setItem('authToken', response.access_token);
      dispatch({ type: 'SET_USER', payload: { user: response.user, token: response.access_token } });
    } catch (error) {
      throw error;
    }
  };

  const loginOAuth = async (provider: string, token: string) => {
    try {
      const response = await authAPI.loginOAuth(provider, token);
      console.log(response);
      localStorage.setItem('authToken', response.access_token);
      dispatch({ type: 'SET_USER', payload: { user: response.user, token: response.access_token } });
    } catch (error) {
      throw error;
    }
  };

  const register = async (email: string, password: string, name: string) => {
    try {
      const response = await authAPI.register(email, password, name);
      localStorage.setItem('authToken', response.access_token);
      dispatch({ type: 'SET_USER', payload: { user: response.user, token: response.access_token } });
    } catch (error) {
      throw error;
    }
  };

  const logout = async () => {
    localStorage.removeItem('authToken');
    dispatch({ type: 'LOGOUT' });
  };

  return (
    <AuthContext.Provider value={{ state, login, loginOAuth, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};