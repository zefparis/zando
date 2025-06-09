import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  // Ne pas mettre de Content-Type global pour permettre à Axios de le définir pour les FormData
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('zando_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Ajout de la nouvelle fonction
export const getAds = () => apiClient.get('/ads/');

// Ajout de la nouvelle fonction
export const createAd = (formData) => {
  return apiClient.post('/ads/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export default apiClient;