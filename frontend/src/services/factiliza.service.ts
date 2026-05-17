import api from './api'

const FACTILIZA_ENDPOINT = '/integraciones/factiliza/'

export const factilizaService = {
  // Obtener configuración de Factiliza
  async getConfig() {
    try {
      const response = await api.get(`${FACTILIZA_ENDPOINT}config`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo configuración de Factiliza:', error)
      throw error
    }
  },

  // Actualizar configuración de Factiliza
  async updateConfig(config: {
    endpoint_url?: string
    auth_token?: string
    timeout_segundos?: number
    max_reintentos?: number
  }) {
    try {
      const response = await api.post(`${FACTILIZA_ENDPOINT}config`, config)
      return response.data
    } catch (error) {
      console.error('Error actualizando configuración de Factiliza:', error)
      throw error
    }
  },

  // Consultar DNI y obtener datos de persona
  async consultarDNI(numero_dni: string) {
    try {
      const response = await api.post(`${FACTILIZA_ENDPOINT}consultar-dni`, {
        numero_dni
      })
      return response.data
    } catch (error) {
      console.error('Error consultando DNI:', error)
      throw error
    }
  },

  // Obtener historial de consultas
  async obtenerHistorialConsultas(filtros?: {
    fecha_inicio?: string
    fecha_fin?: string
    estado?: string
    limit?: number
    offset?: number
  }) {
    try {
      const response = await api.get(`${FACTILIZA_ENDPOINT}historial`, { params: filtros })
      return response.data
    } catch (error) {
      console.error('Error obteniendo historial:', error)
      throw error
    }
  },

  // Obtener detalles de una consulta anterior
  async obtenerConsulta(id_consulta: number) {
    try {
      const response = await api.get(`${FACTILIZA_ENDPOINT}consultas/${id_consulta}`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo consulta:', error)
      throw error
    }
  },

  // Probar conexión
  async testConexion() {
    try {
      const response = await api.get(`${FACTILIZA_ENDPOINT}test`)
      return response.data
    } catch (error) {
      console.error('Error en prueba de conexión:', error)
      throw error
    }
  },

  // Obtener estadísticas de consultas
  async getEstadisticas() {
    try {
      const response = await api.get(`${FACTILIZA_ENDPOINT}estadisticas`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo estadísticas:', error)
      throw error
    }
  }
}

export default factilizaService
