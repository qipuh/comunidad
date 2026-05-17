<template>
  <div class="marca-view">
    <div class="view-header">
      <h1>Configuración de Marca</h1>
    </div>

    <div class="container">
      <!-- Formulario -->
      <div class="form-section">
        <h2>Información de la Organización</h2>

        <div class="form-group">
          <label>Nombre de la Página</label>
          <input v-model="form.nombre_pagina" type="text" placeholder="Ej: Mi Comunidad" />
        </div>

        <div class="form-group">
          <label>Subtítulo</label>
          <input v-model="form.subtitulo" type="text" placeholder="Ej: Sistema de Gestión" />
        </div>

        <div class="form-group">
          <label>Nombre Corto (para sidebar colapsado)</label>
          <input v-model="form.nombre_corto" type="text" maxlength="20" placeholder="Ej: COM" />
        </div>

        <div class="form-group">
          <label>Color Primario</label>
          <div class="color-input">
            <input v-model="form.color_primario" type="color" />
            <span class="color-value">{{ form.color_primario }}</span>
          </div>
        </div>

        <button class="btn-guardar" @click="guardarCambios">Guardar Cambios</button>
      </div>

      <!-- Imágenes -->
      <div class="images-section">
        <h2>Imágenes de Marca</h2>

        <!-- Logo -->
        <div class="image-block">
          <h3>Logo de la Aplicación</h3>
          <div class="image-preview">
            <img v-if="form.logo_url" :src="form.logo_url" alt="Logo" class="logo-preview" />
            <div v-else class="placeholder">No hay logo</div>
          </div>
          <div class="file-upload">
            <input ref="logoInput" type="file" accept="image/*" @change="selectLogoFile" />
            <button @click="$refs.logoInput.click()" class="btn-upload">
              <ion-icon name="cloud-upload-outline"></ion-icon>
              Cambiar Logo
            </button>
          </div>
          <p v-if="logoFile" class="file-info">Archivo seleccionado: {{ logoFile.name }}</p>
          <button v-if="logoFile" @click="subirLogo" class="btn-submit">Subir Logo</button>
        </div>

        <!-- Favicon -->
        <div class="image-block">
          <h3>Favicon (Icono de Pestaña)</h3>
          <div class="image-preview favicon">
            <img v-if="form.favicon_url" :src="form.favicon_url" alt="Favicon" class="favicon-preview" />
            <div v-else class="placeholder">No hay favicon</div>
          </div>
          <div class="file-upload">
            <input ref="faviconInput" type="file" accept="image/*" @change="selectFaviconFile" />
            <button @click="$refs.faviconInput.click()" class="btn-upload">
              <ion-icon name="cloud-upload-outline"></ion-icon>
              Cambiar Favicon
            </button>
          </div>
          <p v-if="faviconFile" class="file-info">Archivo seleccionado: {{ faviconFile.name }}</p>
          <button v-if="faviconFile" @click="subirFavicon" class="btn-submit">Subir Favicon</button>
        </div>
      </div>

      <!-- Preview -->
      <div class="preview-section">
        <h2>Vista Previa</h2>
        <div class="preview-box">
          <div class="preview-header" :style="{ backgroundColor: form.color_primario }">
            <img v-if="form.logo_url" :src="form.logo_url" alt="Logo" class="preview-logo" />
            <div v-else class="preview-logo-placeholder">Logo</div>
            <div class="preview-text">
              <div class="preview-title">{{ form.nombre_pagina }}</div>
              <div class="preview-subtitle">{{ form.subtitulo }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Alert -->
    <Alert
      :visible="alert.visible"
      :type="alert.type"
      :title="alert.title"
      :message="alert.message"
      :duration="alert.duration"
      @close="alert.visible = false"
    />

    <!-- Loading -->
    <div v-if="cargando" class="loading">
      <div class="spinner"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMarca, setMarca } from '@/composables/useMarca'
import { useAlert } from '@/composables/useAlert'
import Alert from '@/components/Alert.vue'
import api from '@/services/api'

const { alert, success, error } = useAlert()

const marca = useMarca()

const form = ref({
  nombre_pagina: 'Comunidad',
  subtitulo: 'Sistema de Gestión',
  nombre_corto: 'COM',
  logo_url: null,
  favicon_url: null,
  color_primario: '#4f46e5'
})

const logoInput = ref(null)
const faviconInput = ref(null)
const logoFile = ref(null)
const faviconFile = ref(null)
const cargando = ref(false)

const cargarMarca = async () => {
  try {
    const response = await api.get('/admin/configuracion/marca')
    form.value = { ...response.data }
  } catch (error) {
    error('Error', 'No se pudo cargar la configuración de marca')
  }
}

const guardarCambios = async () => {
  try {
    cargando.value = true
    const datos = {
      nombre_pagina: form.value.nombre_pagina,
      subtitulo: form.value.subtitulo,
      nombre_corto: form.value.nombre_corto,
      color_primario: form.value.color_primario
    }

    await api.put('/admin/configuracion/marca', datos)

    // Actualizar marca global
    setMarca(form.value)

    // Actualizar document.title
    document.title = form.value.nombre_pagina

    success('Éxito', 'Cambios guardados correctamente')
  } catch (error) {
    error('Error', 'No se pudieron guardar los cambios')
  } finally {
    cargando.value = false
  }
}

const selectLogoFile = (e) => {
  logoFile.value = e.target.files[0]
}

const selectFaviconFile = (e) => {
  faviconFile.value = e.target.files[0]
}

const subirLogo = async () => {
  if (!logoFile.value) return

  try {
    cargando.value = true
    const formData = new FormData()
    formData.append('file', logoFile.value)
    formData.append('tipo', 'logo')

    const response = await api.post('/admin/configuracion/marca/upload', formData, {
      params: { tipo: 'logo' }
    })

    form.value.logo_url = response.data.url
    setMarca({ logo_url: response.data.url })
    logoFile.value = null
    logoInput.value.value = ''

    success('Éxito', 'Logo subido correctamente')
  } catch (error) {
    error('Error', 'No se pudo subir el logo')
  } finally {
    cargando.value = false
  }
}

const subirFavicon = async () => {
  if (!faviconFile.value) return

  try {
    cargando.value = true
    const formData = new FormData()
    formData.append('file', faviconFile.value)
    formData.append('tipo', 'favicon')

    const response = await api.post('/admin/configuracion/marca/upload', formData, {
      params: { tipo: 'favicon' }
    })

    form.value.favicon_url = response.data.url
    setMarca({ favicon_url: response.data.url })

    // Actualizar favicon en el documento
    const link = document.querySelector('link[rel="icon"]')
    if (link) {
      link.href = response.data.url
    }

    faviconFile.value = null
    faviconInput.value.value = ''

    success('Éxito', 'Favicon subido correctamente')
  } catch (error) {
    error('Error', 'No se pudo subir el favicon')
  } finally {
    cargando.value = false
  }
}

onMounted(() => {
  cargarMarca()
})
</script>

<style scoped>
.marca-view {
  padding: 20px;
}

.view-header {
  margin-bottom: 30px;
}

.view-header h1 {
  margin: 0;
  color: #1f2937;
  font-size: 28px;
}

.container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.form-section,
.images-section,
.preview-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

h2 {
  margin: 0 0 20px 0;
  color: #1f2937;
  font-size: 20px;
}

h3 {
  margin: 0 0 12px 0;
  color: #374151;
  font-size: 16px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #374151;
  font-weight: 500;
  font-size: 14px;
}

input[type="text"],
input[type="color"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 14px;
}

.color-input {
  display: flex;
  gap: 12px;
  align-items: center;
}

input[type="color"] {
  width: 60px;
  height: 40px;
  cursor: pointer;
  padding: 2px;
}

.color-value {
  color: #6b7280;
  font-family: monospace;
  font-size: 13px;
}

.btn-guardar {
  width: 100%;
  padding: 12px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-guardar:hover {
  background: #4338ca;
}

.image-block {
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.image-block:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.image-preview {
  width: 100%;
  height: 150px;
  background: #f3f4f6;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.image-preview img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.image-preview.favicon {
  height: 80px;
}

.favicon-preview {
  width: 32px;
  height: 32px;
}

.placeholder {
  color: #9ca3af;
  font-size: 14px;
}

.file-upload {
  display: flex;
  gap: 8px;
}

input[type="file"] {
  display: none;
}

.btn-upload {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px;
  background: #f3f4f6;
  border: 2px solid #e5e7eb;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  transition: all 0.2s;
}

.btn-upload:hover {
  background: #e5e7eb;
}

.file-info {
  margin: 8px 0;
  color: #6b7280;
  font-size: 12px;
}

.btn-submit {
  width: 100%;
  padding: 10px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-submit:hover {
  background: #059669;
}

.preview-box {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.preview-header {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: white;
}

.preview-logo {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  object-fit: contain;
  background: rgba(255, 255, 255, 0.1);
  padding: 4px;
}

.preview-logo-placeholder {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 500;
  flex-shrink: 0;
}

.preview-text {
  flex: 1;
}

.preview-title {
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 2px;
}

.preview-subtitle {
  font-size: 12px;
  opacity: 0.9;
}


.loading {
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

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1024px) {
  .container {
    grid-template-columns: 1fr;
  }
}
</style>
