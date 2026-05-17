<template>
  <div class="elecciones-container">
    <!-- Header -->
    <div class="view-header">
      <h2>Elecciones y Votaciones</h2>
      <button class="btn-primary" @click="showModalCrear = true">
        <ion-icon name="add-outline"></ion-icon> Nueva Elección
      </button>
    </div>

    <!-- Alert -->
    <div v-if="alert.visible" :class="['alert', `alert-${alert.type}`]">
      {{ alert.message }}
      <button @click="alert.visible = false" class="alert-close">
        <ion-icon name="close-outline"></ion-icon>
      </button>
    </div>

    <!-- Tabs de filtro -->
    <div class="filter-tabs">
      <button
        v-for="tab in estadoTabs"
        :key="tab.key"
        :class="['tab-btn', { active: filtroEstado === tab.key }]"
        @click="filtroEstado = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Tabla de elecciones -->
    <div class="table-container">
      <table class="elecciones-table">
        <thead>
          <tr>
            <th>Título</th>
            <th>Tipo</th>
            <th>Estado</th>
            <th>Opciones</th>
            <th>Votos</th>
            <th>Fechas</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="eleccion in eleccionesFiltradas" :key="eleccion.id" class="eleccion-row">
            <td class="titulo-col">
              <strong>{{ eleccion.titulo }}</strong>
              <p v-if="eleccion.descripcion" class="desc">{{ eleccion.descripcion }}</p>
            </td>
            <td>
              <span :class="['badge', `badge-${eleccion.tipo}`]">
                {{ eleccion.tipo === 'cargo' ? 'Cargo' : 'Acuerdo' }}
              </span>
            </td>
            <td>
              <span :class="['estado-badge', `estado-${eleccion.estado}`]">
                {{ estadoLabel(eleccion.estado) }}
              </span>
            </td>
            <td class="center">{{ eleccion.opciones.length }}</td>
            <td class="center">{{ eleccion.total_votos }}</td>
            <td class="dates">
              <small>
                <span v-if="eleccion.fecha_inicio">Inicia: {{ formatFecha(eleccion.fecha_inicio) }}</span>
                <span v-if="eleccion.fecha_fin">Cierra: {{ formatFecha(eleccion.fecha_fin) }}</span>
              </small>
            </td>
            <td class="acciones">
              <button class="btn-icon" @click="irADetalle(eleccion.id)" title="Gestionar">
                <ion-icon name="pencil-outline"></ion-icon>
              </button>
              <button
                v-if="eleccion.estado === 'borrador'"
                class="btn-icon"
                @click="cambiarEstado(eleccion, 'activo')"
                title="Activar"
              >
                <ion-icon name="play-outline"></ion-icon>
              </button>
              <button
                v-if="eleccion.estado === 'activo'"
                class="btn-icon"
                @click="cambiarEstado(eleccion, 'cerrado')"
                title="Cerrar"
              >
                <ion-icon name="stop-outline"></ion-icon>
              </button>
              <button
                v-if="eleccion.estado !== 'borrador'"
                class="btn-icon"
                @click="irAResultados(eleccion)"
                title="Ver resultados"
              >
                <ion-icon name="bar-chart-outline"></ion-icon>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="!eleccionesFiltradas.length" class="empty-state">
        <ion-icon name="checkmark-circle-outline"></ion-icon>
        <p>No hay elecciones en estado {{ filtroEstado }}</p>
      </div>
    </div>

    <!-- Modal crear elección -->
    <div v-if="showModalCrear" class="modal-overlay" @click.self="showModalCrear = false">
      <div class="modal">
        <div class="modal-header">
          <h3>Nueva Elección</h3>
          <button @click="showModalCrear = false" class="close-btn">
            <ion-icon name="close-outline"></ion-icon>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Título *</label>
            <input
              v-model="formNueva.titulo"
              type="text"
              placeholder="Ej: Elección de Presidente"
            />
          </div>
          <div class="form-group">
            <label>Descripción</label>
            <textarea
              v-model="formNueva.descripcion"
              rows="3"
              placeholder="Descripción de la elección..."
            ></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Tipo *</label>
              <select v-model="formNueva.tipo">
                <option value="cargo">Cargo</option>
                <option value="acuerdo">Acuerdo</option>
              </select>
            </div>
            <div class="form-group">
              <label>Resultados públicos</label>
              <label class="checkbox-label">
                <input v-model="formNueva.resultados_publicos" type="checkbox" />
                <span>Mostrar en vivo</span>
              </label>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Fecha inicio</label>
              <input v-model="formNueva.fecha_inicio" type="datetime-local" />
            </div>
            <div class="form-group">
              <label>Fecha fin</label>
              <input v-model="formNueva.fecha_fin" type="datetime-local" />
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="showModalCrear = false">Cancelar</button>
          <button class="btn-primary" @click="crearEleccion" :disabled="creando">
            <span v-if="!creando">Crear Elección</span>
            <span v-else><ion-icon name="hourglass-outline"></ion-icon> Creando...</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import eleccionesService from '@/services/elecciones.service'

const router = useRouter()

const elecciones = ref([])
const filtroEstado = ref('todos')
const showModalCrear = ref(false)
const creando = ref(false)
const alert = ref({ visible: false, type: '', message: '' })

const estadoTabs = [
  { key: 'todos', label: 'Todas' },
  { key: 'borrador', label: 'Borradores' },
  { key: 'activo', label: 'Activas' },
  { key: 'cerrado', label: 'Cerradas' },
]

const formNueva = ref({
  titulo: '',
  descripcion: '',
  tipo: 'cargo',
  fecha_inicio: '',
  fecha_fin: '',
  resultados_publicos: false,
})

const eleccionesFiltradas = computed(() => {
  if (filtroEstado.value === 'todos') return elecciones.value
  return elecciones.value.filter(e => e.estado === filtroEstado.value)
})

const estadoLabel = (estado) => {
  const labels = { borrador: 'Borrador', activo: 'Activa', cerrado: 'Cerrada' }
  return labels[estado] || estado
}

const formatFecha = (fecha) => {
  if (!fecha) return ''
  const d = new Date(fecha)
  return d.toLocaleDateString('es-ES') + ' ' + d.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
}

async function cargarElecciones() {
  try {
    elecciones.value = await eleccionesService.listarElecciones()
  } catch (err) {
    console.error('Error cargando elecciones:', err)
  }
}

async function crearEleccion() {
  if (!formNueva.value.titulo.trim()) {
    alert.value = { visible: true, type: 'error', message: 'El título es obligatorio' }
    return
  }

  creando.value = true
  try {
    await eleccionesService.crearEleccion(formNueva.value)
    alert.value = { visible: true, type: 'success', message: 'Elección creada correctamente' }
    showModalCrear.value = false
    formNueva.value = {
      titulo: '',
      descripcion: '',
      tipo: 'cargo',
      fecha_inicio: '',
      fecha_fin: '',
      resultados_publicos: false,
    }
    await cargarElecciones()
  } catch (err) {
    alert.value = { visible: true, type: 'error', message: err.response?.data?.detail || 'Error creando elección' }
  } finally {
    creando.value = false
  }
}

async function cambiarEstado(eleccion, nuevoEstado) {
  if (!confirm(`¿Cambiar a ${estadoLabel(nuevoEstado)}?`)) return

  try {
    await eleccionesService.cambiarEstado(eleccion.id, nuevoEstado)
    alert.value = { visible: true, type: 'success', message: `Estado actualizado a ${estadoLabel(nuevoEstado)}` }
    await cargarElecciones()
  } catch (err) {
    alert.value = { visible: true, type: 'error', message: err.response?.data?.detail || 'Error actualizando estado' }
  }
}

function irADetalle(id) {
  router.push(`/elecciones/${id}`)
}

function irAResultados(eleccion) {
  router.push({ path: `/elecciones/${eleccion.id}`, query: { tab: 'resultados' } })
}

onMounted(() => {
  console.log('[EleccionesView mounted]')
  console.log('[EleccionesView] localStorage keys:', Object.keys(localStorage))
  console.log('[EleccionesView] localStorage auth_token:', localStorage.getItem('auth_token') ? localStorage.getItem('auth_token').substring(0, 20) + '...' : 'NULL')
  cargarElecciones()
})
</script>

<style scoped>
.elecciones-container {
  padding: 0;
  background: transparent;
  border-radius: 0;
  margin: 0;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  gap: 16px;
}

.view-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
  font-family: inherit;
}

.btn-primary:hover {
  background: #4f46e5;
}

.btn-secondary {
  padding: 10px 20px;
  background: #e2e8f0;
  color: #1e293b;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: #cbd5e1;
}

.alert {
  padding: 14px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.alert-success {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #15803d;
}

.alert-error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
}

.alert-close {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 18px;
}

.filter-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.tab-btn {
  padding: 8px 16px;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  color: #64748b;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn.active {
  background: #6366f1;
  color: white;
  border-color: #6366f1;
}

.tab-btn:hover {
  border-color: #6366f1;
  color: #6366f1;
}

.table-container {
  overflow-x: auto;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.elecciones-table {
  width: 100%;
  border-collapse: collapse;
}

.elecciones-table thead {
  background: #f8fafc;
}

.elecciones-table th {
  padding: 12px 16px;
  text-align: left;
  font-weight: 700;
  color: #64748b;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.elecciones-table td {
  padding: 14px 16px;
  border-top: 1px solid #e2e8f0;
  font-size: 14px;
  color: #475569;
}

.eleccion-row:hover {
  background: #f8fafc;
}

.titulo-col {
  max-width: 250px;
}

.titulo-col strong {
  display: block;
  color: #1e293b;
  margin-bottom: 4px;
}

.desc {
  font-size: 12px;
  color: #94a3b8;
  margin: 0;
}

.badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.badge-cargo {
  background: #dbeafe;
  color: #1d4ed8;
}

.badge-acuerdo {
  background: #fef3c7;
  color: #92400e;
}

.estado-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.estado-borrador {
  background: #f3f4f6;
  color: #6b7280;
}

.estado-activo {
  background: #dcfce7;
  color: #15803d;
}

.estado-cerrado {
  background: #fee2e2;
  color: #991b1b;
}

.center {
  text-align: center;
}

.dates {
  font-size: 12px;
  color: #94a3b8;
}

.dates small {
  display: block;
  line-height: 1.5;
}

.acciones {
  display: flex;
  gap: 6px;
}

.btn-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: white;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  font-size: 16px;
}

.btn-icon:hover {
  background: #eef2ff;
  color: #6366f1;
  border-color: #c7d2fe;
}

.empty-state {
  text-align: center;
  padding: 48px 24px;
  color: #94a3b8;
}

.empty-state ion-icon {
  font-size: 48px;
  margin-bottom: 16px;
  display: block;
  color: #cbd5e1;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
}

.close-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  font-size: 24px;
}

.modal-body {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  color: #1e293b;
  transition: border 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 400;
  cursor: pointer;
}

.checkbox-label input {
  width: 18px;
  height: 18px;
  cursor: pointer;
  margin: 0;
}

.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding: 16px 24px;
  border-top: 1px solid #e2e8f0;
}

.btn-primary:disabled,
.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .view-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .modal {
    width: 95%;
    max-width: none;
  }
}
</style>
