import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export interface AskResponse {
  answer: string;
  sources: { chunk_id: string; content: string }[];
}

export const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await api.post('/documents/upload', formData);
  return res.data;
};

export const askQuestion = async (question: string): Promise<AskResponse> => {
  const res = await api.post('/ask', { question, top_k: 3 });
  return res.data;
};