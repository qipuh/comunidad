# 🎨 Componentes Vue.js Dinámicos

Ejemplos de componentes Vue.js 3 que usan la **Configuración Dinámica** del sistema.

---

## 1. Registro Dinámico con Auto-llenado

### RegistroDinamico.vue

```vue
<template>
  <div class="registro-container">
    <h2>📝 Registro de Usuario</h2>
    
    <!-- Barra de progreso -->
    <div class="progress-bar">
      <div class="progress" :style="{ width: progreso + '%' }"></div>
    </div>
    
    <!-- Formulario dinámico -->
    <form @submit.prevent="guardarRegistro" class="formulario">
      <!-- Campos generados dinámicamente -->
      <div v-for="campo in campos" :key="campo.id" class="campo-grupo">
        <label :for="`campo-${campo.id}`">
          {{ campo.etiqueta }}
          <span v-if="campo.es_obligatorio" class="requerido">*</span>
        </label>
        
        <!-- Input de texto -->
        <input
          v-if="['string', 'email', 'phone', 'url'].includes(campo.tipo_dato)"
          :id="`campo-${campo.id}`"
          v-model="formData[campo.nombre_campo]"
          :type="tipoInput(campo.tipo_dato)"
          :required="campo.es_obligatorio"
          :pattern="campo.expresion_regex"
          @blur="validarCampo(campo)"
          class="campo-input"
        />
        
        <!-- Input de número -->
        <input
          v-else-if="campo.tipo_dato === 'number'"
          :id="`campo-${campo.id}`"
          v-model.number="formData[campo.nombre_campo]"
          type="number"
          :required="campo.es_obligatorio"
          class="campo-input"
        />
        
        <!-- Input de fecha -->
        <input
          v-else-if="campo.tipo_dato === 'date'"
          :id="`campo-${campo.id}`"
          v-model="formData[campo.nombre_campo]"
          type="date"
          :required="campo.es_obligatorio"
          class="campo-input"
        />
        
        <!-- Checkbox -->
        <input
          v-else-if="campo.tipo_dato === 'boolean'"
          :id="`campo-${campo.id}`"
          v-model="formData[campo.nombre_campo]"
          type="checkbox"
          class="campo-checkbox"
        />
        
        <!-- Select (Enum) -->
        <select
          v-else-if="campo.tipo_dato === 'enum'"
          :id="`campo-${campo.id}`"
          v-model="formData[campo.nombre_campo]"
          :required="campo.es_obligatorio"
          class="campo-select"
        >
          <option value="">-- Seleccionar --</option>
          <option v-for="valor in campo.valores_enum" :key="valor" :value="valor">
            {{ valor }}
          </option>
        </select>
        
        <!-- Botón de validación desde API -->
        <button
          v-if="campo.api_integracion_id"
          type="button"
          @click="validarDesdeAPI(campo)"
          :disabled="validando"
          class="btn-validar"
        >
          {{ validando ? '⏳ Validando...' : '🔗 Validar' }}
        </button>
        
        <!-- Error message -->
        <span v-if="errores[campo.nombre_campo]" class="error">
          ⚠️ {{ errores[campo.nombre_campo] }}
        </span>
        
        <!-- Indicador de validación externa -->
        <span v-if="camposValidados[campo.nombre_campo]" class="validado">
          ✅ Validado externamente
        </span>
      </div>
      
      <!-- Botones de acción -->
      <div class="acciones">
        <button type="button" @click="limpiarFormulario" class="btn-secondary">
          🔄 Limpiar
        </button>
        <button type="submit" :disabled="enviando" class="btn-primary">
          {{ enviando ? '⏳ Guardando...' : '✅ Registrarse' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { configuracionService } from '@/services/configuracion.service'
import { validacionesService } from '@/services/validaciones.service'

interface Campo {
  id: number
  nombre_campo: string
  etiqueta: string
  tipo_dato: string
  es_obligatorio: boolean
  expresion_regex?: string
  valores_enum?: string[]
  api_integracion_id?: number
  campo_mapa_api?: string
}

const campos = ref<Campo[]>([])
const formData = ref<Record<string, any>>({})
const errores = ref<Record<string, string>>({})
const camposValidados = ref<Record<string, boolean>>({})
const validando = ref(false)
const enviando = ref(false)

const progreso = computed(() => {
  const camposObligatorios = campos.value.filter(c => c.es_obligatorio)
  if (camposObligatorios.length === 0) return 0
  
  const completados = camposObligatorios.filter(
    c => formData.value[c.nombre_campo]
  ).length
  
  return Math.round((completados / camposObligatorios.length) * 100)
})

const tipoInput = (tipo: string) => {
  const mapeo: Record<string, string> = {
    email: 'email',
    phone: 'tel',
    url: 'url',
    string: 'text'
  }
  return mapeo[tipo] || 'text'
}

const cargarCampos = async () => {
  try {
    campos.value = await configuracionService.obtenerCampos()
    campos.value.forEach(c => {
      formData.value[c.nombre_campo] = c.tipo_dato === 'boolean' ? false : ''
    })
  } catch (error) {
    console.error('Error cargando campos:', error)
  }
}

const validarCampo = (campo: Campo) => {
  const valor = formData.value[campo.nombre_campo]
  delete errores.value[campo.nombre_campo]
  
  if (campo.es_obligatorio && !valor) {
    errores.value[campo.nombre_campo] = `${campo.etiqueta} es obligatorio`
    return false
  }
  
  if (campo.expresion_regex && valor) {
    const regex = new RegExp(campo.expresion_regex)
    if (!regex.test(valor)) {
      errores.value[campo.nombre_campo] = `${campo.etiqueta} tiene un formato inválido`
      return false
    }
  }
  
  return true
}

const validarDesdeAPI = async (campo: Campo) => {
  const valor = formData.value[campo.nombre_campo]
  if (!valor) {
    errores.value[campo.nombre_campo] = 'Ingresa un valor primero'
    return
  }
  
  validando.value = true
  try {
    let resultado = null
    
    if (campo.nombre_campo.includes('dni')) {
      resultado = await validacionesService.consultarDNI(valor)
    } else if (campo.nombre_campo.includes('ruc')) {
      resultado = await validacionesService.consultarRUC(valor)
    }
    
    if (resultado && resultado.exitosa && resultado.datos) {
      // Auto-llenar campos relacionados
      Object.keys(resultado.datos).forEach(key => {
        const campoDestino = campos.value.find(
          c => validacionesService.mapearCampoAPI(key) === c.nombre_campo
        )
        if (campoDestino) {
          formData.value[campoDestino.nombre_campo] = resultado.datos[key]
          camposValidados.value[campoDestino.nombre_campo] = true
        }
      })
      camposValidados.value[campo.nombre_campo] = true
      delete errores.value[campo.nombre_campo]
    } else {
      errores.value[campo.nombre_campo] = resultado?.error || 'Error en validación'
    }
  } catch (error) {
    errores.value[campo.nombre_campo] = 'Error al conectar con la API'
  } finally {
    validando.value = false
  }
}

const guardarRegistro = async () => {
  // Validar todos los campos
  let valido = true
  campos.value.forEach(c => {
    if (!validarCampo(c)) valido = false
  })
  
  if (!valido) return
  
  enviando.value = true
  try {
    // Llamar endpoint para guardar
    const response = await fetch('/api/usuarios/registro-dinamico', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData.value)
    })
    
    if (response.ok) {
      alert('✅ Registro completado exitosamente')
      limpiarFormulario()
    }
  } catch (error) {
    alert('❌ Error al guardar registro')
  } finally {
    enviando.value = false
  }
}

const limpiarFormulario = () => {
  campos.value.forEach(c => {
    formData.value[c.nombre_campo] = c.tipo_dato === 'boolean' ? false : ''
  })
  errores.value = {}
  camposValidados.value = {}
}

onMounted(() => cargarCampos())
</script>

<style scoped>
.registro-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 1rem;
  color: #333;
}

.progress-bar {
  height: 6px;
  background: #eee;
  border-radius: 3px;
  margin: 1rem 0;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
}

.formulario {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.campo-grupo {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 600;
  color: #333;
}

.requerido {
  color: #ef4444;
}

.campo-input,
.campo-select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.campo-input:focus,
.campo-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.campo-checkbox {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.btn-validar {
  background: #10b981;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.btn-validar:hover:not(:disabled) {
  background: #059669;
}

.btn-validar:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  color: #ef4444;
  font-size: 0.85rem;
}

.validado {
  color: #10b981;
  font-size: 0.85rem;
  font-weight: 600;
}

.acciones {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-primary {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f3f4f6;
  color: #333;
  border: 1px solid #ddd;
}

.btn-secondary:hover {
  background: #e5e7eb;
}
</style>
```

---

## 2. Admin Panel - Gestor de Campos

### AdminCampos.vue

```vue
<template>
  <div class="admin-campos">
    <h2>⚙️ Administrar Campos Dinámicos</h2>
    
    <button @click="mostrarFormulario = true" class="btn-agregar">
      ➕ Nuevo Campo
    </button>
    
    <!-- Lista de campos -->
    <div v-if="campos.length" class="lista-campos">
      <div v-for="campo in campos" :key="campo.id" class="campo-item">
        <div class="campo-info">
          <h3>{{ campo.etiqueta }}</h3>
          <p>{{ campo.nombre_campo }} ({{ campo.tipo_dato }})</p>
          <span v-if="campo.es_obligatorio" class="badge obligatorio">Obligatorio</span>
          <span v-if="campo.api_integracion_id" class="badge api">Con API</span>
        </div>
        
        <div class="campo-acciones">
          <button @click="editar(campo)" class="btn-edit">✏️ Editar</button>
          <button @click="eliminar(campo.id)" class="btn-delete">🗑️ Eliminar</button>
        </div>
      </div>
    </div>
    
    <!-- Modal de formulario -->
    <div v-if="mostrarFormulario" class="modal" @click.self="cerrarFormulario">
      <div class="modal-content">
        <h3>{{ editando ? 'Editar Campo' : 'Nuevo Campo' }}</h3>
        
        <input v-model="formulario.nombre_campo" placeholder="nombre_campo" />
        <input v-model="formulario.etiqueta" placeholder="Etiqueta" />
        <input v-model="formulario.descripcion" placeholder="Descripción (opcional)" />
        
        <select v-model="formulario.tipo_dato">
          <option value="">-- Tipo de Dato --</option>
          <option value="string">Texto</option>
          <option value="number">Número</option>
          <option value="date">Fecha</option>
          <option value="email">Email</option>
          <option value="phone">Teléfono</option>
          <option value="boolean">Checkbox</option>
          <option value="enum">Opciones</option>
        </select>
        
        <label>
          <input v-model="formulario.es_obligatorio" type="checkbox" />
          Es obligatorio
        </label>
        
        <input v-model="formulario.expresion_regex" placeholder="Regex (opcional)" />
        
        <div class="modal-footer">
          <button @click="cerrarFormulario" class="btn-secondary">Cancelar</button>
          <button @click="guardarCampo" class="btn-primary">Guardar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { configuracionService } from '@/services/configuracion.service'

const campos = ref([])
const mostrarFormulario = ref(false)
const editando = ref(false)
const formulario = ref({
  nombre_campo: '',
  etiqueta: '',
  descripcion: '',
  tipo_dato: '',
  es_obligatorio: false,
  expresion_regex: ''
})

const cargarCampos = async () => {
  campos.value = await configuracionService.obtenerCampos()
}

const guardarCampo = async () => {
  if (editando.value) {
    await configuracionService.editarCampo(formulario.value.id, formulario.value)
  } else {
    await configuracionService.crearCampo(formulario.value)
  }
  await cargarCampos()
  cerrarFormulario()
}

const editar = (campo) => {
  editando.value = true
  formulario.value = { ...campo }
  mostrarFormulario.value = true
}

const eliminar = async (id) => {
  if (confirm('¿Eliminar este campo?')) {
    await configuracionService.eliminarCampo(id)
    await cargarCampos()
  }
}

const cerrarFormulario = () => {
  mostrarFormulario.value = false
  editando.value = false
  formulario.value = {
    nombre_campo: '',
    etiqueta: '',
    descripcion: '',
    tipo_dato: '',
    es_obligatorio: false,
    expresion_regex: ''
  }
}

onMounted(() => cargarCampos())
</script>

<style scoped>
.admin-campos {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 2rem;
}

h2 {
  margin-bottom: 1rem;
}

.btn-agregar {
  background: #667eea;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 2rem;
}

.lista-campos {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.campo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #eee;
}

.campo-info h3 {
  margin: 0 0 0.5rem 0;
}

.campo-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  margin-right: 0.5rem;
}

.badge.obligatorio {
  background: #fecaca;
  color: #991b1b;
}

.badge.api {
  background: #c7d2fe;
  color: #3730a3;
}

.campo-acciones {
  display: flex;
  gap: 0.5rem;
}

.btn-edit,
.btn-delete {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.btn-edit {
  background: #3b82f6;
  color: white;
}

.btn-delete {
  background: #ef4444;
  color: white;
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
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
}

.modal-content h3 {
  margin-top: 0;
}

.modal-content input,
.modal-content select {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-secondary {
  background: #f3f4f6;
  color: #333;
}
</style>
```

---

## 3. Composable para Validaciones

### useValidaciones.ts

```typescript
import { ref } from 'vue'
import { validacionesService } from '@/services/validaciones.service'

export function useValidaciones() {
  const validando = ref(false)
  const resultado = ref(null)
  const error = ref('')

  const consultarDNI = async (dni: string) => {
    validando.value = true
    error.value = ''
    try {
      resultado.value = await validacionesService.consultarDNI(dni)
      return resultado.value
    } catch (err) {
      error.value = err.message
      return null
    } finally {
      validando.value = false
    }
  }

  const consultarRUC = async (ruc: string) => {
    validando.value = true
    error.value = ''
    try {
      resultado.value = await validacionesService.consultarRUC(ruc)
      return resultado.value
    } catch (err) {
      error.value = err.message
      return null
    } finally {
      validando.value = false
    }
  }

  return {
    validando,
    resultado,
    error,
    consultarDNI,
    consultarRUC
  }
}
```

---

**Nota:** Estos componentes trabajan conjuntamente con:
- El servicio `configuracionService` para CRUD de campos
- El servicio `validacionesService` para consultas a APIs
- Los endpoints en ENDPOINTS_EJEMPLOS.md (Secciones 7-9)
- Los modelos en MODELOS_DATOS.md (Sección 6)
