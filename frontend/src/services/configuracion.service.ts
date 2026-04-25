/**
 * Servicio para comunicación con API de configuración
 *
 * Endpoints:
 * - GET /api/admin/configuracion/campos
 * - POST /api/admin/configuracion/campos
 * - PUT /api/admin/configuracion/campos/{id}
 * - DELETE /api/admin/configuracion/campos/{id}
 * - GET /api/admin/integraciones-api
 * - POST /api/admin/integraciones-api
 * - etc.
 */

import { api } from './api'

export interface ConfiguracionCampo {
  id: number
  nombre_campo: string
  etiqueta: string
  descripcion?: string
  tipo_dato: string
  es_obligatorio: boolean
  posicion: number
  api_integracion_id?: number
  campo_mapa_api?: string
  mostrar_en_registro: boolean
  mostrar_en_perfil: boolean
  mostrar_en_reportes: boolean
}

export interface IntegracionAPI {
  id: number
  nombre: string
  descripcion?: string
  tipo: string
  endpoint_url: string
  auth_type: string
  activa: boolean
  timeout_segundos: number
  max_reintentos: number
  created_at: string
}

export interface ResultadoProeba {
  disponible: boolean
  error?: string
  datos?: Record<string, any>
}

class ConfiguracionService {
  /**
   * Obtener todos los campos configurados
   */
  async obtenerCampos(): Promise<ConfiguracionCampo[]> {
    try {
      const response = await api.get('/admin/configuracion/campos')
      return response.data
    } catch (error) {
      console.error('Error obteniendo campos:', error)
      throw error
    }
  }

  /**
   * Crear nuevo campo
   */
  async crearCampo(campo: Partial<ConfiguracionCampo>): Promise<any> {
    try {
      const response = await api.post('/admin/configuracion/campos', campo)
      return response.data
    } catch (error) {
      console.error('Error creando campo:', error)
      throw error
    }
  }

  /**
   * Editar campo existente
   */
  async editarCampo(id: number, campo: Partial<ConfiguracionCampo>): Promise<any> {
    try {
      const response = await api.put(`/admin/configuracion/campos/${id}`, campo)
      return response.data
    } catch (error) {
      console.error('Error editando campo:', error)
      throw error
    }
  }

  /**
   * Eliminar campo
   */
  async eliminarCampo(id: number): Promise<any> {
    try {
      const response = await api.delete(`/admin/configuracion/campos/${id}`)
      return response.data
    } catch (error) {
      console.error('Error eliminando campo:', error)
      throw error
    }
  }

  /**
   * Obtener todas las integraciones API
   */
  async obtenerIntegraciones(): Promise<IntegracionAPI[]> {
    try {
      const response = await api.get('/admin/integraciones-api')
      return response.data
    } catch (error) {
      console.error('Error obteniendo integraciones:', error)
      throw error
    }
  }

  /**
   * Crear nueva integración API
   */
  async crearIntegracion(integracion: Partial<IntegracionAPI>): Promise<any> {
    try {
      const response = await api.post('/admin/integraciones-api', integracion)
      return response.data
    } catch (error) {
      console.error('Error creando integración:', error)
      throw error
    }
  }

  /**
   * Editar integración API
   */
  async editarIntegracion(id: number, integracion: Partial<IntegracionAPI>): Promise<any> {
    try {
      const response = await api.put(`/admin/integraciones-api/${id}`, integracion)
      return response.data
    } catch (error) {
      console.error('Error editando integración:', error)
      throw error
    }
  }

  /**
   * Eliminar integración API
   */
  async eliminarIntegracion(id: number): Promise<any> {
    try {
      const response = await api.delete(`/admin/integraciones-api/${id}`)
      return response.data
    } catch (error) {
      console.error('Error eliminando integración:', error)
      throw error
    }
  }

  /**
   * Probar integración API
   */
  async probarIntegracion(id: number): Promise<ResultadoProeba> {
    try {
      const response = await api.post(`/admin/integraciones-api/${id}/probar`)
      return response.data
    } catch (error) {
      console.error('Error probando integración:', error)
      throw error
    }
  }

  /**
   * Obtener estadísticas de consultas
   */
  async obtenerEstadisticas(): Promise<any> {
    try {
      const response = await api.get('/admin/estadisticas/consultas')
      return response.data
    } catch (error) {
      console.error('Error obteniendo estadísticas:', error)
      throw error
    }
  }
}

export const configuracionService = new ConfiguracionService()
