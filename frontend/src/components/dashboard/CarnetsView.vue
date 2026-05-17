<template>
  <div class="carnets-container">
    <!-- Toolbar -->
    <div class="carnet-toolbar">
      <button class="btn-config" @click="mostrarConfigModal = true">
        <ion-icon name="settings-outline"></ion-icon>
        Configurar carnet
      </button>
      <button class="btn-exportar-todos" @click="exportarTodosPDF">
        <ion-icon name="download-outline"></ion-icon>
        Exportar todos (PDF)
      </button>
    </div>

    <!-- Modal de Configuración -->
    <div v-if="mostrarConfigModal" class="modal-overlay" @click.self="mostrarConfigModal = false">
      <div class="modal-config-advanced">
        <div class="modal-header">
          <h2>Configurar Carnet</h2>
          <button class="btn-close" @click="mostrarConfigModal = false">&times;</button>
        </div>

        <div class="modal-body-advanced">
          <!-- Panel Izquierdo: Formulario -->
          <div class="config-panel-form">
            <!-- Textos -->
            <div class="config-section">
              <h3><ion-icon name="document-text-outline"></ion-icon> Textos del Carnet</h3>
              <div class="form-group">
                <label>Nombre Comunidad:</label>
                <input v-model="configCarnet.nombre_comunidad" type="text" class="form-input">
              </div>
              <div class="form-group">
                <label>Subtítulo:</label>
                <input v-model="configCarnet.subtitulo" type="text" class="form-input">
              </div>
              <div class="form-group">
                <label>Resolución:</label>
                <input v-model="configCarnet.resolucion" type="text" class="form-input">
              </div>
              <div class="form-group">
                <label>Nombre Corto (Siglas):</label>
                <input v-model="configCarnet.nombre_corto" type="text" class="form-input" placeholder="CC.TPCT">
              </div>
            </div>

            <!-- Imágenes -->
            <div class="config-section">
              <h3><ion-icon name="images-outline"></ion-icon> Imágenes del Carnet</h3>
              <div class="imagenes-grid">
                <!-- Bandera Anverso -->
                <div
                  class="imagen-dropzone"
                  @click="clickInputBandera"
                  @dragover.prevent="dragOverItem = 'bandera'"
                  @dragleave.prevent="dragOverItem = null"
                  @drop.prevent="(e) => handleDrop(e, 'bandera')"
                  :class="{ 'drag-over': dragOverItem === 'bandera' }"
                >
                  <div class="dropzone-label">Bandera/Logo Anverso</div>
                  <div class="dropzone-content">
                    <div v-if="configCarnet.bandera_url" class="imagen-preview-grande">
                      <img :src="configCarnet.bandera_url" alt="Bandera">
                    </div>
                    <div v-else class="dropzone-placeholder">
                      <ion-icon name="cloud-upload-outline" class="dropzone-icon"></ion-icon>
                      <div class="dropzone-text">Arrastra aquí o haz clic</div>
                    </div>
                  </div>
                  <input
                    id="input-bandera"
                    type="file"
                    @change="e => cargarImagen(e, 'bandera')"
                    accept="image/*"
                    class="file-input-hidden"
                  >
                </div>

                <!-- Escudo Reverso -->
                <div
                  class="imagen-dropzone"
                  @click="clickInputEscudo"
                  @dragover.prevent="dragOverItem = 'escudo'"
                  @dragleave.prevent="dragOverItem = null"
                  @drop.prevent="(e) => handleDrop(e, 'escudo')"
                  :class="{ 'drag-over': dragOverItem === 'escudo' }"
                >
                  <div class="dropzone-label">Escudo Reverso</div>
                  <div class="dropzone-content">
                    <div v-if="configCarnet.escudo_url" class="imagen-preview-grande">
                      <img :src="configCarnet.escudo_url" alt="Escudo">
                    </div>
                    <div v-else class="dropzone-placeholder">
                      <ion-icon name="cloud-upload-outline" class="dropzone-icon"></ion-icon>
                      <div class="dropzone-text">Arrastra aquí o haz clic</div>
                    </div>
                  </div>
                  <input
                    id="input-escudo"
                    type="file"
                    @change="e => cargarImagen(e, 'escudo')"
                    accept="image/*"
                    class="file-input-hidden"
                  >
                </div>

                <!-- Fondo Anverso -->
                <div
                  class="imagen-dropzone"
                  @click="clickInputFondoAnverso"
                  @dragover.prevent="dragOverItem = 'fondo_anverso'"
                  @dragleave.prevent="dragOverItem = null"
                  @drop.prevent="(e) => handleDrop(e, 'fondo_anverso')"
                  :class="{ 'drag-over': dragOverItem === 'fondo_anverso' }"
                >
                  <div class="dropzone-label">Fondo Anverso</div>
                  <div class="dropzone-content">
                    <div v-if="configCarnet.fondo_anverso_url" class="imagen-preview-grande">
                      <img :src="configCarnet.fondo_anverso_url" alt="Fondo Anverso">
                    </div>
                    <div v-else class="dropzone-placeholder">
                      <ion-icon name="cloud-upload-outline" class="dropzone-icon"></ion-icon>
                      <div class="dropzone-text">Arrastra aquí o haz clic</div>
                    </div>
                  </div>
                  <input
                    id="input-fondo-anverso"
                    type="file"
                    @change="e => cargarImagen(e, 'fondo_anverso')"
                    accept="image/*"
                    class="file-input-hidden"
                  >
                </div>

                <!-- Fondo Reverso -->
                <div
                  class="imagen-dropzone"
                  @click="clickInputFondoReverso"
                  @dragover.prevent="dragOverItem = 'fondo_reverso'"
                  @dragleave.prevent="dragOverItem = null"
                  @drop.prevent="(e) => handleDrop(e, 'fondo_reverso')"
                  :class="{ 'drag-over': dragOverItem === 'fondo_reverso' }"
                >
                  <div class="dropzone-label">Fondo Reverso</div>
                  <div class="dropzone-content">
                    <div v-if="configCarnet.fondo_reverso_url" class="imagen-preview-grande">
                      <img :src="configCarnet.fondo_reverso_url" alt="Fondo Reverso">
                    </div>
                    <div v-else class="dropzone-placeholder">
                      <ion-icon name="cloud-upload-outline" class="dropzone-icon"></ion-icon>
                      <div class="dropzone-text">Arrastra aquí o haz clic</div>
                    </div>
                  </div>
                  <input
                    id="input-fondo-reverso"
                    type="file"
                    @change="e => cargarImagen(e, 'fondo_reverso')"
                    accept="image/*"
                    class="file-input-hidden"
                  >
                </div>

                <!-- Firma Secretario -->
                <div
                  class="imagen-dropzone"
                  @click="clickInputFirmaSecretario"
                  @dragover.prevent="dragOverItem = 'firma_secretario'"
                  @dragleave.prevent="dragOverItem = null"
                  @drop.prevent="(e) => handleDrop(e, 'firma_secretario')"
                  :class="{ 'drag-over': dragOverItem === 'firma_secretario' }"
                >
                  <div class="dropzone-label">Firma Secretario</div>
                  <div class="dropzone-content">
                    <div v-if="configCarnet.firma_secretario_url" class="imagen-preview-grande">
                      <img :src="configCarnet.firma_secretario_url" alt="Firma Secretario">
                    </div>
                    <div v-else class="dropzone-placeholder">
                      <ion-icon name="cloud-upload-outline" class="dropzone-icon"></ion-icon>
                      <div class="dropzone-text">Arrastra aquí o haz clic</div>
                    </div>
                  </div>
                  <input
                    id="input-firma-secretario"
                    type="file"
                    @change="e => cargarImagen(e, 'firma_secretario')"
                    accept="image/*"
                    class="file-input-hidden"
                  >
                </div>

                <!-- Firma Presidente -->
                <div
                  class="imagen-dropzone"
                  @click="clickInputFirmaPresidente"
                  @dragover.prevent="dragOverItem = 'firma_presidente'"
                  @dragleave.prevent="dragOverItem = null"
                  @drop.prevent="(e) => handleDrop(e, 'firma_presidente')"
                  :class="{ 'drag-over': dragOverItem === 'firma_presidente' }"
                >
                  <div class="dropzone-label">Firma Presidente</div>
                  <div class="dropzone-content">
                    <div v-if="configCarnet.firma_presidente_url" class="imagen-preview-grande">
                      <img :src="configCarnet.firma_presidente_url" alt="Firma Presidente">
                    </div>
                    <div v-else class="dropzone-placeholder">
                      <ion-icon name="cloud-upload-outline" class="dropzone-icon"></ion-icon>
                      <div class="dropzone-text">Arrastra aquí o haz clic</div>
                    </div>
                  </div>
                  <input
                    id="input-firma-presidente"
                    type="file"
                    @change="e => cargarImagen(e, 'firma_presidente')"
                    accept="image/*"
                    class="file-input-hidden"
                  >
                </div>
              </div>
            </div>
          </div>

          <!-- Panel Derecho: Previsualización -->
          <div class="config-panel-preview">
            <h3><ion-icon name="eye-outline"></ion-icon> Previsualización en Vivo</h3>
            <div class="preview-carnet-container">
              <div class="carnet-container-mini">
                <!-- ANVERSO mini -->
                <div class="lado-izquierdo-mini">
                  <div class="header-izquierdo-mini">
                    <div class="bandera-placeholder-mini">
                      <img v-if="configCarnet.bandera_url" :src="configCarnet.bandera_url" class="bandera-img-mini">
                    </div>
                    <div class="titulo-mini">
                      <div class="titulo-principal-mini">{{ configCarnet.nombre_comunidad }}</div>
                      <div class="titulo-subtitulo-mini">{{ configCarnet.resolucion }}</div>
                    </div>
                  </div>
                </div>

                <!-- REVERSO mini -->
                <div class="lado-derecho-mini">
                  <div class="siglas-mini">{{ configCarnet.nombre_corto }}</div>
                  <div class="escudo-placeholder-mini">
                    <img v-if="configCarnet.escudo_url" :src="configCarnet.escudo_url" class="escudo-img-mini">
                    <span v-else>[Escudo]</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-secondary" @click="mostrarConfigModal = false">Cancelar</button>
          <button class="btn-primary" @click="guardarConfiguracion">Guardar Cambios</button>
        </div>
      </div>
    </div>

    <!-- Vista Individual -->
    <div class="carnet-individual-container">
      <div class="usuarios-panel">
        <div class="search-box">
          <ion-icon name="search-outline"></ion-icon>
          <input v-model="busqueda" type="text" placeholder="Buscar usuario..." class="search-input">
        </div>
        <div class="usuarios-list">
          <button
            v-for="usuario in usuariosFiltrados"
            :key="usuario.id"
            class="usuario-item"
            :class="{ active: usuarioSeleccionado?.id === usuario.id }"
            @click="usuarioSeleccionado = usuario"
          >
            <div v-if="usuario.foto_frontal" class="usuario-avatar">
              <img :src="usuario.foto_frontal" :alt="usuario.nombre_completo" class="avatar-img">
            </div>
            <div v-else class="usuario-avatar avatar-placeholder">
              {{ usuario.nombre_completo?.charAt(0) || '?' }}
            </div>
            <div class="usuario-info">
              <div class="usuario-nombre">{{ usuario.nombre_completo }}</div>
              <div class="usuario-dni">DNI: {{ usuario.numero_dni }}</div>
            </div>
          </button>
        </div>
      </div>

      <div class="carnet-panel" v-if="usuarioSeleccionado">
        <div class="carnet-completo-viewport" :id="`carnet-completo-${usuarioSeleccionado.id}`">
          <div class="carnet-container">
            <!-- LADO IZQUIERDO (ANVERSO) -->
            <div class="lado-izquierdo" :style="{ backgroundImage: configCarnet.fondo_anverso_url ? `url(${configCarnet.fondo_anverso_url})` : 'none' }">
              <div class="header-izquierdo">
                <div class="bandera-placeholder">
                  <img v-if="configCarnet.bandera_url" :src="configCarnet.bandera_url" class="bandera-img">
                </div>
                <div>
                  <div class="titulo-comunidad">{{ configCarnet.nombre_comunidad }}</div>
                  <div class="sub-resolucion">{{ configCarnet.resolucion }}</div>
                </div>
              </div>

              <div class="num-carnet-container">
                <div class="etiqueta-carnet">N° CARNET</div>
                <div class="num-carnet">{{ obtenerNumeroCarnet(usuarioSeleccionado) }}</div>
              </div>

              <div class="info-bloque">
                <div class="foto-placeholder">
                  <img v-if="usuarioSeleccionado.foto_frontal" :src="usuarioSeleccionado.foto_frontal" class="foto-img">
                  <div class="texto-foto">CARNET COMUNERO</div>
                </div>

                <div class="datos-personales">
                  <div class="campo">
                    <span class="etiqueta">APELLIDOS:</span>
                    <span class="valor">{{ obtenerApellidos(usuarioSeleccionado) }}</span>
                  </div>
                  <div class="campo">
                    <span class="etiqueta">NOMBRES:</span>
                    <span class="valor">{{ obtenerNombres(usuarioSeleccionado) }}</span>
                  </div>

                  <div class="campo-fechas">
                    <div class="fecha-item">
                      <span class="f-etiqueta">Fecha de Emisión</span>
                      <span class="f-valor">{{ obtenerFechaEmision() }}</span>
                    </div>
                    <div class="fecha-item">
                      <span class="f-etiqueta">Fecha de Caducidad</span>
                      <span class="f-valor">{{ obtenerFechaCaducidad() }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="firmas-container">
                <div class="firma-box">
                  <div v-if="configCarnet.firma_secretario_url" class="firma-imagen">
                    <img :src="configCarnet.firma_secretario_url" alt="Firma Secretario">
                  </div>
                  <div v-else class="firma-placeholder">[Firma]</div>
                  <span>Secretario</span>
                </div>
                <div class="firma-box">
                  <div v-if="configCarnet.firma_presidente_url" class="firma-imagen">
                    <img :src="configCarnet.firma_presidente_url" alt="Firma Presidente">
                  </div>
                  <div v-else class="firma-placeholder">[Firma]</div>
                  <span>Presidente</span>
                </div>
              </div>
            </div>

            <!-- LADO DERECHO (REVERSO) -->
            <div class="lado-derecho" :style="{ backgroundImage: configCarnet.fondo_reverso_url ? `url(${configCarnet.fondo_reverso_url})` : 'none' }">
              <div class="header-derecho">
                <div class="siglas">{{ configCarnet.nombre_corto || 'CC.TPCT' }}</div>
                <div class="escudo-placeholder">
                  <img v-if="configCarnet.escudo_url" :src="configCarnet.escudo_url" class="escudo-img">
                  <span v-else>[Escudo]</span>
                </div>
              </div>

              <div class="footer-derecho">
                <div class="qr-container">
                  <canvas :id="`qr-canvas-completo-${usuarioSeleccionado.id}`" class="qr-placeholder"></canvas>
                  <div class="qr-codigo">{{ obtenerNumeroCarnet(usuarioSeleccionado) }}</div>
                </div>

                <div class="metadatos-derecha">
                  <div class="meta-item">
                    <span class="m-etiqueta">Número de DNI</span>
                    <span class="m-valor">{{ usuarioSeleccionado.numero_dni }}</span>
                  </div>
                  <div class="meta-item">
                    <span class="m-etiqueta">Categoría</span>
                    <span class="m-valor-destacado">COMUNERO(A)</span>
                  </div>
                  <div class="meta-item">
                    <span class="m-etiqueta">Fecha de Nacimiento</span>
                    <span class="m-valor">{{ usuarioSeleccionado.fecha_nacimiento || '-' }}</span>
                  </div>
                  <div class="meta-item">
                    <span class="m-etiqueta">Anexo que Pertenece</span>
                    <span class="m-valor">{{ usuarioSeleccionado.anexo || '-' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <button class="btn-exportar-individual" @click="exportarCarnetIndividual">
          <ion-icon name="download-outline"></ion-icon>
          Descargar este carnet (PDF)
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import QRCode from 'qrcode'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'
import api from '@/services/api'

export default {
  name: 'CarnetsView',
  setup() {
    const route = useRoute()
    const usuarios = ref([])
    const usuarioSeleccionado = ref(null)
    const busqueda = ref('')
    const tabActivo = ref('anverso')
    const mostrarConfigModal = ref(false)
    const cargando = ref(false)
    const dragOverItem = ref(null)

    const configCarnet = ref({
      nombre_comunidad: 'Comunidad Campesina Tumilaca, Pocata, Coscore y Tala',
      subtitulo: 'TUMILACA, POCATA, COSCORE Y TALA',
      resolucion: 'RESOLUCIÓN SUPREMA 07 SET 1949',
      nombre_corto: 'CC.TPCT',
      bandera_url: null,
      escudo_url: null,
      fondo_anverso_url: null,
      fondo_reverso_url: null,
      firma_secretario_url: null,
      firma_presidente_url: null
    })

    const usuariosFiltrados = computed(() => {
      if (!busqueda.value) return usuarios.value
      const q = busqueda.value.toLowerCase()
      return usuarios.value.filter(u =>
        u.nombre_completo?.toLowerCase().includes(q) ||
        u.numero_dni?.includes(q)
      )
    })

    const cargarUsuarios = async () => {
      try {
        cargando.value = true
        const response = await api.get('/usuarios/?limit=100')
        if (response.data.success) {
          usuarios.value = response.data.data
          if (usuarios.value.length > 0) {
            usuarioSeleccionado.value = usuarios.value[0]
          }
        }
      } catch (error) {
        console.error('Error cargando usuarios:', error)
      } finally {
        cargando.value = false
      }
    }

    const cargarConfigCarnet = async () => {
      try {
        const response = await api.get('/admin/configuracion/carnet')
        console.log('Configuración cargada:', response.data)
        configCarnet.value = { ...configCarnet.value, ...response.data }
        console.log('configCarnet actualizado:', configCarnet.value)
      } catch (error) {
        console.error('Error cargando configuración del carnet:', error)
      }
    }

    const cargarImagen = async (event, tipo) => {
      const file = event.target.files[0]
      if (!file) return

      try {
        const formData = new FormData()
        formData.append('file', file)

        const uploadResponse = await api.post(`/admin/configuracion/carnet/upload?tipo=${tipo}`, formData)
        const campo = {
          bandera: 'bandera_url',
          escudo: 'escudo_url',
          fondo_anverso: 'fondo_anverso_url',
          fondo_reverso: 'fondo_reverso_url',
          firma_secretario: 'firma_secretario_url',
          firma_presidente: 'firma_presidente_url'
        }[tipo]
        configCarnet.value[campo] = uploadResponse.data.url
      } catch (error) {
        let errorMsg = 'Error desconocido'
        if (error.response?.data?.detail) {
          errorMsg = error.response.data.detail
        }
        console.error('Error subiendo imagen:', error)
        alert(`Error al subir la imagen: ${errorMsg}`)
      }
    }

    const handleDrop = async (event, tipo) => {
      const files = event.dataTransfer.files
      if (files.length > 0) {
        const file = files[0]
        // Simular un cambio de input para reutilizar cargarImagen
        const fakeEvent = { target: { files: [file] } }
        await cargarImagen(fakeEvent, tipo)
      }
      dragOverItem.value = null
    }

    const clickInputBandera = () => {
      const input = document.getElementById('input-bandera')
      if (input) input.click()
    }

    const clickInputEscudo = () => {
      const input = document.getElementById('input-escudo')
      if (input) input.click()
    }

    const clickInputFondoAnverso = () => {
      const input = document.getElementById('input-fondo-anverso')
      if (input) input.click()
    }

    const clickInputFondoReverso = () => {
      const input = document.getElementById('input-fondo-reverso')
      if (input) input.click()
    }

    const clickInputFirmaSecretario = () => {
      const input = document.getElementById('input-firma-secretario')
      if (input) input.click()
    }

    const clickInputFirmaPresidente = () => {
      const input = document.getElementById('input-firma-presidente')
      if (input) input.click()
    }

    const guardarConfiguracion = async () => {
      try {
        cargando.value = true

        const params = {
          nombre_comunidad: configCarnet.value.nombre_comunidad,
          subtitulo: configCarnet.value.subtitulo,
          resolucion: configCarnet.value.resolucion,
          nombre_corto: configCarnet.value.nombre_corto
        }

        console.log('Guardando configuración:', params)

        const response = await api.put('/admin/configuracion/carnet', null, { params })
        mostrarConfigModal.value = false
        alert('Configuración guardada exitosamente')
      } catch (error) {
        let errorMsg = 'Error desconocido'
        if (error.response?.data?.detail) {
          errorMsg = error.response.data.detail
        } else if (error.response?.data) {
          errorMsg = JSON.stringify(error.response.data)
        }
        console.error('Error guardando configuración:', error)
        alert(`Error al guardar configuración: ${errorMsg}`)
      } finally {
        cargando.value = false
      }
    }

    const obtenerNumeroCarnet = (usuario) => {
      const id = String(usuario.id).padStart(3, '0')
      return id + usuario.numero_dni
    }

    const obtenerApellidos = (usuario) => {
      const apellidos = [usuario.apellido_paterno, usuario.apellido_materno]
        .filter(a => a && a.trim())
        .join(' ')
      return apellidos.toUpperCase()
    }

    const obtenerNombres = (usuario) => {
      return (usuario.nombres || '').toUpperCase()
    }

    const obtenerFechaEmision = () => {
      const hoy = new Date()
      return `${hoy.getDate().toString().padStart(2, '0')}/${(hoy.getMonth() + 1).toString().padStart(2, '0')}/${hoy.getFullYear()}`
    }

    const obtenerFechaCaducidad = () => {
      const hoy = new Date()
      const caducidad = new Date(hoy.getFullYear() + 4, hoy.getMonth(), hoy.getDate())
      return `${caducidad.getDate().toString().padStart(2, '0')}/${(caducidad.getMonth() + 1).toString().padStart(2, '0')}/${caducidad.getFullYear()}`
    }

    const generarQR = async (usuario, canvasId) => {
      if (!usuario) return
      const qrData = {
        dni: usuario.numero_dni,
        nombre: usuario.nombre_completo,
        carnet: obtenerNumeroCarnet(usuario)
      }
      try {
        setTimeout(async () => {
          const canvas = document.getElementById(canvasId)
          if (canvas) {
            await QRCode.toCanvas(canvas, JSON.stringify(qrData), {
              width: 150,
              margin: 1,
              color: { dark: '#000000', light: '#FFFFFF' }
            })
          }
        }, 50)
      } catch (error) {
        console.error('Error generando QR:', error)
      }
    }

    const exportarCarnetIndividual = async () => {
      if (!usuarioSeleccionado.value) return

      try {
        cargando.value = true
        await generarQR(usuarioSeleccionado.value, `qr-canvas-completo-${usuarioSeleccionado.value.id}`)
        await new Promise(r => setTimeout(r, 200))

        const carnetEl = document.getElementById(`carnet-completo-${usuarioSeleccionado.value.id}`)

        if (!carnetEl) {
          console.error('No se encontró el elemento del carnet')
          return
        }

        const pdf = new jsPDF({
          orientation: 'landscape',
          unit: 'mm',
          format: [254, 144]
        })

        const carnetCanvas = await html2canvas(carnetEl, { scale: 2, useCORS: true })
        const carnetImg = carnetCanvas.toDataURL('image/png')
        pdf.addImage(carnetImg, 'PNG', 0, 0, 254, 144)

        pdf.save(`carnet-${usuarioSeleccionado.value.numero_dni}.pdf`)
      } catch (error) {
        console.error('Error exportando carnet:', error)
        alert('Error al exportar carnet: ' + error.message)
      } finally {
        cargando.value = false
      }
    }

    const exportarTodosPDF = async () => {
      if (usuarios.value.length === 0) {
        alert('No hay usuarios para exportar')
        return
      }

      try {
        cargando.value = true

        const pdf = new jsPDF({
          orientation: 'landscape',
          unit: 'mm',
          format: 'A4'
        })

        let pageCount = 0
        const colWidth = 95.6
        const rowHeight = 50

        for (let idx = 0; idx < usuarios.value.length; idx++) {
          const usuario = usuarios.value[idx]
          usuarioSeleccionado.value = usuario

          await generarQR(usuario, `qr-canvas-${usuario.id}`)
          await new Promise(r => setTimeout(r, 100))

          const anversoEl = document.getElementById(`carnet-anverso-${usuario.id}`)
          if (!anversoEl) continue

          const carnetCanvas = await html2canvas(anversoEl, { scale: 1.5, useCORS: true })
          const carnetImg = carnetCanvas.toDataURL('image/png')

          const colIndex = idx % 2
          const rowIndex = Math.floor((idx % 4) / 2)

          const posX = 10 + (colIndex * (colWidth + 5))
          const posY = 10 + (rowIndex * (rowHeight + 5))

          pdf.addImage(carnetImg, 'PNG', posX, posY, colWidth - 5, rowHeight - 5)

          if ((idx + 1) % 4 === 0 && idx < usuarios.value.length - 1) {
            pdf.addPage('A4', 'landscape')
          }
        }

        pdf.save(`carnets-export-${new Date().getTime()}.pdf`)
        alert(`Exportados ${usuarios.value.length} carnets exitosamente`)
      } catch (error) {
        console.error('Error exportando todos los carnets:', error)
        alert('Error al exportar: ' + error.message)
      } finally {
        cargando.value = false
      }
    }

    onMounted(async () => {
      await cargarUsuarios()
      await cargarConfigCarnet()

      // Si viene con query param ?usuario=ID, seleccionar ese usuario
      const usuarioIdParam = route.query.usuario
      if (usuarioIdParam) {
        const encontrado = usuarios.value.find(u => u.id === parseInt(usuarioIdParam))
        if (encontrado) usuarioSeleccionado.value = encontrado
      }

      // Generar QR para todos cuando se carga
      for (const usuario of usuarios.value) {
        await generarQR(usuario, `preview-qr-canvas-${usuario.id}`)
      }
    })

    // Generar QR cuando se selecciona un usuario
    watch(() => usuarioSeleccionado.value, async (nuevoUsuario) => {
      if (nuevoUsuario && !vistaPreview.value) {
        await generarQR(nuevoUsuario, `qr-canvas-completo-${nuevoUsuario.id}`)
      }
    })

    // Recargar configuración cuando se abre la modal
    watch(() => mostrarConfigModal.value, async (estaAbierta) => {
      if (estaAbierta) {
        await cargarConfigCarnet()
      }
    })

    return {
      usuarios,
      usuarioSeleccionado,
      usuariosFiltrados,
      busqueda,
      tabActivo,
      mostrarConfigModal,
      cargando,
      dragOverItem,
      configCarnet,
      cargarImagen,
      handleDrop,
      guardarConfiguracion,
      clickInputBandera,
      clickInputEscudo,
      clickInputFondoAnverso,
      clickInputFondoReverso,
      clickInputFirmaSecretario,
      clickInputFirmaPresidente,
      obtenerNumeroCarnet,
      obtenerApellidos,
      obtenerNombres,
      obtenerFechaEmision,
      obtenerFechaCaducidad,
      exportarCarnetIndividual,
      exportarTodosPDF
    }
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.carnets-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  gap: 15px;
  padding: 20px;
}

/* TOOLBAR */
.carnet-toolbar {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  align-items: center;
}

.btn-config, .btn-togglear-vista, .btn-exportar-todos, .btn-primary, .btn-secondary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-config:hover, .btn-togglear-vista:hover, .btn-exportar-todos:hover, .btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
  background: #6c757d;
}

.btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-2px);
}

/* MODAL */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-config {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  font-size: 18px;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6c757d;
}

.modal-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.config-section h3 {
  margin: 0 0 15px 0;
  font-size: 14px;
  color: #333;
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
  gap: 8px;
}

.config-section h3 ion-icon {
  font-size: 18px;
  color: #667eea;
}

.config-section:first-child {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.config-section:first-child h3 {
  grid-column: 1 / -1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-bottom: 10px;
}

.form-group label {
  font-size: 12px;
  font-weight: 600;
}

.form-input {
  padding: 8px 12px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  font-size: 13px;
  font-family: inherit;
}

.imagen-upload {
  border: 1px solid #dee2e6;
  border-radius: 6px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-input {
  font-size: 12px;
}

.imagen-preview {
  width: 100px;
  height: 100px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  overflow: hidden;
}

.imagen-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.modal-footer {
  padding: 15px 20px;
  border-top: 1px solid #e9ecef;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* MODAL CONFIGURACIÓN AVANZADA */
.modal-config-advanced {
  background: white;
  border-radius: 8px;
  width: 95%;
  max-width: 1200px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.modal-body-advanced {
  display: grid;
  grid-template-columns: 1fr 40%;
  gap: 20px;
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.config-panel-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.config-panel-preview {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  height: fit-content;
  position: sticky;
  top: 0;
  max-height: 90vh;
  overflow-y: auto;
}

.config-panel-preview h3 {
  margin: 0 0 10px 0;
  font-size: 13px;
  color: #333;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.config-panel-preview h3 ion-icon {
  font-size: 16px;
  color: #667eea;
}

.preview-carnet-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  width: 100%;
}

.carnet-container-mini {
  width: 100%;
  aspect-ratio: 5.06 / 1.44;
  background-color: #ffffff;
  border: 1px solid #cccccc;
  display: flex;
  position: relative;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  font-family: 'Segoe UI', 'Roboto', sans-serif;
  overflow: hidden;
}

.carnet-container-mini::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 0;
  width: 1px;
  height: 100%;
  background-color: #cccccc;
}

.lado-izquierdo-mini, .lado-derecho-mini {
  width: 50%;
  height: 100%;
  position: relative;
  padding: 2%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 0.5vw;
}

.header-izquierdo-mini {
  display: flex;
  align-items: center;
  gap: 2%;
  width: 95%;
  font-size: 0.6vw;
}

.bandera-placeholder-mini {
  width: 8%;
  aspect-ratio: 2.5;
  background: linear-gradient(to bottom, #ffeb3b 50%, #e53935 50%);
  border: 0.5px solid #d32f2f;
  flex-shrink: 0;
  border-radius: 1px;
}

.bandera-img-mini {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.titulo-mini {
  flex: 1;
  line-height: 1.15;
  padding: 0 2%;
}

.titulo-principal-mini {
  font-weight: 700;
  font-size: 0.55vw;
}

.titulo-subtitulo-mini {
  font-size: 0.45vw;
  color: #666;
}

.lado-derecho-mini {
  justify-content: space-around;
  gap: 3%;
}

.siglas-mini {
  font-weight: 700;
  font-size: 0.55vw;
}

.escudo-placeholder-mini {
  width: 8%;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.35vw;
  color: #999;
  overflow: hidden;
  border-radius: 1px;
}

.escudo-img-mini {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.imagen-upload-group {
  /*border: 1px solid #dee2e6;*/
  border-radius: 6px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  /*background: #f8f9fa;*/
}

.imagen-label {
  font-size: 12px;
  font-weight: 600;
  color: #333;
}

.imagen-preview-small {
  width: 60px;
  height: 60px;
  /*border: 1px solid #dee2e6;*/
  border-radius: 4px;
  overflow: hidden;
}

.imagen-preview-small img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* DRAG AND DROP IMAGES */
.imagenes-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.imagen-dropzone {
  border: 2px dashed #667eea;
  border-radius: 6px;
  padding: 10px;
  background: #f8f9ff;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  min-height: 100px;
}

.imagen-dropzone:hover {
  border-color: #764ba2;
  background: #f0eeff;
}

.imagen-dropzone.drag-over {
  border-color: #764ba2;
  background: #e8e0ff;
  box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
  transform: scale(1.02);
}

.dropzone-content {
  cursor: pointer;
}

.dropzone-content:hover .dropzone-placeholder {
  color: #667eea;
}

.dropzone-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 15px 10px;
  gap: 6px;
  transition: all 0.2s;
}

.dropzone-icon {
  font-size: 28px;
  color: #667eea;
}

.dropzone-text {
  font-weight: 600;
  color: #333;
  font-size: 11px;
}

.dropzone-hint {
  font-size: 9px;
  color: #999;
  text-align: center;
}

.imagen-preview-grande {
  width: 100%;
  max-height: 80px;
  border-radius: 4px;
  overflow: hidden;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.imagen-preview-grande img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.file-input-hidden {
  display: none;
}

.btn-change {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 6px 12px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s;
}

.imagen-dropzone:hover .btn-change {
  opacity: 1;
}

.btn-change:hover {
  background: #764ba2;
}

/* CARNET COMPLETO - Anverso + Reverso */
.carnet-completo-viewport {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
  background: #f8f9fa;
  border-radius: 6px;
  padding: 20px;
  overflow: auto;
}

.carnet-container {
  width: 1012px;
  height: 288px;
  background-color: #ffffff;
  border: 1px solid #cccccc;
  display: flex;
  position: relative;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow: hidden;
}

.carnet-container::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 0;
  width: 1px;
  height: 100%;
  background-color: #cccccc;
  z-index: 10;
}


.lado-izquierdo, .lado-derecho {
  width: 50%;
  height: 100%;
  position: relative;
  padding: 20px 25px;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: scroll;
}

.lado-izquierdo::before, .lado-derecho::before {
  content: "";
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.65);
  z-index: 0;
  pointer-events: none;
}

.lado-izquierdo > *, .lado-derecho > * {
  position: relative;
  z-index: 1;
}

/* CARNET CARD - 9.5cm × 5cm (para vista previsualización) */
.carnet-card {
  position: relative;
  width: 95mm;
  height: 50mm;
  border: 1px solid #ccc;
  overflow: hidden;
  border-radius: 3mm;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  font-size: 7px;
}

.carnet-card.individual {
  width: 400px;
  height: 210px;
  font-size: 11px;
}

.carnet-fondo {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.35;
  z-index: 0;
}

.carnet-fondo-default {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
  z-index: 0;
}

.carnet-content {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 3mm;
  color: #1a1a1a;
}

/* ANVERSO */
.carnet-top {
  display: grid;
  grid-template-columns: 13mm 1fr 20mm;
  gap: 2mm;
  margin-bottom: 2mm;
  align-items: flex-start;
}

.carnet-logo-section {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 13mm;
}

.carnet-logo {
  width: 100%;
  height: 10mm;
  object-fit: contain;
}

.carnet-logo-placeholder {
  width: 100%;
  height: 10mm;
  /*background: #e9ecef;
  border: 1px solid #dee2e6;*/
}

.carnet-title {
  display: flex;
  flex-direction: column;
  gap: 0.5mm;
  font-size: 0.85em;
}

.titulo-principal {
  font-weight: bold;
  font-size: 0.9em;
  line-height: 1;
}

.titulo-subtitulo {
  font-size: 0.75em;
  color: #666;
  line-height: 1;
}

.titulo-resolucion {
  font-size: 0.65em;
  color: #999;
  line-height: 1;
}

.carnet-numero {
  display: flex;
  flex-direction: column;
  text-align: right;
  justify-content: flex-start;
  gap: 0.5mm;
}

.label-numero {
  font-size: 0.6em;
  font-weight: bold;
}

.valor-numero {
  font-weight: bold;
  font-size: 0.75em;
}

.carnet-body {
  display: grid;
  grid-template-columns: 28mm 1fr;
  gap: 2mm;
  flex: 1;
  min-height: 0;
}

.foto-section {
  display: flex;
  flex-direction: column;
  gap: 1mm;
  align-items: center;
}

.foto-box {
  width: 28mm;
  height: 35mm;
  border: 1px solid #1a1a1a;
  overflow: hidden;
  background: #f5f5f5;
}

.foto-usuario {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.foto-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 0.7em;
}

.foto-label {
  font-weight: bold;
  font-size: 0.65em;
  text-align: center;
  width: 100%;
}

.datos-section {
  display: flex;
  flex-direction: column;
  gap: 1.5mm;
  padding-right: 1mm;
}

.dato-line {
  display: grid;
  grid-template-columns: 35% 65%;
  gap: 1mm;
  align-items: center;
}

.dato-label {
  font-weight: bold;
  font-size: 0.7em;
}

.dato-valor {
  font-weight: bold;
  font-size: 0.75em;
}

.carnet-footer {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2mm;
  padding-top: 1.5mm;
  border-top: 0.5px solid #ccc;
  font-size: 0.65em;
  margin-top: auto;
}

.fechas-section {
  display: flex;
  flex-direction: column;
  gap: 0.5mm;
}

.fecha-item {
  display: flex;
  flex-direction: column;
  gap: 0.3mm;
  line-height: 1;
}

.fecha-label {
  font-weight: bold;
  font-size: 0.65em;
}

.fecha-valor {
  font-size: 0.7em;
}

.firmas-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1mm;
}

.firma-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  font-weight: bold;
  font-size: 0.6em;
  line-height: 1.1;
}

.firma-imagen {
  max-height: 55px;
  max-width: 110px;
  margin-bottom: 15px;
  object-fit: contain;
}

.firma-imagen img {
  max-height: 55px;
  max-width: 110px;
  object-fit: contain;
}

/* REVERSO */
.carnet-card.reverso .carnet-content {
  display: grid;
  grid-template-columns: 45mm 1fr;
  gap: 1.5mm;
  padding: 2mm;
}

.reverso-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
  border-right: 0.5px solid #ddd;
  padding-right: 1mm;
}

.reverso-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1mm;
}

.reverso-titulo {
  font-weight: bold;
  font-size: 0.8em;
}

.escudo {
  width: 12mm;
  height: 12mm;
  object-fit: contain;
}

.escudo-placeholder {
  width: 12mm;
  height: 12mm;
}

.qr-section {
  display: flex;
  align-items: center;
  justify-content: center;
}

.qr-canvas {
  width: 25mm !important;
  height: 25mm !important;
}

.reverso-right {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding-left: 1mm;
  font-size: 0.7em;
}

.dato-reverso-item {
  display: grid;
  grid-template-columns: 50% 50%;
  gap: 0.5mm;
  line-height: 1.1;
  align-items: center;
}

.dato-reverso-label {
  font-weight: bold;
  font-size: 0.65em;
}

.dato-reverso-valor {
  font-size: 0.7em;
}

.numero-carnet-reverso {
  font-weight: bold;
  font-size: 0.7em;
  margin-top: 1mm;
  padding-top: 1mm;
  border-top: 0.5px solid #ccc;
}

/* VISTA INDIVIDUAL */
.carnet-individual-container {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 20px;
  flex: 1;
  min-height: 0;
}

.usuarios-panel {
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  border: 1px solid #e9ecef;
  min-height: 0;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 6px;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
}

.usuarios-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
  flex: 1;
}

.usuario-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
  font-size: 12px;
}

.usuario-item:hover {
  border-color: #667eea;
  background: #f8f9ff;
}

.usuario-item.active {
  background: #667eea;
  border-color: #667eea;
  color: white;
}

.usuario-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  background: #e9ecef;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 16px;
}

.usuario-info {
  flex: 1;
  min-width: 0;
}

.usuario-nombre {
  font-weight: 600;
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.usuario-dni {
  font-size: 11px;
  opacity: 0.7;
  margin-top: 2px;
}

.carnet-panel {
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  min-height: 0;
}

.carnet-tabs {
  display: flex;
  gap: 10px;
  border-bottom: 2px solid #e9ecef;
}

.tab-btn {
  padding: 10px 20px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-weight: 500;
  color: #6c757d;
  transition: all 0.2s;
  font-size: 13px;
}

.tab-btn.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

.carnet-viewport {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
  background: #f8f9fa;
  border-radius: 6px;
  padding: 20px;
  min-height: 450px;
  overflow: auto;
}

.btn-exportar-individual {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  margin-top: auto;
}

.btn-exportar-individual:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
}

/* LADO IZQUIERDO (ANVERSO) */
.header-izquierdo {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 20px;
}

.bandera-placeholder {
  width: 65px;
  height: 40px;
  border: 1px solid #d32f2f;
  position: relative;
  flex-shrink: 0;
  overflow: hidden;
  background: linear-gradient(to bottom, #ffeb3b 50%, #e53935 50%);
}

.bandera-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.titulo-comunidad {
  font-size: 13.5px;
  font-weight: 700;
  color: #0d0d0d;
  line-height: 1.2;
  letter-spacing: 0.2px;
  max-width: 220px;
  word-wrap: break-word;
  white-space: normal;
  margin-top:-4px;
}

.sub-resolucion {
  font-size: 8.5px;
  font-weight: 600;
  color: #444;
  margin-top: 2px;
  letter-spacing: 0.4px;
  line-height: 1.2;
}

.num-carnet-container {
  position: absolute;
  top: 20px;
  right: 25px;
  text-align: right;
}

.etiqueta-carnet {
  font-size: 8px;
  font-weight: 600;
  color: #0d0d0d;
  letter-spacing: 0.5px;
}

.num-carnet {
  font-size: 15px;
  font-weight: 700;
  color: #0d0d0d;
  margin-top: 2px;
  letter-spacing: 0.2px;
  font-family: 'Courier New', monospace;
}

.info-bloque {
  display: flex;
  gap: 15px;
  margin-top: 5px;
}

.foto-placeholder {
  width: 108px;
  height: 135px;
  border: 1px solid #000000;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  padding-bottom: 4px;
  background: #f5f5f5;
  overflow: hidden;
}

.foto-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
}

.texto-foto {
  font-size: 7px;
  font-weight: 700;
  color: #000;
  letter-spacing: 0.3px;
  position: relative;
  z-index: 1;
  line-height: 1.2;
}

.datos-personales {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-top: 2px;
}

.campo {
  display: flex;
  flex-direction: column;
}

.campo .etiqueta {
  font-size: 8.5px;
  color: #666666;
  font-weight: 600;
  letter-spacing: 0.5px;
  line-height: 1.2;
}

.campo .valor {
  font-size: 14px;
  font-weight: 700;
  color: #0d0d0d;
  text-transform: uppercase;
  margin-top: 1px;
  letter-spacing: 0.3px;
  line-height: 1.3;
}

.campo-fechas {
  margin-top: 3px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.fecha-item .f-etiqueta {
  font-size: 10px;
  font-weight: 600;
  color: #616161;
}

.fecha-item .f-valor {
  font-size: 10px;
  font-weight: 700;
  color: #0d0d0d;
  text-transform: uppercase;
  letter-spacing: 0.2px;
  line-height: 1.2;
}

.firmas-container {
  position: absolute;
  bottom: 12px;
  right: 25px;
  display: flex;
  gap: 40px;
}

.firma-box {
  width: 75px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.firma-placeholder {
  width: 100%;
  height: 50px;
  border-bottom: 1px dashed #999;
  margin-bottom: 15px;
  opacity: 0.6;
  font-size: 10px;
  color: #002699;
  display: flex;
  align-items: center;
  justify-content: center;
  font-style: italic;
}

.firma-box span {
  font-size: 8px;
  font-weight: 600;
  color: #222;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  line-height: 1.2;
}

/* LADO DERECHO (REVERSO) */
.lado-derecho {
  padding: 20px 40px;
}

.header-derecho {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: fit-content;
  margin-left: 15px;
}

.siglas {
  font-size: 15px;
  font-weight: 700;
  color: #0d0d0d;
  letter-spacing: 0.5px;
  margin-bottom: 5px;
  font-family: 'Courier New', monospace;
}

.escudo-placeholder {
  width: 55px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 8px;
  color: #777;
  text-align: center;
  overflow: hidden;
}

.escudo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.footer-derecho {
  display: flex;
  align-items: flex-end;
  gap: 25px;
  position: absolute;
  bottom: 20px;
  left: 40px;
  right: 40px;
}

.qr-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.qr-placeholder {
  width: 110px;
  height: 110px;
  border: 1px solid #000;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 10px;
}

.qr-codigo {
  font-size: 11px;
  font-weight: 700;
  color: #0d0d0d;
  letter-spacing: 0.3px;
  font-family: 'Courier New', monospace;
}

.metadatos-derecha {
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: 35px;
  row-gap: 14px;
  flex-grow: 1;
  padding-bottom: 8px;
}

.meta-item {
  display: flex;
  flex-direction: column;
}

.meta-item .m-etiqueta {
  font-size: 8.5px;
  font-weight: 600;
  color: #666666;
  letter-spacing: 0.3px;
  text-transform: uppercase;
  line-height: 1.2;
}

.meta-item .m-valor {
  font-size: 14px;
  font-weight: 700;
  color: #0d0d0d;
  margin-top: 2px;
  letter-spacing: 0.2px;
  line-height: 1.3;
}

.meta-item .m-valor-destacado {
  font-size: 14px;
  font-weight: 700;
  color: #0d0d0d;
  margin-top: 2px;
  letter-spacing: 0.2px;
  line-height: 1.3;
}

@media print {
  .carnet-card {
    box-shadow: none;
    border: 0.5px solid #000;
  }
}
</style>
