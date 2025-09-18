import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { LogOut } from 'lucide-react';
import ChatList from '../components/ChatList';
import ChatWindow from '../components/ChatWindow';

const ChatPage: React.FC = () => {
  const { state: authState, logout } = useAuth();

  const handleLogout = async () => {
    if (window.confirm('Вы уверены, что хотите выйти?')) {
      await logout();
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <div className="flex flex-col h-full">
        {/* User info */}
        <div className="p-4 bg-white border-b border-gray-200 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
              <span className="text-white text-sm font-medium">
                {authState.user?.name.charAt(0).toUpperCase()}
              </span>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-900">{authState.user?.name}</p>
              <p className="text-xs text-gray-500">{authState.user?.email}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            title="Выйти"
          >
            <LogOut className="w-5 h-5" />
          </button>
        </div>
        
        <ChatList />
      </div>
      
      <ChatWindow />
    </div>
  );
};

export default ChatPage;