<template>
  <div class="configurador-apis">
    <div class="header">
      <h2>🔌 Configurar Integraciones API</h2>
      <p class="subtitle">Gestiona conexiones con APIs externas (RENIEC, Facturiza, SUNAT, Custom)</p>
    </div>

    <button @click="mostrarNuevaAPI = true" class="btn-primary btn-lg">
      ➕ Nueva Integración
    </button>

    <!-- Lista de integraciones -->
    <div v-if="integraciones.length > 0" class="integraciones-list">
      <div class="list-header">
        <span class="col-nombre">Nombre</span>
        <span class="col-tipo">Tipo</span>
        <span class="col-status">Estado</span>
        <span class="col-actions">Acciones</span>
      </div>

      <div v-for="api in integraciones" :key="api.id" class="api-item">
        <div class="col-nombre">
          <strong>{{ api.nombre }}</strong>
          <div v-if="api.descripcion" class="api-descripcion">
            {{ api.descripcion }}
          </div>
        </div>

        <div class="col-tipo">
          <span class="badge tipo" :class="`tipo-${api.tipo}`">
            {{ tipoAPILabel(api.tipo) }}
          </span>
        </div>

        <div class="col-status">
          <span v-if="api.activa" class="status active">🟢 Activa</span>
          <span v-else class="status inactive">🔴 Inactiva</span>
        </div>

        <div class="col-actions">
          <button @click="probarAPI(api)" class="btn-test" :disabled="probando === api.id">
            {{ probando === api.id ? '⏳ Probando...' : '🧪 Probar' }}
          </button>
          <button @click="editarAPI(api)" class="btn-edit" title="Editar">
            ✏️ Editar
          </button>
          <button @click="confirmarEliminar(api)" class="btn-delete" title="Eliminar">
            🗑️
          </button>
        </div>
      </div>
    </div>

    <!-- Estado vacío -->
    <div v-else class="empty-state">
      <p>📭 No hay integraciones API configuradas</p>
      <p class="hint">Crea una para conectar con APIs externas como RENIEC o Facturiza</p>
    </div>

    <!-- Modal de Formulario -->
    <div v-if="mostrarFormulario" class="modal-overlay" @click.self="cerrarFormulario">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ editando ? '✏️ Editar Integración' : '➕ Nueva Integración' }}</h3>
          <button class="btn-close" @click="cerrarFormulario">✕</button>
        </div>

        <form @submit.prevent="guardarAPI" class="formulario">
          <!-- Nombre -->
          <div class="form-group">
            <label for="nombre">Nombre *</label>
            <input
              id="nombre"
              v-model="formulario.nombre"
              type="text"
              placeholder="RENIEC, Facturiza, etc."
              required
            />
          </div>

          <!-- Descripción -->
          <div class="form-group">
            <label for="descripcion">Descripción (opcional)</label>
            <textarea
              id="descripcion"
              v-model="formulario.descripcion"
              placeholder="Describe para qué sirve esta integración"
              rows="2"
            ></textarea>
          </div>

          <!-- Tipo de API -->
          <div class="form-group">
            <label for="tipo">Tipo de API *</label>
            <select id="tipo" v-model="formulario.tipo" required>
              <option value="">-- Seleccionar --</option>
              <option value="reniec">🇵🇪 RENIEC (DNI)</option>
              <option value="facturiza">📋 Facturiza (RUC)</option>
              <option value="sunat">🏛️ SUNAT (Contribuyentes)</option>
              <option value="custom">⚙️ API Personalizada</option>
            </select>
          </div>

          <!-- URL del Endpoint -->
          <div class="form-group">
            <label for="endpoint_url">URL del Endpoint *</label>
            <input
              id="endpoint_url"
              v-model="formulario.endpoint_url"
              type="url"
              placeholder="https://api.ejemplo.com/endpoint"
              required
            />
          </div>

          <!-- Tipo de Autenticación -->
          <div class="form-group">
            <label for="auth_type">Tipo de Autenticación *</label>
            <select id="auth_type" v-model="formulario.auth_type" required>
              <option value="">-- Seleccionar --</option>
              <option value="bearer">Bearer Token</option>
              <option value="api_key">API Key</option>
              <option value="oauth2">OAuth2</option>
              <option value="basic">Basic Auth</option>
            </select>
          </div>

          <!-- Token/Credenciales -->
          <div class="form-group">
            <label for="auth_token">
              {{ authTokenLabel() }} *
            </label>
            <input
              id="auth_token"
              v-model="formulario.auth_token"
              type="password"
              placeholder="Ingresa token o credencial"
              required
            />
            <small class="hint-text">🔒 Se encriptará antes de guardarse</small>
          </div>

          <!-- Configuración Avanzada -->
          <div class="advanced-section">
            <h4>⚙️ Configuración Avanzada</h4>

            <div class="form-group">
              <label for="timeout_segundos">Timeout (segundos)</label>
              <input
                id="timeout_segundos"
                v-model.number="formulario.timeout_segundos"
                type="number"
                min="5"
                max="120"
                placeholder="30"
              />
            </div>

            <div class="form-group">
              <label for="max_reintentos">Reintentos Máximos</label>
              <input
                id="max_reintentos"
                v-model.number="formulario.max_reintentos"
                type="number"
                min="1"
                max="5"
                placeholder="3"
              />
            </div>

            <div class="checkbox-group">
              <label>
                <input v-model="formulario.activa" type="checkbox" />
                Integración Activa
              </label>
            </div>
          </div>

          <!-- Botones -->
          <div class="modal-footer">
            <button type="button" @click="cerrarFormulario" class="btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn-primary" :disabled="guardando">
              {{ guardando ? '⏳ Guardando...' : '💾 Guardar' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal de Confirmación de Eliminación -->
    <div v-if="mostrarConfirmDelete" class="modal-overlay" @click.self="cancelarDelete">
      <div class="modal-confirm">
        <h3>⚠️ Confirmar Eliminación</h3>
        <p>¿Eliminar la integración <strong>{{ apiAEliminar?.nombre }}</strong>?</p>
        <p class="warning">Esta acción no se puede deshacer.</p>
        <div class="modal-footer">
          <button @click="cancelarDelete" class="btn-secondary">Cancelar</button>
          <button @click="eliminarAPI" class="btn-delete">Sí, Eliminar</button>
        </div>
      </div>
    </div>

    <!-- Modal de Resultado de Prueba -->
    <div v-if="mostrarResultadoPrueba" class="modal-overlay" @click.self="cerrarResultadoPrueba">
      <div class="modal-resultado">
        <button class="btn-close" @click="cerrarResultadoPrueba">✕</button>
        <div v-if="resultadoPrueba.disponible" class="resultado-success">
          <h3>✅ Integración Funcional</h3>
          <p class="mensaje">La API está respondiendo correctamente.</p>
          <div v-if="resultadoPrueba.datos" class="datos-prueba">
            <h4>Datos Obtenidos:</h4>
            <div class="json-display">
              {{ JSON.stringify(resultadoPrueba.datos, null, 2) }}
            </div>
          </div>
        </div>
        <div v-else class="resultado-error">
          <h3>❌ Error en Integración</h3>
          <p class="mensaje">{{ resultadoPrueba.error }}</p>
        </div>
        <div class="modal-footer">
          <button @click="cerrarResultadoPrueba" class="btn-secondary">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { configuracionService, type IntegracionAPI, type ResultadoProeba } from '@/services/configuracion.service'

const integraciones = ref<IntegracionAPI[]>([])
const mostrarFormulario = ref(false)
const mostrarConfirmDelete = ref(false)
const mostrarResultadoPrueba = ref(false)
const guardando = ref(false)
const probando = ref<number | null>(null)
const editando = ref(false)
const apiAEliminar = ref<IntegracionAPI | null>(null)
const resultadoPrueba = ref<ResultadoProeba>({ disponible: false })
const mostrarNuevaAPI = ref(false)

const formulario = ref({
  nombre: '',
  descripcion: '',
  tipo: '',
  endpoint_url: '',
  auth_type: '',
  auth_token: '',
  timeout_segundos: 30,
  max_reintentos: 3,
  activa: true
})

const formularioOriginal = ref({
  nombre: '',
  descripcion: '',
  tipo: '',
  endpoint_url: '',
  auth_type: '',
  auth_token: '',
  timeout_segundos: 30,
  max_reintentos: 3,
  activa: true
})

const cargarIntegraciones = async () => {
  try {
    integraciones.value = await configuracionService.obtenerIntegraciones()
  } catch (error) {
    console.error('Error cargando integraciones:', error)
  }
}

const tipoAPILabel = (tipo: string): string => {
  const labels: Record<string, string> = {
    reniec: '🇵🇪 RENIEC',
    facturiza: '📋 Facturiza',
    sunat: '🏛️ SUNAT',
    custom: '⚙️ Personalizada'
  }
  return labels[tipo] || tipo
}

const authTokenLabel = (): string => {
  const labels: Record<string, string> = {
    bearer: 'Bearer Token',
    api_key: 'API Key',
    oauth2: 'Access Token',
    basic: 'Credenciales (user:pass)'
  }
  return labels[formulario.value.auth_type] || 'Token/Credencial'
}

const editarAPI = (api: IntegracionAPI) => {
  editando.value = true
  formularioOriginal.value = { ...api }
  formulario.value = { ...api }
  mostrarFormulario.value = true
}

const guardarAPI = async () => {
  if (!formulario.value.nombre || !formulario.value.tipo || !formulario.value.endpoint_url || !formulario.value.auth_token) {
    console.error('Completa todos los campos requeridos')
    return
  }

  guardando.value = true
  try {
    if (editando.value && formularioOriginal.value.nombre) {
      const id = integraciones.value.find(a => a.nombre === formularioOriginal.value.nombre)?.id
      if (id) {
        await configuracionService.editarIntegracion(id, formulario.value)
      }
    } else {
      await configuracionService.crearIntegracion(formulario.value)
    }
    await cargarIntegraciones()
    cerrarFormulario()
  } catch (error) {
    console.error('Error guardando API:', error)
  } finally {
    guardando.value = false
  }
}

const probarAPI = async (api: IntegracionAPI) => {
  probando.value = api.id
  try {
    resultadoPrueba.value = await configuracionService.probarIntegracion(api.id)
    mostrarResultadoPrueba.value = true
  } catch (error) {
    console.error('Error probando API:', error)
    resultadoPrueba.value = {
      disponible: false,
      error: 'Error al conectar con la API'
    }
    mostrarResultadoPrueba.value = true
  } finally {
    probando.value = null
  }
}

const confirmarEliminar = (api: IntegracionAPI) => {
  apiAEliminar.value = api
  mostrarConfirmDelete.value = true
}

const eliminarAPI = async () => {
  if (!apiAEliminar.value) return

  try {
    await configuracionService.eliminarIntegracion(apiAEliminar.value.id)
    await cargarIntegraciones()
    mostrarConfirmDelete.value = false
    apiAEliminar.value = null
  } catch (error) {
    console.error('Error eliminando API:', error)
  }
}

const cerrarFormulario = () => {
  mostrarFormulario.value = false
  editando.value = false
  formulario.value = {
    nombre: '',
    descripcion: '',
    tipo: '',
    endpoint_url: '',
    auth_type: '',
    auth_token: '',
    timeout_segundos: 30,
    max_reintentos: 3,
    activa: true
  }
}

const cerrarResultadoPrueba = () => {
  mostrarResultadoPrueba.value = false
  resultadoPrueba.value = { disponible: false }
}

const cancelarDelete = () => {
  mostrarConfirmDelete.value = false
  apiAEliminar.value = null
}

watch(mostrarNuevaAPI, (newVal) => {
  if (newVal) {
    editando.value = false
    cerrarFormulario()
    mostrarFormulario.value = true
    mostrarNuevaAPI.value = false
  }
})

onMounted(() => {
  cargarIntegraciones()
})
</script>

<style scoped>
.configurador-apis {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  margin-bottom: 2rem;
}

.header h2 {
  font-size: 1.8rem;
  margin: 0 0 0.5rem 0;
  color: #333;
}

.subtitle {
  color: #666;
  margin: 0;
  font-size: 0.95rem;
}

.btn-primary.btn-lg {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  margin-bottom: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary.btn-lg:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 15px rgba(102, 126, 234, 0.3);
}

.integraciones-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.list-header {
  display: grid;
  grid-template-columns: 1fr 150px 120px 200px;
  gap: 1rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  color: #666;
  border-bottom: 2px solid #ddd;
}

.api-item {
  display: grid;
  grid-template-columns: 1fr 150px 120px 200px;
  gap: 1rem;
  padding: 1.5rem;
  background: white;
  border-radius: 8px;
  border: 1px solid #eee;
  align-items: center;
  transition: all 0.3s ease;
}

.api-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #667eea;
}

.col-nombre strong {
  display: block;
  font-size: 1rem;
  color: #333;
  margin-bottom: 0.25rem;
}

.api-descripcion {
  font-size: 0.85rem;
  color: #888;
  margin-top: 0.25rem;
}

.badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.tipo {
  background: #f0f0f0;
  color: #333;
}

.tipo-reniec {
  background: #e3f2fd;
  color: #1976d2;
}

.tipo-facturiza {
  background: #f3e5f5;
  color: #7b1fa2;
}

.tipo-sunat {
  background: #fff3e0;
  color: #e65100;
}

.tipo-custom {
  background: #e8f5e9;
  color: #388e3c;
}

.status {
  font-size: 0.9rem;
  font-weight: 600;
}

.status.active {
  color: #4caf50;
}

.status.inactive {
  color: #f44336;
}

.col-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.btn-test,
.btn-edit,
.btn-delete {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s ease;
}

.btn-test {
  background: #4caf50;
  color: white;
}

.btn-test:hover:not(:disabled) {
  background: #388e3c;
  transform: scale(1.05);
}

.btn-test:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-edit {
  background: #2196f3;
  color: white;
}

.btn-edit:hover {
  background: #1976d2;
  transform: scale(1.05);
}

.btn-delete {
  background: #f44336;
  color: white;
}

.btn-delete:hover {
  background: #da190b;
  transform: scale(1.05);
}

.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  background: #f9f9f9;
  border-radius: 8px;
  color: #666;
}

.empty-state p {
  margin: 0.5rem 0;
  font-size: 1rem;
}

.hint {
  color: #999;
  font-size: 0.9rem;
}

/* Modal Styles */
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

.modal-content,
.modal-confirm,
.modal-resultado {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.3rem;
  color: #333;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.btn-close:hover {
  background: #f0f0f0;
  color: #333;
}

.formulario {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
  font-size: 0.95rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.2s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.hint-text {
  color: #999;
  font-size: 0.85rem;
  margin-top: 0.25rem;
}

.advanced-section {
  border-top: 1px solid #eee;
  padding-top: 1rem;
  margin-top: 1rem;
}

.advanced-section h4 {
  margin: 0 0 1rem 0;
  color: #333;
  font-size: 1rem;
}

.checkbox-group {
  display: flex;
  align-items: center;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  margin: 0;
  font-weight: normal;
}

.checkbox-group input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #eee;
  justify-content: flex-end;
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.btn-primary:not(.btn-lg) {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-primary:not(.btn-lg):disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary:not(.btn-lg):not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.modal-confirm {
  padding: 2rem;
  text-align: center;
}

.modal-confirm h3 {
  font-size: 1.3rem;
  color: #333;
  margin: 0 0 1rem 0;
}

.modal-confirm p {
  color: #666;
  margin: 0.5rem 0;
  line-height: 1.6;
}

.modal-confirm .warning {
  color: #f44336;
  font-weight: 600;
}

.modal-resultado {
  padding: 2rem;
  position: relative;
}

.resultado-success,
.resultado-error {
  text-align: center;
}

.resultado-success h3 {
  color: #4caf50;
  font-size: 1.3rem;
  margin: 0 0 1rem 0;
}

.resultado-error h3 {
  color: #f44336;
  font-size: 1.3rem;
  margin: 0 0 1rem 0;
}

.resultado-success .mensaje,
.resultado-error .mensaje {
  color: #666;
  margin: 0 0 1.5rem 0;
}

.datos-prueba {
  text-align: left;
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 6px;
  margin-top: 1rem;
}

.datos-prueba h4 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.json-display {
  background: white;
  border: 1px solid #ddd;
  padding: 1rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  color: #333;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}

@media (max-width: 1024px) {
  .list-header,
  .api-item {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .col-nombre,
  .col-tipo,
  .col-status,
  .col-actions {
    display: flex;
    align-items: center;
  }

  .col-actions {
    justify-content: flex-start;
  }
}

@media (max-width: 600px) {
  .configurador-apis {
    padding: 1rem;
  }

  .header h2 {
    font-size: 1.4rem;
  }

  .modal-content,
  .modal-confirm,
  .modal-resultado {
    width: 95%;
  }

  .formulario {
    gap: 1rem;
  }
}
</style>
