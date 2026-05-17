<template>
  <div class="operaciones-view">
    <!-- ESTADÍSTICAS RÁPIDAS -->
    <div class="stats-container">
      <div class="stat-card">
        <div class="stat-icon pendientes">
          <ion-icon name="time-outline"></ion-icon>
        </div>
        <div class="stat-content">
          <span class="stat-label">Pendientes</span>
          <span class="stat-number">{{ pagosPendientes.length }}</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon por-revisar">
          <ion-icon name="alert-circle-outline"></ion-icon>
        </div>
        <div class="stat-content">
          <span class="stat-label">Por Revisar</span>
          <span class="stat-number">{{ formatearMoneda(totalPendiente) }}</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon aprobados">
          <ion-icon name="checkmark-circle-outline"></ion-icon>
        </div>
        <div class="stat-content">
          <span class="stat-label">Aprobados</span>
          <span class="stat-number">{{ pagosPagadas.length }}</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon procesado">
          <ion-icon name="cash-outline"></ion-icon>
        </div>
        <div class="stat-content">
          <span class="stat-label">Procesado</span>
          <span class="stat-number">{{ formatearMoneda(totalPagado) }}</span>
        </div>
      </div>
    </div>

    <!-- BREAKDOWN POR MÉTODO DE PAGO -->
    <div class="metodo-breakdown">
      <div class="breakdown-title">
        <ion-icon name="layers-outline"></ion-icon>
        Distribución por Método
      </div>
      <div class="breakdown-items">
        <div class="breakdown-item">
          <div class="breakdown-method">
            <ion-icon name="cash-outline"></ion-icon>
            <span>Efectivo</span>
          </div>
          <div class="breakdown-stats">
            <span class="breakdown-count">{{ pagosPorMetodo.efectivo.count }}</span>
            <span class="breakdown-amount">{{ formatearMoneda(pagosPorMetodo.efectivo.total) }}</span>
          </div>
        </div>

        <div class="breakdown-item">
          <div class="breakdown-method">
            <ion-icon name="swap-horizontal-outline"></ion-icon>
            <span>Transferencia</span>
          </div>
          <div class="breakdown-stats">
            <span class="breakdown-count">{{ pagosPorMetodo.transferencia.count }}</span>
            <span class="breakdown-amount">{{ formatearMoneda(pagosPorMetodo.transferencia.total) }}</span>
          </div>
        </div>

        <div class="breakdown-item">
          <div class="breakdown-method">
            <ion-icon name="wallet-outline"></ion-icon>
            <span>Depósito</span>
          </div>
          <div class="breakdown-stats">
            <span class="breakdown-count">{{ pagosPorMetodo.deposito.count }}</span>
            <span class="breakdown-amount">{{ formatearMoneda(pagosPorMetodo.deposito.total) }}</span>
          </div>
        </div>

        <div class="breakdown-item">
          <div class="breakdown-method">
            <ion-icon name="phone-portrait-outline"></ion-icon>
            <span>Billetera</span>
          </div>
          <div class="breakdown-stats">
            <span class="breakdown-count">{{ pagosPorMetodo.billetera_digital.count }}</span>
            <span class="breakdown-amount">{{ formatearMoneda(pagosPorMetodo.billetera_digital.total) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabs para Pendientes y Pagadas -->
    <div class="tabs-container">
      <button
        :class="['tab-btn', { active: tabActivo === 'pendientes' }]"
        @click="() => { tabActivo = 'pendientes'; filtroMetodoPagadas = null }"
      >
        <ion-icon name="time-outline"></ion-icon>
        Pendientes de Aprobación
        <span class="badge-count">{{ pagosPendientes.length }}</span>
      </button>
      <button
        :class="['tab-btn', { active: tabActivo === 'pagadas' }]"
        @click="tabActivo = 'pagadas'"
      >
        <ion-icon name="checkmark-circle-outline"></ion-icon>
        Pagadas
        <span class="badge-count">{{ pagosPagadas.length }}</span>
      </button>
    </div>

    <!-- TAB: Pendientes -->
    <div v-if="tabActivo === 'pendientes'" class="tab-content">
      <div class="content-header">
        <h2>Pagos Pendientes de Aprobación</h2>
        <div class="stats-bar">
          <div class="stat">
            <span class="stat-label">Total a Revisar</span>
            <span class="stat-value">{{ formatearMoneda(totalPendiente) }}</span>
          </div>
        </div>
      </div>

      <div class="content-container">
        <div v-if="pagosPendientes.length === 0" class="empty-state">
          <ion-icon name="checkmark-circle-outline"></ion-icon>
          <p>No hay pagos pendientes de aprobación</p>
        </div>

        <div v-else class="tabla-responsiva">
          <table class="pagos-tabla">
            <thead>
              <tr>
                <th>Usuario</th>
                <th>Concepto</th>
                <th>Monto</th>
                <th>Método</th>
                <th>Referencia</th>
                <th>Fecha</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="pago in pagosPendientes" :key="pago.id">
                <td class="usuario-cell">{{ pago.usuario_nombre }}</td>
                <td>{{ pago.concepto }}</td>
                <td class="monto-cell">{{ formatearMoneda(pago.monto) }}</td>
                <td>
                  <span class="badge" :class="`method-${pago.metodo_pago}`">
                    {{ formatoMetodo(pago.metodo_pago) }}
                  </span>
                </td>
                <td>{{ pago.referencia || '-' }}</td>
                <td class="fecha-cell">{{ formatarFecha(pago.created_at) }}</td>
                <td class="acciones-cell">
                  <button
                    @click="abrirModalDetalle(pago)"
                    class="btn-action"
                    title="Ver detalle"
                    :disabled="procesando[pago.id]"
                  >
                    <ion-icon name="eye-outline"></ion-icon>
                  </button>
                  <button
                    @click="abrirModalAprobar(pago)"
                    class="btn-action btn-aprobar"
                    title="Aprobar"
                    :disabled="procesando[pago.id]"
                  >
                    <ion-icon name="checkmark-outline"></ion-icon>
                  </button>
                  <button
                    @click="abrirModalRechazo(pago.id)"
                    class="btn-action btn-rechazar"
                    title="Rechazar"
                    :disabled="procesando[pago.id]"
                  >
                    <ion-icon name="close-outline"></ion-icon>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB: Pagadas -->
    <div v-if="tabActivo === 'pagadas'" class="tab-content">
      <div class="content-header">
        <h2>Pagos Aprobados</h2>
        <div class="stats-bar">
          <div class="stat">
            <span class="stat-label">Total Procesado</span>
            <span class="stat-value">{{ formatearMoneda(totalPagado) }}</span>
          </div>
        </div>
      </div>

      <!-- Filtro por método de pago -->
      <div class="filtro-grupo">
        <button
          :class="['filtro-btn', { active: filtroMetodoPagadas === null }]"
          @click="filtroMetodoPagadas = null"
        >
          <ion-icon name="layers-outline"></ion-icon>
          Todos
        </button>
        <button
          :class="['filtro-btn', { active: filtroMetodoPagadas === 'efectivo' }]"
          @click="filtroMetodoPagadas = 'efectivo'"
        >
          <ion-icon name="cash-outline"></ion-icon>
          Efectivo
        </button>
        <button
          :class="['filtro-btn', { active: filtroMetodoPagadas === 'transferencia' }]"
          @click="filtroMetodoPagadas = 'transferencia'"
        >
          <ion-icon name="swap-horizontal-outline"></ion-icon>
          Transferencia
        </button>
        <button
          :class="['filtro-btn', { active: filtroMetodoPagadas === 'deposito' }]"
          @click="filtroMetodoPagadas = 'deposito'"
        >
          <ion-icon name="wallet-outline"></ion-icon>
          Depósito
        </button>
        <button
          :class="['filtro-btn', { active: filtroMetodoPagadas === 'billetera_digital' }]"
          @click="filtroMetodoPagadas = 'billetera_digital'"
        >
          <ion-icon name="phone-portrait-outline"></ion-icon>
          Billetera
        </button>
      </div>

      <div class="content-container">
        <div v-if="pagosPagadasFiltradas.length === 0" class="empty-state">
          <ion-icon name="document-outline"></ion-icon>
          <p>No hay pagos aprobados</p>
        </div>

        <div v-else class="tabla-responsiva">
          <table class="pagos-tabla">
            <thead>
              <tr>
                <th>Usuario</th>
                <th>Concepto</th>
                <th>Monto</th>
                <th>Método</th>
                <th>Referencia</th>
                <th>Fecha Pago</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="pago in pagosPagadasFiltradas" :key="pago.id">
                <td class="usuario-cell">{{ pago.usuario_nombre }}</td>
                <td>{{ pago.concepto }}</td>
                <td class="monto-cell">{{ formatearMoneda(pago.monto) }}</td>
                <td>
                  <span class="badge" :class="`method-${pago.metodo_pago}`">
                    {{ formatoMetodo(pago.metodo_pago) }}
                  </span>
                </td>
                <td>{{ pago.referencia || '-' }}</td>
                <td class="fecha-cell">{{ formatarFecha(pago.created_at) }}</td>
                <td class="acciones-cell">
                  <button
                    @click="abrirModalDetalle(pago)"
                    class="btn-action"
                    title="Ver detalle"
                  >
                    <ion-icon name="eye-outline"></ion-icon>
                  </button>
                  <button
                    @click="descargarPDF(pago.id)"
                    class="btn-action"
                    title="Descargar PDF"
                  >
                    <ion-icon name="download-outline"></ion-icon>
                  </button>
                  <button
                    @click="imprimirPDF(pago.id)"
                    class="btn-action"
                    title="Imprimir"
                  >
                    <ion-icon name="print-outline"></ion-icon>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal de detalle -->
    <div v-if="pagoDetalle" class="modal-overlay" @click="cerrarModalDetalle">
      <div class="modal modal-wide" @click.stop>

        <!-- Hero perfil del pago -->
        <div class="pago-hero">
          <button class="close-btn-hero" @click="cerrarModalDetalle">
            <ion-icon name="close-outline"></ion-icon>
          </button>

          <!-- Avatar iniciales usuario -->
          <div class="pago-avatar">
            <span>{{ inicialesNombre(pagoDetalle.usuario_nombre) }}</span>
          </div>
          <h3 class="pago-hero-nombre">{{ pagoDetalle.usuario_nombre }}</h3>
          <p class="pago-hero-concepto">{{ pagoDetalle.concepto }}</p>

          <!-- Monto destacado -->
          <div class="pago-hero-monto">{{ formatearMoneda(pagoDetalle.monto) }}</div>

          <!-- Pills: método + estado -->
          <div class="pago-hero-pills">
            <span class="hero-pill method">
              <ion-icon :name="iconoMetodo(pagoDetalle.metodo_pago)"></ion-icon>
              {{ formatoMetodo(pagoDetalle.metodo_pago) }}
            </span>
            <span :class="['hero-pill', 'estado', pagoDetalle.estado]">
              <ion-icon :name="iconoEstado(pagoDetalle.estado)"></ion-icon>
              {{ formatarEstado(pagoDetalle.estado) }}
            </span>
          </div>
        </div>

        <!-- Body en dos columnas -->
        <div class="pago-modal-body">

          <!-- Col 1: Detalles -->
          <div class="pago-col-info">
            <div class="info-title">
              <ion-icon name="document-text-outline"></ion-icon>
              Información del pago
            </div>
            <div class="info-row" v-if="pagoDetalle.referencia">
              <span class="ir-label">Referencia</span>
              <span class="ir-val">{{ pagoDetalle.referencia }}</span>
            </div>
            <div class="info-row" v-if="pagoDetalle.observaciones">
              <span class="ir-label">Observaciones</span>
              <span class="ir-val">{{ pagoDetalle.observaciones }}</span>
            </div>
            <div class="info-row">
              <span class="ir-label">Fecha registro</span>
              <span class="ir-val">{{ formatarFecha(pagoDetalle.created_at) }}</span>
            </div>
          </div>

          <!-- Col 2: Acciones -->
          <div class="pago-col-acciones">
            <div class="info-title">
              <ion-icon name="settings-outline"></ion-icon>
              Acciones
            </div>

            <template v-if="pagoDetalle.estado === 'pendiente_aprobacion'">
              <button
                @click="abrirModalAprobar(pagoDetalle)"
                class="accion-btn btn-aprobar-modal"
              >
                <ion-icon name="checkmark-circle-outline"></ion-icon>
                Aprobar pago
              </button>
              <button
                @click="abrirModalRechazo(pagoDetalle.id)"
                class="accion-btn btn-rechazar-modal"
              >
                <ion-icon name="close-circle-outline"></ion-icon>
                Rechazar pago
              </button>
            </template>

            <div v-else class="estado-final" :class="pagoDetalle.estado">
              <ion-icon :name="iconoEstado(pagoDetalle.estado)"></ion-icon>
              <span>{{ formatarEstado(pagoDetalle.estado) }}</span>
            </div>

            <button @click="cerrarModalDetalle" class="accion-btn btn-cerrar-modal">
              <ion-icon name="arrow-back-outline"></ion-icon>
              Cerrar
            </button>
          </div>
        </div>

      </div>
    </div>

    <!-- Modal de confirmación de aprobación -->
    <div v-if="modalAprobar.visible" class="modal-overlay" @click="cerrarModalAprobar">
      <div class="modal modal-confirm" @click.stop>

        <div class="pago-hero hero-green">
          <button class="close-btn-hero" @click="cerrarModalAprobar">
            <ion-icon name="close-outline"></ion-icon>
          </button>
          <div class="pago-avatar avatar-green">
            <ion-icon name="checkmark-outline" style="font-size:32px;color:white;"></ion-icon>
          </div>
          <h3 class="pago-hero-nombre">Aprobar Pago</h3>
          <p class="pago-hero-concepto" v-if="modalAprobar.pago">{{ modalAprobar.pago.usuario_nombre }}</p>
          <div class="pago-hero-monto" v-if="modalAprobar.pago">{{ formatearMoneda(modalAprobar.pago.monto) }}</div>
          <div class="pago-hero-pills" v-if="modalAprobar.pago">
            <span class="hero-pill method">
              <ion-icon :name="iconoMetodo(modalAprobar.pago.metodo_pago)"></ion-icon>
              {{ formatoMetodo(modalAprobar.pago.metodo_pago) }}
            </span>
          </div>
        </div>

        <div class="confirm-body" v-if="modalAprobar.pago">
          <div class="info-row">
            <span class="ir-label">Concepto</span>
            <span class="ir-val">{{ modalAprobar.pago.concepto }}</span>
          </div>
          <div class="info-row" v-if="modalAprobar.pago.referencia">
            <span class="ir-label">Referencia</span>
            <span class="ir-val">{{ modalAprobar.pago.referencia }}</span>
          </div>
          <div class="info-row" v-if="modalAprobar.pago.observaciones">
            <span class="ir-label">Observaciones</span>
            <span class="ir-val">{{ modalAprobar.pago.observaciones }}</span>
          </div>

          <p class="confirm-question">¿Confirmas la aprobación de este pago?</p>

          <div class="confirm-actions">
            <button @click="cerrarModalAprobar" class="accion-btn btn-cerrar-modal">Cancelar</button>
            <button
              @click="confirmarAprobar"
              :disabled="procesando[modalAprobar.pago?.id]"
              class="accion-btn btn-aprobar-modal"
            >
              <ion-icon name="checkmark-circle-outline"></ion-icon>
              Confirmar Aprobación
            </button>
          </div>
        </div>

      </div>
    </div>

    <!-- Modal de rechazo -->
    <div v-if="modalRechazo.visible" class="modal-overlay" @click="cerrarModalRechazo">
      <div class="modal modal-confirm" @click.stop>

        <div class="pago-hero hero-red">
          <button class="close-btn-hero" @click="cerrarModalRechazo">
            <ion-icon name="close-outline"></ion-icon>
          </button>
          <div class="pago-avatar avatar-red">
            <ion-icon name="close-outline" style="font-size:32px;color:white;"></ion-icon>
          </div>
          <h3 class="pago-hero-nombre">Rechazar Pago</h3>
          <p class="pago-hero-concepto">Indica el motivo del rechazo</p>
        </div>

        <div class="confirm-body">
          <textarea
            v-model="modalRechazo.motivo"
            placeholder="Ingrese el motivo del rechazo..."
            class="textarea"
          ></textarea>
          <div class="confirm-actions">
            <button @click="cerrarModalRechazo" class="accion-btn btn-cerrar-modal">Cancelar</button>
            <button
              @click="confirmarRechazo"
              :disabled="!modalRechazo.motivo || procesando[modalRechazo.pagoId]"
              class="accion-btn btn-rechazar-modal"
            >
              <ion-icon name="close-circle-outline"></ion-icon>
              Confirmar Rechazo
            </button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { alertStore } from '../../stores/alertStore'

const pagosPendientes = ref([])
const pagosPagadas = ref([])
const procesando = ref({})
const tabActivo = ref('pendientes')
const pagoDetalle = ref(null)
const filtroMetodoPagadas = ref(null)
const modalRechazo = ref({
  visible: false,
  pagoId: null,
  motivo: ''
})
const modalAprobar = ref({
  visible: false,
  pago: null
})

const totalPendiente = computed(() => {
  return pagosPendientes.value.reduce((sum, pago) => sum + pago.monto, 0)
})

const totalPagado = computed(() => {
  return pagosPagadas.value.reduce((sum, pago) => sum + pago.monto, 0)
})

const pagosPagadasFiltradas = computed(() => {
  if (!filtroMetodoPagadas.value) return pagosPagadas.value
  return pagosPagadas.value.filter(p => p.metodo_pago === filtroMetodoPagadas.value)
})

const pagosPorMetodo = computed(() => {
  const allPagos = [...pagosPendientes.value, ...pagosPagadas.value]
  const metodos = {
    efectivo: { count: 0, total: 0 },
    transferencia: { count: 0, total: 0 },
    deposito: { count: 0, total: 0 },
    billetera_digital: { count: 0, total: 0 }
  }

  allPagos.forEach(pago => {
    const metodo = pago.metodo_pago || 'transferencia'
    if (metodos[metodo]) {
      metodos[metodo].count++
      metodos[metodo].total += pago.monto
    }
  })

  return metodos
})

const pagosPorMetodoPagadas = computed(() => {
  const metodos = {
    efectivo: { count: 0, total: 0 },
    transferencia: { count: 0, total: 0 },
    deposito: { count: 0, total: 0 },
    billetera_digital: { count: 0, total: 0 }
  }

  pagosPagadas.value.forEach(pago => {
    const metodo = pago.metodo_pago || 'transferencia'
    if (metodos[metodo]) {
      metodos[metodo].count++
      metodos[metodo].total += pago.monto
    }
  })

  return metodos
})

const formatearMoneda = (monto) => {
  return new Intl.NumberFormat('es-PE', {
    style: 'currency',
    currency: 'PEN'
  }).format(monto)
}

const formatarFecha = (fecha) => {
  const date = new Date(fecha)
  return date.toLocaleDateString('es-PE', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatoMetodo = (metodo) => {
  const metodos = {
    'efectivo': 'Efectivo',
    'transferencia': 'Transf. / Depósito',
    'deposito': 'Transf. / Depósito',
    'billetera_digital': 'Billetera Digital'
  }
  return metodos[metodo] || metodo
}

const formatarEstado = (estado) => {
  const estados = {
    'pendiente_aprobacion': 'Pendiente',
    'aprobado': 'Aprobado',
    'rechazado': 'Rechazado'
  }
  return estados[estado] || estado
}

const inicialesNombre = (nombre = '') =>
  nombre.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase() || 'U'

const iconoMetodo = (metodo) => ({
  efectivo: 'cash-outline',
  transferencia: 'swap-horizontal-outline',
  deposito: 'wallet-outline',
  billetera_digital: 'phone-portrait-outline'
})[metodo] || 'card-outline'

const iconoEstado = (estado) => ({
  pendiente_aprobacion: 'time-outline',
  aprobado: 'checkmark-circle-outline',
  rechazado: 'close-circle-outline'
})[estado] || 'ellipse-outline'

const cargarPagosPendientes = async () => {
  try {
    const response = await fetch('/api/cobranza/pagos/pendientes/aprobacion')
    const result = await response.json()
    if (result.success) {
      pagosPendientes.value = result.data.filter(p => p.estado === 'pendiente_aprobacion')
      pagosPagadas.value = result.data.filter(p => p.estado === 'aprobado')
    }
  } catch (error) {
    console.error('Error cargando pagos pendientes:', error)
  }
}

const cargarTodosPagos = async () => {
  try {
    // Cargar pagos pendientes
    const responsePendientes = await fetch('/api/cobranza/pagos/pendientes/aprobacion')
    const resultPendientes = await responsePendientes.json()
    if (resultPendientes.success) {
      pagosPendientes.value = resultPendientes.data
    }

    // Cargar todos los pagos para obtener los aprobados
    const responseTodos = await fetch('/api/cobranza/pagos')
    const resultTodos = await responseTodos.json()
    if (resultTodos.success) {
      pagosPagadas.value = resultTodos.data.filter(p => p.estado === 'aprobado')
    }
  } catch (error) {
    console.error('Error cargando pagos:', error)
  }
}

const abrirModalAprobar = (pago) => {
  modalAprobar.value.pago = { ...pago }
  modalAprobar.value.visible = true
}

const cerrarModalAprobar = () => {
  modalAprobar.value.visible = false
  modalAprobar.value.pago = null
}

const confirmarAprobar = async () => {
  const pagoId = modalAprobar.value.pago.id
  procesando.value[pagoId] = true
  try {
    const response = await fetch(`/api/cobranza/pagos/${pagoId}/aprobar`, {
      method: 'PUT'
    })
    const result = await response.json()
    if (result.success) {
      cerrarModalAprobar()
      cerrarModalDetalle()
      await cargarTodosPagos()
      alertStore.success('Pago aprobado', 'Pago registrado exitosamente')
    } else {
      alertStore.error('Error', 'No se pudo aprobar el pago')
    }
  } catch (error) {
    console.error('Error aprobando pago:', error)
    alertStore.error('Error', 'Error al aprobar el pago')
  } finally {
    procesando.value[pagoId] = false
  }
}

const abrirModalDetalle = (pago) => {
  pagoDetalle.value = { ...pago }
}

const cerrarModalDetalle = () => {
  pagoDetalle.value = null
}

const abrirModalRechazo = (pagoId) => {
  cerrarModalDetalle()
  modalRechazo.value.pagoId = pagoId
  modalRechazo.value.visible = true
  modalRechazo.value.motivo = ''
}

const cerrarModalRechazo = () => {
  modalRechazo.value.visible = false
  modalRechazo.value.pagoId = null
  modalRechazo.value.motivo = ''
}

const confirmarRechazo = async () => {
  if (!modalRechazo.value.motivo) return

  procesando.value[modalRechazo.value.pagoId] = true
  try {
    const response = await fetch(
      `/api/cobranza/pagos/${modalRechazo.value.pagoId}/rechazar?motivo=${encodeURIComponent(modalRechazo.value.motivo)}`,
      { method: 'PUT' }
    )
    const result = await response.json()
    if (result.success) {
      await cargarTodosPagos()
      cerrarModalRechazo()
    }
  } catch (error) {
    console.error('Error rechazando pago:', error)
  } finally {
    procesando.value[modalRechazo.value.pagoId] = false
  }
}

const descargarPDF = (pagoId) => {
  alertStore.info('Próximamente', 'Funcionalidad de descarga PDF en desarrollo')
}

const imprimirPDF = (pagoId) => {
  alertStore.info('Próximamente', 'Funcionalidad de impresión en desarrollo')
}

onMounted(() => {
  cargarTodosPagos()
  // Recargar cada 30 segundos
  setInterval(cargarTodosPagos, 30000)
})
</script>

<style scoped>
.operaciones-view {
  padding: 0;
}

/* Tabs */
.tabs-container {
  display: flex;
  gap: 0;
  background: white;
  border-bottom: 2px solid #e2e8f0;
  border-radius: 10px 10px 0 0;
  overflow: hidden;
  margin-bottom: 0;
}

.tab-btn {
  flex: 1;
  padding: 12px 16px;
  border: none;
  background: white;
  border-bottom: 3px solid transparent;
  color: #64748b;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.2s;
  font-size: 13px;
}

.tab-btn:hover {
  background: #f8fafc;
  color: #1e293b;
}

.tab-btn.active {
  color: #6366f1;
  border-bottom-color: #6366f1;
  background: #f8fafc;
}

.tab-btn ion-icon {
  font-size: 20px;
}

.badge-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 6px;
  background: #eef2ff;
  color: #6366f1;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 700;
  margin-left: 4px;
}

.tab-btn.active .badge-count {
  background: #6366f1;
  color: white;
}

.tab-content {
  background: white;
  border-radius: 0 0 10px 10px;
  padding: 16px;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e2e8f0;
}

.content-header h2 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.stats-bar {
  display: flex;
  gap: 20px;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.stat-label {
  font-size: 11px;
  color: #64748b;
  font-weight: 500;
}

.stat-value {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
}

.content-container {
  min-height: 250px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 60px 20px;
  color: #94a3b8;
}

.empty-state ion-icon {
  font-size: 64px;
  color: #cbd5e1;
}

.empty-state p {
  font-size: 16px;
  margin: 0;
}

/* Tabla */
.tabla-responsiva {
  overflow-x: auto;
}

.pagos-tabla {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.pagos-tabla thead {
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.pagos-tabla th {
  padding: 10px 12px;
  text-align: left;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  font-size: 11px;
}

.pagos-tabla td {
  padding: 10px 12px;
  border-bottom: 1px solid #e2e8f0;
  color: #1e293b;
}

.pagos-tabla tbody tr:hover {
  background: #f8fafc;
}

.usuario-cell {
  font-weight: 600;
}

.monto-cell {
  font-weight: 600;
  color: #4f46e5;
}

.fecha-cell {
  color: #64748b;
  font-size: 12px;
}

.acciones-cell {
  display: flex;
  gap: 6px;
}

.btn-action {
  padding: 6px 8px;
  border: none;
  background: none;
  color: #64748b;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-action:hover:not(:disabled) {
  color: #4f46e5;
}

.btn-action:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-action.btn-aprobar:hover:not(:disabled) {
  color: #16a34a;
}

.btn-action.btn-rechazar:hover:not(:disabled) {
  color: #dc2626;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}

.badge.method-efectivo {
  background: #dcfce7;
  color: #166534;
}

.badge.method-transferencia {
  background: #dbeafe;
  color: #0369a1;
}

.badge.method-deposito {
  background: #fce7f3;
  color: #be185d;
}

.badge.method-billetera_digital {
  background: #f3e8ff;
  color: #7e22ce;
}

.badge.aprobado {
  background: #dcfce7;
  color: #166534;
}

.badge.pendiente_aprobacion {
  background: #fef3c7;
  color: #92400e;
}

.badge.rechazado {
  background: #fee2e2;
  color: #991b1b;
}

/* ══ PREMIUM MODAL STYLES ══ */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 480px;
  box-shadow: 0 24px 40px rgba(0,0,0,0.18);
  max-height: 90vh;
  overflow-y: auto;
  overflow-x: hidden;
}

.modal-wide {
  max-width: 680px;
}

.modal-confirm {
  max-width: 440px;
}

/* ── Hero del pago ── */
.pago-hero {
  position: relative;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 60%, #a855f7 100%);
  padding: 32px 24px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  border-radius: 16px 16px 0 0;
}

.pago-hero.hero-green {
  background: linear-gradient(135deg, #059669 0%, #10b981 60%, #34d399 100%);
}

.pago-hero.hero-red {
  background: linear-gradient(135deg, #dc2626 0%, #ef4444 60%, #f87171 100%);
}

.close-btn-hero {
  position: absolute;
  top: 14px; right: 14px;
  background: rgba(255,255,255,0.15);
  border: none; border-radius: 50%;
  width: 32px; height: 32px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: white; font-size: 18px;
  transition: background 0.2s;
}
.close-btn-hero:hover { background: rgba(255,255,255,0.3); }

.pago-avatar {
  width: 68px; height: 68px;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  border: 3px solid rgba(255,255,255,0.5);
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 12px;
  font-size: 24px; font-weight: 700; color: white;
}
.avatar-green { background: rgba(255,255,255,0.25); }
.avatar-red   { background: rgba(255,255,255,0.25); }

.pago-hero-nombre {
  font-size: 17px; font-weight: 700; color: white; margin: 0 0 4px;
}
.pago-hero-concepto {
  font-size: 13px; color: rgba(255,255,255,0.75); margin: 0 0 10px;
}
.pago-hero-monto {
  font-size: 28px; font-weight: 800; color: white;
  margin-bottom: 12px;
  text-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.pago-hero-pills {
  display: flex; gap: 8px; flex-wrap: wrap; justify-content: center;
}

.hero-pill {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px; font-weight: 600;
  background: rgba(255,255,255,0.18);
  color: white;
}
.hero-pill ion-icon { font-size: 13px; }

.hero-pill.estado.pendiente_aprobacion { background: rgba(251,191,36,0.3); }
.hero-pill.estado.aprobado             { background: rgba(16,185,129,0.35); }
.hero-pill.estado.rechazado            { background: rgba(239,68,68,0.35); }

/* ── Body dos columnas (modal-wide) ── */
.pago-modal-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
}

.pago-col-info,
.pago-col-acciones {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.pago-col-info {
  border-right: 1px solid #e2e8f0;
}

.info-title {
  display: flex; align-items: center; gap: 6px;
  font-size: 11px; font-weight: 700; text-transform: uppercase;
  color: #64748b; letter-spacing: 0.5px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e2e8f0;
}
.info-title ion-icon { font-size: 14px; color: #4f46e5; }

.info-row {
  display: flex; flex-direction: column; gap: 2px;
  padding: 8px 0;
  border-bottom: 1px solid #f1f5f9;
}
.info-row:last-child { border-bottom: none; }

.ir-label {
  font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase;
}
.ir-val {
  font-size: 13px; color: #1e293b; word-break: break-word;
}

/* Botones de acción en col-acciones */
.accion-btn {
  width: 100%; padding: 11px 14px;
  border: none; border-radius: 8px;
  font-size: 13px; font-weight: 600;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center; gap: 7px;
  transition: all 0.2s;
}
.accion-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.accion-btn ion-icon { font-size: 17px; }

.btn-aprobar-modal {
  background: linear-gradient(135deg, #059669, #10b981);
  color: white;
}
.btn-aprobar-modal:hover:not(:disabled) { opacity: 0.9; }

.btn-rechazar-modal {
  background: linear-gradient(135deg, #dc2626, #ef4444);
  color: white;
}
.btn-rechazar-modal:hover:not(:disabled) { opacity: 0.9; }

.btn-cerrar-modal {
  background: #f1f5f9; color: #64748b;
  margin-top: 4px;
}
.btn-cerrar-modal:hover { background: #e2e8f0; }

.estado-final {
  display: flex; flex-direction: column; align-items: center;
  gap: 6px; padding: 16px;
  border-radius: 8px;
  font-size: 14px; font-weight: 600;
}
.estado-final ion-icon { font-size: 36px; }
.estado-final.aprobado  { background: #dcfce7; color: #166534; }
.estado-final.rechazado { background: #fee2e2; color: #991b1b; }

/* ── Confirm body (modal-confirm) ── */
.confirm-body {
  padding: 20px;
  display: flex; flex-direction: column; gap: 10px;
}

.confirm-question {
  font-size: 15px; font-weight: 600; color: #1e293b;
  text-align: center; margin: 8px 0;
}

.confirm-actions {
  display: flex; gap: 10px; margin-top: 6px;
}
.confirm-actions .accion-btn { flex: 1; }


/* ══ STATS CARDS ══ */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
  padding: 0;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  transition: all 0.2s;
}

.stat-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  font-size: 20px;
  flex-shrink: 0;
}

.stat-icon.pendientes {
  background: #fef3c7;
  color: #b45309;
}

.stat-icon.por-revisar {
  background: #fee2e2;
  color: #991b1b;
}

.stat-icon.aprobados {
  background: #dcfce7;
  color: #166534;
}

.stat-icon.procesado {
  background: #dbeafe;
  color: #0369a1;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.stat-label {
  font-size: 11px;
  font-weight: 500;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.2px;
}

.stat-number {
  font-size: 18px;
  font-weight: 700;
  color: #334155;
}

/* ══ BREAKDOWN BY METHOD ══ */
.metodo-breakdown {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 14px;
  margin-bottom: 16px;
}

.breakdown-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e2e8f0;
}

.breakdown-title ion-icon {
  font-size: 16px;
  color: #4f46e5;
}

.breakdown-items {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 10px;
}

.breakdown-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s;
}

.breakdown-item:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.breakdown-method {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #334155;
}

.breakdown-method ion-icon {
  font-size: 14px;
  color: #4f46e5;
}

.breakdown-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 1px;
}

.breakdown-count {
  font-size: 14px;
  font-weight: 700;
  color: #1e293b;
}

.breakdown-amount {
  font-size: 11px;
  color: #64748b;
  font-weight: 500;
}

/* ══ FILTER BUTTONS ══ */
.filtro-grupo {
  display: flex;
  gap: 6px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}

.filtro-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  background: white;
  color: #64748b;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.filtro-btn ion-icon {
  font-size: 16px;
}

.filtro-btn:hover {
  border-color: #cbd5e1;
  color: #4f46e5;
}

.filtro-btn.active {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  border-color: #4f46e5;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}

/* ══ BREAKDOWN PAGADAS ══ */
.metodo-breakdown-pagadas {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

.breakdown-card {
  display: flex;
  flex-direction: column;
  padding: 16px;
  border-radius: 12px;
  border: 2px solid;
  transition: all 0.2s;
}

.breakdown-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin-bottom: 10px;
}

.breakdown-header ion-icon {
  font-size: 16px;
}

.breakdown-number {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
}

.breakdown-label {
  font-size: 12px;
  font-weight: 500;
}

.efectivo-card {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-color: #fbbf24;
  color: #92400e;
}

.efectivo-card:hover {
  box-shadow: 0 4px 12px rgba(251, 191, 36, 0.2);
}

.transferencia-card {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  border-color: #60a5fa;
  color: #0369a1;
}

.transferencia-card:hover {
  box-shadow: 0 4px 12px rgba(96, 165, 250, 0.2);
}

.billetera-card {
  background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%);
  border-color: #c084fc;
  color: #6b21a8;
}

.billetera-card:hover {
  box-shadow: 0 4px 12px rgba(192, 132, 252, 0.2);
}

@media (max-width: 1024px) {
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }

  .pagos-tabla th,
  .pagos-tabla td {
    padding: 10px 12px;
    font-size: 12px;
  }

  .content-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .stats-bar {
    width: 100%;
    justify-content: flex-start;
  }
}

@media (max-width: 768px) {
  .operaciones-view {
    padding: 0;
  }

  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }

  .breakdown-items {
    grid-template-columns: 1fr;
  }

  .metodo-breakdown-pagadas {
    grid-template-columns: 1fr;
  }

  .filtro-grupo {
    flex-direction: column;
  }

  .filtro-btn {
    width: 100%;
    justify-content: center;
  }

  .tabs-container {
    border-radius: 0;
  }

  .tab-btn {
    font-size: 12px;
    padding: 12px 10px;
  }

  .tab-btn ion-icon {
    display: none;
  }

  .badge-count {
    margin-left: 2px;
  }

  .tab-content {
    border-radius: 0;
    padding: 16px;
  }

  .pagos-tabla {
    font-size: 12px;
  }

  .pagos-tabla th,
  .pagos-tabla td {
    padding: 8px;
  }

  .acciones-cell {
    gap: 4px;
  }

  .btn-action {
    padding: 4px 6px;
    font-size: 16px;
  }

  .modal {
    width: 95%;
    max-width: none;
  }

  .content-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .content-header h2 {
    font-size: 18px;
  }

  .stats-bar {
    width: 100%;
  }

  .modal-footer {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}
</style>
