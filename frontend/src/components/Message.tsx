import { Check, Edit3, Trash2, User, X } from 'lucide-react';
import React, { useEffect, useState } from 'react';
import { userAPI } from '../api/user';
import { useAuth } from '../hooks/useAuth';
import { useChat } from '../hooks/useChat';
import type { Message as MessageType } from '../types';
import Attachment from './Attachment';

interface MessageProps {
  message: MessageType;
}

const Message: React.FC<MessageProps> = ({ message }) => {
  const { state: authState } = useAuth();
  const { updateMessage, deleteMessage } = useChat();
  const [isEditing, setIsEditing] = useState(false);
  const [editContent, setEditContent] = useState(message.content);
  const [owner, setOwner] = useState<typeof User>();
  
  const isOwner = message.sender_id === authState.user?.id;
  
  useEffect(() => {
  const fetchOwner = async () => {
      try {
        const user = await userAPI.getUserById(message.sender_id);
          setOwner(user as any);
      } catch (error) {
        console.error('Error while loading owner:', error);
      }
    };

    if (message.sender_id) {
      fetchOwner();
    }

    return () => {
    };
  }, [message.sender_id]);

  const handleEdit = async () => {
    if (editContent.trim() === message.content) {
      setIsEditing(false);
      return;
    }
    
    try {
      await updateMessage(message.id, editContent.trim());
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating message:', error);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Удалить сообщение?')) {
      try {
        await deleteMessage(message.id, message.chat_id);
      } catch (error) {
        console.error('Error deleting message:', error);
      }
    }
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`flex ${isOwner ? 'justify-end' : 'justify-start'} mb-4 group`}>
      <div className={`max-w-xs lg:max-w-md ${isOwner ? 'order-2' : 'order-1'}`}>
        <div
          className={`px-4 py-2 rounded-lg ${
            isOwner
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 text-gray-900'
          } shadow-sm`}
        >
          {!isOwner && (
            <div className="flex items-center space-x-2 mb-1">
              <User className="w-4 h-4 text-gray-500" />
              <span className="text-xs text-gray-500">{owner?.name!}</span>
            </div>
          )}
          
          {isEditing ? (
            <div className="space-y-2">
              <textarea
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
                className="w-full p-2 text-gray-900 bg-white rounded border resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={3}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleEdit();
                  } else if (e.key === 'Escape') {
                    setIsEditing(false);
                    setEditContent(message.content);
                  }
                }}
              />
              <div className="flex justify-end space-x-2">
                <button
                  onClick={() => {
                    setIsEditing(false);
                    setEditContent(message.content);
                  }}
                  className="p-1 text-gray-500 hover:text-gray-700 transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
                <button
                  onClick={handleEdit}
                  className="p-1 text-green-500 hover:text-green-700 transition-colors"
                >
                  <Check className="w-4 h-4" />
                </button>
              </div>
            </div>
          ) : (
            <>
              {message.attachments && message.attachments.length > 0 && (
                <div className="mt-2 space-y-2">
                  {message.attachments.map((attachment) => (
                    <Attachment key={attachment.id} attachment={attachment} />
                  ))}
                </div>
              )}

              <p className="text-sm whitespace-pre-wrap break-words">
                {message.content}
              </p>
            </>
          )}
        </div>
        
        <div className={`flex items-center mt-1 space-x-2 ${isOwner ? 'justify-end' : 'justify-start'}`}>
          <span className="text-xs text-gray-500">
            {formatTime(message.created_at)}
          </span>
          
          {message.edited && (
            <span className="text-xs text-gray-400">(изменено)</span>
          )}
          
          {isOwner && !isEditing && (
            <div className="flex space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <button
                onClick={() => setIsEditing(true)}
                className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
              >
                <Edit3 className="w-3 h-3" />
              </button>
              <button
                onClick={handleDelete}
                className="p-1 text-gray-400 hover:text-red-600 transition-colors"
              >
                <Trash2 className="w-3 h-3" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Message;