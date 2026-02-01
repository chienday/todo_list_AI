import authApi from './authApi';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const getHeaders = () => ({
  'Content-Type': 'application/json',
  Authorization: `Bearer ${authApi.getToken()}`,
});

export const chatbotApi = {
  async sendMessage(messages) {
    const response = await fetch(`${API_URL}/api/chatbot/chat`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ messages }),
    });

    if (!response.ok) {
      throw new Error('Failed to send message');
    }

    return response.json();
  },
};

export default chatbotApi;
