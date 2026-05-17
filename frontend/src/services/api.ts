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
    console.log('\n[API Request] ===== REQUEST DEBUG =====')
    console.log('[API Request] URL:', config.url)
    console.log('[API Request] Method:', config.method)
    console.log('[API Request] localStorage.length:', localStorage.length)
    console.log('[API Request] localStorage.keys():', Object.keys(localStorage))
    const token = localStorage.getItem('auth_token')
    console.log('[API Request] localStorage.getItem("auth_token"):', token ? token.substring(0, 20) + '...' : 'NULL')
    console.log('[API Request] localStorage.getItem("auth_usuario"):', localStorage.getItem('auth_usuario') ? 'EXISTS' : 'NULL')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      console.log('[API Request] ✓ Authorization header set')
    } else {
      console.warn('[API Request] ✗ WARNING: No token found in localStorage!')
      console.warn('[API Request] All localStorage keys:', localStorage)
    }
    console.log('[API Request] ===== END DEBUG =====\n')
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
