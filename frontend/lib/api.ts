import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;

// Auth
export const registerUser = async (userData: any) => {
  const response = await api.post('/api/auth/register', userData);
  return response.data;
};

export const getUser = async (userId: number) => {
  const response = await api.get(`/api/auth/user/${userId}`);
  return response.data;
};

// Profile
export const getProfile = async (userId: number) => {
  const response = await api.get(`/api/profile/${userId}`);
  return response.data;
};

export const updateProfile = async (userId: number, data: any) => {
  const response = await api.put(`/api/profile/${userId}`, data);
  return response.data;
};

// Check-in
export const submitCheckIn = async (userId: number, data: any) => {
  const response = await api.post(`/api/checkin/${userId}`, data);
  return response.data;
};

export const getRecentCheckIns = async (userId: number, limit = 7) => {
  const response = await api.get(`/api/checkin/${userId}/recent?limit=${limit}`);
  return response.data;
};

// Nutrition
export const lookupNutrient = async (ingredient: string) => {
  const response = await api.get(`/api/nutrition/lookup/${ingredient}`);
  return response.data;
};

export const generateRecipe = async (data: any) => {
  const response = await api.post('/api/nutrition/recipe/generate', data);
  return response.data;
};

export const getNutritionPlans = async (userId: number, limit = 10) => {
  const response = await api.get(`/api/nutrition/plans/${userId}?limit=${limit}`);
  return response.data;
};

export const getTodayNutritionPlans = async (userId: number) => {
  const response = await api.get(`/api/nutrition/plans/${userId}/today`);
  return response.data;
};

// Yoga
export const createYogaPlan = async (userId: number, data: any) => {
  const response = await api.post(`/api/yoga/plan/${userId}`, data);
  return response.data;
};

export const createWeeklyYogaPlan = async (userId: number) => {
  const response = await api.post(`/api/yoga/weekly/${userId}`);
  return response.data;
};

export const getYogaPlans = async (userId: number, limit = 10) => {
  const response = await api.get(`/api/yoga/plans/${userId}?limit=${limit}`);
  return response.data;
};

export const getTodayYogaPlan = async (userId: number) => {
  const response = await api.get(`/api/yoga/plans/${userId}/today`);
  return response.data;
};

// Quiz
export const submitQuiz = async (userId: number, data: any) => {
  const response = await api.post(`/api/quiz/${userId}`, data);
  return response.data;
};

export const getQuizQuestions = async () => {
  const response = await api.get('/api/quiz/questions');
  return response.data;
};

export const getRecentQuizzes = async (userId: number, limit = 5) => {
  const response = await api.get(`/api/quiz/${userId}/recent?limit=${limit}`);
  return response.data;
};

// Dashboard
export const getDashboardOverview = async (userId: number) => {
  const response = await api.get(`/api/dashboard/${userId}/overview`);
  return response.data;
};

export const getTrends = async (userId: number, days = 30) => {
  const response = await api.get(`/api/dashboard/${userId}/trends?days=${days}`);
  return response.data;
};

export const getTopItems = async (userId: number) => {
  const response = await api.get(`/api/dashboard/${userId}/top-items`);
  return response.data;
};

// Reports
export const getWeeklyReport = async (userId: number) => {
  const response = await api.get(`/api/reports/weekly/${userId}`);
  return response.data;
};

export const getMonthlyReport = async (userId: number) => {
  const response = await api.get(`/api/reports/monthly/${userId}`);
  return response.data;
};

// Chatbot
export const sendChatMessage = async (data: any) => {
  const response = await api.post('/api/chatbot/chat', data);
  return response.data;
};

// Decision Trace
export const getRecentTraces = async (userId: number, limit = 10) => {
  const response = await api.get(`/api/trace/${userId}/recent?limit=${limit}`);
  return response.data;
};

export const getTodayTraces = async (userId: number) => {
  const response = await api.get(`/api/trace/${userId}/today`);
  return response.data;
};

