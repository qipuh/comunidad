<template>
  <div class="usuarios-container">
    <!-- Vista Lista -->
    <div v-if="!showModal" class="vista-lista">
      <div class="view-header">
        <div class="header-content">
          <h2>Gestión de Usuarios</h2>
          <button @click="abrirModalNuevoUsuario" class="btn-primary">
            <ion-icon name="add-circle-outline"></ion-icon>
            Nuevo Usuario
          </button>
        </div>

        <div class="search-bar">
          <ion-icon name="search-outline"></ion-icon>
          <input v-model="busqueda" type="text" placeholder="Buscar usuarios...">
        </div>
      </div>

      <!-- Alert -->
      <div v-if="mensajeAlerta" :class="['alert', tipoAlerta]">
        <ion-icon :name="tipoAlerta === 'success' ? 'checkmark-circle' : 'alert-circle'"></ion-icon>
        {{ mensajeAlerta }}
      </div>

      <!-- Tabla de Usuarios -->
      <div class="usuarios-table">
        <table>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>DNI</th>
              <th>Teléfono</th>
              <th>Rol</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="usuarios.length === 0">
              <td colspan="6" class="sin-datos">No hay usuarios registrados</td>
            </tr>
            <tr v-for="user in usuariosFiltrados" :key="user.id">
              <td>{{ user.nombre_completo }}</td>
              <td>{{ user.numero_dni }}</td>
              <td>{{ user.telefono }}</td>
              <td>{{ user.rol }}</td>
              <td>
                <span :class="['status-badge', user.estado]">{{ user.estado }}</span>
              </td>
              <td class="actions">
                <button @click="editarUsuario(user)" class="btn-icon" title="Editar">
                  <ion-icon name="create-outline"></ion-icon>
                </button>
                <button @click="confirmarEliminar(user)" class="btn-icon" title="Eliminar">
                  <ion-icon name="trash-outline"></ion-icon>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Modal Confirmación Eliminar -->
      <div v-if="usuarioAEliminar" class="modal-overlay" @click.self="usuarioAEliminar = null">
        <div class="modal">
          <div class="modal-header">
            <h3>Confirmar eliminación</h3>
          </div>
          <div class="modal-body">
            <p>¿Estás seguro de que deseas eliminar a {{ usuarioAEliminar.nombre_completo }}?</p>
            <p class="texto-alerta">Esta acción no se puede deshacer.</p>
          </div>
          <div class="modal-footer">
            <button @click="eliminarUsuario" class="btn-danger" :disabled="eliminando">
              {{ eliminando ? 'Eliminando...' : 'Eliminar' }}
            </button>
            <button @click="usuarioAEliminar = null" class="btn-outline">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Vista Modal Crear/Editar Usuario -->
    <div v-if="showModal" class="modal-overlay-full">
      <div class="modal-contenedor">
        <div class="modal-header">
          <h2>{{ usuarioEditando ? 'Editar Usuario' : 'Crear Nuevo Usuario' }}</h2>
          <button @click="cerrarModal" class="btn-close">
            <ion-icon name="close-outline"></ion-icon>
          </button>
        </div>

        <div class="modal-body-scroll">
          <!-- Sección 1: Consulta DNI -->
          <div v-if="!datosFactilizaCargados" class="seccion">
            <h3>1. Consultar Datos Personales</h3>
            <p class="texto-ayuda">Ingresa el DNI para traer los datos de la persona</p>

            <div class="form-group">
              <label>Número de DNI *</label>
              <div class="input-grupo">
                <input
                  v-model="formulario.numero_dni"
                  type="text"
                  placeholder="12345678"
                  maxlength="8"
                  @keyup.enter="consultarDNI"
                  :disabled="consultandoDNI"
                >
                <button @click="consultarDNI" class="btn-consultadni" :disabled="!formulario.numero_dni || consultandoDNI">
                  <ion-icon name="search-outline"></ion-icon>
                  {{ consultandoDNI ? 'Consultando...' : 'Consultar' }}
                </button>
              </div>
              <div v-if="mensajeDNI" :class="['mensaje', mensajeDNI.tipo]">
                {{ mensajeDNI.texto }}
              </div>
            </div>
          </div>

          <!-- Sección 2: Datos Personales (Traídos de Factiliza) -->
          <div v-if="datosFactilizaCargados" class="seccion">
            <h3>2. Datos Personales</h3>

            <div class="grid-2">
              <div class="form-group">
                <label>Nombre Completo *</label>
                <input v-model="formulario.nombre_completo" type="text" disabled>
              </div>
              <div class="form-group">
                <label>Fecha de Nacimiento</label>
                <input v-model="formulario.fecha_nacimiento" type="text" disabled>
              </div>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label>Sexo</label>
                <input v-model="formulario.sexo" type="text" disabled>
              </div>
              <div class="form-group">
                <label>Estado Civil</label>
                <input v-model="formulario.estado_civil" type="text" disabled>
              </div>
            </div>

            <div class="form-group">
              <label>Dirección</label>
              <input v-model="formulario.direccion" type="text" disabled>
            </div>

            <div class="grid-3">
              <div class="form-group">
                <label>Departamento</label>
                <input v-model="formulario.departamento" type="text" disabled>
              </div>
              <div class="form-group">
                <label>Provincia</label>
                <input v-model="formulario.provincia" type="text" disabled>
              </div>
              <div class="form-group">
                <label>Distrito</label>
                <input v-model="formulario.distrito" type="text" disabled>
              </div>
            </div>

            <button @click="limpiarDatos" class="btn-cambiar-dni">
              <ion-icon name="refresh-outline"></ion-icon>
              Cambiar DNI
            </button>
          </div>

          <!-- Sección 3: Contacto -->
          <div v-if="datosFactilizaCargados" class="seccion">
            <h3>3. Información de Contacto</h3>

            <div class="form-group">
              <label>Teléfono/Celular *</label>
              <input v-model="formulario.telefono" type="tel" placeholder="987654321">
            </div>
          </div>

          <!-- Sección 4: Fotos para Reconocimiento Facial -->
          <div v-if="datosFactilizaCargados" class="seccion">
            <h3>4. Fotos para Reconocimiento Facial</h3>
            <p class="texto-ayuda">Sube 3 fotos: frontal, lateral izquierda y lateral derecha</p>

            <div class="fotos-grid">
              <!-- Foto Frontal -->
              <div class="foto-item">
                <label>Foto Frontal *</label>
                <div class="foto-box" @click="$refs.fotoFrontal.click()">
                  <img v-if="previews.frontal" :src="previews.frontal" alt="Frontal">
                  <div v-else class="foto-placeholder">
                    <ion-icon name="camera-outline"></ion-icon>
                    <p>Frontal</p>
                  </div>
                  <input
                    ref="fotoFrontal"
                    type="file"
                    accept="image/*"
                    @change="cargarFoto($event, 'frontal')"
                    style="display: none"
                  >
                </div>
              </div>

              <!-- Foto Lateral Izquierda -->
              <div class="foto-item">
                <label>Lateral Izquierda *</label>
                <div class="foto-box" @click="$refs.fotoLateralIzq.click()">
                  <img v-if="previews.lateral_izq" :src="previews.lateral_izq" alt="Lateral Izquierda">
                  <div v-else class="foto-placeholder">
                    <ion-icon name="camera-outline"></ion-icon>
                    <p>Lat. Izq.</p>
                  </div>
                  <input
                    ref="fotoLateralIzq"
                    type="file"
                    accept="image/*"
                    @change="cargarFoto($event, 'lateral_izq')"
                    style="display: none"
                  >
                </div>
              </div>

              <!-- Foto Lateral Derecha -->
              <div class="foto-item">
                <label>Lateral Derecha *</label>
                <div class="foto-box" @click="$refs.fotoLateralDer.click()">
                  <img v-if="previews.lateral_der" :src="previews.lateral_der" alt="Lateral Derecha">
                  <div v-else class="foto-placeholder">
                    <ion-icon name="camera-outline"></ion-icon>
                    <p>Lat. Der.</p>
                  </div>
                  <input
                    ref="fotoLateralDer"
                    type="file"
                    accept="image/*"
                    @change="cargarFoto($event, 'lateral_der')"
                    style="display: none"
                  >
                </div>
              </div>
            </div>
          </div>

          <!-- Sección 5: Credenciales de Acceso -->
          <div v-if="datosFactilizaCargados" class="seccion">
            <h3>5. Credenciales de Acceso</h3>
            <p class="texto-ayuda">El DNI será el usuario. Elige contraseña o usa reconocimiento facial</p>

            <div class="form-group">
              <label>Usuario (DNI)</label>
              <input v-model="formulario.numero_dni" type="text" disabled style="background: #f0f0f0;">
            </div>

            <div v-if="!usuarioEditando" class="form-group">
              <label>Contraseña *</label>
              <input v-model="formulario.password" type="password" placeholder="••••••••">
            </div>

            <div class="form-group">
              <label>
                <input v-model="formulario.usar_reconocimiento_facial" type="checkbox">
                Usar reconocimiento facial para acceder
              </label>
            </div>

            <div class="form-group">
              <label>Rol</label>
              <select v-model="formulario.rol">
                <option value="usuario">Usuario</option>
                <option value="editor">Editor</option>
                <option value="admin">Administrador</option>
              </select>
            </div>

            <div v-if="usuarioEditando" class="form-group">
              <label>Estado</label>
              <select v-model="formulario.estado">
                <option value="activo">Activo</option>
                <option value="inactivo">Inactivo</option>
              </select>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="cerrarModal" class="btn-outline">Cancelar</button>
          <button
            @click="guardarUsuario"
            class="btn-primary"
            :disabled="guardando || !formularioValido"
          >
            <ion-icon name="checkmark-outline"></ion-icon>
            {{ guardando ? 'Guardando...' : 'Guardar Usuario' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import usuariosService from '@/services/usuarios.service'
import factilizaService from '@/services/factiliza.service'

const usuarios = ref([])
const busqueda = ref('')
const showModal = ref(false)
const usuarioEditando = ref(null)
const usuarioAEliminar = ref(null)
const guardando = ref(false)
const eliminando = ref(false)
const consultandoDNI = ref(false)
const cargando = ref(false)
const datosFactilizaCargados = ref(false)
const mensajeAlerta = ref('')
const tipoAlerta = ref('success')
const mensajeDNI = ref(null)

const formulario = ref({
  numero_dni: '',
  nombre_completo: '',
  fecha_nacimiento: '',
  sexo: '',
  estado_civil: '',
  direccion: '',
  departamento: '',
  provincia: '',
  distrito: '',
  telefono: '',
  password: '',
  rol: 'usuario',
  estado: 'activo',
  usar_reconocimiento_facial: false,
  foto_frontal: null,
  foto_lateral_izq: null,
  foto_lateral_der: null
})

const previews = ref({
  frontal: null,
  lateral_izq: null,
  lateral_der: null
})

const usuariosFiltrados = computed(() => {
  if (!busqueda.value) return usuarios.value
  return usuarios.value.filter(u =>
    u.nombre_completo.toLowerCase().includes(busqueda.value.toLowerCase()) ||
    u.numero_dni.includes(busqueda.value) ||
    (u.telefono && u.telefono.includes(busqueda.value))
  )
})

const formularioValido = computed(() => {
  if (!datosFactilizaCargados.value) return false
  if (!formulario.value.nombre_completo) return false
  if (!formulario.value.telefono) return false
  if (!usuarioEditando.value && !formulario.value.password && !formulario.value.usar_reconocimiento_facial) return false
  if (!usuarioEditando.value && (!previews.value.frontal || !previews.value.lateral_izq || !previews.value.lateral_der)) return false
  return true
})

onMounted(async () => {
  await cargarUsuarios()
})

const cargarUsuarios = async () => {
  cargando.value = true
  try {
    const result = await usuariosService.listarUsuarios(100, 0)
    usuarios.value = result.data || []
  } catch (error) {
    mensajeAlerta.value = 'Error cargando usuarios'
    tipoAlerta.value = 'error'
  } finally {
    cargando.value = false
  }
}

const consultarDNI = async () => {
  if (!formulario.value.numero_dni || formulario.value.numero_dni.length !== 8) {
    mensajeDNI.value = { tipo: 'error', texto: 'Ingresa un DNI válido (8 dígitos)' }
    return
  }

  consultandoDNI.value = true
  mensajeDNI.value = null
  try {
    const respuesta = await factilizaService.consultarDNI(formulario.value.numero_dni)

    if (!respuesta.success) {
      mensajeDNI.value = { tipo: 'error', texto: respuesta.message || 'Error consultando DNI' }
      return
    }

    const datos = respuesta.data

    formulario.value.nombre_completo = datos.nombre_completo || ''
    formulario.value.fecha_nacimiento = datos.fecha_nacimiento || ''
    formulario.value.sexo = datos.sexo || ''
    formulario.value.estado_civil = datos.estado_civil || ''
    formulario.value.direccion = datos.direccion || ''
    formulario.value.departamento = datos.departamento || ''
    formulario.value.provincia = datos.provincia || ''
    formulario.value.distrito = datos.distrito || ''

    datosFactilizaCargados.value = true
    mensajeDNI.value = { tipo: 'success', texto: 'Datos cargados correctamente' }
  } catch (error) {
    mensajeDNI.value = { tipo: 'error', texto: 'Error consultando DNI: ' + (error.response?.data?.message || error.message) }
  } finally {
    consultandoDNI.value = false
  }
}

const cargarFoto = (event, tipo) => {
  const file = event.target.files[0]
  if (file) {
    formulario.value[`foto_${tipo}`] = file
    const reader = new FileReader()
    reader.onload = (e) => {
      previews.value[tipo] = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const limpiarDatos = () => {
  formulario.value.numero_dni = ''
  formulario.value.nombre_completo = ''
  formulario.value.fecha_nacimiento = ''
  formulario.value.sexo = ''
  formulario.value.estado_civil = ''
  formulario.value.direccion = ''
  formulario.value.departamento = ''
  formulario.value.provincia = ''
  formulario.value.distrito = ''
  datosFactilizaCargados.value = false
  mensajeDNI.value = null
}

const abrirModalNuevoUsuario = () => {
  resetFormulario()
  usuarioEditando.value = null
  showModal.value = true
}

const editarUsuario = (usuario) => {
  usuarioEditando.value = usuario
  formulario.value = {
    numero_dni: usuario.numero_dni,
    nombre_completo: usuario.nombre_completo,
    fecha_nacimiento: usuario.fecha_nacimiento || '',
    sexo: usuario.sexo || '',
    estado_civil: usuario.estado_civil || '',
    direccion: usuario.direccion || '',
    departamento: usuario.departamento || '',
    provincia: usuario.provincia || '',
    distrito: usuario.distrito || '',
    telefono: usuario.telefono || '',
    password: '',
    rol: usuario.rol,
    estado: usuario.estado,
    usar_reconocimiento_facial: usuario.usar_reconocimiento_facial || false,
    foto_frontal: null,
    foto_lateral_izq: null,
    foto_lateral_der: null
  }
  // Mostrar fotos existentes como previews
  const fotoUrl = (path) => {
    if (!path) return null
    // path puede ser "uploads/usuarios/archivo.jpg" o absoluto
    const parte = path.replace(/\\/g, '/').split('uploads/').pop()
    return `/uploads/${parte}`
  }
  previews.value = {
    frontal: fotoUrl(usuario.foto_frontal),
    lateral_izq: fotoUrl(usuario.foto_lateral_izq),
    lateral_der: fotoUrl(usuario.foto_lateral_der),
  }
  datosFactilizaCargados.value = true
  showModal.value = true
}

const guardarUsuario = async () => {
  if (!formularioValido.value) {
    mensajeAlerta.value = 'Por favor completa todos los campos requeridos'
    tipoAlerta.value = 'error'
    return
  }

  guardando.value = true
  try {
    const formData = new FormData()
    formData.append('numero_dni', formulario.value.numero_dni)
    formData.append('nombre_completo', formulario.value.nombre_completo)
    formData.append('fecha_nacimiento', formulario.value.fecha_nacimiento)
    formData.append('sexo', formulario.value.sexo)
    formData.append('estado_civil', formulario.value.estado_civil)
    formData.append('direccion', formulario.value.direccion)
    formData.append('departamento', formulario.value.departamento)
    formData.append('provincia', formulario.value.provincia)
    formData.append('distrito', formulario.value.distrito)
    formData.append('telefono', formulario.value.telefono)
    formData.append('username', formulario.value.numero_dni)
    formData.append('password', formulario.value.password)
    formData.append('rol', formulario.value.rol)
    formData.append('estado', formulario.value.estado)
    formData.append('usar_reconocimiento_facial', formulario.value.usar_reconocimiento_facial ? 'true' : 'false')

    if (formulario.value.foto_frontal) {
      formData.append('foto_frontal', formulario.value.foto_frontal)
    }
    if (formulario.value.foto_lateral_izq) {
      formData.append('foto_lateral_izq', formulario.value.foto_lateral_izq)
    }
    if (formulario.value.foto_lateral_der) {
      formData.append('foto_lateral_der', formulario.value.foto_lateral_der)
    }

    if (usuarioEditando.value) {
      await usuariosService.actualizarUsuario(usuarioEditando.value.id, formData)
      mensajeAlerta.value = 'Usuario actualizado exitosamente'
    } else {
      await usuariosService.crearUsuario(formData)
      mensajeAlerta.value = 'Usuario creado exitosamente'
    }

    tipoAlerta.value = 'success'
    cerrarModal()
    await cargarUsuarios()
  } catch (error) {
    mensajeAlerta.value = error.response?.data?.detail || 'Error guardando usuario'
    tipoAlerta.value = 'error'
  } finally {
    guardando.value = false
  }
}

const confirmarEliminar = (usuario) => {
  usuarioAEliminar.value = usuario
}

const eliminarUsuario = async () => {
  if (!usuarioAEliminar.value) return

  eliminando.value = true
  try {
    await usuariosService.eliminarUsuario(usuarioAEliminar.value.id)
    mensajeAlerta.value = 'Usuario eliminado exitosamente'
    tipoAlerta.value = 'success'
    usuarioAEliminar.value = null
    await cargarUsuarios()
  } catch (error) {
    mensajeAlerta.value = 'Error eliminando usuario'
    tipoAlerta.value = 'error'
  } finally {
    eliminando.value = false
  }
}

const cerrarModal = () => {
  showModal.value = false
  resetFormulario()
}

const resetFormulario = () => {
  formulario.value = {
    numero_dni: '',
    nombre_completo: '',
    fecha_nacimiento: '',
    sexo: '',
    estado_civil: '',
    direccion: '',
    departamento: '',
    provincia: '',
    distrito: '',
    telefono: '',
    password: '',
    rol: 'usuario',
    estado: 'activo',
    usar_reconocimiento_facial: false,
    foto_frontal: null,
    foto_lateral_izq: null,
    foto_lateral_der: null
  }
  previews.value = {
    frontal: null,
    lateral_izq: null,
    lateral_der: null
  }
  datosFactilizaCargados.value = false
  mensajeDNI.value = null
}
</script>

<style scoped>
.usuarios-container {
  padding: 20px;
}

.vista-lista {
  /* estilos para tabla */
}

/* HEADER */
.view-header {
  margin-bottom: 32px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
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
  font-size: 14px;
}

.btn-primary:hover:not(:disabled) {
  background: #4338ca;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary ion-icon {
  font-size: 18px;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  max-width: 300px;
}

.search-bar ion-icon {
  font-size: 18px;
  color: #64748b;
}

.search-bar input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  color: #1e293b;
}

/* ALERT */
.alert {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 6px;
  margin-bottom: 20px;
  font-size: 14px;
  font-weight: 500;
}

.alert.success {
  background: #dcfce7;
  color: #166534;
}

.alert.error {
  background: #fee2e2;
  color: #991b1b;
}

/* TABLA */
.usuarios-table {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
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
  padding: 16px;
  text-align: left;
  font-weight: 600;
  color: #64748b;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

td {
  padding: 16px;
  border-bottom: 1px solid #e2e8f0;
  color: #1e293b;
  font-size: 14px;
}

tbody tr:hover {
  background: #f8fafc;
}

.sin-datos {
  text-align: center;
  color: #94a3b8;
  font-style: italic;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
}

.status-badge.activo {
  background: #dcfce7;
  color: #166534;
}

.status-badge.inactivo {
  background: #fee2e2;
  color: #991b1b;
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
  font-size: 18px;
}

/* MODAL */
.modal-overlay-full {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-contenedor {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.15);
  max-width: 700px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h2 {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  color: #64748b;
  padding: 4px;
  display: flex;
  align-items: center;
}

.btn-close:hover {
  color: #1e293b;
}

.btn-close ion-icon {
  font-size: 20px;
}

.modal-body-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.seccion {
  margin-bottom: 32px;
  padding-bottom: 32px;
  border-bottom: 1px solid #e2e8f0;
}

.seccion:last-child {
  border-bottom: none;
}

.seccion h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.texto-ayuda {
  color: #64748b;
  font-size: 13px;
  margin: 0 0 16px 0;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #1e293b;
  font-size: 14px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  color: #1e293b;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.form-group input:disabled {
  background: #f8fafc;
  cursor: not-allowed;
}

.input-grupo {
  display: flex;
  gap: 8px;
}

.input-grupo input {
  flex: 1;
}

.btn-consultadni {
  padding: 10px 16px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
}

.btn-consultadni:hover:not(:disabled) {
  background: #4338ca;
}

.btn-consultadni:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-consultadni ion-icon {
  font-size: 16px;
}

.mensaje {
  font-size: 13px;
  padding: 8px;
  border-radius: 4px;
  margin-top: 8px;
}

.mensaje.success {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #86efac;
}

.mensaje.error {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fca5a5;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.btn-cambiar-dni {
  padding: 10px 16px;
  background: #f1f5f9;
  color: #4f46e5;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.btn-cambiar-dni:hover {
  background: #e0e7ff;
  border-color: #4f46e5;
}

.btn-cambiar-dni ion-icon {
  font-size: 16px;
}

/* FOTOS */
.fotos-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.foto-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.foto-item label {
  font-weight: 600;
  color: #1e293b;
  font-size: 14px;
}

.foto-box {
  border: 2px dashed #e2e8f0;
  border-radius: 8px;
  width: 100%;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  background: #f8fafc;
  overflow: hidden;
}

.foto-box:hover {
  border-color: #4f46e5;
  background: #f0f4ff;
}

.foto-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.foto-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #64748b;
}

.foto-placeholder ion-icon {
  font-size: 40px;
}

.foto-placeholder p {
  margin: 0;
  font-size: 12px;
  font-weight: 600;
}

/* MODAL FOOTER */
.modal-footer {
  padding: 20px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-outline {
  padding: 10px 16px;
  background: white;
  color: #64748b;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.btn-outline:hover {
  border-color: #64748b;
  color: #1e293b;
}

.btn-danger {
  padding: 10px 16px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.btn-danger:hover:not(:disabled) {
  background: #dc2626;
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.texto-alerta {
  color: #991b1b;
  font-size: 13px;
  margin-top: 8px;
}

/* Modal confirmación eliminar */
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
  z-index: 1001;
}

.modal {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.15);
  max-width: 400px;
  width: 90%;
}

@media (max-width: 768px) {
  /* Header */
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  .header-content h2 { font-size: 18px; }
  .btn-primary { width: 100%; justify-content: center; }
  .search-bar { max-width: 100%; }

  /* Tabla: scroll horizontal */
  .usuarios-table {
    overflow-x: auto;
  }
  table { min-width: 520px; }
  th, td { padding: 10px 12px; font-size: 13px; }

  /* Modal ocupa toda la pantalla */
  .modal-overlay-full { padding: 0; align-items: flex-end; }
  .modal-contenedor {
    max-width: 100%;
    border-radius: 16px 16px 0 0;
    max-height: 95vh;
  }

  /* Grids del formulario en 1 columna */
  .fotos-grid,
  .grid-2,
  .grid-3 { grid-template-columns: 1fr; }
}

@media (max-width: 480px) {
  th, td { padding: 8px 10px; font-size: 12px; }
  .modal-header { padding: 14px 16px; }
  .modal-body-scroll { padding: 14px 16px; }
  .seccion { margin-bottom: 20px; padding-bottom: 20px; }
}
</style>
