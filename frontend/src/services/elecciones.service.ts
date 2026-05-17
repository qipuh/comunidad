import api from './api'

const ELECCIONES_ENDPOINT = '/elecciones/'

export const eleccionesService = {
  async listarElecciones(estado?: string, tipo?: string) {
    try {
      const response = await api.get(ELECCIONES_ENDPOINT, {
        params: { estado, tipo }
      })
      return response.data
    } catch (error) {
      console.error('Error listando elecciones:', error)
      throw error
    }
  },

  async obtenerEleccion(eleccionId: number) {
    try {
      const response = await api.get(`/elecciones/${eleccionId}`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo elección:', error)
      throw error
    }
  },

  async crearEleccion(datos: any) {
    try {
      const response = await api.post(ELECCIONES_ENDPOINT, datos)
      return response.data
    } catch (error) {
      console.error('Error creando elección:', error)
      throw error
    }
  },

  async cambiarEstado(eleccionId: number, estado: string) {
    try {
      const response = await api.put(`/elecciones/${eleccionId}/estado`, { estado })
      return response.data
    } catch (error) {
      console.error('Error cambiando estado:', error)
      throw error
    }
  },

  async agregarOpcion(eleccionId: number, datos: any) {
    try {
      const response = await api.post(`/elecciones/${eleccionId}/opciones`, datos)
      return response.data
    } catch (error) {
      console.error('Error agregando opción:', error)
      throw error
    }
  },

  async eliminarOpcion(eleccionId: number, opcionId: number) {
    try {
      const response = await api.delete(`/elecciones/${eleccionId}/opciones/${opcionId}`)
      return response.data
    } catch (error) {
      console.error('Error eliminando opción:', error)
      throw error
    }
  },

  async votar(eleccionId: number, datos: any) {
    try {
      const response = await api.post(`/elecciones/${eleccionId}/votar`, datos)
      return response.data
    } catch (error) {
      console.error('Error votando:', error)
      throw error
    }
  },

  async obtenerResultados(eleccionId: number) {
    try {
      const response = await api.get(`/elecciones/${eleccionId}/resultados`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo resultados:', error)
      throw error
    }
  }
}

export default eleccionesService
