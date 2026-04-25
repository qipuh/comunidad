<template>
  <div class="integraciones-container">
    <div class="view-header">
      <div class="header-content">
        <h2>Integraciones con APIs</h2>
        <button class="btn-primary">
          <ion-icon name="add-circle-outline"></ion-icon>
          Nueva Integración
        </button>
      </div>
    </div>

    <!-- Tab Navigation -->
    <div class="tabs-navigation">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="['tab-btn', { active: activeTab === tab.id }]"
      >
        <ion-icon :name="tab.icono"></ion-icon>
        {{ tab.nombre }}
      </button>
    </div>

    <!-- Factiliza Manager -->
    <div v-if="activeTab === 'factiliza'" class="tab-content">
      <FactilizaManager />
    </div>

    <!-- Integraciones Grid -->
    <div v-if="activeTab === 'todas'" class="tab-content">

    <div class="integraciones-grid">
      <div v-for="integracion in integraciones" :key="integracion.id" class="integracion-card">
        <div class="integracion-header">
          <div class="integracion-icon" :class="integracion.tipo">
            <ion-icon :name="integracion.icono"></ion-icon>
          </div>
          <div class="integracion-title">
            <h3>{{ integracion.nombre }}</h3>
            <p class="tipo">{{ integracion.tipo }}</p>
          </div>
          <div class="status-dot" :class="integracion.activa ? 'activa' : 'inactiva'"></div>
        </div>

        <p class="descripcion">{{ integracion.descripcion }}</p>

        <div class="integracion-stats">
          <div class="stat">
            <span class="stat-value">{{ integracion.llamadas }}</span>
            <span class="stat-label">Llamadas</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ integracion.tasa }}%</span>
            <span class="stat-label">Éxito</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ integracion.tiempo }}ms</span>
            <span class="stat-label">Promedio</span>
          </div>
        </div>

        <div class="integracion-actions">
          <button class="btn-icon" title="Configurar">
            <ion-icon name="settings-outline"></ion-icon>
            Configurar
          </button>
          <button class="btn-icon" title="Prueba">
            <ion-icon name="play-outline"></ion-icon>
            Prueba
          </button>
          <button class="btn-icon" title="Más opciones">
            <ion-icon name="ellipsis-vertical"></ion-icon>
          </button>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import FactilizaManager from './FactilizaManager.vue'

const activeTab = ref('todas')

const tabs = ref([
  { id: 'todas', nombre: 'Todas', icono: 'grid-outline' },
  { id: 'factiliza', nombre: 'Factiliza', icono: 'receipt-outline' },
  { id: 'reniec', nombre: 'RENIEC', icono: 'id-card-outline' },
  { id: 'sunat', nombre: 'SUNAT', icono: 'document-outline' }
])

const integraciones = ref([
  {
    id: 1,
    nombre: 'RENIEC',
    tipo: 'reniec',
    icono: 'id-card-outline',
    descripcion: 'Validación de identidad con RENIEC',
    activa: true,
    llamadas: '1,234',
    tasa: 98,
    tiempo: 450
  },
  {
    id: 2,
    nombre: 'Factiliza',
    tipo: 'factiliza',
    icono: 'receipt-outline',
    descripcion: 'Generación de facturas electrónicas',
    activa: true,
    llamadas: '856',
    tasa: 95,
    tiempo: 320
  },
  {
    id: 3,
    nombre: 'SUNAT',
    tipo: 'sunat',
    icono: 'document-outline',
    descripcion: 'Consultas a SUNAT',
    activa: false,
    llamadas: '142',
    tasa: 92,
    tiempo: 580
  },
  {
    id: 4,
    nombre: 'Webhook Personalizado',
    tipo: 'custom',
    icono: 'git-network-outline',
    descripcion: 'Integración personalizada con tu API',
    activa: true,
    llamadas: '2,341',
    tasa: 99,
    tiempo: 280
  }
])
</script>

<style scoped>
.integraciones-container {
  padding: 20px;
}

.view-header {
  margin-bottom: 32px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
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

.btn-primary:hover {
  background: #4338ca;
}

.btn-primary ion-icon {
  font-size: 18px;
}

.integraciones-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.integracion-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.integracion-card:hover {
  border-color: #4f46e5;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.1);
}

.integracion-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 16px;
  position: relative;
}

.integracion-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.integracion-icon.reniec {
  background: #dbeafe;
  color: #0369a1;
}

.integracion-icon.factiliza {
  background: #ddd6fe;
  color: #6d28d9;
}

.integracion-icon.sunat {
  background: #fed7aa;
  color: #b45309;
}

.integracion-icon.custom {
  background: #d1fae5;
  color: #059669;
}

.integracion-title {
  flex: 1;
}

.integracion-title h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 4px 0;
}

.tipo {
  font-size: 12px;
  color: #64748b;
  margin: 0;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 4px;
}

.status-dot.activa {
  background: #10b981;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.5);
}

.status-dot.inactiva {
  background: #ef4444;
}

.descripcion {
  font-size: 13px;
  color: #64748b;
  margin: 0 0 16px 0;
  padding: 12px;
  background: #f8fafc;
  border-radius: 6px;
}

.integracion-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 16px;
  padding: 12px 0;
  border-top: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
}

.stat {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.stat-label {
  display: block;
  font-size: 11px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.integracion-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 12px;
  background: #f1f5f9;
  color: #4f46e5;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-icon:hover {
  background: #e0e7ff;
  border-color: #4f46e5;
}

.btn-icon ion-icon {
  font-size: 16px;
}

.btn-icon:last-child {
  flex: 0;
  width: auto;
}

/* Tab Navigation */
.tabs-navigation {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 0;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 12px 16px;
  background: none;
  border: none;
  color: #64748b;
  font-weight: 600;
  cursor: pointer;
  font-size: 14px;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s;
}

.tab-btn:hover {
  color: #1e293b;
}

.tab-btn.active {
  color: #4f46e5;
  border-bottom-color: #4f46e5;
}

.tab-btn ion-icon {
  font-size: 16px;
}

.tab-content {
  animation: fadeIn 0.2s ease;
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
</style>
