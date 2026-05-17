<template>
  <div class="cobranza-container">
    <div class="cobranza-header">
      <h2>Gestión de Cobranza</h2>
    </div>

    <!-- ESTADÍSTICAS RÁPIDAS -->
    <div class="stats-container">
      <div class="stat-card">
        <div class="stat-header">
          <div class="stat-icon usuarios">
            <ion-icon name="people-outline"></ion-icon>
          </div>
        </div>
        <div class="stat-content">
          <span class="stat-label">Total Usuarios</span>
          <span class="stat-number">{{ usuarios.length }}</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <div class="stat-icon cuotas">
            <ion-icon name="receipt-outline"></ion-icon>
          </div>
        </div>
        <div class="stat-content">
          <span class="stat-label">Cuotas Pendientes</span>
          <span class="stat-number">{{ totalCuotasPendientes }}</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <div class="stat-icon adeudado">
            <ion-icon name="alert-circle-outline"></ion-icon>
          </div>
        </div>
        <div class="stat-content">
          <span class="stat-label">Total Adeudado</span>
          <span class="stat-number">{{ formatearMoneda(totalAdeudadoGlobal) }}</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <div class="stat-icon pagadas">
            <ion-icon name="checkmark-done-outline"></ion-icon>
          </div>
        </div>
        <div class="stat-content">
          <span class="stat-label">Cuotas Pagadas</span>
          <span class="stat-number">{{ totalCuotasPagadas }}</span>
        </div>
      </div>
    </div>

    <!-- CONTROLES Y FILTROS -->
    <div class="controles-section">
      <div class="buscador-container">
        <ion-icon name="search-outline"></ion-icon>
        <input
          v-model="filtroNombre"
          type="text"
          placeholder="Buscar por nombre, DNI o email..."
          class="buscador"
        >
      </div>

      <div class="filtros-container">
        <!-- Filtro por Estado -->
        <div class="filtro-grupo">
          <button
            @click="filtroEstado = 'activo'"
            :class="['btn-filtro', { active: filtroEstado === 'activo' }]"
          >
            <ion-icon name="checkmark-circle"></ion-icon>
            Activo
          </button>
          <button
            @click="filtroEstado = 'inactivo'"
            :class="['btn-filtro', { active: filtroEstado === 'inactivo' }]"
          >
            <ion-icon name="close-circle"></ion-icon>
            Inactivo
          </button>
        </div>

        <!-- Filtro por Pago -->
        <div class="filtro-grupo">
          <button
            @click="filtroPago = 'al-dia'"
            :class="['btn-filtro', { active: filtroPago === 'al-dia' }]"
          >
            <ion-icon name="checkmark-circle"></ion-icon>
            Al día
          </button>
          <button
            @click="filtroPago = 'atrasado'"
            :class="['btn-filtro', { active: filtroPago === 'atrasado' }]"
          >
            <ion-icon name="alert-circle"></ion-icon>
            Atrasado
          </button>
        </div>

        <button
          @click="limpiarFiltros"
          :disabled="!(filtroNombre || filtroEstado || filtroPago)"
          class="btn-limpiar"
        >
          <ion-icon name="close-outline"></ion-icon>
          Limpiar
        </button>
      </div>
    </div>

    <!-- RESULTADOS -->
    <div class="usuarios-seccion">
      <div class="resultados-info" v-if="usuariosFiltrados.length > 0">
        <span class="resultado-text">{{ usuariosFiltrados.length }} de {{ usuarios.length }} usuarios</span>
      </div>

      <div v-if="usuariosFiltrados.length === 0" class="sin-resultados">
        <ion-icon name="search-outline"></ion-icon>
        <p>No se encontraron usuarios</p>
        <button @click="limpiarFiltros" class="btn-resetear">
          Limpiar filtros
        </button>
      </div>

      <div v-else class="tabla-responsiva">
        <table class="usuarios-tabla">
          <thead>
            <tr>
              <th>Usuario</th>
              <th>DNI</th>
              <th>Estado</th>
              <th>Pendientes</th>
              <th>Adeudado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="usuario in usuariosFiltrados" :key="usuario.id" :class="{ 'fila-atrasado': usuarioTieneAtraso(usuario.id) }">
              <td class="col-usuario">
                <div class="usuario-info">
                  <div class="usuario-avatar">{{ iniciales(usuario.nombre_completo) }}</div>
                  <div class="usuario-nombre">{{ usuario.nombre_completo }}</div>
                </div>
              </td>
              <td class="col-dni">{{ usuario.numero_dni }}</td>
              <td class="col-estado">
                <span :class="['badge', usuario.estado]">
                  {{ usuario.estado }}
                </span>
              </td>
              <td class="col-pendientes">
                <span class="badge-pendientes">{{ obtenerCuotasPendientes(usuario.id).length }}</span>
              </td>
              <td class="col-adeudado">
                <span :class="['monto-adeudado', { 'text-danger': obtenerTotalAdeudado(usuario.id) > 0 }]">
                  {{ formatearMoneda(obtenerTotalAdeudado(usuario.id)) }}
                </span>
              </td>
              <td class="col-acciones">
                <button
                  @click="abrirSidebarCobranza(usuario)"
                  class="btn-gestion"
                  title="Gestionar cobranza"
                >
                  <ion-icon name="cash-outline"></ion-icon>
                  Gestionar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Sidebar Cobranza Usuario -->
    <div v-if="usuarioSeleccionado" class="sidebar-overlay" @click="cerrarSidebar">
      <div class="sidebar-cobranza" @click.stop>

        <!-- ════ PERFIL HERO MODERNO ════ -->
        <div class="perfil-hero">
          <button @click="cerrarSidebar" class="btn-close-hero">
            <ion-icon name="close-outline"></ion-icon>
          </button>

          <div class="perfil-content">
            <!-- Avatar a la izquierda -->
            <div class="perfil-avatar-section">
              <div class="perfil-avatar">
                <span class="avatar-iniciales">{{ iniciales(usuarioSeleccionado.nombre_completo) }}</span>
                <button class="btn-cambiar-foto" title="Cambiar foto">
                  <ion-icon name="camera-outline"></ion-icon>
                </button>
              </div>
            </div>

            <!-- Información a la derecha -->
            <div class="perfil-info-section">
              <div class="perfil-header">
                <div>
                  <h3 class="perfil-nombre">{{ usuarioSeleccionado.nombre_completo }}</h3>
                  <span :class="['perfil-badge', usuarioSeleccionado.estado]">
                    <ion-icon :name="usuarioSeleccionado.estado === 'activo' ? 'checkmark-circle' : 'close-circle'"></ion-icon>
                    {{ usuarioSeleccionado.estado }}
                  </span>
                </div>
              </div>

              <!-- Datos principales -->
              <div class="perfil-detalles">
                <div class="detalle-item">
                  <span class="detalle-label">DNI:</span>
                  <span class="detalle-valor">{{ usuarioSeleccionado.numero_dni }}</span>
                </div>
                <div class="detalle-item" v-if="usuarioSeleccionado.email">
                  <span class="detalle-label">Email:</span>
                  <span class="detalle-valor">{{ usuarioSeleccionado.email }}</span>
                </div>
                <div class="detalle-item" v-if="usuarioSeleccionado.telefono">
                  <span class="detalle-label">Teléfono:</span>
                  <span class="detalle-valor">{{ usuarioSeleccionado.telefono }}</span>
                </div>
                <div class="detalle-item">
                  <span class="detalle-label">Desde:</span>
                  <span class="detalle-valor">{{ formatearFecha(usuarioSeleccionado.created_at) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Stats mejorados -->
          <div class="perfil-stats">
            <div class="stat-box">
              <span class="stat-label">Pendientes</span>
              <span class="stat-valor">{{ cuotasPendientes.length }}</span>
            </div>
            <div class="stat-box warning">
              <span class="stat-label">Adeudado</span>
              <span class="stat-valor">{{ formatearMoneda(totalAdeudado) }}</span>
            </div>
            <div class="stat-box success">
              <span class="stat-label">Pagadas</span>
              <span class="stat-valor">{{ cuotasPagadas.length }}</span>
            </div>
          </div>
        </div>

        <!-- Tabs -->
        <div class="sidebar-tabs">
          <button
            :class="['tab', { active: tabSidebar === 'gestion' }]"
            @click="tabSidebar = 'gestion'"
          >
            <ion-icon name="receipt-outline"></ion-icon>
            Gestión de Pagos
          </button>
          <button
            :class="['tab', { active: tabSidebar === 'historial' }]"
            @click="() => {
              tabSidebar = 'historial'
              if (!yearExpanded.value || typeof yearExpanded.value !== 'object') {
                yearExpanded.value = {}
              }
              const currentYear = new Date().getFullYear().toString()
              if (cuotasPagadas.length > 0 && !yearExpanded.value[currentYear]) {
                yearExpanded.value[currentYear] = true
              }
            }"
          >
            <ion-icon name="time-outline"></ion-icon>
            Historial
          </button>
          <button
            :class="['tab', { active: tabSidebar === 'nueva-cuota' }]"
            @click="abrirNuevaCuota"
          >
            <ion-icon name="add-circle-outline"></ion-icon>
            Agregar Cuota
          </button>
        </div>

        <!-- Contenido Tabs -->
        <div class="sidebar-content">
          <!-- Tab: Gestión de Pagos -->
          <div v-if="tabSidebar === 'gestion'" class="tab-pane">

            <div v-if="cuotasPendientes.length === 0" class="sin-cuotas">
              <ion-icon name="checkmark-circle-outline"></ion-icon>
              <p>Sin cuotas pendientes</p>
              <button class="btn-add-cuota" @click="abrirNuevaCuota">
                <ion-icon name="add-outline"></ion-icon>
                Agregar cuota futura
              </button>
            </div>

            <div v-else class="gestion-grid">

              <!-- Columna 1: Cuotas -->
              <div class="col-cuotas">
                <div class="col-title-row">
                  <div class="col-title">
                    <ion-icon name="list-outline"></ion-icon>
                    Cuotas Pendientes
                    <span class="col-badge">{{ cuotasPendientes.length }}</span>
                  </div>
                  <button class="btn-agregar-rapido" @click="generarProximalCuotaRecurrente" title="Generar próxima cuota recurrente" :disabled="cargandoProxima">
                    <ion-icon :name="cargandoProxima ? 'hourglass' : 'add-circle-outline'"></ion-icon>
                  </button>
                </div>

                <div class="cuotas-header">
                  <label class="checkbox-header">
                    <input
                      type="checkbox"
                      v-model="seleccionarTodas"
                      @change="toggleTodosPagos"
                    >
                    <span>Seleccionar todas</span>
                  </label>
                  <span class="count">{{ cuotasSeleccionadas.length }}/{{ cuotasPendientes.length }}</span>
                </div>

                <div class="cuotas-lista">
                  <div v-for="cuota in cuotasPendientes" :key="cuota.id"
                    class="cuota-item"
                    :class="{ selected: cuotasSeleccionadas.includes(cuota.id) }"
                  >
                    <label class="checkbox-cuota">
                      <input
                        type="checkbox"
                        :value="cuota.id"
                        v-model="cuotasSeleccionadas"
                      >
                      <div class="cuota-info">
                        <div class="cuota-concepto">{{ cuota.concepto }}</div>
                        <div class="cuota-fecha">
                          <ion-icon name="calendar-outline"></ion-icon>
                          Vence: {{ formatearFecha(cuota.fecha_vencimiento) }}
                        </div>
                      </div>
                    </label>
                    <div class="cuota-right">
                      <div class="cuota-monto">{{ formatearMoneda(cuota.monto) }}</div>
                      <button
                        @click="eliminarCuota(cuota.id)"
                        class="btn-eliminar-cuota"
                        title="Eliminar cuota"
                      >
                        <ion-icon name="close-outline"></ion-icon>
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Sub-total cuotas seleccionadas -->
                <div class="subtotal-cuotas">
                  <span>Subtotal ({{ cuotasSeleccionadas.length }} cuota{{ cuotasSeleccionadas.length !== 1 ? 's' : '' }})</span>
                  <span class="subtotal-val">{{ formatearMoneda(totalSeleccionado) }}</span>
                </div>
              </div>

              <!-- Columna 2: Métodos de pago + sumatoria -->
              <div class="col-pago">
                <div class="col-title">
                  <ion-icon name="card-outline"></ion-icon>
                  Método de Pago
                </div>

                <div class="metodos-grid">
                  <button
                    v-for="m in metodos"
                    :key="m.valor"
                    @click="metodoPago = m.valor"
                    :class="['btn-metodo', { active: metodoPago === m.valor }]"
                  >
                    <ion-icon :name="m.icono"></ion-icon>
                    <span>{{ m.label }}</span>
                  </button>
                </div>

                <input
                  v-if="metodoPago !== 'efectivo'"
                  v-model="referenciaPago"
                  type="text"
                  :placeholder="metodoPago === 'transferencia' ? 'N° de transferencia' :
                               metodoPago === 'deposito' ? 'Comprobante / Referencia' :
                               'Referencia de transacción'"
                  class="input-referencia"
                >

                <textarea
                  v-model="observacionesPago"
                  placeholder="Observaciones (opcional)"
                  class="observaciones-input"
                ></textarea>

                <!-- Sumatoria ordenada -->
                <div class="sumatoria-box">
                  <div class="sumatoria-title">Resumen del pago</div>
                  <div class="sumatoria-row" v-for="cuota in cuotasSeleccionadasDetalle" :key="cuota.id">
                    <span class="sm-concepto">{{ cuota.concepto }}</span>
                    <span class="sm-monto">{{ formatearMoneda(cuota.monto) }}</span>
                  </div>
                  <div v-if="cuotasSeleccionadas.length === 0" class="sumatoria-empty">
                    Selecciona cuotas para ver el resumen
                  </div>
                  <div class="sumatoria-total">
                    <span>Total a pagar</span>
                    <span class="total-grande">{{ formatearMoneda(totalSeleccionado) }}</span>
                  </div>
                </div>

                <button
                  @click="registrarPagos"
                  :disabled="cuotasSeleccionadas.length === 0 || cargandoPago"
                  class="btn-pagar"
                >
                  <ion-icon v-if="!cargandoPago" name="checkmark-circle-outline"></ion-icon>
                  <span v-if="cargandoPago">Registrando...</span>
                  <span v-else>Registrar Pago</span>
                </button>
              </div>

            </div>
          </div>

          <!-- Tab: Historial -->
          <div v-if="tabSidebar === 'historial'" class="tab-pane">
            <div v-if="cuotasPagadas.length === 0" class="sin-historial">
              <ion-icon name="document-outline"></ion-icon>
              <p>Sin historial de pagos</p>
            </div>

            <div v-else class="historial-accordion">
              <div v-for="(grupo, year) in pagosPorAño" :key="year" class="year-group">
                <!-- Encabezado del año (accordion) -->
                <button
                  @click="toggleYear(year)"
                  class="year-header"
                  :class="{ expanded: yearExpanded[year] }"
                >
                  <div class="year-title">
                    <ion-icon :name="yearExpanded[year] ? 'chevron-down-outline' : 'chevron-forward-outline'"></ion-icon>
                    <span class="year-label">{{ year }}</span>
                    <span class="year-count">{{ grupo.length }} pago{{ grupo.length !== 1 ? 's' : '' }}</span>
                  </div>
                  <div class="year-total">{{ formatearMoneda(calcularTotalAño(grupo)) }}</div>
                </button>

                <!-- Contenido del año (tabla de pagos) -->
                <transition name="accordion">
                  <div v-show="yearExpanded[year]" class="year-content">
                    <table class="historial-table">
                      <thead>
                        <tr>
                          <th>Item</th>
                          <th>Correspond. a</th>
                          <th>Fecha de Pago</th>
                          <th>Monto</th>
                          <th>Acciones</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="pago in grupo" :key="pago.id" class="pago-row">
                          <td class="pago-concepto">{{ pago.concepto }}</td>
                          <td class="pago-vencimiento">{{ formatearFecha(pago.fecha_vencimiento) }}</td>
                          <td class="pago-fecha">{{ formatearFecha(pago.fecha_pagada) }}</td>
                          <td class="pago-monto">{{ formatearMoneda(pago.monto) }}</td>
                          <td class="pago-acciones">
                            <button @click="verDetallePago(pago)" class="btn-icon-small" title="Ver detalle">
                              <ion-icon name="eye-outline"></ion-icon>
                            </button>
                            <button @click="descargarComprobante(pago.id)" class="btn-icon-small" title="Descargar PDF">
                              <ion-icon name="download-outline"></ion-icon>
                            </button>
                            <button @click="imprimirComprobante(pago.id)" class="btn-icon-small" title="Imprimir">
                              <ion-icon name="print-outline"></ion-icon>
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </transition>
              </div>
            </div>
          </div>
          <!-- Tab: Nueva Cuota Futura -->
          <div v-if="tabSidebar === 'nueva-cuota'" class="tab-pane">
            <div class="nueva-cuota-form">
              <div class="nc-header">
                <ion-icon name="add-circle-outline"></ion-icon>
                <div>
                  <h3>Nueva Cuota Futura</h3>
                  <p>Agrega una cuota manual para este usuario</p>
                </div>
              </div>

              <div class="nc-field">
                <label class="nc-label">
                  <ion-icon name="list-outline"></ion-icon>
                  Concepto de pago
                </label>
                <select v-model="nuevaCuota.concepto_id" class="nc-select">
                  <option value="" disabled>Selecciona un concepto...</option>
                  <option v-for="c in conceptosUsuario" :key="c.id" :value="c.id">
                    {{ c.nombre }} — {{ formatearMoneda(c.monto) }}
                  </option>
                </select>
              </div>

              <div class="nc-form-row">
                <div class="nc-field">
                  <label class="nc-label">
                    <ion-icon name="calendar-outline"></ion-icon>
                    Fecha de vencimiento
                  </label>
                  <input
                    type="date"
                    v-model="nuevaCuota.fecha_vencimiento"
                    class="nc-input"
                    :min="hoyStr"
                  >
                </div>

                <div class="nc-field">
                  <label class="nc-label">
                    <ion-icon name="cash-outline"></ion-icon>
                    Monto
                    <span class="nc-hint">(opcional)</span>
                  </label>
                  <input
                    type="number"
                    v-model="nuevaCuota.monto"
                    class="nc-input"
                    placeholder="Usa el del concepto"
                    min="0"
                    step="0.01"
                  >
                  <p v-if="!nuevaCuota.monto && nuevaCuota.concepto_id" class="nc-info">
                    Usará: {{ formatearMoneda(montoNuevaCuota) }}
                  </p>
                </div>
              </div>

              <div class="nc-field">
                <label class="nc-label">
                  <ion-icon name="document-text-outline"></ion-icon>
                  Descripción
                  <span class="nc-hint">(opcional)</span>
                </label>
                <input
                  type="text"
                  v-model="nuevaCuota.descripcion"
                  class="nc-input"
                  placeholder="Ej: Cuota adelantada junio"
                >
              </div>

              <!-- Preview Mejorado -->
              <div v-if="nuevaCuota.concepto_id && nuevaCuota.fecha_vencimiento" class="nc-preview-card">
                <div class="nc-preview-header">
                  <ion-icon name="checkmark-circle-outline"></ion-icon>
                  <span>Resumen de la cuota</span>
                </div>
                <div class="nc-preview-content">
                  <div class="nc-preview-row">
                    <span class="nc-preview-label">Concepto</span>
                    <span class="nc-preview-value">{{ conceptoSeleccionadoNombre }}</span>
                  </div>
                  <div class="nc-preview-row">
                    <span class="nc-preview-label">Vencimiento</span>
                    <span class="nc-preview-value">{{ formatearFecha(nuevaCuota.fecha_vencimiento) }}</span>
                  </div>
                  <div class="nc-preview-row nc-preview-total">
                    <span class="nc-preview-label">Monto Total</span>
                    <span class="nc-preview-value-total">{{ formatearMoneda(montoNuevaCuota) }}</span>
                  </div>
                </div>
              </div>

              <button
                @click="guardarNuevaCuota"
                :disabled="!nuevaCuota.concepto_id || !nuevaCuota.fecha_vencimiento || guardandoCuota"
                class="nc-btn-guardar"
              >
                <ion-icon :name="guardandoCuota ? 'hourglass' : 'checkmark-circle-outline'"></ion-icon>
                <span>{{ guardandoCuota ? 'Creando...' : 'Crear Cuota' }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Detalle Pago -->
    <div v-if="pagoSeleccionado" class="modal-overlay" @click.self="pagoSeleccionado = null">
      <div class="modal-detalle">
        <div class="modal-header">
          <h3>Detalle del Pago</h3>
          <button @click="pagoSeleccionado = null" class="btn-close">
            <ion-icon name="close-outline"></ion-icon>
          </button>
        </div>
        <div class="modal-body">
          <div class="detalle-item">
            <span class="label">Concepto:</span>
            <span class="valor">{{ pagoSeleccionado.concepto }}</span>
          </div>
          <div class="detalle-item">
            <span class="label">Monto:</span>
            <span class="valor">{{ formatearMoneda(pagoSeleccionado.monto) }}</span>
          </div>
          <div class="detalle-item">
            <span class="label">Fecha de Pago:</span>
            <span class="valor">{{ formatearFecha(pagoSeleccionado.fecha_pagada) }}</span>
          </div>
          <div class="detalle-item">
            <span class="label">Método:</span>
            <span class="valor">{{ pagoSeleccionado.metodo_pago || '-' }}</span>
          </div>
          <div class="detalle-item">
            <span class="label">Referencia:</span>
            <span class="valor">{{ pagoSeleccionado.referencia || '-' }}</span>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="imprimirComprobante(pagoSeleccionado.id)" class="btn-primary">
            <ion-icon name="print-outline"></ion-icon>
            Imprimir
          </button>
          <button @click="descargarComprobante(pagoSeleccionado.id)" class="btn-primary">
            <ion-icon name="download-outline"></ion-icon>
            Descargar PDF
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../services/api'
import { alertStore } from '../../stores/alertStore'

const usuarios = ref([])
const usuarioSeleccionado = ref(null)
const tabSidebar = ref('gestion')
const cuotas = ref([])
const pagoSeleccionado = ref(null)

// Filtros
const filtroNombre = ref('')
const filtroEstado = ref('')
const filtroPago = ref('')

const cuotasSeleccionadas = ref([])
const seleccionarTodas = ref(false)
const metodoPago = ref('efectivo')
const referenciaPago = ref('')
const observacionesPago = ref('')
const cargandoPago = ref(false)
const cargandoProxima = ref(false)

const yearExpanded = ref({})

// Initialize yearExpanded with empty object
const initYearExpanded = () => {
  yearExpanded.value = {}
}

const metodos = [
  { valor: 'efectivo',          label: 'Efectivo',          icono: 'cash-outline' },
  { valor: 'transferencia',     label: 'Transf. / Dep.',    icono: 'swap-horizontal-outline' },
  { valor: 'billetera_digital', label: 'Billetera',         icono: 'phone-portrait-outline' },
]

const iniciales = (nombre = '') =>
  nombre.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase() || 'U'

const cuotasPendientes = computed(() => {
  if (!usuarioSeleccionado.value) return []
  return cuotas.value.filter(c => c.usuario_id === usuarioSeleccionado.value.id && c.estado === 'pendiente')
})

const cuotasPagadas = computed(() => {
  if (!usuarioSeleccionado.value) return []
  return cuotas.value.filter(c => c.usuario_id === usuarioSeleccionado.value.id && c.estado === 'pagada')
})

const totalAdeudado = computed(() => {
  return cuotasPendientes.value.reduce((sum, c) => sum + c.monto, 0)
})

const totalSeleccionado = computed(() => {
  return cuotasPendientes.value
    .filter(c => cuotasSeleccionadas.value.includes(c.id))
    .reduce((sum, c) => sum + c.monto, 0)
})

const cuotasSeleccionadasDetalle = computed(() =>
  cuotasPendientes.value.filter(c => cuotasSeleccionadas.value.includes(c.id))
)

const pagosPorAño = computed(() => {
  const agrupados = {}
  cuotasPagadas.value.forEach(pago => {
    // Agrupar por el año a que corresponde (fecha_vencimiento)
    const año = new Date(pago.fecha_vencimiento).getFullYear()
    if (!agrupados[año]) {
      agrupados[año] = []
    }
    agrupados[año].push(pago)
  })

  // Retornar años en orden descendente y ordenar pagos dentro de cada año por fecha de vencimiento
  return Object.keys(agrupados)
    .sort((a, b) => b - a)
    .reduce((obj, year) => {
      obj[year] = agrupados[year].sort((a, b) =>
        new Date(b.fecha_vencimiento) - new Date(a.fecha_vencimiento)
      )
      return obj
    }, {})
})

// Estadísticas Globales
const totalCuotasPendientes = computed(() => {
  return cuotas.value.filter(c => c.estado === 'pendiente').length
})

const totalCuotasPagadas = computed(() => {
  return cuotas.value.filter(c => c.estado === 'pagada').length
})

const totalAdeudadoGlobal = computed(() => {
  return cuotas.value
    .filter(c => c.estado === 'pendiente')
    .reduce((sum, c) => sum + c.monto, 0)
})

// Funciones para obtener datos de usuarios
const obtenerCuotasPendientes = (usuarioId) => {
  return cuotas.value.filter(c => c.usuario_id === usuarioId && c.estado === 'pendiente')
}

const obtenerTotalAdeudado = (usuarioId) => {
  return obtenerCuotasPendientes(usuarioId).reduce((sum, c) => sum + c.monto, 0)
}

const usuarioTieneAtraso = (usuarioId) => {
  const hoy = new Date()
  return obtenerCuotasPendientes(usuarioId).some(c => new Date(c.fecha_vencimiento) < hoy)
}

// Filtros
const usuariosFiltrados = computed(() => {
  return usuarios.value.filter(usuario => {
    // Filtro por nombre, DNI o email
    const textoBusqueda = filtroNombre.value.toLowerCase()
    const coincideBusqueda = !textoBusqueda ||
      usuario.nombre_completo.toLowerCase().includes(textoBusqueda) ||
      usuario.numero_dni.includes(textoBusqueda) ||
      (usuario.email && usuario.email.toLowerCase().includes(textoBusqueda))

    // Filtro por estado
    const coincideEstado = !filtroEstado.value || usuario.estado === filtroEstado.value

    // Filtro por pago
    let coincidePago = true
    if (filtroPago.value) {
      const tieneAtraso = usuarioTieneAtraso(usuario.id)
      if (filtroPago.value === 'al-dia') {
        coincidePago = !tieneAtraso && obtenerTotalAdeudado(usuario.id) === 0
      } else if (filtroPago.value === 'atrasado') {
        coincidePago = tieneAtraso || obtenerTotalAdeudado(usuario.id) > 0
      }
    }

    return coincideBusqueda && coincideEstado && coincidePago
  })
})

const limpiarFiltros = () => {
  filtroNombre.value = ''
  filtroEstado.value = ''
  filtroPago.value = ''
}

const formatearMoneda = (monto) => {
  return new Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN' }).format(monto)
}

const formatearFecha = (fecha) => {
  if (!fecha) return '-'
  return new Date(fecha).toLocaleDateString('es-PE')
}

const toggleYear = (year) => {
  if (!yearExpanded.value) yearExpanded.value = {}
  yearExpanded.value[year] = !yearExpanded.value[year]
}

const calcularTotalAño = (pagos) => {
  return pagos.reduce((sum, pago) => sum + pago.monto, 0)
}

const eliminarCuota = async (cuotaId) => {
  try {
    await api.delete(`/cobranza/cuotas/${cuotaId}`)
    await cargarCuotas()
    cuotasSeleccionadas.value = cuotasSeleccionadas.value.filter(id => id !== cuotaId)
  } catch (error) {
    console.error('Error eliminando cuota:', error)
  }
}

const cargarUsuarios = async () => {
  try {
    const res = await api.get('/usuarios/', { params: { limit: 100 } })
    // Solo usuarios con rol 'user' o 'usuario'
    usuarios.value = res.data.data.filter(u => u.rol === 'user' || u.rol === 'usuario')
    console.log('Usuarios cargados:', usuarios.value)
  } catch (error) {
    console.error('Error cargando usuarios:', error)
    usuarios.value = []
  }
}

const cargarCuotas = async () => {
  try {
    const res = await api.get('/cobranza/cuotas')
    cuotas.value = res.data.data || []
    console.log('Cuotas cargadas:', cuotas.value)
  } catch (error) {
    console.error('Error cargando cuotas:', error)
    cuotas.value = []
  }
}

const abrirSidebarCobranza = async (usuario) => {
  usuarioSeleccionado.value = usuario
  tabSidebar.value = 'gestion'
  cuotasSeleccionadas.value = []
  seleccionarTodas.value = false
  yearExpanded.value = {}

  // Cargar cuotas específicas de este usuario (esto dispara la generación de cuotas mensuales si faltan)
  try {
    const res = await api.get(`/cobranza/cuotas/${usuario.id}`)
    // Actualizar las cuotas del usuario en la lista local para este usuario
    if (res.data.success) {
      // Reemplazar o actualizar en la lista general de cuotas
      const nuevasCuotas = res.data.data
      const otrasCuotas = cuotas.value.filter(c => c.usuario_id !== usuario.id)
      cuotas.value = [...otrasCuotas, ...nuevasCuotas]
    }
  } catch (error) {
    console.error('Error cargando cuotas del usuario:', error)
  }
}

const cerrarSidebar = () => {
  usuarioSeleccionado.value = null
  cuotasSeleccionadas.value = []
}

const toggleTodosPagos = () => {
  if (seleccionarTodas.value) {
    cuotasSeleccionadas.value = cuotasPendientes.value.map(c => c.id)
  } else {
    cuotasSeleccionadas.value = []
  }
}

const generarProximalCuotaRecurrente = async () => {
  if (!usuarioSeleccionado.value) return

  cargandoProxima.value = true
  try {
    const res = await api.post(`/cobranza/cuotas/${usuarioSeleccionado.value.id}/generar-siguiente`)

    if (res.data.success) {
      // Recargar cuotas
      await cargarCuotas()
      alertStore.success('Éxito', res.data.message)
    }
  } catch (e) {
    console.error('Error generando cuota recurrente:', e)
    const mensaje = e.response?.data?.detail || 'No se pudo generar la próxima cuota'
    alertStore.error('Error', mensaje)
  } finally {
    cargandoProxima.value = false
  }
}

const registrarPagos = async () => {
  if (cuotasSeleccionadas.value.length === 0) return

  cargandoPago.value = true
  try {
    for (const cuotaId of cuotasSeleccionadas.value) {
      const cuota = cuotasPendientes.value.find(c => c.id === cuotaId)
      await api.post('/cobranza/pagos', {
        cuota_id: cuotaId,
        monto: cuota.monto,
        metodo_pago: metodoPago.value,
        referencia: referenciaPago.value,
        observaciones: observacionesPago.value
      })
    }

    await cargarCuotas()
    alertStore.success('Éxito', 'Pagos registrados correctamente')
    cuotasSeleccionadas.value = []
    seleccionarTodas.value = false
    metodoPago.value = 'efectivo'
    referenciaPago.value = ''
    observacionesPago.value = ''
  } catch (error) {
    console.error('Error registrando pagos:', error)
    alertStore.error('Error', 'No se pudieron registrar los pagos')
  } finally {
    cargandoPago.value = false
  }
}

const verDetallePago = (pago) => {
  pagoSeleccionado.value = pago
}

const descargarComprobante = (pagoId) => {
  alertStore.info('Información', 'Descarga PDF en desarrollo')
}

const imprimirComprobante = (pagoId) => {
  alertStore.info('Información', 'Impresión en desarrollo')
}

// ── Nueva Cuota Futura ──────────────────────────────────────────
const conceptosUsuario = ref([])
const guardandoCuota = ref(false)
const nuevaCuota = ref({
  concepto_id: '',
  fecha_vencimiento: '',
  monto: '',
  descripcion: ''
})

const hoyStr = computed(() => new Date().toISOString().split('T')[0])

const montoNuevaCuota = computed(() => {
  if (nuevaCuota.value.monto) return parseFloat(nuevaCuota.value.monto)
  const c = conceptosUsuario.value.find(c => c.id === nuevaCuota.value.concepto_id)
  return c ? c.monto : 0
})

const conceptoSeleccionadoNombre = computed(() => {
  const c = conceptosUsuario.value.find(c => c.id === nuevaCuota.value.concepto_id)
  return c ? c.nombre : ''
})

const cargarConceptosUsuario = async (usuarioId) => {
  try {
    const res = await api.get(`/cobranza/conceptos-usuario/${usuarioId}`)
    let conceptos = res.data.data || []
    
    // Si no hay conceptos asignados aún, cargar todos los conceptos de cuota activos
    if (conceptos.length === 0) {
      const res2 = await api.get('/cobranza/conceptos')
      conceptos = res2.data.data?.filter(c => c.activo) || []
    }
    
    conceptosUsuario.value = conceptos
  } catch (e) {
    console.error('Error cargando conceptos para nueva cuota:', e)
    conceptosUsuario.value = []
  }
}

const abrirNuevaCuota = async () => {
  tabSidebar.value = 'nueva-cuota'
  nuevaCuota.value = { concepto_id: '', fecha_vencimiento: '', monto: '', descripcion: '' }
  if (usuarioSeleccionado.value) {
    await cargarConceptosUsuario(usuarioSeleccionado.value.id)
  }
}

const guardarNuevaCuota = async () => {
  if (!nuevaCuota.value.concepto_id || !nuevaCuota.value.fecha_vencimiento) return
  guardandoCuota.value = true
  try {
    const payload = {
      usuario_id: usuarioSeleccionado.value.id,
      concepto_id: nuevaCuota.value.concepto_id,
      fecha_vencimiento: new Date(nuevaCuota.value.fecha_vencimiento).toISOString(),
      descripcion: nuevaCuota.value.descripcion || null,
      monto: nuevaCuota.value.monto ? parseFloat(nuevaCuota.value.monto) : null
    }
    await api.post('/cobranza/cuotas', payload)
    await cargarCuotas()
    alertStore.success('Éxito', 'Cuota creada correctamente')
    nuevaCuota.value = { concepto_id: '', fecha_vencimiento: '', monto: '', descripcion: '' }
    tabSidebar.value = 'gestion'
  } catch (e) {
    console.error('Error creando cuota:', e)
    alertStore.error('Error', 'No se pudo crear la cuota')
  } finally {
    guardandoCuota.value = false
  }
}

onMounted(() => {
  cargarUsuarios()
  cargarCuotas()
})
</script>

<style scoped>
.cobranza-container {
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ══ ESTADÍSTICAS RÁPIDAS ══ */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 14px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  transition: all 0.2s ease;
  border: 1px solid #e8eef7;
}

.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.stat-header {
  flex-shrink: 0;
}

.stat-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.stat-icon.usuarios {
  background: rgba(79, 70, 229, 0.12);
  color: #4f46e5;
}

.stat-icon.cuotas {
  background: rgba(59, 130, 246, 0.12);
  color: #3b82f6;
}

.stat-icon.adeudado {
  background: rgba(239, 68, 68, 0.12);
  color: #ef4444;
}

.stat-icon.pagadas {
  background: rgba(16, 185, 129, 0.12);
  color: #10b981;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.stat-label {
  font-size: 11px;
  color: #334155;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  line-height: 1.2;
}

.stat-number {
  font-size: 20px;
  font-weight: 800;
  color: #0f172a;
  line-height: 1;
  letter-spacing: -0.5px;
}

/* ══ CONTROLES Y FILTROS ══ */
.controles-section {
  background: white;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.buscador-container {
  flex: 1;
  min-width: 280px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  transition: all 0.2s;
}

.buscador-container:focus-within {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.buscador-container ion-icon {
  color: #cbd5e1;
  font-size: 18px;
  flex-shrink: 0;
}

.buscador {
  flex: 1;
  border: none;
  background: none;
  outline: none;
  font-size: 14px;
  color: #1e293b;
  font-family: inherit;
  min-width: 0;
}

.buscador::placeholder {
  color: #cbd5e1;
}

.filtros-container {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}

.filtro-grupo {
  display: flex;
  gap: 6px;
  align-items: center;
}

.btn-filtro {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #64748b;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
  white-space: nowrap;
}

.btn-filtro:hover {
  border-color: #cbd5e1;
  background: #f8fafc;
  color: #475569;
}

.btn-filtro.active {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  border-color: #4f46e5;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.btn-filtro.active:hover {
  box-shadow: 0 6px 16px rgba(79, 70, 229, 0.4);
}

.btn-filtro ion-icon {
  font-size: 16px;
}

.btn-limpiar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: #fef2f2;
  color: #dc2626;
  border: 1.5px solid #fecaca;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
  white-space: nowrap;
}

.btn-limpiar:hover:not(:disabled) {
  background: #fee2e2;
  border-color: #fca5a5;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
}

.btn-limpiar:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-limpiar ion-icon {
  font-size: 16px;
}

/* ══ RESULTADOS ══ */
.resultados-info {
  padding: 12px 0;
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
}

.sin-resultados {
  background: white;
  border-radius: 12px;
  padding: 60px 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.sin-resultados ion-icon {
  font-size: 48px;
  color: #cbd5e1;
}

.sin-resultados p {
  margin: 0;
  color: #64748b;
  font-size: 16px;
  font-weight: 500;
}

.btn-resetear {
  padding: 10px 16px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 8px;
}

.btn-resetear:hover {
  background: #4338ca;
}

.col-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.btn-agregar-rapido {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 22px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.btn-agregar-rapido:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
}

.btn-agregar-rapido:active {
  transform: scale(0.95);
}

.cobranza-header {
  background: white;
  padding: 0;
  margin-bottom: 20px;
  border-radius: 0;
  border: none;
}

.cobranza-header h2 {
  display: none;
}

.usuarios-seccion {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.tabla-responsiva {
  overflow-x: auto;
}

.usuarios-tabla {
  width: 100%;
  border-collapse: collapse;
}

.usuarios-tabla thead {
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.usuarios-tabla th {
  padding: 14px 20px;
  text-align: left;
  font-weight: 600;
  color: #64748b;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.usuarios-tabla td {
  padding: 14px 20px;
  border-bottom: 1px solid #f1f5f9;
  font-size: 14px;
  color: #1e293b;
}

.usuarios-tabla tbody tr {
  transition: background 0.15s;
}

.usuarios-tabla tbody tr:hover {
  background: #f8fafc;
}

.usuarios-tabla tbody tr.fila-atrasado {
  background: rgba(239, 68, 68, 0.04);
}

.usuarios-tabla tbody tr.fila-atrasado:hover {
  background: rgba(239, 68, 68, 0.08);
}

.usuarios-tabla tbody tr:last-child td {
  border-bottom: none;
}

.col-usuario {
  padding: 16px 20px !important;
}

.usuario-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.usuario-avatar {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  font-weight: 700;
  flex-shrink: 0;
}

.usuario-nombre {
  font-weight: 600;
  color: #1e293b;
  font-size: 14px;
}

.col-dni {
  color: #64748b;
  font-family: 'Courier New', monospace;
  font-size: 13px;
}

.col-estado {
  text-align: center;
}

.col-pendientes {
  text-align: center;
}

.col-adeudado {
  text-align: right;
  font-weight: 600;
}

.col-acciones {
  text-align: center;
}

.badge-pendientes {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: #eef2ff;
  color: #4f46e5;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 700;
}

.monto-adeudado {
  font-weight: 700;
  color: #059669;
}

.monto-adeudado.text-danger {
  color: #dc2626;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
}

.badge.activo {
  background: #ecfdf5;
  color: #059669;
}

.badge.inactivo {
  background: #fef2f2;
  color: #dc2626;
}

.btn-gestion {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-gestion:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.btn-gestion:active {
  transform: translateY(0);
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  font-size: 18px;
  padding: 6px;
  display: flex;
  align-items: center;
  border-radius: 6px;
  transition: all 0.15s;
}

.btn-icon:hover {
  color: #6366f1;
  background: #eef2ff;
}

/* Sidebar */
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15,23,42,0.5);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: flex-end;
  z-index: 999;
}

.sidebar-cobranza {
  background: #f8fafc;
  width: 85%;
  max-width: 980px;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: -8px 0 30px rgba(0,0,0,0.15);
  animation: slideIn 0.25s ease;
}

@keyframes slideIn {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

/* ══ PERFIL HERO MODERNO ══ */
.perfil-hero {
  position: relative;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #334155 100%);
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  flex-shrink: 0;
}

.btn-close-hero {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(255, 255, 255, 0.12);
  border: none;
  border-radius: 8px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  font-size: 20px;
  transition: all 0.2s;
}
.btn-close-hero:hover {
  background: rgba(255, 255, 255, 0.2);
}

.perfil-content {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.perfil-avatar-section {
  flex-shrink: 0;
}

.perfil-avatar {
  width: 120px;
  height: 120px;
  border-radius: 16px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: 3px solid rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.avatar-iniciales {
  font-size: 48px;
  font-weight: 800;
  color: white;
  letter-spacing: 1px;
}

.btn-cambiar-foto {
  position: absolute;
  bottom: -12px;
  right: -12px;
  background: linear-gradient(135deg, #10b981, #059669);
  border: 4px solid #1e293b;
  border-radius: 14px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  font-size: 24px;
  transition: all 0.2s;
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.4);
}

.btn-cambiar-foto:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.5);
}

.btn-cambiar-foto:active {
  transform: scale(0.95);
}

.perfil-info-section {
  flex: 1;
  min-width: 0;
}

.perfil-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.perfil-nombre {
  font-size: 20px;
  font-weight: 800;
  color: white;
  margin: 0 0 6px;
  letter-spacing: -0.3px;
}

.perfil-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: capitalize;
  backdrop-filter: blur(8px);
  width: fit-content;
}
.perfil-badge.activo {
  background: rgba(16, 185, 129, 0.25);
  color: #86efac;
  border: 1px solid rgba(16, 185, 129, 0.3);
}
.perfil-badge.inactivo {
  background: rgba(239, 68, 68, 0.25);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.3);
}
.perfil-badge ion-icon {
  font-size: 13px;
}

.perfil-detalles {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detalle-item {
  display: flex;
  gap: 8px;
  font-size: 12px;
}

.detalle-label {
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
  min-width: 60px;
}

.detalle-valor {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 400;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.perfil-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.stat-box {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
  cursor: default;
}

.stat-box:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.2);
}

.stat-box.warning {
  border-color: rgba(239, 68, 68, 0.2);
}

.stat-box.success {
  border-color: rgba(16, 185, 129, 0.2);
}

.stat-label {
  font-size: 11px;
  color: rgba(97, 97, 97, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.stat-valor {
  font-size: 18px;
  font-weight: 800;
  color: white;
  line-height: 1;
}

.stat-box.warning .stat-valor {
  color: #fca5a5;
}

.stat-box.success .stat-valor {
  color: #86efac;
}


.datos-basicos {
  padding: 16px 20px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  font-size: 14px;
}

.dato-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.dato-item:last-child { margin-bottom: 0; }

.dato-item .label {
  font-weight: 600;
  color: #64748b;
}

.dato-item .valor {
  color: #1e293b;
}

.badge-item {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
}

.badge-item.activo {
  background: #dcfce7;
  color: #166534;
}

.sidebar-tabs {
  display: flex;
  gap: 0;
  border-bottom: 1px solid #e2e8f0;
  background: white;
}

.sidebar-tabs .tab {
  flex: 1;
  padding: 12px 16px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-weight: 500;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 13px;
  font-family: inherit;
  transition: all 0.15s;
  position: relative;
}

.sidebar-tabs .tab:hover { color: #334155; background: #f8fafc; }
.sidebar-tabs .tab.active {
  color: #6366f1;
  font-weight: 600;
}
.sidebar-tabs .tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 20%;
  right: 20%;
  height: 2px;
  border-radius: 1px;
  background: #6366f1;
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.tab-pane { display: flex; flex-direction: column; height: 100%; }

/* ══ GESTION GRID: dos columnas ══ */
.gestion-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  height: 100%;
  align-items: start;
}

.col-cuotas,
.col-pago {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 0;
}

.col-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  color: #64748b;
  letter-spacing: 0.5px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e2e8f0;
}
.col-title ion-icon { font-size: 15px; color: #4f46e5; }

.col-badge {
  margin-left: auto;
  background: #e0e7ff;
  color: #4f46e5;
  font-size: 11px;
  font-weight: 700;
  padding: 1px 7px;
  border-radius: 20px;
}

.cuotas-lista {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: 320px;
  overflow-y: auto;
}

.cuota-item.selected {
  border-color: #4f46e5;
  background: #f0f4ff;
}

.subtotal-cuotas {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 10px;
  background: #f0f4ff;
  border: 1px solid #e0e7ff;
  border-radius: 6px;
  font-size: 12px;
  color: #64748b;
  font-weight: 600;
}
.subtotal-val {
  font-size: 14px;
  font-weight: 700;
  color: #4f46e5;
}

/* Sumatoria box */
.sumatoria-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}
.sumatoria-title {
  padding: 8px 12px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  color: #64748b;
  background: #f1f5f9;
  border-bottom: 1px solid #e2e8f0;
  letter-spacing: 0.5px;
}
.sumatoria-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 12px;
  border-bottom: 1px solid #f1f5f9;
  font-size: 12px;
}
.sm-concepto { color: #475569; flex: 1; }
.sm-monto { font-weight: 600; color: #1e293b; }
.sumatoria-empty {
  padding: 12px;
  font-size: 12px;
  color: #94a3b8;
  text-align: center;
  font-style: italic;
}
.sumatoria-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: #0f172a;
  font-size: 12px;
  font-weight: 700;
  color: rgba(255,255,255,0.85);
}
.total-grande {
  font-size: 16px;
  font-weight: 800;
  color: white;
}


.sin-cuotas,
.sin-historial {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #94a3b8;
  text-align: center;
}

.sin-cuotas ion-icon,
.sin-historial ion-icon {
  font-size: 48px;
  color: #cbd5e1;
  margin-bottom: 12px;
}

.cuotas-resumen {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}

.resumen-card {
  padding: 12px;
  background: #f1f5f9;
  border-radius: 6px;
  text-align: center;
}

.resumen-card.total {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.resumen-label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  opacity: 0.8;
  margin-bottom: 4px;
}

.resumen-valor {
  font-size: 20px;
  font-weight: 700;
}

.cuotas-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e2e8f0;
}

.checkbox-header {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
}

.checkbox-header input {
  cursor: pointer;
}

.count {
  font-size: 12px;
  color: #94a3b8;
}

.cuota-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  margin-bottom: 10px;
  background: white;
  transition: all 0.2s ease;
  gap: 10px;
}

.cuota-item:hover {
  background: #fafbfc;
  border-color: #cbd5e1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.cuota-item.selected {
  background: #f0f4ff;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.checkbox-cuota {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  flex: 1;
  margin: 0;
}

.checkbox-cuota input {
  cursor: pointer;
  margin: 0;
  accent-color: #4f46e5;
}

.cuota-info {
  flex: 1;
}

.cuota-concepto {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
}

.cuota-fecha {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #94a3b8;
}

.cuota-fecha ion-icon {
  font-size: 12px;
}

.cuota-right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.cuota-monto {
  font-size: 14px;
  font-weight: 700;
  color: #4f46e5;
  white-space: nowrap;
  min-width: 90px;
  text-align: right;
}

.btn-eliminar-cuota {
  background: none;
  border: none;
  cursor: pointer;
  color: #cbd5e1;
  font-size: 20px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.btn-eliminar-cuota:hover {
  background: #fee2e2;
  color: #ef4444;
}

.btn-eliminar-cuota:active {
  transform: scale(0.95);
}

.resumen-seleccion {
  background: #f0f4ff;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 16px;
  border: 1px solid #e0e7ff;
}

.total-seleccionado {
  display: flex;
  justify-content: space-between;
  font-weight: 600;
  color: #1e293b;
}

.total-seleccionado .monto {
  color: #4f46e5;
  font-size: 16px;
}

.opciones-pago {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.pago-header {
  margin-bottom: 12px;
}

.pago-header h4 {
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  color: #64748b;
  margin: 0;
}

.metodos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 8px;
  margin-bottom: 12px;
}

.btn-metodo {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 12px 8px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  transition: all 0.2s ease;
}

.btn-metodo:hover {
  border-color: #cbd5e1;
  background: #f8fafc;
}

.btn-metodo.active {
  border-color: #3b82f6;
  background: #dbeafe;
  color: #1e40af;
}

.btn-metodo ion-icon {
  font-size: 24px;
}

.input-referencia {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 13px;
  margin-top: 6px;
  margin-left: 28px;
  background: white;
}

.observaciones-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 13px;
  min-height: 60px;
  resize: vertical;
  margin: 12px 0;
  font-family: inherit;
}

.btn-pagar {
  width: 100%;
  padding: 11px;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-family: inherit;
  font-size: 14px;
  transition: background 0.15s;
  margin-top: 12px;
}

.btn-pagar:hover:not(:disabled) {
  background: #4f46e5;
}


.btn-pagar:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Historial Accordion */
.historial-accordion {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.year-group {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  background: white;
}

.year-header {
  width: 100%;
  padding: 14px 16px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: none;
  border-bottom: 1px solid #e2e8f0;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  transition: all 0.2s ease;
}

.year-header:hover {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
}

.year-header.expanded {
  background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
  border-bottom-color: #d4d8ff;
}

.year-title {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  font-weight: 600;
  color: #1e293b;
}

.year-title ion-icon {
  font-size: 18px;
  color: #4f46e5;
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.year-header.expanded .year-title ion-icon {
  transform: rotate(0deg);
}

.year-label {
  font-size: 15px;
  font-weight: 700;
  color: #1e293b;
}

.year-count {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
  padding: 2px 8px;
  background: rgba(99, 102, 241, 0.1);
  border-radius: 12px;
}

.year-total {
  font-size: 14px;
  font-weight: 700;
  color: #4f46e5;
  white-space: nowrap;
}

.year-content {
  padding: 0;
  background: #fafbfc;
}

/* Historial Table */
.historial-table {
  width: 100%;
  border-collapse: collapse;
}

.historial-table thead {
  background: #f1f5f9;
  border-bottom: 2px solid #e2e8f0;
}

.historial-table th {
  padding: 10px 12px;
  text-align: left;
  font-weight: 600;
  font-size: 12px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.historial-table tbody tr {
  border-bottom: 1px solid #e2e8f0;
  transition: background 0.15s;
}

.historial-table tbody tr:last-child {
  border-bottom: none;
}

.historial-table tbody tr:hover {
  background: #f8fafc;
}

.pago-row td {
  padding: 12px;
  font-size: 13px;
  color: #475569;
}

.pago-concepto {
  font-weight: 600;
  color: #1e293b;
}

.pago-vencimiento {
  color: #64748b;
  font-size: 12px;
}

.pago-fecha {
  color: #64748b;
  font-size: 12px;
}

.pago-monto {
  font-weight: 700;
  color: #4f46e5;
}

.pago-acciones {
  display: flex;
  gap: 6px;
  justify-content: flex-start;
}

.btn-icon-small {
  background: none;
  border: none;
  cursor: pointer;
  color: #64748b;
  font-size: 16px;
  padding: 4px;
  display: flex;
  align-items: center;
  transition: color 0.2s;
}

.btn-icon-small:hover {
  color: #4f46e5;
}

/* Modal Detalle */
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

.modal-detalle {
  background: white;
  border-radius: 12px;
  max-width: 400px;
  width: 100%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 25px rgba(0,0,0,0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  font-size: 16px;
  font-weight: 700;
  margin: 0;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.detalle-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e2e8f0;
}

.detalle-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.detalle-item .label {
  font-weight: 600;
  color: #64748b;
  font-size: 13px;
}

.detalle-item .valor {
  color: #1e293b;
  text-align: right;
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 20px;
  border-top: 1px solid #e2e8f0;
}

.btn-primary {
  flex: 1;
  padding: 10px 16px;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 14px;
  font-family: inherit;
  transition: background 0.15s;
}

.btn-primary:hover {
  background: #4f46e5;
}

/* Accordion transition */
.accordion-enter-active,
.accordion-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.accordion-enter-from {
  opacity: 0;
  max-height: 0;
}

.accordion-leave-to {
  opacity: 0;
  max-height: 0;
}

.accordion-enter-to,
.accordion-leave-from {
  opacity: 1;
  max-height: 1000px;
}

@media (max-width: 768px) {
  .sidebar-cobranza {
    width: 100%;
  }

  .usuarios-tabla th,
  .usuarios-tabla td {
    padding: 8px 12px;
    font-size: 12px;
  }

  .cuotas-resumen {
    grid-template-columns: 1fr;
  }

  .gestion-grid {
    grid-template-columns: 1fr;
  }

  .year-title {
    flex-wrap: wrap;
  }

  .year-total {
    flex-basis: 100%;
  }
}

/* ══ Botón agregar cuota en estado vacío ══ */
.btn-add-cuota {
  margin-top: 12px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 18px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-add-cuota:hover { opacity: 0.9; }
.btn-add-cuota ion-icon { font-size: 16px; }

/* ══ Formulario Nueva Cuota Mejorado ══ */
.nueva-cuota-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.nc-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e0e7ff;
}

.nc-header ion-icon {
  font-size: 24px;
  color: #4f46e5;
  flex-shrink: 0;
  margin-top: 2px;
}

.nc-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
}

.nc-header p {
  margin: 4px 0 0 0;
  font-size: 13px;
  color: #64748b;
  font-weight: 400;
}

.nc-form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.nc-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.nc-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #334155;
  text-transform: capitalize;
  letter-spacing: 0.2px;
}

.nc-label ion-icon {
  font-size: 16px;
  color: #4f46e5;
}

.nc-hint {
  font-size: 11px;
  color: #94a3b8;
  font-weight: 400;
  text-transform: lowercase;
}

.nc-select,
.nc-input {
  padding: 11px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  color: #1e293b;
  background: white;
  transition: all 0.2s ease;
  font-family: inherit;
  width: 100%;
}

.nc-select:hover,
.nc-input:hover {
  border-color: #cbd5e1;
}

.nc-select:focus,
.nc-input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.nc-info {
  margin: 0;
  padding: 6px 10px;
  font-size: 12px;
  color: #4f46e5;
  background: rgba(79, 70, 229, 0.05);
  border-left: 3px solid #4f46e5;
  border-radius: 4px;
}

/* Preview Card Mejorado */
.nc-preview-card {
  background: white;
  border: 1px solid #e0e7ff;
  border-radius: 10px;
  overflow: hidden;
  margin: 8px 0;
}

.nc-preview-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
  background: linear-gradient(135deg, #f0f4ff 0%, #e0e7ff 100%);
  border-bottom: 1px solid #d4d8ff;
  font-size: 12px;
  font-weight: 600;
  color: #4f46e5;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.nc-preview-header ion-icon {
  font-size: 16px;
}

.nc-preview-content {
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.nc-preview-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0;
  font-size: 13px;
}

.nc-preview-label {
  color: #64748b;
  font-weight: 500;
}

.nc-preview-value {
  color: #1e293b;
  font-weight: 600;
  text-align: right;
}

.nc-preview-row.nc-preview-total {
  padding-top: 8px;
  border-top: 1px solid #e0e7ff;
  padding-bottom: 0;
}

.nc-preview-row.nc-preview-total .nc-preview-label {
  font-weight: 700;
  color: #334155;
}

.nc-preview-value-total {
  font-size: 18px;
  font-weight: 800;
  color: #4f46e5;
}

.nc-btn-guardar {
  width: 100%;
  padding: 12px 16px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s ease;
  margin-top: 12px;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}

.nc-btn-guardar:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(79, 70, 229, 0.3);
}

.nc-btn-guardar:active:not(:disabled) {
  transform: translateY(0);
}

.nc-btn-guardar:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.nc-btn-guardar ion-icon {
  font-size: 18px;
}
</style>
