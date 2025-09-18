import { axiosInstance } from '../utils/axios';

export const attachmentAPI = {
  getAttachmentUrl(attachmentId: string): string {
    return `${axiosInstance.defaults.baseURL}/attachments/${attachmentId}`;
  },

  async downloadAttachment(attachmentId: string, filename: string): Promise<void> {
    const response = await axiosInstance.get(`/attachments/${attachmentId}`, {
      responseType: 'blob',
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },
};