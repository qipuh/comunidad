<template>
  <div class="dashboard-container">
    <!-- Overlay móvil -->
    <div class="sidebar-overlay" :class="{ active: sidebarOpen }" @click="sidebarOpen = false"></div>

    <!-- Sidebar -->
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-header">
        <div class="logo">
          <ion-icon name="analytics-outline" class="logo-icon"></ion-icon>
          <span class="logo-text">Comunidad</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <button
          @click="navigateTo('dashboard')"
          :class="['nav-item', { active: activeView === 'dashboard' }]"
        >
          <ion-icon name="home-outline" class="nav-icon"></ion-icon>
          <span class="nav-label">Inicio</span>
        </button>
        <button
          @click="navigateTo('usuarios')"
          :class="['nav-item', { active: activeView === 'usuarios' }]"
        >
          <ion-icon name="people-outline" class="nav-icon"></ion-icon>
          <span class="nav-label">Usuarios</span>
        </button>
        <button
          @click="navigateTo('configuracion')"
          :class="['nav-item', { active: activeView === 'configuracion' }]"
        >
          <ion-icon name="settings-outline" class="nav-icon"></ion-icon>
          <span class="nav-label">Configuración</span>
        </button>
        <button
          @click="navigateTo('reportes')"
          :class="['nav-item', { active: activeView === 'reportes' }]"
        >
          <ion-icon name="document-text-outline" class="nav-icon"></ion-icon>
          <span class="nav-label">Reportes</span>
        </button>
        <button
          @click="navigateTo('integraciones')"
          :class="['nav-item', { active: activeView === 'integraciones' }]"
        >
          <ion-icon name="flash-outline" class="nav-icon"></ion-icon>
          <span class="nav-label">Integraciones</span>
        </button>
      </nav>

      <div class="sidebar-footer">
        <button class="upgrade-btn">
          <ion-icon name="rocket-outline"></ion-icon>
          Upgrade Plan
        </button>
        <a href="#" class="help-link">
          <ion-icon name="help-circle-outline"></ion-icon>
          Ayuda & Información
        </a>
        <a href="#" class="logout-link" @click.prevent="$emit('cerrar-sesion')">
          <ion-icon name="log-out-outline"></ion-icon>
          Cerrar Sesión
        </a>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Header -->
      <header class="top-header">
        <div class="header-left">
          <button class="menu-toggle" @click="sidebarOpen = !sidebarOpen">
            <ion-icon name="menu-outline"></ion-icon>
          </button>
          <h1 v-if="activeView === 'dashboard'">Hola, {{ usuario?.nombre_completo?.split(' ')[0] || 'Bienvenido' }}</h1>
          <h1 v-else-if="activeView === 'usuarios'">Usuarios</h1>
          <h1 v-else-if="activeView === 'configuracion'">Configuración</h1>
          <h1 v-else-if="activeView === 'reportes'">Reportes</h1>
          <h1 v-else-if="activeView === 'integraciones'">Integraciones</h1>
          <p class="header-subtitle">
            <span v-if="activeView === 'dashboard'">Bienvenido a tu panel de control</span>
            <span v-else-if="activeView === 'usuarios'">Gestiona todos los usuarios del sistema</span>
            <span v-else-if="activeView === 'configuracion'">Configura los campos del formulario</span>
            <span v-else-if="activeView === 'reportes'">Visualiza los reportes del sistema</span>
            <span v-else-if="activeView === 'integraciones'">Gestiona las integraciones con APIs externas</span>
          </p>
        </div>

        <div class="header-right">
          <div class="user-profile">
            <div class="avatar-initials" style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:1rem;">{{ inicialesUsuario }}</div>
            <div class="user-info">
              <p class="user-name">{{ usuario?.nombre_completo?.split(' ')[0] || 'Usuario' }}</p>
              <p class="user-role">{{ usuario?.rol === 'admin' ? 'Administrador' : 'Usuario' }}</p>
            </div>
            <button class="menu-btn">
              <ion-icon name="ellipsis-vertical"></ion-icon>
            </button>
          </div>
        </div>
      </header>

      <!-- Dashboard View -->
      <div v-if="activeView === 'dashboard'">
      <!-- Stats Grid -->
      <section class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon users">
            <ion-icon name="people"></ion-icon>
          </div>
          <div class="stat-content">
            <p class="stat-label">Usuarios Totales</p>
            <p class="stat-value">1,234</p>
            <p class="stat-change positive">+12% este mes</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon events">
            <ion-icon name="calendar"></ion-icon>
          </div>
          <div class="stat-content">
            <p class="stat-label">Eventos</p>
            <p class="stat-value">456</p>
            <p class="stat-change positive">+8% esta semana</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon active">
            <ion-icon name="checkmark-circle"></ion-icon>
          </div>
          <div class="stat-content">
            <p class="stat-label">Activos Hoy</p>
            <p class="stat-value">89%</p>
            <p class="stat-change positive">+5% vs ayer</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon revenue">
            <ion-icon name="wallet"></ion-icon>
          </div>
          <div class="stat-content">
            <p class="stat-label">Ingresos</p>
            <p class="stat-value">$12.5K</p>
            <p class="stat-change negative">-3% este mes</p>
          </div>
        </div>
      </section>

      <div class="dashboard-grid">
        <!-- Left Column -->
        <div class="col-left">
          <!-- Performance Chart -->
          <section class="card performance-card">
            <div class="card-header">
              <div class="header-title">
                <ion-icon name="trending-up-outline"></ion-icon>
                <h2>Performance</h2>
              </div>
              <select class="time-filter">
                <option>Últimos 7 días</option>
                <option>Últimos 30 días</option>
                <option>Últimos 90 días</option>
              </select>
            </div>
            <div class="chart-container">
              <canvas id="performanceChart"></canvas>
            </div>
            <div class="chart-legend">
              <span class="legend-item">
                <span class="legend-dot" style="background: #3B82F6;"></span>
                Usuarios Registrados
              </span>
              <span class="legend-item">
                <span class="legend-dot" style="background: #10B981;"></span>
                Usuarios Activos
              </span>
            </div>
          </section>

          <!-- Current Tasks -->
          <section class="card tasks-card">
            <div class="card-header">
              <div class="header-title">
                <ion-icon name="checkmark-done-outline"></ion-icon>
                <h2>Tareas Actuales</h2>
              </div>
              <a href="#" class="see-all">Ver todas</a>
            </div>
            <div class="tasks-list">
              <div class="task-item">
                <input type="checkbox" class="task-checkbox">
                <div class="task-details">
                  <p class="task-title">Validar campos dinámicos</p>
                  <p class="task-time">En progreso</p>
                </div>
              </div>
              <div class="task-item">
                <input type="checkbox" class="task-checkbox">
                <div class="task-details">
                  <p class="task-title">Integrar API RENIEC</p>
                  <p class="task-time">Completado</p>
                </div>
              </div>
              <div class="task-item">
                <input type="checkbox" class="task-checkbox">
                <div class="task-details">
                  <p class="task-title">Configurar Facturiza</p>
                  <p class="task-time">Pendiente</p>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- Right Column -->
        <aside class="col-right">
          <!-- Activity Feed -->
          <section class="card activity-card">
            <div class="card-header">
              <div class="header-title">
                <ion-icon name="notifications-outline"></ion-icon>
                <h2>Actividad</h2>
              </div>
              <a href="#" class="see-all">Ver más</a>
            </div>
            <div class="activity-list">
              <div class="activity-item">
                <div class="activity-avatar" style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;color:white;font-size:0.75rem;font-weight:700;">U</div>
                <div class="activity-details">
                  <p class="activity-user">John Doe</p>
                  <p class="activity-action">creó un nuevo campo</p>
                  <p class="activity-time">Hace 2 horas</p>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-avatar" style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;color:white;font-size:0.75rem;font-weight:700;">U</div>
                <div class="activity-details">
                  <p class="activity-user">Jane Smith</p>
                  <p class="activity-action">completó un registro</p>
                  <p class="activity-time">Hace 4 horas</p>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-avatar" style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;color:white;font-size:0.75rem;font-weight:700;">U</div>
                <div class="activity-details">
                  <p class="activity-user">Mike Johnson</p>
                  <p class="activity-action">actualizó la configuración</p>
                  <p class="activity-time">Hace 1 día</p>
                </div>
              </div>
            </div>
          </section>

          <!-- Quick Stats -->
          <section class="card quick-stats">
            <div class="header-title">
              <ion-icon name="stats-chart-outline"></ion-icon>
              <h3>Estadísticas Rápidas</h3>
            </div>
            <div class="stat-item">
              <span class="stat-name">Tasa de Conversión</span>
              <span class="stat-val">42.5%</span>
            </div>
            <div class="stat-item">
              <span class="stat-name">Usuarios Nuevos</span>
              <span class="stat-val">142</span>
            </div>
            <div class="stat-item">
              <span class="stat-name">Campos Configurados</span>
              <span class="stat-val">18</span>
            </div>
          </section>
        </aside>
      </div>
      </div>

      <!-- Usuarios View -->
      <UsuariosView v-if="activeView === 'usuarios'" />

      <!-- Configuración View -->
      <ConfiguracionView v-if="activeView === 'configuracion'" />

      <!-- Reportes View -->
      <ReportesView v-if="activeView === 'reportes'" />

      <!-- Integraciones View -->
      <IntegracionesView v-if="activeView === 'integraciones'" />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import UsuariosView from './dashboard/UsuariosView.vue'
import ConfiguracionView from './dashboard/ConfiguracionView.vue'
import ReportesView from './dashboard/ReportesView.vue'
import IntegracionesView from './dashboard/IntegracionesView.vue'

const props = defineProps({ usuario: Object })
const emit = defineEmits(['cerrar-sesion'])

const inicialesUsuario = computed(() => {
  const nombre = props.usuario?.nombre_completo || ''
  return nombre.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase() || 'U'
})

const activeView = ref('dashboard')
const sidebarOpen = ref(false)

const navigateTo = (view) => {
  activeView.value = view
  sidebarOpen.value = false
}

onMounted(() => {
  console.log('Dashboard mounted')
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.dashboard-container {
  display: flex;
  height: 100vh;
  background: #f8fafc;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
}

/* SIDEBAR */
.sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #e2e8f0;
  padding: 24px 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  margin-bottom: 32px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
}

.logo-icon {
  font-size: 28px;
  color: #4f46e5;
}

ion-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  text-decoration: none;
  color: #64748b;
  transition: all 0.2s;
  cursor: pointer;
}

.nav-item:hover {
  background: #f1f5f9;
  color: #334155;
}

.nav-item.active {
  background: #e0e7ff;
  color: #4f46e5;
}

.nav-icon {
  font-size: 20px;
  min-width: 20px;
}

.nav-icon {
  font-size: 20px;
}

.nav-label {
  font-size: 14px;
  font-weight: 500;
}

.sidebar-footer {
  border-top: 1px solid #e2e8f0;
  padding-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.upgrade-btn {
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
  font-size: 14px;
}

.upgrade-btn:hover {
  background: #4338ca;
}

.upgrade-btn ion-icon {
  font-size: 18px;
}

.help-link,
.logout-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  color: #64748b;
  text-decoration: none;
  font-size: 13px;
  transition: color 0.2s;
}

.help-link:hover,
.logout-link:hover {
  color: #1e293b;
}

.help-link ion-icon,
.logout-link ion-icon {
  font-size: 16px;
}

/* MAIN CONTENT */
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}

/* HEADER */
.top-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.header-left h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.header-subtitle {
  color: #64748b;
  font-size: 14px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user-info {
  text-align: right;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.user-role {
  font-size: 12px;
  color: #64748b;
}

.menu-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #64748b;
  padding: 8px;
  display: flex;
  align-items: center;
}

.menu-btn ion-icon {
  font-size: 20px;
}

/* STATS GRID */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon ion-icon {
  font-size: 28px;
}

.stat-icon.users {
  background: #dbeafe;
}

.stat-icon.events {
  background: #dbeafe;
}

.stat-icon.active {
  background: #dcfce7;
}

.stat-icon.revenue {
  background: #fef3c7;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 12px;
  color: #64748b;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.stat-change {
  font-size: 12px;
}

.stat-change.positive {
  color: #10b981;
}

.stat-change.negative {
  color: #ef4444;
}

/* DASHBOARD GRID */
.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

/* CARDS */
.card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header h2,
.card-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-title ion-icon {
  font-size: 20px;
  color: #4f46e5;
}

.time-filter {
  padding: 6px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 13px;
  color: #64748b;
  background: white;
  cursor: pointer;
}

.see-all {
  color: #4f46e5;
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
}

.see-all:hover {
  text-decoration: underline;
}

/* CHART */
.chart-container {
  height: 300px;
  margin-bottom: 16px;
  background: #f8fafc;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}

.chart-legend {
  display: flex;
  gap: 24px;
  justify-content: center;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #64748b;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 2px;
}

/* TASKS */
.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
}

.task-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.task-details {
  flex: 1;
}

.task-title {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 2px;
}

.task-time {
  font-size: 12px;
  color: #64748b;
}

/* ACTIVITY */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  gap: 12px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.activity-details {
  flex: 1;
}

.activity-user {
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
}

.activity-action {
  font-size: 13px;
  color: #64748b;
}

.activity-time {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 2px;
}

/* QUICK STATS */
.quick-stats .header-title {
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #e2e8f0;
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-name {
  font-size: 13px;
  color: #64748b;
}

.stat-val {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
}

/* RESPONSIVE */
@media (max-width: 1200px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

/* MENU TOGGLE - oculto en desktop */
.menu-toggle {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  color: #334155;
  padding: 4px;
  line-height: 1;
}

/* OVERLAY */
.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  z-index: 99;
}
.sidebar-overlay.active { display: block; }

/* VIEW CONTENT */
.view-content {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 200px);
  padding: 20px;
}

.placeholder-card {
  background: white;
  padding: 60px 40px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  max-width: 500px;
}

.placeholder-icon {
  font-size: 64px;
  color: #4f46e5;
  margin-bottom: 20px;
  display: block;
}

.placeholder-card h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 12px;
}

.placeholder-card p {
  font-size: 16px;
  color: #64748b;
  margin-bottom: 8px;
}

.placeholder-text {
  font-size: 14px;
  color: #94a3b8;
  font-style: italic;
}

.nav-item {
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
}

@media (max-width: 768px) {
  /* Sidebar como drawer */
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    z-index: 100;
    transform: translateX(-100%);
    transition: transform 0.25s ease;
    box-shadow: 4px 0 20px rgba(0,0,0,0.15);
    width: 260px;
  }
  .sidebar.open {
    transform: translateX(0);
  }

  /* Mostrar botón hamburguesa */
  .menu-toggle {
    display: flex;
    align-items: center;
  }

  /* Header compacto */
  .top-header {
    padding: 12px 16px;
    gap: 12px;
  }

  .header-subtitle { display: none; }

  .top-header h1 {
    font-size: 1.1rem;
  }

  .user-info { display: none; }

  /* Main content ocupa todo el ancho */
  .main-content {
    padding: 16px;
    width: 100%;
  }

  /* Stats en 2 columnas */
  .stats-grid {
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }

  .stat-card {
    padding: 14px;
  }

  .stat-value { font-size: 1.4rem; }

  /* Dashboard grid en 1 columna */
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }

  .stat-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .top-header h1 { font-size: 1rem; }

  .main-content { padding: 12px; }
}
</style>
