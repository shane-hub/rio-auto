// @ts-ignore
import axios, { type AxiosResponse, type InternalAxiosRequestConfig } from 'axios'
// @ts-ignore
import { ElMessage } from 'element-plus'

const service = axios.create({
  baseURL: (import.meta as any).env.VITE_API_BASE_URL || '/api/v1',
  timeout: 5000,
})

service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error: any) => {
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  (response: AxiosResponse) => {
    return response.data
  },
  (error: any) => {
    if (error.response && error.response.status === 401) {
        localStorage.removeItem('token')
        window.location.href = '/login'
    }
    ElMessage.error(error.message || 'Request Error')
    return Promise.reject(error)
  }
)

export default service
