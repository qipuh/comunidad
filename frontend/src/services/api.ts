/**
 * Configuración de Axios para comunicación con el backend
 */

import axios from 'axios'

// Crear instancia de axios con configuración base
export const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  maxRedirects: 5  // Ensure axios follows redirects (307, 308, etc.)
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
    // No limpiar tokens en 401 - dejar que el usuario maneje la sesión
    return Promise.reject(error)
  }
)

export default api
