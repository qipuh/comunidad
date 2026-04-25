<template>
  <div class="factiliza-manager">
    <div class="manager-header">
      <h3>
        <ion-icon name="id-card-outline"></ion-icon>
        Consultor de DNI - Factiliza
      </h3>
      <div class="header-actions">
        <button @click="testConexion" class="btn-secondary" :disabled="testing">
          <ion-icon name="checkmark-circle-outline"></ion-icon>
          {{ testing ? 'Probando...' : 'Probar Conexión' }}
        </button>
        <button @click="toggleConfigPanel" class="btn-secondary">
          <ion-icon name="settings-outline"></ion-icon>
          Configurar
        </button>
      </div>
    </div>

    <!-- Configuration Panel -->
    <div v-if="showConfigPanel" class="config-panel">
      <div class="config-form">
        <div class="form-group">
          <label>URL del Endpoint</label>
          <input v-model="config.endpoint_url" type="text" placeholder="https://api.factiliza.com">
        </div>
        <div class="form-group">
          <label>Token de Autenticación</label>
          <input v-model="config.auth_token" type="password" placeholder="Tu token API">
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Timeout (segundos)</label>
            <input v-model.number="config.timeout_segundos" type="number" min="5" max="120">
          </div>
          <div class="form-group">
            <label>Máx. Reintentos</label>
            <input v-model.number="config.max_reintentos" type="number" min="1" max="10">
          </div>
        </div>
        <div class="form-actions">
          <button @click="saveConfig" class="btn-primary" :disabled="saving">
            <ion-icon name="checkmark-outline"></ion-icon>
            {{ saving ? 'Guardando...' : 'Guardar Configuración' }}
          </button>
          <button @click="toggleConfigPanel" class="btn-outline">Cancelar</button>
        </div>
      </div>
    </div>

    <!-- Status Alert -->
    <div v-if="statusMessage" :class="['alert', statusType]">
      <ion-icon :name="statusType === 'success' ? 'checkmark-circle' : 'alert-circle'"></ion-icon>
      {{ statusMessage }}
    </div>

    <!-- Consultar DNI Section -->
    <div class="consultar-dni-section">
      <h4>Consultar DNI</h4>
      <div class="dni-form">
        <div class="form-row">
          <div class="form-group">
            <label>Número de DNI</label>
            <input
              v-model="numeroDNI"
              type="text"
              placeholder="Ej: 12345678"
              @keyup.enter="consultarDNI"
              maxlength="8"
            >
          </div>
          <button @click="consultarDNI" class="btn-primary" :disabled="consultando || !numeroDNI">
            <ion-icon name="search-outline"></ion-icon>
            {{ consultando ? 'Consultando...' : 'Consultar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Datos de Persona -->
    <div v-if="datosPersona" class="datos-persona-section">
      <h4>Datos de la Persona</h4>
      <div class="datos-grid">
        <div class="dato-item">
          <span class="label">Nombre Completo</span>
          <span class="valor">{{ datosPersona.nombre_completo || 'N/A' }}</span>
        </div>
        <div class="dato-item">
          <span class="label">Número de DNI</span>
          <span class="valor">{{ datosPersona.numero_dni }}</span>
        </div>
        <div class="dato-item">
          <span class="label">Fecha de Nacimiento</span>
          <span class="valor">{{ datosPersona.fecha_nacimiento || 'N/A' }}</span>
        </div>
        <div class="dato-item">
          <span class="label">Sexo</span>
          <span class="valor">{{ datosPersona.sexo || 'N/A' }}</span>
        </div>
        <div class="dato-item">
          <span class="label">Dirección</span>
          <span class="valor">{{ datosPersona.direccion || 'N/A' }}</span>
        </div>
        <div class="dato-item">
          <span class="label">Departamento</span>
          <span class="valor">{{ datosPersona.departamento || 'N/A' }}</span>
        </div>
        <div class="dato-item">
          <span class="label">Provincia</span>
          <span class="valor">{{ datosPersona.provincia || 'N/A' }}</span>
        </div>
        <div class="dato-item">
          <span class="label">Distrito</span>
          <span class="valor">{{ datosPersona.distrito || 'N/A' }}</span>
        </div>
        <div class="dato-item">
          <span class="label">Estado Civil</span>
          <span class="valor">{{ datosPersona.estado_civil || 'N/A' }}</span>
        </div>
        <div class="dato-item">
          <span class="label">Edad</span>
          <span class="valor">{{ datosPersona.edad || 'N/A' }}</span>
        </div>
      </div>
    </div>

    <!-- Historial de Consultas -->
    <div class="historial-consultas">
      <h4>Historial de Consultas</h4>
      <div v-if="historial.length === 0" class="empty-state">
        <ion-icon name="document-outline"></ion-icon>
        <p>No hay consultas realizadas</p>
      </div>
      <div v-else class="consultas-list">
        <div v-for="consulta in historial" :key="consulta.id" class="consulta-item">
          <div class="consulta-info">
            <h5>{{ consulta.nombre_completo }}</h5>
            <p class="dni">DNI: {{ consulta.numero_dni }}</p>
            <p class="fecha">{{ new Date(consulta.fecha).toLocaleString() }}</p>
          </div>
          <div class="consulta-estado">
            <span :class="['estado', consulta.estado]">{{ consulta.estado }}</span>
          </div>
          <div class="consulta-actions">
            <button class="btn-icon" @click="cargarConsulta(consulta.id)" title="Ver detalles">
              <ion-icon name="eye-outline"></ion-icon>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import factilizaService from '@/services/factiliza.service'

const showConfigPanel = ref(false)
const testing = ref(false)
const saving = ref(false)
const consultando = ref(false)
const statusMessage = ref('')
const statusType = ref('success')

const config = reactive({
  endpoint_url: 'https://api.factiliza.com',
  auth_token: '',
  timeout_segundos: 30,
  max_reintentos: 3
})

const numeroDNI = ref('')
const datosPersona = ref(null)

const historial = ref([
  {
    id: 1,
    numero_dni: '12345678',
    nombre_completo: 'Juan Pérez García',
    fecha: '2026-04-25T14:30:00',
    estado: 'Exitosa'
  },
  {
    id: 2,
    numero_dni: '87654321',
    nombre_completo: 'María López Rodríguez',
    fecha: '2026-04-24T10:15:00',
    estado: 'Exitosa'
  },
  {
    id: 3,
    numero_dni: '11223344',
    nombre_completo: 'Carlos Sánchez Pérez',
    fecha: '2026-04-23T09:45:00',
    estado: 'Exitosa'
  }
])

const toggleConfigPanel = () => {
  showConfigPanel.value = !showConfigPanel.value
}

const testConexion = async () => {
  testing.value = true
  statusMessage.value = ''
  try {
    const result = await factilizaService.testConexion()
    statusMessage.value = 'Conexión exitosa con Factiliza'
    statusType.value = 'success'
  } catch (error) {
    statusMessage.value = 'Error en la conexión: ' + error.message
    statusType.value = 'error'
  } finally {
    testing.value = false
  }
}

const saveConfig = async () => {
  saving.value = true
  statusMessage.value = ''
  try {
    await factilizaService.updateConfig(config)
    statusMessage.value = 'Configuración guardada exitosamente'
    statusType.value = 'success'
    showConfigPanel.value = false
  } catch (error) {
    statusMessage.value = 'Error al guardar configuración: ' + error.message
    statusType.value = 'error'
  } finally {
    saving.value = false
  }
}

const consultarDNI = async () => {
  if (!numeroDNI.value || numeroDNI.value.length !== 8) {
    statusMessage.value = 'Por favor ingresa un DNI válido (8 dígitos)'
    statusType.value = 'error'
    return
  }

  consultando.value = true
  statusMessage.value = ''
  try {
    const result = await factilizaService.consultarDNI(numeroDNI.value)
    datosPersona.value = result.data
    statusMessage.value = `Datos de ${result.data.nombre_completo} obtenidos exitosamente`
    statusType.value = 'success'

    // Agregar al historial si no está
    const existe = historial.value.find(h => h.numero_dni === numeroDNI.value)
    if (!existe) {
      historial.value.unshift({
        id: Date.now(),
        numero_dni: numeroDNI.value,
        nombre_completo: result.data.nombre_completo,
        fecha: new Date().toISOString(),
        estado: 'Exitosa'
      })
    }
  } catch (error) {
    statusMessage.value = 'Error al consultar DNI: ' + error.message
    statusType.value = 'error'
    datosPersona.value = null
  } finally {
    consultando.value = false
  }
}

const cargarConsulta = async (idConsulta) => {
  try {
    const result = await factilizaService.obtenerConsulta(idConsulta)
    datosPersona.value = result.data
    statusMessage.value = 'Consulta cargada exitosamente'
    statusType.value = 'success'
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } catch (error) {
    statusMessage.value = 'Error al cargar consulta: ' + error.message
    statusType.value = 'error'
  }
}
</script>

<style scoped>
.factiliza-manager {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.manager-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.manager-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.manager-header h3 ion-icon {
  font-size: 24px;
  color: #6d28d9;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-secondary {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: #f1f5f9;
  color: #4f46e5;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}

.btn-secondary:hover:not(:disabled) {
  background: #e0e7ff;
  border-color: #4f46e5;
}

.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary ion-icon {
  font-size: 16px;
}

/* Config Panel */
.config-panel {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.config-form {
  max-width: 600px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #1e293b;
  font-size: 14px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  color: #1e293b;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
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
  font-size: 14px;
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #4338ca;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary ion-icon {
  font-size: 18px;
}

.btn-outline {
  padding: 10px 16px;
  background: white;
  color: #64748b;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.btn-outline:hover {
  border-color: #64748b;
  color: #1e293b;
}

/* Alert */
.alert {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 6px;
  margin-bottom: 20px;
  font-size: 14px;
  font-weight: 500;
}

.alert ion-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.alert.success {
  background: #dcfce7;
  color: #166534;
}

.alert.error {
  background: #fee2e2;
  color: #991b1b;
}

/* Consultar DNI Section */
.consultar-dni-section,
.datos-persona-section,
.historial-consultas {
  margin-bottom: 28px;
}

.consultar-dni-section h4,
.datos-persona-section h4,
.historial-consultas h4 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 16px 0;
}

.dni-form {
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
}

.dni-form .form-row {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.dni-form .form-group {
  flex: 1;
}

/* Datos de Persona */
.datos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.dato-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 6px;
}

.dato-item .label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.dato-item .valor {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #94a3b8;
}

.empty-state ion-icon {
  font-size: 48px;
  color: #cbd5e1;
  margin-bottom: 12px;
}

.consultas-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.consulta-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  transition: all 0.2s;
}

.consulta-item:hover {
  border-color: #4f46e5;
  background: #f0f4ff;
}

.consulta-info h5 {
  font-size: 15px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.consulta-info .dni {
  font-size: 13px;
  color: #64748b;
  margin: 4px 0 0 0;
}

.consulta-info .fecha {
  font-size: 12px;
  color: #94a3b8;
  margin: 2px 0 0 0;
}

.consulta-estado {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.consulta-estado .estado {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.consulta-estado .estado.Exitosa {
  background: #dcfce7;
  color: #166534;
}

.consulta-estado .estado.Error {
  background: #fee2e2;
  color: #991b1b;
}

.consulta-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 6px;
  display: flex;
  align-items: center;
  transition: color 0.2s;
}

.btn-icon:hover {
  color: #4f46e5;
}

.btn-icon ion-icon {
  font-size: 18px;
}
</style>
