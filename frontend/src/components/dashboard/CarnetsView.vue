<template>
  <div class="carnets-container">
    <!-- Toolbar -->
    <div class="carnet-toolbar">
      <button class="btn-config" @click="mostrarConfigModal = true">
        <ion-icon name="settings-outline"></ion-icon>
        Configurar carnet
      </button>
      <button class="btn-togglear-vista" @click="vistaPreview = !vistaPreview">
        <ion-icon :name="vistaPreview ? 'eye-outline' : 'grid-outline'"></ion-icon>
        {{ vistaPreview ? 'Vista Individual' : 'Vista Previsualización' }}
      </button>
      <button class="btn-exportar-todos" @click="exportarTodosPDF">
        <ion-icon name="download-outline"></ion-icon>
        Exportar todos (PDF)
      </button>
    </div>

    <!-- Modal de Configuración -->
    <div v-if="mostrarConfigModal" class="modal-overlay" @click.self="mostrarConfigModal = false">
      <div class="modal-config">
        <div class="modal-header">
          <h2>Configurar Carnet Comunero</h2>
          <button class="btn-close" @click="mostrarConfigModal = false">&times;</button>
        </div>

        <div class="modal-body">
          <!-- Textos -->
          <div class="config-section">
            <h3>Textos del Carnet</h3>
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
          </div>

          <!-- Imágenes -->
          <div class="config-section">
            <h3>Imágenes del Carnet</h3>

            <div class="imagen-upload">
              <label>Bandera/Logo Anverso:</label>
              <input type="file" @change="e => cargarImagen(e, 'bandera')" accept="image/*" class="file-input">
              <div v-if="configCarnet.bandera_url" class="imagen-preview">
                <img :src="configCarnet.bandera_url" alt="Bandera">
              </div>
            </div>

            <div class="imagen-upload">
              <label>Escudo Reverso:</label>
              <input type="file" @change="e => cargarImagen(e, 'escudo')" accept="image/*" class="file-input">
              <div v-if="configCarnet.escudo_url" class="imagen-preview">
                <img :src="configCarnet.escudo_url" alt="Escudo">
              </div>
            </div>

            <div class="imagen-upload">
              <label>Fondo Anverso:</label>
              <input type="file" @change="e => cargarImagen(e, 'fondo_anverso')" accept="image/*" class="file-input">
              <div v-if="configCarnet.fondo_anverso_url" class="imagen-preview">
                <img :src="configCarnet.fondo_anverso_url" alt="Fondo Anverso">
              </div>
            </div>

            <div class="imagen-upload">
              <label>Fondo Reverso:</label>
              <input type="file" @change="e => cargarImagen(e, 'fondo_reverso')" accept="image/*" class="file-input">
              <div v-if="configCarnet.fondo_reverso_url" class="imagen-preview">
                <img :src="configCarnet.fondo_reverso_url" alt="Fondo Reverso">
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-secondary" @click="mostrarConfigModal = false">Cancelar</button>
          <button class="btn-primary" @click="guardarConfiguracion">Guardar</button>
        </div>
      </div>
    </div>

    <!-- Vista de Previsualización -->
    <div v-if="vistaPreview" class="carnet-preview-container">
      <div class="carnet-preview-grid">
        <div v-for="usuario in usuarios" :key="usuario.id" class="carnet-preview-item">
          <!-- ANVERSO -->
          <div :id="`preview-anverso-${usuario.id}`" class="carnet-card anverso">
            <!-- Fondo -->
            <img v-if="configCarnet.fondo_anverso_url" :src="configCarnet.fondo_anverso_url" class="carnet-fondo">
            <div v-else class="carnet-fondo-default"></div>

            <!-- Contenido del anverso -->
            <div class="carnet-content">
              <!-- Top section: Logo + Título + N° Carnet -->
              <div class="carnet-top">
                <div class="carnet-logo-section">
                  <img v-if="configCarnet.bandera_url" :src="configCarnet.bandera_url" class="carnet-logo">
                  <div v-else class="carnet-logo-placeholder"></div>
                </div>

                <div class="carnet-title">
                  <div class="titulo-principal">{{ configCarnet.nombre_comunidad }}</div>
                  <div class="titulo-subtitulo">{{ configCarnet.subtitulo }}</div>
                  <div class="titulo-resolucion">{{ configCarnet.resolucion }}</div>
                </div>

                <div class="carnet-numero">
                  <div class="label-numero">N° CARNET</div>
                  <div class="valor-numero">{{ obtenerNumeroCarnet(usuario) }}</div>
                </div>
              </div>

              <!-- Body: Foto + Datos -->
              <div class="carnet-body">
                <div class="foto-section">
                  <div class="foto-box">
                    <img v-if="usuario.foto_frontal" :src="usuario.foto_frontal" class="foto-usuario">
                    <div v-else class="foto-placeholder">SIN FOTO</div>
                  </div>
                  <div class="foto-label">CARNET COMUNERO</div>
                </div>

                <div class="datos-section">
                  <div class="dato-line">
                    <span class="dato-label">APELLIDOS:</span>
                    <span class="dato-valor">{{ obtenerApellidos(usuario) }}</span>
                  </div>
                  <div class="dato-line">
                    <span class="dato-label">NOMBRES:</span>
                    <span class="dato-valor">{{ obtenerNombres(usuario) }}</span>
                  </div>
                </div>
              </div>

              <!-- Footer: Fechas y firmas -->
              <div class="carnet-footer">
                <div class="fechas-section">
                  <div class="fecha-item">
                    <span class="fecha-label">Fecha de Emisión</span>
                    <span class="fecha-valor">{{ obtenerFechaEmision() }}</span>
                  </div>
                  <div class="fecha-item">
                    <span class="fecha-label">Fecha de Caducidad</span>
                    <span class="fecha-valor">{{ obtenerFechaCaducidad() }}</span>
                  </div>
                </div>

                <div class="firmas-section">
                  <div class="firma-item">_______________<br>SECRETARIO</div>
                  <div class="firma-item">_______________<br>PRESIDENTE</div>
                </div>
              </div>
            </div>
          </div>

          <!-- REVERSO -->
          <div :id="`preview-reverso-${usuario.id}`" class="carnet-card reverso">
            <!-- Fondo -->
            <img v-if="configCarnet.fondo_reverso_url" :src="configCarnet.fondo_reverso_url" class="carnet-fondo">
            <div v-else class="carnet-fondo-default"></div>

            <!-- Contenido del reverso -->
            <div class="carnet-content">
              <!-- QR + Escudo izquierda -->
              <div class="reverso-left">
                <div class="reverso-header">
                  <div class="reverso-titulo">CC.TPCT</div>
                  <img v-if="configCarnet.escudo_url" :src="configCarnet.escudo_url" class="escudo">
                  <div v-else class="escudo-placeholder"></div>
                </div>

                <div class="qr-section">
                  <canvas :id="`preview-qr-canvas-${usuario.id}`" class="qr-canvas"></canvas>
                </div>
              </div>

              <!-- Datos derecha -->
              <div class="reverso-right">
                <div class="dato-reverso-item">
                  <span class="dato-reverso-label">N° CARNET:</span>
                  <span class="dato-reverso-valor">{{ obtenerNumeroCarnet(usuario) }}</span>
                </div>
                <div class="dato-reverso-item">
                  <span class="dato-reverso-label">DNI:</span>
                  <span class="dato-reverso-valor">{{ usuario.numero_dni }}</span>
                </div>
                <div class="dato-reverso-item">
                  <span class="dato-reverso-label">F. NACIMIENTO:</span>
                  <span class="dato-reverso-valor">{{ usuario.fecha_nacimiento || '-' }}</span>
                </div>
                <div class="dato-reverso-item">
                  <span class="dato-reverso-label">CATEGORÍA:</span>
                  <span class="dato-reverso-valor">COMUNERO(A)</span>
                </div>
                <div class="dato-reverso-item">
                  <span class="dato-reverso-label">ANEXO:</span>
                  <span class="dato-reverso-valor">{{ usuario.anexo || '-' }}</span>
                </div>

                <div class="numero-carnet-reverso">{{ obtenerNumeroCarnet(usuario) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Vista Individual (Original) -->
    <div v-else class="carnet-individual-container">
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
        <div class="carnet-tabs">
          <button
            class="tab-btn"
            :class="{ active: tabActivo === 'anverso' }"
            @click="tabActivo = 'anverso'"
          >
            Anverso
          </button>
          <button
            class="tab-btn"
            :class="{ active: tabActivo === 'reverso' }"
            @click="tabActivo = 'reverso'"
          >
            Reverso
          </button>
        </div>

        <div class="carnet-viewport">
          <!-- ANVERSO individual -->
          <div v-if="tabActivo === 'anverso'" :id="`carnet-anverso-${usuarioSeleccionado.id}`" class="carnet-card anverso individual">
            <img v-if="configCarnet.fondo_anverso_url" :src="configCarnet.fondo_anverso_url" class="carnet-fondo">
            <div v-else class="carnet-fondo-default"></div>

            <div class="carnet-content">
              <div class="carnet-top">
                <div class="carnet-logo-section">
                  <img v-if="configCarnet.bandera_url" :src="configCarnet.bandera_url" class="carnet-logo">
                  <div v-else class="carnet-logo-placeholder"></div>
                </div>

                <div class="carnet-title">
                  <div class="titulo-principal">{{ configCarnet.nombre_comunidad }}</div>
                  <div class="titulo-subtitulo">{{ configCarnet.subtitulo }}</div>
                  <div class="titulo-resolucion">{{ configCarnet.resolucion }}</div>
                </div>

                <div class="carnet-numero">
                  <div class="label-numero">N° CARNET</div>
                  <div class="valor-numero">{{ obtenerNumeroCarnet(usuarioSeleccionado) }}</div>
                </div>
              </div>

              <div class="carnet-body">
                <div class="foto-section">
                  <div class="foto-box">
                    <img v-if="usuarioSeleccionado.foto_frontal" :src="usuarioSeleccionado.foto_frontal" class="foto-usuario">
                    <div v-else class="foto-placeholder">SIN FOTO</div>
                  </div>
                  <div class="foto-label">CARNET COMUNERO</div>
                </div>

                <div class="datos-section">
                  <div class="dato-line">
                    <span class="dato-label">APELLIDOS:</span>
                    <span class="dato-valor">{{ obtenerApellidos(usuarioSeleccionado) }}</span>
                  </div>
                  <div class="dato-line">
                    <span class="dato-label">NOMBRES:</span>
                    <span class="dato-valor">{{ obtenerNombres(usuarioSeleccionado) }}</span>
                  </div>
                </div>
              </div>

              <div class="carnet-footer">
                <div class="fechas-section">
                  <div class="fecha-item">
                    <span class="fecha-label">Fecha de Emisión</span>
                    <span class="fecha-valor">{{ obtenerFechaEmision() }}</span>
                  </div>
                  <div class="fecha-item">
                    <span class="fecha-label">Fecha de Caducidad</span>
                    <span class="fecha-valor">{{ obtenerFechaCaducidad() }}</span>
                  </div>
                </div>

                <div class="firmas-section">
                  <div class="firma-item">_______________<br>SECRETARIO</div>
                  <div class="firma-item">_______________<br>PRESIDENTE</div>
                </div>
              </div>
            </div>
          </div>

          <!-- REVERSO individual -->
          <div v-else :id="`carnet-reverso-${usuarioSeleccionado.id}`" class="carnet-card reverso individual">
            <img v-if="configCarnet.fondo_reverso_url" :src="configCarnet.fondo_reverso_url" class="carnet-fondo">
            <div v-else class="carnet-fondo-default"></div>

            <div class="carnet-content">
              <div class="reverso-left">
                <div class="reverso-header">
                  <div class="reverso-titulo">CC.TPCT</div>
                  <img v-if="configCarnet.escudo_url" :src="configCarnet.escudo_url" class="escudo">
                  <div v-else class="escudo-placeholder"></div>
                </div>

                <div class="qr-section">
                  <canvas :id="`qr-canvas-${usuarioSeleccionado.id}`" class="qr-canvas"></canvas>
                </div>
              </div>

              <div class="reverso-right">
                <div class="dato-reverso-item">
                  <span class="dato-reverso-label">N° CARNET:</span>
                  <span class="dato-reverso-valor">{{ obtenerNumeroCarnet(usuarioSeleccionado) }}</span>
                </div>
                <div class="dato-reverso-item">
                  <span class="dato-reverso-label">DNI:</span>
                  <span class="dato-reverso-valor">{{ usuarioSeleccionado.numero_dni }}</span>
                </div>
                <div class="dato-reverso-item">
                  <span class="dato-reverso-label">F. NACIMIENTO:</span>
                  <span class="dato-reverso-valor">{{ usuarioSeleccionado.fecha_nacimiento || '-' }}</span>
                </div>
                <div class="dato-reverso-item">
                  <span class="dato-reverso-label">CATEGORÍA:</span>
                  <span class="dato-reverso-valor">COMUNERO(A)</span>
                </div>
                <div class="dato-reverso-item">
                  <span class="dato-reverso-label">ANEXO:</span>
                  <span class="dato-reverso-valor">{{ usuarioSeleccionado.anexo || '-' }}</span>
                </div>

                <div class="numero-carnet-reverso">{{ obtenerNumeroCarnet(usuarioSeleccionado) }}</div>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import QRCode from 'qrcode'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'

export default {
  name: 'CarnetsView',
  setup() {
    const route = useRoute()
    const usuarios = ref([])
    const usuarioSeleccionado = ref(null)
    const busqueda = ref('')
    const tabActivo = ref('anverso')
    const vistaPreview = ref(false)
    const mostrarConfigModal = ref(false)
    const cargando = ref(false)

    const configCarnet = ref({
      nombre_comunidad: 'COMUNIDAD CAMPESINA',
      subtitulo: 'TUMILACA, POCATA, COSCORE Y TALA',
      resolucion: 'RESOLUCIÓN SUPREMA 07 SET 1949',
      bandera_url: null,
      escudo_url: null,
      fondo_anverso_url: null,
      fondo_reverso_url: null
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
        const response = await fetch('/api/usuarios/?limit=100', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        })
        const data = await response.json()
        if (data.success) {
          usuarios.value = data.data
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
        const response = await fetch('/api/admin/configuracion/carnet', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        })
        const data = await response.json()
        configCarnet.value = data
      } catch (error) {
        console.error('Error cargando configuración del carnet:', error)
      }
    }

    const cargarImagen = (event, tipo) => {
      const file = event.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          const campo = {
            bandera: 'bandera_url',
            escudo: 'escudo_url',
            fondo_anverso: 'fondo_anverso_url',
            fondo_reverso: 'fondo_reverso_url'
          }[tipo]
          configCarnet.value[campo] = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }

    const guardarConfiguracion = async () => {
      try {
        cargando.value = true

        // Guardar textos
        const params = new URLSearchParams({
          nombre_comunidad: configCarnet.value.nombre_comunidad,
          subtitulo: configCarnet.value.subtitulo,
          resolucion: configCarnet.value.resolucion
        })

        await fetch(`/api/admin/configuracion/carnet?${params}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' }
        })

        // Guardar imágenes
        const tipos = ['bandera', 'escudo', 'fondo_anverso', 'fondo_reverso']
        for (const tipo of tipos) {
          const inputEl = document.querySelector(`input[accept="image/*"]`)
          if (inputEl && inputEl.files.length > 0) {
            const formData = new FormData()
            formData.append('file', inputEl.files[0])

            const uploadResponse = await fetch(`/api/admin/configuracion/carnet/upload?tipo=${tipo}`, {
              method: 'POST',
              body: formData
            })

            if (uploadResponse.ok) {
              const uploadData = await uploadResponse.json()
              const campo = {
                bandera: 'bandera_url',
                escudo: 'escudo_url',
                fondo_anverso: 'fondo_anverso_url',
                fondo_reverso: 'fondo_reverso_url'
              }[tipo]
              configCarnet.value[campo] = uploadData.url
            }
          }
        }

        mostrarConfigModal.value = false
        alert('Configuración guardada exitosamente')
      } catch (error) {
        console.error('Error guardando configuración:', error)
        alert('Error al guardar configuración')
      } finally {
        cargando.value = false
      }
    }

    const obtenerNumeroCarnet = (usuario) => {
      const id = String(usuario.id).padStart(3, '0')
      return id + usuario.numero_dni
    }

    const obtenerApellidos = (usuario) => {
      const nombre = usuario.nombre_completo || ''
      const partes = nombre.split(' ')
      if (partes.length >= 2) {
        return partes.slice(1).join(' ').toUpperCase()
      }
      return nombre.toUpperCase()
    }

    const obtenerNombres = (usuario) => {
      const nombre = usuario.nombre_completo || ''
      const partes = nombre.split(' ')
      return (partes[0] || '').toUpperCase()
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
        await generarQR(usuarioSeleccionado.value, `qr-canvas-${usuarioSeleccionado.value.id}`)
        await new Promise(r => setTimeout(r, 200))

        const anversoEl = document.getElementById(`carnet-anverso-${usuarioSeleccionado.value.id}`)
        const reversoEl = document.getElementById(`carnet-reverso-${usuarioSeleccionado.value.id}`)

        if (!anversoEl || !reversoEl) {
          console.error('No se encontraron elementos del carnet')
          return
        }

        const pdf = new jsPDF({
          orientation: 'landscape',
          unit: 'mm',
          format: [95.6, 50]
        })

        const anversoCanvas = await html2canvas(anversoEl, { scale: 2, useCORS: true })
        const anversoImg = anversoCanvas.toDataURL('image/png')
        pdf.addImage(anversoImg, 'PNG', 0, 0, 95.6, 50)

        pdf.addPage([95.6, 50], 'landscape')
        const reversoCanvas = await html2canvas(reversoEl, { scale: 2, useCORS: true })
        const reversoImg = reversoCanvas.toDataURL('image/png')
        pdf.addImage(reversoImg, 'PNG', 0, 0, 95.6, 50)

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

    return {
      usuarios,
      usuarioSeleccionado,
      usuariosFiltrados,
      busqueda,
      tabActivo,
      vistaPreview,
      mostrarConfigModal,
      cargando,
      configCarnet,
      cargarImagen,
      guardarConfiguracion,
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

/* VISTA PREVIEW */
.carnet-preview-container {
  flex: 1;
  overflow-y: auto;
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
}

.carnet-preview-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.carnet-preview-item {
  display: grid;
  grid-template-columns: 95mm 95mm;
  gap: 0;
  page-break-after: avoid;
  page-break-inside: avoid;
}

/* CARNET CARD - 9.5cm × 5cm */
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
  background: #e9ecef;
  border: 1px solid #dee2e6;
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
  background: #e9ecef;
  border: 1px solid #dee2e6;
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
  gap: 12px;
  padding: 12px;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
  font-size: 13px;
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
  width: 40px;
  height: 40px;
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
  min-height: 300px;
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

@media print {
  .carnet-card {
    box-shadow: none;
    border: 0.5px solid #000;
  }

  .carnet-preview-item {
    page-break-after: avoid;
    page-break-inside: avoid;
    margin-bottom: 0;
  }
}
</style>
