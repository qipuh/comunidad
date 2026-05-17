<template>
  <div class="reportes-container">
    <div class="view-header">
      <h2>Reportes del Sistema</h2>
      <p class="subtitle">Visualiza y descarga reportes de tu sistema</p>
    </div>

    <div class="reportes-grid">
      <div class="reporte-card">
        <div class="reporte-icon usuarios">
          <ion-icon name="people"></ion-icon>
        </div>
        <h3>Reporte de Usuarios</h3>
        <p>Datos generales de los usuarios registrados</p>
        <button class="btn-secondary">
          <ion-icon name="download-outline"></ion-icon>
          Descargar
        </button>
      </div>

      <div class="reporte-card">
        <div class="reporte-icon registros">
          <ion-icon name="document-text"></ion-icon>
        </div>
        <h3>Reporte de Registros</h3>
        <p>Detalle de todos los registros completados</p>
        <button class="btn-secondary">
          <ion-icon name="download-outline"></ion-icon>
          Descargar
        </button>
      </div>

      <div class="reporte-card">
        <div class="reporte-icon actividad">
          <ion-icon name="flash"></ion-icon>
        </div>
        <h3>Reporte de Actividad</h3>
        <p>Registro de acciones y cambios del sistema</p>
        <button class="btn-secondary">
          <ion-icon name="download-outline"></ion-icon>
          Descargar
        </button>
      </div>

      <div class="reporte-card">
        <div class="reporte-icon apis">
          <ion-icon name="server"></ion-icon>
        </div>
        <h3>Reporte de Integraciones</h3>
        <p>Estadísticas de llamadas a APIs externas</p>
        <button class="btn-secondary">
          <ion-icon name="download-outline"></ion-icon>
          Descargar
        </button>
      </div>
    </div>

    <div class="reportes-table-section">
      <h3>Reportes Generados Recientemente</h3>
      <div class="reportes-table">
        <table>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Tipo</th>
              <th>Fecha</th>
              <th>Tamaño</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="reporte in reportesRecientes" :key="reporte.id">
              <td>{{ reporte.nombre }}</td>
              <td>{{ reporte.tipo }}</td>
              <td>{{ reporte.fecha }}</td>
              <td>{{ reporte.tamaño }}</td>
              <td class="actions">
                <button class="btn-icon" title="Descargar">
                  <ion-icon name="download-outline"></ion-icon>
                </button>
                <button class="btn-icon" title="Eliminar">
                  <ion-icon name="trash-outline"></ion-icon>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const reportesRecientes = ref([
  { id: 1, nombre: 'Usuarios_Abril_2026', tipo: 'Usuarios', fecha: '2026-04-25', tamaño: '245 KB' },
  { id: 2, nombre: 'Registros_Completos', tipo: 'Registros', fecha: '2026-04-24', tamaño: '512 KB' },
  { id: 3, nombre: 'Actividad_Semanal', tipo: 'Actividad', fecha: '2026-04-23', tamaño: '128 KB' }
])
</script>

<style scoped>
.reportes-container {
  padding: 0;
}

.view-header {
  margin-bottom: 32px;
}

.view-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.subtitle {
  color: #64748b;
  font-size: 14px;
}

.reportes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.reporte-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  transition: all 0.15s;
}

.reporte-card:hover {
  border-color: #c7d2fe;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.06);
}

.reporte-icon {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  font-size: 28px;
}

.reporte-icon.usuarios {
  background: #dbeafe;
  color: #0369a1;
}

.reporte-icon.registros {
  background: #ddd6fe;
  color: #6d28d9;
}

.reporte-icon.actividad {
  background: #fed7aa;
  color: #b45309;
}

.reporte-icon.apis {
  background: #d1fae5;
  color: #059669;
}

.reporte-card h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.reporte-card p {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 16px;
}

.btn-secondary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 10px 12px;
  background: #f1f5f9;
  color: #4f46e5;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
}

.btn-secondary:hover {
  background: #eef2ff;
  border-color: #6366f1;
}

.btn-secondary ion-icon {
  font-size: 16px;
}

.reportes-table-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e2e8f0;
}

.reportes-table-section h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 20px;
}

.reportes-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

th {
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: #64748b;
  font-size: 13px;
  text-transform: uppercase;
}

td {
  padding: 12px 16px;
  border-bottom: 1px solid #e2e8f0;
  color: #1e293b;
  font-size: 14px;
}

tbody tr:hover {
  background: #f8fafc;
}

.actions {
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
  font-size: 16px;
}
</style>
