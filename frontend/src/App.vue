<template>
  <div class="app-container">
    <!-- Login -->
    <Login v-if="!autenticado" @autenticado="onAutenticado" />

    <!-- Dashboard (después de login) -->
    <div v-else class="full-height-view">
      <Dashboard :usuario="usuarioActual" @cerrar-sesion="cerrarSesion" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Login from './components/Login.vue'
import Dashboard from './components/Dashboard.vue'
import authService from './services/auth.service'

const autenticado = ref(false)
const usuarioActual = ref(null)

onMounted(() => {
  if (authService.estaAutenticado()) {
    usuarioActual.value = authService.obtenerUsuario()
    autenticado.value = true
  }
})

const onAutenticado = (usuario) => {
  usuarioActual.value = usuario
  autenticado.value = true
}

const cerrarSesion = async () => {
  await authService.logout()
  usuarioActual.value = null
  autenticado.value = false
}
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.full-height-view {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.app-header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.app-header h1 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

.nav-menu {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.nav-btn {
  padding: 0.5rem 1rem;
  background-color: #34495e;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.nav-btn:hover {
  background-color: #1abc9c;
}

.nav-btn.active {
  background-color: #1abc9c;
  font-weight: bold;
}

.app-main {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem;
}

.view-container {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.home-view {
  text-align: center;
}

.home-view h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.home-view p {
  color: #7f8c8d;
  margin-bottom: 2rem;
}

.btn-dashboard {
  padding: 0.75rem 1.5rem;
  background-color: #1abc9c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s ease;
  margin-bottom: 2rem;
}

.btn-dashboard:hover {
  background-color: #16a085;
}

.status-info {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 2rem;
  text-align: left;
}

.status-info h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.status-info p {
  margin: 0.5rem 0;
  color: #2c3e50;
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 3px;
  font-weight: bold;
  font-size: 0.85rem;
}

.status.healthy {
  background-color: #d4edda;
  color: #155724;
}

.status.offline {
  background-color: #f8d7da;
  color: #721c24;
}

.status.checking {
  background-color: #fff3cd;
  color: #856404;
}

.app-footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 1.5rem;
  margin-top: 2rem;
}

.app-footer p {
  margin: 0;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 1rem;
  }

  .app-main {
    padding: 1rem;
  }

  .view-container {
    padding: 1rem;
  }

  .app-header h1 {
    font-size: 1.4rem;
  }

  .nav-menu {
    gap: 0.5rem;
  }

  .nav-btn {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
}
</style>
