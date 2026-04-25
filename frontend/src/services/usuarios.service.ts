import api from './api'

const USUARIOS_ENDPOINT = '/usuarios'

export const usuariosService = {
  // Listar todos los usuarios
  async listarUsuarios(limit = 50, offset = 0) {
    try {
      const response = await api.get(USUARIOS_ENDPOINT, {
        params: { limit, offset }
      })
      return response.data
    } catch (error) {
      console.error('Error listando usuarios:', error)
      throw error
    }
  },

  // Obtener un usuario por ID
  async obtenerUsuario(usuarioId: number) {
    try {
      const response = await api.get(`${USUARIOS_ENDPOINT}/${usuarioId}`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo usuario:', error)
      throw error
    }
  },

  // Crear nuevo usuario
  async crearUsuario(datos: FormData) {
    try {
      const response = await api.post(USUARIOS_ENDPOINT + '/', datos)
      return response.data
    } catch (error) {
      console.error('Error creando usuario:', error)
      throw error
    }
  },

  // Actualizar usuario
  async actualizarUsuario(usuarioId: number, datos: FormData) {
    try {
      const response = await api.put(`${USUARIOS_ENDPOINT}/${usuarioId}`, datos)
      return response.data
    } catch (error) {
      console.error('Error actualizando usuario:', error)
      throw error
    }
  },

  // Eliminar usuario
  async eliminarUsuario(usuarioId: number) {
    try {
      const response = await api.delete(`${USUARIOS_ENDPOINT}/${usuarioId}`)
      return response.data
    } catch (error) {
      console.error('Error eliminando usuario:', error)
      throw error
    }
  },

  // Buscar usuario por email
  async buscarPorEmail(email: string) {
    try {
      const response = await api.get(`${USUARIOS_ENDPOINT}/buscar/por-email`, {
        params: { email }
      })
      return response.data
    } catch (error) {
      console.error('Error buscando usuario:', error)
      throw error
    }
  },

  // Obtener estadísticas
  async obtenerEstadisticas() {
    try {
      const response = await api.get(`${USUARIOS_ENDPOINT}/estadisticas/total`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo estadísticas:', error)
      throw error
    }
  }
}

export default usuariosService
