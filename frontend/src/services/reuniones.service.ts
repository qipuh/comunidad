import api from './api'

const REUNIONES_ENDPOINT = '/reuniones'

export const reunionesService = {
  async listarReuniones(estado?: string, tipo?: string) {
    try {
      const response = await api.get(`${REUNIONES_ENDPOINT}/`, {
        params: { estado, tipo }
      })
      return response.data
    } catch (error) {
      console.error('Error listando reuniones:', error)
      throw error
    }
  },

  async crearReunion(datos: any) {
    try {
      const response = await api.post(`${REUNIONES_ENDPOINT}/`, datos)
      return response.data
    } catch (error) {
      console.error('Error creando reunión:', error)
      throw error
    }
  },

  async obtenerReunion(reunionId: number) {
    try {
      const response = await api.get(`${REUNIONES_ENDPOINT}/${reunionId}`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo reunión:', error)
      throw error
    }
  },

  async actualizarReunion(reunionId: number, datos: any) {
    try {
      const response = await api.put(`${REUNIONES_ENDPOINT}/${reunionId}`, datos)
      return response.data
    } catch (error) {
      console.error('Error actualizando reunión:', error)
      throw error
    }
  },

  async eliminarReunion(reunionId: number) {
    try {
      const response = await api.delete(`${REUNIONES_ENDPOINT}/${reunionId}`)
      return response.data
    } catch (error) {
      console.error('Error eliminando reunión:', error)
      throw error
    }
  },

  async cambiarEstado(reunionId: number, estado: string) {
    try {
      const response = await api.put(`${REUNIONES_ENDPOINT}/${reunionId}/estado`, { estado })
      return response.data
    } catch (error) {
      console.error('Error cambiando estado:', error)
      throw error
    }
  },

  async registrarAsistenciaQR(reunionId: number, dni: string) {
    try {
      const response = await api.post(`${REUNIONES_ENDPOINT}/${reunionId}/asistencia/qr`, { dni })
      return response.data
    } catch (error) {
      console.error('Error registrando asistencia por QR:', error)
      throw error
    }
  },

  async registrarAsistenciaFacial(reunionId: number, fotoBase64: string) {
    try {
      const response = await api.post(`${REUNIONES_ENDPOINT}/${reunionId}/asistencia/facial`, { foto_base64: fotoBase64 })
      return response.data
    } catch (error) {
      console.error('Error registrando asistencia por facial:', error)
      throw error
    }
  },

  async listarAsistentes(reunionId: number) {
    try {
      const response = await api.get(`${REUNIONES_ENDPOINT}/${reunionId}/asistentes`)
      return response.data
    } catch (error) {
      console.error('Error listando asistentes:', error)
      throw error
    }
  },

  async removerAsistente(reunionId: number, usuarioId: number) {
    try {
      const response = await api.delete(`${REUNIONES_ENDPOINT}/${reunionId}/asistentes/${usuarioId}`)
      return response.data
    } catch (error) {
      console.error('Error removiendo asistente:', error)
      throw error
    }
  },

  async obtenerReporte(reunionId: number) {
    try {
      const response = await api.get(`${REUNIONES_ENDPOINT}/${reunionId}/reporte`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo reporte:', error)
      throw error
    }
  }
}

export default reunionesService
