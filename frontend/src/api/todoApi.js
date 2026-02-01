import authApi from './authApi';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const getHeaders = () => ({
  'Content-Type': 'application/json',
  Authorization: `Bearer ${authApi.getToken()}`,
});

export const todoApi = {
  async getTodos() {
    const response = await fetch(`${API_URL}/api/todos/`, {
      headers: getHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch todos');
    }

    return response.json();
  },

  async createTodo(todoData) {
    const response = await fetch(`${API_URL}/api/todos/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(todoData),
    });

    if (!response.ok) {
      throw new Error('Failed to create todo');
    }

    return response.json();
  },

  async updateTodo(todoId, todoData) {
    const response = await fetch(`${API_URL}/api/todos/${todoId}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(todoData),
    });

    if (!response.ok) {
      throw new Error('Failed to update todo');
    }

    return response.json();
  },

  async deleteTodo(todoId) {
    const response = await fetch(`${API_URL}/api/todos/${todoId}`, {
      method: 'DELETE',
      headers: getHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to delete todo');
    }

    return true;
  },
};

export default todoApi;
