import api from './api'

export interface Usuario {
  id: number
  nombre_completo: string
  username: string
  numero_dni: string
  email: string
  rol: string
  foto_frontal?: string
  usar_reconocimiento_facial: boolean
}

export const authService = {
  async login(username: string, password: string) {
    const response = await api.post('/auth/login', { username, password })
    return response.data
  },

  async loginFacial(foto_base64: string) {
    const response = await api.post('/auth/login-facial', { foto_base64 })
    return response.data
  },

  async logout() {
    await api.post('/auth/logout').catch(() => {})
    localStorage.removeItem('auth_token')
    localStorage.removeItem('auth_usuario')
  },

  guardarSesion(token: string, usuario: Usuario) {
    localStorage.setItem('auth_token', token)
    localStorage.setItem('auth_usuario', JSON.stringify(usuario))
  },

  obtenerUsuario(): Usuario | null {
    const data = localStorage.getItem('auth_usuario')
    return data ? JSON.parse(data) : null
  },

  estaAutenticado(): boolean {
    return !!localStorage.getItem('auth_token')
  }
}

export default authService
