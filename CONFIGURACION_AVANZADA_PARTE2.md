# ⚙️ Configuración Avanzada – Parte 2: Componentes y Casos de Uso

**Continuación de [CONFIGURACION_CAMPOS_Y_APIS.md](CONFIGURACION_CAMPOS_Y_APIS.md)**

---

## 🎨 ConfiguradorAPIs.vue – Panel de Administración

```vue
<!-- frontend/src/components/admin/ConfiguradorAPIs.vue -->
<template>
  <div class="configurador-apis">
    <h2>Configurar Integraciones API</h2>
    
    <button @click="mostrarNuevaAPI = true" class="btn-primary">
      ➕ Nueva Integración
    </button>
    
    <div class="apis-grid">
      <div v-for="api in apis" :key="api.id" class="api-card">
        <div class="api-header">
          <h3>{{ api.nombre }}</h3>
          <span :class="['status', api.activa ? 'activa' : 'inactiva']">
            {{ api.activa ? '🟢 Activa' : '🔴 Inactiva' }}
          </span>
        </div>
        
        <p class="tipo">Tipo: <strong>{{ api.tipo }}</strong></p>
        <p class="endpoint">URL: <code>{{ api.endpoint_url }}</code></p>
        <p class="timeout">Timeout: {{ api.timeout_segundos }}s | Reintentos: {{ api.max_reintentos }}</p>
        
        <div class="card-actions">
          <button @click="probarConexion(api)" class="btn-test">
            🧪 Probar Conexión
          </button>
          <button @click="editarAPI(api)" class="btn-edit">
            ✏️ Editar
          </button>
          <button @click="eliminarAPI(api.id)" class="btn-delete">
            🗑️ Eliminar
          </button>
        </div>
        
        <div v-if="api.ultimaPrueba" class="ultima-prueba">
          <small>Última prueba: {{ formatoFecha(api.ultimaPrueba.timestamp) }}</small>
          <small :class="api.ultimaPrueba.exitosa ? 'exito' : 'error'">
            {{ api.ultimaPrueba.exitosa ? '✓ Exitosa' : '✗ Falló' }}
          </small>
        </div>
      </div>
    </div>
    
    <!-- Modal: Nueva/Editar API -->
    <div v-if="mostrarNuevaAPI" class="modal">
      <div class="modal-content">
        <h3>{{ editandoAPI ? 'Editar' : 'Nueva' }} Integración API</h3>
        
        <div class="form-group">
          <label>Nombre de la Integración *</label>
          <select v-model="formulario.nombre">
            <option value="">-- Seleccionar --</option>
            <option value="RENIEC">RENIEC (Perú)</option>
            <option value="Facturiza">Facturiza</option>
            <option value="SUNAT">SUNAT (RUC)</option>
            <option value="Custom">API Personalizada</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>Tipo *</label>
          <select v-model="formulario.tipo">
            <option value="reniec">RENIEC</option>
            <option value="facturiza">Facturiza</option>
            <option value="sunat">SUNAT</option>
            <option value="custom">Custom</option>
          </select>
        </div>
        
        <div class="info-api">
          <h4>ℹ️ Información sobre {{ formulario.nombre || 'la API' }}</h4>
          <div v-if="formulario.tipo === 'reniec'" class="info-box">
            <p><strong>RENIEC (Perú):</strong> Consulta de datos por DNI</p>
            <p>Endpoint: <code>https://api.reniec.gob.pe/dni/{dni}</code></p>
            <p>Auth: Bearer Token</p>
            <p>Retorna: nombres, apellidos, género, fecha_nacimiento, estado_civil</p>
          </div>
          
          <div v-else-if="formulario.tipo === 'facturiza'" class="info-box">
            <p><strong>Facturiza:</strong> Consulta de RUC y datos de empresa</p>
            <p>Endpoint: <code>https://api.facturiza.com/consultas/ruc</code></p>
            <p>Auth: API Key (header X-API-Key)</p>
            <p>Retorna: razon_social, direccion, representante, actividad_economica, estado</p>
          </div>
          
          <div v-else-if="formulario.tipo === 'sunat'" class="info-box">
            <p><strong>SUNAT RUC:</strong> Información de contribuyentes (Perú)</p>
            <p>Requiere: Certificado digital o token de acceso</p>
            <p>Retorna: nombre, domicilio, estado de contribuyente</p>
          </div>
        </div>
        
        <div class="form-group">
          <label>Endpoint URL *</label>
          <input v-model="formulario.endpoint_url" type="text" 
                 placeholder="https://api.reniec.gob.pe/dni/" />
        </div>
        
        <div class="form-group">
          <label>Tipo de Autenticación *</label>
          <select v-model="formulario.auth_type">
            <option value="bearer">Bearer Token</option>
            <option value="api_key">API Key</option>
            <option value="basic">Basic Auth</option>
            <option value="oauth2">OAuth2</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>
            {{ formulario.auth_type === 'api_key' ? 'API Key' : 
               formulario.auth_type === 'bearer' ? 'Bearer Token' : 
               'Credenciales' }} *
          </label>
          <input v-model="formulario.auth_token" type="password" 
                 placeholder="Ingresa tu token o API key" />
          <small>Será encriptado antes de guardarse</small>
        </div>
        
        <div class="form-group">
          <label>Timeout (segundos)</label>
          <input v-model.number="formulario.timeout_segundos" type="number" 
                 min="5" max="120" />
        </div>
        
        <div class="form-group">
          <label>Máximo de Reintentos</label>
          <input v-model.number="formulario.max_reintentos" type="number" 
                 min="1" max="5" />
        </div>
        
        <div class="form-group">
          <label>
            <input v-model="formulario.activa" type="checkbox" />
            Integración Activa
          </label>
        </div>
        
        <div class="modal-actions">
          <button @click="probarAntesDeGuardar" class="btn-test">
            🧪 Probar Primero
          </button>
          <button @click="guardarAPI" class="btn-success">
            💾 Guardar
          </button>
          <button @click="cancelar" class="btn-secondary">
            Cancelar
          </button>
        </div>
      </div>
    </div>
    
    <!-- Modal: Resultado Prueba -->
    <div v-if="mostrarResultadoPrueba" class="modal">
      <div class="modal-content resultado-prueba">
        <h3>Resultado de la Prueba</h3>
        
        <div :class="['resultado', resultadoPrueba.exitosa ? 'exitosa' : 'fallida']">
          <p v-if="resultadoPrueba.exitosa" class="icono">✅</p>
          <p v-else class="icono">❌</p>
          
          <p v-if="resultadoPrueba.exitosa" class="mensaje">
            ¡Conexión exitosa!
          </p>
          <p v-else class="mensaje">
            Error: {{ resultadoPrueba.error }}
          </p>
        </div>
        
        <div v-if="resultadoPrueba.datos" class="datos-retornados">
          <h4>Datos de Ejemplo Retornados:</h4>
          <pre>{{ JSON.stringify(resultadoPrueba.datos, null, 2) }}</pre>
        </div>
        
        <button @click="cerrarResultadoPrueba" class="btn-primary">
          Cerrar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '@/services/api'

interface IntegracionAPI {
  id: number
  nombre: string
  tipo: string
  endpoint_url: string
  auth_type: string
  activa: boolean
  timeout_segundos: number
  max_reintentos: number
  ultimaPrueba?: {
    timestamp: string
    exitosa: boolean
    error?: string
  }
}

const apis = ref<IntegracionAPI[]>([])
const mostrarNuevaAPI = ref(false)
const mostrarResultadoPrueba = ref(false)
const editandoAPI = ref(false)
const resultadoPrueba = ref<any>(null)

const formulario = ref({
  nombre: '',
  tipo: '',
  endpoint_url: '',
  auth_type: 'bearer',
  auth_token: '',
  timeout_segundos: 30,
  max_reintentos: 3,
  activa: true
})

onMounted(() => cargarAPIs())

const cargarAPIs = async () => {
  try {
    const res = await api.get('/admin/integraciones-api')
    apis.value = res.data.apis
  } catch (error) {
    console.error('Error cargando APIs:', error)
  }
}

const editarAPI = (integracion: IntegracionAPI) => {
  formulario.value = { ...integracion, auth_token: '' }
  editandoAPI.value = true
  mostrarNuevaAPI.value = true
}

const probarConexion = async (integracion: IntegracionAPI) => {
  try {
    const res = await api.post(`/admin/integraciones-api/${integracion.id}/probar`)
    resultadoPrueba.value = res.data
    mostrarResultadoPrueba.value = true
  } catch (error: any) {
    resultadoPrueba.value = {
      exitosa: false,
      error: error.response?.data?.detail || 'Error al conectar'
    }
    mostrarResultadoPrueba.value = true
  }
}

const probarAntesDeGuardar = async () => {
  try {
    const res = await api.post('/admin/integraciones-api/probar-temporal', formulario.value)
    resultadoPrueba.value = res.data
    mostrarResultadoPrueba.value = true
  } catch (error: any) {
    resultadoPrueba.value = {
      exitosa: false,
      error: error.response?.data?.detail || 'Error al conectar'
    }
    mostrarResultadoPrueba.value = true
  }
}

const guardarAPI = async () => {
  try {
    await api.post('/admin/integraciones-api', formulario.value)
    await cargarAPIs()
    cancelar()
  } catch (error) {
    console.error('Error guardando API:', error)
  }
}

const eliminarAPI = async (id: number) => {
  if (confirm('¿Eliminar esta integración?')) {
    try {
      await api.delete(`/admin/integraciones-api/${id}`)
      await cargarAPIs()
    } catch (error) {
      console.error('Error eliminando:', error)
    }
  }
}

const cancelar = () => {
  mostrarNuevaAPI.value = false
  editandoAPI.value = false
  formulario.value = {
    nombre: '',
    tipo: '',
    endpoint_url: '',
    auth_type: 'bearer',
    auth_token: '',
    timeout_segundos: 30,
    max_reintentos: 3,
    activa: true
  }
}

const cerrarResultadoPrueba = () => {
  mostrarResultadoPrueba.value = false
  resultadoPrueba.value = null
}

const formatoFecha = (fecha: string) => {
  return new Date(fecha).toLocaleString()
}
</script>

<style scoped>
.configurador-apis {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.apis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.api-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.api-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  border-bottom: 2px solid #f3f4f6;
  padding-bottom: 10px;
}

.api-header h3 {
  margin: 0;
  color: #1f2937;
}

.status {
  font-size: 12px;
  font-weight: 600;
}

.status.activa {
  color: #15803d;
}

.status.inactiva {
  color: #991b1b;
}

.tipo,
.endpoint,
.timeout {
  margin: 10px 0;
  color: #6b7280;
  font-size: 14px;
}

.endpoint code {
  background: #f3f4f6;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 12px;
  word-break: break-all;
}

.card-actions {
  display: flex;
  gap: 8px;
  margin-top: 15px;
}

.card-actions button {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
}

.btn-test {
  background: #dbeafe;
  color: #1e40af;
}

.btn-edit {
  background: #fef3c7;
  color: #92400e;
}

.btn-delete {
  background: #fee2e2;
  color: #991b1b;
}

.ultima-prueba {
  margin-top: 15px;
  padding: 10px;
  background: #f9fafb;
  border-radius: 4px;
  font-size: 12px;
}

.ultima-prueba small {
  display: block;
  color: #6b7280;
}

.ultima-prueba .exito {
  color: #15803d;
}

.ultima-prueba .error {
  color: #991b1b;
}

.modal {
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

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  max-width: 700px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.resultado-prueba {
  max-width: 500px;
}

.resultado {
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  margin: 20px 0;
}

.resultado.exitosa {
  background: #d1fae5;
  color: #065f46;
}

.resultado.fallida {
  background: #fee2e2;
  color: #991b1b;
}

.resultado .icono {
  font-size: 40px;
  margin: 0;
}

.resultado .mensaje {
  margin: 10px 0 0 0;
  font-size: 16px;
  font-weight: 600;
}

.datos-retornados {
  background: #f3f4f6;
  padding: 15px;
  border-radius: 4px;
  margin: 20px 0;
}

.datos-retornados pre {
  background: white;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 12px;
}

.info-api {
  background: #f0f9ff;
  padding: 15px;
  border-radius: 8px;
  margin: 15px 0;
  border-left: 4px solid #0284c7;
}

.info-box {
  background: white;
  padding: 10px;
  border-radius: 4px;
  margin: 10px 0;
  font-size: 13px;
  line-height: 1.6;
}

.info-box code {
  background: #e0e7ff;
  padding: 2px 6px;
  border-radius: 3px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #374151;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
}

.modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.modal-actions button {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-success {
  background: #10b981;
  color: white;
}

.btn-secondary {
  background: #e5e7eb;
  color: #374151;
}
</style>
```

---

## 📋 FormularioRegistroDinamico.vue

```vue
<!-- frontend/src/pages/RegistroDinamico.vue -->
<template>
  <div class="registro-dinamico">
    <h1>Registro de Usuario</h1>
    
    <form @submit.prevent="registrar">
      <!-- Campos dinámicos según configuración -->
      <div v-for="campo in camposConfiguracion" :key="campo.id" class="form-group">
        <label :for="campo.nombre_campo">
          {{ campo.etiqueta }}
          <span v-if="campo.es_obligatorio" class="requerido">*</span>
          <span v-if="campo.api_integracion_id" class="icono-api">🔗</span>
        </label>
        
        <!-- Input tipo texto -->
        <input
          v-if="['string', 'email', 'phone', 'url'].includes(campo.tipo_dato)"
          :id="campo.nombre_campo"
          v-model="formulario[campo.nombre_campo]"
          :type="getTipoInput(campo.tipo_dato)"
          :placeholder="campo.etiqueta"
          :required="campo.es_obligatorio"
          @blur="validarYConsultarAPI(campo)"
          class="input-field"
        />
        
        <!-- Input tipo número -->
        <input
          v-else-if="campo.tipo_dato === 'number'"
          :id="campo.nombre_campo"
          v-model.number="formulario[campo.nombre_campo]"
          type="number"
          :required="campo.es_obligatorio"
          class="input-field"
        />
        
        <!-- Input tipo fecha -->
        <input
          v-else-if="campo.tipo_dato === 'date'"
          :id="campo.nombre_campo"
          v-model="formulario[campo.nombre_campo]"
          type="date"
          :required="campo.es_obligatorio"
          class="input-field"
        />
        
        <!-- Selector para enum -->
        <select
          v-else-if="campo.tipo_dato === 'enum'"
          :id="campo.nombre_campo"
          v-model="formulario[campo.nombre_campo]"
          :required="campo.es_obligatorio"
          class="input-field"
        >
          <option value="">-- Seleccionar --</option>
          <option v-for="opcion in campo.valores_enum" :key="opcion" :value="opcion">
            {{ opcion }}
          </option>
        </select>
        
        <!-- Checkbox para booleano -->
        <label v-else-if="campo.tipo_dato === 'boolean'" class="checkbox-label">
          <input
            :id="campo.nombre_campo"
            v-model="formulario[campo.nombre_campo]"
            type="checkbox"
          />
          <span>{{ campo.etiqueta }}</span>
        </label>
        
        <!-- Indicador de carga para consultas API -->
        <div v-if="consultandoAPI[campo.nombre_campo]" class="loading">
          ⏳ Consultando datos...
        </div>
        
        <!-- Indicador de dato auto-llenado -->
        <div v-if="camposAutoLlenados[campo.nombre_campo]" class="auto-llenado">
          ✅ Datos auto-llenados desde {{ camposAutoLlenados[campo.nombre_campo] }}
        </div>
        
        <!-- Mostrar errores de validación -->
        <span v-if="erroresValidacion[campo.nombre_campo]" class="error">
          {{ erroresValidacion[campo.nombre_campo] }}
        </span>
      </div>
      
      <!-- Sección de fotos facial -->
      <div class="form-group">
        <h3>Captura de Rostro</h3>
        <FaceScanner @photos-captured="onFotosCapturadas" />
      </div>
      
      <!-- Botón de envío -->
      <button type="submit" class="btn-submit" :disabled="enviando">
        {{ enviando ? '⏳ Registrando...' : '✓ Registrar Usuario' }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { api } from '@/services/api'
import FaceScanner from '@/components/facial/FaceScanner.vue'

interface CampoConfig {
  id: number
  nombre_campo: string
  etiqueta: string
  tipo_dato: string
  es_obligatorio: boolean
  expresion_regex?: string
  valores_enum?: string[]
  api_integracion_id?: number
  campo_mapa_api?: string
  mostrar_en_registro: boolean
}

const camposConfiguracion = ref<CampoConfig[]>([])
const formulario = reactive<Record<string, any>>({})
const camposAutoLlenados = reactive<Record<string, string>>({})
const consultandoAPI = reactive<Record<string, boolean>>({})
const erroresValidacion = reactive<Record<string, string>>({})
const enviando = ref(false)
const fotosCapturadas = ref<any>(null)

onMounted(async () => {
  await cargarCamposConfiguracion()
})

const cargarCamposConfiguracion = async () => {
  try {
    const res = await api.get('/configuracion/campos/registro')
    camposConfiguracion.value = res.data.campos
      .filter((c: CampoConfig) => c.mostrar_en_registro)
      .sort((a: CampoConfig, b: CampoConfig) => (a.posicion || 0) - (b.posicion || 0))
    
    // Inicializar formulario
    camposConfiguracion.value.forEach(campo => {
      formulario[campo.nombre_campo] = ''
    })
  } catch (error) {
    console.error('Error cargando campos:', error)
  }
}

const getTipoInput = (tipoDato: string): string => {
  const mapa: Record<string, string> = {
    'email': 'email',
    'phone': 'tel',
    'url': 'url',
    'string': 'text'
  }
  return mapa[tipoDato] || 'text'
}

const validarYConsultarAPI = async (campo: CampoConfig) => {
  // Validar con regex si existe
  if (campo.expresion_regex) {
    const regex = new RegExp(campo.expresion_regex)
    const valor = formulario[campo.nombre_campo]
    
    if (valor && !regex.test(valor)) {
      erroresValidacion[campo.nombre_campo] = `Formato inválido para ${campo.etiqueta}`
      return
    }
  }
  
  // Consultar API si está configurada
  if (campo.api_integracion_id && formulario[campo.nombre_campo]) {
    consultandoAPI[campo.nombre_campo] = true
    
    try {
      let endpoint = ''
      let parametro = formulario[campo.nombre_campo]
      
      // Determinar endpoint según tipo de integración
      if (campo.nombre_campo === 'documento_identidad') {
        endpoint = `/validaciones/consultar-dni?dni=${parametro}`
      } else if (campo.nombre_campo === 'ruc') {
        endpoint = `/validaciones/consultar-ruc?ruc=${parametro}`
      }
      
      const res = await api.post(endpoint)
      
      if (res.data.exitosa) {
        // Auto-llenar campos relacionados
        Object.entries(res.data.datos).forEach(([key, value]) => {
          const nombreCampo = mapearCampoAPI(key)
          if (nombreCampo && formulario.hasOwnProperty(nombreCampo)) {
            formulario[nombreCampo] = value
            camposAutoLlenados[nombreCampo] = campo.etiqueta
          }
        })
      }
    } catch (error) {
      console.error('Error consultando API:', error)
      erroresValidacion[campo.nombre_campo] = 'No se pudo validar los datos'
    } finally {
      consultandoAPI[campo.nombre_campo] = false
    }
  }
}

const mapearCampoAPI = (campoAPI: string): string | null => {
  const mapeo: Record<string, string> = {
    'nombre': 'nombre',
    'nombres': 'nombre',
    'apellido_paterno': 'apellido_paterno',
    'apellido_materno': 'apellido_materno',
    'razon_social': 'razon_social',
    'direccion': 'direccion',
    'genero': 'genero',
    'fecha_nacimiento': 'fecha_nacimiento'
  }
  return mapeo[campoAPI] || null
}

const onFotosCapturadas = (fotos: any) => {
  fotosCapturadas.value = fotos
}

const registrar = async () => {
  if (!fotosCapturadas.value) {
    alert('Debes capturar las 3 fotos para registrarte')
    return
  }
  
  enviando.value = true
  
  try {
    const formData = new FormData()
    
    // Agregar campos dinámicos
    Object.entries(formulario).forEach(([key, value]) => {
      formData.append(key, String(value))
    })
    
    // Agregar fotos
    formData.append('foto_frontal', fotosCapturadas.value.frontal)
    formData.append('foto_lateral_izquierda', fotosCapturadas.value.lateral_izquierdo)
    formData.append('foto_lateral_derecha', fotosCapturadas.value.lateral_derecho)
    
    const res = await api.post('/usuarios/registro', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    alert('✓ Usuario registrado exitosamente')
    // Redirigir a login o dashboard
  } catch (error: any) {
    alert('Error: ' + (error.response?.data?.detail || 'Error al registrar'))
  } finally {
    enviando.value = false
  }
}
</script>

<style scoped>
.registro-dinamico {
  max-width: 700px;
  margin: 0 auto;
  padding: 30px 20px;
}

h1 {
  text-align: center;
  color: #1f2937;
  margin-bottom: 30px;
}

form {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 25px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #374151;
}

.requerido {
  color: #ef4444;
}

.icono-api {
  margin-left: 8px;
  font-size: 12px;
}

.input-field,
select {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
  transition: border-color 0.2s;
}

.input-field:focus,
select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.checkbox-label input {
  width: auto;
}

.loading {
  margin-top: 8px;
  color: #f59e0b;
  font-size: 12px;
  font-weight: 600;
}

.auto-llenado {
  margin-top: 8px;
  color: #10b981;
  font-size: 12px;
  font-weight: 600;
}

.error {
  display: block;
  margin-top: 8px;
  color: #ef4444;
  font-size: 12px;
}

.btn-submit {
  width: 100%;
  padding: 14px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-submit:hover:not(:disabled) {
  background: #2563eb;
}

.btn-submit:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}
</style>
```

---

## 🔐 Endpoint de Prueba de Integración

```python
# backend/app/routes/admin_configuracion.py

@router.post("/integraciones-api/{integracion_id}/probar")
async def probar_integracion(
    integracion_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Prueba una integración API antes de usar en producción"""
    
    # Solo admin
    if current_user.rol != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    integracion = db.query(IntegracionAPI).filter_by(id=integracion_id).first()
    if not integracion:
        raise HTTPException(status_code=404, detail="Integración no encontrada")
    
    service = IntegracionAPIService(db)
    
    # Probar conexión según tipo
    if integracion.tipo == TipoAPIEnum.RENIEC:
        # Usar un DNI de prueba
        resultado = service.consultar_reniec("12345678", integracion)
    elif integracion.tipo == TipoAPIEnum.FACTURIZA:
        # Usar un RUC de prueba
        resultado = service.consultar_facturiza("20000000001", integracion)
    else:
        resultado = service.consultar_api_custom("test", integracion)
    
    return resultado
```

---

## 📊 Caso de Uso Completo: Registro con RENIEC

```
1. Admin configura campo "documento_identidad"
   ├─ Nombre: documento_identidad
   ├─ Tipo: string
   ├─ Regex: ^[0-9]{8}$
   ├─ API: RENIEC
   ├─ Campo en API: dni
   └─ Guardar

2. Admin configura integración RENIEC
   ├─ URL: https://api.reniec.gob.pe/dni/
   ├─ Token: [token_encriptado]
   └─ Prueba: ✅ Exitosa

3. Usuario abre RegistroDinamico.vue
   ├─ Ve campo "Documento de Identidad" con 🔗
   └─ Ingresa: "12345678"

4. Sistema auto-completa:
   ├─ POST /validaciones/consultar-dni?dni=12345678
   ├─ RENIEC responde: {nombres: "Juan", apellido_paterno: "Pérez", ...}
   ├─ Auto-llena campos "nombre", "apellido_paterno", etc.
   ├─ Marca: "✅ Datos auto-llenados desde RENIEC"
   └─ Usuario confirma/corrige

5. Usuario completa fotos y registra
   └─ Consulta guardada en ConsultaExterna (auditoría)
```

---

## 🎯 Resumen

Este módulo permite:
- ✅ Configurar dinámicamente qué campos se muestran
- ✅ Conectar con APIs externas (RENIEC, Facturiza, SUNAT)
- ✅ Auto-llenar datos desde APIs
- ✅ Validar datos contra fuentes oficiales
- ✅ Mantener auditoría de consultas
- ✅ Seguridad: tokens encriptados, rate limiting, retry logic

