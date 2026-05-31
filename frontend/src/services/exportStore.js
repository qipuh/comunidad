import { reactive } from 'vue'

export const exportStore = reactive({
  taskId: null,
  estado: null,       // 'procesando' | 'completada' | 'cancelada' | 'error'
  progreso: 0,
  mensaje: '',
  totalCarnets: 0,
  pollingInterval: null,

  activo() {
    return this.taskId && (this.estado === 'procesando' || this.estado === 'pendiente')
  },

  reset() {
    if (this.pollingInterval) clearInterval(this.pollingInterval)
    this.taskId = null
    this.estado = null
    this.progreso = 0
    this.mensaje = ''
    this.totalCarnets = 0
    this.pollingInterval = null
  }
})
