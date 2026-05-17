<template>
  <div class="perfil-container">
    <!-- Loading -->
    <div v-if="cargando" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Cargando perfil...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="error-state">
      <ion-icon name="alert-circle-outline"></ion-icon>
      <h3>Usuario no encontrado</h3>
      <p>{{ error }}</p>
      <router-link to="/usuarios" class="btn-back">← Volver a Usuarios</router-link>
    </div>

    <template v-else-if="usuario">
      <!-- Compact Header -->
      <div class="perfil-header">
        <router-link to="/usuarios" class="btn-back">
          <ion-icon name="arrow-back-outline"></ion-icon>
        </router-link>
        <div class="header-content">
          <div class="header-avatar">
            <img v-if="usuario.foto_frontal" :src="'/' + usuario.foto_frontal" :alt="usuario.nombre_completo">
            <span v-else>{{ iniciales }}</span>
          </div>
          <div class="header-info">
            <h1>{{ usuario.nombre_completo }}</h1>
            <div class="header-badges">
              <span class="badge" :class="usuario.estado">{{ usuario.estado }}</span>
              <span class="badge">{{ usuario.rol === 'admin' ? '👤 Admin' : '👤 Usuario' }}</span>
            </div>
            <div class="header-details">
              <span class="detail-item">
                <span class="detail-label">Usuario:</span>
                <span class="detail-value">{{ usuario.username }}</span>
              </span>
              <span class="detail-item">
                <span class="detail-label">Rol:</span>
                <span class="detail-value">{{ usuario.rol === 'admin' ? 'Admin' : 'Usuario' }}</span>
              </span>
              <span class="detail-item">
                <span class="detail-label">Facial:</span>
                <span class="detail-value">{{ usuario.usar_reconocimiento_facial ? '✓ Activo' : '✗ Inactivo' }}</span>
              </span>
              <span class="detail-item">
                <span class="detail-label">Cobranza desde:</span>
                <span class="detail-value">{{ formatFechaCorta(usuario.fecha_inicio_cobranza) || '—' }}</span>
              </span>
            </div>
          </div>
          <div class="header-actions">
            <button @click="editarUsuario" class="btn-action">
              <ion-icon name="pencil-outline"></ion-icon>
            </button>
            <router-link :to="`/carnets?usuario=${usuario.id}`" class="btn-action">
              <ion-icon name="card-outline"></ion-icon>
            </router-link>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="perfil-tabs">
        <button
          :class="['tab', { active: tabActivo === 'informacion' }]"
          @click="tabActivo = 'informacion'"
        >
          <ion-icon name="person-outline"></ion-icon>
          Información
        </button>
        <button
          :class="['tab', { active: tabActivo === 'cobranza' }]"
          @click="tabActivo = 'cobranza'"
        >
          <ion-icon name="receipt-outline"></ion-icon>
          Cobranza
        </button>
        <button
          :class="['tab', { active: tabActivo === 'fotos' }]"
          @click="tabActivo = 'fotos'"
        >
          <ion-icon name="camera-outline"></ion-icon>
          Fotos
        </button>
      </div>

      <!-- Tab Content -->
      <div class="perfil-content">
        <!-- Información (consolidado) -->
        <div v-if="tabActivo === 'informacion'" class="tab-pane personal-dashboard">
          <!-- Grid Layout: 2 columns -->
          <div class="dashboard-grid">
            <!-- Left Column: Statistics -->
            <div class="grid-col">
              <!-- My Statistics Card -->
              <div class="dashboard-card">
                <h3 class="card-header">Asistencia</h3>
                <div class="stats-list">
                  <div class="stat-row" v-if="asistencia">
                    <span class="stat-name">Total</span>
                    <div class="stat-visual">
                      <div class="stat-bar" :style="{ width: '70%' }"></div>
                    </div>
                    <span class="stat-value">{{ asistencia.total_reuniones || 0 }}</span>
                  </div>
                  <div class="stat-row" v-if="asistencia">
                    <span class="stat-name">Presentes</span>
                    <div class="stat-visual">
                      <div class="stat-bar" :style="{ width: '85%', backgroundColor: '#10b981' }"></div>
                    </div>
                    <span class="stat-value success">{{ asistencia.asistencias || 0 }}</span>
                  </div>
                  <div class="stat-row" v-if="asistencia">
                    <span class="stat-name">Ausentes</span>
                    <div class="stat-visual">
                      <div class="stat-bar" :style="{ width: '30%', backgroundColor: '#ef4444' }"></div>
                    </div>
                    <span class="stat-value danger">{{ asistencia.inasistencias || 0 }}</span>
                  </div>
                  <div class="stat-row" v-if="asistencia">
                    <span class="stat-name">Promedio</span>
                    <div class="stat-visual">
                      <div class="stat-bar" :style="{ width: (asistencia.porcentaje || 0) + '%', backgroundColor: '#6366f1' }"></div>
                    </div>
                    <span class="stat-value primary">{{ asistencia.porcentaje || 0 }}%</span>
                  </div>
                </div>
              </div>

              <!-- My Information Card -->
              <div class="dashboard-card">
                <h3 class="card-header">Información de Contacto</h3>
                <div class="info-cards-row">
                  <div class="mini-card">
                    <p class="mini-label">Email</p>
                    <p class="mini-value">{{ usuario.email }}</p>
                  </div>
                  <div class="mini-card">
                    <p class="mini-label">Teléfono</p>
                    <p class="mini-value">{{ usuario.telefono || '—' }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Right Column: Elections & Summary -->
            <div class="grid-col">
              <!-- My Elections Card -->
              <div class="dashboard-card">
                <h3 class="card-header">Elecciones</h3>
                <div v-if="eleccionesLoading" class="loading-mini">Cargando...</div>
                <div v-else-if="elecciones.length === 0" class="empty-elections">
                  <p>No ha participado en elecciones</p>
                </div>
                <div v-else class="elections-cards">
                  <div v-for="(eleccion, idx) in elecciones.slice(0, 3)" :key="eleccion.id"
                       class="election-card" :style="{ backgroundColor: getElectionColor(idx) }">
                    <div class="election-badge">
                      <span v-if="eleccion.voto_emitido" class="badge-check">✓</span>
                      <span v-else class="badge-pending">!</span>
                    </div>
                    <p class="election-name">{{ eleccion.nombre }}</p>
                    <p class="election-date">{{ formatFecha(eleccion.fecha) }}</p>
                  </div>
                </div>
              </div>

              <!-- Member Since Card -->
              <div class="dashboard-card summary-card">
                <div class="summary-icon">📅</div>
                <p class="summary-label">Miembro desde</p>
                <h2 class="summary-value">{{ formatFechaCorta(usuario.created_at) }}</h2>
                <p class="summary-detail">Rol: {{ usuario.rol === 'admin' ? 'Administrador' : 'Usuario' }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Cobranza (Cuotas) -->
        <div v-if="tabActivo === 'cobranza'" class="tab-pane">
          <div v-if="cuotas.length === 0" class="empty-state">
            <ion-icon name="document-outline"></ion-icon>
            <p>Sin cuotas asignadas</p>
          </div>
          <div v-else class="table-wrap">
            <table class="simple-table">
              <thead>
                <tr>
                  <th>Concepto</th>
                  <th class="center">#</th>
                  <th class="right">Monto</th>
                  <th>Vencimiento</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="c in cuotas" :key="c.id">
                  <td>{{ c.concepto }}</td>
                  <td class="center">{{ c.numero_cuota }}</td>
                  <td class="right fw600">S/. {{ Number(c.monto).toFixed(2) }}</td>
                  <td>{{ formatFecha(c.fecha_vencimiento) }}</td>
                  <td><span class="estado-badge" :class="c.estado">{{ c.estado }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Fotos Tab -->
        <div v-if="tabActivo === 'fotos'" class="tab-pane">
          <div v-if="!usuario.foto_frontal && !usuario.foto_lateral_izq && !usuario.foto_lateral_der" class="empty-state">
            <ion-icon name="camera-outline"></ion-icon>
            <p>Sin fotos de reconocimiento</p>
          </div>
          <div v-else class="fotos-gallery">
            <div class="foto-card" v-if="usuario.foto_frontal">
              <img :src="'/' + usuario.foto_frontal" alt="Frontal">
              <span class="foto-label">Frontal</span>
            </div>
            <div class="foto-card" v-if="usuario.foto_lateral_izq">
              <img :src="'/' + usuario.foto_lateral_izq" alt="Lateral Izquierda">
              <span class="foto-label">Lateral Izq</span>
            </div>
            <div class="foto-card" v-if="usuario.foto_lateral_der">
              <img :src="'/' + usuario.foto_lateral_der" alt="Lateral Derecha">
              <span class="foto-label">Lateral Der</span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()
const cargando = ref(true)
const error = ref(null)
const usuario = ref(null)
const cuotas = ref([])
const tabActivo = ref('informacion')
const asistencia = ref(null)
const asistenciaLoading = ref(false)
const elecciones = ref([])
const eleccionesLoading = ref(false)
const operacionesPendientes = ref([])
const operacionesAprobadas = ref([])

const iniciales = computed(() => {
  if (!usuario.value?.nombre_completo) return 'U'
  return usuario.value.nombre_completo.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase()
})

const formatFecha = (fecha) => {
  if (!fecha) return '—'
  try {
    return new Date(fecha).toLocaleDateString('es-PE', { year: 'numeric', month: 'long', day: 'numeric' })
  } catch { return fecha }
}

const formatFechaCorta = (fecha) => {
  if (!fecha) return '—'
  try {
    return new Date(fecha).toLocaleDateString('es-PE', { year: 'numeric', month: 'long' })
  } catch { return fecha }
}

const editarUsuario = () => {
  router.push({ path: '/usuarios', query: { editar: usuario.value.id } })
}

const iconoTab = (tab) => {
  const iconos = {
    personal: 'person-outline',
    contacto: 'call-outline',
    sistema: 'settings-outline',
    cuotas: 'receipt-outline',
    fotos: 'camera-outline'
  }
  return iconos[tab] || 'help-outline'
}

const labelTab = (tab) => {
  const labels = {
    personal: 'Personal',
    contacto: 'Contacto',
    sistema: 'Sistema',
    cuotas: 'Cuotas',
    fotos: 'Fotos'
  }
  return labels[tab] || tab
}

const getElectionColor = (index) => {
  const colors = ['#6366f1', '#ec4899', '#f59e0b']
  return colors[index % colors.length]
}

const formatearMoneda = (monto) => {
  return new Intl.NumberFormat('es-PE', {
    style: 'currency',
    currency: 'PEN'
  }).format(monto)
}

const formatarFecha = (fecha) => {
  if (!fecha) return '—'
  const date = new Date(fecha)
  return date.toLocaleDateString('es-PE', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatoMetodo = (metodo) => {
  const metodos = {
    'efectivo': 'Efectivo',
    'transferencia': 'Transf.',
    'deposito': 'Depósito',
    'billetera_digital': 'Billetera'
  }
  return metodos[metodo] || metodo
}

const cargarAsistencia = async (usuarioId) => {
  asistenciaLoading.value = true
  try {
    const res = await api.get(`/reuniones/asistencia/${usuarioId}`)
    if (res.data?.success) {
      asistencia.value = res.data.data || {}
    }
  } catch (e) {
    console.error('Error cargando asistencia:', e)
  } finally {
    asistenciaLoading.value = false
  }
}

const cargarElecciones = async (usuarioId) => {
  eleccionesLoading.value = true
  try {
    const res = await api.get(`/elecciones/usuario/${usuarioId}`)
    if (res.data?.success) {
      elecciones.value = res.data.data || []
    }
  } catch (e) {
    console.error('Error cargando elecciones:', e)
  } finally {
    eleccionesLoading.value = false
  }
}

const cargarOperaciones = async (usuarioId) => {
  try {
    const resPendientes = await api.get(`/cobranza/pagos/usuario/${usuarioId}?estado=pendiente_aprobacion`)
    if (resPendientes.data?.success) {
      operacionesPendientes.value = resPendientes.data.data || []
    }

    const resAprobadas = await api.get(`/cobranza/pagos/usuario/${usuarioId}?estado=aprobado`)
    if (resAprobadas.data?.success) {
      operacionesAprobadas.value = resAprobadas.data.data || []
    }
  } catch (e) {
    console.error('Error cargando operaciones:', e)
  }
}

async function cargarUsuario() {
  const id = route.params.id
  cargando.value = true
  error.value = null
  try {
    const [resUsuario, resCuotas] = await Promise.allSettled([
      api.get(`/usuarios/${id}`),
      api.get(`/cobranza/cuotas/${id}`)
    ])
    if (resUsuario.status === 'fulfilled' && resUsuario.value.data?.success) {
      usuario.value = resUsuario.value.data.data
      cargarAsistencia(id)
      cargarElecciones(id)
      cargarOperaciones(id)
    } else {
      error.value = 'No se pudo cargar el usuario'
    }
    if (resCuotas.status === 'fulfilled' && resCuotas.value.data?.success) {
      cuotas.value = resCuotas.value.data.data || []
    }
  } catch (e) {
    error.value = e.message || 'Error de conexión'
  } finally {
    cargando.value = false
  }
}

onMounted(cargarUsuario)
</script>

<style scoped>
.perfil-container { display: flex; flex-direction: column; gap: 0; }

/* Loading / Error */
.loading-state, .error-state {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 12px; padding: 80px 20px; color: #64748b;
}
.loading-spinner {
  width: 40px; height: 40px; border: 3px solid #e2e8f0; border-top-color: #6366f1;
  border-radius: 50%; animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.error-state ion-icon { font-size: 48px; color: #f43f5e; }
.error-state h3 { font-size: 18px; color: #1e293b; margin: 0; }
.error-state p { font-size: 14px; margin: 0; }
.btn-back {
  display: inline-flex; align-items: center; justify-content: center;
  width: 40px; height: 40px; background: white; border: 1px solid #e2e8f0;
  border-radius: 10px; color: #64748b; cursor: pointer; transition: all 0.2s;
  text-decoration: none;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.btn-back:hover {
  background: #eef2ff;
  color: #4f46e5;
  border-color: #4f46e5;
}
.btn-back ion-icon { font-size: 20px; }

/* Header */
.perfil-header {
  background: white; border-bottom: none;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08); padding: 20px;
  display: flex; align-items: center; gap: 16px;
}

/* System Info Bar */
.system-info-bar {
  display: flex; gap: 24px; padding: 16px 20px; background: #f8fafc;
  border-bottom: none; flex-wrap: wrap;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.sys-item {
  display: flex; flex-direction: column; gap: 2px;
}
.sys-label {
  font-size: 10px; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.3px;
}
.sys-value {
  font-size: 12px; color: #1e293b; font-weight: 600;
}
.sys-value.mono { font-family: 'SF Mono', monospace; }
.sys-pill {
  display: inline-block; padding: 2px 6px; border-radius: 3px; font-size: 10px;
  font-weight: 700; text-transform: uppercase;
}
.sys-pill.admin { background: #eef2ff; color: #6366f1; }
.sys-pill.usuario, .sys-pill.user { background: #f0fdf4; color: #16a34a; }

@media (max-width: 768px) {
  .system-info-bar { gap: 12px; padding: 10px 16px; }
  .sys-item { gap: 1px; }
}
.header-content {
  display: flex; align-items: center; gap: 14px; flex: 1;
}
.header-avatar {
  width: 72px; height: 72px; border-radius: 16px; overflow: hidden; flex-shrink: 0;
  background: linear-gradient(135deg, #6366f1, #8b5cf6); display: flex;
  align-items: center; justify-content: center; font-size: 28px;
  font-weight: 800; color: white; border: none;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}
.header-avatar img { width: 100%; height: 100%; object-fit: cover; }
.header-info { flex: 1; }
.header-info h1 { font-size: 18px; font-weight: 700; margin: 0 0 6px; color: #1e293b; }
.header-badges { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px; }

.header-details {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  font-size: 12px;
}

.detail-item {
  display: flex;
  gap: 4px;
  align-items: center;
}

.detail-label {
  color: #94a3b8;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.detail-value {
  color: #1e293b;
  font-weight: 600;
}
.badge {
  padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.3px; background: #f1f5f9; color: #64748b;
}
.badge.activo { background: #dcfce7; color: #166534; }
.badge.inactivo { background: #fee2e2; color: #991b1b; }
.badge.pendiente { background: #fef3c7; color: #b45309; }
.header-actions { display: flex; gap: 8px; }
.btn-action {
  display: flex; align-items: center; justify-content: center; width: 40px; height: 40px;
  background: white; border: 1px solid #e2e8f0; border-radius: 10px;
  color: #64748b; cursor: pointer; transition: all 0.2s; font-size: 18px;
  text-decoration: none;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.btn-action:hover {
  background: #eef2ff;
  color: #4f46e5;
  border-color: #4f46e5;
}

/* Tabs */
.perfil-tabs {
  display: flex; gap: 8px; background: white; border-bottom: none;
  overflow-x: auto; padding: 16px 20px; margin-bottom: 0;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.tab {
  flex: 0 0 auto; padding: 10px 16px; border: none; background: transparent;
  color: #64748b; font-weight: 600;
  font-size: 13px; cursor: pointer; transition: all 0.2s; display: flex;
  align-items: center; gap: 6px; white-space: nowrap;
  border-radius: 8px;
}
.tab:hover {
  background: #f1f5f9;
  color: #4f46e5;
}
.tab.active {
  color: white;
  background: #4f46e5;
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3);
}
.tab ion-icon { font-size: 16px; }

/* Content */
.perfil-content { background: white; padding: 0; border-radius: 0; }
.tab-pane { animation: fadeIn 0.15s; padding: 24px; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(2px); } to { opacity: 1; transform: translateY(0); } }

/* Personal Dashboard */
.personal-dashboard { padding: 24px; background: #fafbfc; }

/* Dashboard Grid */
.dashboard-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 24px; padding: 0;
}
.grid-col { display: flex; flex-direction: column; gap: 20px; }

/* Dashboard Cards */
.dashboard-card {
  background: white; border: 1px solid #e2e8f0; border-radius: 12px;
  padding: 18px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  transition: box-shadow 0.2s;
}
.dashboard-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.card-header {
  font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase;
  letter-spacing: 0.4px; margin: 0 0 12px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;
}

/* Stats List */
.stats-list { display: flex; flex-direction: column; gap: 12px; }
.stat-row {
  display: flex; align-items: center; gap: 8px; font-size: 12px;
}
.stat-name { flex: 0 0 80px; color: #64748b; font-weight: 500; }
.stat-visual {
  flex: 1; height: 6px; background: #e2e8f0; border-radius: 3px; overflow: hidden;
}
.stat-bar {
  height: 100%; background: #6366f1; border-radius: 3px; transition: width 0.3s;
}
.stat-value {
  font-weight: 700; color: #4f46e5; min-width: 30px; text-align: right;
}
.stat-value.success { color: #10b981; }
.stat-value.danger { color: #ef4444; }
.stat-value.primary { color: #6366f1; }

/* Info Cards Row */
.info-cards-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.mini-card {
  background: #f8fafc; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0;
}
.mini-label { font-size: 10px; color: #64748b; margin: 0; font-weight: 600; text-transform: uppercase; }
.mini-value { font-size: 13px; color: #1e293b; margin: 4px 0 0; font-weight: 700; }

/* Elections Cards */
.elections-cards { display: grid; grid-template-columns: 1fr; gap: 8px; }
.election-card {
  padding: 12px; border-radius: 8px; color: white; position: relative;
  overflow: hidden;
}
.election-badge {
  display: inline-flex; align-items: center; justify-content: center;
  width: 24px; height: 24px; border-radius: 50%; background: rgba(255,255,255,0.3);
  font-weight: 700; margin-bottom: 6px;
}
.badge-check { font-size: 14px; }
.badge-pending { font-size: 12px; }
.election-name { font-size: 13px; font-weight: 700; margin: 0; }
.election-date { font-size: 11px; opacity: 0.85; margin: 2px 0 0; }
.empty-elections {
  padding: 24px; text-align: center; color: #94a3b8; background: #f8fafc;
  border-radius: 8px; font-size: 13px;
}

/* Summary Card */
.summary-card {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 12px; padding: 24px; background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white; text-align: center;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
  border: none;
}
.summary-icon {
  font-size: 32px; font-weight: 800; width: 60px; height: 60px;
  border-radius: 50%; background: rgba(255,255,255,0.2);
  display: flex; align-items: center; justify-content: center;
}
.summary-label { font-size: 11px; margin: 0; opacity: 0.9; text-transform: uppercase; font-weight: 600; }
.summary-value { font-size: 22px; font-weight: 800; margin: 0; text-transform: capitalize; }
.summary-detail { font-size: 12px; margin: 0; opacity: 0.85; }

@media (max-width: 1024px) {
  .dashboard-grid { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
  .welcome-card { flex-direction: column; align-items: flex-start; gap: 12px; }
  .welcome-actions { width: 100%; justify-content: flex-start; }
  .dashboard-grid { grid-template-columns: 1fr; padding: 12px; gap: 12px; }
  .info-cards-row { grid-template-columns: 1fr; }
}

/* Info Grid */
.info-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px; margin-bottom: 20px;
}
.info-item {
  display: flex; flex-direction: column; gap: 4px; padding: 10px;
  background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;
}
.info-item .label { font-size: 11px; color: #64748b; font-weight: 600; text-transform: uppercase; }
.info-item .value { font-size: 13px; color: #1e293b; font-weight: 600; }
.info-item .value.mono { font-family: 'SF Mono', monospace; letter-spacing: 0.3px; }

/* Pills */
.pill {
  display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 11px;
  font-weight: 700; text-transform: uppercase;
}
.pill.admin { background: #eef2ff; color: #6366f1; }
.pill.usuario, .pill.user { background: #f0fdf4; color: #16a34a; }
.pill.activo { background: #dcfce7; color: #166534; }
.pill.inactivo { background: #fee2e2; color: #991b1b; }
.pill.pendiente { background: #fef3c7; color: #b45309; }

/* Table */
.table-wrap { overflow-x: auto; }
.simple-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.simple-table th {
  padding: 8px 10px; text-align: left; font-weight: 600; color: #64748b;
  font-size: 10px; text-transform: uppercase; background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}
.simple-table td { padding: 8px 10px; border-bottom: 1px solid #f1f5f9; color: #1e293b; }
.simple-table tbody tr:hover { background: #f8fafc; }
.simple-table .center { text-align: center; }
.simple-table .right { text-align: right; }
.simple-table .fw600 { font-weight: 600; }

.estado-badge {
  display: inline-block; padding: 2px 6px; border-radius: 3px; font-size: 10px;
  font-weight: 700; text-transform: uppercase;
}
.estado-badge.pagada { background: #dcfce7; color: #166534; }
.estado-badge.pendiente { background: #fef3c7; color: #b45309; }
.estado-badge.vencida { background: #fee2e2; color: #991b1b; }

/* Fotos Gallery */
.fotos-gallery {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 14px;
}
.foto-card {
  display: flex; flex-direction: column; gap: 8px;
  border-radius: 10px; overflow: hidden; border: 1px solid #e2e8f0;
}
.foto-card img { width: 100%; aspect-ratio: 3/4; object-fit: cover; }
.foto-label { padding: 8px 10px; background: #f8fafc; font-size: 12px;
  font-weight: 600; color: #64748b; text-align: center;
}

/* Empty State */
.empty-state {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 8px; padding: 40px 20px; color: #94a3b8;
}
.empty-state ion-icon { font-size: 32px; color: #cbd5e1; }
.empty-state p { font-size: 13px; margin: 0; }

.empty-mini {
  padding: 24px; text-align: center; background: #f8fafc; border-radius: 8px;
  border: 1px solid #e2e8f0; color: #94a3b8; font-size: 13px;
}

.loading-mini {
  padding: 20px; text-align: center; color: #64748b; font-size: 13px;
}

/* Operaciones */
.operaciones-container { padding: 20px; }
.op-section { margin-bottom: 24px; }
.op-section:last-child { margin-bottom: 0; }
.op-title { font-size: 14px; font-weight: 700; color: #1e293b; margin: 0 0 12px;
  padding-bottom: 10px; border-bottom: 2px solid #e2e8f0;
}
.op-table { overflow-x: auto; }
.op-table table { width: 100%; border-collapse: collapse; font-size: 13px; }
.op-table th {
  padding: 10px 12px; text-align: left; font-weight: 600; color: #64748b;
  font-size: 11px; text-transform: uppercase; background: #f8fafc; border-bottom: 1px solid #e2e8f0;
}
.op-table td { padding: 10px 12px; border-bottom: 1px solid #f1f5f9; color: #1e293b; }
.op-table tbody tr:hover { background: #f8fafc; }
.op-table .monto { font-weight: 700; color: #4f46e5; text-align: right; }
.op-table .fecha { color: #64748b; font-size: 12px; }
.op-table .badge {
  display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 10px;
  font-weight: 700; white-space: nowrap;
}
.op-table .badge.method-efectivo { background: #dcfce7; color: #166534; }
.op-table .badge.method-transferencia { background: #dbeafe; color: #0369a1; }
.op-table .badge.method-deposito { background: #fce7f3; color: #be185d; }
.op-table .badge.method-billetera_digital { background: #f3e8ff; color: #7e22ce; }

/* Responsive */
@media (max-width: 768px) {
  .perfil-header { flex-direction: column; align-items: flex-start; }
  .header-content { width: 100%; }
  .info-grid { grid-template-columns: 1fr; }
  .perfil-tabs { padding: 0; }
  .tab { flex: 1; justify-content: center; padding: 10px 12px; }
  .tab ion-icon { display: none; }
}
</style>
