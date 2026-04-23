import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000/api',
})

export const getHealth = async () => (await api.get('/health')).data
export const getCropRecommendation = async (payload) => (await api.post('/recommend/crop', payload)).data
