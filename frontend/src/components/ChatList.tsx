import { Plus, Search, User } from 'lucide-react';
import React, { useEffect, useState } from 'react';
import { chatAPI } from '../api/chat';
import { userAPI } from '../api/user';
import { useAuth } from '../hooks/useAuth';
import { useChat } from '../hooks/useChat';
import type { User as UserType } from '../types';

const ChatList: React.FC = () => {
  const { chats, currentChatId, selectChat, loadChats } = useChat();
  const { state: authState } = useAuth();
  const [searchQuery, setSearchQuery] = useState('');
  const [showNewChatModal, setShowNewChatModal] = useState(false);
  const [userSearchQuery, setUserSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<UserType[]>([]);

  useEffect(() => {
    loadChats();
  }, []);

  const filteredChats = chats.filter(chat => {
    const otherUser = chat.members.find(p => p.id !== authState.user?.id);
    return otherUser?.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
           otherUser?.email.toLowerCase().includes(searchQuery.toLowerCase());
  });

  const searchUsers = async (query: string) => {
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }
    
    try {
      const results = await userAPI.searchUsers(query);
      setSearchResults(results.filter(user => user.id !== authState.user?.id));
    } catch (error) {
      console.error('Error searching users:', error);
    }
  };

  const createChat = async (userId: string) => {
    try {
      const newChat = await chatAPI.createChat([userId]);
      await loadChats();
      selectChat(newChat.id);
      setShowNewChatModal(false);
      setUserSearchQuery('');
      setSearchResults([]);
    } catch (error) {
      console.error('Error creating chat:', error);
    }
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    
    if (diff < 24 * 60 * 60 * 1000) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else {
      return date.toLocaleDateString([], { day: '2-digit', month: '2-digit' });
    }
  };

  return (
    <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-xl font-semibold text-gray-800">Чаты</h1>
          <button
            onClick={() => setShowNewChatModal(true)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <Plus className="w-5 h-5 text-gray-600" />
          </button>
        </div>
        
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <input
            type="text"
            placeholder="Поиск чатов..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Chat List */}
      <div className="flex-1 overflow-y-auto">
        {filteredChats.map((chat) => {
          const otherUser = chat.members.find(p => p.id !== authState.user?.id);
          const isActive = chat.id === currentChatId;
          
          return (
            <div
              key={chat.id}
              onClick={() => selectChat(chat.id)}
              className={`p-4 border-b border-gray-100 cursor-pointer hover:bg-gray-50 transition-colors ${
                isActive ? 'bg-blue-50 border-r-4 border-r-blue-500' : ''
              }`}
            >
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
                    <User className="w-6 h-6 text-gray-600" />
                  </div>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {otherUser?.name || 'Unknown User'}
                    </p>
                    {chat.last_message && (
                      <p className="text-xs text-gray-500 flex-shrink-0">
                        {formatTime(chat.last_message.created_at)}
                      </p>
                    )}
                  </div>
                  {chat.last_message && (
                    <p className="text-sm text-gray-500 truncate mt-1">
                      {chat.last_message.content}
                    </p>
                  )}
                </div>
              </div>
            </div>
          );
        })}
        
        {filteredChats.length === 0 && (
          <div className="p-8 text-center text-gray-500">
            <p>Чаты не найдены</p>
          </div>
        )}
      </div>

      {/* New Chat Modal */}
      {showNewChatModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-96 max-w-full mx-4">
            <h2 className="text-lg font-semibold mb-4">Создать новый чат</h2>
            
            <div className="relative mb-4">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Поиск пользователей..."
                value={userSearchQuery}
                onChange={(e) => {
                  setUserSearchQuery(e.target.value);
                  searchUsers(e.target.value);
                }}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div className="max-h-60 overflow-y-auto mb-4">
              {searchResults.map((user) => (
                <div
                  key={user.id}
                  onClick={() => createChat(user.id)}
                  className="p-3 hover:bg-gray-50 rounded-lg cursor-pointer flex items-center space-x-3"
                >
                  <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                    <User className="w-4 h-4 text-gray-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">{user.name}</p>
                    <p className="text-xs text-gray-500">{user.email}</p>
                  </div>
                </div>
              ))}
              
              {userSearchQuery && searchResults.length === 0 && (
                <p className="text-center text-gray-500 py-4">Пользователи не найдены</p>
              )}
            </div>

            <div className="flex justify-end space-x-2">
              <button
                onClick={() => {
                  setShowNewChatModal(false);
                  setUserSearchQuery('');
                  setSearchResults([]);
                }}
                className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Отмена
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatList;