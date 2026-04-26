<template>
  <div class="cobranza-container">
    <!-- Tabs -->
    <div class="cobranza-tabs">
      <button
        :class="['tab', { active: tab === 'conceptos' }]"
        @click="tab = 'conceptos'"
      >
        <ion-icon name="document-text-outline"></ion-icon>
        Conceptos de Pago
      </button>
      <button
        :class="['tab', { active: tab === 'cuotas' }]"
        @click="tab = 'cuotas'"
      >
        <ion-icon name="receipt-outline"></ion-icon>
        Cuotas
      </button>
      <button
        :class="['tab', { active: tab === 'pagos' }]"
        @click="tab = 'pagos'"
      >
        <ion-icon name="card-outline"></ion-icon>
        Pagos
      </button>
    </div>

    <!-- Tab: Conceptos de Pago -->
    <div v-if="tab === 'conceptos'" class="tab-content">
      <div class="section-header">
        <h2>Conceptos de Pago</h2>
        <button @click="mostrarModalConcepto = true" class="btn-primary">
          <ion-icon name="add-outline"></ion-icon>
          Nuevo Concepto
        </button>
      </div>

      <div class="conceptos-grid">
        <div v-for="concepto in conceptos" :key="concepto.id" class="concepto-card">
          <div class="concepto-header">
            <h3>{{ concepto.nombre }}</h3>
            <span :class="['badge', concepto.activo ? 'activo' : 'inactivo']">
              {{ concepto.activo ? 'Activo' : 'Inactivo' }}
            </span>
          </div>
          <div class="concepto-info">
            <p><strong>Monto:</strong> {{ formatearMoneda(concepto.monto) }}</p>
            <p><strong>Tipo:</strong> {{ concepto.tipo }}</p>
            <p><strong>Recurrencia:</strong> {{ concepto.recurrencia }}</p>
          </div>
          <div class="concepto-actions">
            <button @click="editarConcepto(concepto)" class="btn-icon">
              <ion-icon name="pencil-outline"></ion-icon>
            </button>
            <button @click="eliminarConcepto(concepto.id)" class="btn-icon danger">
              <ion-icon name="trash-outline"></ion-icon>
            </button>
          </div>
        </div>
      </div>

      <!-- Modal Crear/Editar Concepto -->
      <div v-if="mostrarModalConcepto" class="modal-overlay" @click.self="mostrarModalConcepto = false">
        <div class="modal-contenedor modal-grande">
          <div class="modal-header">
            <h2>{{ conceptoEditando ? 'Editar' : 'Nuevo' }} Concepto de Pago</h2>
            <button @click="mostrarModalConcepto = false" class="btn-close">
              <ion-icon name="close-outline"></ion-icon>
            </button>
          </div>
          <div class="modal-body">
            <div class="grid-2">
              <div class="form-group">
                <label>Nombre *</label>
                <input v-model="formularioConcepto.nombre" type="text" placeholder="Ej: Cuota Mensual">
              </div>
              <div class="form-group">
                <label>Monto *</label>
                <input v-model.number="formularioConcepto.monto" type="number" placeholder="0.00">
              </div>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label>Tipo *</label>
                <select v-model="formularioConcepto.tipo">
                  <option value="cuota">Cuota (Recurrente)</option>
                  <option value="multa">Multa (Una sola vez)</option>
                  <option value="derecho">Derecho (Una sola vez)</option>
                </select>
              </div>
              <div class="form-group">
                <label>Recurrencia *</label>
                <select v-model="formularioConcepto.recurrencia">
                  <option value="diario">Diario</option>
                  <option value="semanal">Semanal</option>
                  <option value="mensual">Mensual</option>
                  <option value="bimestral">Bimestral</option>
                  <option value="trimestral">Trimestral</option>
                  <option value="semestral">Semestral</option>
                  <option value="anual">Anual</option>
                </select>
              </div>
            </div>

            <div v-if="formularioConcepto.tipo === 'cuota'" class="grid-2">
              <div class="form-group">
                <label>Día de Cobro (1-31, 0=Último día)</label>
                <input v-model.number="formularioConcepto.dia_cobro" type="number" min="0" max="31">
              </div>
              <div class="form-group">
                <label>Cada cuántos períodos</label>
                <input v-model.number="formularioConcepto.cada_n_periodos" type="number" min="1">
              </div>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label>Fecha Inicio *</label>
                <input v-model="formularioConcepto.fecha_inicio" type="date">
              </div>
              <div class="form-group">
                <label>Fecha Fin (Opcional)</label>
                <input v-model="formularioConcepto.fecha_fin" type="date">
              </div>
            </div>

            <div class="form-group">
              <label>Descripción</label>
              <textarea v-model="formularioConcepto.descripcion" placeholder="Descripción del concepto"></textarea>
            </div>

            <div class="modal-actions">
              <button @click="mostrarModalConcepto = false" class="btn-secondary">Cancelar</button>
              <button @click="guardarConcepto" class="btn-primary" :disabled="cargandoConcepto">
                {{ cargandoConcepto ? 'Guardando...' : 'Guardar' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab: Cuotas -->
    <div v-if="tab === 'cuotas'" class="tab-content">
      <div class="section-header">
        <h2>Cuotas del Sistema</h2>
        <div class="filter-group">
          <select v-model="filtroEstadoCuota" class="filter-select">
            <option value="">Todos los estados</option>
            <option value="pendiente">Pendiente</option>
            <option value="pagada">Pagada</option>
            <option value="vencida">Vencida</option>
          </select>
        </div>
      </div>

      <div class="tabla-responsiva">
        <table class="cuotas-tabla">
          <thead>
            <tr>
              <th>Usuario</th>
              <th>Concepto</th>
              <th>Monto</th>
              <th>Vencimiento</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cuota in cuotasFiltradas" :key="cuota.id">
              <td>{{ cuota.usuario_nombre }}</td>
              <td>{{ cuota.concepto }}</td>
              <td>{{ formatearMoneda(cuota.monto) }}</td>
              <td>{{ formatearFecha(cuota.fecha_vencimiento) }}</td>
              <td><span :class="['badge', cuota.estado]">{{ cuota.estado }}</span></td>
              <td>
                <button class="btn-icon" title="Ver detalles">
                  <ion-icon name="eye-outline"></ion-icon>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tab: Pagos -->
    <div v-if="tab === 'pagos'" class="tab-content">
      <div class="section-header">
        <h2>Pagos Registrados</h2>
        <div class="filter-group">
          <select v-model="filtroEstadoPago" class="filter-select">
            <option value="">Todos los estados</option>
            <option value="pendiente_aprobacion">Pendiente Aprobación</option>
            <option value="aprobado">Aprobado</option>
            <option value="rechazado">Rechazado</option>
          </select>
        </div>
      </div>

      <div class="tabla-responsiva">
        <table class="pagos-tabla">
          <thead>
            <tr>
              <th>Usuario</th>
              <th>Monto</th>
              <th>Método</th>
              <th>Estado</th>
              <th>Fecha</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="pago in pagosFiltrados" :key="pago.id">
              <td>{{ pago.usuario_nombre }}</td>
              <td>{{ formatearMoneda(pago.monto) }}</td>
              <td>{{ pago.metodo_pago }}</td>
              <td><span :class="['badge', pago.estado]">{{ pago.estado }}</span></td>
              <td>{{ formatearFecha(pago.created_at) }}</td>
              <td>
                <button
                  v-if="pago.estado === 'pendiente_aprobacion'"
                  @click="aprobarPago(pago.id)"
                  class="btn-icon success"
                  title="Aprobar"
                >
                  <ion-icon name="checkmark-circle-outline"></ion-icon>
                </button>
                <button
                  v-if="pago.estado === 'pendiente_aprobacion'"
                  @click="rechazarPago(pago.id)"
                  class="btn-icon danger"
                  title="Rechazar"
                >
                  <ion-icon name="close-circle-outline"></ion-icon>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../services/api'

const tab = ref('conceptos')
const conceptos = ref([])
const cuotas = ref([])
const pagos = ref([])

const mostrarModalConcepto = ref(false)
const conceptoEditando = ref(null)
const cargandoConcepto = ref(false)

const filtroEstadoCuota = ref('')
const filtroEstadoPago = ref('')

const formularioConcepto = ref({
  nombre: '',
  descripcion: '',
  monto: 0,
  tipo: 'cuota',
  recurrencia: 'mensual',
  dia_cobro: 1,
  cada_n_periodos: 1,
  fecha_inicio: new Date().toISOString().split('T')[0],
  fecha_fin: null
})

const cuotasFiltradas = computed(() => {
  if (!filtroEstadoCuota.value) return cuotas.value
  return cuotas.value.filter(c => c.estado === filtroEstadoCuota.value)
})

const pagosFiltrados = computed(() => {
  if (!filtroEstadoPago.value) return pagos.value
  return pagos.value.filter(p => p.estado === filtroEstadoPago.value)
})

const formatearMoneda = (monto) => {
  return new Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN' }).format(monto)
}

const formatearFecha = (fecha) => {
  return new Date(fecha).toLocaleDateString('es-PE')
}

const cargarConceptos = async () => {
  try {
    const res = await api.get('/cobranza/conceptos/')
    conceptos.value = res.data.data || []
  } catch (error) {
    console.error('Error cargando conceptos:', error)
  }
}

const cargarCuotas = async () => {
  try {
    const res = await api.get('/cobranza/cuotas/')
    cuotas.value = res.data.data || []
  } catch (error) {
    console.error('Error cargando cuotas:', error)
  }
}

const cargarPagos = async () => {
  try {
    const res = await api.get('/cobranza/pagos/')
    pagos.value = res.data.data || []
  } catch (error) {
    console.error('Error cargando pagos:', error)
  }
}

const guardarConcepto = async () => {
  cargandoConcepto.value = true
  try {
    if (conceptoEditando.value) {
      // Editar
      await api.put(`/cobranza/conceptos/${conceptoEditando.value.id}`, formularioConcepto.value)
    } else {
      // Crear
      await api.post('/cobranza/conceptos/', formularioConcepto.value)
    }
    mostrarModalConcepto.value = false
    cargarConceptos()
  } catch (error) {
    console.error('Error guardando concepto:', error)
  } finally {
    cargandoConcepto.value = false
  }
}

const editarConcepto = (concepto) => {
  conceptoEditando.value = concepto
  formularioConcepto.value = { ...concepto }
  mostrarModalConcepto.value = true
}

const eliminarConcepto = async (id) => {
  if (!confirm('¿Eliminar este concepto?')) return
  try {
    await api.delete(`/cobranza/conceptos/${id}`)
    cargarConceptos()
  } catch (error) {
    console.error('Error eliminando:', error)
  }
}

const aprobarPago = async (id) => {
  try {
    await api.put(`/cobranza/pagos/${id}/aprobar`)
    cargarPagos()
  } catch (error) {
    console.error('Error aprobando pago:', error)
  }
}

const rechazarPago = async (id) => {
  const motivo = prompt('Motivo del rechazo:')
  if (!motivo) return
  try {
    await api.put(`/cobranza/pagos/${id}/rechazar?motivo=${encodeURIComponent(motivo)}`)
    cargarPagos()
  } catch (error) {
    console.error('Error rechazando pago:', error)
  }
}

onMounted(() => {
  cargarConceptos()
  cargarCuotas()
  cargarPagos()
})
</script>

<style scoped>
.cobranza-container {
  padding: 0;
}

.cobranza-tabs {
  display: flex;
  gap: 0;
  border-bottom: 1px solid #e2e8f0;
  background: white;
  border-radius: 8px 8px 0 0;
  overflow: hidden;
}

.tab {
  flex: 1;
  padding: 12px 16px;
  border: none;
  background: #f8fafc;
  cursor: pointer;
  font-weight: 500;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
}

.tab:hover { background: #f1f5f9; }
.tab.active {
  background: white;
  color: #4f46e5;
  border-bottom: 2px solid #4f46e5;
}

.tab-content {
  background: white;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header h2 {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
}

.filter-group {
  display: flex;
  gap: 8px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  background: white;
  cursor: pointer;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover { background: #4338ca; }

/* Conceptos Grid */
.conceptos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.concepto-card {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
  background: #f8fafc;
  transition: all 0.2s;
}

.concepto-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.concepto-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 12px;
}

.concepto-header h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.badge.activo {
  background: #dcfce7;
  color: #166534;
}

.badge.inactivo {
  background: #fee2e2;
  color: #991b1b;
}

.concepto-info {
  margin-bottom: 12px;
}

.concepto-info p {
  font-size: 14px;
  color: #64748b;
  margin: 4px 0;
}

.concepto-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  color: #64748b;
  padding: 4px;
  display: flex;
  align-items: center;
  font-size: 18px;
  transition: color 0.2s;
}

.btn-icon:hover { color: #4f46e5; }
.btn-icon.danger:hover { color: #dc2626; }

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-contenedor {
  background: white;
  border-radius: 12px;
  max-height: 90vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-grande { max-width: 600px; }

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h2 {
  font-size: 18px;
  font-weight: 700;
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  color: #64748b;
  font-size: 20px;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 6px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
}

.form-group textarea {
  min-height: 80px;
  resize: vertical;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.btn-secondary {
  padding: 10px 16px;
  background: #f1f5f9;
  color: #1e293b;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}

/* Tablas */
.tabla-responsiva {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

th {
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: #64748b;
  font-size: 13px;
}

td {
  padding: 12px 16px;
  border-bottom: 1px solid #e2e8f0;
  font-size: 14px;
}

tbody tr:hover { background: #f8fafc; }

.badge.pendiente { background: #fef3c7; color: #92400e; }
.badge.pagada { background: #dcfce7; color: #166534; }
.badge.vencida { background: #fee2e2; color: #991b1b; }
.badge.pendiente_aprobacion { background: #fef3c7; color: #92400e; }
.badge.aprobado { background: #dcfce7; color: #166534; }
.badge.rechazado { background: #fee2e2; color: #991b1b; }

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .conceptos-grid {
    grid-template-columns: 1fr;
  }

  .grid-2 { grid-template-columns: 1fr; }

  .modal-overlay { padding: 0; }
  .modal-contenedor {
    border-radius: 16px 16px 0 0;
    max-height: 95vh;
  }
}
</style>
