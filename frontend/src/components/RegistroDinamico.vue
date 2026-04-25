<template>
  <div class="registro-dinamico">
    <div class="form-container">
      <div class="form-header">
        <h2>📝 Registro de Usuario</h2>
        <p class="form-subtitle">Completa el formulario con tus datos personales</p>
      </div>

      <!-- Indicadores de progreso -->
      <div class="progress-bar">
        <div class="progress" :style="{ width: progreso + '%' }"></div>
      </div>
      <p class="progress-text">{{ progreso }}% completado</p>

      <!-- Mensaje de carga inicial -->
      <div v-if="cargando" class="loading-state">
        <p>⏳ Cargando formulario...</p>
      </div>

      <!-- Formulario dinámico -->
      <form v-else @submit.prevent="enviarFormulario" class="formulario-dinamico">
        <!-- Campos dinámicos -->
        <div v-for="campo in camposVisibles" :key="campo.id" class="form-group">
          <label :for="`campo-${campo.id}`" class="form-label">
            {{ campo.etiqueta }}
            <span v-if="campo.es_obligatorio" class="obligatorio">*</span>
          </label>

          <!-- Campo de texto -->
          <div v-if="['string', 'email', 'phone', 'url'].includes(campo.tipo_dato)" class="field-wrapper">
            <input
              :id="`campo-${campo.id}`"
              v-model="formData[campo.nombre_campo]"
              :type="tipoInputHTML(campo.tipo_dato)"
              :placeholder="`Ingresa tu ${campo.etiqueta.toLowerCase()}`"
              :required="campo.es_obligatorio"
              :pattern="campo.expresion_regex || undefined"
              class="form-input"
              @blur="validarCampo(campo)"
            />
            <div v-if="errores[campo.nombre_campo]" class="error-message">
              ⚠️ {{ errores[campo.nombre_campo] }}
            </div>

            <!-- Botón para auto-llenar desde API -->
            <button
              v-if="campo.api_integracion_id"
              type="button"
              @click="autoLlenarDesdeAPI(campo)"
              :disabled="autoLlenando === campo.nombre_campo"
              class="btn-autofill"
            >
              {{ autoLlenando === campo.nombre_campo ? '⏳ Validando...' : '🔗 Validar' }}
            </button>
          </div>

          <!-- Campo numérico -->
          <div v-else-if="campo.tipo_dato === 'number'" class="field-wrapper">
            <input
              :id="`campo-${campo.id}`"
              v-model.number="formData[campo.nombre_campo]"
              type="number"
              :placeholder="`Ingresa ${campo.etiqueta.toLowerCase()}`"
              :required="campo.es_obligatorio"
              class="form-input"
              @blur="validarCampo(campo)"
            />
            <div v-if="errores[campo.nombre_campo]" class="error-message">
              ⚠️ {{ errores[campo.nombre_campo] }}
            </div>
          </div>

          <!-- Campo de fecha -->
          <div v-else-if="campo.tipo_dato === 'date'" class="field-wrapper">
            <input
              :id="`campo-${campo.id}`"
              v-model="formData[campo.nombre_campo]"
              type="date"
              :required="campo.es_obligatorio"
              class="form-input"
              @blur="validarCampo(campo)"
            />
            <div v-if="errores[campo.nombre_campo]" class="error-message">
              ⚠️ {{ errores[campo.nombre_campo] }}
            </div>
          </div>

          <!-- Campo booleano -->
          <div v-else-if="campo.tipo_dato === 'boolean'" class="checkbox-wrapper">
            <label class="checkbox-label">
              <input
                :id="`campo-${campo.id}`"
                v-model="formData[campo.nombre_campo]"
                type="checkbox"
              />
              {{ campo.etiqueta }}
            </label>
          </div>

          <!-- Campo de selección (enum) -->
          <div v-else-if="campo.tipo_dato === 'enum'" class="field-wrapper">
            <select
              :id="`campo-${campo.id}`"
              v-model="formData[campo.nombre_campo]"
              :required="campo.es_obligatorio"
              class="form-select"
              @blur="validarCampo(campo)"
            >
              <option value="">-- Seleccionar --</option>
              <option v-for="valor in campo.valores_enum" :key="valor" :value="valor">
                {{ valor }}
              </option>
            </select>
            <div v-if="errores[campo.nombre_campo]" class="error-message">
              ⚠️ {{ errores[campo.nombre_campo] }}
            </div>
          </div>

          <!-- Descripción del campo -->
          <small v-if="campo.descripcion" class="field-description">
            {{ campo.descripcion }}
          </small>

          <!-- Indicador de validación externa -->
          <div v-if="camposValidados[campo.nombre_campo]" class="validation-badge">
            ✅ Validado externamente
          </div>
        </div>

        <!-- Botones de acción -->
        <div class="form-actions">
          <button type="button" @click="limpiarFormulario" class="btn-secondary">
            🔄 Limpiar
          </button>
          <button type="submit" :disabled="enviando" class="btn-submit">
            {{ enviando ? '⏳ Registrando...' : '✅ Registrarse' }}
          </button>
        </div>
      </form>

      <!-- Mensaje de éxito -->
      <div v-if="mostrarExito" class="success-message">
        <div class="success-content">
          <p>🎉 ¡Registro completado exitosamente!</p>
          <small>Tu información ha sido guardada correctamente.</small>
        </div>
      </div>
    </div>

    <!-- Panel de información lateral -->
    <aside class="info-panel">
      <div class="info-card">
        <h3>📋 Información del Formulario</h3>
        <ul>
          <li v-if="campos.length > 0">
            <strong>Campos:</strong> {{ campos.length }}
          </li>
          <li v-if="camposObligatorios.length > 0">
            <strong>Obligatorios:</strong> {{ camposObligatorios.length }}
          </li>
          <li v-if="camposConAPI.length > 0">
            <strong>Con validación:</strong> {{ camposConAPI.length }}
          </li>
        </ul>
      </div>

      <div class="info-card">
        <h3>🔒 Privacidad</h3>
        <p>Tus datos serán encriptados y guardados de forma segura conforme a las normas de protección de datos.</p>
      </div>

      <div class="info-card">
        <h3>💡 Consejos</h3>
        <ul>
          <li v-if="camposConAPI.length > 0">
            Usa los botones "Validar" para auto-llenar tus datos
          </li>
          <li>Completa todos los campos marcados con *</li>
          <li>Verifica tus datos antes de enviar</li>
        </ul>
      </div>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { configuracionService, type ConfiguracionCampo } from '@/services/configuracion.service'
import { validacionesService } from '@/services/validaciones.service'

const campos = ref<ConfiguracionCampo[]>([])
const formData = ref<Record<string, any>>({})
const errores = ref<Record<string, string>>({})
const camposValidados = ref<Record<string, boolean>>({})
const cargando = ref(true)
const enviando = ref(false)
const autoLlenando = ref<string | null>(null)
const mostrarExito = ref(false)

const camposVisibles = computed(() =>
  campos.value.filter(c => c.mostrar_en_registro).sort((a, b) => a.posicion - b.posicion)
)

const camposObligatorios = computed(() =>
  campos.value.filter(c => c.es_obligatorio)
)

const camposConAPI = computed(() =>
  campos.value.filter(c => c.api_integracion_id)
)

const progreso = computed(() => {
  if (camposObligatorios.value.length === 0) return 0
  const completados = camposObligatorios.value.filter(
    c => formData.value[c.nombre_campo] && formData.value[c.nombre_campo].toString().trim()
  ).length
  return Math.round((completados / camposObligatorios.value.length) * 100)
})

const cargarCampos = async () => {
  try {
    cargando.value = true
    campos.value = await configuracionService.obtenerCampos()
    campos.value.forEach(campo => {
      formData.value[campo.nombre_campo] = campo.tipo_dato === 'boolean' ? false : ''
    })
  } catch (error) {
    console.error('Error cargando campos:', error)
  } finally {
    cargando.value = false
  }
}

const tipoInputHTML = (tipo: string): string => {
  const tipos: Record<string, string> = {
    string: 'text',
    email: 'email',
    phone: 'tel',
    url: 'url'
  }
  return tipos[tipo] || 'text'
}

const validarCampo = (campo: ConfiguracionCampo) => {
  const valor = formData.value[campo.nombre_campo]
  delete errores.value[campo.nombre_campo]

  if (campo.es_obligatorio && (!valor || valor.toString().trim() === '')) {
    errores.value[campo.nombre_campo] = `${campo.etiqueta} es obligatorio`
    return false
  }

  if (campo.expresion_regex && valor) {
    const regex = new RegExp(campo.expresion_regex)
    if (!regex.test(valor.toString())) {
      errores.value[campo.nombre_campo] = `${campo.etiqueta} tiene un formato inválido`
      return false
    }
  }

  return true
}

const autoLlenarDesdeAPI = async (campo: ConfiguracionCampo) => {
  const valor = formData.value[campo.nombre_campo]

  if (!valor) {
    errores.value[campo.nombre_campo] = 'Ingresa un valor antes de validar'
    return
  }

  autoLlenando.value = campo.nombre_campo

  try {
    let resultado = null

    if (campo.nombre_campo === 'dni' || campo.nombre_campo.includes('documento')) {
      resultado = await validacionesService.consultarDNI(valor)
    } else if (campo.nombre_campo === 'ruc' || campo.nombre_campo.includes('ruc')) {
      resultado = await validacionesService.consultarRUC(valor)
    }

    if (resultado && resultado.exitosa && resultado.datos) {
      Object.keys(resultado.datos).forEach(key => {
        const campoDestino = camposVisibles.value.find(c => validacionesService.mapearCampoAPI(key) === c.nombre_campo)
        if (campoDestino) {
          formData.value[campoDestino.nombre_campo] = resultado!.datos![key]
          camposValidados.value[campoDestino.nombre_campo] = true
        }
      })
      camposValidados.value[campo.nombre_campo] = true
      delete errores.value[campo.nombre_campo]
    } else {
      errores.value[campo.nombre_campo] = resultado?.error || 'No se encontraron datos'
    }
  } catch (error) {
    console.error('Error validando desde API:', error)
    errores.value[campo.nombre_campo] = 'Error al conectar con la API'
  } finally {
    autoLlenando.value = null
  }
}

const validarFormulario = (): boolean => {
  errores.value = {}
  let valido = true

  camposObligatorios.value.forEach(campo => {
    if (!validarCampo(campo)) {
      valido = false
    }
  })

  return valido
}

const enviarFormulario = async () => {
  if (!validarFormulario()) {
    console.error('Formulario inválido')
    return
  }

  enviando.value = true
  try {
    // Aquí iría la lógica de envío del formulario
    console.log('Datos del formulario:', formData.value)
    mostrarExito.value = true
    setTimeout(() => {
      limpiarFormulario()
      mostrarExito.value = false
    }, 3000)
  } catch (error) {
    console.error('Error enviando formulario:', error)
  } finally {
    enviando.value = false
  }
}

const limpiarFormulario = () => {
  campos.value.forEach(campo => {
    formData.value[campo.nombre_campo] = campo.tipo_dato === 'boolean' ? false : ''
  })
  errores.value = {}
  camposValidados.value = {}
  mostrarExito.value = false
}

onMounted(() => {
  cargarCampos()
})
</script>

<style scoped>
.registro-dinamico {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 2rem;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.form-container {
  background: white;
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.form-header {
  margin-bottom: 2rem;
  text-align: center;
}

.form-header h2 {
  font-size: 1.8rem;
  margin: 0 0 0.5rem 0;
  color: #333;
}

.form-subtitle {
  color: #666;
  margin: 0;
  font-size: 1rem;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: #e0e0e0;
  border-radius: 3px;
  overflow: hidden;
  margin: 1.5rem 0 0.5rem 0;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
}

.progress-text {
  text-align: right;
  font-size: 0.85rem;
  color: #999;
  margin: 0.5rem 0 2rem 0;
}

.loading-state {
  text-align: center;
  padding: 3rem 2rem;
  color: #666;
}

.formulario-dinamico {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #333;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.obligatorio {
  color: #f44336;
  font-size: 1.1rem;
}

.field-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  position: relative;
}

.form-input,
.form-select {
  padding: 0.875rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.3s ease;
  background: #fafafa;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input:disabled,
.form-select:disabled {
  background: #f0f0f0;
  cursor: not-allowed;
  opacity: 0.6;
}

.btn-autofill {
  position: absolute;
  right: 8px;
  top: 42px;
  padding: 0.5rem 1rem;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-autofill:hover:not(:disabled) {
  background: #388e3c;
  transform: scale(1.05);
}

.btn-autofill:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  color: #f44336;
  font-size: 0.85rem;
  margin-top: 0.25rem;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  user-select: none;
  font-weight: normal;
}

.checkbox-label input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: #667eea;
}

.field-description {
  color: #999;
  font-size: 0.85rem;
  margin-top: -0.25rem;
}

.validation-badge {
  color: #4caf50;
  font-size: 0.85rem;
  font-weight: 600;
  margin-top: 0.25rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

.btn-secondary,
.btn-submit {
  padding: 0.875rem 1.75rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
  border: 1px solid #ddd;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.btn-submit {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 15px rgba(102, 126, 234, 0.3);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.success-message {
  position: fixed;
  top: 20px;
  right: 20px;
  background: white;
  border: 2px solid #4caf50;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  animation: slideIn 0.3s ease;
}

.success-content {
  text-align: center;
}

.success-content p {
  margin: 0;
  color: #4caf50;
  font-weight: 600;
  font-size: 1rem;
}

.success-content small {
  color: #999;
  display: block;
  margin-top: 0.5rem;
}

@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Info Panel */
.info-panel {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.info-card h3 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  color: #333;
}

.info-card ul {
  margin: 0;
  padding-left: 1.5rem;
  list-style: none;
}

.info-card li {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  position: relative;
  padding-left: 1rem;
}

.info-card li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #667eea;
  font-weight: 600;
}

.info-card p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.6;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .registro-dinamico {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .info-panel {
    grid-column: 1;
    flex-direction: row;
    flex-wrap: wrap;
  }

  .info-card {
    flex: 1;
    min-width: 250px;
  }
}

@media (max-width: 768px) {
  .registro-dinamico {
    padding: 1rem;
  }

  .form-container {
    padding: 1.5rem;
  }

  .form-header h2 {
    font-size: 1.5rem;
  }

  .btn-autofill {
    position: static;
    width: 100%;
    margin-top: 0.5rem;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .success-message {
    right: 10px;
    left: 10px;
  }
}

@media (max-width: 480px) {
  .registro-dinamico {
    padding: 0.5rem;
    grid-template-columns: 1fr;
  }

  .form-container {
    padding: 1rem;
    border-radius: 8px;
  }

  .form-header h2 {
    font-size: 1.3rem;
  }

  .info-panel {
    flex-direction: column;
  }

  .info-card {
    padding: 1rem;
  }
}
</style>
