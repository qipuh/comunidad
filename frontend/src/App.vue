<template>
  <div>
    <!-- Web pública multi-página -->
    <WebApp v-if="vista === 'web'" />

    <!-- Login admin -->
    <Login v-else-if="vista === 'login'" @autenticado="onAutenticado" @volver="volverAWeb" />

    <!-- Dashboard -->
    <Dashboard v-else-if="vista === 'dashboard'" :usuario="usuarioActual" @cerrar-sesion="cerrarSesion" />

    <!-- Global Alert -->
    <Alert
      :visible="alertState.visible"
      :type="alertState.type"
      :title="alertState.title"
      :message="alertState.message"
      :duration="alertState.duration"
      @close="alertState.visible = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import WebApp from './pages/web/WebApp.vue'
import Login from './components/Login.vue'
import Dashboard from './components/Dashboard.vue'
import Alert from './components/Alert.vue'
import authService from './services/auth.service'
import { useWebNav } from './composables/useWebNav'
import { alertStore } from './stores/alertStore'

const RUTAS_DASHBOARD = ['/dashboard', '/usuarios', '/configuracion', '/marca', '/reportes',
  '/integraciones', '/cobranza', '/operaciones', '/elecciones', '/votacion',
  '/carnets', '/reuniones']

function vistaDesdeUrl() {
  const path = window.location.pathname || '/'
  if (path === '/admin' || path === '/login') return 'login'
  if (RUTAS_DASHBOARD.some(r => path === r || path.startsWith(r + '/'))) {
    return authService.estaAutenticado() ? 'dashboard' : 'login'
  }
  return 'web'
}

const vista = ref(vistaDesdeUrl())
const usuarioActual = ref(null)
const { setIrAdmin } = useWebNav()
const alertState = alertStore.state

// Cuando el usuario hace clic en "Área Admin" desde cualquier página web
setIrAdmin(() => {
  vista.value = 'login'
  window.history.pushState({}, '', '/admin')
})

onMounted(() => {
  if (authService.estaAutenticado() && vista.value === 'web') {
    usuarioActual.value = authService.obtenerUsuario()
    // No forzar dashboard si está navegando la web pública
  } else if (vista.value === 'dashboard') {
    usuarioActual.value = authService.obtenerUsuario()
  }
})

const onAutenticado = (usuario) => {
  usuarioActual.value = usuario
  vista.value = 'dashboard'
  window.history.pushState({}, '', '/dashboard')
}

const cerrarSesion = async () => {
  await authService.logout()
  usuarioActual.value = null
  vista.value = 'web'
  window.history.pushState({}, '', '/')
}

const volverAWeb = () => {
  vista.value = 'web'
  window.history.pushState({}, '', '/')
}

window.addEventListener('popstate', () => {
  vista.value = vistaDesdeUrl()
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f1f5f9; color: #1e293b; -webkit-font-smoothing: antialiased; }
</style>
