<template>
  <div class="dashboard-layout">
    <!-- Overlay móvil -->
    <div class="sidebar-overlay" :class="{ active: sidebarOpen }" @click="sidebarOpen = false"></div>

    <!-- Sidebar -->
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <!-- Brand -->
      <div class="sidebar-brand">
        <div class="brand-mark">
          <img :src="'/uploads/logo/logo.png'" alt="Logo" class="brand-logo" />
        </div>
        <div class="brand-text">
          <span class="brand-name">{{ marca.nombre_pagina || 'Comunidad' }}</span>
          <span class="brand-edition">{{ esAdmin ? 'Panel Administrativo' : 'Panel Comunero' }}</span>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="sidebar-nav">

        <!-- ── SIDEBAR ADMIN ─────────────────────────── -->
        <template v-if="esAdmin">
          <div class="nav-section-label">Principal</div>
          <RouterLink to="/dashboard" :class="['nav-link', { active: activeView === 'dashboard' }]" @click="sidebarOpen = false">
            <ion-icon name="grid-outline" class="nav-link-icon"></ion-icon>
            <span class="nav-link-text">Inicio</span>
          </RouterLink>
          <RouterLink to="/usuarios" :class="['nav-link', { active: activeView === 'usuarios' }]" @click="sidebarOpen = false">
            <ion-icon name="people-outline" class="nav-link-icon"></ion-icon>
            <span class="nav-link-text">Usuarios</span>
          </RouterLink>
          <RouterLink to="/carnets" :class="['nav-link', { active: activeView === 'carnets' }]" @click="sidebarOpen = false">
            <ion-icon name="card-outline" class="nav-link-icon"></ion-icon>
            <span class="nav-link-text">Carnets</span>
          </RouterLink>

          <div class="nav-section-label">Finanzas</div>
          <RouterLink to="/cobranza" :class="['nav-link', { active: activeView === 'cobranza' }]" @click="sidebarOpen = false">
            <ion-icon name="wallet-outline" class="nav-link-icon"></ion-icon>
            <span class="nav-link-text">Cobranza</span>
          </RouterLink>
          <RouterLink to="/operaciones" :class="['nav-link', { active: activeView === 'operaciones' }]" @click="sidebarOpen = false">
            <ion-icon name="checkmark-done-outline" class="nav-link-icon"></ion-icon>
            <span class="nav-link-text">Operaciones</span>
          </RouterLink>

          <div class="nav-section-label">Gobernanza</div>
          <RouterLink to="/votacion" :class="['nav-link', { active: activeView === 'votacion' }]" @click="sidebarOpen = false">
            <ion-icon name="checkbox-outline" class="nav-link-icon"></ion-icon>
            <span class="nav-link-text">Votaciones</span>
          </RouterLink>
          <RouterLink to="/reuniones" :class="['nav-link', { active: activeView === 'reuniones' }]" @click="sidebarOpen = false">
            <ion-icon name="calendar-outline" class="nav-link-icon"></ion-icon>
            <span class="nav-link-text">Reuniones</span>
          </RouterLink>
          <RouterLink to="/elecciones" :class="['nav-link', { active: activeView === 'elecciones' }]" @click="sidebarOpen = false">
            <ion-icon name="podium-outline" class="nav-link-icon"></ion-icon>
            <span class="nav-link-text">Elecciones</span>
          </RouterLink>

          <div class="nav-section-label">Sistema</div>
          <RouterLink to="/reportes" :class="['nav-link', { active: activeView === 'reportes' }]" @click="sidebarOpen = false">
            <ion-icon name="stats-chart-outline" class="nav-link-icon"></ion-icon>
            <span class="nav-link-text">Reportes</span>
          </RouterLink>

          <div class="nav-group">
            <button class="nav-group-toggle" :class="{ active: isConfigGroup }" @click="configOpen = !configOpen">
              <ion-icon name="settings-outline" class="nav-link-icon"></ion-icon>
              <span class="nav-link-text">Configuración</span>
              <ion-icon name="chevron-down-outline" class="chevron" :class="{ rotated: configOpen }"></ion-icon>
            </button>
            <div class="nav-group-children" :class="{ open: configOpen }">
              <RouterLink to="/configuracion" class="nav-link nav-child" :class="{ active: activeView === 'configuracion' }" @click="sidebarOpen = false">
                <ion-icon name="construct-outline" class="nav-link-icon"></ion-icon>
                <span class="nav-link-text">General</span>
              </RouterLink>
              <RouterLink to="/configuracion/marca" class="nav-link nav-child" :class="{ active: activeView === 'marca' }" @click="sidebarOpen = false">
                <ion-icon name="image-outline" class="nav-link-icon"></ion-icon>
                <span class="nav-link-text">Marca</span>
              </RouterLink>
              <RouterLink to="/integraciones" class="nav-link nav-child" :class="{ active: activeView === 'integraciones' }" @click="sidebarOpen = false">
                <ion-icon name="flash-outline" class="nav-link-icon"></ion-icon>
                <span class="nav-link-text">Integraciones</span>
              </RouterLink>
              <RouterLink to="/config-cobranza" class="nav-link nav-child" :class="{ active: activeView === 'config-cobranza' }" @click="sidebarOpen = false">
                <ion-icon name="cash-outline" class="nav-link-icon"></ion-icon>
                <span class="nav-link-text">Config. Cobranza</span>
              </RouterLink>
            </div>
          </div>
        </template>

        <!-- ── SIDEBAR USUARIO COMUNERO ──────────────── -->
        <template v-else>
          <div class="nav-section-label">Mi Espacio</div>
          <RouterLink to="/mi-panel" :class="['nav-link', { active: activeView === 'mi-panel' }]" @click="sidebarOpen = false">
            <ion-icon name="person-circle-outline" class="nav-link-icon"></ion-icon>
            <span class="nav-link-text">Mi Perfil</span>
          </RouterLink>
          <RouterLink to="/votacion" :class="['nav-link', { active: activeView === 'votacion' }]" @click="sidebarOpen = false">
            <ion-icon name="checkbox-outline" class="nav-link-icon"></ion-icon>
            <span class="nav-link-text">Votaciones</span>
          </RouterLink>
        </template>

      </nav>

      <!-- Footer -->
      <div class="sidebar-extras">
        <a href="/" class="sidebar-ver-web" @click.prevent="irAWeb">
          <ion-icon name="globe-outline"></ion-icon>
          <span>Ver sitio web</span>
        </a>
      </div>
      <div class="sidebar-user">
        <div class="sidebar-user-avatar">{{ inicialesUsuario }}</div>
        <div class="sidebar-user-info">
          <span class="sidebar-user-name">{{ usuario?.nombre_completo?.split(' ').slice(0,2).join(' ') || 'Usuario' }}</span>
          <span class="sidebar-user-role">{{ usuario?.rol === 'admin' ? 'Administrador' : 'Usuario' }}</span>
        </div>
        <button class="sidebar-logout" @click="$emit('cerrar-sesion')" title="Cerrar sesión">
          <ion-icon name="log-out-outline"></ion-icon>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-area">
      <!-- Top Bar -->
      <header class="topbar">
        <div class="topbar-left">
          <button class="hamburger" @click="sidebarOpen = !sidebarOpen">
            <ion-icon name="menu-outline"></ion-icon>
          </button>
          <img :src="'/uploads/logo/logo.png'" alt="Logo" class="topbar-logo" />
          <div class="topbar-title">
            <h1>{{ (activeView === 'dashboard' || activeView === 'mi-panel') ? `Hola, ${usuario?.nombre_completo?.split(' ')[0] || 'Bienvenido'}` : getTituloVista() }}</h1>
            <p class="topbar-subtitle">{{ (activeView === 'dashboard' || activeView === 'mi-panel') ? (esAdmin ? 'Bienvenido a tu panel de control' : 'Bienvenido a tu espacio comunero') : getSubtituloVista() }}</p>
          </div>
        </div>
        <div class="topbar-right">
          <div class="topbar-date">
            <ion-icon name="calendar-outline"></ion-icon>
            <span>{{ fechaHoy }}</span>
          </div>
          <div class="topbar-avatar">
            <div class="topbar-avatar-circle">{{ inicialesUsuario }}</div>
          </div>
        </div>
      </header>

      <!-- Routed views -->
      <div class="main-content-area">
        <RouterView />
      </div>
    </main>

    <!-- Barra flotante de exportación -->
    <Transition name="slide-up">
      <div v-if="exportStore.activo()" class="export-toast">
        <div class="export-toast-info">
          <ion-icon name="document-outline" class="export-toast-icon"></ion-icon>
          <div class="export-toast-texts">
            <span class="export-toast-titulo">Generando PDF...</span>
            <span class="export-toast-msg">{{ exportStore.mensaje }}</span>
          </div>
        </div>
        <div class="export-toast-barra">
          <div class="export-toast-fill" :style="{ width: exportStore.progreso + '%' }"></div>
        </div>
        <div class="export-toast-actions">
          <span class="export-toast-pct">{{ exportStore.progreso }}%</span>
          <button class="export-toast-cancelar" @click="cancelarExportacion">
            <ion-icon name="stop-circle-outline"></ion-icon>
            Detener
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { exportStore } from '@/services/exportStore'
import api from '@/services/api'
import { useMarca } from '@/composables/useMarca'

const props = defineProps({ usuario: Object })
const emit = defineEmits(['cerrar-sesion'])

const route = useRoute()
const sidebarOpen = ref(false)
const marca = useMarca()

// La vista activa se deriva directamente de la ruta actual
const activeView = computed(() => route.name || 'dashboard')

// Grupo Configuración
const configRoutes = ['configuracion', 'marca', 'integraciones', 'config-cobranza']
const isConfigGroup = computed(() => configRoutes.includes(activeView.value))
const configOpen = ref(isConfigGroup.value)

// Auto-abre el grupo si se navega a una sub-ruta
watch(isConfigGroup, (val) => {
  if (val) configOpen.value = true
})

const inicialesUsuario = computed(() => {
  const nombre = props.usuario?.nombre_completo || ''
  return nombre.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase() || 'U'
})

const esAdmin = computed(() => {
  const rol = props.usuario?.rol
  return rol === 'admin' || rol === 'editor' || rol === 'moderator'
})

const fechaHoy = computed(() => {
  const hoy = new Date()
  return hoy.toLocaleDateString('es-PE', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
})

const irAWeb = () => {
  window.location.href = '/'
}

const titulos = {
  'mi-panel': { titulo: 'Mi Panel', subtitulo: 'Tu información personal, reuniones y elecciones' },
  usuarios: { titulo: 'Usuarios', subtitulo: 'Gestiona todos los usuarios del sistema' },
  configuracion: { titulo: 'Configuración', subtitulo: 'Configura los campos del formulario' },
  marca: { titulo: 'Configuración de Marca', subtitulo: 'Personaliza el logo, favicon y colores de tu organización' },
  reportes: { titulo: 'Reportes', subtitulo: 'Visualiza los reportes del sistema' },
  integraciones: { titulo: 'Integraciones', subtitulo: 'Gestiona las integraciones con APIs externas' },
  cobranza: { titulo: 'Cobranza', subtitulo: 'Gestiona la cobranza a usuarios' },
  'config-cobranza': { titulo: 'Configuración de Cobranza', subtitulo: 'Configura conceptos de pago' },
  operaciones: { titulo: 'Operaciones', subtitulo: 'Aprueba o rechaza pagos pendientes' },
  votacion: { titulo: 'Votaciones', subtitulo: 'Participa en las votaciones activas de la comunidad' },
  carnets: { titulo: 'Carnets', subtitulo: 'Emite y gestiona carnets de Usuarios' },
  elecciones: { titulo: 'Elecciones', subtitulo: 'Crea y gestiona elecciones y votaciones' },
  'eleccion-detalle': { titulo: 'Detalle de Elección', subtitulo: 'Gestiona opciones y resultados de la elección' },
  reuniones: { titulo: 'Reuniones', subtitulo: 'Gestiona las reuniones de la comunidad' },
  'usuario-perfil': { titulo: 'Perfil de Usuario', subtitulo: 'Información detallada del usuario' }
}

const getTituloVista = () => {
  const info = titulos[activeView.value]
  return info?.titulo || 'Panel de Control'
}

const getSubtituloVista = () => {
  const info = titulos[activeView.value]
  return info?.subtitulo || ''
}

const cancelarExportacion = async () => {
  if (exportStore.taskId) {
    try {
      await api.post(`/carnets/cancelar/${exportStore.taskId}`)
    } catch (e) { /* ya terminó */ }
  }
  exportStore.reset()
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.dashboard-layout {
  display: flex;
  height: 100vh;
  background: #f1f5f9;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #1e293b;
}

/* ═══════════════════════════════════════════
   SIDEBAR
   ═══════════════════════════════════════════ */
.sidebar {
  width: 272px;
  background: #0f172a;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #334155 transparent;
}

.sidebar::-webkit-scrollbar { width: 4px; }
.sidebar::-webkit-scrollbar-track { background: transparent; }
.sidebar::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }

/* Brand */
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 24px 24px 28px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.brand-mark {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.brand-icon {
  font-size: 22px;
  color: white;
}

.brand-logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 4px;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-name {
  font-size: 17px;
  font-weight: 700;
  color: #f8fafc;
  letter-spacing: -0.3px;
}

.brand-edition {
  font-size: 11px;
  color: #64748b;
  font-weight: 500;
  letter-spacing: 0.2px;
}

/* Navigation */
.sidebar-nav {
  flex: 1;
  padding: 16px 14px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-section-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: #475569;
  padding: 16px 12px 6px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  text-decoration: none;
  color: #94a3b8;
  font-size: 13.5px;
  font-weight: 500;
  transition: all 0.15s ease;
  position: relative;
}

.nav-link:hover {
  background: rgba(255,255,255,0.04);
  color: #e2e8f0;
}

.nav-link.active {
  background: rgba(99, 102, 241, 0.12);
  color: #a5b4fc;
}

.nav-link.active::before {
  content: '';
  position: absolute;
  left: -14px;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 20px;
  border-radius: 0 3px 3px 0;
  background: #6366f1;
}

.nav-link-icon {
  font-size: 18px;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.nav-link-text {
  flex: 1;
}

ion-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* Collapsible group */
.nav-group {
  display: flex;
  flex-direction: column;
}

.nav-group-toggle {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  color: #94a3b8;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 13.5px;
  font-weight: 500;
  width: 100%;
  text-align: left;
  transition: all 0.15s ease;
  font-family: inherit;
}

.nav-group-toggle:hover {
  background: rgba(255,255,255,0.04);
  color: #e2e8f0;
}

.nav-group-toggle.active {
  color: #a5b4fc;
}

.chevron {
  font-size: 14px;
  transition: transform 0.25s ease;
  margin-left: auto;
}

.chevron.rotated {
  transform: rotate(-180deg);
}

.nav-group-children {
  overflow: hidden;
  max-height: 0;
  transition: max-height 0.3s ease;
  display: flex;
  flex-direction: column;
  gap: 1px;
  padding-left: 12px;
}

.nav-group-children.open {
  max-height: 200px;
}

.nav-child {
  padding: 8px 12px;
  font-size: 13px;
}

.nav-child.active::before {
  left: -26px;
}

/* User footer */
.sidebar-extras {
  margin-top: auto;
  padding: 8px 12px 0;
}
.sidebar-ver-web {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px; border-radius: 8px;
  color: rgba(255,255,255,0.85); text-decoration: none;
  font-size: 13px; font-weight: 600;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  transition: all 0.2s;
}
.sidebar-ver-web:hover {
  background: rgba(134,239,172,0.15);
  color: #86efac;
  border-color: rgba(134,239,172,0.3);
}
.sidebar-ver-web ion-icon { font-size: 18px; }

.sidebar-user {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid rgba(255,255,255,0.06);
}

.sidebar-user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
}

.sidebar-user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.sidebar-user-name {
  font-size: 13px;
  font-weight: 600;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-user-role {
  font-size: 11px;
  color: #64748b;
  font-weight: 500;
}

.sidebar-logout {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  transition: all 0.15s;
  font-size: 18px;
}

.sidebar-logout:hover {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

/* ═══════════════════════════════════════════
   MAIN AREA
   ═══════════════════════════════════════════ */
.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-width: 0;
}

/* Top bar */
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 32px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.topbar-logo {
  height: 44px;
  width: auto;
  object-fit: contain;
}

.topbar-title h1 {
  font-size: 22px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.3px;
  line-height: 1.2;
}

.topbar-subtitle {
  font-size: 13px;
  color: #64748b;
  font-weight: 400;
  margin-top: 2px;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.topbar-date {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
  text-transform: capitalize;
}

.topbar-date ion-icon {
  font-size: 16px;
  color: #94a3b8;
}

.topbar-avatar-circle {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 13px;
}

/* Hamburger */
.hamburger {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  color: #334155;
  padding: 4px;
  line-height: 1;
}

/* Main content */
.main-content-area {
  flex: 1;
  overflow-y: auto;
  padding: 28px 32px;
}

/* Overlay */
.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 99;
  backdrop-filter: blur(4px);
}
.sidebar-overlay.active { display: block; }

/* ═══════════════════════════════════════════
   RESPONSIVE
   ═══════════════════════════════════════════ */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    z-index: 100;
    transform: translateX(-100%);
    transition: transform 0.25s ease;
    box-shadow: 4px 0 20px rgba(0,0,0,0.3);
  }
  .sidebar.open {
    transform: translateX(0);
  }

  .hamburger {
    display: flex;
    align-items: center;
  }

  .topbar {
    padding: 14px 16px;
  }

  .topbar-title h1 {
    font-size: 16px;
  }

  .topbar-subtitle,
  .topbar-date { display: none; }

  .main-content-area {
    padding: 16px;
  }
}

@media (max-width: 480px) {
  .main-content-area { padding: 12px; }
  .topbar-title h1 { font-size: 15px; }
}

/* BARRA FLOTANTE DE EXPORTACIÓN */
.export-toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 340px;
  background: #1e293b;
  color: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.35);
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.export-toast-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.export-toast-icon {
  font-size: 22px;
  color: #818cf8;
  flex-shrink: 0;
}

.export-toast-texts {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.export-toast-titulo {
  font-size: 13px;
  font-weight: 700;
  color: white;
}

.export-toast-msg {
  font-size: 11px;
  color: #94a3b8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.export-toast-barra {
  height: 4px;
  background: #334155;
  border-radius: 4px;
  overflow: hidden;
}

.export-toast-fill {
  height: 100%;
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
  border-radius: 4px;
  transition: width 0.4s ease;
}

.export-toast-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.export-toast-pct {
  font-size: 13px;
  font-weight: 700;
  color: #a5b4fc;
}

.export-toast-cancelar {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.export-toast-cancelar:hover {
  background: #dc2626;
}

.export-toast-cancelar ion-icon {
  font-size: 14px;
}

/* Animación entrada/salida */
.slide-up-enter-active, .slide-up-leave-active {
  transition: all 0.3s ease;
}
.slide-up-enter-from, .slide-up-leave-to {
  transform: translateY(20px);
  opacity: 0;
}
</style>
