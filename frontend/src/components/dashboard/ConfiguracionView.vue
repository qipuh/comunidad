<template>
  <div class="configuracion-container">
    <div class="view-header">
      <div class="header-content">
        <h2>Configuración de Campos</h2>
        <button class="btn-primary">
          <ion-icon name="add-circle-outline"></ion-icon>
          Nuevo Campo
        </button>
      </div>
    </div>

    <div class="campos-grid">
      <div v-for="campo in campos" :key="campo.id" class="campo-card">
        <div class="campo-header">
          <h3>{{ campo.nombre }}</h3>
          <div class="campo-actions">
            <button class="btn-icon" title="Editar">
              <ion-icon name="create-outline"></ion-icon>
            </button>
            <button class="btn-icon" title="Eliminar">
              <ion-icon name="trash-outline"></ion-icon>
            </button>
          </div>
        </div>

        <div class="campo-info">
          <p><strong>Tipo:</strong> {{ campo.tipo }}</p>
          <p><strong>Obligatorio:</strong> {{ campo.obligatorio ? 'Sí' : 'No' }}</p>
          <p><strong>Descripción:</strong> {{ campo.descripcion }}</p>
        </div>

        <div class="campo-footer">
          <span class="badge" :class="campo.estado">{{ campo.estado }}</span>
          <span class="campo-date">{{ campo.creado }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const campos = ref([
  {
    id: 1,
    nombre: 'Nombre Completo',
    tipo: 'Texto',
    obligatorio: true,
    descripcion: 'Campo para el nombre completo del usuario',
    estado: 'Activo',
    creado: '2026-04-20'
  },
  {
    id: 2,
    nombre: 'Email',
    tipo: 'Email',
    obligatorio: true,
    descripcion: 'Campo para el email del usuario',
    estado: 'Activo',
    creado: '2026-04-20'
  },
  {
    id: 3,
    nombre: 'Teléfono',
    tipo: 'Teléfono',
    obligatorio: false,
    descripcion: 'Número de contacto',
    estado: 'Activo',
    creado: '2026-04-21'
  }
])
</script>

<style scoped>
.configuracion-container {
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

.campos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.campo-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.campo-card:hover {
  border-color: #4f46e5;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.1);
}

.campo-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 16px;
}

.campo-header h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.campo-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  transition: color 0.2s;
}

.btn-icon:hover {
  color: #4f46e5;
}

.btn-icon ion-icon {
  font-size: 18px;
}

.campo-info {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.campo-info p {
  margin: 8px 0;
  font-size: 13px;
  color: #64748b;
}

.campo-info strong {
  color: #1e293b;
}

.campo-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.badge.Activo {
  background: #dcfce7;
  color: #166534;
}

.campo-date {
  font-size: 12px;
  color: #94a3b8;
}
</style>
