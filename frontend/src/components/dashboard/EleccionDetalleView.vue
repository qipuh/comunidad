<template>
  <div class="detalle-container">
    <!-- Header -->
    <div class="header-detalle">
      <div class="header-left">
        <button class="back-btn" @click="$router.back()">
          <ion-icon name="arrow-back-outline"></ion-icon>
        </button>
        <div>
          <h2>{{ eleccion?.titulo }}</h2>
          <p v-if="eleccion?.descripcion" class="desc">{{ eleccion.descripcion }}</p>
        </div>
      </div>
      <div class="header-right">
        <span :class="['estado-badge', `estado-${eleccion?.estado}`]">
          {{ estadoLabel(eleccion?.estado) }}
        </span>
        <span :class="['tipo-badge', `tipo-${eleccion?.tipo}`]">
          {{ eleccion?.tipo === 'cargo' ? 'Cargo' : 'Acuerdo' }}
        </span>
        <button v-if="isAdmin && eleccion?.estado !== 'cerrado'" class="btn-cambiar-estado" @click="mostrarDialogoCambioEstado = true">
          Siguiente estado
        </button>
      </div>
    </div>

    <!-- Alert -->
    <div v-if="alert.visible" :class="['alert', `alert-${alert.type}`]">
      {{ alert.message }}
      <button class="alert-close" @click="alert.visible = false">×</button>
    </div>

    <!-- Tabs -->
    <div class="tabs-header">
      <button v-for="tab in tabs" :key="tab" :class="['tab-btn', { 'tab-active': tabActivo === tab }]" @click="tabActivo = tab">
        {{ tabLabels[tab] }}
      </button>
    </div>

    <!-- TAB: CANDIDATOS/OPCIONES -->
    <div v-if="tabActivo === 'candidatos'" class="tab-content">
      <div class="panel opciones-panel">
        <div class="panel-header">
          <h3>Opciones / Candidatos</h3>
          <span v-if="eleccion?.estado === 'borrador'" class="hint">(estado: borrador)</span>
        </div>

        <!-- Para tipo cargo: buscar y agregar usuario -->
        <div v-if="eleccion?.tipo === 'cargo'" class="agregar-opcion">
          <div class="busqueda-usuario">
            <input v-model="busquedaUsuario" type="text" placeholder="Buscar usuario..." @input="buscarUsuarios" />
            <div v-if="usuariosSugeridos.length" class="sugerencias">
              <div v-for="u in usuariosSugeridos" :key="u.id" class="sugerencia-item" @click="agregarOpcionDesdeUsuario(u)">
                <div class="usuario-info">
                  <strong>{{ obtenerNombreCompleto(u) }}</strong>
                  <small>{{ u.numero_dni }}</small>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Para tipo acuerdo: input de texto -->
        <div v-if="eleccion?.tipo === 'acuerdo'" v-show="eleccion?.estado === 'borrador'" class="agregar-opcion">
          <div class="form-agregar">
            <input v-model="nuevaOpcion.nombre" type="text" placeholder="Nombre de la opción" />
            <textarea v-model="nuevaOpcion.descripcion" rows="2" placeholder="Descripción (opcional)"></textarea>
            <button class="btn-agregar" @click="agregarOpcion" :disabled="!nuevaOpcion.nombre.trim()">
              <ion-icon name="add-outline"></ion-icon> Agregar opción
            </button>
          </div>
        </div>

        <!-- Lista de opciones -->
        <div class="opciones-lista">
          <div v-for="(op, idx) in eleccion?.opciones" :key="op.id" :class="['opcion-item', { 'con-usuario': op.usuario_id }]">
            <div class="opcion-info">
              <strong>{{ op.nombre }}</strong>
              <small v-if="op.usuario_id" class="usuario-badge">
                <ion-icon name="id-card-outline"></ion-icon> {{ extraerDNI(op.descripcion) }}
              </small>
              <p v-else-if="op.descripcion" class="desc-opcion">{{ op.descripcion }}</p>
            </div>
            <div class="opcion-votos">
              <span class="votos-count">{{ op.votos || 0 }} votos</span>
              <button v-if="eleccion?.estado === 'borrador'" class="btn-eliminar" @click="eliminarOpcion(op.id)" title="Eliminar">
                <ion-icon name="trash-outline"></ion-icon>
              </button>
            </div>
          </div>
          <div v-if="!eleccion?.opciones?.length" class="empty">
            <p>No hay opciones aún</p>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB: PADRÓN -->
    <div v-if="tabActivo === 'padron'" class="tab-content">
      <div class="padron-panel">
        <div class="panel-header">
          <h3>Padrón de Electores</h3>
          <span v-if="eleccion?.estado === 'borrador'" class="hint">(editable)</span>
        </div>

        <div v-if="eleccion?.estado === 'borrador'" class="padron-acciones">
          <div class="busqueda-elector">
            <input v-model="busquedaPadron" type="text" placeholder="Buscar usuario para agregar..." @input="buscarParaPadron" />
            <div v-if="usuariosParaPadron.length" class="sugerencias">
              <div v-for="u in usuariosParaPadron" :key="u.id" class="sugerencia-item" @click="agregarToPadron([u.id])">
                {{ obtenerNombreCompleto(u) }} - {{ u.numero_dni }}
              </div>
            </div>
          </div>
          <button class="btn-importar" @click="importarTodosPadron">
            <ion-icon name="download-outline"></ion-icon> Importar todos los activos
          </button>
        </div>

        <div class="padron-stats">
          <div class="stat">Total: {{ padron.length }}</div>
          <div class="stat votaron">Votaron: {{ padronVotaron }} ({{ padronParticipacion.toFixed(1) }}%)</div>
          <div class="stat no-votaron">No votaron: {{ padron.length - padronVotaron }}</div>
        </div>

        <table class="padron-tabla">
          <thead>
            <tr>
              <th>Nombre Completo</th>
              <th>DNI</th>
              <th>Estado</th>
              <th v-if="eleccion?.estado === 'borrador'">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in padron" :key="p.id" :class="{ 'fila-voto': p.votó }">
              <td>{{ p.nombres }} {{ p.apellido_paterno }} {{ p.apellido_materno }}</td>
              <td>{{ p.numero_dni }}</td>
              <td>
                <span v-if="p.votó" class="chip votó">✓ Votó</span>
                <span v-else class="chip pendiente">⊘ Pendiente</span>
              </td>
              <td v-if="eleccion?.estado === 'borrador'">
                <button class="btn-eliminar-sm" @click="removerDelPadron(p.usuario_id)">
                  <ion-icon name="trash-outline"></ion-icon>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- TAB: RESULTADOS -->
    <div v-if="tabActivo === 'resultados'" class="tab-content">
      <div class="resultados-panel">
        <div class="panel-header">
          <h3>Resultados</h3>
        </div>

        <!-- Stats Cards -->
        <div class="stats-grid">
          <div class="stat-card">
            <span class="stat-label">Padrón Total</span>
            <span class="stat-value">{{ resultados.total_padron || 0 }}</span>
          </div>
          <div class="stat-card">
            <span class="stat-label">Votaron</span>
            <span class="stat-value verde">{{ resultados.total_votaron || 0 }}</span>
          </div>
          <div class="stat-card">
            <span class="stat-label">No Votaron</span>
            <span class="stat-value gris">{{ resultados.total_no_votaron || 0 }}</span>
          </div>
          <div class="stat-card">
            <span class="stat-label">% Participación</span>
            <span class="stat-value">{{ resultados.participacion_pct || 0 }}%</span>
          </div>
        </div>

        <!-- Gráficos -->
        <div class="graficos-container">
          <div class="grafico-dona">
            <h4>Participación</h4>
            <canvas ref="canvasDona" width="300" height="300"></canvas>
          </div>
          <div class="grafico-barras">
            <h4>Votos por Opción</h4>
            <canvas ref="canvasBarras" width="400" height="300"></canvas>
          </div>
        </div>

        <!-- Tabla de resultados -->
        <div class="resultados-tabla-wrapper">
          <table class="resultados-tabla">
            <thead>
              <tr>
                <th>#</th>
                <th>Opción</th>
                <th>Votos</th>
                <th>%</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(op, idx) in resultados.opciones" :key="op.id">
                <td>{{ idx + 1 }}</td>
                <td>{{ op.nombre }}</td>
                <td>{{ op.votos }}</td>
                <td>{{ op.porcentaje }}%</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Nota de impugnados -->
        <div v-if="resultados.total_impugnados > 0" class="nota-impugnados">
          <ion-icon name="warning-outline"></ion-icon>
          {{ resultados.total_impugnados }} voto(s) impugnado(s)
        </div>

        <!-- Botones de exportación -->
        <div class="exportacion-botones">
          <button class="btn-exportar excel" @click="exportarExcel">
            <ion-icon name="document-outline"></ion-icon> Exportar Excel
          </button>
          <button class="btn-exportar pdf" @click="exportarPDF">
            <ion-icon name="download-outline"></ion-icon> Exportar PDF
          </button>
        </div>
      </div>
    </div>

    <!-- TAB: VOTOS -->
    <div v-if="tabActivo === 'votos'" class="tab-content">
      <div v-if="!isAdmin" class="alert alert-info">
        Solo administradores pueden ver los votos individuales
      </div>
      <div v-else class="votos-panel">
        <div class="panel-header">
          <h3>Listado de Votos</h3>
        </div>

        <table class="votos-tabla">
          <thead>
            <tr>
              <th>#</th>
              <th>Elector (DNI)</th>
              <th>Opción Votada</th>
              <th>Método</th>
              <th>Fecha</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(v, idx) in votos" :key="v.id" :class="{ 'fila-impugnada': v.impugnado }">
              <td>{{ idx + 1 }}</td>
              <td>{{ v.nombres }} {{ v.apellido_paterno }} ({{ v.numero_dni }})</td>
              <td>{{ v.opcion_nombre }}</td>
              <td><span class="chip">{{ v.metodo_validacion }}</span></td>
              <td>{{ formatFecha(v.created_at) }}</td>
              <td>
                <span v-if="v.impugnado" class="chip impugnado" :title="v.motivo_impugnacion">
                  ⚠ Impugnado
                </span>
                <span v-else class="chip valido">✓ Válido</span>
              </td>
              <td>
                <button v-if="!v.impugnado" class="btn-accion" @click="abrirModalImpugnar(v)">
                  <ion-icon name="flag-outline"></ion-icon> Impugnar
                </button>
                <button v-else class="btn-accion danger" @click="desimpugnarVoto(v.id)">
                  <ion-icon name="close-outline"></ion-icon> Quitar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODALES -->
    <!-- Modal: Cambiar estado -->
    <div v-if="mostrarDialogoCambioEstado" class="modal-overlay" @click.self="mostrarDialogoCambioEstado = false">
      <div class="modal-content">
        <h3>Cambiar estado a {{ siguienteEstado(eleccion?.estado) }}</h3>
        <p v-if="siguienteEstado(eleccion?.estado) === 'Activo'">
          ¿Activar la elección? Se creará automáticamente una opción "VOTO EN BLANCO".
        </p>
        <p v-else>¿Cerrar la elección? Los resultados quedarán finales.</p>
        <div class="modal-botones">
          <button class="btn-cancelar" @click="mostrarDialogoCambioEstado = false">Cancelar</button>
          <button class="btn-confirmar" @click="cambiarEstado">Confirmar</button>
        </div>
      </div>
    </div>

    <!-- Modal: Impugnar voto -->
    <div v-if="votoEnModalImpugnar" class="modal-overlay" @click.self="votoEnModalImpugnar = null">
      <div class="modal-content">
        <h3>Impugnar Voto</h3>
        <p>Elector: {{ votoEnModalImpugnar.nombres }} {{ votoEnModalImpugnar.apellido_paterno }}</p>
        <p>Opción: {{ votoEnModalImpugnar.opcion_nombre }}</p>
        <textarea v-model="motivoImpugnacion" placeholder="Motivo de la impugnación..." rows="3"></textarea>
        <div class="modal-botones">
          <button class="btn-cancelar" @click="votoEnModalImpugnar = null">Cancelar</button>
          <button class="btn-confirmar" @click="confirmarImpugnar">Impugnar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import eleccionesService from '@/services/elecciones.service'
import { usuariosService } from '@/services/usuarios.service'
import { Chart, ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js'
import * as XLSX from 'xlsx'

Chart.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend)

const route = useRoute()
const eleccionId = route.params.id

const eleccion = ref(null)
const resultados = ref({})
const padron = ref([])
const votos = ref([])
const tabActivo = ref('candidatos')
const alert = ref({ visible: false, type: '', message: '' })
const isAdmin = ref(false)

const busquedaUsuario = ref('')
const usuariosSugeridos = ref([])
const busquedaPadron = ref('')
const usuariosParaPadron = ref([])
const nuevaOpcion = ref({ nombre: '', descripcion: '' })
const mostrarDialogoCambioEstado = ref(false)
const votoEnModalImpugnar = ref(null)
const motivoImpugnacion = ref('')

const canvasDona = ref(null)
const canvasBarras = ref(null)
let chartDona = null
let chartBarras = null

const tabs = ['candidatos', 'padron', 'resultados', 'votos']
const tabLabels = {
  candidatos: '📋 Candidatos',
  padron: '👥 Padrón',
  resultados: '📊 Resultados',
  votos: '🗳️ Votos'
}

const padronVotaron = computed(() => padron.value.filter(p => p.votó).length)
const padronParticipacion = computed(() => (padronVotaron.value / padron.value.length * 100) || 0)

const obtenerNombreCompleto = (usuario) => {
  const partes = [usuario.nombres, usuario.apellido_paterno, usuario.apellido_materno].filter(p => p && p.trim())
  return partes.join(' ') || 'Sin nombre'
}

const extraerDNI = (descripcion) => {
  if (!descripcion) return ''
  if (descripcion.includes('@')) return descripcion.split('@')[0]
  return descripcion
}

const estadoLabel = (estado) => {
  const labels = { borrador: 'Borrador', activo: 'Activa', cerrado: 'Cerrada' }
  return labels[estado] || estado
}

const siguienteEstado = (estado) => {
  if (estado === 'borrador') return 'Activo'
  if (estado === 'activo') return 'Cerrado'
  return 'Finalizado'
}

const formatFecha = (fecha) => {
  if (!fecha) return ''
  const d = new Date(fecha)
  return d.toLocaleDateString('es-ES') + ' ' + d.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
}

async function cargarDetalle() {
  try {
    eleccion.value = await eleccionesService.obtenerEleccion(eleccionId)
    await Promise.all([cargarResultados(), cargarPadron(), cargarVotos()])
  } catch (err) {
    console.error('Error cargando elección:', err)
    alert.value = { visible: true, type: 'error', message: 'Error cargando elección' }
  }
}

async function cargarResultados() {
  try {
    resultados.value = await eleccionesService.obtenerResultados(eleccionId)
    await nextTick()
    dibujarGraficos()
  } catch (err) {
    console.error('Error cargando resultados:', err)
  }
}

async function cargarPadron() {
  try {
    const resp = await eleccionesService.obtenerPadron(eleccionId)
    padron.value = resp.data || []
  } catch (err) {
    console.error('Error cargando padrón:', err)
  }
}

async function cargarVotos() {
  try {
    const resp = await eleccionesService.obtenerVotos(eleccionId)
    votos.value = resp.data || []
  } catch (err) {
    console.error('Error cargando votos:', err)
  }
}

function dibujarGraficos() {
  if (!canvasDona.value || !canvasBarras.value) return

  // Destruir gráficos anteriores
  if (chartDona) chartDona.destroy()
  if (chartBarras) chartBarras.destroy()

  // Gráfico Dona
  const ctxDona = canvasDona.value.getContext('2d')
  chartDona = new Chart(ctxDona, {
    type: 'doughnut',
    data: {
      labels: ['Votaron', 'No votaron'],
      datasets: [{
        data: [resultados.value.total_votaron || 0, resultados.value.total_no_votaron || 0],
        backgroundColor: ['#16a34a', '#e5e7eb'],
        borderColor: ['#15803d', '#d1d5db']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  })

  // Gráfico Barras
  const ctxBarras = canvasBarras.value.getContext('2d')
  chartBarras = new Chart(ctxBarras, {
    type: 'bar',
    data: {
      labels: (resultados.value.opciones || []).map(o => o.nombre),
      datasets: [{
        label: 'Votos',
        data: (resultados.value.opciones || []).map(o => o.votos),
        backgroundColor: '#4f46e5',
        borderColor: '#4338ca'
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: false }
      }
    }
  })
}

async function buscarUsuarios() {
  if (!busquedaUsuario.value.trim()) {
    usuariosSugeridos.value = []
    return
  }
  try {
    const resp = await usuariosService.buscarPorNombre(busquedaUsuario.value)
    const usuarios = resp.data || []
    const usuarioIds = new Set(eleccion.value?.opciones?.map(o => o.usuario_id) || [])
    usuariosSugeridos.value = usuarios.filter(u => !usuarioIds.has(u.id))
  } catch (err) {
    console.error('Error buscando usuarios:', err)
  }
}

async function buscarParaPadron() {
  if (!busquedaPadron.value.trim()) {
    usuariosParaPadron.value = []
    return
  }
  try {
    const resp = await usuariosService.buscarPorNombre(busquedaPadron.value)
    const usuarios = resp.data || []
    const padronIds = new Set(padron.value.map(p => p.usuario_id))
    usuariosParaPadron.value = usuarios.filter(u => !padronIds.has(u.id))
  } catch (err) {
    console.error('Error buscando para padrón:', err)
  }
}

async function agregarOpcionDesdeUsuario(usuario) {
  const opcion = {
    nombre: obtenerNombreCompleto(usuario),
    descripcion: usuario.numero_dni,
    usuario_id: usuario.id,
    orden: (eleccion.value?.opciones?.length || 0) + 1
  }
  try {
    await eleccionesService.agregarOpcion(eleccionId, opcion)
    busquedaUsuario.value = ''
    usuariosSugeridos.value = []
    alert.value = { visible: true, type: 'success', message: 'Candidato agregado' }
    await cargarDetalle()
  } catch (err) {
    alert.value = { visible: true, type: 'error', message: 'Error agregando candidato' }
  }
}

async function agregarOpcion() {
  if (!nuevaOpcion.value.nombre.trim()) return
  try {
    await eleccionesService.agregarOpcion(eleccionId, {
      nombre: nuevaOpcion.value.nombre,
      descripcion: nuevaOpcion.value.descripcion,
      orden: (eleccion.value?.opciones?.length || 0) + 1
    })
    nuevaOpcion.value = { nombre: '', descripcion: '' }
    alert.value = { visible: true, type: 'success', message: 'Opción agregada' }
    await cargarDetalle()
  } catch (err) {
    alert.value = { visible: true, type: 'error', message: 'Error agregando opción' }
  }
}

async function eliminarOpcion(opcionId) {
  if (!confirm('¿Eliminar opción?')) return
  try {
    await eleccionesService.eliminarOpcion(eleccionId, opcionId)
    alert.value = { visible: true, type: 'success', message: 'Opción eliminada' }
    await cargarDetalle()
  } catch (err) {
    alert.value = { visible: true, type: 'error', message: 'Error eliminando opción' }
  }
}

async function agregarToPadron(usuariosIds) {
  try {
    await eleccionesService.agregarAlPadron(eleccionId, usuariosIds)
    busquedaPadron.value = ''
    usuariosParaPadron.value = []
    alert.value = { visible: true, type: 'success', message: 'Usuario(s) agregado(s)' }
    await cargarPadron()
  } catch (err) {
    alert.value = { visible: true, type: 'error', message: 'Error agregando usuario' }
  }
}

async function importarTodosPadron() {
  try {
    await eleccionesService.importarTodosPadron(eleccionId)
    alert.value = { visible: true, type: 'success', message: 'Padrón importado' }
    await cargarPadron()
  } catch (err) {
    alert.value = { visible: true, type: 'error', message: 'Error importando padrón' }
  }
}

async function removerDelPadron(usuarioId) {
  if (!confirm('¿Remover elector del padrón?')) return
  try {
    await eleccionesService.removerDelPadron(eleccionId, usuarioId)
    alert.value = { visible: true, type: 'success', message: 'Elector removido' }
    await cargarPadron()
  } catch (err) {
    alert.value = { visible: true, type: 'error', message: 'Error removiendo elector' }
  }
}

function abrirModalImpugnar(voto) {
  votoEnModalImpugnar.value = voto
  motivoImpugnacion.value = ''
}

async function confirmarImpugnar() {
  if (!motivoImpugnacion.value.trim()) {
    alert.value = { visible: true, type: 'error', message: 'Ingresa un motivo' }
    return
  }
  try {
    await eleccionesService.impugnarVoto(eleccionId, votoEnModalImpugnar.value.id, true, motivoImpugnacion.value)
    votoEnModalImpugnar.value = null
    motivoImpugnacion.value = ''
    alert.value = { visible: true, type: 'success', message: 'Voto impugnado' }
    await cargarVotos()
    await cargarResultados()
  } catch (err) {
    alert.value = { visible: true, type: 'error', message: 'Error impugnando voto' }
  }
}

async function desimpugnarVoto(votoId) {
  try {
    await eleccionesService.impugnarVoto(eleccionId, votoId, false)
    alert.value = { visible: true, type: 'success', message: 'Impugnación removida' }
    await cargarVotos()
    await cargarResultados()
  } catch (err) {
    alert.value = { visible: true, type: 'error', message: 'Error desimpugnando voto' }
  }
}

async function cambiarEstado() {
  const nuevoEstado = siguienteEstado(eleccion.value.estado).toLowerCase()
  try {
    await eleccionesService.cambiarEstado(eleccionId, nuevoEstado)
    mostrarDialogoCambioEstado.value = false
    alert.value = { visible: true, type: 'success', message: `Estado cambiado a ${nuevoEstado}` }
    await cargarDetalle()
  } catch (err) {
    alert.value = { visible: true, type: 'error', message: 'Error cambiando estado' }
  }
}

function exportarExcel() {
  try {
    const wb = XLSX.utils.book_new()

    // Hoja 1: Padrón
    const padronData = padron.value.map(p => ({
      'Nombre': obtenerNombreCompleto(p.usuario),
      'DNI': p.usuario?.numero_dni || '',
      'Estado': p.votó ? 'Votó' : 'Pendiente',
      'Fecha Voto': p.votó ? formatFecha(p.fecha_voto) : ''
    }))
    const ws1 = XLSX.utils.json_to_sheet(padronData)
    XLSX.utils.book_append_sheet(wb, ws1, 'Padrón')

    // Hoja 2: Resultados
    const resultadosData = (resultados.value.opciones || []).map((op, idx) => ({
      'Posición': idx + 1,
      'Opción': op.nombre,
      'Votos': op.votos,
      'Porcentaje': op.porcentaje + '%'
    }))
    const ws2 = XLSX.utils.json_to_sheet(resultadosData)
    XLSX.utils.book_append_sheet(wb, ws2, 'Resultados')

    // Hoja 3: Resumen
    const resumenData = [{
      'Métrica': 'Padrón Total',
      'Valor': resultados.value.total_padron
    }, {
      'Métrica': 'Votaron',
      'Valor': resultados.value.total_votaron
    }, {
      'Métrica': 'No Votaron',
      'Valor': resultados.value.total_no_votaron
    }, {
      'Métrica': 'Participación',
      'Valor': resultados.value.participacion_pct + '%'
    }, {
      'Métrica': 'Votos Impugnados',
      'Valor': resultados.value.total_impugnados
    }]
    const ws3 = XLSX.utils.json_to_sheet(resumenData)
    XLSX.utils.book_append_sheet(wb, ws3, 'Resumen')

    const fecha = new Date().toISOString().split('T')[0]
    XLSX.writeFile(wb, `${eleccion.value?.titulo || 'eleccion'}_${fecha}.xlsx`)
    alert.value = { visible: true, type: 'success', message: 'Excel exportado correctamente' }
  } catch (err) {
    console.error('Error exportando Excel:', err)
    alert.value = { visible: true, type: 'error', message: 'Error al exportar Excel' }
  }
}

async function exportarPDF() {
  try {
    const html2canvas = (await import('html2canvas')).default
    const jsPDF = (await import('jspdf')).jsPDF

    const element = document.querySelector('.resultados-panel')
    if (!element) {
      alert.value = { visible: true, type: 'error', message: 'No se pudo encontrar la sección de resultados' }
      return
    }

    const canvas = await html2canvas(element, {
      scale: 2,
      logging: false,
      useCORS: true
    })

    const imgData = canvas.toDataURL('image/png')
    const pdf = new jsPDF({
      orientation: canvas.width > canvas.height ? 'landscape' : 'portrait',
      unit: 'mm',
      format: 'a4'
    })

    const pdfWidth = pdf.internal.pageSize.getWidth()
    const pdfHeight = pdf.internal.pageSize.getHeight()
    const imgWidth = canvas.width
    const imgHeight = canvas.height
    const ratio = Math.min(pdfWidth / imgWidth * 25.4, pdfHeight / imgHeight * 25.4)

    const finalWidth = imgWidth * ratio / 25.4
    const finalHeight = imgHeight * ratio / 25.4
    const x = (pdfWidth - finalWidth) / 2
    const y = (pdfHeight - finalHeight) / 2

    pdf.addImage(imgData, 'PNG', x, y, finalWidth, finalHeight)
    const fecha = new Date().toISOString().split('T')[0]
    pdf.save(`${eleccion.value?.titulo || 'eleccion'}_${fecha}.pdf`)
    alert.value = { visible: true, type: 'success', message: 'PDF exportado correctamente' }
  } catch (err) {
    console.error('Error exportando PDF:', err)
    alert.value = { visible: true, type: 'error', message: 'Error al exportar PDF' }
  }
}

onMounted(() => {
  cargarDetalle()
  isAdmin.value = localStorage.getItem('user_rol') === 'admin'
})
</script>

<style scoped>
.detalle-container {
  padding: 24px;
  background: white;
  border-radius: 12px;
  max-width: 1400px;
  margin: 0 auto;
}

.header-detalle {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  gap: 16px;
}

.header-left {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  flex: 1;
}

.back-btn {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: white;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #16a34a;
  color: white;
  border-color: #16a34a;
}

.header-left h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

.header-left .desc {
  margin: 4px 0 0;
  font-size: 13px;
  color: #64748b;
}

.header-right {
  display: flex;
  gap: 8px;
  align-items: center;
}

.estado-badge,
.tipo-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.estado-borrador {
  background: #f3f4f6;
  color: #6b7280;
}

.estado-activo {
  background: #dcfce7;
  color: #166534;
}

.estado-cerrado {
  background: #fee2e2;
  color: #991b1b;
}

.tipo-cargo {
  background: #dbeafe;
  color: #1e40af;
}

.tipo-acuerdo {
  background: #fef3c7;
  color: #92400e;
}

.btn-cambiar-estado {
  padding: 6px 12px;
  border: none;
  background: #4f46e5;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: background 0.2s;
}

.btn-cambiar-estado:hover {
  background: #4338ca;
}

.alert {
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  animation: slideIn 0.3s ease;
}

.alert-success {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.alert-error {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.alert-info {
  background: #dbeafe;
  color: #1e40af;
  border: 1px solid #bfdbfe;
}

.alert-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: inherit;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.alert-close:hover {
  opacity: 1;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* TABS */
.tabs-header {
  display: flex;
  gap: 8px;
  border-bottom: 2px solid #e2e8f0;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 12px 16px;
  border: none;
  background: none;
  color: #64748b;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
}

.tab-btn:hover {
  color: #4f46e5;
}

.tab-btn.tab-active {
  color: #4f46e5;
  border-bottom-color: #4f46e5;
}

.tab-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* PANELES */
.panel {
  background: white;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.panel-header h3 {
  margin: 0;
  font-size: 18px;
  color: #1e293b;
}

.hint {
  font-size: 12px;
  color: #94a3b8;
  font-weight: normal;
}

/* CANDIDATOS */
.agregar-opcion {
  margin-bottom: 24px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
}

.busqueda-usuario {
  position: relative;
  margin-bottom: 12px;
}

.busqueda-usuario input,
.form-agregar input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
}

.sugerencias {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
  margin-top: 4px;
}

.sugerencia-item {
  padding: 10px 12px;
  cursor: pointer;
  border-bottom: 1px solid #f1f5f9;
  transition: background 0.2s;
}

.sugerencia-item:hover {
  background: #f8fafc;
}

.usuario-info strong {
  display: block;
  font-size: 14px;
  color: #1e293b;
}

.usuario-info small {
  display: block;
  font-size: 12px;
  color: #94a3b8;
  margin-top: 2px;
}

.form-agregar {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-agregar input,
.form-agregar textarea {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
}

.btn-agregar {
  padding: 8px 16px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: background 0.2s;
}

.btn-agregar:hover:not(:disabled) {
  background: #4338ca;
}

.btn-agregar:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.opciones-lista {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.opcion-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f8fafc;
  border-radius: 6px;
  border-left: 3px solid #e2e8f0;
  transition: all 0.2s;
}

.opcion-item.con-usuario {
  border-left-color: #16a34a;
  background: #f0fdf4;
}

.opcion-info strong {
  display: block;
  color: #1e293b;
  margin-bottom: 4px;
}

.usuario-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #16a34a;
}

.desc-opcion {
  font-size: 13px;
  color: #64748b;
  margin: 4px 0 0;
}

.opcion-votos {
  display: flex;
  align-items: center;
  gap: 12px;
}

.votos-count {
  font-weight: 600;
  color: #1e293b;
}

.btn-eliminar,
.btn-eliminar-sm {
  width: 32px;
  height: 32px;
  border: none;
  background: #fee2e2;
  color: #991b1b;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-eliminar:hover,
.btn-eliminar-sm:hover {
  background: #fecaca;
}

.empty {
  padding: 24px;
  text-align: center;
  color: #94a3b8;
}

/* PADRÓN */
.padron-acciones {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.busqueda-elector {
  flex: 1;
  position: relative;
  min-width: 250px;
}

.busqueda-elector input {
  width: 100%;
}

.btn-importar {
  padding: 8px 16px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
}

.btn-importar:hover {
  background: #4338ca;
}

.padron-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.stat {
  padding: 8px 16px;
  background: #f1f5f9;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
}

.stat.votaron {
  background: #dcfce7;
  color: #166534;
}

.stat.no-votaron {
  background: #fee2e2;
  color: #991b1b;
}

.padron-tabla,
.votos-tabla,
.resultados-tabla {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  margin-top: 16px;
}

.padron-tabla thead,
.votos-tabla thead,
.resultados-tabla thead {
  background: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
}

.padron-tabla th,
.votos-tabla th,
.resultados-tabla th {
  padding: 10px;
  text-align: left;
  font-weight: 600;
  color: #475569;
}

.padron-tabla td,
.votos-tabla td,
.resultados-tabla td {
  padding: 10px;
  border-bottom: 1px solid #f1f5f9;
}

.padron-tabla tbody tr:hover,
.votos-tabla tbody tr:hover,
.resultados-tabla tbody tr:hover {
  background: #f8fafc;
}

.fila-voto {
  background: #f0fdf4;
}

.fila-impugnada {
  background: #fef3c7;
  opacity: 0.8;
  text-decoration: line-through;
}

.chip {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}

.chip.votó {
  background: #dcfce7;
  color: #166534;
}

.chip.pendiente {
  background: #fee2e2;
  color: #991b1b;
}

.chip.valido {
  background: #dcfce7;
  color: #166534;
}

.chip.impugnado {
  background: #fef3c7;
  color: #92400e;
}

/* RESULTADOS */
.resultados-panel {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.stat-card {
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
  border-left: 3px solid #4f46e5;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-label {
  font-size: 12px;
  color: #64748b;
  font-weight: 600;
  text-transform: uppercase;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
}

.stat-value.verde {
  color: #16a34a;
}

.stat-value.gris {
  color: #94a3b8;
}

.graficos-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

@media (max-width: 1024px) {
  .graficos-container {
    grid-template-columns: 1fr;
  }
}

.grafico-dona,
.grafico-barras {
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
}

.grafico-dona h4,
.grafico-barras h4 {
  margin: 0 0 12px;
  font-size: 14px;
  color: #1e293b;
}

.resultados-tabla-wrapper {
  margin-top: 16px;
}

.nota-impugnados {
  padding: 12px 16px;
  background: #fef3c7;
  border: 1px solid #fcd34d;
  border-radius: 6px;
  color: #92400e;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.exportacion-botones {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.btn-exportar {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.btn-exportar.excel {
  background: #dcfce7;
  color: #166534;
}

.btn-exportar.excel:hover {
  background: #bbf7d0;
}

.btn-exportar.pdf {
  background: #fee2e2;
  color: #991b1b;
}

.btn-exportar.pdf:hover {
  background: #fecaca;
}

/* VOTOS */
.votos-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.btn-accion {
  padding: 4px 8px;
  border: none;
  background: #dcfce7;
  color: #166534;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s;
}

.btn-accion:hover {
  background: #bbf7d0;
}

.btn-accion.danger {
  background: #fee2e2;
  color: #991b1b;
}

.btn-accion.danger:hover {
  background: #fecaca;
}

/* MODALES */
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
  z-index: 100;
  animation: fadeIn 0.2s ease;
}

.modal-content {
  background: white;
  padding: 24px;
  border-radius: 12px;
  max-width: 400px;
  width: 90%;
  animation: slideIn 0.2s ease;
}

.modal-content h3 {
  margin: 0 0 12px;
  font-size: 18px;
  color: #1e293b;
}

.modal-content p {
  margin: 0 0 12px;
  font-size: 14px;
  color: #64748b;
}

.modal-content textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
}

.modal-botones {
  display: flex;
  gap: 12px;
  margin-top: 16px;
  justify-content: flex-end;
}

.btn-cancelar {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  background: white;
  color: #64748b;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-cancelar:hover {
  background: #f1f5f9;
}

.btn-confirmar {
  padding: 8px 16px;
  border: none;
  background: #4f46e5;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s;
}

.btn-confirmar:hover {
  background: #4338ca;
}
</style>
