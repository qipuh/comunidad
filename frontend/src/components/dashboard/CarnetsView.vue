<template>
  <div class="carnets-container">
    <!-- Toolbar -->
    <div class="carnet-toolbar">
      <button class="btn-config" @click="mostrarConfigModal = true">
        <ion-icon name="settings-outline"></ion-icon>
        Configurar carnet
      </button>
      <button class="btn-exportar-todos" @click="mostrarModalBloques = true">
        <ion-icon name="download-outline"></ion-icon>
        Exportar por bloques (PDF)
      </button>
      <button class="btn-vincular-fotos" @click="mostrarModalVincularFotos = true">
        <ion-icon name="image-outline"></ion-icon>
        Vincular Fotos
      </button>
    </div>

    <!-- Modal de Progreso de Exportación -->
    <div v-if="mostrarModalProgreso" class="modal-overlay modal-overlay-progress">
      <div class="modal-progreso">
        <div class="modal-header-progreso">
          <h2>Generando PDF...</h2>
        </div>

        <div class="modal-body-progreso">
          <div class="progreso-info">
            <p v-if="tareaActual" class="total-carnets">
              {{ tareaActual.totalCarnets }} carnet(s)
            </p>
            <p class="mensaje-progreso">{{ mensajeProgreso }}</p>
          </div>

          <div class="progreso-container">
            <div class="progreso-barra">
              <div class="progreso-fill" :style="{ width: progreso + '%' }"></div>
            </div>
            <div class="progreso-porcentaje">{{ progreso }}%</div>
          </div>

          <div class="progreso-detalles">
            <p v-if="tareaActual && tareaActual.inicio">
              Tiempo: {{ Math.floor((new Date() - tareaActual.inicio) / 1000) }}s
            </p>
          </div>
        </div>

        <div class="modal-footer-progreso">
          <button class="btn-outline" @click="cancelarExportacion">Cancelar</button>
        </div>
      </div>
    </div>

    <!-- Modal de Bloques -->
    <div v-if="mostrarModalBloques" class="modal-overlay" @click.self="mostrarModalBloques = false">
      <div class="modal-bloques">
        <div class="modal-header">
          <h2>Descargar Carnets por Bloques</h2>
          <button class="btn-close" @click="mostrarModalBloques = false">&times;</button>
        </div>

        <div class="modal-body-bloques">
          <p class="info-bloques">
            Total de usuarios: <strong>{{ usuarios?.length || 0 }}</strong>
          </p>

          <div class="selector-tamano">
            <label class="selector-label">Tamaño de bloque:</label>
            <div class="selector-botones">
              <button
                v-for="opcion in [50, 100, 200]"
                :key="opcion"
                class="btn-tamano"
                :class="{ activo: tamanoBloque === opcion }"
                @click="tamanoBloque = opcion"
                :disabled="cargando"
              >
                {{ opcion }}
              </button>
              <button
                class="btn-tamano btn-tamano-todos"
                :class="{ activo: tamanoBloque === 'todos' }"
                @click="tamanoBloque = 'todos'"
                :disabled="cargando"
              >
                TODOS ({{ usuarios?.length || 0 }})
              </button>
            </div>
          </div>

          <div v-if="tamanoBloque !== 'todos'" class="bloques-section">
            <p class="info-bloques">
              {{ totalBloques }} bloque(s) de {{ tamanoBloque }} carnets
            </p>
            <div class="grid-bloques">
              <button
                v-for="bloque in totalBloques"
                :key="bloque"
                class="btn-bloque"
                @click="exportarBloqueePDF(bloque)"
                :disabled="cargando"
              >
                <div class="numero-bloque">Bloque {{ bloque }}</div>
                <div class="rango-bloque">
                  {{ (bloque - 1) * tamanoBloque + 1 }} - {{ Math.min(bloque * tamanoBloque, usuarios?.length || 0) }}
                </div>
                <ion-icon name="download-outline"></ion-icon>
              </button>
            </div>
          </div>

          <button
            v-if="tamanoBloque === 'todos'"
            class="btn-todos-pdf"
            @click="exportarTodosPDF"
            :disabled="cargando"
          >
            <ion-icon name="cloud-download-outline"></ion-icon>
            Descargar TODOS en un solo PDF ({{ usuarios?.length || 0 }} carnets)
          </button>

          <div class="nota-bloques">
            PDF vectorial de alta calidad generado en el servidor (Chromium headless).
            El servidor tarda ~1-2s por carnet.
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Configuración -->
    <div v-if="mostrarConfigModal" class="modal-overlay" @click.self="mostrarConfigModal = false">
      <div class="modal-config-advanced">
        <div class="modal-header">
          <h2>Configurar Carnet</h2>
          <button class="btn-close" @click="mostrarConfigModal = false">&times;</button>
        </div>

        <div class="modal-body-advanced">
          <!-- Panel Izquierdo: Formulario -->
          <div class="config-panel-form">
            <!-- Textos -->
            <div class="config-section">
              <h3><ion-icon name="document-text-outline"></ion-icon> Textos del Carnet</h3>
              <div class="form-group">
                <label>Nombre Comunidad:</label>
                <input v-model="configCarnet.nombre_comunidad" type="text" class="form-input">
              </div>
              <div class="form-group">
                <label>Subtítulo:</label>
                <input v-model="configCarnet.subtitulo" type="text" class="form-input">
              </div>
              <div class="form-group">
                <label>Resolución:</label>
                <input v-model="configCarnet.resolucion" type="text" class="form-input">
              </div>
              <div class="form-group">
                <label>Nombre Corto (Siglas):</label>
                <input v-model="configCarnet.nombre_corto" type="text" class="form-input" placeholder="CC.TPCT">
              </div>
              <div class="form-group">
                <label>URL QR (para reverso):</label>
                <input v-model="configCarnet.url_qr" type="text" class="form-input" placeholder="https://ejemplo.com">
              </div>
            </div>

            <!-- Imágenes -->
            <div class="config-section">
              <h3><ion-icon name="images-outline"></ion-icon> Imágenes del Carnet</h3>
              <div class="imagenes-grid">
                <!-- Bandera Anverso -->
                <div
                  class="imagen-dropzone"
                  @click="clickInputBandera"
                  @dragover.prevent="dragOverItem = 'bandera'"
                  @dragleave.prevent="dragOverItem = null"
                  @drop.prevent="(e) => handleDrop(e, 'bandera')"
                  :class="{ 'drag-over': dragOverItem === 'bandera' }"
                >
                  <div class="dropzone-label">Bandera/Logo Anverso</div>
                  <div class="dropzone-content">
                    <div v-if="configCarnet.bandera_url" class="imagen-preview-grande">
                      <img :src="configCarnet.bandera_url" alt="Bandera">
                    </div>
                    <div v-else class="dropzone-placeholder">
                      <ion-icon name="cloud-upload-outline" class="dropzone-icon"></ion-icon>
                      <div class="dropzone-text">Arrastra aquí o haz clic</div>
                    </div>
                  </div>
                  <input
                    id="input-bandera"
                    type="file"
                    @change="e => cargarImagen(e, 'bandera')"
                    accept="image/*"
                    class="file-input-hidden"
                  >
                </div>

                <!-- Escudo Reverso -->
                <div
                  class="imagen-dropzone"
                  @click="clickInputEscudo"
                  @dragover.prevent="dragOverItem = 'escudo'"
                  @dragleave.prevent="dragOverItem = null"
                  @drop.prevent="(e) => handleDrop(e, 'escudo')"
                  :class="{ 'drag-over': dragOverItem === 'escudo' }"
                >
                  <div class="dropzone-label">Escudo Reverso</div>
                  <div class="dropzone-content">
                    <div v-if="configCarnet.escudo_url" class="imagen-preview-grande">
                      <img :src="configCarnet.escudo_url" alt="Escudo">
                    </div>
                    <div v-else class="dropzone-placeholder">
                      <ion-icon name="cloud-upload-outline" class="dropzone-icon"></ion-icon>
                      <div class="dropzone-text">Arrastra aquí o haz clic</div>
                    </div>
                  </div>
                  <input
                    id="input-escudo"
                    type="file"
                    @change="e => cargarImagen(e, 'escudo')"
                    accept="image/*"
                    class="file-input-hidden"
                  >
                </div>

                <!-- Fondo Anverso -->
                <div
                  class="imagen-dropzone"
                  @click="clickInputFondoAnverso"
                  @dragover.prevent="dragOverItem = 'fondo_anverso'"
                  @dragleave.prevent="dragOverItem = null"
                  @drop.prevent="(e) => handleDrop(e, 'fondo_anverso')"
                  :class="{ 'drag-over': dragOverItem === 'fondo_anverso' }"
                >
                  <div class="dropzone-label">Fondo Anverso</div>
                  <div class="dropzone-content">
                    <div v-if="configCarnet.fondo_anverso_url" class="imagen-preview-grande">
                      <img :src="configCarnet.fondo_anverso_url" alt="Fondo Anverso">
                    </div>
                    <div v-else class="dropzone-placeholder">
                      <ion-icon name="cloud-upload-outline" class="dropzone-icon"></ion-icon>
                      <div class="dropzone-text">Arrastra aquí o haz clic</div>
                    </div>
                  </div>
                  <input
                    id="input-fondo-anverso"
                    type="file"
                    @change="e => cargarImagen(e, 'fondo_anverso')"
                    accept="image/*"
                    class="file-input-hidden"
                  >
                </div>

                <!-- Fondo Reverso -->
                <div
                  class="imagen-dropzone"
                  @click="clickInputFondoReverso"
                  @dragover.prevent="dragOverItem = 'fondo_reverso'"
                  @dragleave.prevent="dragOverItem = null"
                  @drop.prevent="(e) => handleDrop(e, 'fondo_reverso')"
                  :class="{ 'drag-over': dragOverItem === 'fondo_reverso' }"
                >
                  <div class="dropzone-label">Fondo Reverso</div>
                  <div class="dropzone-content">
                    <div v-if="configCarnet.fondo_reverso_url" class="imagen-preview-grande">
                      <img :src="configCarnet.fondo_reverso_url" alt="Fondo Reverso">
                    </div>
                    <div v-else class="dropzone-placeholder">
                      <ion-icon name="cloud-upload-outline" class="dropzone-icon"></ion-icon>
                      <div class="dropzone-text">Arrastra aquí o haz clic</div>
                    </div>
                  </div>
                  <input
                    id="input-fondo-reverso"
                    type="file"
                    @change="e => cargarImagen(e, 'fondo_reverso')"
                    accept="image/*"
                    class="file-input-hidden"
                  >
                </div>

                <!-- Firma Secretario -->
                <div
                  class="imagen-dropzone"
                  @click="clickInputFirmaSecretario"
                  @dragover.prevent="dragOverItem = 'firma_secretario'"
                  @dragleave.prevent="dragOverItem = null"
                  @drop.prevent="(e) => handleDrop(e, 'firma_secretario')"
                  :class="{ 'drag-over': dragOverItem === 'firma_secretario' }"
                >
                  <div class="dropzone-label">Firma Secretario</div>
                  <div class="dropzone-content">
                    <div v-if="configCarnet.firma_secretario_url" class="imagen-preview-grande">
                      <img :src="configCarnet.firma_secretario_url" alt="Firma Secretario">
                    </div>
                    <div v-else class="dropzone-placeholder">
                      <ion-icon name="cloud-upload-outline" class="dropzone-icon"></ion-icon>
                      <div class="dropzone-text">Arrastra aquí o haz clic</div>
                    </div>
                  </div>
                  <input
                    id="input-firma-secretario"
                    type="file"
                    @change="e => cargarImagen(e, 'firma_secretario')"
                    accept="image/*"
                    class="file-input-hidden"
                  >
                </div>

                <!-- Firma Presidente -->
                <div
                  class="imagen-dropzone"
                  @click="clickInputFirmaPresidente"
                  @dragover.prevent="dragOverItem = 'firma_presidente'"
                  @dragleave.prevent="dragOverItem = null"
                  @drop.prevent="(e) => handleDrop(e, 'firma_presidente')"
                  :class="{ 'drag-over': dragOverItem === 'firma_presidente' }"
                >
                  <div class="dropzone-label">Firma Presidente</div>
                  <div class="dropzone-content">
                    <div v-if="configCarnet.firma_presidente_url" class="imagen-preview-grande">
                      <img :src="configCarnet.firma_presidente_url" alt="Firma Presidente">
                    </div>
                    <div v-else class="dropzone-placeholder">
                      <ion-icon name="cloud-upload-outline" class="dropzone-icon"></ion-icon>
                      <div class="dropzone-text">Arrastra aquí o haz clic</div>
                    </div>
                  </div>
                  <input
                    id="input-firma-presidente"
                    type="file"
                    @change="e => cargarImagen(e, 'firma_presidente')"
                    accept="image/*"
                    class="file-input-hidden"
                  >
                </div>
              </div>
            </div>
          </div>

          <!-- Panel Derecho: Previsualización -->
          <div class="config-panel-preview">
            <h3><ion-icon name="eye-outline"></ion-icon> Previsualización en Vivo</h3>
            <div class="preview-carnet-container">
              <div class="carnet-container-mini">
                <!-- ANVERSO mini -->
                <div class="lado-izquierdo-mini">
                  <div class="header-izquierdo-mini">
                    <div class="bandera-placeholder-mini">
                      <img v-if="configCarnet.bandera_url" :src="configCarnet.bandera_url" class="bandera-img-mini">
                    </div>
                    <div class="titulo-mini">
                      <div class="titulo-principal-mini">{{ configCarnet.nombre_comunidad }}</div>
                      <div class="titulo-subtitulo-mini">{{ configCarnet.resolucion }}</div>
                    </div>
                  </div>
                </div>

                <!-- REVERSO mini -->
                <div class="lado-derecho-mini">
                  <div class="siglas-mini">{{ configCarnet.nombre_corto }}</div>
                  <div class="escudo-placeholder-mini">
                    <img v-if="configCarnet.escudo_url" :src="configCarnet.escudo_url" class="escudo-img-mini">
                    <span v-else>[Escudo]</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-secondary" @click="mostrarConfigModal = false">Cancelar</button>
          <button class="btn-primary" @click="guardarConfiguracion">Guardar Cambios</button>
        </div>
      </div>
    </div>

    <!-- Modal Vincular Fotos -->
    <div v-if="mostrarModalVincularFotos" class="modal-overlay" @click.self="mostrarModalVincularFotos = false">
      <div class="modal-vincular-fotos">
        <div class="modal-header">
          <h2>Vincular Fotos</h2>
          <button class="btn-close" @click="cerrarModalVincularFotos">&times;</button>
        </div>

        <div class="modal-body-vincular">
          <div v-if="!resultadoVincularFotos" class="content-vincular">
            <!-- Tabs -->
            <div class="tabs-vincular">
              <button
                :class="['tab-button', { active: tabVincular === 'vincular' }]"
                @click="tabVincular = 'vincular'"
              >
                <ion-icon name="folder-outline"></ion-icon>
                Vincular Existentes
              </button>
              <button
                :class="['tab-button', { active: tabVincular === 'cargar' }]"
                @click="tabVincular = 'cargar'"
              >
                <ion-icon name="cloud-upload-outline"></ion-icon>
                Cargar Fotos
              </button>
            </div>

            <!-- Tab 1: Vincular -->
            <div v-if="tabVincular === 'vincular'" class="tab-content">
              <p class="info-vincular">
                <ion-icon name="image-outline" class="icon-grande"></ion-icon>
              </p>
              <h3>¿Vincular fotos a usuarios?</h3>
              <p class="descripcion-vincular">
                Se buscarán todas las fotos en <code>uploads/usuarios/</code> nombradas por DNI (ej: 12345678.png)
                y se vincularán automáticamente a los usuarios correspondientes.
              </p>
              <div class="info-extensiones">
                <strong>Extensiones soportadas:</strong> PNG, JPG, JPEG, WebP
              </div>
              <div class="modal-footer">
                <button class="btn-outline" @click="cerrarModalVincularFotos" :disabled="vinculandoFotos">
                  Cancelar
                </button>
                <button class="btn-primary" @click="ejecutarVincularFotos" :disabled="vinculandoFotos">
                  <ion-icon v-if="!vinculandoFotos" name="image-outline"></ion-icon>
                  <span v-if="vinculandoFotos">Vinculando...</span>
                  <span v-else>Vincular Fotos</span>
                </button>
              </div>
            </div>

            <!-- Tab 2: Cargar Fotos -->
            <div v-else class="tab-content">
              <div
                class="drag-drop-area"
                @dragover.prevent="dragOverArea = true"
                @dragleave.prevent="dragOverArea = false"
                @drop.prevent="manejarDropFotos"
                :class="{ 'drag-over': dragOverArea }"
              >
                <div class="drag-drop-content">
                  <ion-icon name="cloud-upload-outline" class="drag-icon"></ion-icon>
                  <h3>Arrastra fotos aquí</h3>
                  <p>o haz clic para seleccionar</p>
                  <p class="drag-info">Nombra las fotos con el DNI del usuario (ej: 12345678.png)</p>
                </div>
                <input
                  ref="inputFotosCargar"
                  type="file"
                  multiple
                  accept="image/*"
                  @change="manejarSeleccionFotos"
                  style="display: none"
                >
              </div>

              <!-- Vista previa de fotos a cargar -->
              <div v-if="fotosACargar.length > 0" class="preview-fotos-cargar">
                <h4>Fotos a cargar ({{ fotosACargar.length }})</h4>
                <div class="fotos-preview-grid">
                  <div v-for="(foto, idx) in fotosACargar" :key="idx" class="foto-preview-item">
                    <img :src="foto.preview" :alt="foto.nombre" class="foto-thumb">
                    <div class="foto-info">
                      <div class="foto-nombre">{{ foto.nombre }}</div>
                      <div class="foto-tamaño">{{ formatarTamaño(foto.archivo.size) }}</div>
                    </div>
                    <button class="btn-remove-foto" @click="eliminarFotoCargar(idx)">
                      <ion-icon name="close-outline"></ion-icon>
                    </button>
                  </div>
                </div>
              </div>

              <div class="modal-footer">
                <button class="btn-outline" @click="cerrarModalVincularFotos" :disabled="cargandoFotos">
                  Cancelar
                </button>
                <button
                  class="btn-secondary"
                  @click="$refs.inputFotosCargar.click()"
                  :disabled="cargandoFotos"
                >
                  <ion-icon name="add-outline"></ion-icon>
                  Seleccionar más
                </button>
                <button
                  class="btn-primary"
                  @click="enviarFotos"
                  :disabled="fotosACargar.length === 0 || cargandoFotos"
                >
                  <ion-icon v-if="!cargandoFotos" name="cloud-upload-outline"></ion-icon>
                  <span v-if="cargandoFotos">Cargando...</span>
                  <span v-else>Cargar {{ fotosACargar.length }} foto(s)</span>
                </button>
              </div>
            </div>
          </div>

          <div v-else class="resultado-vincular">
            <div class="resumen-resultado">
              <h3>Resultados</h3>
              <div class="stats-grid-vincular">
                <div class="stat-card-vincular" :class="{ success: resultadoVincularFotos.resumen.vinculados > 0 }">
                  <div class="stat-icon">✅</div>
                  <div class="stat-content">
                    <div class="stat-label">Vinculadas</div>
                    <div class="stat-number">{{ resultadoVincularFotos.resumen.vinculados }}</div>
                  </div>
                </div>
                <div class="stat-card-vincular" :class="{ warning: resultadoVincularFotos.resumen.ya_vinculados > 0 }">
                  <div class="stat-icon">⏭️</div>
                  <div class="stat-content">
                    <div class="stat-label">Ya tenían foto</div>
                    <div class="stat-number">{{ resultadoVincularFotos.resumen.ya_vinculados }}</div>
                  </div>
                </div>
                <div class="stat-card-vincular" :class="{ info: resultadoVincularFotos.resumen.no_encontrados > 0 }">
                  <div class="stat-icon">⚠️</div>
                  <div class="stat-content">
                    <div class="stat-label">No encontrados</div>
                    <div class="stat-number">{{ resultadoVincularFotos.resumen.no_encontrados }}</div>
                  </div>
                </div>
                <div class="stat-card-vincular" :class="{ error: resultadoVincularFotos.resumen.errores > 0 }">
                  <div class="stat-icon">❌</div>
                  <div class="stat-content">
                    <div class="stat-label">Errores</div>
                    <div class="stat-number">{{ resultadoVincularFotos.resumen.errores }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="detalles-vincular" v-if="resultadoVincularFotos.detalles?.length > 0">
              <h4>Detalles:</h4>
              <div class="detalles-lista">
                <div v-for="detalle in resultadoVincularFotos.detalles" :key="detalle.dni" :class="['detalle-item', detalle.estado]">
                  <span class="detalle-dni">{{ detalle.dni }}</span>
                  <span class="detalle-nombre">{{ detalle.nombre || '—' }}</span>
                  <span class="detalle-estado">{{ detalle.mensaje }}</span>
                </div>
              </div>
            </div>

            <div class="modal-footer">
              <button class="btn-primary" @click="cerrarModalVincularFotos">Cerrar</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Vista Individual -->
    <div class="carnet-individual-container">
      <div class="usuarios-panel">
        <div class="search-box">
          <ion-icon name="search-outline"></ion-icon>
          <input v-model="busqueda" type="text" placeholder="Buscar usuario..." class="search-input">
        </div>
        <div class="usuarios-list">
          <button
            v-for="usuario in usuariosFiltrados"
            :key="usuario.id"
            class="usuario-item"
            :class="{ active: usuarioSeleccionado?.id === usuario.id }"
            @click="usuarioSeleccionado = usuario"
          >
            <div v-if="usuario.foto_frontal" class="usuario-avatar">
              <img :src="usuario.foto_frontal" :alt="usuario.nombre_completo" class="avatar-img">
            </div>
            <div v-else class="usuario-avatar avatar-placeholder">
              {{ usuario.nombre_completo?.charAt(0) || '?' }}
            </div>
            <div class="usuario-info">
              <div class="usuario-nombre">{{ usuario.nombre_completo }}</div>
              <div class="usuario-dni">DNI: {{ usuario.numero_dni }}</div>
            </div>
          </button>
        </div>
      </div>

      <div class="carnet-panel" v-if="usuarioSeleccionado">
        <div class="carnet-completo-viewport" :id="`carnet-completo-${usuarioSeleccionado.id}`">
          <div class="carnet-container">
            <!-- LADO IZQUIERDO (ANVERSO) -->
            <div class="lado-izquierdo" :style="{ backgroundImage: configCarnet.fondo_anverso_url ? `url(${configCarnet.fondo_anverso_url})` : 'none' }">
              <div class="header-izquierdo">
                <div class="bandera-placeholder">
                  <img v-if="configCarnet.bandera_url" :src="configCarnet.bandera_url" class="bandera-img">
                </div>
                <div>
                  <div class="titulo-comunidad">{{ configCarnet.nombre_comunidad }}</div>
                  <div class="sub-resolucion">{{ configCarnet.resolucion }}</div>
                </div>
              </div>

              <div class="num-carnet-container">
                <div class="etiqueta-carnet">N° CARNET</div>
                <div style="font-size: 8pt; text-shadow: 0 0 5px rgba(255, 255, 255, 1), 0 0 10px rgba(255, 255, 255, 1), 0 0 15px rgba(255, 255, 255, 1), 0 0 20px rgba(255, 255, 255, 1), 0 0 25px rgba(255, 255, 255, 1), 0 0 30px rgba(255, 255, 255, 1), 0 0 35px rgba(255, 255, 255, 1); font-weight: 700; white-space: nowrap;">{{ obtenerNumeroCarnet(usuarioSeleccionado) }}</div>
              </div>

              <div class="info-bloque">
                <div class="foto-section">
                  <div class="foto-placeholder">
                    <img v-if="usuarioSeleccionado.foto_frontal" :src="usuarioSeleccionado.foto_frontal" class="foto-img">
                  </div>
                  <div class="texto-foto">CARNET COMUNERO</div>
                </div>

                <div class="datos-personales">
                  <div class="campo">
                    <span class="etiqueta">APELLIDOS:</span>
                    <span class="valor">{{ obtenerApellidos(usuarioSeleccionado) }}</span>
                  </div>
                  <div class="campo">
                    <span class="etiqueta">NOMBRES:</span>
                    <span class="valor">{{ obtenerNombres(usuarioSeleccionado) }}</span>
                  </div>

                  <div class="campo-fechas">
                    <div class="fecha-item">
                      <span class="f-etiqueta">Fecha de Emisión</span>
                      <span class="f-valor">{{ obtenerFechaEmision() }}</span>
                    </div>
                    <div class="fecha-item">
                      <span class="f-etiqueta">Fecha de Caducidad</span>
                      <span class="f-valor">{{ obtenerFechaCaducidad() }}</span>
                    </div>
                    <div class="fecha-item">
                      <span class="f-etiqueta">Estado Civil</span>
                      <span class="f-valor">{{ usuarioSeleccionado.estado_civil || '-' }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="firmas-container">
                <div class="firma-box">
                  <div v-if="configCarnet.firma_secretario_url" class="firma-imagen">
                    <img :src="configCarnet.firma_secretario_url" alt="Firma Secretario">
                  </div>
                  <div v-else class="firma-placeholder">[Firma]</div>
                  <span style="font-size:6px!important; text-shadow: 0 0 5px rgba(255, 255, 255, 1), 0 0 10px rgba(255, 255, 255, 1), 0 0 15px rgba(255, 255, 255, 1), 0 0 20px rgba(255, 255, 255, 1), 0 0 25px rgba(255, 255, 255, 1), 0 0 30px rgba(255, 255, 255, 1), 0 0 35px rgba(255, 255, 255, 1); font-weight: 700; white-space: nowrap;">Secretario CC-TPCT</span>
                  <span style="font-size:6px!important; text-shadow: 0 0 5px rgba(255, 255, 255, 1), 0 0 10px rgba(255, 255, 255, 1), 0 0 15px rgba(255, 255, 255, 1), 0 0 20px rgba(255, 255, 255, 1), 0 0 25px rgba(255, 255, 255, 1), 0 0 30px rgba(255, 255, 255, 1), 0 0 35px rgba(255, 255, 255, 1); font-weight: 700;">F. Paripanca R</span>
                </div>
                <div class="firma-box">
                  <div v-if="configCarnet.firma_presidente_url" class="firma-imagen">
                    <img :src="configCarnet.firma_presidente_url" alt="Firma Presidente">
                  </div>
                  <div v-else class="firma-placeholder">[Firma]</div>
                  <span style="font-size:6px!important; text-shadow: 0 0 5px rgba(255, 255, 255, 1), 0 0 10px rgba(255, 255, 255, 1), 0 0 15px rgba(255, 255, 255, 1), 0 0 20px rgba(255, 255, 255, 1), 0 0 25px rgba(255, 255, 255, 1), 0 0 30px rgba(255, 255, 255, 1), 0 0 35px rgba(255, 255, 255, 1); font-weight: 700; white-space: nowrap;">Presidente CC-TPCT</span>
                  <span style="font-size:6px!important; text-shadow: 0 0 5px rgba(255, 255, 255, 1), 0 0 10px rgba(255, 255, 255, 1), 0 0 15px rgba(255, 255, 255, 1), 0 0 20px rgba(255, 255, 255, 1), 0 0 25px rgba(255, 255, 255, 1), 0 0 30px rgba(255, 255, 255, 1), 0 0 35px rgba(255, 255, 255, 1); font-weight: 700;">M. García N.</span>
                </div>
              </div>
            </div>

            <!-- LADO DERECHO (REVERSO) -->
            <div class="lado-derecho" :style="{ backgroundImage: configCarnet.fondo_reverso_url ? `url(${configCarnet.fondo_reverso_url})` : 'none' }">
              <div class="header-derecho">
                <div class="siglas">{{ configCarnet.nombre_corto || 'CC.TPCT' }}</div>
                <div class="escudo-placeholder">
                  <img v-if="configCarnet.escudo_url" :src="configCarnet.escudo_url" class="escudo-img">
                  <span v-else>[Escudo]</span>
                </div>
              </div>

              <div class="footer-derecho">
                <div class="qr-row">
                  <div class="qr-container">
                    <canvas :id="`qr-canvas-completo-${usuarioSeleccionado.id}`" class="qr-placeholder"></canvas>
                    <div class="qr-codigo">{{ obtenerNumeroCarnet(usuarioSeleccionado) }}</div>
                  </div>

                  <div class="metadatos-qr">
                    <div class="meta-item">
                      <span class="m-etiqueta">Número de DNI</span>
                      <span class="m-valor">{{ usuarioSeleccionado.numero_dni }}</span>
                    </div>
                    <div class="meta-item">
                      <span class="m-etiqueta">Categoría</span>
                      <span class="m-valor-destacado">COMUNERO(A)</span>
                    </div>
                    <div class="meta-item">
                      <span class="m-etiqueta">Fecha de Nacimiento</span>
                      <span class="m-valor">{{ usuarioSeleccionado.fecha_nacimiento || '-' }}</span>
                    </div>
                    <div class="meta-item">
                      <span class="m-etiqueta">Anexo que Pertenece</span>
                      <span class="m-valor">{{ usuarioSeleccionado.anexo || '-' }}</span>
                    </div>
                  </div>

                  <div v-if="configCarnet.url_qr" class="qr-url-wrapper">
                    <div class="qr-url-label">Página Web:</div>
                    <canvas :id="`qr-url-canvas-${usuarioSeleccionado.id}`" class="qr-url"></canvas>
                    <div class="qr-url-text">{{ configCarnet.url_qr }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <button class="btn-exportar-individual" @click="exportarCarnetIndividual">
          <ion-icon name="download-outline"></ion-icon>
          Descargar este carnet (PDF)
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import QRCode from 'qrcode'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'
import api from '@/services/api'

export default {
  name: 'CarnetsView',
  setup() {
    const route = useRoute()
    const usuarios = ref([])
    const usuarioSeleccionado = ref(null)
    const busqueda = ref('')
    const tabActivo = ref('anverso')
    const mostrarConfigModal = ref(false)
    const mostrarModalBloques = ref(false)
    const mostrarModalVincularFotos = ref(false)
    const cargando = ref(false)
    const vinculandoFotos = ref(false)
    const resultadoVincularFotos = ref(null)
    const tabVincular = ref('vincular')
    const dragOverArea = ref(false)
    const fotosACargar = ref([])
    const cargandoFotos = ref(false)
    const dragOverItem = ref(null)

    const configCarnet = ref({
      nombre_comunidad: 'Comunidad Campesina Tumilaca, Pocata, Coscore y Tala',
      subtitulo: 'TUMILACA, POCATA, COSCORE Y TALA',
      resolucion: 'RESOLUCIÓN SUPREMA 07 SET 1949',
      nombre_corto: 'CC.TPCT',
      bandera_url: null,
      escudo_url: null,
      fondo_anverso_url: null,
      fondo_reverso_url: null,
      firma_secretario_url: null,
      firma_presidente_url: null,
      url_qr: null
    })

    const usuariosFiltrados = computed(() => {
      if (!busqueda.value) return usuarios.value
      const q = busqueda.value.toLowerCase()
      return usuarios.value.filter(u =>
        u.nombre_completo?.toLowerCase().includes(q) ||
        u.numero_dni?.includes(q)
      )
    })

    const tamanoBloque = ref(200)

    const totalBloques = computed(() => {
      if (!usuarios.value || usuarios.value.length === 0) return 0
      if (tamanoBloque.value === 'todos') return 1
      return Math.ceil(usuarios.value.length / tamanoBloque.value)
    })

    const cargarUsuarios = async () => {
      try {
        cargando.value = true
        const response = await api.get('/usuarios/?limit=10000')
        if (response.data.success) {
          usuarios.value = response.data.data
          if (usuarios.value.length > 0) {
            usuarioSeleccionado.value = usuarios.value[0]
          }
        }
      } catch (error) {
        console.error('Error cargando usuarios:', error)
      } finally {
        cargando.value = false
      }
    }

    const cargarConfigCarnet = async () => {
      try {
        const response = await api.get('/admin/configuracion/carnet')
        console.log('Configuración cargada:', response.data)
        configCarnet.value = { ...configCarnet.value, ...response.data }
        console.log('configCarnet actualizado:', configCarnet.value)
      } catch (error) {
        console.error('Error cargando configuración del carnet:', error)
      }
    }

    const cargarImagen = async (event, tipo) => {
      const file = event.target.files[0]
      if (!file) return

      try {
        const formData = new FormData()
        formData.append('file', file)

        const uploadResponse = await api.post(`/admin/configuracion/carnet/upload?tipo=${tipo}`, formData)
        const campo = {
          bandera: 'bandera_url',
          escudo: 'escudo_url',
          fondo_anverso: 'fondo_anverso_url',
          fondo_reverso: 'fondo_reverso_url',
          firma_secretario: 'firma_secretario_url',
          firma_presidente: 'firma_presidente_url'
        }[tipo]
        configCarnet.value[campo] = uploadResponse.data.url
      } catch (error) {
        let errorMsg = 'Error desconocido'
        if (error.response?.data?.detail) {
          errorMsg = error.response.data.detail
        }
        console.error('Error subiendo imagen:', error)
        alert(`Error al subir la imagen: ${errorMsg}`)
      }
    }

    const handleDrop = async (event, tipo) => {
      const files = event.dataTransfer.files
      if (files.length > 0) {
        const file = files[0]
        // Simular un cambio de input para reutilizar cargarImagen
        const fakeEvent = { target: { files: [file] } }
        await cargarImagen(fakeEvent, tipo)
      }
      dragOverItem.value = null
    }

    const clickInputBandera = () => {
      const input = document.getElementById('input-bandera')
      if (input) input.click()
    }

    const clickInputEscudo = () => {
      const input = document.getElementById('input-escudo')
      if (input) input.click()
    }

    const clickInputFondoAnverso = () => {
      const input = document.getElementById('input-fondo-anverso')
      if (input) input.click()
    }

    const clickInputFondoReverso = () => {
      const input = document.getElementById('input-fondo-reverso')
      if (input) input.click()
    }

    const clickInputFirmaSecretario = () => {
      const input = document.getElementById('input-firma-secretario')
      if (input) input.click()
    }

    const clickInputFirmaPresidente = () => {
      const input = document.getElementById('input-firma-presidente')
      if (input) input.click()
    }

    const guardarConfiguracion = async () => {
      try {
        cargando.value = true

        const params = {
          nombre_comunidad: configCarnet.value.nombre_comunidad,
          subtitulo: configCarnet.value.subtitulo,
          resolucion: configCarnet.value.resolucion,
          nombre_corto: configCarnet.value.nombre_corto,
          url_qr: configCarnet.value.url_qr || ''
        }

        console.log('Guardando configuración:', params)

        const response = await api.put('/admin/configuracion/carnet', null, { params })
        mostrarConfigModal.value = false
        alert('Configuración guardada exitosamente')
      } catch (error) {
        let errorMsg = 'Error desconocido'
        if (error.response?.data?.detail) {
          errorMsg = error.response.data.detail
        } else if (error.response?.data) {
          errorMsg = JSON.stringify(error.response.data)
        }
        console.error('Error guardando configuración:', error)
        alert(`Error al guardar configuración: ${errorMsg}`)
      } finally {
        cargando.value = false
      }
    }

    const obtenerNumeroCarnet = (usuario) => {
      let padron = usuario.num_padron || String(usuario.id).padStart(3, '0')

      // Extraer solo los números del padrón
      const numPadron = parseInt(padron.replace(/\D/g, '')) || 0

      // Aplicar padding según el rango
      let padronFormateado
      if (numPadron < 100) {
        padronFormateado = String(numPadron).padStart(4, '0')  // 00XX
      } else if (numPadron < 1000) {
        padronFormateado = String(numPadron).padStart(4, '0')  // 0XXX
      } else {
        padronFormateado = String(numPadron)  // XXXX+
      }

      return padronFormateado + usuario.numero_dni
    }

    const obtenerApellidos = (usuario) => {
      const apellidos = [usuario.apellido_paterno, usuario.apellido_materno]
        .filter(a => a && a.trim())
        .join(' ')
      return apellidos.toUpperCase()
    }

    const obtenerNombres = (usuario) => {
      return (usuario.nombres || '').toUpperCase()
    }

    const obtenerFechaEmision = () => {
      const hoy = new Date()
      return `${hoy.getDate().toString().padStart(2, '0')}/${(hoy.getMonth() + 1).toString().padStart(2, '0')}/${hoy.getFullYear()}`
    }

    const obtenerFechaCaducidad = () => {
      const hoy = new Date()
      const caducidad = new Date(hoy.getFullYear() + 4, hoy.getMonth(), hoy.getDate())
      return `${caducidad.getDate().toString().padStart(2, '0')}/${(caducidad.getMonth() + 1).toString().padStart(2, '0')}/${caducidad.getFullYear()}`
    }

    const generarQR = async (usuario, canvasId) => {
      if (!usuario) return
      const qrData = obtenerNumeroCarnet(usuario)
      try {
        setTimeout(async () => {
          const canvas = document.getElementById(canvasId)
          if (canvas) {
            await QRCode.toCanvas(canvas, qrData, {
              width: 100,
              margin: 1,
              color: { dark: '#000000', light: '#FFFFFF' }
            })
          }
        }, 50)
      } catch (error) {
        console.error('Error generando QR:', error)
      }
    }

    const generarQRURL = async (usuario, urlQR) => {
      if (!usuario || !urlQR) return
      try {
        setTimeout(async () => {
          const canvas = document.getElementById(`qr-url-canvas-${usuario.id}`)
          if (canvas) {
            await QRCode.toCanvas(canvas, urlQR, {
              width: 60,
              margin: 1,
              color: { dark: '#000000', light: '#FFFFFF' }
            })
          }
        }, 50)
      } catch (error) {
        console.error('Error generando QR de URL:', error)
      }
    }

    const descargarBlob = (blob, nombre) => {
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = nombre
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    }

    const exportarCarnetIndividual = async () => {
      if (!usuarioSeleccionado.value) return

      try {
        cargando.value = true
        const response = await api.get(
          `/carnets/exportar-pdf-individual/${usuarioSeleccionado.value.id}`,
          { responseType: 'blob' }
        )
        const dni = usuarioSeleccionado.value.numero_dni || usuarioSeleccionado.value.id
        descargarBlob(response.data, `carnet-${dni}.pdf`)
      } catch (error) {
        console.error('Error exportando carnet:', error)
        alert('Error al exportar carnet: ' + (error.response?.data?.detail || error.message))
      } finally {
        cargando.value = false
      }
    }

    // Sistema de tareas con progreso
    const mostrarModalProgreso = ref(false)
    const tareaActual = ref(null)
    const progreso = ref(0)
    const mensajeProgreso = ref('')
    const pollingInterval = ref(null)

    const iniciarExportacion = async (params) => {
      try {
        const response = await api.post('/carnets/exportar-async', null, { params })
        tareaActual.value = {
          task_id: response.data.task_id,
          inicio: new Date(),
          totalCarnets: params.todos ? usuarios.value.length : (params.limit || 200)
        }
        mostrarModalProgreso.value = true
        progreso.value = 0
        mensajeProgreso.value = 'En cola de espera...'
        mostrarModalBloques.value = false

        // Iniciar polling
        rastrearProgreso()
      } catch (error) {
        console.error('Error iniciando exportación:', error)
        alert('Error al iniciar exportación: ' + (error.response?.data?.detail || error.message))
      }
    }

    const rastrearProgreso = async () => {
      if (!tareaActual.value) return

      const chequearEstado = async () => {
        try {
          const response = await api.get(`/carnets/tarea/${tareaActual.value.task_id}`)
          const estado = response.data

          progreso.value = estado.porcentaje || 0
          mensajeProgreso.value = estado.mensaje || ''

          if (estado.estado === 'completada') {
            clearInterval(pollingInterval.value)
            // Descargar automáticamente
            await descargarPDF(tareaActual.value.task_id, estado.total_carnets)
            mostrarModalProgreso.value = false
          } else if (estado.estado === 'error') {
            clearInterval(pollingInterval.value)
            alert(`Error: ${estado.error || 'Error desconocido'}`)
            mostrarModalProgreso.value = false
          }
        } catch (error) {
          console.error('Error rastreando progreso:', error)
          clearInterval(pollingInterval.value)
          alert('Error al rastrear progreso')
          mostrarModalProgreso.value = false
        }
      }

      // Check inicial inmediato
      await chequearEstado()

      // Polling cada 500ms
      if (tareaActual.value) {
        pollingInterval.value = setInterval(chequearEstado, 500)
      }
    }

    const descargarPDF = async (taskId, totalCarnets) => {
      try {
        const response = await api.get(`/carnets/descargar/${taskId}`, {
          responseType: 'blob'
        })

        const nombreArchivo = totalCarnets === 1
          ? `carnet.pdf`
          : `carnets-${totalCarnets}.pdf`

        descargarBlob(response.data, nombreArchivo)
      } catch (error) {
        console.error('Error descargando PDF:', error)
        alert('Error al descargar PDF: ' + (error.response?.data?.detail || error.message))
      }
    }

    const cancelarExportacion = () => {
      if (pollingInterval.value) {
        clearInterval(pollingInterval.value)
      }
      tareaActual.value = null
      mostrarModalProgreso.value = false
    }

    const exportarTodosPDF = async () => {
      if (usuarios.value.length === 0) {
        alert('No hay usuarios para exportar')
        return
      }

      const segundosEstimados = Math.ceil(usuarios.value.length * 1.5)
      const minutosEstimados = Math.ceil(segundosEstimados / 60)
      if (!confirm(`Vas a generar un único PDF con TODOS los ${usuarios.value.length} carnets.\n\nTiempo estimado: ~${minutosEstimados} minuto(s).\n\n¿Continuar?`)) {
        return
      }

      await iniciarExportacion({ todos: true })
    }

    const exportarBloqueePDF = async (numBloque) => {
      const tamano = tamanoBloque.value === 'todos' ? usuarios.value.length : tamanoBloque.value
      const offset = (numBloque - 1) * tamano
      await iniciarExportacion({ limit: tamano, offset })
    }

    onMounted(async () => {
      await cargarUsuarios()
      await cargarConfigCarnet()

      // Si viene con query param ?usuario=ID, seleccionar ese usuario
      const usuarioIdParam = route.query.usuario
      if (usuarioIdParam) {
        const encontrado = usuarios.value.find(u => u.id === parseInt(usuarioIdParam))
        if (encontrado) usuarioSeleccionado.value = encontrado
      }

      // Generar QR para todos cuando se carga
      for (const usuario of usuarios.value) {
        await generarQR(usuario, `preview-qr-canvas-${usuario.id}`)
      }
    })

    // Generar QR cuando se selecciona un usuario
    watch(() => usuarioSeleccionado.value, async (nuevoUsuario) => {
      if (nuevoUsuario) {
        await generarQR(nuevoUsuario, `qr-canvas-completo-${nuevoUsuario.id}`)
        if (configCarnet.value.url_qr) {
          await generarQRURL(nuevoUsuario, configCarnet.value.url_qr)
        }
      }
    })

    // Regenerar QR de URL cuando cambia
    watch(() => configCarnet.value.url_qr, async (nuevaUrl) => {
      if (usuarioSeleccionado.value && nuevaUrl) {
        await generarQRURL(usuarioSeleccionado.value, nuevaUrl)
      }
    })

    // Recargar configuración cuando se abre la modal
    watch(() => mostrarConfigModal.value, async (estaAbierta) => {
      if (estaAbierta) {
        await cargarConfigCarnet()
      }
    })

    const ejecutarVincularFotos = async () => {
      vinculandoFotos.value = true
      resultadoVincularFotos.value = null
      try {
        const respuesta = await fetch('/api/carnets/vincular-fotos', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        })

        if (!respuesta.ok) {
          throw new Error('Error al vincular fotos')
        }

        const resultado = await respuesta.json()
        resultadoVincularFotos.value = resultado
      } catch (error) {
        console.error('Error vinculando fotos:', error)
        resultadoVincularFotos.value = {
          success: false,
          error: error.message,
          resumen: {
            vinculados: 0,
            ya_vinculados: 0,
            no_encontrados: 0,
            errores: 0,
            total: 0
          }
        }
      } finally {
        vinculandoFotos.value = false
      }
    }

    const cerrarModalVincularFotos = () => {
      mostrarModalVincularFotos.value = false
      resultadoVincularFotos.value = null
      tabVincular.value = 'vincular'
      fotosACargar.value = []
    }

    const manejarDropFotos = (event) => {
      dragOverArea.value = false
      const archivos = event.dataTransfer.files
      procesarArchivos(archivos)
    }

    const manejarSeleccionFotos = (event) => {
      const archivos = event.target.files
      procesarArchivos(archivos)
    }

    const procesarArchivos = (archivos) => {
      for (let archivo of archivos) {
        if (archivo.type.startsWith('image/')) {
          const reader = new FileReader()
          reader.onload = (e) => {
            fotosACargar.value.push({
              archivo: archivo,
              preview: e.target.result,
              nombre: archivo.name
            })
          }
          reader.readAsDataURL(archivo)
        }
      }
    }

    const eliminarFotoCargar = (index) => {
      fotosACargar.value.splice(index, 1)
    }

    const formatarTamaño = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
    }

    const enviarFotos = async () => {
      if (fotosACargar.value.length === 0) return

      cargandoFotos.value = true
      const formData = new FormData()

      for (let foto of fotosACargar.value) {
        formData.append('archivos', foto.archivo)
      }

      try {
        const respuesta = await fetch('/api/carnets/cargar-fotos', {
          method: 'POST',
          body: formData
        })

        if (!respuesta.ok) {
          throw new Error('Error al cargar fotos')
        }

        const resultado = await respuesta.json()
        resultadoVincularFotos.value = resultado
        fotosACargar.value = []
      } catch (error) {
        console.error('Error cargando fotos:', error)
        resultadoVincularFotos.value = {
          success: false,
          error: error.message,
          resumen: {
            cargadas: 0,
            errores: 0,
            total: 0
          }
        }
      } finally {
        cargandoFotos.value = false
      }
    }

    return {
      usuarios,
      usuarioSeleccionado,
      usuariosFiltrados,
      busqueda,
      tabActivo,
      mostrarConfigModal,
      mostrarModalBloques,
      cargando,
      dragOverItem,
      configCarnet,
      totalBloques,
      cargarImagen,
      handleDrop,
      guardarConfiguracion,
      clickInputBandera,
      clickInputEscudo,
      clickInputFondoAnverso,
      clickInputFondoReverso,
      clickInputFirmaSecretario,
      clickInputFirmaPresidente,
      obtenerNumeroCarnet,
      obtenerApellidos,
      obtenerNombres,
      obtenerFechaEmision,
      obtenerFechaCaducidad,
      exportarCarnetIndividual,
      exportarTodosPDF,
      exportarBloqueePDF,
      mostrarModalVincularFotos,
      vinculandoFotos,
      resultadoVincularFotos,
      ejecutarVincularFotos,
      cerrarModalVincularFotos,
      tabVincular,
      dragOverArea,
      fotosACargar,
      cargandoFotos,
      manejarDropFotos,
      manejarSeleccionFotos,
      eliminarFotoCargar,
      formatarTamaño,
      enviarFotos,
      mostrarModalProgreso,
      progreso,
      mensajeProgreso,
      cancelarExportacion,
      tareaActual,
      tamanoBloque
    }
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.carnets-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  gap: 15px;
  padding: 20px;
}

/* TOOLBAR */
.carnet-toolbar {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  align-items: center;
}

.btn-config, .btn-togglear-vista, .btn-exportar-todos, .btn-primary, .btn-secondary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-config:hover, .btn-togglear-vista:hover, .btn-exportar-todos:hover, .btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
  background: #6c757d;
}

.btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-2px);
}

/* MODAL */
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
  z-index: 1000;
}

.modal-config {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  font-size: 18px;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6c757d;
}

.modal-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.config-section h3 {
  margin: 0 0 15px 0;
  font-size: 14px;
  color: #333;
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
  gap: 8px;
}

.config-section h3 ion-icon {
  font-size: 18px;
  color: #667eea;
}

.config-section:first-child {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.config-section:first-child h3 {
  grid-column: 1 / -1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-bottom: 10px;
}

.form-group label {
  font-size: 12px;
  font-weight: 600;
}

.form-input {
  padding: 8px 12px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  font-size: 13px;
  font-family: inherit;
}

.imagen-upload {
  border: 1px solid #dee2e6;
  border-radius: 6px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-input {
  font-size: 12px;
}

.imagen-preview {
  width: 100px;
  height: 100px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  overflow: hidden;
}

.imagen-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.modal-footer {
  padding: 15px 20px;
  border-top: 1px solid #e9ecef;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* MODAL CONFIGURACIÓN AVANZADA */
.modal-config-advanced {
  background: white;
  border-radius: 8px;
  width: 95%;
  max-width: 1200px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.modal-body-advanced {
  display: grid;
  grid-template-columns: 1fr 40%;
  gap: 20px;
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.config-panel-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.config-panel-preview {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  height: fit-content;
  position: sticky;
  top: 0;
  max-height: 90vh;
  overflow-y: auto;
}

.config-panel-preview h3 {
  margin: 0 0 10px 0;
  font-size: 13px;
  color: #333;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.config-panel-preview h3 ion-icon {
  font-size: 16px;
  color: #667eea;
}

.preview-carnet-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  width: 100%;
}

.carnet-container-mini {
  width: 100%;
  aspect-ratio: 5.06 / 1.44;
  background-color: #ffffff;
  border: 1px solid #cccccc;
  display: flex;
  position: relative;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  font-family: 'Segoe UI', 'Roboto', sans-serif;
  overflow: hidden;
}

.carnet-container-mini::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 0;
  width: 1px;
  height: 100%;
  background-color: #cccccc;
}

.lado-izquierdo-mini, .lado-derecho-mini {
  width: 50%;
  height: 100%;
  position: relative;
  padding: 2%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 0.5vw;
}

.header-izquierdo-mini {
  display: flex;
  align-items: center;
  gap: 2%;
  width: 95%;
  font-size: 0.6vw;
}

.bandera-placeholder-mini {
  width: 8%;
  aspect-ratio: 2.5;
  background: linear-gradient(to bottom, #ffeb3b 50%, #e53935 50%);
  /*border: 0.5px solid #d32f2f;*/
  flex-shrink: 0;
  border-radius: 1px;
}

.bandera-img-mini {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.titulo-mini {
  flex: 1;
  line-height: 1.15;
  padding: 0 2%;
}

.titulo-principal-mini {
  font-weight: 700;
  font-size: 0.55vw;
}

.titulo-subtitulo-mini {
  font-size: 0.45vw;
  color: #666;
}

.lado-derecho-mini {
  justify-content: space-around;
  gap: 3%;
}

.siglas-mini {
  font-weight: 700;
  font-size: 0.55vw;
}

.escudo-placeholder-mini {
  width: 8%;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.35vw;
  color: #999;
  overflow: hidden;
  border-radius: 1px;
}

.escudo-img-mini {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.imagen-upload-group {
  /*border: 1px solid #dee2e6;*/
  border-radius: 6px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  /*background: #f8f9fa;*/
}

.imagen-label {
  font-size: 12px;
  font-weight: 600;
  color: #333;
}

.imagen-preview-small {
  width: 60px;
  height: 60px;
  /*border: 1px solid #dee2e6;*/
  border-radius: 4px;
  overflow: hidden;
}

.imagen-preview-small img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* DRAG AND DROP IMAGES */
.imagenes-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.imagen-dropzone {
  border: 2px dashed #667eea;
  border-radius: 6px;
  padding: 10px;
  background: #f8f9ff;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  min-height: 100px;
}

.imagen-dropzone:hover {
  border-color: #764ba2;
  background: #f0eeff;
}

.imagen-dropzone.drag-over {
  border-color: #764ba2;
  background: #e8e0ff;
  box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
  transform: scale(1.02);
}

.dropzone-content {
  cursor: pointer;
}

.dropzone-content:hover .dropzone-placeholder {
  color: #667eea;
}

.dropzone-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 15px 10px;
  gap: 6px;
  transition: all 0.2s;
}

.dropzone-icon {
  font-size: 28px;
  color: #667eea;
}

.dropzone-text {
  font-weight: 600;
  color: #333;
  font-size: 11px;
}

.dropzone-hint {
  font-size: 9px;
  color: #999;
  text-align: center;
}

.imagen-preview-grande {
  width: 100%;
  max-height: 80px;
  border-radius: 4px;
  overflow: hidden;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.imagen-preview-grande img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.file-input-hidden {
  display: none;
}

.btn-change {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 6px 12px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s;
}

.imagen-dropzone:hover .btn-change {
  opacity: 1;
}

.btn-change:hover {
  background: #764ba2;
}

/* CARNET COMPLETO - Anverso + Reverso */
.carnet-completo-viewport {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
  background: #f8f9fa;
  border-radius: 6px;
  padding: 20px;
  overflow: auto;
}

.carnet-container {
  width: 642px;
  height: 204px;
  background-color: #ffffff;
  border: 1px solid #cccccc;
  display: flex;
  position: relative;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow: hidden;
}

.carnet-container::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 0;
  width: 1px;
  height: 100%;
  background-color: #cccccc;
  z-index: 10;
}


.lado-izquierdo, .lado-derecho {
  width: 50%;
  height: 100%;
  position: relative;
  padding: 12px 15px;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: scroll;
}

.lado-izquierdo::before, .lado-derecho::before {
  content: "";
  position: absolute;
  inset: 0;
  background: transparent;
  z-index: 0;
  pointer-events: none;
}

.lado-izquierdo > *, .lado-derecho > * {
  position: relative;
  z-index: 1;
}

/* CARNET CARD - 9.5cm × 5cm (para vista previsualización) */
.carnet-card {
  position: relative;
  width: 95mm;
  height: 50mm;
  border: 1px solid #ccc;
  overflow: hidden;
  border-radius: 3mm;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  font-size: 7px;
}

.carnet-card.individual {
  width: 400px;
  height: 210px;
  font-size: 11px;
}

.carnet-fondo {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.35;
  z-index: 0;
}

.carnet-fondo-default {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
  z-index: 0;
}

.carnet-content {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 3mm;
  color: #1a1a1a;
}

/* ANVERSO */
.carnet-top {
  display: grid;
  grid-template-columns: 13mm 1fr 20mm;
  gap: 2mm;
  margin-bottom: 2mm;
  align-items: flex-start;
}

.carnet-logo-section {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 13mm;
}

.carnet-logo {
  width: 100%;
  height: 10mm;
  object-fit: contain;
}

.carnet-logo-placeholder {
  width: 100%;
  height: 10mm;
  /*background: #e9ecef;
  border: 1px solid #dee2e6;*/
}

.carnet-title {
  display: flex;
  flex-direction: column;
  gap: 0.5mm;
  font-size: 0.85em;
}

.titulo-principal {
  font-weight: bold;
  font-size: 0.9em;
  line-height: 1;
}

.titulo-subtitulo {
  font-size: 0.75em;
  color: #666;
  line-height: 1;
}

.titulo-resolucion {
  font-size: 0.65em;
  color: #999;
  line-height: 1;
}

.carnet-numero {
  display: flex;
  flex-direction: column;
  text-align: right;
  justify-content: flex-start;
  gap: 0.5mm;
}

.label-numero {
  font-size: 0.6em;
  font-weight: bold;
}

.valor-numero {
  font-weight: bold;
  font-size: 0.75em;
}

.carnet-body {
  display: grid;
  grid-template-columns: 28mm 1fr;
  gap: 2mm;
  flex: 1;
  min-height: 0;
}

.foto-section {
  display: flex;
  flex-direction: column;
  gap: 1mm;
  align-items: center;
}

.foto-box {
  width: 28mm;
  height: 35mm;
  border: 1px solid #1a1a1a;
  overflow: hidden;
  background: #f5f5f5;
}

.foto-usuario {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.foto-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 0.7em;
}

.foto-label {
  font-weight: bold;
  font-size: 0.65em;
  text-align: center;
  width: 100%;
}

.datos-section {
  display: flex;
  flex-direction: column;
  gap: 1.5mm;
  padding-right: 1mm;
}

.dato-line {
  display: grid;
  grid-template-columns: 35% 65%;
  gap: 1mm;
  align-items: center;
}

.dato-label {
  font-weight: bold;
  font-size: 0.7em;
}

.dato-valor {
  font-weight: bold;
  font-size: 0.75em;
}

.carnet-footer {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2mm;
  padding-top: 1.5mm;
  border-top: 0.5px solid #ccc;
  font-size: 0.65em;
  margin-top: auto;
}

.fechas-section {
  display: flex;
  flex-direction: column;
  gap: 0.5mm;
}

.fecha-item {
  display: flex;
  flex-direction: column;
  gap: 0.3mm;
  line-height: 1;
}

.fecha-label {
  font-weight: bold;
  font-size: 0.65em;
}

.fecha-valor {
  font-size: 0.7em;
}

.firmas-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1mm;
}

.firma-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  font-weight: bold;
  font-size: 0.6em;
  line-height: 1.1;
}

.firma-imagen {
  max-height: 44px;
  max-width: 90px;
  margin-bottom: 1px;
  object-fit: contain;
  z-index: 9;
}

.firma-imagen img {
  max-height: 44px;
  max-width: 90px;
  object-fit: contain;
}

/* REVERSO */
.carnet-card.reverso .carnet-content {
  display: grid;
  grid-template-columns: 45mm 1fr;
  gap: 1.5mm;
  padding: 2mm;
}

.reverso-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
  border-right: 0.5px solid #ddd;
  padding-right: 1mm;
}

.reverso-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1mm;
}

.reverso-titulo {
  font-weight: bold;
  font-size: 0.8em;
}

.escudo {
  width: 12mm;
  height: 12mm;
  object-fit: contain;
}

.escudo-placeholder {
  width: 12mm;
  height: 12mm;
}

.qr-section {
  display: flex;
  align-items: center;
  justify-content: center;
}

.qr-canvas {
  width: 25mm !important;
  height: 25mm !important;
}

.reverso-right {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding-left: 1mm;
  font-size: 0.7em;
}

.dato-reverso-item {
  display: grid;
  grid-template-columns: 50% 50%;
  gap: 0.5mm;
  line-height: 1.1;
  align-items: center;
}

.dato-reverso-label {
  font-weight: bold;
  font-size: 0.65em;
}

.dato-reverso-valor {
  font-size: 0.7em;
}

.numero-carnet-reverso {
  font-weight: bold;
  font-size: 0.7em;
  margin-top: 1mm;
  padding-top: 1mm;
  border-top: 0.5px solid #ccc;
}

/* VISTA INDIVIDUAL */
.carnet-individual-container {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 20px;
  flex: 1;
  min-height: 0;
}

.usuarios-panel {
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  border: 1px solid #e9ecef;
  min-height: 0;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 6px;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
}

.usuarios-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
  flex: 1;
}

.usuario-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
  font-size: 12px;
}

.usuario-item:hover {
  border-color: #667eea;
  background: #f8f9ff;
}

.usuario-item.active {
  background: #667eea;
  border-color: #667eea;
  color: white;
}

.usuario-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  background: #e9ecef;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 16px;
}

.usuario-info {
  flex: 1;
  min-width: 0;
}

.usuario-nombre {
  font-weight: 600;
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.usuario-dni {
  font-size: 11px;
  opacity: 0.7;
  margin-top: 2px;
}

.carnet-panel {
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  min-height: 0;
}

.carnet-tabs {
  display: flex;
  gap: 10px;
  border-bottom: 2px solid #e9ecef;
}

.tab-btn {
  padding: 10px 20px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-weight: 500;
  color: #6c757d;
  transition: all 0.2s;
  font-size: 13px;
}

.tab-btn.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

.carnet-viewport {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
  background: #f8f9fa;
  border-radius: 6px;
  padding: 20px;
  min-height: 450px;
  overflow: auto;
}

.btn-exportar-individual {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  margin-top: auto;
}

.btn-exportar-individual:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
}

/* LADO IZQUIERDO (ANVERSO) */
.header-izquierdo {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 12px;
}

.bandera-placeholder {
  width: 41px;
  height: 25px;
  /*border: 1px solid #d32f2f;*/
  position: relative;
  flex-shrink: 0;
  overflow: hidden;
  background: linear-gradient(to bottom, #ffeb3b 50%, #e53935 50%);
}

.bandera-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.titulo-comunidad {
  font-size: 9.5px;
  font-weight: 700;
  color: #0d0d0d;
  line-height: 1.2;
  letter-spacing: 0.1px;
  max-width: 150px;
  word-wrap: break-word;
  white-space: normal;
  margin-top: -2px;
}

.sub-resolucion {
  font-size: 7px;
  font-weight: 600;
  color: #0f0f0f;
  margin-top: 1px;
  letter-spacing: 0.3px;
  line-height: 1.1;
}

.num-carnet-container {
  position: absolute;
  top: 12px;
  right: 15px;
  text-align: right;
}

.etiqueta-carnet {
  font-size: 8px;
  font-weight: 600;
  color: #0d0d0d;
  letter-spacing: 0.3px;
  z-index: 9999999999999999999;
}

.num-carnet {
  font-size: 9px;
  font-weight: 700;
  color: #0d0d0d;
  margin-top: 1px;
  letter-spacing: 0.1px;
  font-family: 'Courier New', monospace;
  background-color: #fff;
  padding: 2px 2px 0;
}

.info-bloque {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.foto-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1px;
}

.foto-placeholder {
  width: 68px;
  height: 85px;
  border: 1px solid #000000;
  background: #f5f5f5;
  overflow: hidden;
  position: relative;
}

.foto-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
}

.texto-foto {
  font-size: 7px;
  font-weight: 700;
  color: #000;
  letter-spacing: 0.2px;
  line-height: 1.1;
  text-align: center;
}

.datos-personales {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-top: 1px;
}

.campo {
  display: flex;
  flex-direction: column;
}

.campo .etiqueta {
  font-size: 8px;
  color: #000000;
  font-weight: 600;
  letter-spacing: 0.3px;
  line-height: 1.1;
}

.campo .valor {
  font-size: 9.5px;
  font-weight: 700;
  color: #0d0d0d;
  text-transform: uppercase;
  margin-top: 0.5px;
  letter-spacing: 0.2px;
  line-height: 1.2;
}

.campo-fechas {
  margin-top: 2px;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.fecha-item .f-etiqueta {
  font-size: 8px;
  font-weight: 600;
  color: #000000;
}

.fecha-item .f-valor {
  font-size: 10px;
  font-weight: 700;
  color: #0d0d0d;
  text-transform: uppercase;
  letter-spacing: 0.1px;
  line-height: 1.1;
}

.firmas-container {
  position: absolute;
  bottom: 8px;
  right: 15px;
  display: flex;
  gap: 25px;
}

.firma-box {
  width: 48px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.firma-placeholder {
  width: 100%;
  height: 30px;
  border-bottom: 1px dashed #999;
  margin-bottom: 8px;
  opacity: 0.6;
  font-size: 5px;
  color: #002699;
  display: flex;
  align-items: center;
  justify-content: center;
  font-style: italic;
}

.firma-box span {
  font-size: 5px;
  font-weight: 600;
  color: #222;
  letter-spacing: 0.3px;
  text-transform: uppercase;
  line-height: 1.1;
}

/* LADO DERECHO (REVERSO) */
.lado-derecho {
  padding: 12px 12px;
}

.header-derecho {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: fit-content;
  position: absolute;
  top: 12px;
  left: 32px;
}

.siglas {
  font-size: 9px;
  font-weight: 700;
  color: #0d0d0d;
  letter-spacing: 0.3px;
  margin-bottom: 3px;
  font-family: 'Courier New', monospace;
}

.escudo-placeholder {
  width: 50px;
  height: 55px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 5px;
  color: #777;
  text-align: center;
  overflow: hidden;
}

.escudo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.footer-derecho {
  display: flex;
  flex-direction: column;
  gap: 8px;
  position: absolute;
  bottom: 12px;
  left: 12px;
  right: 12px;
}

.qr-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.qr-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}

.qr-placeholder {
  width: 100px;
  height: 100px;
  border: 1px solid #000;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 6px;
}

.qr-codigo {
  font-size: 9px;
  font-weight: 700;
  color: #0d0d0d;
  letter-spacing: 0.2px;
  font-family: 'Courier New', monospace;
  text-align: center;
  width: 100px;
}

.metadatos-qr {
  display: flex;
  flex-direction: column;
  gap: 5px;
  flex: 1;
}

.metadatos-derecha {
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: 20px;
  row-gap: 8px;
  flex-grow: 1;
  padding-bottom: 5px;
}

.meta-item {
  display: flex;
  flex-direction: column;
}

.meta-item .m-etiqueta {
  font-size: 7px;
  font-weight: 600;
  color: #3b3b3b;
  letter-spacing: 0.2px;
  text-transform: uppercase;
  line-height: 1.1;
}

.meta-item .m-valor {
  font-size: 10px;
  font-weight: 700;
  color: #0d0d0d;
  margin-top: 1px;
  letter-spacing: 0.1px;
  line-height: 1.2;
}

.meta-item .m-valor-destacado {
  font-size: 8px;
  font-weight: 700;
  color: #0d0d0d;
  margin-top: 1px;
  letter-spacing: 0.1px;
  line-height: 1.2;
}

.qr-url-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  flex-shrink: 0;
  margin-left: auto;
}

.qr-url-label {
  font-size: 9px;
  font-weight: 600;
  color: #000000;
  text-transform: uppercase;
  letter-spacing: 0.2px;
  white-space: nowrap;
}

.qr-url {
  width: 60px !important;
  height: 60px !important;
  padding: 2px;
  border: 1px solid #000;
  background-color: #f5f5f5;
}

.qr-url-text {
  font-size: 6pt;
  font-weight: 500;
  color: #000000;
  max-width: 90px;
  word-break: break-all;
  text-align: center;
  line-height: 1;
}

/* Modal de Bloques */
.modal-bloques {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  animation: slideInModal 0.3s ease;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.modal-header h2 {
  margin: 0;
  font-size: 18px;
}

.btn-close {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: white;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-body-bloques {
  padding: 30px;
}

.info-bloques {
  text-align: center;
  color: #666;
  margin-bottom: 25px;
  font-size: 14px;
}

.grid-bloques {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

.btn-bloque {
  padding: 15px;
  border: 2px solid #667eea;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.btn-bloque:hover:not(:disabled) {
  background: #667eea;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(102, 126, 234, 0.3);
}

.btn-bloque:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.numero-bloque {
  font-size: 14px;
  font-weight: 700;
}

.rango-bloque {
  font-size: 11px;
  color: #999;
  text-align: center;
}

.spinner-mini {
  width: 16px;
  height: 16px;
  border: 2px solid #667eea;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.btn-bloque ion-icon {
  font-size: 20px;
}

.nota-bloques {
  text-align: center;
  color: #999;
  font-size: 12px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.btn-todos-pdf {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 14px;
  margin: 15px 0;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-todos-pdf:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(34, 197, 94, 0.3);
}

.btn-todos-pdf:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@keyframes slideInModal {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media print {
  .carnet-card {
    box-shadow: none;
    border: 0.5px solid #000;
  }
}

/* Estilos para modal Vincular Fotos */
.btn-vincular-fotos {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-vincular-fotos:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.modal-vincular-fotos {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 900px;
  max-height: 85vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-body-vincular {
  overflow-y: auto;
  overflow-x: hidden;
  flex: 1;
}

.content-vincular {
  text-align: center;
  padding: 40px 25px;
}

.info-vincular {
  font-size: 60px;
  margin: 0 0 20px 0;
  opacity: 0.8;
}

.icon-grande {
  font-size: 60px;
  display: inline-block;
}

.content-vincular h3 {
  font-size: 22px;
  color: #333;
  margin: 20px 0 15px 0;
}

.descripcion-vincular {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin: 15px 0;
}

.info-extensiones {
  background: #f0f4ff;
  padding: 12px;
  border-radius: 8px;
  font-size: 13px;
  color: #555;
  margin: 20px 0;
}

.info-extensiones code {
  background: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
  color: #667eea;
}

.resultado-vincular {
  padding: 25px;
}

.resumen-resultado h3 {
  font-size: 18px;
  color: #333;
  margin: 0 0 20px 0;
}

.stats-grid-vincular {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
  margin-bottom: 25px;
}

.stat-card-vincular {
  background: #f8f9fa;
  padding: 12px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  border-left: 4px solid #ddd;
  text-align: center;
}

.stat-card-vincular.success {
  background: #f0fdf4;
  border-left-color: #22c55e;
}

.stat-card-vincular.warning {
  background: #fffbeb;
  border-left-color: #f59e0b;
}

.stat-card-vincular.info {
  background: #eff6ff;
  border-left-color: #3b82f6;
}

.stat-card-vincular.error {
  background: #fef2f2;
  border-left-color: #ef4444;
}

.stat-icon {
  font-size: 24px;
  min-width: 30px;
  text-align: center;
}

.stat-content {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.stat-label {
  font-size: 10px;
  color: #666;
  text-transform: uppercase;
  font-weight: 600;
}

.stat-number {
  font-size: 22px;
  font-weight: 700;
  color: #333;
}

.detalles-vincular {
  margin-top: 30px;
}

.detalles-vincular h4 {
  font-size: 14px;
  color: #333;
  margin: 0 0 15px 0;
  text-transform: uppercase;
  font-weight: 600;
}

.detalles-lista {
  max-height: 280px;
  overflow-y: auto;
  overflow-x: hidden;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fafafa;
}

.detalle-item {
  display: grid;
  grid-template-columns: 70px 1fr auto;
  gap: 10px;
  padding: 10px;
  border-bottom: 1px solid #e5e7eb;
  align-items: center;
  font-size: 12px;
  word-break: break-word;
}

.detalle-item:last-child {
  border-bottom: none;
}

.detalle-item.vinculada {
  background: #f0fdf4;
}

.detalle-item.ya_vinculada {
  background: #fffbeb;
}

.detalle-item.no_encontrado {
  background: #eff6ff;
}

.detalle-item.error {
  background: #fef2f2;
}

.detalle-dni {
  font-weight: 600;
  color: #333;
  font-family: monospace;
}

.detalle-nombre {
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.detalle-estado {
  color: #999;
  font-size: 12px;
  text-align: right;
}

/* Tabs para Vincular/Cargar */
.tabs-vincular {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  border-bottom: 2px solid #e5e7eb;
}

.tab-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #999;
  transition: all 0.3s ease;
  margin-bottom: -2px;
}

.tab-button:hover {
  color: #667eea;
}

.tab-button.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

.tab-content {
  padding: 20px 0;
}

/* Drag and Drop Area */
.drag-drop-area {
  border: 2px dashed #ccc;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #fafafa;
  min-height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.drag-drop-area:hover {
  border-color: #667eea;
  background: #f0f4ff;
}

.drag-drop-area.drag-over {
  border-color: #667eea;
  background: #f0f4ff;
  box-shadow: 0 0 20px rgba(102, 126, 234, 0.2);
}

.drag-drop-content {
  pointer-events: none;
  width: 100%;
}

.drag-icon {
  font-size: 48px;
  color: #667eea;
  margin-bottom: 10px;
  display: block;
}

.drag-drop-area h3 {
  font-size: 18px;
  color: #333;
  margin: 10px 0;
}

.drag-drop-area p {
  color: #666;
  font-size: 13px;
  margin: 5px 0;
}

.drag-info {
  color: #999;
  font-size: 12px !important;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #ddd;
}

/* Preview de Fotos a Cargar */
.preview-fotos-cargar {
  margin-top: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.preview-fotos-cargar h4 {
  font-size: 14px;
  color: #333;
  margin: 0 0 15px 0;
  text-transform: uppercase;
  font-weight: 600;
}

.fotos-preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 12px;
}

.foto-preview-item {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: all 0.3s ease;
}

.foto-preview-item:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.foto-thumb {
  width: 100%;
  height: 80px;
  object-fit: cover;
  display: block;
}

.foto-info {
  padding: 8px;
  background: white;
  min-height: 50px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.foto-nombre {
  font-size: 11px;
  color: #333;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.foto-tamaño {
  font-size: 10px;
  color: #999;
  margin-top: 3px;
}

.btn-remove-foto {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 24px;
  height: 24px;
  background: rgba(239, 68, 68, 0.9);
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  transition: all 0.2s ease;
  opacity: 0;
}

.foto-preview-item:hover .btn-remove-foto {
  opacity: 1;
}

.btn-remove-foto:hover {
  background: rgba(239, 68, 68, 1);
}

/* MODAL DE PROGRESO */
.modal-overlay-progress {
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-progreso {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 500px;
  overflow: hidden;
}

.modal-header-progreso {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.modal-header-progreso h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.modal-body-progreso {
  padding: 30px;
}

.progreso-info {
  text-align: center;
  margin-bottom: 25px;
}

.total-carnets {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 5px 0;
}

.mensaje-progreso {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
  min-height: 20px;
}

.progreso-container {
  margin: 25px 0;
}

.progreso-barra {
  width: 100%;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 10px;
}

.progreso-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
  border-radius: 4px;
}

.progreso-porcentaje {
  text-align: center;
  font-size: 24px;
  font-weight: 700;
  color: #667eea;
}

.progreso-detalles {
  text-align: center;
  font-size: 12px;
  color: #9ca3af;
  margin-top: 15px;
}

.modal-footer-progreso {
  padding: 20px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn-outline {
  padding: 10px 16px;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  color: #374151;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-outline:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.btn-outline:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* SELECTOR DE TAMAÑO DE BLOQUE */
.selector-tamano {
  margin: 20px 0;
  padding: 15px;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.selector-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 10px;
}

.selector-botones {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.btn-tamano {
  padding: 8px 18px;
  border: 1.5px solid #d1d5db;
  background: white;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 60px;
}

.btn-tamano:hover:not(:disabled) {
  border-color: #667eea;
  background: #f3f4ff;
}

.btn-tamano.activo {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.btn-tamano:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-tamano-todos {
  background: white;
  border-color: #10b981;
  color: #10b981;
}

.btn-tamano-todos:hover:not(:disabled) {
  background: #ecfdf5;
  border-color: #10b981;
}

.btn-tamano-todos.activo {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border-color: transparent;
}

.bloques-section {
  margin-top: 15px;
}
</style>
