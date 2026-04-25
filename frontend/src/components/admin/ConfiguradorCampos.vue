<template>
  <div class="configurador-campos">
    <div class="header">
      <h2>⚙️ Configurar Campos de Registro</h2>
      <p class="subtitle">Define qué campos aparecerán en el formulario de registro</p>
    </div>

    <button @click="mostrarNuevoCampo = true" class="btn-primary btn-lg">
      ➕ Nuevo Campo
    </button>

    <!-- Lista de campos existentes -->
    <div v-if="campos.length > 0" class="campos-list">
      <div class="list-header">
        <span class="col-order">Orden</span>
        <span class="col-info">Información</span>
        <span class="col-actions">Acciones</span>
      </div>

      <draggable
        v-model="campos"
        @change="onReordenar"
        class="draggable-list"
        item-key="id"
      >
        <template #item="{ element: campo }">
          <div class="campo-item">
            <div class="col-order">
              <span class="drag-handle">≡</span>
              <span class="posicion">{{ campo.posicion }}</span>
            </div>

            <div class="col-info">
              <div class="campo-titulo">
                <strong>{{ campo.etiqueta }}</strong>
                <span v-if="campo.es_obligatorio" class="badge obligatorio">Obligatorio</span>
                <span v-if="campo.api_integracion_id" class="badge api">🔗 API</span>
              </div>
              <div class="campo-detalles">
                <small>{{ campo.nombre_campo }}</small>
                <span class="tipo-dato">{{ campo.tipo_dato }}</span>
              </div>
              <div v-if="campo.descripcion" class="campo-descripcion">
                {{ campo.descripcion }}
              </div>
            </div>

            <div class="col-actions">
              <button @click="editarCampo(campo)" class="btn-edit" title="Editar">
                ✏️ Editar
              </button>
              <button @click="eliminarCampo(campo.id)" class="btn-delete" title="Eliminar">
                🗑️ Eliminar
              </button>
            </div>
          </div>
        </template>
      </draggable>
    </div>

    <div v-else class="empty-state">
      <p>📋 No hay campos configurados aún</p>
      <p class="hint">Crea el primer campo haciendo clic en "Nuevo Campo"</p>
    </div>

    <!-- Modal: Nuevo/Editar Campo -->
    <div v-if="mostrarNuevoCampo" class="modal-overlay" @click="cancelar">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editandoCampo ? '✏️ Editar' : '➕ Nuevo' }} Campo</h3>
          <button @click="cancelar" class="btn-close">✕</button>
        </div>

        <form @submit.prevent="guardarCampo" class="formulario">
          <!-- Nombre del campo -->
          <div class="form-group">
            <label for="nombre_campo">Nombre del Campo *</label>
            <input
              id="nombre_campo"
              v-model="formulario.nombre_campo"
              type="text"
              placeholder="documento_identidad"
              :disabled="editandoCampo"
              required
            />
            <small>Identificador único, usado en la BD (sin espacios)</small>
          </div>

          <!-- Etiqueta -->
          <div class="form-group">
            <label for="etiqueta">Etiqueta (lo que ve el usuario) *</label>
            <input
              id="etiqueta"
              v-model="formulario.etiqueta"
              type="text"
              placeholder="Documento de Identidad"
              required
            />
            <small>Texto que aparecerá en el formulario</small>
          </div>

          <!-- Descripción -->
          <div class="form-group">
            <label for="descripcion">Descripción</label>
            <textarea
              id="descripcion"
              v-model="formulario.descripcion"
              placeholder="Descripción adicional del campo"
              rows="2"
            ></textarea>
          </div>

          <!-- Tipo de dato -->
          <div class="form-group">
            <label for="tipo_dato">Tipo de Dato *</label>
            <select v-model="formulario.tipo_dato" id="tipo_dato" required>
              <option value="">-- Seleccionar --</option>
              <option value="string">📝 Texto</option>
              <option value="number">🔢 Número</option>
              <option value="date">📅 Fecha</option>
              <option value="email">📧 Email</option>
              <option value="phone">📱 Teléfono</option>
              <option value="url">🔗 URL</option>
              <option value="enum">📋 Lista de Opciones</option>
              <option value="boolean">✓ Sí/No</option>
            </select>
          </div>

          <!-- Obligatorio -->
          <div class="form-group checkbox">
            <input
              id="es_obligatorio"
              v-model="formulario.es_obligatorio"
              type="checkbox"
            />
            <label for="es_obligatorio">Campo Obligatorio</label>
          </div>

          <!-- Expresión Regular -->
          <div class="form-group">
            <label for="expresion_regex">Expresión Regular (validación)</label>
            <input
              id="expresion_regex"
              v-model="formulario.expresion_regex"
              type="text"
              placeholder="^[0-9]{8}$"
            />
            <small>Ej: ^[0-9]{8}$ para 8 dígitos</small>
          </div>

          <!-- Valores enum -->
          <div v-if="formulario.tipo_dato === 'enum'" class="form-group">
            <label for="valores_enum">Valores (separados por coma)</label>
            <textarea
              id="valores_enum"
              v-model="formulario.valores_enum_texto"
              placeholder="Opción 1, Opción 2, Opción 3"
              rows="3"
            ></textarea>
            <small>Ej: Activo, Inactivo, Suspendido</small>
          </div>

          <!-- API Integration -->
          <div class="form-section">
            <h4>🔌 Integración con API Externa (Opcional)</h4>

            <div class="form-group">
              <label for="api_integracion_id">Conectar con API</label>
              <select v-model="formulario.api_integracion_id" id="api_integracion_id">
                <option :value="null">-- Sin API --</option>
                <option v-for="api in integraciones" :key="api.id" :value="api.id">
                  {{ api.nombre }} ({{ api.tipo }})
                </option>
              </select>
              <small v-if="integraciones.length === 0">
                ℹ️ No hay integraciones configuradas. Crea una en "Integraciones API"
              </small>
            </div>

            <div v-if="formulario.api_integracion_id" class="form-group">
              <label for="campo_mapa_api">Campo en la API que mapea a este</label>
              <input
                id="campo_mapa_api"
                v-model="formulario.campo_mapa_api"
                type="text"
                placeholder="nombres, apellido_paterno, etc."
              />
              <small>Nombre del campo en la respuesta de la API</small>
            </div>
          </div>

          <!-- Visibilidad -->
          <div class="form-section">
            <h4>👁️ Visibilidad</h4>

            <div class="form-group checkbox">
              <input
                id="mostrar_en_registro"
                v-model="formulario.mostrar_en_registro"
                type="checkbox"
              />
              <label for="mostrar_en_registro">Mostrar en formulario de registro</label>
            </div>

            <div class="form-group checkbox">
              <input
                id="mostrar_en_perfil"
                v-model="formulario.mostrar_en_perfil"
                type="checkbox"
              />
              <label for="mostrar_en_perfil">Mostrar en perfil del usuario</label>
            </div>

            <div class="form-group checkbox">
              <input
                id="mostrar_en_reportes"
                v-model="formulario.mostrar_en_reportes"
                type="checkbox"
              />
              <label for="mostrar_en_reportes">Incluir en reportes</label>
            </div>
          </div>

          <!-- Botones -->
          <div class="modal-actions">
            <button type="submit" class="btn-success">
              💾 {{ editandoCampo ? 'Actualizar' : 'Crear' }} Campo
            </button>
            <button type="button" @click="cancelar" class="btn-secondary">
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Toast de notificaciones -->
    <div v-if="notificacion" :class="['toast', notificacion.tipo]">
      {{ notificacion.mensaje }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import draggable from 'vuedraggable'
import { configuracionService, ConfiguracionCampo, IntegracionAPI } from '@/services/configuracion.service'

// Estado
const campos = ref<ConfiguracionCampo[]>([])
const integraciones = ref<IntegracionAPI[]>([])
const mostrarNuevoCampo = ref(false)
const editandoCampo = ref(false)
const notificacion = ref<{ mensaje: string; tipo: 'exito' | 'error' } | null>(null)

// Formulario
const formulario = ref({
  nombre_campo: '',
  etiqueta: '',
  descripcion: '',
  tipo_dato: '',
  es_obligatorio: false,
  expresion_regex: '',
  valores_enum_texto: '',
  posicion: 0,
  api_integracion_id: null as number | null,
  campo_mapa_api: '',
  mostrar_en_registro: true,
  mostrar_en_perfil: true,
  mostrar_en_reportes: true
})

// Lifecycle
onMounted(async () => {
  await cargarCampos()
  await cargarIntegraciones()
})

// Métodos
const cargarCampos = async () => {
  try {
    campos.value = await configuracionService.obtenerCampos()
  } catch (error) {
    mostrarNotificacion('Error cargando campos', 'error')
  }
}

const cargarIntegraciones = async () => {
  try {
    integraciones.value = await configuracionService.obtenerIntegraciones()
  } catch (error) {
    console.error('Error cargando integraciones:', error)
  }
}

const editarCampo = (campo: ConfiguracionCampo) => {
  formulario.value = {
    nombre_campo: campo.nombre_campo,
    etiqueta: campo.etiqueta,
    descripcion: campo.descripcion || '',
    tipo_dato: campo.tipo_dato,
    es_obligatorio: campo.es_obligatorio,
    expresion_regex: campo.expresion_regex || '',
    valores_enum_texto: '',
    posicion: campo.posicion,
    api_integracion_id: campo.api_integracion_id || null,
    campo_mapa_api: campo.campo_mapa_api || '',
    mostrar_en_registro: campo.mostrar_en_registro,
    mostrar_en_perfil: campo.mostrar_en_perfil,
    mostrar_en_reportes: campo.mostrar_en_reportes
  }
  editandoCampo.value = true
  mostrarNuevoCampo.value = true
}

const guardarCampo = async () => {
  try {
    const datos = {
      nombre_campo: formulario.value.nombre_campo,
      etiqueta: formulario.value.etiqueta,
      descripcion: formulario.value.descripcion || undefined,
      tipo_dato: formulario.value.tipo_dato,
      es_obligatorio: formulario.value.es_obligatorio,
      expresion_regex: formulario.value.expresion_regex || undefined,
      valores_enum: formulario.value.tipo_dato === 'enum'
        ? formulario.value.valores_enum_texto.split(',').map(v => v.trim())
        : undefined,
      posicion: formulario.value.posicion,
      api_integracion_id: formulario.value.api_integracion_id,
      campo_mapa_api: formulario.value.campo_mapa_api || undefined,
      mostrar_en_registro: formulario.value.mostrar_en_registro,
      mostrar_en_perfil: formulario.value.mostrar_en_perfil,
      mostrar_en_reportes: formulario.value.mostrar_en_reportes
    }

    if (editandoCampo.value) {
      const campoActual = campos.value.find(c => c.nombre_campo === formulario.value.nombre_campo)
      if (campoActual) {
        await configuracionService.editarCampo(campoActual.id, datos)
        mostrarNotificacion('Campo actualizado exitosamente', 'exito')
      }
    } else {
      await configuracionService.crearCampo(datos)
      mostrarNotificacion('Campo creado exitosamente', 'exito')
    }

    await cargarCampos()
    cancelar()
  } catch (error: any) {
    mostrarNotificacion(
      error.response?.data?.detail || 'Error guardando campo',
      'error'
    )
  }
}

const eliminarCampo = async (id: number) => {
  if (!confirm('¿Estás seguro de que deseas eliminar este campo?')) {
    return
  }

  try {
    await configuracionService.eliminarCampo(id)
    mostrarNotificacion('Campo eliminado exitosamente', 'exito')
    await cargarCampos()
  } catch (error) {
    mostrarNotificacion('Error eliminando campo', 'error')
  }
}

const onReordenar = async () => {
  // Actualizar posiciones
  campos.value.forEach((campo, index) => {
    campo.posicion = index
  })

  // Guardar cambios
  for (const campo of campos.value) {
    try {
      await configuracionService.editarCampo(campo.id, { posicion: campo.posicion })
    } catch (error) {
      console.error('Error reordenando:', error)
    }
  }

  mostrarNotificacion('Orden actualizado', 'exito')
}

const cancelar = () => {
  mostrarNuevoCampo.value = false
  editandoCampo.value = false
  formulario.value = {
    nombre_campo: '',
    etiqueta: '',
    descripcion: '',
    tipo_dato: '',
    es_obligatorio: false,
    expresion_regex: '',
    valores_enum_texto: '',
    posicion: campos.value.length,
    api_integracion_id: null,
    campo_mapa_api: '',
    mostrar_en_registro: true,
    mostrar_en_perfil: true,
    mostrar_en_reportes: true
  }
}

const mostrarNotificacion = (mensaje: string, tipo: 'exito' | 'error') => {
  notificacion.value = { mensaje, tipo }
  setTimeout(() => {
    notificacion.value = null
  }, 3000)
}
</script>

<style scoped>
.configurador-campos {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  margin-bottom: 30px;
}

.header h2 {
  margin: 0 0 5px 0;
  color: #1f2937;
  font-size: 24px;
}

.subtitle {
  color: #6b7280;
  margin: 0;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  margin-bottom: 20px;
  transition: all 0.3s;
}

.btn-primary:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-lg {
  font-size: 16px;
  padding: 14px 24px;
}

/* Lista de campos */
.campos-list {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.list-header {
  display: grid;
  grid-template-columns: 80px 1fr 200px;
  gap: 20px;
  padding: 15px 20px;
  background: #f9fafb;
  border-bottom: 2px solid #e5e7eb;
  font-weight: 600;
  color: #6b7280;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.draggable-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.campo-item {
  display: grid;
  grid-template-columns: 80px 1fr 200px;
  gap: 20px;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
  transition: all 0.3s;
}

.campo-item:hover {
  background: #f9fafb;
}

.campo-item:last-child {
  border-bottom: none;
}

.col-order {
  display: flex;
  align-items: center;
  gap: 10px;
}

.drag-handle {
  cursor: grab;
  color: #9ca3af;
  font-size: 18px;
  font-weight: bold;
}

.drag-handle:active {
  cursor: grabbing;
}

.posicion {
  color: #6b7280;
  font-weight: 600;
}

.col-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.campo-titulo {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 5px;
}

.campo-titulo strong {
  color: #1f2937;
}

.badge {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 3px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}

.badge.obligatorio {
  background: #fee2e2;
  color: #991b1b;
}

.badge.api {
  background: #d1fae5;
  color: #065f46;
}

.campo-detalles {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.campo-detalles small {
  color: #9ca3af;
  font-family: 'Monaco', 'Courier New', monospace;
}

.tipo-dato {
  background: #ede9fe;
  color: #7c3aed;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 11px;
  font-weight: 600;
}

.campo-descripcion {
  color: #6b7280;
  font-size: 12px;
  margin-top: 5px;
  max-width: 300px;
}

.col-actions {
  display: flex;
  gap: 8px;
}

.btn-edit,
.btn-delete {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-edit {
  background: #fef3c7;
  color: #92400e;
}

.btn-edit:hover {
  background: #fcd34d;
}

.btn-delete {
  background: #fee2e2;
  color: #991b1b;
}

.btn-delete:hover {
  background: #fca5a5;
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #9ca3af;
}

.empty-state p {
  margin: 10px 0;
}

.hint {
  font-size: 14px;
  color: #d1d5db;
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
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 2px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  color: #1f2937;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #9ca3af;
  transition: all 0.2s;
}

.btn-close:hover {
  color: #6b7280;
  transform: scale(1.1);
}

.formulario {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-weight: 600;
  color: #374151;
  font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-family: inherit;
  font-size: 14px;
  transition: all 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-group input:disabled {
  background: #f3f4f6;
  color: #9ca3af;
  cursor: not-allowed;
}

.form-group small {
  color: #9ca3af;
  font-size: 12px;
}

.form-group.checkbox {
  flex-direction: row;
  align-items: center;
  gap: 10px;
}

.form-group.checkbox input {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.form-group.checkbox label {
  margin: 0;
}

.form-section {
  padding: 15px;
  background: #f9fafb;
  border-radius: 6px;
  border-left: 4px solid #3b82f6;
}

.form-section h4 {
  margin: 0 0 15px 0;
  color: #1f2937;
  font-size: 14px;
}

.modal-actions {
  display: flex;
  gap: 10px;
  padding: 20px;
  border-top: 2px solid #e5e7eb;
  background: #f9fafb;
}

.btn-success,
.btn-secondary {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.2s;
}

.btn-success {
  background: #10b981;
  color: white;
}

.btn-success:hover {
  background: #059669;
  transform: translateY(-2px);
}

.btn-secondary {
  background: #e5e7eb;
  color: #374151;
}

.btn-secondary:hover {
  background: #d1d5db;
}

/* Toast */
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 16px 20px;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.3s ease-out;
  z-index: 2000;
}

.toast.exito {
  background: #10b981;
}

.toast.error {
  background: #ef4444;
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

/* Responsive */
@media (max-width: 768px) {
  .list-header,
  .campo-item {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .col-order,
  .col-info,
  .col-actions {
    width: 100%;
  }

  .campo-item {
    padding: 15px;
  }

  .modal-content {
    max-width: 95vw;
    border-radius: 8px;
  }

  .modal-actions {
    flex-direction: column;
  }
}
</style>
