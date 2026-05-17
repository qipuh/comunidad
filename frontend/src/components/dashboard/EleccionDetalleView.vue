<template>
  <div class="detalle-container">
    <!-- Header con info de elección -->
    <div class="header-detalle">
      <div class="header-left">
        <button class="back-btn" @click="$router.back()">
          <ion-icon name="arrow-back-outline"></ion-icon>
        </button>
        <div>
          <h2>{{ eleccion?.titulo }}</h2>
          <p v-if="eleccion?.descripcion" class="desc">{{ eleccion.descripcion }}</p>
        </div>
      </div>
      <div class="header-right">
        <span :class="['estado-badge', `estado-${eleccion?.estado}`]">
          {{ estadoLabel(eleccion?.estado) }}
        </span>
        <span :class="['tipo-badge', `tipo-${eleccion?.tipo}`]">
          {{ eleccion?.tipo === 'cargo' ? 'Cargo' : 'Acuerdo' }}
        </span>
      </div>
    </div>

    <!-- Alert -->
    <div v-if="alert.visible" :class="['alert', `alert-${alert.type}`]">
      {{ alert.message }}
    </div>

    <!-- Contenido principal -->
    <div class="content-grid">
      <!-- Panel izquierdo: Opciones -->
      <div class="panel opciones-panel">
        <div class="panel-header">
          <h3>Opciones / Candidatos</h3>
          <span v-if="eleccion?.estado === 'borrador'" class="hint">(estado: borrador)</span>
        </div>

        <!-- Para tipo cargo: buscar y agregar usuario -->
        <div v-if="eleccion?.tipo === 'cargo'" class="agregar-opcion">
          <div class="busqueda-usuario">
            <input
              v-model="busquedaUsuario"
              type="text"
              placeholder="Buscar usuario por nombre o email..."
              @input="buscarUsuarios"
            />
            <div v-if="usuariosSugeridos.length" class="sugerencias">
              <div
                v-for="u in usuariosSugeridos"
                :key="u.id"
                class="sugerencia-item"
                @click="agregarOpcionDesdeUsuario(u)"
              >
                <div class="usuario-info">
                  <strong>{{ obtenerNombreCompleto(u) }}</strong>
                  <small>{{ u.numero_dni }}</small>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Para tipo acuerdo: input de texto -->
        <div v-if="eleccion?.tipo === 'acuerdo'" class="agregar-opcion" v-show="eleccion?.estado === 'borrador'">
          <div class="form-agregar">
            <input
              v-model="nuevaOpcion.nombre"
              type="text"
              placeholder="Nombre de la opción"
            />
            <textarea
              v-model="nuevaOpcion.descripcion"
              rows="2"
              placeholder="Descripción (opcional)"
            ></textarea>
            <button
              class="btn-agregar"
              @click="agregarOpcion"
              :disabled="!nuevaOpcion.nombre.trim()"
            >
              <ion-icon name="add-outline"></ion-icon> Agregar opción
            </button>
          </div>
        </div>

        <!-- Lista de opciones -->
        <div class="opciones-lista">
          <div
            v-for="(op, idx) in eleccion?.opciones"
            :key="op.id"
            :class="['opcion-item', { 'con-usuario': op.usuario_id }]"
          >
            <div class="opcion-info">
              <strong>{{ op.nombre }}</strong>
              <small v-if="op.usuario_id" class="usuario-badge">
                <ion-icon name="id-card-outline"></ion-icon> {{ op.descripcion }}
              </small>
              <p v-else-if="op.descripcion" class="desc-opcion">{{ op.descripcion }}</p>
            </div>
            <div class="opcion-votos">
              <span class="votos-count">{{ op.votos || 0 }} votos</span>
              <button
                v-if="eleccion?.estado === 'borrador'"
                class="btn-eliminar"
                @click="eliminarOpcion(op.id)"
                title="Eliminar"
              >
                <ion-icon name="trash-outline"></ion-icon>
              </button>
            </div>
          </div>
          <div v-if="!eleccion?.opciones?.length" class="empty">
            <p>No hay opciones aún</p>
          </div>
        </div>
      </div>

      <!-- Panel derecho: Resultados -->
      <div class="panel resultados-panel">
        <div class="panel-header">
          <h3>Resultados</h3>
          <button v-if="eleccion?.estado === 'activo'" class="refresh-btn" @click="cargarDetalle">
            <ion-icon name="refresh-outline"></ion-icon>
          </button>
        </div>

        <!-- Stats -->
        <div class="stats-box">
          <div class="stat">
            <span class="stat-label">Total votos</span>
            <span class="stat-value">{{ eleccion?.total_votos || 0 }}</span>
          </div>
          <div class="stat">
            <span class="stat-label">Participación</span>
            <span class="stat-value">-</span>
          </div>
        </div>

        <!-- Barras de resultado -->
        <div class="resultados-list">
          <div
            v-for="op in eleccion?.opciones"
            :key="op.id"
            class="resultado-item"
          >
            <div class="resultado-label">
              <strong>{{ op.nombre }}</strong>
              <span class="resultado-count">{{ op.votos || 0 }}</span>
            </div>
            <div class="resultado-bar">
              <div
                class="resultado-fill"
                :style="{ width: calcularPorcentaje(op.votos, eleccion?.total_votos) + '%' }"
              ></div>
            </div>
            <span class="resultado-porcentaje">
              {{ calcularPorcentaje(op.votos, eleccion?.total_votos) }}%
            </span>
          </div>
          <div v-if="!eleccion?.opciones?.length" class="empty">
            <p>Sin datos para mostrar</p>
          </div>
        </div>

        <!-- Info de elección -->
        <div class="info-box">
          <div v-if="eleccion?.fecha_inicio" class="info-item">
            <span class="label">Inicia:</span>
            <span>{{ formatFecha(eleccion.fecha_inicio) }}</span>
          </div>
          <div v-if="eleccion?.fecha_fin" class="info-item">
            <span class="label">Cierra:</span>
            <span>{{ formatFecha(eleccion.fecha_fin) }}</span>
          </div>
          <div class="info-item">
            <span class="label">Resultados públicos:</span>
            <span>{{ eleccion?.resultados_publicos ? 'Sí' : 'No' }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import eleccionesService from '@/services/elecciones.service'
import { usuariosService } from '@/services/usuarios.service'

const route = useRoute()
const eleccionId = route.params.id

const eleccion = ref(null)
const alert = ref({ visible: false, type: '', message: '' })
const busquedaUsuario = ref('')
const usuariosSugeridos = ref([])
const nuevaOpcion = ref({ nombre: '', descripcion: '' })
let pollInterval = null

const estadoLabel = (estado) => {
  const labels = { borrador: 'Borrador', activo: 'Activa', cerrado: 'Cerrada' }
  return labels[estado] || estado
}

const formatFecha = (fecha) => {
  if (!fecha) return ''
  const d = new Date(fecha)
  return d.toLocaleDateString('es-ES') + ' ' + d.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
}

const calcularPorcentaje = (votos, total) => {
  if (!total || total === 0) return 0
  return Math.round((votos / total) * 100)
}

const obtenerNombreCompleto = (usuario) => {
  const partes = [usuario.nombres, usuario.apellido_paterno, usuario.apellido_materno].filter(p => p && p.trim())
  return partes.join(' ') || 'Sin nombre'
}

async function cargarDetalle() {
  try {
    eleccion.value = await eleccionesService.obtenerEleccion(eleccionId)
  } catch (err) {
    console.error('Error cargando detalle:', err)
  }
}

async function buscarUsuarios() {
  if (!busquedaUsuario.value.trim()) {
    usuariosSugeridos.value = []
    return
  }

  try {
    const respuesta = await usuariosService.buscarPorNombre(busquedaUsuario.value)
    const usuarios = Array.isArray(respuesta) ? respuesta : (respuesta?.data || [])

    // Filtrar usuarios que ya son candidatos
    const usuarioIds = new Set(eleccion.value?.opciones?.map(o => o.usuario_id) || [])
    usuariosSugeridos.value = usuarios.filter(u => !usuarioIds.has(u.id))
  } catch (err) {
    console.error('Error buscando usuarios:', err)
  }
}

async function agregarOpcionDesdeUsuario(usuario) {
  const opcion = {
    nombre: obtenerNombreCompleto(usuario),
    descripcion: usuario.numero_dni,
    usuario_id: usuario.id,
    orden: (eleccion.value?.opciones?.length || 0) + 1,
  }

  try {
    await eleccionesService.agregarOpcion(eleccionId, opcion)
    busquedaUsuario.value = ''
    usuariosSugeridos.value = []
    alert.value = { visible: true, type: 'success', message: 'Candidato agregado' }
    await cargarDetalle()
  } catch (err) {
    const mensaje = err?.response?.data?.detail || 'Error agregando candidato'
    alert.value = { visible: true, type: 'error', message: mensaje }
  }
}

async function agregarOpcion() {
  if (!nuevaOpcion.value.nombre.trim()) return

  const opcion = {
    nombre: nuevaOpcion.value.nombre,
    descripcion: nuevaOpcion.value.descripcion,
    orden: (eleccion.value?.opciones?.length || 0) + 1,
  }

  try {
    await eleccionesService.agregarOpcion(eleccionId, opcion)
    nuevaOpcion.value = { nombre: '', descripcion: '' }
    alert.value = { visible: true, type: 'success', message: 'Opción agregada' }
    await cargarDetalle()
  } catch (err) {
    const mensaje = err?.response?.data?.detail || 'Error agregando opción'
    alert.value = { visible: true, type: 'error', message: mensaje }
  }
}

async function eliminarOpcion(opcionId) {
  if (!confirm('¿Eliminar opción?')) return

  try {
    await eleccionesService.eliminarOpcion(eleccionId, opcionId)
    alert.value = { visible: true, type: 'success', message: 'Opción eliminada' }
    await cargarDetalle()
  } catch (err) {
    const mensaje = err?.response?.data?.detail || 'Error eliminando opción'
    alert.value = { visible: true, type: 'error', message: mensaje }
  }
}

onMounted(() => {
  cargarDetalle()
  // Polling cada 10s si está activa
  if (eleccion.value?.estado === 'activo') {
    pollInterval = setInterval(cargarDetalle, 10000)
  }
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})
</script>

<style scoped>
.detalle-container {
  padding: 24px;
  background: white;
  border-radius: 12px;
}

.header-detalle {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  gap: 16px;
}

.header-left {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  flex: 1;
}

.back-btn {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: white;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #16a34a;
  color: white;
  border-color: #16a34a;
}

.header-left h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.3;
}

.header-left .desc {
  margin: 4px 0 0;
  font-size: 13px;
  color: #64748b;
}

.header-right {
  display: flex;
  gap: 8px;
}

.estado-badge,
.tipo-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
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

.tipo-cargo {
  background: #dbeafe;
  color: #1d4ed8;
}

.tipo-acuerdo {
  background: #fef3c7;
  color: #92400e;
}

.alert {
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 14px;
}

.alert-error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
}

.alert-success {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #15803d;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.panel {
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
}

.hint {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 400;
}

.refresh-btn {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: none;
  background: white;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.refresh-btn:hover {
  background: #16a34a;
  color: white;
}

.agregar-opcion {
  background: white;
  border-radius: 8px;
  padding: 14px;
  border: 1px solid #e2e8f0;
}

.busqueda-usuario {
  position: relative;
}

.busqueda-usuario input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  transition: border 0.2s;
}

.busqueda-usuario input:focus {
  outline: none;
  border-color: #16a34a;
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1);
}

.sugerencias {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e2e8f0;
  border-top: none;
  border-radius: 0 0 8px 8px;
  max-height: 250px;
  overflow-y: auto;
  z-index: 10;
}

.sugerencia-item {
  padding: 12px;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
  transition: background 0.2s;
}

.sugerencia-item:last-child {
  border-bottom: none;
}

.sugerencia-item:hover {
  background: #f8fafc;
}

.usuario-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.usuario-info strong {
  font-size: 13px;
  color: #1e293b;
}

.usuario-info small {
  font-size: 12px;
  color: #94a3b8;
}

.form-agregar {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-agregar input,
.form-agregar textarea {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  transition: border 0.2s;
}

.form-agregar input:focus,
.form-agregar textarea:focus {
  outline: none;
  border-color: #16a34a;
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1);
}

.btn-agregar {
  padding: 10px 12px;
  background: #16a34a;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: background 0.2s;
  font-size: 13px;
}

.btn-agregar:hover:not(:disabled) {
  background: #15803d;
}

.btn-agregar:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.opciones-lista {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.opcion-item {
  background: white;
  border-radius: 8px;
  padding: 12px;
  border: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.2s;
}

.opcion-item:hover {
  border-color: #16a34a;
  box-shadow: 0 2px 8px rgba(22, 163, 74, 0.1);
}

.opcion-info {
  flex: 1;
}

.opcion-info strong {
  display: block;
  font-size: 13px;
  color: #1e293b;
  margin-bottom: 2px;
}

.desc-opcion {
  margin: 4px 0 0;
  font-size: 12px;
  color: #94a3b8;
}

.usuario-badge {
  display: inline-block;
  background: #dbeafe;
  color: #1d4ed8;
  padding: 2px 8px;
  border-radius: 4px;
  margin-top: 4px;
}

.opcion-votos {
  display: flex;
  align-items: center;
  gap: 8px;
}

.votos-count {
  font-size: 12px;
  font-weight: 700;
  color: #16a34a;
  min-width: 50px;
  text-align: right;
}

.btn-eliminar {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: none;
  background: #fee2e2;
  color: #991b1b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-eliminar:hover {
  background: #fecaca;
}

.empty {
  text-align: center;
  padding: 20px;
  color: #94a3b8;
  font-size: 13px;
}

.stats-box {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.stat {
  background: white;
  border-radius: 8px;
  padding: 12px;
  border: 1px solid #e2e8f0;
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #94a3b8;
  margin-bottom: 4px;
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: #16a34a;
}

.resultados-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.resultado-item {
  background: white;
  border-radius: 8px;
  padding: 12px;
  border: 1px solid #e2e8f0;
}

.resultado-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.resultado-label strong {
  font-size: 13px;
  color: #1e293b;
}

.resultado-count {
  font-size: 12px;
  font-weight: 700;
  color: #16a34a;
}

.resultado-bar {
  height: 24px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 4px;
}

.resultado-fill {
  height: 100%;
  background: linear-gradient(90deg, #16a34a, #15803d);
  transition: width 0.3s ease;
}

.resultado-porcentaje {
  display: block;
  font-size: 11px;
  color: #94a3b8;
  text-align: right;
}

.info-box {
  background: white;
  border-radius: 8px;
  padding: 12px;
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.info-item .label {
  font-weight: 600;
  color: #64748b;
}

.info-item span:last-child {
  color: #1e293b;
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .header-detalle {
    flex-direction: column;
  }

  .header-left {
    width: 100%;
  }
}
</style>
