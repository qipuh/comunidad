/**
 * Configuración de Axios para comunicación con el backend
 */

import axios from 'axios'

// Crear instancia de axios con configuración base
export const api = axios.create({
  baseURL: 'http://localhost:8080/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para agregar token si existe
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Manejar errores 401 (no autorizado)
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token')
      // Opcional: redirigir a login
      // window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
