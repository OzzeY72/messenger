import React, { useEffect, useRef } from 'react';
import { User } from 'lucide-react';
import { useChat } from '../hooks/useChat';
import { useAuth } from '../hooks/useAuth';
import Message from './Message';
import MessageInput from './MessageInput';

const ChatWindow: React.FC = () => {
  const { getCurrentChat, getCurrentMessages } = useChat();
  const { state: authState } = useAuth();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const currentChat = getCurrentChat();
  const messages = getCurrentMessages();

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  if (!currentChat) {
    return (
      <div className="flex-1 flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
            <User className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Выберите чат
          </h3>
          <p className="text-gray-500">
            Выберите существующий чат или создайте новый для начала общения
          </p>
        </div>
      </div>
    );
  }

  const otherUser = currentChat.members.find(p => p.id !== authState.user?.id);

  return (
    <div className="flex-1 flex flex-col">
      {/* Chat Header */}
      <div className="p-4 border-b border-gray-200 bg-white">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
            <User className="w-6 h-6 text-gray-600" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">
              {otherUser?.name || 'Unknown User'}
            </h2>
            <p className="text-sm text-gray-500">{otherUser?.email}</p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-500 text-center">
              Начните общение, отправив первое сообщение
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            {messages.map((message) => (
              <Message key={message.id} message={message} />
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Message Input */}
      <MessageInput />
    </div>
  );
};

export default ChatWindow;