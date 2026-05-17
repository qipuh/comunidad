<template>
  <div class="dash-home">

    <!-- Loading State -->
    <div v-if="cargando" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Cargando estadísticas...</p>
    </div>

    <template v-else>

    <!-- KPI Row -->
    <section class="kpi-row">
      <div class="kpi-card">
        <div class="kpi-icon kpi-blue">
          <ion-icon name="people-outline"></ion-icon>
        </div>
        <div class="kpi-body">
          <span class="kpi-label">Usuarios Totales</span>
          <span class="kpi-value">{{ stats.usuarios_totales }}</span>
          <span class="kpi-meta">
            <span class="kpi-chip" :class="stats.pct_crecimiento_usuarios >= 0 ? 'positive' : 'negative'">
              {{ stats.pct_crecimiento_usuarios >= 0 ? '+' : '' }}{{ stats.pct_crecimiento_usuarios }}%
            </span>
            este mes
          </span>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-icon kpi-emerald">
          <ion-icon name="wallet-outline"></ion-icon>
        </div>
        <div class="kpi-body">
          <span class="kpi-label">Cobranza Total</span>
          <span class="kpi-value">S/. {{ formatearNumero(stats.cobranza_total) }}</span>
          <span class="kpi-meta">
            <span class="kpi-chip positive">+S/. {{ formatearNumero(stats.recaudado_semana) }}</span>
            esta semana
          </span>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-icon kpi-violet">
          <ion-icon name="card-outline"></ion-icon>
        </div>
        <div class="kpi-body">
          <span class="kpi-label">Carnets Emitidos</span>
          <span class="kpi-value">{{ stats.carnets_emitidos }}</span>
          <span class="kpi-meta">
            <span class="kpi-chip neutral">{{ stats.usuarios_totales > 0 ? Math.round(stats.carnets_emitidos / stats.usuarios_totales * 100) : 0 }}%</span>
            completado
          </span>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-icon kpi-amber">
          <ion-icon name="checkbox-outline"></ion-icon>
        </div>
        <div class="kpi-body">
          <span class="kpi-label">Votaciones Activas</span>
          <span class="kpi-value">{{ stats.votaciones_activas }}</span>
          <span class="kpi-meta">
            {{ stats.votaciones_cerradas }} completadas
          </span>
        </div>
      </div>
    </section>

    <!-- Charts Row -->
    <div class="charts-row">
      <!-- Left: Cobranza Mensual -->
      <div class="panel panel-chart">
        <div class="panel-header">
          <div>
            <h3 class="panel-title">Cobranza Mensual</h3>
            <p class="panel-desc">Ingresos del último semestre</p>
          </div>
          <div class="panel-badge" v-if="stats.pagos_pendientes > 0">
            <ion-icon name="time-outline"></ion-icon>
            {{ stats.pagos_pendientes }} por aprobar
          </div>
        </div>
        <div class="chart-wrap">
          <canvas id="cobranzaChart"></canvas>
        </div>
        <div class="chart-footer">
          <div class="chart-footer-stat">
            <span class="chart-footer-label">Promedio</span>
            <span class="chart-footer-value">S/. {{ formatearNumero(stats.promedio_cobranza) }}</span>
          </div>
          <div class="chart-footer-stat">
            <span class="chart-footer-label">Total acumulado</span>
            <span class="chart-footer-value">S/. {{ formatearNumero(stats.cobranza_total) }}</span>
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <div class="right-column">
        <!-- Estado de Cobranza -->
        <div class="panel">
          <div class="panel-header">
            <h3 class="panel-title">Estado de Cobranza</h3>
          </div>
          <div class="status-bars">
            <div class="status-bar-item">
              <div class="status-bar-top">
                <div class="status-bar-indicator emerald"></div>
                <span class="status-bar-label">Pagado</span>
                <span class="status-bar-pct">{{ stats.cobranza_pct_pagado }}%</span>
              </div>
              <div class="status-bar-track">
                <div class="status-bar-fill emerald" :style="{ width: stats.cobranza_pct_pagado + '%' }"></div>
              </div>
            </div>
            <div class="status-bar-item">
              <div class="status-bar-top">
                <div class="status-bar-indicator amber"></div>
                <span class="status-bar-label">Pendiente</span>
                <span class="status-bar-pct">{{ stats.cobranza_pct_pendiente }}%</span>
              </div>
              <div class="status-bar-track">
                <div class="status-bar-fill amber" :style="{ width: stats.cobranza_pct_pendiente + '%' }"></div>
              </div>
            </div>
            <div class="status-bar-item">
              <div class="status-bar-top">
                <div class="status-bar-indicator rose"></div>
                <span class="status-bar-label">Vencido</span>
                <span class="status-bar-pct">{{ stats.cobranza_pct_vencido }}%</span>
              </div>
              <div class="status-bar-track">
                <div class="status-bar-fill rose" :style="{ width: stats.cobranza_pct_vencido + '%' }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Actividad Reciente -->
        <div class="panel">
          <div class="panel-header">
            <h3 class="panel-title">Actividad Reciente</h3>
          </div>
          <div class="activity-feed">
            <div class="activity-row" v-for="(item, idx) in stats.actividad_reciente" :key="idx">
              <div class="activity-dot" :style="{ background: item.color }"></div>
              <div class="activity-body">
                <p class="activity-msg">{{ item.titulo }}</p>
                <p class="activity-when">{{ item.tiempo }}</p>
              </div>
            </div>
            <div v-if="!stats.actividad_reciente?.length" class="empty-activity">
              <ion-icon name="pulse-outline"></ion-icon>
              <p>Sin actividad reciente</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Users Chart + Quick Actions -->
    <div class="bottom-row">
      <!-- Users Chart -->
      <div class="panel panel-chart-sm">
        <div class="panel-header">
          <div>
            <h3 class="panel-title">Crecimiento de Usuarios</h3>
            <p class="panel-desc">Nuevos usuarios registrados por mes</p>
          </div>
        </div>
        <div class="chart-wrap chart-wrap-sm">
          <canvas id="usuariosChart"></canvas>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="panel panel-actions">
        <div class="panel-header">
          <h3 class="panel-title">Acciones Rápidas</h3>
        </div>
        <div class="quick-grid">
          <router-link to="/usuarios" class="quick-btn">
            <div class="quick-btn-icon qb-blue">
              <ion-icon name="person-add-outline"></ion-icon>
            </div>
            <span class="quick-btn-label">Crear Usuario</span>
          </router-link>
          <router-link to="/carnets" class="quick-btn">
            <div class="quick-btn-icon qb-violet">
              <ion-icon name="card-outline"></ion-icon>
            </div>
            <span class="quick-btn-label">Generar Carnet</span>
          </router-link>
          <router-link to="/cobranza" class="quick-btn">
            <div class="quick-btn-icon qb-emerald">
              <ion-icon name="cash-outline"></ion-icon>
            </div>
            <span class="quick-btn-label">Registrar Pago</span>
          </router-link>
          <router-link to="/operaciones" class="quick-btn">
            <div class="quick-btn-icon qb-amber">
              <ion-icon name="checkmark-done-outline"></ion-icon>
            </div>
            <span class="quick-btn-label">Operaciones</span>
            <span v-if="stats.pagos_pendientes > 0" class="quick-btn-badge">{{ stats.pagos_pendientes }}</span>
          </router-link>
        </div>
      </div>
    </div>

    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import Chart from 'chart.js/auto'
import api from '@/services/api'

const cargando = ref(true)
const stats = ref({
  usuarios_totales: 0,
  usuarios_activos: 0,
  usuarios_nuevos_mes: 0,
  pct_crecimiento_usuarios: 0,
  cobranza_total: 0,
  recaudado_semana: 0,
  carnets_emitidos: 0,
  votaciones_activas: 0,
  votaciones_cerradas: 0,
  pagos_pendientes: 0,
  cobranza_pct_pagado: 0,
  cobranza_pct_pendiente: 0,
  cobranza_pct_vencido: 0,
  promedio_cobranza: 0,
  grafico_cobranza: { labels: [], data: [] },
  grafico_usuarios: { labels: [], data: [] },
  actividad_reciente: []
})

let chartCobranza = null
let chartUsuarios = null

const formatearNumero = (num) => {
  if (!num && num !== 0) return '0'
  return Number(num).toLocaleString('es-PE', { minimumFractionDigits: 0, maximumFractionDigits: 2 })
}

async function cargarEstadisticas() {
  cargando.value = true
  try {
    const response = await api.get('/dashboard/estadisticas')
    if (response.data?.success) {
      stats.value = { ...stats.value, ...response.data.data }
    }
  } catch (error) {
    console.error('Error cargando estadísticas del dashboard:', error)
    // Los valores por defecto (0) se mantendrán
  } finally {
    cargando.value = false
    await nextTick()
    renderizarGraficos()
  }
}

function renderizarGraficos() {
  // Destruir gráficos previos si existen
  if (chartCobranza) { chartCobranza.destroy(); chartCobranza = null }
  if (chartUsuarios) { chartUsuarios.destroy(); chartUsuarios = null }

  // Gráfico de Cobranza
  const cobranzaCtx = document.getElementById('cobranzaChart')
  if (cobranzaCtx) {
    chartCobranza = new Chart(cobranzaCtx, {
      type: 'line',
      data: {
        labels: stats.value.grafico_cobranza.labels,
        datasets: [
          {
            label: 'Cobranza (S/.)',
            data: stats.value.grafico_cobranza.data,
            borderColor: '#6366f1',
            backgroundColor: (ctx) => {
              const canvas = ctx.chart.ctx
              const gradient = canvas.createLinearGradient(0, 0, 0, 280)
              gradient.addColorStop(0, 'rgba(99, 102, 241, 0.12)')
              gradient.addColorStop(1, 'rgba(99, 102, 241, 0.01)')
              return gradient
            },
            borderWidth: 2.5,
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointBackgroundColor: '#6366f1',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointHoverRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#0f172a',
            titleColor: '#f8fafc',
            bodyColor: '#e2e8f0',
            borderColor: '#334155',
            borderWidth: 1,
            cornerRadius: 8,
            padding: 12,
            titleFont: { size: 13, weight: '600' },
            bodyFont: { size: 12 },
            callbacks: {
              label: (ctx) => `S/. ${Number(ctx.raw).toLocaleString('es-PE')}`
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: { color: 'rgba(0,0,0,0.04)', drawBorder: false },
            ticks: {
              color: '#94a3b8',
              font: { size: 11 },
              callback: (val) => `S/.${val >= 1000 ? (val/1000).toFixed(0) + 'K' : val}`
            },
            border: { display: false }
          },
          x: {
            grid: { display: false },
            ticks: { color: '#94a3b8', font: { size: 11 } },
            border: { display: false }
          }
        }
      }
    })
  }

  // Gráfico de Usuarios
  const usuariosCtx = document.getElementById('usuariosChart')
  if (usuariosCtx) {
    chartUsuarios = new Chart(usuariosCtx, {
      type: 'bar',
      data: {
        labels: stats.value.grafico_usuarios.labels,
        datasets: [
          {
            label: 'Usuarios Nuevos',
            data: stats.value.grafico_usuarios.data,
            backgroundColor: '#6366f1',
            borderRadius: 6,
            maxBarThickness: 32
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#0f172a',
            titleColor: '#f8fafc',
            bodyColor: '#e2e8f0',
            borderColor: '#334155',
            borderWidth: 1,
            cornerRadius: 8,
            padding: 12
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: { color: 'rgba(0,0,0,0.04)', drawBorder: false },
            ticks: { color: '#94a3b8', font: { size: 11 }, stepSize: 1 },
            border: { display: false }
          },
          x: {
            grid: { display: false },
            ticks: { color: '#94a3b8', font: { size: 11 } },
            border: { display: false }
          }
        }
      }
    })
  }
}

onMounted(() => {
  cargarEstadisticas()
})
</script>

<style scoped>
.dash-home {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ═══ LOADING ═══ */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 80px 20px;
  color: #64748b;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  font-size: 14px;
  font-weight: 500;
}

/* ═══ KPI ROW ═══ */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}

.kpi-card {
  background: white;
  border-radius: 12px;
  padding: 22px 20px;
  display: flex;
  align-items: flex-start;
  gap: 16px;
  border: 1px solid #e2e8f0;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.kpi-card:hover {
  border-color: #c7d2fe;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.06);
}

.kpi-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 22px;
}

.kpi-blue { background: #eef2ff; color: #6366f1; }
.kpi-emerald { background: #ecfdf5; color: #10b981; }
.kpi-violet { background: #f5f3ff; color: #8b5cf6; }
.kpi-amber { background: #fffbeb; color: #f59e0b; }

.kpi-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.kpi-label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.kpi-value {
  font-size: 26px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.5px;
  line-height: 1.1;
}

.kpi-meta {
  font-size: 12px;
  color: #94a3b8;
  display: flex;
  align-items: center;
  gap: 6px;
}

.kpi-chip {
  display: inline-flex;
  align-items: center;
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
}

.kpi-chip.positive {
  background: #ecfdf5;
  color: #059669;
}

.kpi-chip.negative {
  background: #fef2f2;
  color: #dc2626;
}

.kpi-chip.neutral {
  background: #eef2ff;
  color: #6366f1;
}

/* ═══ PANELS ═══ */
.panel {
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  padding: 22px 24px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.panel-title {
  font-size: 15px;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
  letter-spacing: -0.2px;
}

.panel-desc {
  font-size: 12px;
  color: #94a3b8;
  margin: 3px 0 0;
}

.panel-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  background: #fffbeb;
  color: #d97706;
}

.panel-badge ion-icon { font-size: 14px; }

/* ═══ CHARTS ROW ═══ */
.charts-row {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 18px;
}

.right-column {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.chart-wrap {
  height: 260px;
}

.chart-wrap-sm {
  height: 200px;
}

.chart-footer {
  display: flex;
  gap: 24px;
  padding-top: 16px;
  border-top: 1px solid #f1f5f9;
  margin-top: 16px;
}

.chart-footer-stat {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.chart-footer-label {
  font-size: 11px;
  color: #94a3b8;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.chart-footer-value {
  font-size: 16px;
  font-weight: 700;
  color: #0f172a;
}

/* ═══ STATUS BARS ═══ */
.status-bars {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.status-bar-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.status-bar-top {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-bar-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-bar-indicator.emerald { background: #10b981; }
.status-bar-indicator.amber { background: #f59e0b; }
.status-bar-indicator.rose { background: #f43f5e; }

.status-bar-label {
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
  flex: 1;
}

.status-bar-pct {
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
}

.status-bar-track {
  height: 6px;
  background: #f1f5f9;
  border-radius: 3px;
  overflow: hidden;
}

.status-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.6s ease;
}

.status-bar-fill.emerald { background: #10b981; }
.status-bar-fill.amber { background: #f59e0b; }
.status-bar-fill.rose { background: #f43f5e; }

/* ═══ ACTIVITY FEED ═══ */
.activity-feed {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.activity-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
}

.activity-row:last-child { border-bottom: none; }

.activity-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-top: 5px;
  flex-shrink: 0;
}

.activity-body {
  flex: 1;
}

.activity-msg {
  font-size: 13px;
  font-weight: 500;
  color: #1e293b;
  margin: 0 0 2px;
  line-height: 1.4;
}

.activity-when {
  font-size: 11px;
  color: #94a3b8;
  margin: 0;
}

.empty-activity {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 24px;
  color: #94a3b8;
}

.empty-activity ion-icon {
  font-size: 32px;
  color: #cbd5e1;
}

.empty-activity p {
  font-size: 13px;
  margin: 0;
}

/* ═══ BOTTOM ROW ═══ */
.bottom-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

/* ═══ QUICK ACTIONS ═══ */
.quick-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.quick-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 20px 16px;
  border-radius: 10px;
  text-decoration: none;
  border: 1px solid #e2e8f0;
  background: white;
  transition: all 0.2s ease;
  cursor: pointer;
  position: relative;
}

.quick-btn:hover {
  border-color: #c7d2fe;
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.08);
  transform: translateY(-2px);
}

.quick-btn-icon {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.qb-blue { background: #eef2ff; color: #6366f1; }
.qb-violet { background: #f5f3ff; color: #8b5cf6; }
.qb-emerald { background: #ecfdf5; color: #10b981; }
.qb-amber { background: #fffbeb; color: #f59e0b; }

.quick-btn-label {
  font-size: 13px;
  font-weight: 600;
  color: #334155;
}

.quick-btn-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background: #ef4444;
  color: white;
  font-size: 11px;
  font-weight: 700;
  min-width: 20px;
  height: 20px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 5px;
}

/* ═══ RESPONSIVE ═══ */
@media (max-width: 1200px) {
  .kpi-row {
    grid-template-columns: 1fr 1fr;
  }
  .charts-row {
    grid-template-columns: 1fr;
  }
  .bottom-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .kpi-row {
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
  .kpi-value {
    font-size: 22px;
  }
  .quick-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 480px) {
  .kpi-row {
    grid-template-columns: 1fr;
  }
  .quick-grid {
    grid-template-columns: 1fr;
  }
}
</style>
