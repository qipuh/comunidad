<template>
  <div class="config-cobranza-container">
    <div class="config-header">
      <h2>Configuración de Cobranza</h2>
    </div>

    <!-- Tabs -->
    <div class="config-tabs">
      <button
        :class="['tab', { active: tabConfig === 'conceptos' }]"
        @click="tabConfig = 'conceptos'"
      >
        <ion-icon name="document-text-outline"></ion-icon>
        Conceptos de Pago
      </button>
      <button
        :class="['tab', { active: tabConfig === 'metodos' }]"
        @click="tabConfig = 'metodos'"
      >
        <ion-icon name="card-outline"></ion-icon>
        Métodos de Pago
      </button>
      <button
        :class="['tab', { active: tabConfig === 'asignacion' }]"
        @click="tabConfig = 'asignacion'"
      >
        <ion-icon name="people-circle-outline"></ion-icon>
        Asignación Masiva
      </button>
    </div>

    <!-- Tab: Conceptos de Pago -->
    <div v-if="tabConfig === 'conceptos'" class="tab-content">
      <div class="section-header">
        <h3>Conceptos de Pago</h3>
        <button @click="abrirModalConcepto()" class="btn-primary">
          <ion-icon name="add-outline"></ion-icon>
          Nuevo Concepto
        </button>
      </div>

      <div class="conceptos-grid">
        <div v-for="concepto in conceptos" :key="concepto.id" class="concepto-card">
          <div class="concepto-header">
            <div>
              <h4>{{ concepto.nombre }}</h4>
              <p class="tipo-badge">{{ concepto.tipo }}</p>
            </div>
            <span :class="['badge', concepto.activo ? 'activo' : 'inactivo']">
              {{ concepto.activo ? 'Activo' : 'Inactivo' }}
            </span>
          </div>

          <div class="concepto-details">
            <div class="detail-item">
              <span class="label">Monto:</span>
              <span class="valor">{{ formatearMoneda(concepto.monto) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Recurrencia:</span>
              <span class="valor">{{ concepto.recurrencia }}</span>
            </div>
            <div v-if="concepto.tipo === 'cuota'" class="detail-item">
              <span class="label">Día de Cobro:</span>
              <span class="valor">{{ concepto.dia_cobro === 0 ? 'Último día' : `Día ${concepto.dia_cobro}` }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Vigencia:</span>
              <span class="valor">{{ formatearFecha(concepto.fecha_inicio) }} {{ concepto.fecha_fin ? `- ${formatearFecha(concepto.fecha_fin)}` : '(Sin límite)' }}</span>
            </div>
          </div>

          <div class="concepto-actions">
            <button @click="editarConcepto(concepto)" class="btn-icon">
              <ion-icon name="pencil-outline"></ion-icon>
              Editar
            </button>
            <button @click="eliminarConcepto(concepto.id)" class="btn-icon danger">
              <ion-icon name="trash-outline"></ion-icon>
              Eliminar
            </button>
          </div>
        </div>
      </div>

      <!-- Modal Concepto -->
      <div v-if="mostrarModalConcepto" class="modal-overlay" @click.self="cerrarModalConcepto">
        <div class="modal-contenedor modal-grande">
          <div class="modal-header">
            <h2>{{ conceptoEditando ? 'Editar' : 'Nuevo' }} Concepto de Pago</h2>
            <button @click="cerrarModalConcepto" class="btn-close">
              <ion-icon name="close-outline"></ion-icon>
            </button>
          </div>

          <div class="modal-body">
            <div class="grid-2">
              <div class="form-group">
                <label>Nombre *</label>
                <input v-model="formularioConcepto.nombre" type="text" placeholder="Ej: Cuota Mensual">
              </div>
              <div class="form-group">
                <label>Monto *</label>
                <input v-model.number="formularioConcepto.monto" type="number" step="0.01" placeholder="0.00">
              </div>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label>Tipo de Concepto *</label>
                <select v-model="formularioConcepto.tipo">
                  <option value="cuota">Cuota (Recurrente)</option>
                  <option value="multa">Multa (Una sola vez)</option>
                  <option value="derecho">Derecho (Una sola vez)</option>
                </select>
              </div>
              <div class="form-group">
                <label>Recurrencia *</label>
                <select v-model="formularioConcepto.recurrencia">
                  <option value="diario">Diario</option>
                  <option value="semanal">Semanal</option>
                  <option value="mensual">Mensual</option>
                  <option value="bimestral">Bimestral</option>
                  <option value="trimestral">Trimestral</option>
                  <option value="semestral">Semestral</option>
                  <option value="anual">Anual</option>
                </select>
              </div>
            </div>

            <div v-if="formularioConcepto.tipo === 'cuota'" class="grid-2">
              <div class="form-group">
                <label>Día de Cobro (1-31, 0=Último día) *</label>
                <input v-model.number="formularioConcepto.dia_cobro" type="number" min="0" max="31">
              </div>
              <div class="form-group">
                <label>Cada cuántos períodos</label>
                <input v-model.number="formularioConcepto.cada_n_periodos" type="number" min="1">
              </div>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label>Fecha de Inicio de Cobranza *</label>
                <input v-model="formularioConcepto.fecha_inicio" type="date">
              </div>
              <div class="form-group">
                <label>Fecha de Finalización (Opcional)</label>
                <input v-model="formularioConcepto.fecha_fin" type="date">
              </div>
            </div>

            <div class="form-group">
              <label>Descripción</label>
              <textarea v-model="formularioConcepto.descripcion" placeholder="Descripción del concepto"></textarea>
            </div>

            <div class="form-group checkbox">
              <label>
                <input type="checkbox" v-model="formularioConcepto.activo">
                Concepto activo
              </label>
            </div>

            <div class="modal-actions">
              <button @click="cerrarModalConcepto" class="btn-secondary">Cancelar</button>
              <button @click="guardarConcepto" class="btn-primary" :disabled="cargandoConcepto">
                {{ cargandoConcepto ? 'Guardando...' : 'Guardar Concepto' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab: Métodos de Pago -->
    <div v-if="tabConfig === 'metodos'" class="tab-content">
      <div class="section-header">
        <h3>Métodos de Pago</h3>
        <button @click="abrirModalMetodo()" class="btn-primary">
          <ion-icon name="add-outline"></ion-icon>
          Nuevo Método
        </button>
      </div>

      <div class="metodos-grid">
        <div v-for="metodo in metodos" :key="metodo.id" class="metodo-card">
          <div class="metodo-icon">
            <ion-icon :name="getIconoMetodo(metodo.tipo)"></ion-icon>
          </div>
          <h4>{{ metodo.nombre }}</h4>
          <p class="metodo-tipo">{{ metodo.tipo }}</p>
          <p v-if="metodo.descripcion" class="metodo-descripcion">{{ metodo.descripcion }}</p>

          <div class="metodo-actions">
            <button @click="editarMetodo(metodo)" class="btn-icon">
              <ion-icon name="pencil-outline"></ion-icon>
            </button>
            <button @click="eliminarMetodo(metodo.id)" class="btn-icon danger">
              <ion-icon name="trash-outline"></ion-icon>
            </button>
          </div>
        </div>
      </div>

      <!-- Modal Método -->
      <div v-if="mostrarModalMetodo" class="modal-overlay" @click.self="cerrarModalMetodo">
        <div class="modal-contenedor">
          <div class="modal-header">
            <h2>{{ metodoEditando ? 'Editar' : 'Nuevo' }} Método de Pago</h2>
            <button @click="cerrarModalMetodo" class="btn-close">
              <ion-icon name="close-outline"></ion-icon>
            </button>
          </div>

          <div class="modal-body">
            <div class="form-group">
              <label>Nombre *</label>
              <input v-model="formularioMetodo.nombre" type="text" placeholder="Ej: Transferencia Bancaria">
            </div>

            <div class="form-group">
              <label>Tipo de Método *</label>
              <select v-model="formularioMetodo.tipo">
                <option value="efectivo">Efectivo</option>
                <option value="transferencia">Transferencia Bancaria</option>
                <option value="deposito">Depósito Bancario</option>
                <option value="billetera_digital">Billetera Digital</option>
              </select>
            </div>

            <div class="form-group">
              <label>Descripción / Instrucciones</label>
              <textarea v-model="formularioMetodo.descripcion" placeholder="Instrucciones para usar este método de pago"></textarea>
            </div>

            <div class="modal-actions">
              <button @click="cerrarModalMetodo" class="btn-secondary">Cancelar</button>
              <button @click="guardarMetodo" class="btn-primary" :disabled="cargandoMetodo">
                {{ cargandoMetodo ? 'Guardando...' : 'Guardar Método' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab: Asignación Masiva -->
    <div v-if="tabConfig === 'asignacion'" class="tab-content">
      <div class="section-header">
        <h3>Asignación Masiva de Cuotas</h3>
      </div>
      
      <div class="asignacion-box">
        <p class="asignacion-desc">
          Esta acción asignará todos los <strong>Conceptos de Pago activos de tipo Cuota</strong> a <strong>todos los usuarios activos</strong> en el sistema, y generará automáticamente sus recibos pendientes empezando desde la fecha seleccionada.
        </p>

        <div class="form-group" style="max-width: 300px; margin-top: 20px;">
          <label>Fecha de Inicio de Cobranza *</label>
          <input v-model="fechaInicioMasiva" type="date">
          <small class="help-text">Ejemplo: 01/05/2026</small>
        </div>

        <div v-if="mensajeMasivo" :class="['alert-box', tipoMensajeMasivo]">
          <ion-icon :name="tipoMensajeMasivo === 'success' ? 'checkmark-circle' : 'alert-circle'"></ion-icon>
          <span>{{ mensajeMasivo }}</span>
        </div>

        <button 
          class="btn-primary btn-large mt-4" 
          @click="ejecutarAsignacionMasiva" 
          :disabled="cargandoMasivo || !fechaInicioMasiva"
        >
          <ion-icon name="flash-outline"></ion-icon>
          {{ cargandoMasivo ? 'Procesando a todos los usuarios...' : 'Ejecutar Asignación Masiva' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'

const tabConfig = ref('conceptos')
const conceptos = ref([])
const metodos = ref([])

// Asignación Masiva
const fechaInicioMasiva = ref('2026-05-01')
const cargandoMasivo = ref(false)
const mensajeMasivo = ref('')
const tipoMensajeMasivo = ref('success')

// Modal Concepto
const mostrarModalConcepto = ref(false)
const conceptoEditando = ref(null)
const cargandoConcepto = ref(false)
const formularioConcepto = ref({
  nombre: '',
  descripcion: '',
  monto: 0,
  tipo: 'cuota',
  recurrencia: 'mensual',
  dia_cobro: 1,
  cada_n_periodos: 1,
  fecha_inicio: new Date().toISOString().split('T')[0],
  fecha_fin: null,
  activo: true
})

// Modal Método
const mostrarModalMetodo = ref(false)
const metodoEditando = ref(null)
const cargandoMetodo = ref(false)
const formularioMetodo = ref({
  nombre: '',
  tipo: 'efectivo',
  descripcion: ''
})

const formatearMoneda = (monto) => {
  return new Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN' }).format(monto)
}

const formatearFecha = (fecha) => {
  if (!fecha) return '-'
  return new Date(fecha).toLocaleDateString('es-PE')
}

const getIconoMetodo = (tipo) => {
  const iconos = {
    efectivo: 'cash-outline',
    transferencia: 'swap-horizontal-outline',
    deposito: 'wallet-outline',
    billetera_digital: 'phone-portrait-outline'
  }
  return iconos[tipo] || 'card-outline'
}

// Conceptos
const cargarConceptos = async () => {
  try {
    const res = await api.get('/cobranza/conceptos')
    conceptos.value = res.data.data || []
  } catch (error) {
    console.error('Error cargando conceptos:', error)
  }
}

const abrirModalConcepto = () => {
  conceptoEditando.value = null
  formularioConcepto.value = {
    nombre: '',
    descripcion: '',
    monto: 0,
    tipo: 'cuota',
    recurrencia: 'mensual',
    dia_cobro: 1,
    cada_n_periodos: 1,
    fecha_inicio: new Date().toISOString().split('T')[0],
    fecha_fin: null,
    activo: true
  }
  mostrarModalConcepto.value = true
}

const editarConcepto = (concepto) => {
  conceptoEditando.value = concepto
  formularioConcepto.value = {
    nombre: concepto.nombre,
    descripcion: concepto.descripcion || '',
    monto: concepto.monto,
    tipo: concepto.tipo,
    recurrencia: concepto.recurrencia,
    dia_cobro: concepto.dia_cobro || 1,
    cada_n_periodos: concepto.cada_n_periodos || 1,
    fecha_inicio: concepto.fecha_inicio?.split('T')[0],
    fecha_fin: concepto.fecha_fin?.split('T')[0] || null,
    activo: concepto.activo
  }
  mostrarModalConcepto.value = true
}

const cerrarModalConcepto = () => {
  mostrarModalConcepto.value = false
  conceptoEditando.value = null
}

const guardarConcepto = async () => {
  cargandoConcepto.value = true
  try {
    const payload = { ...formularioConcepto.value }
    // Asegurar formato de fechas para el backend (datetime)
    if (payload.fecha_inicio) payload.fecha_inicio = payload.fecha_inicio + 'T00:00:00'
    if (payload.fecha_fin) {
      payload.fecha_fin = payload.fecha_fin + 'T00:00:00'
    } else {
      payload.fecha_fin = null
    }

    if (conceptoEditando.value) {
      await api.put(`/cobranza/conceptos/${conceptoEditando.value.id}`, payload)
    } else {
      await api.post('/cobranza/conceptos', payload)
    }
    cerrarModalConcepto()
    await cargarConceptos()
  } catch (error) {
    console.error('Error guardando concepto:', error.response?.data || error)
    alert(error.response?.data?.detail || 'Error al guardar el concepto')
  } finally {
    cargandoConcepto.value = false
  }
}

const eliminarConcepto = async (id) => {
  if (!confirm('¿Eliminar este concepto? Se perderán todas sus cuotas asociadas.')) return
  try {
    await api.delete(`/cobranza/conceptos/${id}`)
    await cargarConceptos()
  } catch (error) {
    console.error('Error eliminando concepto:', error)
    alert('Error al eliminar el concepto')
  }
}

// Métodos
const cargarMetodos = async () => {
  // Por ahora métodos hardcodeados, se pueden guardar en BD si es necesario
  metodos.value = [
    { id: 1, nombre: 'Efectivo', tipo: 'efectivo', descripcion: 'Pago en efectivo en oficina' },
    { id: 2, nombre: 'Transferencia Bancaria', tipo: 'transferencia', descripcion: 'Transferencia a cuenta bancaria' },
    { id: 3, nombre: 'Depósito Bancario', tipo: 'deposito', descripcion: 'Depósito en cualquier banco' },
    { id: 4, nombre: 'Billetera Digital', tipo: 'billetera_digital', descripcion: 'A través de aplicación de billetera' }
  ]
}

const abrirModalMetodo = () => {
  metodoEditando.value = null
  formularioMetodo.value = {
    nombre: '',
    tipo: 'efectivo',
    descripcion: ''
  }
  mostrarModalMetodo.value = true
}

const editarMetodo = (metodo) => {
  metodoEditando.value = metodo
  formularioMetodo.value = { ...metodo }
  mostrarModalMetodo.value = true
}

const cerrarModalMetodo = () => {
  mostrarModalMetodo.value = false
  metodoEditando.value = null
}

const guardarMetodo = async () => {
  cargandoMetodo.value = true
  try {
    // Métodos se guardan en BD cuando se implemente
    alert('Método guardado correctamente')
    cerrarModalMetodo()
    await cargarMetodos()
  } catch (error) {
    console.error('Error guardando método:', error)
  } finally {
    cargandoMetodo.value = false
  }
}

const eliminarMetodo = (id) => {
  if (!confirm('¿Eliminar este método de pago?')) return
  // Implementar eliminación
  alert('Método eliminado correctamente')
}

// Asignación Masiva
const ejecutarAsignacionMasiva = async () => {
  if (!fechaInicioMasiva.value) return;
  if (!confirm(`¿Estás seguro que deseas generar cuotas para TODOS los usuarios activos empezando desde el ${formatearFecha(fechaInicioMasiva.value)}? Esta acción no se puede deshacer.`)) {
    return;
  }
  
  cargandoMasivo.value = true;
  mensajeMasivo.value = '';
  
  try {
    const res = await api.post('/cobranza/asignar-masivo', {
      fecha_inicio_cobranza: fechaInicioMasiva.value + 'T00:00:00'
    });
    
    tipoMensajeMasivo.value = 'success';
    mensajeMasivo.value = res.data.message || 'Asignación masiva completada con éxito.';
  } catch (error) {
    console.error('Error en asignación masiva:', error);
    tipoMensajeMasivo.value = 'error';
    mensajeMasivo.value = error.response?.data?.detail || 'Ocurrió un error al procesar la asignación masiva.';
  } finally {
    cargandoMasivo.value = false;
  }
}

onMounted(() => {
  cargarConceptos()
  cargarMetodos()
})
</script>

<style scoped>
.config-cobranza-container {
  padding: 0;
}

.config-header {
  background: white;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 20px;
  border-radius: 8px;
}

.config-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.config-tabs {
  display: flex;
  gap: 0;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 20px;
}

.tab {
  flex: 1;
  padding: 12px 16px;
  border: none;
  background: #f8fafc;
  cursor: pointer;
  font-weight: 500;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
}

.tab:hover { background: #f1f5f9; }
.tab.active {
  background: white;
  color: #4f46e5;
  border-bottom: 2px solid #4f46e5;
}

.tab-content {
  background: white;
  padding: 24px;
  border-radius: 8px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
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
  transition: background 0.2s;
}

.btn-primary:hover { background: #4338ca; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }

/* Conceptos Grid */
.conceptos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.concepto-card {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
  background: #fafbfc;
  transition: all 0.2s;
}

.concepto-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.concepto-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 12px;
}

.concepto-header h4 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.tipo-badge {
  font-size: 12px;
  color: #64748b;
  text-transform: capitalize;
  margin: 4px 0 0 0;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.badge.activo { background: #dcfce7; color: #166534; }
.badge.inactivo { background: #fee2e2; color: #991b1b; }

.concepto-details {
  margin-bottom: 12px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  margin-bottom: 6px;
}

.detail-item .label {
  font-weight: 600;
  color: #64748b;
}

.detail-item .valor {
  color: #1e293b;
  text-align: right;
}

.concepto-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  flex: 1;
  padding: 8px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  color: #4f46e5;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  transition: all 0.2s;
}

.btn-icon:hover {
  background: #f1f5f9;
  border-color: #4f46e5;
}

.btn-icon.danger {
  color: #dc2626;
}

.btn-icon.danger:hover {
  background: #fee2e2;
  border-color: #dc2626;
}

/* Métodos Grid */
.metodos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.metodo-card {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 20px;
  background: #fafbfc;
  text-align: center;
  transition: all 0.2s;
}

.metodo-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.metodo-icon {
  font-size: 36px;
  color: #4f46e5;
  margin-bottom: 12px;
}

.metodo-card h4 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 6px 0;
}

.metodo-tipo {
  font-size: 12px;
  color: #64748b;
  text-transform: capitalize;
  margin: 0 0 8px 0;
}

.metodo-descripcion {
  font-size: 13px;
  color: #64748b;
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.metodo-actions {
  display: flex;
  gap: 8px;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-contenedor {
  background: white;
  border-radius: 12px;
  max-height: 90vh;
  width: 100%;
  max-width: 500px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 20px 25px rgba(0,0,0,0.15);
}

.modal-grande { max-width: 600px; }

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h2 {
  font-size: 18px;
  font-weight: 700;
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  color: #64748b;
  font-size: 20px;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 6px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
}

.form-group textarea {
  min-height: 80px;
  resize: vertical;
}

.form-group.checkbox label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-group.checkbox input {
  width: auto;
  margin: 0;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.btn-secondary {
  padding: 10px 16px;
  background: #f1f5f9;
  color: #1e293b;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .conceptos-grid,
  .metodos-grid {
    grid-template-columns: 1fr;
  }

  .grid-2 { grid-template-columns: 1fr; }

  .config-tabs {
    flex-wrap: wrap;
  }
}

/* Asignacion Masiva */
.asignacion-box {
  background: #fafbfc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 24px;
}

.asignacion-desc {
  font-size: 15px;
  color: #334155;
  line-height: 1.6;
  margin: 0;
}

.asignacion-desc strong {
  color: #0f172a;
}

.help-text {
  display: block;
  font-size: 12px;
  color: #64748b;
  margin-top: 4px;
}

.mt-4 {
  margin-top: 24px;
}

.btn-large {
  padding: 12px 24px;
  font-size: 15px;
}

.alert-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 6px;
  margin-top: 20px;
  font-size: 14px;
  font-weight: 500;
}

.alert-box.success {
  background: #ecfdf5;
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.alert-box.error {
  background: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.alert-box ion-icon {
  font-size: 20px;
}
</style>
