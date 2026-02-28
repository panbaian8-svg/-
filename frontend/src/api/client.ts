import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// AI Provider API
export const getProvider = () => api.get('/knowledge/provider')

export const switchProvider = (provider: string) =>
  api.post('/knowledge/provider/switch', { provider })

export default api
