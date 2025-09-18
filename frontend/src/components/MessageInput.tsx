import React, { useState, useRef } from 'react';
import { Send, Paperclip, X } from 'lucide-react';
import { useChat } from '../hooks/useChat';

const MessageInput: React.FC = () => {
  const { sendMessage } = useChat();
  const [content, setContent] = useState('');
  const [files, setFiles] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!content.trim() && files.length === 0) return;
    
    try {
      setIsLoading(true);
      await sendMessage(content, files);
      setContent('');
      setFiles([]);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || []);
    setFiles(prev => [...prev, ...selectedFiles]);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="p-4 border-t border-gray-200 bg-white">
      {/* File previews */}
      {files.length > 0 && (
        <div className="mb-3 space-y-2">
          {files.map((file, index) => (
            <div key={index} className="flex items-center space-x-3 p-2 bg-gray-50 rounded-lg">
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">{file.name}</p>
                <p className="text-xs text-gray-500">{formatFileSize(file.size)}</p>
              </div>
              <button
                onClick={() => removeFile(index)}
                className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Input form */}
      <form onSubmit={handleSubmit} className="flex items-end space-x-3">
        <div className="flex-1">
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Введите сообщение..."
            rows={1}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            style={{ minHeight: '40px', maxHeight: '120px' }}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
          />
        </div>

        <div className="flex items-center space-x-2">
          <input
            ref={fileInputRef}
            type="file"
            multiple
            onChange={handleFileSelect}
            className="hidden"
            accept="image/*,.pdf,.doc,.docx,.txt"
          />
          
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <Paperclip className="w-5 h-5" />
          </button>

          <button
            type="submit"
            disabled={isLoading || (!content.trim() && files.length === 0)}
            className="p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  );
};

export default MessageInput;