<template>
  <div class="panel-usuario">

    <!-- Perfil -->
    <div class="perfil-card">
      <div class="perfil-avatar">
        <img v-if="usuario.foto_frontal" :src="usuario.foto_frontal" alt="Foto" class="avatar-img">
        <div v-else class="avatar-placeholder">{{ iniciales }}</div>
      </div>
      <div class="perfil-info">
        <h2>{{ usuario.nombre_completo }}</h2>
        <p class="perfil-dni"><ion-icon name="id-card-outline"></ion-icon> DNI: {{ usuario.numero_dni }}</p>
        <p v-if="usuario.anexo" class="perfil-anexo"><ion-icon name="location-outline"></ion-icon> {{ usuario.anexo }}</p>
        <span class="perfil-badge">Comunero</span>
      </div>
      <div class="perfil-datos-extra">
        <div class="dato-item" v-if="datosCompletos?.estado_civil">
          <span class="dato-label">Estado Civil</span>
          <span class="dato-valor">{{ datosCompletos.estado_civil }}</span>
        </div>
        <div class="dato-item" v-if="datosCompletos?.fecha_nacimiento">
          <span class="dato-label">F. Nacimiento</span>
          <span class="dato-valor">{{ datosCompletos.fecha_nacimiento }}</span>
        </div>
        <div class="dato-item" v-if="datosCompletos?.num_padron">
          <span class="dato-label">N° Padrón</span>
          <span class="dato-valor">{{ datosCompletos.num_padron }}</span>
        </div>
        <div class="dato-item" v-if="datosCompletos?.telefono">
          <span class="dato-label">Teléfono</span>
          <span class="dato-valor">{{ datosCompletos.telefono }}</span>
        </div>
      </div>
    </div>

    <div class="panel-grid">

      <!-- Mis Reuniones -->
      <div class="seccion-card">
        <div class="seccion-header">
          <ion-icon name="calendar-outline"></ion-icon>
          <h3>Mis Reuniones</h3>
        </div>
        <div v-if="cargandoReuniones" class="estado-carga">Cargando...</div>
        <div v-else-if="reuniones.length === 0" class="estado-vacio">
          <ion-icon name="calendar-clear-outline"></ion-icon>
          <p>Sin reuniones registradas</p>
        </div>
        <div v-else class="lista-items">
          <div v-for="r in reuniones" :key="r.id" class="item-reunion">
            <div class="item-icono" :class="estadoClase(r.estado)">
              <ion-icon :name="estadoIcono(r.estado)"></ion-icon>
            </div>
            <div class="item-cuerpo">
              <span class="item-titulo">{{ r.titulo }}</span>
              <span class="item-fecha">{{ formatFecha(r.fecha) }}</span>
              <span class="item-lugar" v-if="r.lugar">{{ r.lugar }}</span>
            </div>
            <span :class="['item-badge', estadoClase(r.estado)]">{{ r.estado }}</span>
          </div>
        </div>
      </div>

      <!-- Mis Elecciones -->
      <div class="seccion-card">
        <div class="seccion-header">
          <ion-icon name="podium-outline"></ion-icon>
          <h3>Mis Elecciones</h3>
        </div>
        <div v-if="cargandoElecciones" class="estado-carga">Cargando...</div>
        <div v-else-if="elecciones.length === 0" class="estado-vacio">
          <ion-icon name="podium-outline"></ion-icon>
          <p>Sin elecciones disponibles</p>
        </div>
        <div v-else class="lista-items">
          <div v-for="e in elecciones" :key="e.id" class="item-eleccion">
            <div class="item-icono" :class="e.estado === 'activa' ? 'activa' : 'inactiva'">
              <ion-icon :name="e.estado === 'activa' ? 'radio-button-on-outline' : 'radio-button-off-outline'"></ion-icon>
            </div>
            <div class="item-cuerpo">
              <span class="item-titulo">{{ e.titulo }}</span>
              <span class="item-fecha">{{ formatFecha(e.fecha_inicio) }} — {{ formatFecha(e.fecha_fin) }}</span>
            </div>
            <div class="item-accion">
              <span v-if="e.ya_voto" class="badge-voto votado">
                <ion-icon name="checkmark-circle-outline"></ion-icon> Votado
              </span>
              <router-link v-else-if="e.estado === 'activa'" :to="`/votacion`" class="btn-votar">
                Votar
              </router-link>
              <span v-else class="badge-voto pendiente">{{ e.estado }}</span>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import authService from '@/services/auth.service'

const usuario = authService.obtenerUsuario() || {}
const datosCompletos = ref(null)
const reuniones = ref([])
const elecciones = ref([])
const cargandoReuniones = ref(true)
const cargandoElecciones = ref(true)

const iniciales = computed(() => {
  const nombre = usuario.nombre_completo || ''
  return nombre.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase()
})

const formatFecha = (f) => {
  if (!f) return '—'
  return new Date(f).toLocaleDateString('es-PE', { day: '2-digit', month: 'short', year: 'numeric' })
}

const estadoClase = (estado) => {
  const map = { programada: 'programada', realizada: 'realizada', cancelada: 'cancelada' }
  return map[estado?.toLowerCase()] || 'programada'
}

const estadoIcono = (estado) => {
  const map = { programada: 'time-outline', realizada: 'checkmark-circle-outline', cancelada: 'close-circle-outline' }
  return map[estado?.toLowerCase()] || 'time-outline'
}

onMounted(async () => {
  // Cargar datos completos del usuario
  try {
    const res = await fetch(`/api/usuarios/${usuario.id}`)
    if (res.ok) {
      const data = await res.json()
      datosCompletos.value = data.data
    }
  } catch {}

  // Cargar reuniones
  try {
    const res = await fetch('/api/reuniones/')
    if (res.ok) {
      const data = await res.json()
      reuniones.value = (data.data || data || []).slice(0, 10)
    }
  } catch {} finally {
    cargandoReuniones.value = false
  }

  // Cargar elecciones
  try {
    const res = await fetch('/api/elecciones/')
    if (res.ok) {
      const data = await res.json()
      const lista = data.data || data || []
      // Marcar si el usuario ya votó
      elecciones.value = await Promise.all(lista.slice(0, 10).map(async (el) => {
        try {
          const vRes = await fetch(`/api/elecciones/${el.id}/mi-voto?usuario_id=${usuario.id}`)
          const vData = vRes.ok ? await vRes.json() : {}
          return { ...el, ya_voto: vData.ya_voto || false }
        } catch {
          return { ...el, ya_voto: false }
        }
      }))
    }
  } catch {} finally {
    cargandoElecciones.value = false
  }
})
</script>

<style scoped>
.panel-usuario {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* PERFIL */
.perfil-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}

.perfil-avatar {
  flex-shrink: 0;
}

.avatar-img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #e0e7ff;
}

.avatar-placeholder {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
}

.perfil-info {
  flex: 1;
  min-width: 200px;
}

.perfil-info h2 {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 6px;
}

.perfil-dni, .perfil-anexo {
  font-size: 14px;
  color: #64748b;
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 3px 0;
}

.perfil-badge {
  display: inline-block;
  margin-top: 8px;
  padding: 3px 12px;
  background: #e0e7ff;
  color: #4338ca;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.perfil-datos-extra {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.dato-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.dato-label {
  font-size: 11px;
  color: #94a3b8;
  font-weight: 600;
  text-transform: uppercase;
}

.dato-valor {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

/* GRID */
.panel-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

@media (max-width: 768px) {
  .panel-grid { grid-template-columns: 1fr; }
}

/* SECCIONES */
.seccion-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.seccion-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f1f5f9;
}

.seccion-header ion-icon {
  font-size: 20px;
  color: #6366f1;
}

.seccion-header h3 {
  font-size: 15px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.estado-carga, .estado-vacio {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 30px 0;
  color: #94a3b8;
  font-size: 13px;
}

.estado-vacio ion-icon { font-size: 32px; }

.lista-items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.item-reunion, .item-eleccion {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #f1f5f9;
}

.item-icono {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.item-icono.programada { background: #e0f2fe; color: #0284c7; }
.item-icono.realizada  { background: #dcfce7; color: #16a34a; }
.item-icono.cancelada  { background: #fee2e2; color: #dc2626; }
.item-icono.activa     { background: #dcfce7; color: #16a34a; }
.item-icono.inactiva   { background: #f1f5f9; color: #94a3b8; }

.item-cuerpo {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.item-titulo {
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-fecha {
  font-size: 11px;
  color: #64748b;
}

.item-lugar {
  font-size: 11px;
  color: #94a3b8;
}

.item-badge {
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: capitalize;
  flex-shrink: 0;
}

.item-badge.programada { background: #e0f2fe; color: #0284c7; }
.item-badge.realizada  { background: #dcfce7; color: #16a34a; }
.item-badge.cancelada  { background: #fee2e2; color: #dc2626; }

.item-accion { flex-shrink: 0; }

.badge-voto {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
}

.badge-voto.votado   { background: #dcfce7; color: #16a34a; }
.badge-voto.pendiente { background: #f1f5f9; color: #64748b; }

.btn-votar {
  padding: 5px 14px;
  background: #6366f1;
  color: white;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.15s;
}

.btn-votar:hover { background: #4f46e5; }
</style>
