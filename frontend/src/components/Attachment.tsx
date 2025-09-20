import { Download, File } from 'lucide-react';
import React from 'react';
import { attachmentAPI } from '../api/attachment';
import { useProtectedFile } from "../hooks/useProtectedFile";
import type { Attachment as AttachmentType } from '../types';

interface AttachmentProps {
  attachment: AttachmentType;
}

const Attachment: React.FC<AttachmentProps> = ({ attachment }) => {
  const isImage = attachment.file_type.startsWith('image/');
  
  const handleDownload = () => {
    attachmentAPI.downloadAttachment(attachment.id, attachment.file_path);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  if (isImage) {
    const imgSrc = useProtectedFile(attachmentAPI.getAttachmentUrl(attachment.id));

    if (!imgSrc) return <div className="text-gray-500">Загрузка...</div>

    return (
      <div className="relative group">
        <img
          src={imgSrc}
          alt={attachment.file_path}
          className="max-w-full max-h-64 rounded-lg cursor-pointer hover:opacity-90 transition-opacity"
          onClick={handleDownload}
        />
        <div className="absolute inset-0 bg-opacity-0 group-hover:bg-opacity-10 rounded-lg flex items-center justify-center transition-all pointer-events-none">
          <Download href={imgSrc} className="w-6 h-6 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
        </div>
      </div>
    );
  }

  const fileSrc = useProtectedFile(attachmentAPI.getAttachmentUrl(attachment.id));

  return (
    <div
      onClick={handleDownload}
      className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors"
    >
      <div className="flex-shrink-0">
        <File className="w-8 h-8 text-gray-400" />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-900 truncate">
          {attachment.file_path}
        </p>
        <p className="text-xs text-gray-500">
          {formatFileSize(attachment.file_size)}
        </p>
      </div>
      <div className="flex-shrink-0">
        <Download href={fileSrc!} className="w-5 h-5 text-gray-400" />
      </div>
    </div>
  );
};

export default Attachment;