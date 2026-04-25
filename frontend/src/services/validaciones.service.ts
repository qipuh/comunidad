/**
 * Servicio para consultar APIs externas desde el frontend
 *
 * Endpoints:
 * - POST /api/validaciones/consultar-dni
 * - POST /api/validaciones/consultar-ruc
 * - GET /api/validaciones/historial/{usuario_id}
 */

import { api } from './api'

export interface ResultadoValidacion {
  exitosa: boolean
  datos?: Record<string, any>
  validado_externamente: boolean
  fuente?: string
  error?: string
}

export interface HistorialConsulta {
  id: number
  tipo_consulta: string
  parametro: string
  integracion: string
  estado: string
  fecha: string
  campos_obtenidos: string[]
  error?: string
}

class ValidacionesService {
  /**
   * Consultar RENIEC por DNI
   *
   * @param dni Número de documento (8 dígitos)
   * @returns Datos de la persona si existe
   */
  async consultarDNI(dni: string): Promise<ResultadoValidacion> {
    try {
      if (!dni.match(/^\d{8}$/)) {
        return {
          exitosa: false,
          validado_externamente: false,
          error: 'DNI debe ser 8 dígitos'
        }
      }

      const response = await api.post('/validaciones/consultar-dni', { dni })
      return response.data
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Error al consultar RENIEC'
      console.error('Error consultando DNI:', errorMsg)
      return {
        exitosa: false,
        validado_externamente: false,
        error: errorMsg
      }
    }
  }

  /**
   * Consultar Facturiza por RUC
   *
   * @param ruc Número de RUC (11 dígitos)
   * @returns Datos de la empresa si existe
   */
  async consultarRUC(ruc: string): Promise<ResultadoValidacion> {
    try {
      if (!ruc.match(/^\d{11}$/)) {
        return {
          exitosa: false,
          validado_externamente: false,
          error: 'RUC debe ser 11 dígitos'
        }
      }

      const response = await api.post('/validaciones/consultar-ruc', { ruc })
      return response.data
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Error al consultar Facturiza'
      console.error('Error consultando RUC:', errorMsg)
      return {
        exitosa: false,
        validado_externamente: false,
        error: errorMsg
      }
    }
  }

  /**
   * Obtener historial de consultas de un usuario
   *
   * @param usuarioId ID del usuario
   * @returns Historial de consultas realizadas
   */
  async obtenerHistorial(usuarioId: number): Promise<HistorialConsulta[]> {
    try {
      const response = await api.get(`/validaciones/historial/${usuarioId}`)
      return response.data.consultas || []
    } catch (error: any) {
      console.error('Error obteniendo historial:', error)
      return []
    }
  }

  /**
   * Probar si RENIEC está disponible
   */
  async probarRENIEC(): Promise<boolean> {
    try {
      const response = await api.get('/validaciones/probar-reniec')
      return response.data.disponible === true
    } catch (error) {
      console.error('Error probando RENIEC:', error)
      return false
    }
  }

  /**
   * Probar si Facturiza está disponible
   */
  async probarFacturiza(): Promise<boolean> {
    try {
      const response = await api.get('/validaciones/probar-facturiza')
      return response.data.disponible === true
    } catch (error) {
      console.error('Error probando Facturiza:', error)
      return false
    }
  }

  /**
   * Mapear nombre de campo API a campo local
   * Utilidad para auto-llenar formularios
   */
  mapearCampoAPI(campoAPI: string): string | null {
    const mapeo: Record<string, string> = {
      'nombre': 'nombre',
      'nombres': 'nombre',
      'apellido_paterno': 'apellido_paterno',
      'apellido_materno': 'apellido_materno',
      'razon_social': 'razon_social',
      'direccion': 'direccion',
      'genero': 'genero',
      'fecha_nacimiento': 'fecha_nacimiento',
      'estado_civil': 'estado_civil',
      'representante_legal': 'representante_legal',
      'actividad_economica': 'actividad_economica',
      'estado_contribuyente': 'estado_contribuyente'
    }
    return mapeo[campoAPI] || null
  }
}

export const validacionesService = new ValidacionesService()
