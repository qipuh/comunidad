<template>
  <div class="usuarios-container">
    <!-- Vista Lista -->
    <div v-if="!showModal" class="vista-lista">
      <!-- Toolbar -->
      <div class="toolbar">
        <div class="toolbar-left">
          <div class="search-bar">
            <ion-icon name="search-outline"></ion-icon>
            <input v-model="busqueda" type="text" placeholder="Buscar por nombre, DNI o teléfono...">
          </div>
          <div class="filtros-inline">
            <select v-model="filtroEstado" class="filtro-select">
              <option value="">Todos los estados</option>
              <option value="activo">Activo</option>
              <option value="inactivo">Inactivo</option>
              <option value="pendiente">Pendiente</option>
            </select>
            <select v-model="filtroRol" class="filtro-select">
              <option value="">Todos los roles</option>
              <option value="usuario">Usuario</option>
              <option value="admin">Admin</option>
            </select>
            <button v-if="filtroEstado || filtroRol" @click="limpiarFiltros()" class="btn-limpiar-filtros">
              <ion-icon name="close-circle-outline"></ion-icon>
            </button>
          </div>
        </div>
        <div class="toolbar-right">
          <button @click="abrirModalNuevoUsuario" class="btn-primary">
            <ion-icon name="person-add-outline"></ion-icon>
            Nuevo Usuario
          </button>
          <button @click="descargarPlantilla" class="btn-secondary" title="Descargar plantilla de importación">
            <ion-icon name="download-outline"></ion-icon>
            Plantilla
          </button>
          <button @click="$refs.importarArchivo.click()" class="btn-secondary">
            <ion-icon name="cloud-upload-outline"></ion-icon>
            Importar
          </button>
          <input
            ref="importarArchivo"
            type="file"
            accept=".xlsx,.xls"
            @change="manejarImportarExcel"
            style="display: none"
          >
        </div>
      </div>

      <!-- Alert -->
      <div v-if="mensajeAlerta" :class="['alert', tipoAlerta]">
        <ion-icon :name="tipoAlerta === 'success' ? 'checkmark-circle' : 'alert-circle'"></ion-icon>
        <span>{{ mensajeAlerta }}</span>
      </div>

      <!-- Tabla de Usuarios -->
      <div class="tabla-card">
        <div v-if="usuariosFiltrados.length === 0" class="empty-state">
          <ion-icon name="people-outline"></ion-icon>
          <h3>No hay usuarios</h3>
          <p>{{ usuarios.length === 0 ? 'Crea tu primer usuario para comenzar' : 'No coincide con los filtros aplicados' }}</p>
        </div>
        <table v-else>
          <thead>
            <tr>
              <th style="width: 28%;">Nombre</th>
              <th style="width: 12%;">DNI</th>
              <th style="width: 12%;">Teléfono</th>
              <th style="width: 10%;">Rol</th>
              <th style="width: 10%;">Estado</th>
              <th style="width: 12%;">Carnet</th>
              <th style="width: 16%;">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in usuariosFiltrados" :key="user.id" class="tabla-row">
              <td class="nombre-cell">
                <div class="avatar-placeholder">{{ user.nombre_completo.charAt(0).toUpperCase() }}</div>
                <span>{{ user.nombre_completo }}</span>
              </td>
              <td><span class="codigo-badge">{{ user.numero_dni }}</span></td>
              <td>{{ user.telefono || '—' }}</td>
              <td>
                <span :class="['role-badge', user.rol]">
                  {{ user.rol === 'admin' ? 'Administrador' : 'Usuario' }}
                </span>
              </td>
              <td>
                <span :class="['status-badge', user.estado]">{{ user.estado }}</span>
              </td>
              <td class="carnet-cell">
                <router-link :to="`/carnets?usuario=${user.id}`" class="btn-carnet-link" title="Ver carnet del usuario">
                  <ion-icon name="card-outline"></ion-icon>
                  <span class="carnet-numero">{{ numeroCarnet(user) }}</span>
                </router-link>
              </td>
              <td class="actions-cell">
                <div class="actions-buttons">
                  <router-link :to="`/usuarios/${user.id}`" class="btn-action-icon view" title="Ver perfil">
                    <ion-icon name="eye-outline"></ion-icon>
                  </router-link>
                  <button @click="abrirCobranzaSidebar(user)" class="btn-action-icon cobranza" title="Ver cobranza">
                    <ion-icon name="receipt-outline"></ion-icon>
                  </button>
                  <button @click="editarUsuario(user)" class="btn-action-icon edit" title="Editar usuario">
                    <ion-icon name="pencil-outline"></ion-icon>
                  </button>
                  <button @click="confirmarEliminar(user)" class="btn-action-icon delete" title="Eliminar usuario">
                    <ion-icon name="trash-outline"></ion-icon>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Sidebar Cobranza -->
      <div v-if="usuarioCobranzaSeleccionado" class="sidebar-overlay" @click.self="usuarioCobranzaSeleccionado = null">
        <div class="sidebar-content">
          <div class="sidebar-header">
            <div>
              <h3>Cobranza - {{ usuarioCobranzaSeleccionado.nombre_completo }}</h3>
              <p class="sidebar-subtitle">DNI: {{ usuarioCobranzaSeleccionado.numero_dni }}</p>
            </div>
            <button @click="usuarioCobranzaSeleccionado = null" class="btn-close-sidebar">
              <ion-icon name="close-outline"></ion-icon>
            </button>
          </div>

          <div class="sidebar-body">
            <!-- Estadísticas -->
            <div class="stats-grid">
              <div class="stat-card-sidebar">
                <div class="stat-icon">
                  <ion-icon name="receipt-outline"></ion-icon>
                </div>
                <div class="stat-content">
                  <span class="stat-label">Pendientes</span>
                  <span class="stat-number">{{ cuotasPendientes.length }}</span>
                </div>
              </div>
              <div class="stat-card-sidebar">
                <div class="stat-icon alert">
                  <ion-icon name="alert-circle-outline"></ion-icon>
                </div>
                <div class="stat-content">
                  <span class="stat-label">Adeudado</span>
                  <span class="stat-number">{{ formatearMoneda(totalAdeudado) }}</span>
                </div>
              </div>
              <div class="stat-card-sidebar">
                <div class="stat-icon success">
                  <ion-icon name="checkmark-done-outline"></ion-icon>
                </div>
                <div class="stat-content">
                  <span class="stat-label">Pagadas</span>
                  <span class="stat-number">{{ cuotasPagadas.length }}</span>
                </div>
              </div>
            </div>

            <!-- Cuotas Pendientes Section -->
            <div class="cobranza-section">
              <h4>Cuotas Pendientes ({{ cuotasPendientes.length }})</h4>
              <div v-if="cuotasPendientes.length === 0" class="empty-section">
                <ion-icon name="document-outline"></ion-icon>
                <p>Sin cuotas pendientes</p>
              </div>
              <div v-else class="cuotas-list">
                <div v-for="cuota in cuotasPendientes.slice(0, 5)" :key="cuota.id" class="cuota-item">
                  <div class="cuota-header">
                    <span class="cuota-concepto">{{ cuota.concepto }}</span>
                    <span class="cuota-monto">{{ formatearMoneda(cuota.monto) }}</span>
                  </div>
                  <div class="cuota-fecha">Vence: {{ formatarFecha(cuota.fecha_vencimiento) }}</div>
                </div>
              </div>
            </div>

            <!-- Operaciones Aprobadas Section -->
            <div class="cobranza-section">
              <h4>Operaciones Aprobadas ({{ operacionesAprobadas.length }})</h4>
              <div v-if="operacionesAprobadas.length === 0" class="empty-section">
                <ion-icon name="swap-horizontal-outline"></ion-icon>
                <p>Sin operaciones aprobadas</p>
              </div>
              <div v-else class="operaciones-list">
                <div v-for="op in operacionesAprobadas.slice(0, 5)" :key="op.id" class="operacion-item">
                  <div class="op-header">
                    <span class="op-concepto">{{ op.concepto }}</span>
                    <span class="op-monto">{{ formatearMoneda(op.monto) }}</span>
                  </div>
                  <div class="op-detalles">
                    <span :class="['op-metodo', formatoMetodo(op.metodo_pago).clase]">
                      {{ formatoMetodo(op.metodo_pago).nombre }}
                    </span>
                    <span class="op-fecha">{{ formatarFecha(op.fecha_pagada) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
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

      <!-- Modal Previsualización de Importación -->
      <div v-if="mostrarModalPreview" class="modal-overlay-full" @click.self="cerrarPreview">
        <div class="modal-contenedor-preview">
          <div class="modal-header">
            <div>
              <h2>Previsualización de Importación</h2>
              <p class="preview-resumen">
                <span class="badge badge-validos">✅ {{ resumenImport.validos }} válidos</span>
                <span class="badge badge-duplicados">⚠️ {{ resumenImport.duplicados }} duplicados</span>
                <span class="badge badge-errores">❌ {{ resumenImport.errores }} errores</span>
              </p>
            </div>
            <button @click="cerrarPreview" class="btn-close">
              <ion-icon name="close-outline"></ion-icon>
            </button>
          </div>

          <div class="preview-filtros">
            <button
              v-for="filtro in filtrosPreview"
              :key="filtro.estado"
              @click="filtroPreview = filtro.estado"
              :class="['btn-filtro', { activo: filtroPreview === filtro.estado }]"
            >
              {{ filtro.icon }} {{ filtro.label }} ({{ filtro.count }})
            </button>
          </div>

          <div class="modal-body-scroll">
            <!-- Info del filtro actual -->
            <div v-if="filasPreviewFiltradas.length === 0" class="empty-preview">
              <ion-icon name="document-outline"></ion-icon>
              <p>No hay registros {{ filtroPreviewTexto }}</p>
            </div>

            <!-- Tabla de filas -->
            <div v-else class="preview-tabla">
              <table>
                <thead>
                  <tr>
                    <th style="width: 50px;">Fila</th>
                    <th style="width: 60px;">
                      <input
                        type="checkbox"
                        :checked="todosSeleccionados"
                        @change="alternarTodos"
                        :disabled="filasPreviewFiltradas.every(f => f.estado === 'error')"
                        title="Seleccionar/deseleccionar todos"
                      >
                    </th>
                    <th>Padrón</th>
                    <th>Nombre Completo</th>
                    <th>DNI</th>
                    <th>Sexo</th>
                    <th>F. Nacimiento</th>
                    <th>Est. Civil</th>
                    <th style="width: 180px;">Estado</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="fila in filasPreviewFiltradas" :key="fila.fila" :class="['fila-' + fila.estado]">
                    <td class="fila-num">{{ fila.fila }}</td>
                    <td class="checkbox-cell">
                      <input
                        v-if="fila.estado !== 'error'"
                        type="checkbox"
                        :checked="filasSeleccionadas.has(fila.fila)"
                        @change="toggleFila(fila.fila)"
                        :disabled="fila.estado === 'error'"
                      >
                    </td>
                    <td class="num-padron">{{ fila.datos.num_padron || '-' }}</td>
                    <td>{{ [fila.datos.nombres, fila.datos.apellido_paterno, fila.datos.apellido_materno].filter(n => n).join(' ') }}</td>
                    <td class="dni">{{ fila.datos.dni }}</td>
                    <td>{{ fila.datos.sexo || '-' }}</td>
                    <td>{{ fila.datos.fecha_nacimiento || '-' }}</td>
                    <td>{{ fila.datos.estado_civil || '-' }}</td>
                    <td class="estado-cell">
                      <span v-if="fila.estado === 'valido'" class="badge-estado valido">
                        ✅ Nuevo
                      </span>
                      <span v-else-if="fila.estado === 'duplicado'" class="badge-estado duplicado">
                        ⚠️ Actualizar
                      </span>
                      <span v-else class="badge-estado error" :title="fila.motivo">
                        ❌ {{ fila.motivo }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="modal-footer">
            <div class="footer-info">
              <p>{{ filasSeleccionadas.size }} fila(s) seleccionada(s) para importar</p>
            </div>
            <div class="footer-buttons">
              <button @click="cerrarPreview" class="btn-outline">Cancelar</button>
              <button
                @click="mostrarConfirmacion = true"
                class="btn-primary"
                :disabled="filasSeleccionadas.size === 0 || importando"
              >
                <ion-icon name="download-outline"></ion-icon>
                {{ importando ? 'Importando...' : `Importar (${filasSeleccionadas.size})` }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal Confirmación de Importación -->
      <div v-if="mostrarConfirmacion && mostrarModalPreview" class="modal-overlay" @click.self="mostrarConfirmacion = false">
        <div class="modal">
          <div class="modal-header">
            <h3>Confirmar Importación</h3>
          </div>
          <div class="modal-body">
            <p><strong>¿Continuar con la importación?</strong></p>
            <ul class="confirmacion-lista">
              <li v-if="conteoFilasImportacion.nuevos > 0">
                <span class="icon nuevo">+</span>
                <strong>{{ conteoFilasImportacion.nuevos }}</strong> nuevo(s) usuario(s)
              </li>
              <li v-if="conteoFilasImportacion.actualizar > 0">
                <span class="icon actualizar">↻</span>
                <strong>{{ conteoFilasImportacion.actualizar }}</strong> usuario(s) se actualizará(n)
              </li>
            </ul>
            <p class="nota-importante">✓ Los usuarios se crearán con contraseña = DNI</p>
          </div>
          <div class="modal-footer">
            <button @click="mostrarConfirmacion = false" class="btn-outline" :disabled="importando">Cancelar</button>
            <button @click="confirmarImportacion" class="btn-primary" :disabled="importando">
              {{ importando ? 'Importando...' : 'Confirmar Importación' }}
            </button>
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
                <label>Nombres *</label>
                <input v-model="formulario.nombres" type="text" disabled>
              </div>
              <div class="form-group">
                <label>Fecha de Nacimiento</label>
                <input v-model="formulario.fecha_nacimiento" type="text" disabled>
              </div>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label>Apellido Paterno</label>
                <input v-model="formulario.apellido_paterno" type="text" disabled>
              </div>
              <div class="form-group">
                <label>Apellido Materno</label>
                <input v-model="formulario.apellido_materno" type="text" disabled>
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

          <!-- Sección Asignación de Conceptos (solo si rol es usuario) -->
          <div v-if="formulario.rol === 'usuario' || formulario.rol === 'user'" class="seccion">
            <h3>6. Asignación de Conceptos de Pago</h3>
            <p class="texto-ayuda">Asigna los conceptos de pago que aplican a este usuario. Las cuotas se generarán automáticamente desde la fecha de inicio.</p>

            <div class="form-group">
              <label>Fecha de Inicio de Afiliación/Cobranza *</label>
              <input v-model="formulario.fecha_inicio_cobranza" type="date">
              <small class="help-text">Se generarán cuotas desde esta fecha hasta hoy</small>
            </div>

            <!-- Cuotas (se asignan automáticamente) -->
            <div class="conceptos-seccion">
              <h4>Cuotas (Recurrentes)</h4>
              <p class="texto-ayuda-pequeño">Se asignarán automáticamente al usuario</p>
              <div class="conceptos-lista">
                <div v-for="concepto in conceptosCuota" :key="concepto.id" class="concepto-item">
                  <label class="checkbox-concepto">
                    <input type="checkbox" :checked="true" disabled>
                    <div class="concepto-info">
                      <strong>{{ concepto.nombre }}</strong>
                      <span class="concepto-monto">{{ formatearMoneda(concepto.monto) }}</span>
                      <span class="concepto-recurrencia">Cada {{ concepto.recurrencia }}</span>
                    </div>
                  </label>
                </div>
              </div>
            </div>

            <!-- Multas y Derechos (seleccionables) -->
            <div class="conceptos-seccion">
              <h4>Multas y Derechos (Una sola vez)</h4>
              <div v-if="conceptosMulDer.length === 0" class="sin-conceptos">
                <p>No hay conceptos disponibles</p>
              </div>
              <div v-else class="conceptos-lista">
                <div v-for="concepto in conceptosMulDer" :key="concepto.id" class="concepto-item">
                  <label class="checkbox-concepto">
                    <input
                      type="checkbox"
                      :value="concepto.id"
                      v-model="formulario.conceptos_asignados"
                    >
                    <div class="concepto-info">
                      <strong>{{ concepto.nombre }}</strong>
                      <span class="concepto-monto">{{ formatearMoneda(concepto.monto) }}</span>
                      <span class="concepto-tipo">{{ concepto.tipo }}</span>
                    </div>
                  </label>
                </div>
              </div>
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
import * as XLSX from 'xlsx'

const formatearMoneda = (monto) => {
  return new Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN' }).format(monto)
}

const usuarios = ref([])
const busqueda = ref('')
const showModal = ref(false)
const usuarioEditando = ref(null)
const usuarioAEliminar = ref(null)
const usuarioCobranzaSeleccionado = ref(null)
const cuotasCobranza = ref([])
const operacionesCobranza = ref([])
const guardando = ref(false)
const eliminando = ref(false)
const consultandoDNI = ref(false)
const cargando = ref(false)
const datosFactilizaCargados = ref(false)
const mensajeAlerta = ref('')
const tipoAlerta = ref('success')
const mensajeDNI = ref(null)
const conceptos = ref([])
const mostrarModalPreview = ref(false)
const filasPreview = ref([])
const filasSeleccionadas = ref(new Set())
const resumenImport = ref({ validos: 0, duplicados: 0, errores: 0 })
const importando = ref(false)
const filtroEstado = ref('')
const filtroRol = ref('')
const filtroPreview = ref('todos')
const mostrarConfirmacion = ref(false)

const formulario = ref({
  numero_dni: '',
  nombres: '',
  apellido_paterno: '',
  apellido_materno: '',
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
  foto_lateral_der: null,
  fecha_inicio_cobranza: new Date().toISOString().split('T')[0],
  conceptos_asignados: []
})

const previews = ref({
  frontal: null,
  lateral_izq: null,
  lateral_der: null
})

const conceptosCuota = computed(() => {
  return conceptos.value.filter(c => c.tipo === 'cuota')
})

const conceptosMulDer = computed(() => {
  return conceptos.value.filter(c => c.tipo === 'multa' || c.tipo === 'derecho')
})

const usuariosFiltrados = computed(() => {
  return usuarios.value.filter(u => {
    const matchBusqueda = !busqueda.value ||
      u.nombre_completo.toLowerCase().includes(busqueda.value.toLowerCase()) ||
      u.numero_dni.includes(busqueda.value) ||
      (u.telefono && u.telefono.includes(busqueda.value))
    const matchEstado = !filtroEstado.value || u.estado === filtroEstado.value
    const matchRol = !filtroRol.value || u.rol === filtroRol.value
    return matchBusqueda && matchEstado && matchRol
  })
})

const formularioValido = computed(() => {
  if (!datosFactilizaCargados.value) return false
  if (!formulario.value.nombres) return false
  if (!formulario.value.telefono) return false
  if (!usuarioEditando.value && !formulario.value.password && !formulario.value.usar_reconocimiento_facial) return false
  if (!usuarioEditando.value && (!previews.value.frontal || !previews.value.lateral_izq || !previews.value.lateral_der)) return false
  return true
})

const filtrosPreview = computed(() => [
  {
    estado: 'todos',
    label: 'Todos',
    icon: '📋',
    count: filasPreview.value.length
  },
  {
    estado: 'valido',
    label: 'Nuevos',
    icon: '✅',
    count: filasPreview.value.filter(f => f.estado === 'valido').length
  },
  {
    estado: 'duplicado',
    label: 'Actualizar',
    icon: '⚠️',
    count: filasPreview.value.filter(f => f.estado === 'duplicado').length
  },
  {
    estado: 'error',
    label: 'Errores',
    icon: '❌',
    count: filasPreview.value.filter(f => f.estado === 'error').length
  }
])

const filtroPreviewTexto = computed(() => {
  const map = {
    'todos': '',
    'valido': 'válidos',
    'duplicado': 'para actualizar',
    'error': 'con errores'
  }
  return map[filtroPreview.value] || ''
})

const filasPreviewFiltradas = computed(() => {
  if (filtroPreview.value === 'todos') return filasPreview.value
  return filasPreview.value.filter(f => f.estado === filtroPreview.value)
})

const conteoFilasImportacion = computed(() => {
  let nuevos = 0
  let actualizar = 0

  filasSeleccionadas.value.forEach(numFila => {
    const fila = filasPreview.value.find(f => f.fila === numFila)
    if (fila) {
      if (fila.estado === 'valido') nuevos++
      else if (fila.estado === 'duplicado') actualizar++
    }
  })

  return { nuevos, actualizar }
})

const todosSeleccionados = computed(() => {
  if (filasPreviewFiltradas.value.length === 0) return false
  const filasSeleccionables = filasPreviewFiltradas.value.filter(f => f.estado !== 'error')
  return filasSeleccionables.length > 0 && filasSeleccionables.every(f => filasSeleccionadas.value.has(f.fila))
})

const cuotasDelUsuario = computed(() => {
  if (!usuarioCobranzaSeleccionado.value) return []
  return cuotasCobranza.value.filter(c => c.usuario_id === usuarioCobranzaSeleccionado.value.id)
})

const cuotasPendientes = computed(() => {
  return cuotasDelUsuario.value.filter(c => c.estado && c.estado.toLowerCase() === 'pendiente')
})

const cuotasPagadas = computed(() => {
  return cuotasDelUsuario.value.filter(c => c.estado && c.estado.toLowerCase() === 'pagada')
})

const totalAdeudado = computed(() => {
  return cuotasPendientes.value.reduce((sum, c) => sum + (parseFloat(c.monto) || 0), 0)
})

const operacionesDelUsuario = computed(() => {
  if (!usuarioCobranzaSeleccionado.value) return []
  return operacionesCobranza.value.filter(o => o.usuario_id === usuarioCobranzaSeleccionado.value.id)
})

const operacionesAprobadas = computed(() => {
  return operacionesDelUsuario.value.filter(o => o.estado && o.estado.toLowerCase() === 'aprobado')
})

onMounted(async () => {
  await cargarUsuarios()
  await cargarConceptos()
})

const cargarConceptos = async () => {
  try {
    const res = await fetch('/api/cobranza/conceptos/')
    if (!res.ok) {
      console.warn('No se pudieron cargar conceptos de cobranza')
      conceptos.value = []
      return
    }
    const data = await res.json()
    conceptos.value = data.data || []
  } catch (error) {
    // Silencioso - continuar sin conceptos
    conceptos.value = []
  }
}

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

    formulario.value.nombres = datos.nombres || ''
    formulario.value.apellido_paterno = datos.apellido_paterno || ''
    formulario.value.apellido_materno = datos.apellido_materno || ''
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
  formulario.value.nombres = ''
  formulario.value.apellido_paterno = ''
  formulario.value.apellido_materno = ''
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

  // Formatear fecha_inicio_cobranza para el input date
  let fechaInicio = new Date().toISOString().split('T')[0]
  if (usuario.fecha_inicio_cobranza) {
    fechaInicio = usuario.fecha_inicio_cobranza.split('T')[0]
  }

  formulario.value = {
    numero_dni: usuario.numero_dni,
    nombres: usuario.nombres || '',
    apellido_paterno: usuario.apellido_paterno || '',
    apellido_materno: usuario.apellido_materno || '',
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
    fecha_inicio_cobranza: fechaInicio,
    conceptos_asignados: [],
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
    formData.append('nombres', formulario.value.nombres)
    formData.append('apellido_paterno', formulario.value.apellido_paterno)
    formData.append('apellido_materno', formulario.value.apellido_materno)
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

    // Campos de cobranza
    if (formulario.value.fecha_inicio_cobranza) {
      formData.append('fecha_inicio_cobranza', formulario.value.fecha_inicio_cobranza)
    }
    if (formulario.value.conceptos_asignados && formulario.value.conceptos_asignados.length > 0) {
      formData.append('conceptos_asignados', JSON.stringify(formulario.value.conceptos_asignados))
    }

    if (formulario.value.foto_frontal) {
      formData.append('foto_frontal', formulario.value.foto_frontal)
    }
    if (formulario.value.foto_lateral_izq) {
      formData.append('foto_lateral_izq', formulario.value.foto_lateral_izq)
    }
    if (formulario.value.foto_lateral_der) {
      formData.append('foto_lateral_der', formulario.value.foto_lateral_der)
    }

    let usuarioId
    if (usuarioEditando.value) {
      await usuariosService.actualizarUsuario(usuarioEditando.value.id, formData)
      usuarioId = usuarioEditando.value.id
      mensajeAlerta.value = 'Usuario actualizado exitosamente'
    } else {
      const res = await usuariosService.crearUsuario(formData)
      usuarioId = res.data.id
      mensajeAlerta.value = 'Usuario creado exitosamente'
    }

    // Asignar conceptos de cobranza si es usuario
    if (formulario.value.rol === 'usuario' || formulario.value.rol === 'user') {
      try {
        await fetch('/api/cobranza/asignar-conceptos/' + usuarioId, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            fecha_inicio_cobranza: formulario.value.fecha_inicio_cobranza,
            conceptos_multas_derechos: formulario.value.conceptos_asignados || []
          })
        })
      } catch (error) {
        console.error('Error asignando conceptos:', error)
      }
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
    nombres: '',
    apellido_paterno: '',
    apellido_materno: '',
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

const manejarImportarExcel = async (event) => {
  const archivo = event.target.files[0]
  if (!archivo) return

  try {
    const formData = new FormData()
    formData.append('archivo', archivo)

    // Llamar al endpoint de preview
    const respuesta = await fetch('/api/usuarios/preview-excel', {
      method: 'POST',
      body: formData
    })

    const datos = await respuesta.json()

    if (!respuesta.ok) {
      mensajeAlerta.value = datos.detail || 'Error leyendo archivo'
      tipoAlerta.value = 'error'
      event.target.value = ''
      return
    }

    // Cargar preview
    filasPreview.value = datos.filas
    resumenImport.value = datos.resumen

    // Pre-seleccionar todos los válidos
    filasSeleccionadas.value = new Set()
    datos.filas.forEach(fila => {
      if (fila.estado === 'valido') {
        filasSeleccionadas.value.add(fila.fila)
      }
    })

    // Mostrar modal de preview
    mostrarModalPreview.value = true

    // Limpiar input
    event.target.value = ''
  } catch (error) {
    mensajeAlerta.value = 'Error al leer archivo: ' + error.message
    tipoAlerta.value = 'error'
    event.target.value = ''
  }
}

const toggleFila = (numeroFila) => {
  if (filasSeleccionadas.value.has(numeroFila)) {
    filasSeleccionadas.value.delete(numeroFila)
  } else {
    filasSeleccionadas.value.add(numeroFila)
  }
}

const alternarTodos = () => {
  const filasSeleccionables = filasPreviewFiltradas.value.filter(f => f.estado !== 'error')

  if (todosSeleccionados.value) {
    // Deseleccionar todos
    filasSeleccionables.forEach(f => filasSeleccionadas.value.delete(f.fila))
  } else {
    // Seleccionar todos
    filasSeleccionables.forEach(f => filasSeleccionadas.value.add(f.fila))
  }
}

const cerrarPreview = () => {
  mostrarModalPreview.value = false
  mostrarConfirmacion.value = false
  filasPreview.value = []
  filasSeleccionadas.value = new Set()
  filtroPreview.value = 'todos'
}

const confirmarImportacion = async () => {
  if (filasSeleccionadas.value.size === 0) {
    mensajeAlerta.value = 'Selecciona al menos un usuario para importar'
    tipoAlerta.value = 'error'
    return
  }

  importando.value = true
  try {
    // Preparar datos a importar incluyendo flag de actualización
    const usuariosAImportar = filasPreview.value
      .filter(f => filasSeleccionadas.value.has(f.fila))
      .map(f => ({
        ...f.datos,
        actualizar: f.estado === 'duplicado'  // Marcar los duplicados para actualizar
      }))

    console.log('Enviando usuarios a importar:', usuariosAImportar)

    const respuesta = await fetch('/api/usuarios/importar-confirmado', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ usuarios: usuariosAImportar })
    })

    console.log('Respuesta status:', respuesta.status)

    const datos = await respuesta.json()
    console.log('Datos recibidos:', datos)

    if (!respuesta.ok) {
      mensajeAlerta.value = datos.detail || 'Error importando'
      tipoAlerta.value = 'error'
      return
    }

    // Mostrar resultado
    const creados = datos.usuarios_creados ? datos.usuarios_creados.length : 0
    const actualizados = datos.usuarios_actualizados ? datos.usuarios_actualizados.length : 0
    const total = creados + actualizados

    if (total > 0) {
      const mensaje = []
      if (creados > 0) mensaje.push(`${creados} nuevo${creados > 1 ? 's' : ''}`)
      if (actualizados > 0) mensaje.push(`${actualizados} actualizado${actualizados > 1 ? 's' : ''}`)
      mensajeAlerta.value = `✅ Importación exitosa: ${mensaje.join(' + ')} usuario${total > 1 ? 's' : ''}`
      tipoAlerta.value = 'success'
    } else {
      const erroresMsg = datos.errores && datos.errores.length > 0 ? datos.errores[0] : 'desconocido'
      mensajeAlerta.value = `❌ No se importó ningún usuario. Errores: ${erroresMsg}`
      tipoAlerta.value = 'error'
    }

    // Cerrar modales y recargar
    mostrarConfirmacion.value = false
    cerrarPreview()
    await cargarUsuarios()
  } catch (error) {
    console.error('Error en confirmarImportacion:', error)
    mensajeAlerta.value = 'Error al importar: ' + error.message
    tipoAlerta.value = 'error'
  } finally {
    importando.value = false
  }
}

const numeroCarnet = (user) => {
  return String(user.id).padStart(3, '0') + (user.numero_dni || '')
}

const limpiarFiltros = () => {
  filtroEstado.value = ''
  filtroRol.value = ''
}

const descargarPlantilla = async () => {
  try {
    const respuesta = await fetch('/api/usuarios/descargar-plantilla')
    if (!respuesta.ok) {
      mensajeAlerta.value = 'Error descargando plantilla'
      tipoAlerta.value = 'error'
      return
    }

    const blob = await respuesta.blob()
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'plantilla_usuarios.xlsx'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Error descargando plantilla:', error)
    mensajeAlerta.value = 'Error: ' + error.message
    tipoAlerta.value = 'error'
  }
}

const abrirCobranzaSidebar = async (usuario) => {
  console.log('Abriendo cobranza para:', usuario)
  usuarioCobranzaSeleccionado.value = usuario

  try {
    // Cargar cuotas - endpoint toma usuario_id como parámetro de ruta
    console.log('Cargando cuotas desde:', `/api/cobranza/cuotas/${usuario.id}`)
    const resCuotas = await fetch(`/api/cobranza/cuotas/${usuario.id}`)
    console.log('Respuesta cuotas:', resCuotas.status)
    if (resCuotas.ok) {
      const dataCuotas = await resCuotas.json()
      console.log('Cuotas cargadas:', dataCuotas)
      cuotasCobranza.value = dataCuotas.data || []
    } else {
      console.warn('Error en cuotas:', resCuotas.statusText)
    }

    // Cargar operaciones/pagos
    console.log('Cargando pagos...')
    const resOps = await fetch('/api/cobranza/pagos')
    console.log('Respuesta pagos:', resOps.status)
    if (resOps.ok) {
      const dataOps = await resOps.json()
      console.log('Pagos cargados:', dataOps)
      operacionesCobranza.value = (dataOps.data || []).filter(o => o.usuario_id === usuario.id)
    } else {
      console.warn('Error en pagos:', resOps.statusText)
    }
  } catch (error) {
    console.error('Error cargando cobranza:', error)
  }
}

const formatarFecha = (fecha) => {
  if (!fecha) return '—'
  return new Date(fecha).toLocaleDateString('es-PE', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

const formatoMetodo = (metodo) => {
  const mapeo = {
    'efectivo': { nombre: 'Efectivo', clase: 'metodo-efectivo' },
    'transferencia': { nombre: 'Transferencia', clase: 'metodo-transferencia' },
    'deposito': { nombre: 'Depósito', clase: 'metodo-deposito' },
    'billetera': { nombre: 'Billetera', clase: 'metodo-billetera' }
  }
  return mapeo[metodo?.toLowerCase()] || { nombre: metodo, clase: 'metodo-otro' }
}
</script>

<style scoped>
.usuarios-container {
  padding: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.vista-lista {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 0;
}

/* TOOLBAR */
.toolbar {
  display: flex;
  gap: 16px;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

.toolbar-left {
  display: flex;
  gap: 12px;
  align-items: center;
  flex: 1;
  min-width: 300px;
}

.toolbar-right {
  display: flex;
  gap: 8px;
  align-items: center;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
  font-size: 14px;
  white-space: nowrap;
  font-family: inherit;
}

.btn-primary:hover:not(:disabled) {
  background: #4f46e5;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary ion-icon {
  font-size: 18px;
}

.btn-secondary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: white;
  color: #6b7280;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
  white-space: nowrap;
}

.btn-secondary:hover {
  background: #f9fafb;
  border-color: #9ca3af;
  color: #374151;
}

.btn-secondary ion-icon {
  font-size: 18px;
}

/* SEARCH BAR */
.search-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  flex: 1;
  min-width: 250px;
  transition: all 0.2s;
}

.search-bar:focus-within {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.search-bar ion-icon {
  font-size: 18px;
  color: #9ca3af;
}

.search-bar input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  color: #1f2937;
  background: transparent;
}

.search-bar input::placeholder {
  color: #d1d5db;
}

/* FILTROS INLINE */
.filtros-inline {
  display: flex;
  gap: 8px;
  align-items: center;
}

.filtro-select {
  padding: 9px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 13px;
  background: white;
  color: #1f2937;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.filtro-select:hover {
  border-color: #4f46e5;
  background: #f9f5ff;
}

.filtro-select:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.btn-limpiar-filtros {
  padding: 9px 12px;
  background: #f3f4f6;
  color: #6b7280;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
}

.btn-limpiar-filtros:hover {
  background: #ef4444;
  color: white;
}

/* TABLA CARD */
.tabla-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 60px 20px;
  color: #9ca3af;
}

.empty-state ion-icon {
  font-size: 64px;
  color: #d1d5db;
}

.empty-state h3 {
  font-size: 18px;
  font-weight: 600;
  color: #6b7280;
  margin: 0;
}

.empty-state p {
  font-size: 14px;
  color: #9ca3af;
  margin: 0;
}

/* TABLA */
table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

thead {
  background: #f9fafb;
  border-bottom: 2px solid #e5e7eb;
}

th {
  padding: 16px;
  text-align: left;
  font-weight: 600;
  color: #6b7280;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tabla-row {
  border-bottom: 1px solid #f3f4f6;
  transition: background 0.2s;
}

.tabla-row:hover {
  background: #f9fafb;
}

.tabla-row:last-child {
  border-bottom: none;
}

td {
  padding: 16px;
  color: #1f2937;
  font-size: 14px;
  vertical-align: middle;
}

/* NOMBRE CELL */
.nombre-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
  overflow: hidden;
}

.nombre-cell span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.avatar-placeholder {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 13px;
  flex-shrink: 0;
}

.codigo-badge {
  padding: 4px 8px;
  background: #f3f4f6;
  border-radius: 6px;
  font-family: monospace;
  font-weight: 600;
  color: #1f2937;
  font-size: 13px;
}

.role-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
}

.role-badge.admin {
  background: #fef3c7;
  color: #92400e;
}

.role-badge.usuario {
  background: #dbeafe;
  color: #1e40af;
}

.role-badge.editor {
  background: #d1fae5;
  color: #065f46;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
}

.status-badge.activo {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.inactivo {
  background: #fee2e2;
  color: #991b1b;
}

.status-badge.pendiente {
  background: #fef3c7;
  color: #92400e;
}

/* CARNET CELL */
.carnet-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-carnet-link {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #4f46e5;
  text-decoration: none;
  font-size: 12px;
  font-weight: 600;
  padding: 6px 10px;
  border-radius: 6px;
  background: #ede9fe;
  transition: all 0.2s;
  cursor: pointer;
  border: none;
}

.btn-carnet-link:hover {
  background: #ddd6fe;
  color: #4338ca;
}

.btn-carnet-link ion-icon {
  font-size: 16px;
}

.carnet-numero {
  font-family: monospace;
  font-weight: 600;
}

/* ACTIONS CELL */
.actions-cell {
  padding: 12px 16px;
  text-align: center;
  width: 16%;
}

.actions-buttons {
  display: flex;
  gap: 6px;
  align-items: center;
  justify-content: center;
}

.btn-action-icon {
  padding: 8px 10px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  min-width: 36px;
  height: 36px;
  text-decoration: none;
}

.btn-action-icon.view {
  color: #6366f1;
}

.btn-action-icon.view:hover {
  background: #eef2ff;
  color: #4f46e5;
}

.btn-action-icon.edit {
  color: #6366f1;
}

.btn-action-icon.edit:hover {
  background: #eef2ff;
  color: #6366f1;
}

.btn-action-icon.delete {
  color: #ef4444;
}

.btn-action-icon.delete:hover {
  background: #fef2f2;
  color: #dc2626;
}

/* ALERT */
.alert {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 0;
  font-size: 14px;
  font-weight: 500;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    transform: translateY(-10px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.alert.success {
  background: #ecfdf5;
  color: #065f46;
  border-left: 4px solid #10b981;
}

.alert.error {
  background: #fef2f2;
  color: #991b1b;
  border-left: 4px solid #ef4444;
}

.alert ion-icon {
  font-size: 20px;
  flex-shrink: 0;
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
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
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

/* Conceptos de Pago */
.conceptos-seccion {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.conceptos-seccion h4 {
  font-size: 14px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.texto-ayuda-pequeño {
  font-size: 12px;
  color: #94a3b8;
  margin: 0 0 12px 0;
}

.conceptos-lista {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.concepto-item {
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: #fafbfc;
}

.checkbox-concepto {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  cursor: pointer;
}

.checkbox-concepto input {
  margin-top: 4px;
  cursor: pointer;
}

.concepto-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.concepto-info strong {
  font-size: 14px;
  color: #1e293b;
}

.concepto-monto {
  font-size: 13px;
  font-weight: 700;
  color: #4f46e5;
}

.concepto-recurrencia,
.concepto-tipo {
  font-size: 12px;
  color: #64748b;
  text-transform: capitalize;
}

.sin-conceptos {
  padding: 20px;
  text-align: center;
  color: #94a3b8;
  font-size: 13px;
  background: #f8fafc;
  border-radius: 6px;
}

.help-text {
  display: block;
  font-size: 12px;
  color: #94a3b8;
  margin-top: 4px;
}

/* Preview Modal */
.modal-contenedor-preview {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  max-width: 1400px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.preview-resumen {
  display: flex;
  gap: 12px;
  margin-top: 8px;
  font-size: 13px;
  flex-wrap: wrap;
}

.badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 600;
  display: inline-block;
}

.badge-validos {
  background: #dcfce7;
  color: #166534;
}

.badge-duplicados {
  background: #fef3c7;
  color: #92400e;
}

.badge-errores {
  background: #fee2e2;
  color: #991b1b;
}

.preview-tabla {
  width: 100%;
  overflow-x: auto;
}

.preview-tabla table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.preview-tabla thead {
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  z-index: 10;
}

.preview-tabla th {
  padding: 12px;
  text-align: left;
  font-weight: 600;
  color: #64748b;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.preview-tabla td {
  padding: 12px;
  border-bottom: 1px solid #e2e8f0;
  color: #1e293b;
}

.preview-tabla tbody tr:hover {
  background: #f8fafc;
}

.preview-tabla .fila-valido {
  background: #f0fdf4;
}

.preview-tabla .fila-duplicado {
  background: #fffbeb;
}

.preview-tabla .fila-error {
  background: #fef2f2;
}

.preview-tabla .fila-num {
  text-align: center;
  font-weight: 600;
  color: #94a3b8;
}

.preview-tabla .checkbox-cell {
  text-align: center;
  padding: 8px 12px;
}

.preview-tabla .checkbox-cell input {
  cursor: pointer;
  width: 18px;
  height: 18px;
}

.preview-tabla .dni {
  font-family: monospace;
  font-weight: 600;
}

.preview-tabla .estado-cell {
  text-align: center;
}

.badge-estado {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 11px;
  white-space: nowrap;
}

.badge-estado.valido {
  background: #dcfce7;
  color: #166534;
}

.badge-estado.duplicado {
  background: #fef3c7;
  color: #92400e;
  cursor: help;
}

.badge-estado.error {
  background: #fee2e2;
  color: #991b1b;
  cursor: help;
}

/* Preview Filtros */
.preview-filtros {
  padding: 16px 20px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.btn-filtro {
  padding: 8px 14px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-filtro:hover {
  border-color: #cbd5e1;
  background: #f1f5f9;
}

.btn-filtro.activo {
  background: #4f46e5;
  color: white;
  border-color: #4f46e5;
}

/* Empty state en preview */
.empty-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 60px 20px;
  color: #94a3b8;
}

.empty-preview ion-icon {
  font-size: 48px;
  color: #cbd5e1;
}

.empty-preview p {
  margin: 0;
  font-size: 14px;
}

/* Footer mejorado */
.modal-footer {
  padding: 16px 20px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.footer-info {
  flex: 1;
  font-size: 13px;
  color: #64748b;
}

.footer-info p {
  margin: 0;
}

.footer-buttons {
  display: flex;
  gap: 12px;
}

/* Columna num_padron */
.preview-tabla .num-padron {
  font-weight: 600;
  color: #4f46e5;
  font-family: monospace;
}

/* Lista de confirmación */
.confirmacion-lista {
  list-style: none;
  padding: 0;
  margin: 12px 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.confirmacion-lista li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  background: #f8fafc;
  border-radius: 6px;
  font-size: 14px;
}

.confirmacion-lista li strong {
  color: #4f46e5;
  font-size: 16px;
}

.confirmacion-lista .icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 4px;
  font-weight: 700;
  color: white;
  font-size: 12px;
}

.confirmacion-lista .icon.nuevo {
  background: #10b981;
}

.confirmacion-lista .icon.actualizar {
  background: #f59e0b;
}

.nota-importante {
  margin: 12px 0 0 0;
  padding: 8px 12px;
  background: #f0fdf4;
  border-left: 3px solid #10b981;
  color: #166534;
  font-size: 12px;
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

/* SIDEBAR COBRANZA */
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: flex-end;
  z-index: 1002;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { background: rgba(0, 0, 0, 0); }
  to { background: rgba(0, 0, 0, 0.5); }
}

.sidebar-content {
  background: white;
  width: 620px;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.2s ease;
}

@keyframes slideIn {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.sidebar-header h3 {
  margin: 0 0 4px 0;
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
}

.sidebar-subtitle {
  margin: 0;
  font-size: 13px;
  color: #64748b;
}

.btn-close-sidebar {
  background: none;
  border: none;
  cursor: pointer;
  color: #64748b;
  padding: 4px;
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.btn-close-sidebar:hover {
  color: #1e293b;
}

.btn-close-sidebar ion-icon {
  font-size: 20px;
}

.sidebar-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 8px;
}

.stat-card-sidebar {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  text-align: center;
}

.stat-card-sidebar .stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #4f46e5;
}

.stat-card-sidebar .stat-icon.alert {
  color: #f59e0b;
}

.stat-card-sidebar .stat-icon.success {
  color: #10b981;
}

.stat-card-sidebar .stat-label {
  font-size: 11px;
  color: #64748b;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-card-sidebar .stat-number {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
}

.cobranza-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cobranza-section h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 700;
  color: #1e293b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #64748b;
}

.empty-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 32px 20px;
  background: #f8fafc;
  border-radius: 8px;
  color: #94a3b8;
  text-align: center;
}

.empty-section ion-icon {
  font-size: 32px;
  color: #cbd5e1;
}

.empty-section p {
  margin: 0;
  font-size: 13px;
}

/* CUOTAS LIST */
.cuotas-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.cuota-item {
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 10px;
  background: #fafbfc;
  font-size: 13px;
}

.cuota-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 6px;
  gap: 8px;
}

.cuota-concepto {
  font-weight: 600;
  color: #1e293b;
  font-size: 12px;
  flex: 1;
}

.cuota-monto {
  font-weight: 700;
  color: #4f46e5;
  font-size: 12px;
  white-space: nowrap;
}

.cuota-fecha {
  font-size: 11px;
  color: #64748b;
}

.cuota-estado {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  text-transform: capitalize;
}

.cuota-estado.pendiente {
  background: #fef3c7;
  color: #92400e;
}

.cuota-estado.pagada {
  background: #dcfce7;
  color: #166534;
}

.cuota-estado.vencida {
  background: #fee2e2;
  color: #991b1b;
}

.cuota-detalles {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  font-size: 12px;
}

.cuota-dato {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.cuota-dato .label {
  color: #94a3b8;
}

.cuota-dato .valor {
  font-weight: 600;
  color: #1e293b;
}

/* OPERACIONES LIST */
.operaciones-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.operacion-item {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px;
  background: #fafbfc;
}

.op-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.op-concepto {
  font-weight: 600;
  color: #1e293b;
  font-size: 13px;
}

.op-monto {
  font-weight: 700;
  color: #4f46e5;
  font-size: 13px;
}

.op-detalles {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  font-size: 12px;
}

.op-metodo {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 4px;
  font-weight: 600;
  text-transform: capitalize;
  font-size: 11px;
}

.op-metodo.metodo-efectivo {
  background: #d1fae5;
  color: #065f46;
}

.op-metodo.metodo-transferencia {
  background: #bfdbfe;
  color: #1e40af;
}

.op-metodo.metodo-deposito {
  background: #fbcfe8;
  color: #831843;
}

.op-metodo.metodo-billetera {
  background: #d8b4fe;
  color: #581c87;
}

.op-metodo.metodo-otro {
  background: #f3f4f6;
  color: #6b7280;
}

.op-fecha {
  color: #94a3b8;
  font-size: 12px;
}

.btn-action-icon.cobranza {
  color: #8b5cf6;
}

.btn-action-icon.cobranza:hover {
  background: #f3e8ff;
  color: #7c3aed;
}

@media (max-width: 1024px) {
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .toolbar-left {
    flex-direction: column;
  }

  .toolbar-right {
    width: 100%;
    justify-content: stretch;
  }

  .toolbar-right button {
    flex: 1;
  }
}

@media (max-width: 768px) {
  .vista-lista {
    padding: 16px;
  }

  .toolbar {
    flex-direction: column;
  }

  .toolbar-left {
    width: 100%;
  }

  .search-bar {
    width: 100%;
  }

  .filtros-inline {
    width: 100%;
  }

  .filtro-select {
    flex: 1;
  }

  .toolbar-right {
    width: 100%;
  }

  .toolbar-right button {
    flex: 1;
  }

  /* Tabla: scroll horizontal */
  .tabla-card {
    overflow-x: auto;
  }

  table {
    min-width: 600px;
  }

  th, td {
    padding: 12px 8px;
    font-size: 13px;
  }

  .nombre-cell {
    gap: 8px;
  }

  .avatar-placeholder {
    width: 32px;
    height: 32px;
    font-size: 12px;
  }

  .btn-carnet-link {
    flex-direction: column;
    gap: 4px;
  }

  .carnet-numero {
    display: none;
  }

  /* Modal ocupa toda la pantalla */
  .modal-overlay-full {
    padding: 0;
    align-items: flex-end;
  }

  .modal-contenedor {
    max-width: 100%;
    border-radius: 16px 16px 0 0;
    max-height: 95vh;
  }

  /* Grids del formulario en 1 columna */
  .fotos-grid,
  .grid-2,
  .grid-3 {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .vista-lista {
    padding: 12px;
    gap: 12px;
  }

  .toolbar-left {
    flex-direction: column;
  }

  .search-bar {
    padding: 8px 12px;
  }

  .btn-primary,
  .btn-secondary {
    padding: 8px 12px;
    font-size: 13px;
  }

  th, td {
    padding: 8px 4px;
    font-size: 12px;
  }

  .actions-cell {
    gap: 4px;
  }

  .btn-action-icon {
    padding: 6px 8px;
    font-size: 14px;
    min-width: 32px;
    height: 32px;
  }
}

@media (max-width: 480px) {
  th, td { padding: 8px 10px; font-size: 12px; }
  .modal-header { padding: 14px 16px; }
  .modal-body-scroll { padding: 14px 16px; }
  .seccion { margin-bottom: 20px; padding-bottom: 20px; }

  .sidebar-content {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .sidebar-content {
    width: 100%;
    max-width: 420px;
  }
}
</style>
