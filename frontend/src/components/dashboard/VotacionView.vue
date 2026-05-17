<template>
  <div class="votacion-container">
    <!-- Header -->
    <div class="view-header">
      <h2>Votaciones Activas</h2>
      <div class="header-actions">
        <button class="refresh-btn" @click="cargarElecciones">
          <ion-icon name="refresh-outline"></ion-icon> Actualizar
        </button>
        <router-link v-if="esAdmin" to="/elecciones" class="btn-crear-votacion">
          <ion-icon name="add-circle-outline"></ion-icon> Crear Votación
        </router-link>
      </div>
    </div>

    <!-- Alert -->
    <div v-if="alert.visible" :class="['alert', `alert-${alert.type}`]">
      {{ alert.message }}
      <button @click="alert.visible = false" class="alert-close">×</button>
    </div>

    <!-- Grid de elecciones -->
    <div class="elecciones-grid">
      <div
        v-for="eleccion in eleccionesActivas"
        :key="eleccion.id"
        :class="['eleccion-card', { 'ya-votado': eleccion.ya_vote }]"
      >
        <div class="card-header">
          <span :class="['tipo-badge', `tipo-${eleccion.tipo}`]">
            {{ eleccion.tipo === 'cargo' ? '👥 Cargo' : '📋 Acuerdo' }}
          </span>
          <span v-if="eleccion.ya_vote" class="votado-badge">✓ Votaste</span>
        </div>

        <h3>{{ eleccion.titulo }}</h3>
        <p v-if="eleccion.descripcion" class="desc">{{ eleccion.descripcion }}</p>

        <div class="opciones-preview">
          <div v-for="op in eleccion.opciones.slice(0, 3)" :key="op.id" class="opcion-preview">
            {{ op.nombre }}
          </div>
          <div v-if="eleccion.opciones.length > 3" class="opcion-more">
            +{{ eleccion.opciones.length - 3 }} más
          </div>
        </div>

        <div class="card-footer">
          <div class="info">
            <small>
              <span v-if="eleccion.fecha_fin">Cierra: {{ formatFecha(eleccion.fecha_fin) }}</span>
              <span v-if="!eleccion.fecha_fin">Abierta</span>
            </small>
          </div>
          <button
            v-if="!eleccion.ya_vote"
            class="btn-votar"
            @click="abrirModalVotar(eleccion)"
          >
            <ion-icon name="checkbox-outline"></ion-icon> Votar
          </button>
          <button v-else class="btn-votado" disabled>
            <ion-icon name="checkmark-outline"></ion-icon> Votado
          </button>
        </div>
      </div>

      <div v-if="!eleccionesActivas.length" class="empty-state">
        <ion-icon name="ballot-outline"></ion-icon>
        <h3>No hay votaciones activas</h3>
        <p>Vuelve luego para participar en las elecciones de la comunidad</p>
      </div>
    </div>

    <!-- Modal de votación -->
    <div v-if="modalAbierto" class="modal-overlay" @click.self="cerrarModal">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ eleccionActiva?.titulo }}</h3>
          <button @click="cerrarModal" class="close-btn">
            <ion-icon name="close-outline"></ion-icon>
          </button>
        </div>

        <div class="modal-body">
          <!-- Paso 1: Selección -->
          <div v-if="pasoVotacion === 1" class="paso-seleccion">
            <p class="paso-info">Selecciona tu opción:</p>
            <div class="opciones-seleccion">
              <label
                v-for="op in eleccionActiva?.opciones"
                :key="op.id"
                class="opcion-radio"
              >
                <input
                  type="radio"
                  :value="op.id"
                  v-model="opcionSeleccionada"
                  name="opcion"
                />
                <span class="radio-custom"></span>
                <div class="opcion-texto">
                  <strong>{{ op.nombre }}</strong>
                  <p v-if="op.descripcion">{{ op.descripcion }}</p>
                </div>
              </label>
            </div>

            <div class="paso-actions">
              <button class="btn-secondary" @click="cerrarModal">Cancelar</button>
              <button
                class="btn-primary"
                :disabled="!opcionSeleccionada"
                @click="pasoVotacion = 2"
              >
                Continuar →
              </button>
            </div>
          </div>

          <!-- Paso 2: Validación -->
          <div v-if="pasoVotacion === 2" class="paso-validacion">
            <div class="validacion-tabs">
              <button
                :class="['tab', { active: tabValidacion === 'facial' }]"
                @click="cambiarTab('facial')"
              >
                📷 Reconocimiento Facial
              </button>
              <button
                :class="['tab', { active: tabValidacion === 'manual' }]"
                @click="cambiarTab('manual')"
              >
                ✓ Validación Manual
              </button>
            </div>

            <!-- Tab Facial -->
            <div v-if="tabValidacion === 'facial'" class="validacion-facial">
              <p class="info">Apunta tu rostro a la cámara para validar tu identidad</p>
              <div class="camera-container">
                <video
                  ref="videoRef"
                  autoplay
                  playsinline
                  muted
                ></video>
                <canvas ref="canvasRef" style="display: none;"></canvas>
                <div class="camera-overlay">
                  <div class="face-circle"></div>
                </div>
              </div>
              <p v-if="estadoFacial" :class="['estado-msg', estadoFacial]">
                {{ mensajeFacial }}
              </p>
              <div class="paso-actions">
                <button class="btn-secondary" @click="pasoVotacion = 1">← Atrás</button>
                <button
                  class="btn-primary"
                  @click="validarYVotar('facial')"
                  :disabled="validando"
                >
                  <span v-if="!validando">Validar y Votar</span>
                  <span v-else><ion-icon name="hourglass-outline"></ion-icon> Validando...</span>
                </button>
              </div>
            </div>

            <!-- Tab Manual -->
            <div v-if="tabValidacion === 'manual'" class="validacion-manual">
              <p class="info">Sube una foto y captura tu ubicación</p>

              <!-- Foto -->
              <div class="upload-section">
                <label class="upload-label">
                  📸 Foto de validación *
                  <input
                    ref="fotoInput"
                    type="file"
                    accept="image/*"
                    capture="user"
                    @change="onFotoSeleccionada"
                    style="display: none;"
                  />
                </label>
                <div v-if="fotoPreview" class="foto-preview">
                  <img :src="fotoPreview" alt="Foto capturada" />
                  <button class="btn-cambiar" @click="$refs.fotoInput.click()">
                    Cambiar foto
                  </button>
                </div>
                <button v-else class="btn-upload" @click="$refs.fotoInput.click()">
                  <ion-icon name="cloud-upload-outline"></ion-icon> Seleccionar foto
                </button>
              </div>

              <!-- GPS -->
              <div class="gps-section">
                <label>📍 Ubicación *</label>
                <button
                  v-if="!gps.latitud"
                  class="btn-gps"
                  @click="capturarGPS"
                  :disabled="gps.estado === 'cargando'"
                >
                  <span v-if="gps.estado === 'idle'">
                    <ion-icon name="locate-outline"></ion-icon> Capturar ubicación
                  </span>
                  <span v-else-if="gps.estado === 'cargando'">
                    <ion-icon name="hourglass-outline"></ion-icon> Obteniendo...
                  </span>
                  <span v-else-if="gps.estado === 'error'" class="error">
                    Error obteniendo ubicación
                  </span>
                </button>
                <div v-if="gps.latitud" class="gps-info">
                  <p>✓ Ubicación capturada</p>
                  <small>{{ gps.latitud.toFixed(5) }}, {{ gps.longitud.toFixed(5) }}</small>
                </div>
              </div>

              <div class="paso-actions">
                <button class="btn-secondary" @click="pasoVotacion = 1">← Atrás</button>
                <button
                  class="btn-primary"
                  @click="validarYVotar('manual')"
                  :disabled="!fotoPreview || !gps.latitud || validando"
                >
                  <span v-if="!validando">Confirmar Voto</span>
                  <span v-else><ion-icon name="hourglass-outline"></ion-icon> Registrando...</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Paso 3: Confirmación -->
          <div v-if="pasoVotacion === 3" class="paso-confirmacion">
            <div class="confirmacion-icon">
              <ion-icon name="checkmark-circle"></ion-icon>
            </div>
            <h3>¡Voto Registrado!</h3>
            <p>Tu voto ha sido registrado exitosamente y de forma segura.</p>
            <p class="info-seguridad">
              Tu privacidad es importante. Tu voto es secreto y no será asociado públicamente con tu identidad.
            </p>
            <button class="btn-primary" @click="cerrarModal">Cerrar</button>
          </div>

          <!-- Paso Error -->
          <div v-if="pasoVotacion === 4" class="paso-error">
            <div class="error-icon">
              <ion-icon name="close-circle"></ion-icon>
            </div>
            <h3>Error en la validación</h3>
            <p>{{ mensajeError }}</p>
            <button class="btn-secondary" @click="pasoVotacion = 2">Intentar de nuevo</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import eleccionesService from '@/services/elecciones.service'

const elecciones = ref([])
const modalAbierto = ref(false)
const eleccionActiva = ref(null)
const opcionSeleccionada = ref(null)
const pasoVotacion = ref(1)
const tabValidacion = ref('facial')
const validando = ref(false)
const alert = ref({ visible: false, type: '', message: '' })

const videoRef = ref(null)
const canvasRef = ref(null)
const fotoInput = ref(null)
const fotoPreview = ref(null)
const fotoBase64 = ref(null)

const estadoFacial = ref('')
const mensajeFacial = ref('')
const mensajeError = ref('')

const gps = ref({
  latitud: null,
  longitud: null,
  estado: 'idle', // idle | cargando | ok | error
})

let stream = null

const eleccionesActivas = computed(() =>
  elecciones.value.filter(e => e.estado === 'activo' && !e.ya_vote)
)

const esAdmin = computed(() => {
  const usuarioStr = localStorage.getItem('auth_usuario')
  if (usuarioStr) {
    try {
      const usuario = JSON.parse(usuarioStr)
      return usuario.rol === 'admin'
    } catch {
      return false
    }
  }
  return false
})

const formatFecha = (fecha) => {
  if (!fecha) return ''
  const d = new Date(fecha)
  return d.toLocaleDateString('es-ES', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

async function cargarElecciones() {
  try {
    const resultado = await eleccionesService.listarElecciones()
    elecciones.value = Array.isArray(resultado) ? resultado : (resultado?.data || [])
  } catch (err) {
    console.error('Error cargando elecciones:', err)
  }
}

function abrirModalVotar(eleccion) {
  eleccionActiva.value = eleccion
  opcionSeleccionada.value = null
  pasoVotacion.value = 1
  fotoPreview.value = null
  fotoBase64.value = null
  gps.value = { latitud: null, longitud: null, estado: 'idle' }

  // Determinar tab default según perfil del usuario
  const usuarioStr = localStorage.getItem('auth_usuario')
  if (usuarioStr) {
    const usuario = JSON.parse(usuarioStr)
    tabValidacion.value = usuario.usar_reconocimiento_facial ? 'facial' : 'manual'
  }

  modalAbierto.value = true

  // Abrir cámara si es facial
  if (tabValidacion.value === 'facial') {
    setTimeout(() => abrirCamara(), 100)
  } else {
    capturarGPS()
  }
}

function cerrarModal() {
  modalAbierto.value = false
  cerrarCamara()
  pasoVotacion.value = 1
}

async function abrirCamara() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user' },
      audio: false,
    })
    videoRef.value.srcObject = stream
    estadoFacial.value = 'listo'
    mensajeFacial.value = 'Cámara lista - mira al frente'
  } catch (err) {
    estadoFacial.value = 'error'
    mensajeFacial.value = 'No se pudo acceder a la cámara'
  }
}

function cerrarCamara() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
    stream = null
  }
}

function capturarFrame() {
  const canvas = canvasRef.value
  const video = videoRef.value
  if (!canvas || !video) return null

  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  const ctx = canvas.getContext('2d')
  ctx.drawImage(video, 0, 0)
  return canvas.toDataURL('image/jpeg', 0.8)
}

function onFotoSeleccionada(e) {
  const file = e.target.files?.[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (event) => {
    fotoPreview.value = event.target.result
    fotoBase64.value = event.target.result
  }
  reader.readAsDataURL(file)
}

function capturarGPS() {
  if (!navigator.geolocation) {
    gps.value.estado = 'error'
    return
  }

  gps.value.estado = 'cargando'
  navigator.geolocation.getCurrentPosition(
    (position) => {
      gps.value.latitud = position.coords.latitude
      gps.value.longitud = position.coords.longitude
      gps.value.estado = 'ok'
    },
    (error) => {
      gps.value.estado = 'error'
      console.error('Error GPS:', error)
    },
    { timeout: 10000 }
  )
}

async function validarYVotar(metodo) {
  validando.value = true
  try {
    let fotoAEnviar = null

    if (metodo === 'facial') {
      fotoAEnviar = capturarFrame()
      if (!fotoAEnviar) {
        throw new Error('No se pudo capturar la foto')
      }
    } else {
      fotoAEnviar = fotoBase64.value
    }

    const body = {
      opcion_id: opcionSeleccionada.value,
      metodo_validacion: metodo,
      foto_base64: fotoAEnviar,
      latitud: metodo === 'manual' ? gps.value.latitud : null,
      longitud: metodo === 'manual' ? gps.value.longitud : null,
    }

    await eleccionesService.votar(eleccionActiva.value.id, body)
    pasoVotacion.value = 3
    cerrarCamara()
    // Recargar elecciones en 2 segundos
    setTimeout(() => {
      cargarElecciones()
    }, 2000)
  } catch (err) {
    mensajeError.value = err.message || 'Error inesperado'
    pasoVotacion.value = 4
  } finally {
    validando.value = false
  }
}

function cambiarTab(tab) {
  tabValidacion.value = tab
  if (tab === 'facial') {
    abrirCamara()
  } else {
    cerrarCamara()
    if (!gps.value.latitud) {
      capturarGPS()
    }
  }
}

watch(() => modalAbierto.value, (abierto) => {
  if (!abierto) {
    cerrarCamara()
  }
})

onMounted(() => {
  cargarElecciones()
})

onUnmounted(() => {
  cerrarCamara()
})
</script>

<style scoped>
.votacion-container {
  padding: 24px;
  background: white;
  border-radius: 12px;
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

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: #f1f5f9;
  color: #64748b;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn:hover {
  background: #16a34a;
  color: white;
  border-color: #16a34a;
}

.btn-crear-votacion {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  font-size: 14px;
}

.btn-crear-votacion:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(79, 70, 229, 0.3);
}

.btn-crear-votacion ion-icon {
  font-size: 18px;
}

.alert {
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.alert-close {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 20px;
  padding: 0;
}

.elecciones-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.eleccion-card {
  background: white;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: all 0.3s;
  cursor: default;
}

.eleccion-card:hover:not(.ya-votado) {
  border-color: #16a34a;
  box-shadow: 0 8px 24px rgba(22, 163, 74, 0.15);
  transform: translateY(-2px);
}

.eleccion-card.ya-votado {
  opacity: 0.7;
  border-color: #dcfce7;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tipo-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  background: #f1f5f9;
  color: #64748b;
}

.tipo-cargo {
  background: #dbeafe;
  color: #1d4ed8;
}

.tipo-acuerdo {
  background: #fef3c7;
  color: #92400e;
}

.votado-badge {
  display: inline-block;
  background: #dcfce7;
  color: #15803d;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
}

.eleccion-card h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.3;
}

.desc {
  margin: 0;
  font-size: 13px;
  color: #64748b;
  line-height: 1.5;
}

.opciones-preview {
  display: flex;
  flex-direction: column;
  gap: 6px;
  background: #f8fafc;
  padding: 10px;
  border-radius: 8px;
}

.opcion-preview {
  font-size: 13px;
  color: #1e293b;
  padding: 4px;
  border-left: 2px solid #16a34a;
  padding-left: 8px;
}

.opcion-more {
  font-size: 12px;
  color: #94a3b8;
  font-style: italic;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.info small {
  color: #94a3b8;
  font-size: 12px;
}

.btn-votar,
.btn-votado {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 13px;
}

.btn-votar {
  background: #16a34a;
  color: white;
}

.btn-votar:hover {
  background: #15803d;
  transform: scale(1.02);
}

.btn-votado {
  background: #f0fdf4;
  color: #15803d;
  cursor: default;
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 24px;
  color: #94a3b8;
}

.empty-state ion-icon {
  font-size: 48px;
  margin-bottom: 16px;
  display: block;
  color: #cbd5e1;
}

.empty-state h3 {
  margin: 0 0 8px;
  color: #64748b;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  flex: 1;
}

.close-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  font-size: 24px;
  padding: 0;
  display: flex;
}

.modal-body {
  overflow-y: auto;
  padding: 20px 24px;
  flex: 1;
}

.paso-info {
  margin: 0 0 16px;
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.opciones-seleccion {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.opcion-radio {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
  padding: 12px;
  border-radius: 10px;
  border: 2px solid #e2e8f0;
  transition: all 0.2s;
}

.opcion-radio:hover {
  border-color: #16a34a;
  background: #f0fdf4;
}

.opcion-radio input[type="radio"] {
  width: 20px;
  height: 20px;
  margin: 0;
  cursor: pointer;
  flex-shrink: 0;
  margin-top: 2px;
}

.radio-custom {
  display: none;
}

.opcion-texto {
  flex: 1;
}

.opcion-texto strong {
  display: block;
  color: #1e293b;
  margin-bottom: 2px;
}

.opcion-texto p {
  margin: 0;
  font-size: 12px;
  color: #64748b;
  line-height: 1.4;
}

.validacion-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  border-bottom: 2px solid #e2e8f0;
}

.tab {
  padding: 12px 16px;
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  border-bottom: 3px solid transparent;
  transition: all 0.2s;
  margin-bottom: -2px;
}

.tab.active {
  color: #16a34a;
  border-bottom-color: #16a34a;
}

.validacion-facial,
.validacion-manual {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info {
  font-size: 13px;
  color: #64748b;
  margin: 0;
}

.camera-container {
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  border-radius: 12px;
  overflow: hidden;
  background: #000;
}

.camera-container video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.camera-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.face-circle {
  width: 120px;
  height: 120px;
  border: 3px solid rgba(134, 239, 172, 0.5);
  border-radius: 50%;
  box-shadow: 0 0 0 1000px rgba(0, 0, 0, 0.3);
}

.estado-msg {
  font-size: 13px;
  text-align: center;
  padding: 8px;
  border-radius: 6px;
  background: #f0fdf4;
  color: #15803d;
  margin: 0;
}

.estado-msg.error {
  background: #fef2f2;
  color: #991b1b;
}

.upload-section,
.gps-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.upload-label,
.gps-section label {
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
}

.foto-preview {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
}

.foto-preview img {
  width: 100%;
  height: auto;
  display: block;
}

.btn-cambiar {
  position: absolute;
  bottom: 12px;
  right: 12px;
  padding: 8px 14px;
  background: rgba(22, 163, 74, 0.9);
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  font-size: 12px;
  transition: background 0.2s;
}

.btn-cambiar:hover {
  background: #16a34a;
}

.btn-upload,
.btn-gps {
  padding: 12px 16px;
  border: 2px dashed #16a34a;
  background: #f0fdf4;
  color: #16a34a;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-upload:hover,
.btn-gps:hover {
  background: #dcfce7;
}

.btn-upload:disabled,
.btn-gps:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.gps-info {
  background: #f0fdf4;
  border-left: 3px solid #16a34a;
  padding: 10px 12px;
  border-radius: 6px;
}

.gps-info p {
  margin: 0;
  font-size: 13px;
  font-weight: 600;
  color: #15803d;
}

.gps-info small {
  display: block;
  font-size: 12px;
  color: #64748b;
  margin-top: 2px;
}

.paso-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
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

.btn-primary {
  padding: 10px 20px;
  background: #16a34a;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: background 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #15803d;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.paso-confirmacion,
.paso-error {
  text-align: center;
  padding: 40px 20px;
}

.confirmacion-icon,
.error-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.confirmacion-icon {
  color: #16a34a;
}

.error-icon {
  color: #ef4444;
}

.paso-confirmacion h3,
.paso-error h3 {
  margin: 0 0 12px;
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
}

.paso-confirmacion p,
.paso-error p {
  margin: 0 0 8px;
  font-size: 14px;
  color: #64748b;
}

.info-seguridad {
  background: #f0fdf4;
  border-left: 3px solid #16a34a;
  padding: 12px;
  border-radius: 6px;
  color: #15803d !important;
  font-size: 13px !important;
  margin: 16px 0 !important;
}

@media (max-width: 768px) {
  .elecciones-grid {
    grid-template-columns: 1fr;
  }

  .modal {
    max-width: 100%;
    border-radius: 16px 16px 0 0;
  }

  .paso-actions {
    flex-direction: column-reverse;
  }

  .btn-secondary,
  .btn-primary {
    width: 100%;
  }
}
</style>
