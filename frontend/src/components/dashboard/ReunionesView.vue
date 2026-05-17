<template>
  <div class="reuniones-view">
    <div class="view-header">
      <h1>Gestión de Reuniones</h1>
      <button class="btn-primary" @click="abrirModalNueva" v-if="usuarioActual?.rol === 'admin'">
        <ion-icon name="add-circle-outline"></ion-icon>
        Nueva Reunión
      </button>
    </div>

    <!-- Filtros -->
    <div class="filtros">
      <select v-model="filtroEstado" class="select-filter">
        <option value="">Todos los estados</option>
        <option value="programada">Programada</option>
        <option value="en_curso">En Curso</option>
        <option value="finalizada">Finalizada</option>
        <option value="cancelada">Cancelada</option>
      </select>
      <select v-model="filtroTipo" class="select-filter">
        <option value="">Todos los tipos</option>
        <option value="asamblea">Asamblea</option>
        <option value="reunion">Reunión</option>
        <option value="ordinaria">Ordinaria</option>
        <option value="extraordinaria">Extraordinaria</option>
        <option value="sesion">Sesión</option>
      </select>
    </div>

    <!-- Tabla de Reuniones -->
    <div class="tabla-container">
      <table class="tabla-reuniones">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Tipo</th>
            <th>Fecha</th>
            <th>Lugar</th>
            <th>Estado</th>
            <th>Asistentes</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="reunion in reunionesFiltradas" :key="reunion.id">
            <td class="nombre" @click="abrirSidebar(reunion)">{{ reunion.nombre }}</td>
            <td>
              <span class="badge" :class="'tipo-' + reunion.tipo">
                {{ reunion.tipo }}
              </span>
            </td>
            <td>{{ formatearFecha(reunion.fecha_inicio) }}</td>
            <td>{{ reunion.lugar || '-' }}</td>
            <td>
              <span class="badge" :class="'estado-' + reunion.estado">
                {{ reunion.estado }}
              </span>
            </td>
            <td class="asistentes">{{ reunion.total_asistentes }}</td>
            <td class="acciones">
              <button
                class="btn-icon"
                @click="abrirSidebar(reunion)"
                title="Ver detalles"
              >
                <ion-icon name="eye-outline"></ion-icon>
              </button>
              <button
                class="btn-icon btn-danger"
                @click="eliminarReunion(reunion.id)"
                v-if="usuarioActual?.rol === 'admin'"
                title="Eliminar"
              >
                <ion-icon name="trash-outline"></ion-icon>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Crear/Editar Reunión -->
    <div class="modal-overlay" v-if="mostrarModalReunion" @click.self="cerrarModalReunion">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ editandoReunion ? 'Editar Reunión' : 'Nueva Reunión' }}</h2>
          <button class="btn-cerrar" @click="cerrarModalReunion">
            <ion-icon name="close-outline"></ion-icon>
          </button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label>Nombre</label>
            <input v-model="formReunion.nombre" type="text" placeholder="Nombre de la reunión" />
          </div>

          <div class="form-group">
            <label>Descripción</label>
            <textarea v-model="formReunion.descripcion" placeholder="Descripción..."></textarea>
          </div>

          <div class="form-group">
            <label>Tipo</label>
            <select v-model="formReunion.tipo">
              <option value="asamblea">Asamblea</option>
              <option value="reunion">Reunión</option>
              <option value="ordinaria">Ordinaria</option>
              <option value="extraordinaria">Extraordinaria</option>
              <option value="sesion">Sesión</option>
            </select>
          </div>

          <div class="form-group">
            <label>Lugar</label>
            <input v-model="formReunion.lugar" type="text" placeholder="Lugar de la reunión" />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Fecha Inicio</label>
              <input v-model="formReunion.fecha_inicio" type="datetime-local" />
            </div>
            <div class="form-group">
              <label>Fecha Fin</label>
              <input v-model="formReunion.fecha_fin" type="datetime-local" />
            </div>
          </div>

          <div class="form-group">
            <label>Estados de usuario permitidos</label>
            <div class="checkboxes">
              <label>
                <input type="checkbox" value="activo" v-model="formReunion.estados_usuario_permitidos" />
                Activo
              </label>
              <label>
                <input type="checkbox" value="inactivo" v-model="formReunion.estados_usuario_permitidos" />
                Inactivo
              </label>
              <label>
                <input type="checkbox" value="pendiente" v-model="formReunion.estados_usuario_permitidos" />
                Pendiente
              </label>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-secondary" @click="cerrarModalReunion">Cancelar</button>
          <button class="btn-primary" @click="guardarReunion">
            {{ editandoReunion ? 'Actualizar' : 'Crear' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Sidebar Detalles -->
    <div class="sidebar-overlay" v-if="reunionSeleccionada" @click.self="cerrarSidebar">
      <div class="sidebar">
        <!-- Header Hero -->
        <div class="sidebar-hero">
          <div class="hero-gradient"></div>
          <div class="hero-content">
            <h2>{{ reunionSeleccionada.nombre }}</h2>
            <div class="badges">
              <span class="badge" :class="'tipo-' + reunionSeleccionada.tipo">
                {{ reunionSeleccionada.tipo }}
              </span>
              <span class="badge" :class="'estado-' + reunionSeleccionada.estado">
                {{ reunionSeleccionada.estado }}
              </span>
            </div>
          </div>
          <button class="btn-cerrar" @click="cerrarSidebar">
            <ion-icon name="close-outline"></ion-icon>
          </button>
        </div>

        <!-- Info Rápida -->
        <div class="info-rapida">
          <div class="info-item">
            <ion-icon name="calendar-outline"></ion-icon>
            <span>{{ formatearFecha(reunionSeleccionada.fecha_inicio) }}</span>
          </div>
          <div class="info-item">
            <ion-icon name="location-outline"></ion-icon>
            <span>{{ reunionSeleccionada.lugar || '-' }}</span>
          </div>
          <div class="info-item">
            <ion-icon name="people-outline"></ion-icon>
            <span>{{ reunionSeleccionada.total_asistentes }} asistentes</span>
          </div>
        </div>

        <!-- Tabs -->
        <div class="tabs">
          <button
            v-for="tab in ['asistencia', 'asistentes', 'reporte']"
            :key="tab"
            :class="{ active: tabActivo === tab }"
            @click="tabActivo = tab"
            class="tab-btn"
          >
            {{ tab.charAt(0).toUpperCase() + tab.slice(1) }}
          </button>
        </div>

        <!-- Tab Content -->
        <div class="tab-content">
          <!-- Tab Asistencia -->
          <div v-if="tabActivo === 'asistencia'" class="tab-pane">
            <div v-if="!mostrandoScanQR && !mostrandoScanFacial" class="botones-asistencia">
              <button class="btn-grande" @click="iniciarScanQR">
                <ion-icon name="qr-code-outline"></ion-icon>
                Escanear QR
              </button>
              <button class="btn-grande" @click="iniciarScanFacial">
                <ion-icon name="camera-outline"></ion-icon>
                Reconocimiento Facial
              </button>

              <!-- Cambiar estado -->
              <div class="cambiar-estado" v-if="usuarioActual?.rol === 'admin'">
                <label>Cambiar estado:</label>
                <select v-model="nuevoEstado" class="select-filter">
                  <option value="programada">Programada</option>
                  <option value="en_curso">En Curso</option>
                  <option value="finalizada">Finalizada</option>
                  <option value="cancelada">Cancelada</option>
                </select>
                <button class="btn-small" @click="cambiarEstadoReunion">Aplicar</button>
              </div>
            </div>

            <!-- Panel QR -->
            <div v-if="mostrandoScanQR" class="panel-escaneo">
              <h3>Escanear QR del Carnet</h3>
              <video ref="videoQR" width="100%" height="auto"></video>
              <div v-if="resultadoQR" :class="['resultado', resultadoQR.success ? 'exito' : 'error']">
                <ion-icon :name="resultadoQR.success ? 'checkmark-circle-outline' : 'close-circle-outline'"></ion-icon>
                <p v-if="resultadoQR.success">
                  {{ resultadoQR.asistencia.nombre_completo }} registrado
                </p>
                <p v-else>{{ resultadoQR.error }}</p>
                <button @click="finalizarEscaneoQR" class="btn-secondary">Cerrar</button>
              </div>
              <button @click="cancelarScanQR" class="btn-secondary" v-if="!resultadoQR">
                Cancelar
              </button>
            </div>

            <!-- Panel Facial -->
            <div v-if="mostrandoScanFacial" class="panel-escaneo">
              <h3>Reconocimiento Facial</h3>
              <video ref="videoFacial" width="100%" height="auto"></video>
              <button @click="capturarFoto" class="btn-primary">Capturar Foto</button>
              <div v-if="resultadoFacial" :class="['resultado', resultadoFacial.success ? 'exito' : 'error']">
                <ion-icon :name="resultadoFacial.success ? 'checkmark-circle-outline' : 'close-circle-outline'"></ion-icon>
                <p v-if="resultadoFacial.success">
                  {{ resultadoFacial.asistencia.nombre_completo }} registrado
                </p>
                <p v-else>{{ resultadoFacial.error }}</p>
                <button @click="finalizarEscaneoFacial" class="btn-secondary">Cerrar</button>
              </div>
              <button @click="cancelarScanFacial" class="btn-secondary" v-if="!resultadoFacial">
                Cancelar
              </button>
            </div>
          </div>

          <!-- Tab Asistentes -->
          <div v-if="tabActivo === 'asistentes'" class="tab-pane">
            <h3>Asistentes Registrados</h3>
            <p class="stats">{{ asistentes.length }} de {{ estadisticasReporte?.estadisticas?.total_permitidos || 0 }} presentes</p>
            <div class="asistentes-list">
              <div v-for="asistente in asistentes" :key="asistente.usuario_id" class="asistente-item">
                <div class="avatar" v-if="asistente.foto_url">
                  <img :src="asistente.foto_url" :alt="asistente.nombre_completo" />
                </div>
                <div class="info">
                  <p class="nombre">{{ asistente.nombre_completo }}</p>
                  <p class="dni">{{ asistente.numero_dni }}</p>
                  <p class="hora">{{ formatearHora(asistente.fecha_hora_registro) }}</p>
                </div>
                <span class="badge metodo" :class="'metodo-' + asistente.metodo_registro">
                  {{ asistente.metodo_registro }}
                </span>
                <button
                  class="btn-icon btn-danger"
                  @click="removerAsistente(asistente.usuario_id)"
                  v-if="usuarioActual?.rol === 'admin'"
                  title="Remover"
                >
                  <ion-icon name="trash-outline"></ion-icon>
                </button>
              </div>
            </div>
          </div>

          <!-- Tab Reporte -->
          <div v-if="tabActivo === 'reporte'" class="tab-pane">
            <h3>Reporte de Asistencia</h3>

            <div class="stats-reporte" v-if="estadisticasReporte">
              <div class="stat">
                <span class="label">Asistentes:</span>
                <span class="valor">{{ estadisticasReporte.estadisticas.total_asistentes }}</span>
              </div>
              <div class="stat">
                <span class="label">Inasistentes:</span>
                <span class="valor">{{ estadisticasReporte.estadisticas.total_inasistentes }}</span>
              </div>
              <div class="stat">
                <span class="label">Porcentaje:</span>
                <span class="valor">{{ estadisticasReporte.estadisticas.porcentaje_asistencia }}%</span>
              </div>
            </div>

            <button class="btn-primary" @click="exportarExcel" v-if="estadisticasReporte">
              <ion-icon name="download-outline"></ion-icon>
              Descargar Excel
            </button>

            <!-- Inasistentes -->
            <h4>Inasistentes</h4>
            <div class="inasistentes-list" v-if="estadisticasReporte?.inasistentes">
              <div v-for="inasistente in estadisticasReporte.inasistentes" :key="inasistente.numero_dni" class="inasistente-item">
                <p class="nombre">{{ inasistente.nombre_completo }}</p>
                <p class="dni">{{ inasistente.numero_dni }}</p>
              </div>
            </div>
            <p v-else class="sin-datos">No hay inasistentes</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Alert -->
    <div v-if="alert.visible" :class="['alert', 'alert-' + alert.type]">
      {{ alert.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import reunionesService from '@/services/reuniones.service'
import authService from '@/services/auth.service'
import jsQR from 'jsqr'
import * as XLSX from 'xlsx'

// Estado
const reuniones = ref([])
const reunionSeleccionada = ref(null)
const usuarioActual = ref(null)
const mostrarModalReunion = ref(false)
const editandoReunion = ref(false)
const tabActivo = ref('asistencia')
const filtroEstado = ref('')
const filtroTipo = ref('')

// Asistencia
const mostrandoScanQR = ref(false)
const mostrandoScanFacial = ref(false)
const videoQR = ref(null)
const videoFacial = ref(null)
const canvasQR = ref(null)
const resultadoQR = ref(null)
const resultadoFacial = ref(null)
const asistentes = ref([])
const estadisticasReporte = ref(null)
const nuevoEstado = ref('en_curso')

// Formulario
const formReunion = ref({
  nombre: '',
  descripcion: '',
  lugar: '',
  tipo: 'reunion',
  fecha_inicio: '',
  fecha_fin: '',
  estados_usuario_permitidos: ['activo']
})

// Alert
const alert = ref({
  visible: false,
  type: 'success',
  message: ''
})

// Computed
const reunionesFiltradas = computed(() => {
  return reuniones.value.filter(r => {
    if (filtroEstado.value && r.estado !== filtroEstado.value) return false
    if (filtroTipo.value && r.tipo !== filtroTipo.value) return false
    return true
  })
})

// Métodos
const mostrarAlert = (message, type = 'success') => {
  alert.value = { visible: true, type, message }
  setTimeout(() => {
    alert.value.visible = false
  }, 3000)
}

const cargarReuniones = async () => {
  try {
    const data = await reunionesService.listarReuniones(filtroEstado.value || undefined, filtroTipo.value || undefined)
    reuniones.value = data
  } catch (error) {
    mostrarAlert('Error cargando reuniones', 'error')
  }
}

const abrirModalNueva = () => {
  editandoReunion.value = false
  formReunion.value = {
    nombre: '',
    descripcion: '',
    lugar: '',
    tipo: 'reunion',
    fecha_inicio: '',
    fecha_fin: '',
    estados_usuario_permitidos: ['activo']
  }
  mostrarModalReunion.value = true
}

const cerrarModalReunion = () => {
  mostrarModalReunion.value = false
}

const guardarReunion = async () => {
  try {
    if (!formReunion.value.nombre) {
      mostrarAlert('El nombre es requerido', 'error')
      return
    }
    if (!formReunion.value.fecha_inicio || !formReunion.value.fecha_fin) {
      mostrarAlert('Las fechas son requeridas', 'error')
      return
    }

    const datos = {
      ...formReunion.value,
      fecha_inicio: new Date(formReunion.value.fecha_inicio).toISOString(),
      fecha_fin: new Date(formReunion.value.fecha_fin).toISOString()
    }

    if (editandoReunion.value) {
      await reunionesService.actualizarReunion(reunionSeleccionada.value.id, datos)
      mostrarAlert('Reunión actualizada', 'success')
    } else {
      await reunionesService.crearReunion(datos)
      mostrarAlert('Reunión creada', 'success')
    }

    cerrarModalReunion()
    cargarReuniones()
  } catch (error) {
    mostrarAlert('Error guardando reunión', 'error')
  }
}

const eliminarReunion = async (id) => {
  if (!confirm('¿Deseas eliminar esta reunión?')) return

  try {
    await reunionesService.eliminarReunion(id)
    mostrarAlert('Reunión eliminada', 'success')
    cargarReuniones()
  } catch (error) {
    mostrarAlert('Error eliminando reunión', 'error')
  }
}

const abrirSidebar = (reunion) => {
  reunionSeleccionada.value = reunion
  tabActivo.value = 'asistencia'
  nuevoEstado.value = reunion.estado
  cargarAsistentes()
  cargarReporte()
}

const cerrarSidebar = () => {
  reunionSeleccionada.value = null
  mostrandoScanQR.value = false
  mostrandoScanFacial.value = false
  resultadoQR.value = null
  resultadoFacial.value = null
}

const cargarAsistentes = async () => {
  try {
    const data = await reunionesService.listarAsistentes(reunionSeleccionada.value.id)
    asistentes.value = data
  } catch (error) {
    mostrarAlert('Error cargando asistentes', 'error')
  }
}

const cargarReporte = async () => {
  try {
    const data = await reunionesService.obtenerReporte(reunionSeleccionada.value.id)
    estadisticasReporte.value = data
  } catch (error) {
    mostrarAlert('Error cargando reporte', 'error')
  }
}

const cambiarEstadoReunion = async () => {
  try {
    await reunionesService.cambiarEstado(reunionSeleccionada.value.id, nuevoEstado.value)
    reunionSeleccionada.value.estado = nuevoEstado.value
    mostrarAlert('Estado actualizado', 'success')
  } catch (error) {
    mostrarAlert('Error cambiando estado', 'error')
  }
}

// QR Scanning
const iniciarScanQR = async () => {
  mostrandoScanQR.value = true
  resultadoQR.value = null

  await new Promise(resolve => setTimeout(resolve, 300))

  try {
    const constraints = {
      video: {
        facingMode: 'user',
        width: { ideal: 640 },
        height: { ideal: 480 }
      }
    }

    const stream = await navigator.mediaDevices.getUserMedia(constraints)

    if (videoQR.value) {
      videoQR.value.srcObject = stream
      escanearQR()
    } else {
      mostrarAlert('Error: elemento de vídeo no encontrado', 'error')
      stream.getTracks().forEach(track => track.stop())
    }
  } catch (error) {
    mostrandoScanQR.value = false
    const mensajeError = error.name === 'NotAllowedError'
      ? 'Permiso denegado. Permite el acceso a la cámara en los ajustes del navegador'
      : error.name === 'NotFoundError'
      ? 'Cámara no encontrada. Verifica que tu dispositivo tenga cámara'
      : `Error de cámara: ${error.message}`

    mostrarAlert(mensajeError, 'error')
    console.error('Error accediendo a cámara:', error)
  }
}

const escanearQR = () => {
  if (!videoQR.value || !mostrandoScanQR.value) return

  const { videoWidth, videoHeight } = videoQR.value

  // Esperar a que el video tenga dimensiones
  if (videoWidth === 0 || videoHeight === 0) {
    requestAnimationFrame(escanearQR)
    return
  }

  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  canvas.width = videoWidth
  canvas.height = videoHeight

  ctx.drawImage(videoQR.value, 0, 0)
  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
  const code = jsQR(imageData.data, canvas.width, canvas.height)

  if (code) {
    detenerScanQR()
    procesarQR(code.data)
  } else {
    requestAnimationFrame(escanearQR)
  }
}

const procesarQR = async (qrData) => {
  try {
    const datos = JSON.parse(qrData)
    const resultado = await reunionesService.registrarAsistenciaQR(
      reunionSeleccionada.value.id,
      datos.dni
    )
    resultadoQR.value = resultado
    cargarAsistentes()
  } catch (error) {
    resultadoQR.value = {
      success: false,
      error: error.response?.data?.detail || 'Error registrando asistencia'
    }
  }
}

const cancelarScanQR = () => {
  detenerScanQR()
  mostrandoScanQR.value = false
}

const finalizarEscaneoQR = () => {
  detenerScanQR()
  mostrandoScanQR.value = false
  resultadoQR.value = null
}

const detenerScanQR = () => {
  if (videoQR.value && videoQR.value.srcObject) {
    videoQR.value.srcObject.getTracks().forEach(track => track.stop())
  }
}

// Facial Recognition
const iniciarScanFacial = async () => {
  mostrandoScanFacial.value = true
  resultadoFacial.value = null

  await new Promise(resolve => setTimeout(resolve, 300))

  try {
    const constraints = {
      video: {
        facingMode: 'user',
        width: { ideal: 640 },
        height: { ideal: 480 }
      }
    }

    const stream = await navigator.mediaDevices.getUserMedia(constraints)

    if (videoFacial.value) {
      videoFacial.value.srcObject = stream
    } else {
      mostrarAlert('Error: elemento de vídeo no encontrado', 'error')
      stream.getTracks().forEach(track => track.stop())
    }
  } catch (error) {
    mostrandoScanFacial.value = false
    const mensajeError = error.name === 'NotAllowedError'
      ? 'Permiso denegado. Permite el acceso a la cámara en los ajustes del navegador'
      : error.name === 'NotFoundError'
      ? 'Cámara no encontrada. Verifica que tu dispositivo tenga cámara'
      : `Error de cámara: ${error.message}`

    mostrarAlert(mensajeError, 'error')
    console.error('Error accediendo a cámara:', error)
  }
}

const capturarFoto = async () => {
  if (!videoFacial.value) {
    resultadoFacial.value = {
      success: false,
      error: 'Video no disponible'
    }
    return
  }

  const { videoWidth, videoHeight } = videoFacial.value

  if (videoWidth === 0 || videoHeight === 0) {
    resultadoFacial.value = {
      success: false,
      error: 'Espera a que la cámara se cargue completamente'
    }
    return
  }

  const canvas = document.createElement('canvas')
  canvas.width = videoWidth
  canvas.height = videoHeight

  const ctx = canvas.getContext('2d')
  ctx.drawImage(videoFacial.value, 0, 0)

  const fotoBase64 = canvas.toDataURL('image/jpeg').split(',')[1]

  if (!fotoBase64 || fotoBase64.length < 100) {
    resultadoFacial.value = {
      success: false,
      error: 'No se pudo capturar la foto. Intenta de nuevo'
    }
    return
  }

  try {
    const resultado = await reunionesService.registrarAsistenciaFacial(
      reunionSeleccionada.value.id,
      fotoBase64
    )
    resultadoFacial.value = resultado
    cargarAsistentes()
  } catch (error) {
    resultadoFacial.value = {
      success: false,
      error: error.response?.data?.detail || 'Error registrando asistencia'
    }
  }
}

const cancelarScanFacial = () => {
  detenerScanFacial()
  mostrandoScanFacial.value = false
}

const finalizarEscaneoFacial = () => {
  detenerScanFacial()
  mostrandoScanFacial.value = false
  resultadoFacial.value = null
}

const detenerScanFacial = () => {
  if (videoFacial.value && videoFacial.value.srcObject) {
    videoFacial.value.srcObject.getTracks().forEach(track => track.stop())
  }
}

const removerAsistente = async (usuarioId) => {
  if (!confirm('¿Deseas remover este asistente?')) return

  try {
    await reunionesService.removerAsistente(reunionSeleccionada.value.id, usuarioId)
    mostrarAlert('Asistente removido', 'success')
    cargarAsistentes()
  } catch (error) {
    mostrarAlert('Error removiendo asistente', 'error')
  }
}

const exportarExcel = () => {
  if (!estadisticasReporte.value) return

  const wb = XLSX.utils.book_new()

  // Hoja de asistentes
  const asistentes_data = estadisticasReporte.value.asistentes.map(a => ({
    Nombre: a.nombre_completo,
    DNI: a.numero_dni,
    Email: a.email,
    Estado: a.estado,
    Hora: new Date(a.fecha_hora_registro).toLocaleTimeString(),
    Método: a.metodo_registro
  }))

  const ws_asistentes = XLSX.utils.json_to_sheet(asistentes_data)
  XLSX.utils.book_append_sheet(wb, ws_asistentes, 'Asistentes')

  // Hoja de inasistentes
  const inasistentes_data = estadisticasReporte.value.inasistentes.map(i => ({
    Nombre: i.nombre_completo,
    DNI: i.numero_dni,
    Email: i.email,
    Estado: i.estado
  }))

  const ws_inasistentes = XLSX.utils.json_to_sheet(inasistentes_data)
  XLSX.utils.book_append_sheet(wb, ws_inasistentes, 'Inasistentes')

  const filename = `Asistencia_${reunionSeleccionada.value.nombre}_${new Date().toLocaleDateString()}.xlsx`
  XLSX.writeFile(wb, filename)
}

// Utilidades
const formatearFecha = (fecha) => {
  return new Date(fecha).toLocaleDateString('es-PE', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatearHora = (fecha) => {
  return new Date(fecha).toLocaleTimeString('es-PE', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Lifecycle
onMounted(async () => {
  try {
    usuarioActual.value = authService.obtenerUsuario()
    console.log('Usuario actual:', usuarioActual.value)
    if (!usuarioActual.value) {
      mostrarAlert('No hay usuario autenticado', 'error')
      return
    }
    await cargarReuniones()
  } catch (error) {
    console.error('Error en onMounted:', error)
    mostrarAlert('Error cargando página', 'error')
  }
})

watch([filtroEstado, filtroTipo], () => {
  cargarReuniones()
})
</script>

<style scoped>
.reuniones-view {
  padding: 20px;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.view-header h1 {
  margin: 0;
  color: #1f2937;
  font-size: 28px;
}

.filtros {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.select-filter {
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 14px;
  background: white;
  cursor: pointer;
}

.tabla-container {
  overflow-x: auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tabla-reuniones {
  width: 100%;
  border-collapse: collapse;
}

.tabla-reuniones thead {
  background: #f3f4f6;
  border-bottom: 2px solid #e5e7eb;
}

.tabla-reuniones th {
  padding: 12px;
  text-align: left;
  font-weight: 600;
  color: #374151;
  font-size: 14px;
}

.tabla-reuniones td {
  padding: 12px;
  border-bottom: 1px solid #e5e7eb;
  font-size: 14px;
}

.tabla-reuniones tbody tr:hover {
  background: #f9fafb;
}

.nombre {
  font-weight: 500;
  color: #4f46e5;
  cursor: pointer;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.tipo-asamblea { background: #dbeafe; color: #1e40af; }
.tipo-reunion { background: #d1fae5; color: #065f46; }
.tipo-ordinaria { background: #fcd34d; color: #78350f; }
.tipo-extraordinaria { background: #fed7aa; color: #92400e; }
.tipo-sesion { background: #e9d5ff; color: #6b21a8; }

.estado-programada { background: #e0e7ff; color: #3730a3; }
.estado-en_curso { background: #dcfce7; color: #166534; }
.estado-finalizada { background: #f3f4f6; color: #4b5563; }
.estado-cancelada { background: #fee2e2; color: #991b1b; }

.asistentes {
  font-weight: 600;
  color: #4f46e5;
}

.acciones {
  display: flex;
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  color: #6b7280;
  transition: color 0.2s;
}

.btn-icon:hover {
  color: #4f46e5;
}

.btn-danger:hover {
  color: #dc2626;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  margin: 0;
  color: #1f2937;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #374151;
  font-weight: 500;
  font-size: 14px;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 14px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.checkboxes {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.checkboxes label {
  display: flex;
  align-items: center;
  margin: 0;
  cursor: pointer;
}

.checkboxes input {
  margin-right: 8px;
}

.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding: 20px;
  border-top: 1px solid #e5e7eb;
}

/* Sidebar */
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: flex-end;
  z-index: 999;
}

.sidebar {
  background: white;
  width: 85%;
  max-width: 980px;
  height: 100%;
  overflow-y: auto;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

.sidebar-hero {
  position: relative;
  padding: 30px 20px;
  color: white;
  overflow: hidden;
}

.hero-gradient {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #4f46e5, #7c3aed, #a855f7);
  z-index: -1;
}

.hero-content {
  position: relative;
}

.hero-content h2 {
  margin: 0 0 12px 0;
  font-size: 24px;
}

.badges {
  display: flex;
  gap: 8px;
}

.btn-cerrar {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  border-radius: 4px;
  padding: 4px 8px;
}

.info-rapida {
  display: flex;
  gap: 20px;
  padding: 20px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #374151;
  font-size: 14px;
}

.info-item ion-icon {
  color: #4f46e5;
  font-size: 18px;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #e5e7eb;
}

.tab-btn {
  flex: 1;
  padding: 12px;
  background: none;
  border: none;
  cursor: pointer;
  color: #6b7280;
  font-weight: 500;
  border-bottom: 3px solid transparent;
  transition: all 0.2s;
}

.tab-btn.active {
  color: #4f46e5;
  border-bottom-color: #4f46e5;
}

.tab-content {
  padding: 20px;
}

.tab-pane h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #1f2937;
}

.botones-asistencia {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.btn-grande {
  padding: 20px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  transition: background 0.2s;
}

.btn-grande:hover {
  background: #4338ca;
}

.btn-grande ion-icon {
  font-size: 24px;
}

.cambiar-estado {
  grid-column: 1 / -1;
  padding: 12px;
  background: #f3f4f6;
  border-radius: 8px;
  display: flex;
  gap: 8px;
  align-items: center;
}

.cambiar-estado label {
  margin: 0;
  font-size: 14px;
}

.panel-escaneo {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.panel-escaneo h3 {
  margin: 0;
}

.panel-escaneo video {
  border-radius: 8px;
  width: 100%;
  height: auto;
}

.resultado {
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
}

.resultado.exito {
  background: #dcfce7;
  color: #166534;
}

.resultado.error {
  background: #fee2e2;
  color: #991b1b;
}

.resultado ion-icon {
  font-size: 32px;
}

.resultado p {
  margin: 0;
  font-weight: 500;
}

.asistentes-list,
.inasistentes-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.asistente-item,
.inasistente-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.asistente-item .info {
  flex: 1;
}

.asistente-item .nombre,
.inasistente-item .nombre {
  margin: 0;
  font-weight: 500;
  color: #1f2937;
  font-size: 14px;
}

.asistente-item .dni,
.inasistente-item .dni {
  margin: 0;
  color: #6b7280;
  font-size: 13px;
}

.asistente-item .hora {
  margin: 0;
  color: #9ca3af;
  font-size: 12px;
}

.metodo-qr { background: #dbeafe; color: #1e40af; }
.metodo-facial { background: #e0e7ff; color: #3730a3; }
.metodo-manual { background: #f3e8ff; color: #581c87; }

.stats,
.stats-reporte {
  color: #6b7280;
  font-size: 14px;
  margin-bottom: 16px;
}

.stats-reporte {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.stat {
  background: #f9fafb;
  padding: 12px;
  border-radius: 8px;
  text-align: center;
}

.stat .label {
  display: block;
  color: #6b7280;
  font-size: 13px;
  margin-bottom: 4px;
}

.stat .valor {
  display: block;
  font-size: 20px;
  font-weight: 600;
  color: #4f46e5;
}

.sin-datos {
  color: #9ca3af;
  text-align: center;
  padding: 20px;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #4338ca;
}

.btn-secondary {
  padding: 10px 16px;
  background: #6b7280;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: #4b5563;
}

.btn-small {
  padding: 6px 12px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
}

.alert {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 16px 20px;
  border-radius: 8px;
  font-weight: 500;
  z-index: 2000;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from { transform: translateY(100%); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.alert-success {
  background: #dcfce7;
  color: #166534;
}

.alert-error {
  background: #fee2e2;
  color: #991b1b;
}

@media (max-width: 768px) {
  .reuniones-view {
    padding: 12px;
  }

  .view-header {
    flex-direction: column;
    gap: 12px;
  }

  .botones-asistencia {
    grid-template-columns: 1fr;
  }

  .sidebar {
    width: 100%;
    max-width: none;
  }

  .stats-reporte {
    grid-template-columns: 1fr;
  }
}
</style>
