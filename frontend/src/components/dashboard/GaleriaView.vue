<template>
  <div class="galerias-admin">
    <!-- ════════════════════════════════════════════════════════════════
         NIVEL 1: LISTADO DE TODAS LAS GALERÍAS (ÁLBUMES)
         ════════════════════════════════════════════════════════════════ -->
    <div v-if="!galeriaSeleccionada" class="vista-lista-galerias">
      <!-- Header principal -->
      <div class="admin-header">
        <div class="header-info">
          <div class="header-tag">
            <ion-icon name="albums-outline"></ion-icon>
            <span>Portal Web</span>
          </div>
          <h1>Galerías Fotográficas</h1>
          <p>Crea y administra los diferentes álbumes fotográficos que se exhiben en el sitio web de la comunidad.</p>
        </div>

        <div class="header-actions">
          <a href="/galeria" target="_blank" class="btn-secondary" title="Ver cómo se ve en la web">
            <ion-icon name="open-outline"></ion-icon>
            <span>Ver en la Web</span>
          </a>
          <button class="btn-outline" @click="confirmarRestablecer" title="Restablecer álbumes originales">
            <ion-icon name="refresh-outline"></ion-icon>
            <span>Restablecer</span>
          </button>
          <button class="btn-primary" @click="abrirModalNuevaGaleria">
            <ion-icon name="add-circle-outline"></ion-icon>
            <span>Nueva Galería</span>
          </button>
        </div>
      </div>

      <!-- Tarjetas de métricas -->
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-icon bg-indigo">
            <ion-icon name="albums-outline"></ion-icon>
          </div>
          <div class="metric-data">
            <span class="metric-value">{{ galerias.length }}</span>
            <span class="metric-label">Galerías / Álbumes</span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon bg-emerald">
            <ion-icon name="images-outline"></ion-icon>
          </div>
          <div class="metric-data">
            <span class="metric-value">{{ totalFotosEnSistema }}</span>
            <span class="metric-label">Total de Fotos</span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon bg-amber">
            <ion-icon name="star-outline"></ion-icon>
          </div>
          <div class="metric-data">
            <span class="metric-value">{{ galeriasDestacadasCount }}</span>
            <span class="metric-label">Galerías Destacadas</span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon bg-blue">
            <ion-icon name="pricetags-outline"></ion-icon>
          </div>
          <div class="metric-data">
            <span class="metric-value">{{ categoriasCount }}</span>
            <span class="metric-label">Categorías</span>
          </div>
        </div>
      </div>

      <!-- Barra de Filtros y Búsqueda -->
      <div class="controls-card">
        <div class="controls-top">
          <!-- Búsqueda -->
          <div class="search-box">
            <ion-icon name="search-outline" class="search-icon"></ion-icon>
            <input
              v-model="busqueda"
              type="text"
              placeholder="Buscar galería por nombre, lugar o descripción..."
              class="search-input"
            />
            <button v-if="busqueda" class="clear-search" @click="busqueda = ''">
              <ion-icon name="close-circle"></ion-icon>
            </button>
          </div>

          <div class="quick-filters">
            <div class="filter-group">
              <label>Estado:</label>
              <select v-model="filtroEstado" class="control-select">
                <option value="todos">Todos</option>
                <option value="activos">Visibles</option>
                <option value="ocultos">Ocultos</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Pills de categorías -->
        <div class="categorias-pills">
          <button
            v-for="cat in categoriasPills"
            :key="cat.key"
            :class="['cat-pill', { active: categoriaActiva === cat.key }]"
            @click="categoriaActiva = cat.key"
          >
            <span>{{ cat.label }}</span>
            <span class="pill-count">{{ contarGaleriasPorCat(cat.key) }}</span>
          </button>
        </div>
      </div>

      <!-- Estado de carga -->
      <div v-if="cargando" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando álbumes y galerías...</p>
      </div>

      <!-- Estado vacío -->
      <div v-else-if="galeriasFiltradas.length === 0" class="empty-state">
        <div class="empty-icon">
          <ion-icon name="albums-outline"></ion-icon>
        </div>
        <h3>No se encontraron galerías</h3>
        <p>Crea tu primera galería comunal para empezar a publicar álbumes fotográficos.</p>
        <button class="btn-primary" @click="abrirModalNuevaGaleria">
          <ion-icon name="add-circle-outline"></ion-icon>
          Crear Primera Galería
        </button>
      </div>

      <!-- Grid de Galerías -->
      <div v-else class="galerias-cards-grid">
        <div
          v-for="galeria in galeriasFiltradas"
          :key="galeria.id"
          class="galeria-card"
          :class="{ inactiva: !galeria.activo, destacada: galeria.destacada }"
        >
          <!-- Portada -->
          <div class="galeria-cover" @click="seleccionarGaleria(galeria)">
            <img :src="galeria.portada || '/uploads/img/web/2.png'" :alt="galeria.titulo" loading="lazy" />
            <div class="cover-overlay">
              <ion-icon name="images-outline"></ion-icon>
              <span>Gestionar Fotografías</span>
            </div>

            <!-- Badges sobre la portada -->
            <div class="cover-badges">
              <span class="badge-cat">{{ galeria.categoriaLabel || galeria.categoria }}</span>
              <span v-if="galeria.destacada" class="badge-star">
                <ion-icon name="star"></ion-icon> Destacada
              </span>
            </div>

            <div class="cover-photos-count">
              <ion-icon name="camera-outline"></ion-icon>
              <span>{{ galeria.fotos?.length || 0 }} fotos</span>
            </div>
          </div>

          <!-- Contenido de la tarjeta -->
          <div class="galeria-content">
            <div class="galeria-meta-row">
              <span v-if="galeria.fecha" class="meta-item">
                <ion-icon name="calendar-outline"></ion-icon> {{ galeria.fecha }}
              </span>
              <span v-if="galeria.lugar" class="meta-item">
                <ion-icon name="location-outline"></ion-icon> {{ galeria.lugar }}
              </span>
            </div>

            <h3 class="galeria-title" @click="seleccionarGaleria(galeria)" :title="galeria.titulo">
              {{ galeria.titulo }}
            </h3>
            <p class="galeria-desc">{{ galeria.descripcion || 'Sin descripción ingresada.' }}</p>

            <!-- Tira previa de miniaturas si tiene fotos -->
            <div v-if="galeria.fotos && galeria.fotos.length > 0" class="mini-thumbs-strip">
              <div
                v-for="f in galeria.fotos.slice(0, 4)"
                :key="f.id"
                class="mini-thumb"
                @click="seleccionarGaleria(galeria)"
              >
                <img :src="f.img" :alt="f.titulo" />
              </div>
              <div v-if="galeria.fotos.length > 4" class="mini-thumb-more" @click="seleccionarGaleria(galeria)">
                +{{ galeria.fotos.length - 4 }}
              </div>
            </div>

            <!-- Acciones -->
            <div class="galeria-actions">
              <button class="btn-manage" @click="seleccionarGaleria(galeria)">
                <ion-icon name="images-outline"></ion-icon>
                <span>Administrar Fotos ({{ galeria.fotos?.length || 0 }})</span>
              </button>

              <div class="action-icons">
                <button
                  class="btn-icon"
                  :class="{ active: galeria.activo }"
                  @click="toggleActivoGaleria(galeria)"
                  :title="galeria.activo ? 'Ocultar de la web' : 'Hacer visible en la web'"
                >
                  <ion-icon :name="galeria.activo ? 'eye-outline' : 'eye-off-outline'"></ion-icon>
                </button>
                <button class="btn-icon btn-edit" @click="abrirModalEditarGaleria(galeria)" title="Editar información del álbum">
                  <ion-icon name="create-outline"></ion-icon>
                </button>
                <button class="btn-icon btn-danger" @click="confirmarEliminarGaleria(galeria)" title="Eliminar galería">
                  <ion-icon name="trash-outline"></ion-icon>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ════════════════════════════════════════════════════════════════
         NIVEL 2: GESTOR DE FOTOS DE UNA GALERÍA SELECCIONADA
         ════════════════════════════════════════════════════════════════ -->
    <div v-else class="vista-detalle-galeria">
      <!-- Breadcrumb y navegación superior -->
      <div class="breadcrumb-bar">
        <button class="btn-back" @click="galeriaSeleccionada = null">
          <ion-icon name="arrow-back-outline"></ion-icon>
          <span>Volver a todas las Galerías</span>
        </button>
        <div class="breadcrumb-path">
          <span>Galerías</span>
          <ion-icon name="chevron-forward-outline"></ion-icon>
          <strong>{{ galeriaSeleccionada.titulo }}</strong>
        </div>
      </div>

      <!-- Banner de la Galería seleccionada -->
      <div class="galeria-hero-card">
        <div class="hero-cover-wrap">
          <img :src="galeriaSeleccionada.portada || '/uploads/img/web/2.png'" :alt="galeriaSeleccionada.titulo" />
        </div>
        <div class="hero-info">
          <div class="hero-tags">
            <span class="badge-cat">{{ galeriaSeleccionada.categoriaLabel || galeriaSeleccionada.categoria }}</span>
            <span v-if="galeriaSeleccionada.destacada" class="badge-star">
              <ion-icon name="star"></ion-icon> Destacada
            </span>
            <span :class="galeriaSeleccionada.activo ? 'status-active' : 'status-hidden'" class="status-pill">
              {{ galeriaSeleccionada.activo ? 'Visible en Web' : 'Oculta' }}
            </span>
          </div>

          <h2>{{ galeriaSeleccionada.titulo }}</h2>
          <p>{{ galeriaSeleccionada.descripcion || 'Sin descripción' }}</p>

          <div class="hero-meta">
            <span v-if="galeriaSeleccionada.fecha">
              <ion-icon name="calendar-outline"></ion-icon> {{ galeriaSeleccionada.fecha }}
            </span>
            <span v-if="galeriaSeleccionada.lugar">
              <ion-icon name="location-outline"></ion-icon> {{ galeriaSeleccionada.lugar }}
            </span>
            <span>
              <ion-icon name="images-outline"></ion-icon> {{ galeriaSeleccionada.fotos?.length || 0 }} fotografías
            </span>
          </div>
        </div>

        <div class="hero-actions">
          <button class="btn-primary btn-add-photo" @click="abrirModalNuevaFoto">
            <ion-icon name="add-circle-outline"></ion-icon>
            <span>Agregar Foto</span>
          </button>
          <button class="btn-secondary" @click="abrirModalEditarGaleria(galeriaSeleccionada)">
            <ion-icon name="create-outline"></ion-icon>
            <span>Editar Datos de Galería</span>
          </button>
        </div>
      </div>

      <!-- ════════════════════════════════════════════════════════════════
           ZONA DE CARGA RÁPIDA POR ARRASTRE MÚLTIPLE (DRAG & DROP)
           ════════════════════════════════════════════════════════════════ -->
      <div
        class="batch-dropzone"
        :class="{ 'drag-over': arrastrandoSobreZona, 'is-uploading': subiendoBatch }"
        @dragover.prevent="arrastrandoSobreZona = true"
        @dragenter.prevent="arrastrandoSobreZona = true"
        @dragleave="onDragLeave"
        @drop.prevent="onDropMultiplesFotos"
        @click="triggerMultiFileInput"
      >
        <input
          ref="multiFileInputRef"
          type="file"
          multiple
          accept="image/png, image/jpeg, image/jpg, image/webp"
          class="hidden-file-input"
          @change="onMultiFilesSelected"
        />

        <div v-if="!subiendoBatch" class="batch-content">
          <div class="batch-icon-ring">
            <ion-icon name="cloud-upload-outline"></ion-icon>
          </div>
          <div class="batch-texts">
            <h4>Arrastra y suelta múltiples fotos aquí</h4>
            <p>Puedes arrastrar y soltar <strong>varias fotos a la vez</strong> desde tu computadora (JPG, PNG, WEBP), o hacer clic para seleccionarlas en lote.</p>
          </div>
          <button type="button" class="btn-select-batch" @click.stop="triggerMultiFileInput">
            <ion-icon name="images-outline"></ion-icon>
            <span>Seleccionar Fotos Múltiples</span>
          </button>
        </div>

        <div v-else class="batch-uploading">
          <div class="batch-progress-header">
            <div class="batch-spinner"></div>
            <div class="batch-progress-texts">
              <h4>Subiendo fotografías al álbum...</h4>
              <p>Procesando imagen {{ batchProgreso.actual }} de {{ batchProgreso.total }} ({{ batchProgreso.porcentaje }}%)</p>
            </div>
          </div>
          <div class="batch-progress-bar">
            <div class="batch-progress-fill" :style="{ width: batchProgreso.porcentaje + '%' }"></div>
          </div>
        </div>
      </div>

      <!-- Sección de Fotos de esta Galería -->
      <div class="fotos-section-header">
        <div>
          <h3>Fotografías del Álbum</h3>
          <p>Organiza, destaca o añade nuevas imágenes pertenecientes a esta galería.</p>
        </div>
        <button class="btn-primary" @click="abrirModalNuevaFoto">
          <ion-icon name="cloud-upload-outline"></ion-icon>
          <span>Nueva Fotografía</span>
        </button>
      </div>

      <!-- Estado vacío si el álbum no tiene fotos -->
      <div v-if="!galeriaSeleccionada.fotos || galeriaSeleccionada.fotos.length === 0" class="empty-state">
        <div class="empty-icon">
          <ion-icon name="images-outline"></ion-icon>
        </div>
        <h3>Este álbum aún no tiene fotos</h3>
        <p>Agrega la primera imagen para que los visitantes puedan contemplarla en la web.</p>
        <button class="btn-primary" @click="abrirModalNuevaFoto">
          <ion-icon name="add-circle-outline"></ion-icon>
          Agregar Foto a este Álbum
        </button>
      </div>

      <!-- Cuadrícula de fotos dentro del álbum -->
      <div v-else class="fotos-album-grid">
        <div
          v-for="(foto, index) in galeriaSeleccionada.fotos"
          :key="foto.id"
          class="foto-card"
          :class="{ grande: foto.grande, inactiva: !foto.activo }"
        >
          <!-- Imagen de la foto -->
          <div class="foto-card-img" @click="abrirLightbox(foto)">
            <img :src="foto.img" :alt="foto.titulo" loading="lazy" />
            <div class="foto-card-overlay">
              <ion-icon name="scan-outline"></ion-icon>
              <span>Ver Ampliada</span>
            </div>

            <div class="foto-badges-top">
              <span v-if="foto.grande" class="badge-grande">
                <ion-icon name="sparkles"></ion-icon> 2x Ancha
              </span>
            </div>

            <div class="foto-status-badge" :class="foto.activo ? 'status-active' : 'status-hidden'">
              <span class="status-dot"></span>
              {{ foto.activo ? 'Visible' : 'Oculta' }}
            </div>
          </div>

          <!-- Datos de la foto -->
          <div class="foto-card-body">
            <div class="foto-meta-row">
              <span class="foto-orden">#{{ index + 1 }}</span>
              <div class="foto-order-btns">
                <button
                  class="btn-order"
                  :disabled="index === 0"
                  @click="moverFotoInterna(index, -1)"
                  title="Mover antes"
                >
                  <ion-icon name="arrow-up-outline"></ion-icon>
                </button>
                <button
                  class="btn-order"
                  :disabled="index === galeriaSeleccionada.fotos.length - 1"
                  @click="moverFotoInterna(index, 1)"
                  title="Mover después"
                >
                  <ion-icon name="arrow-down-outline"></ion-icon>
                </button>
              </div>
            </div>

            <h4 class="foto-titulo" :title="foto.titulo">{{ foto.titulo }}</h4>
            <p class="foto-desc">{{ foto.desc || 'Sin descripción' }}</p>

            <!-- Acciones de la foto -->
            <div class="foto-card-actions">
              <button
                class="action-btn"
                :class="{ active: foto.grande }"
                @click="toggleGrandeFoto(foto)"
                :title="foto.grande ? 'Cambiar a tamaño normal' : 'Destacar a 2 columnas'"
              >
                <ion-icon :name="foto.grande ? 'contract-outline' : 'expand-outline'"></ion-icon>
                <span>{{ foto.grande ? 'Normal' : 'Destacar' }}</span>
              </button>

              <button
                class="action-btn"
                :class="{ active: foto.activo }"
                @click="toggleActivoFoto(foto)"
                :title="foto.activo ? 'Ocultar foto' : 'Mostrar foto'"
              >
                <ion-icon :name="foto.activo ? 'eye-outline' : 'eye-off-outline'"></ion-icon>
                <span>{{ foto.activo ? 'Visible' : 'Oculto' }}</span>
              </button>

              <button
                class="action-btn"
                @click="usarComoPortada(foto)"
                title="Establecer como foto de portada del álbum"
              >
                <ion-icon name="image-outline"></ion-icon>
                <span>Portada</span>
              </button>

              <button class="action-btn edit-btn" @click="abrirModalEditarFoto(foto)" title="Editar foto">
                <ion-icon name="create-outline"></ion-icon>
              </button>

              <button class="action-btn delete-btn" @click="confirmarEliminarFoto(foto)" title="Eliminar foto">
                <ion-icon name="trash-outline"></ion-icon>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ════════════════════════════════════════════════════════════════
         MODALES
         ════════════════════════════════════════════════════════════════ -->

    <!-- MODAL 1: CREAR / EDITAR GALERÍA (ÁLBUM) -->
    <div v-if="modalGaleriaVisible" class="modal-overlay" @click.self="cerrarModalGaleria">
      <div class="modal-box modal-lg">
        <div class="modal-header">
          <div class="modal-title-group">
            <ion-icon :name="editandoGaleriaId ? 'create-outline' : 'albums-outline'"></ion-icon>
            <h2>{{ editandoGaleriaId ? 'Editar Galería' : 'Nueva Galería Fotográfica' }}</h2>
          </div>
          <button class="btn-close" @click="cerrarModalGaleria">
            <ion-icon name="close-outline"></ion-icon>
          </button>
        </div>

        <form @submit.prevent="guardarGaleria" class="modal-body">
          <div class="modal-columns">
            <!-- Columna Izquierda: Portada y Switches -->
            <div class="modal-col">
              <label class="form-label">Foto de Portada de la Galería</label>

              <!-- Upload o URL de portada -->
              <div class="upload-dropzone" @click="triggerPortadaInput">
                <input
                  ref="portadaInputRef"
                  type="file"
                  accept="image/png, image/jpeg, image/jpg, image/webp"
                  class="hidden-file-input"
                  @change="onPortadaSelected"
                />
                <div v-if="!formGaleria.portada" class="dropzone-placeholder">
                  <ion-icon name="cloud-upload-outline" class="drop-icon"></ion-icon>
                  <p class="drop-text">Haz clic para subir imagen de portada</p>
                  <span class="drop-hint">JPG, PNG, WEBP (hasta 8MB)</span>
                </div>
                <div v-else class="preview-container">
                  <img :src="formGaleria.portada" alt="Portada de galería" class="img-preview" />
                  <div class="preview-change-overlay">
                    <ion-icon name="camera-outline"></ion-icon>
                    <span>Cambiar Portada</span>
                  </div>
                </div>
              </div>

              <!-- Input URL alternativo -->
              <div class="form-group">
                <label class="sub-label">O ingresa URL de la imagen:</label>
                <input
                  v-model="formGaleria.portada"
                  type="text"
                  placeholder="Ej: /uploads/img/web/2.png o https://..."
                  class="form-input"
                />
              </div>

              <!-- Switches -->
              <div class="form-switch-card">
                <div class="switch-info">
                  <span class="switch-title">Galería Destacada</span>
                  <span class="switch-subtitle">Aparecerá con un badge dorado en la cabecera de la web pública</span>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="formGaleria.destacada" />
                  <span class="slider round"></span>
                </label>
              </div>

              <div class="form-switch-card">
                <div class="switch-info">
                  <span class="switch-title">Visible en el Sitio Web</span>
                  <span class="switch-subtitle">Si se desactiva, el álbum quedará guardado pero no visible para visitantes</span>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="formGaleria.activo" />
                  <span class="slider round"></span>
                </label>
              </div>
            </div>

            <!-- Columna Derecha: Información textual -->
            <div class="modal-col">
              <div class="form-group">
                <label class="form-label required">Título del Álbum / Galería</label>
                <input
                  v-model="formGaleria.titulo"
                  type="text"
                  class="form-input"
                  placeholder="Ej: Asamblea General Ordinaria 2026"
                  required
                />
              </div>

              <div class="form-group">
                <label class="form-label required">Categoría</label>
                <select v-model="formGaleria.categoria" class="form-select" @change="alCambiarCatGaleria">
                  <option v-for="cat in categoriasDisponibles" :key="cat.key" :value="cat.key">
                    {{ cat.label }}
                  </option>
                  <option value="__nueva__">+ Crear Nueva Categoría...</option>
                </select>

                <div v-if="esNuevaCatGaleria" class="nueva-cat-box">
                  <label class="sub-label">Nombre de la nueva categoría:</label>
                  <input
                    v-model="nuevaCatGaleriaNombre"
                    type="text"
                    placeholder="Ej: Danzas y Festividades"
                    class="form-input"
                    @input="autoGenerarCatGaleria"
                  />
                </div>
              </div>

              <div class="form-row-2">
                <div class="form-group">
                  <label class="form-label">Fecha o Año</label>
                  <input
                    v-model="formGaleria.fecha"
                    type="text"
                    class="form-input"
                    placeholder="Ej: Mayo 2026"
                  />
                </div>
                <div class="form-group">
                  <label class="form-label">Lugar o Sector</label>
                  <input
                    v-model="formGaleria.lugar"
                    type="text"
                    class="form-input"
                    placeholder="Ej: Anexo Tumilaca"
                  />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Descripción</label>
                <textarea
                  v-model="formGaleria.descripcion"
                  rows="3"
                  class="form-textarea"
                  placeholder="Explica de qué trata este álbum o acontecimiento..."
                ></textarea>
              </div>

              <div class="form-group">
                <label class="form-label">Orden de Visualización</label>
                <input
                  v-model.number="formGaleria.orden"
                  type="number"
                  min="1"
                  class="form-input"
                  placeholder="1, 2, 3..."
                />
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cerrarModalGaleria">Cancelar</button>
            <button type="submit" class="btn-save" :disabled="guardando || !formGaleria.titulo">
              <ion-icon v-if="guardando" name="sync-outline" class="spin"></ion-icon>
              <ion-icon v-else name="checkmark-outline"></ion-icon>
              <span>{{ guardando ? 'Guardando...' : (editandoGaleriaId ? 'Actualizar Galería' : 'Crear Galería') }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL 2: CREAR / EDITAR FOTO DENTRO DE LA GALERÍA -->
    <div v-if="modalFotoVisible" class="modal-overlay" @click.self="cerrarModalFoto">
      <div class="modal-box modal-lg">
        <div class="modal-header">
          <div class="modal-title-group">
            <ion-icon :name="editandoFotoId ? 'create-outline' : 'cloud-upload-outline'"></ion-icon>
            <h2>{{ editandoFotoId ? 'Editar Fotografía' : 'Agregar Fotografía al Álbum' }}</h2>
          </div>
          <button class="btn-close" @click="cerrarModalFoto">
            <ion-icon name="close-outline"></ion-icon>
          </button>
        </div>

        <form @submit.prevent="guardarFoto" class="modal-body">
          <div class="modal-columns">
            <div class="modal-col">
              <label class="form-label required">Imagen de la Foto</label>

              <!-- Upload o URL -->
              <div class="upload-dropzone" @click="triggerFotoInput">
                <input
                  ref="fotoInputRef"
                  type="file"
                  multiple
                  accept="image/png, image/jpeg, image/jpg, image/webp"
                  class="hidden-file-input"
                  @change="onFotoSelected"
                />
                <div v-if="!formFoto.img" class="dropzone-placeholder">
                  <ion-icon name="cloud-upload-outline" class="drop-icon"></ion-icon>
                  <p class="drop-text">Haz clic o arrastra fotos aquí</p>
                  <span class="drop-hint">Puedes seleccionar una o varias fotos a la vez (hasta 8MB c/u)</span>
                </div>
                <div v-else class="preview-container">
                  <img :src="formFoto.img" alt="Foto preview" class="img-preview" />
                  <div class="preview-change-overlay">
                    <ion-icon name="camera-outline"></ion-icon>
                    <span>Cambiar Foto</span>
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label class="sub-label">O ingresa URL de la imagen:</label>
                <input
                  v-model="formFoto.img"
                  type="text"
                  placeholder="Ej: /uploads/img/web/2.png o https://..."
                  class="form-input"
                  required
                />
              </div>

              <!-- Switches -->
              <div class="form-switch-card">
                <div class="switch-info">
                  <span class="switch-title">Foto Destacada (2 columnas)</span>
                  <span class="switch-subtitle">Ocupará el doble de ancho en la cuadrícula visual</span>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="formFoto.grande" />
                  <span class="slider round"></span>
                </label>
              </div>

              <div class="form-switch-card">
                <div class="switch-info">
                  <span class="switch-title">Visible en la Galería Web</span>
                  <span class="switch-subtitle">Desactivar si aún no deseas publicarla</span>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="formFoto.activo" />
                  <span class="slider round"></span>
                </label>
              </div>
            </div>

            <div class="modal-col">
              <div class="form-group">
                <label class="form-label required">Título de la Fotografía</label>
                <input
                  v-model="formFoto.titulo"
                  type="text"
                  class="form-input"
                  placeholder="Ej: Vista panorámica de los asistentes"
                  required
                />
              </div>

              <div class="form-group">
                <label class="form-label">Descripción o Pie de Foto</label>
                <textarea
                  v-model="formFoto.desc"
                  rows="4"
                  class="form-textarea"
                  placeholder="Contexto, personas retratadas o detalles del momento..."
                ></textarea>
              </div>

              <div class="form-group">
                <label class="form-label">Orden</label>
                <input
                  v-model.number="formFoto.orden"
                  type="number"
                  min="1"
                  class="form-input"
                  placeholder="1, 2, 3..."
                />
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cerrarModalFoto">Cancelar</button>
            <button type="submit" class="btn-save" :disabled="guardando || !formFoto.img || !formFoto.titulo">
              <ion-icon v-if="guardando" name="sync-outline" class="spin"></ion-icon>
              <ion-icon v-else name="checkmark-outline"></ion-icon>
              <span>{{ guardando ? 'Guardando...' : (editandoFotoId ? 'Actualizar Foto' : 'Agregar al Álbum') }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL CONFIRMAR ELIMINACIÓN DE GALERÍA -->
    <div v-if="galeriaAEliminar" class="modal-overlay" @click.self="galeriaAEliminar = null">
      <div class="modal-box modal-sm">
        <div class="modal-alert-icon delete">
          <ion-icon name="trash-outline"></ion-icon>
        </div>
        <h3 class="modal-alert-title">¿Eliminar Galería Completa?</h3>
        <p class="modal-alert-msg">
          Se eliminará la galería <strong>"{{ galeriaAEliminar.titulo }}"</strong> junto con todas sus fotografías asociadas.
        </p>
        <div class="modal-alert-actions">
          <button class="btn-cancel" @click="galeriaAEliminar = null">Cancelar</button>
          <button class="btn-danger-confirm" @click="ejecutarEliminarGaleria">
            <ion-icon name="trash-outline"></ion-icon>
            Sí, Eliminar
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL CONFIRMAR ELIMINACIÓN DE FOTO -->
    <div v-if="fotoAEliminar" class="modal-overlay" @click.self="fotoAEliminar = null">
      <div class="modal-box modal-sm">
        <div class="modal-alert-icon delete">
          <ion-icon name="trash-outline"></ion-icon>
        </div>
        <h3 class="modal-alert-title">¿Eliminar Fotografía?</h3>
        <p class="modal-alert-msg">
          Se quitará <strong>"{{ fotoAEliminar.titulo }}"</strong> de este álbum.
        </p>
        <div class="modal-alert-actions">
          <button class="btn-cancel" @click="fotoAEliminar = null">Cancelar</button>
          <button class="btn-danger-confirm" @click="ejecutarEliminarFoto">
            <ion-icon name="trash-outline"></ion-icon>
            Sí, Eliminar
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL CONFIRMAR RESTABLECER -->
    <div v-if="mostrarConfirmarRestablecer" class="modal-overlay" @click.self="mostrarConfirmarRestablecer = false">
      <div class="modal-box modal-sm">
        <div class="modal-alert-icon warning">
          <ion-icon name="alert-circle-outline"></ion-icon>
        </div>
        <h3 class="modal-alert-title">¿Restablecer galerías iniciales?</h3>
        <p class="modal-alert-msg">
          Se restaurarán los 3 álbumes institucionales por defecto (Identidad y Tradición, Territorio y Paisajes, Trabajo Agrícola y ECOSER).
        </p>
        <div class="modal-alert-actions">
          <button class="btn-cancel" @click="mostrarConfirmarRestablecer = false">Cancelar</button>
          <button class="btn-warning-confirm" @click="ejecutarRestablecer">
            <ion-icon name="refresh-outline"></ion-icon>
            Sí, Restablecer
          </button>
        </div>
      </div>
    </div>

    <!-- LIGHTBOX PREVIEW -->
    <div v-if="lightboxFoto" class="lightbox" @click.self="lightboxFoto = null">
      <button class="lb-close" @click="lightboxFoto = null">
        <ion-icon name="close-outline"></ion-icon>
      </button>
      <div class="lb-content">
        <div class="lb-img-wrap">
          <img :src="lightboxFoto.img" :alt="lightboxFoto.titulo" />
        </div>
        <div class="lb-info">
          <h3>{{ lightboxFoto.titulo }}</h3>
          <p>{{ lightboxFoto.desc || 'Sin descripción adicional.' }}</p>
        </div>
      </div>
    </div>

    <!-- TOAST NOTIFICACIÓN -->
    <Transition name="toast">
      <div v-if="toast.visible" :class="['admin-toast', toast.type]">
        <ion-icon :name="toast.icon"></ion-icon>
        <span>{{ toast.message }}</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { galeriaService, CATEGORIAS_PREDEFINIDAS } from '@/services/galeria.service'

const cargando = ref(true)
const guardando = ref(false)
const galerias = ref([])
const galeriaSeleccionada = ref(null)

// Filtros y búsqueda
const busqueda = ref('')
const categoriaActiva = ref('todas')
const filtroEstado = ref('todos')

// Modales Galería
const modalGaleriaVisible = ref(false)
const editandoGaleriaId = ref(null)
const portadaInputRef = ref(null)
const esNuevaCatGaleria = ref(false)
const nuevaCatGaleriaNombre = ref('')

const formGaleria = ref({
  titulo: '',
  descripcion: '',
  categoria: 'comunidad',
  categoriaLabel: 'Comunidad',
  portada: '',
  fecha: '',
  lugar: '',
  destacada: false,
  orden: 1,
  activo: true
})

// Modales Foto
const modalFotoVisible = ref(false)
const editandoFotoId = ref(null)
const fotoInputRef = ref(null)

const formFoto = ref({
  titulo: '',
  desc: '',
  img: '',
  grande: false,
  orden: 1,
  activo: true
})

// Carga Múltiple (Drag & Drop en Álbum)
const arrastrandoSobreZona = ref(false)
const multiFileInputRef = ref(null)
const subiendoBatch = ref(false)
const batchProgreso = ref({ actual: 0, total: 0, porcentaje: 0 })

// Confirmaciones
const galeriaAEliminar = ref(null)
const fotoAEliminar = ref(null)
const mostrarConfirmarRestablecer = ref(false)
const lightboxFoto = ref(null)

// Toast
const toast = ref({
  visible: false,
  message: '',
  type: 'success',
  icon: 'checkmark-circle'
})

function notificar(message, type = 'success') {
  toast.value = {
    visible: true,
    message,
    type,
    icon: type === 'success' ? 'checkmark-circle' : 'alert-circle'
  }
  setTimeout(() => {
    toast.value.visible = false
  }, 3500)
}

// Cargar galerías
async function cargarGalerias() {
  cargando.value = true
  try {
    const data = await galeriaService.obtenerAdmin()
    galerias.value = data
    // Si hay una seleccionada actualmente, refrescar su referencia
    if (galeriaSeleccionada.value) {
      const refreshed = data.find(g => String(g.id) === String(galeriaSeleccionada.value.id))
      if (refreshed) {
        galeriaSeleccionada.value = refreshed
      }
    }
  } catch (err) {
    console.error('Error cargando galerías:', err)
    notificar('Error al cargar galerías', 'error')
  } finally {
    cargando.value = false
  }
}

onMounted(() => {
  cargarGalerias()
})

// Métricas computadas
const totalFotosEnSistema = computed(() => {
  return galerias.value.reduce((acc, g) => acc + (g.fotos?.length || 0), 0)
})

const galeriasDestacadasCount = computed(() => {
  return galerias.value.filter(g => g.destacada).length
})

const categoriasDisponibles = computed(() => {
  const map = new Map()
  CATEGORIAS_PREDEFINIDAS.forEach(c => map.set(c.key, c.label))
  galerias.value.forEach(g => {
    if (g.categoria && !map.has(g.categoria)) {
      map.set(g.categoria, g.categoriaLabel || g.categoria)
    }
  })
  return Array.from(map.entries()).map(([key, label]) => ({ key, label }))
})

const categoriasCount = computed(() => categoriasDisponibles.value.length)

const categoriasPills = computed(() => {
  const list = [{ key: 'todas', label: 'Todos los álbumes' }]
  categoriasDisponibles.value.forEach(c => list.push(c))
  return list
})

function contarGaleriasPorCat(key) {
  if (key === 'todas') return galerias.value.length
  return galerias.value.filter(g => g.categoria === key).length
}

// Filtrado de galerías
const galeriasFiltradas = computed(() => {
  return galerias.value.filter(g => {
    if (busqueda.value.trim()) {
      const q = busqueda.value.toLowerCase()
      const matchTitulo = g.titulo?.toLowerCase().includes(q)
      const matchDesc = g.descripcion?.toLowerCase().includes(q)
      const matchLugar = g.lugar?.toLowerCase().includes(q)
      const matchCat = (g.categoriaLabel || g.categoria)?.toLowerCase().includes(q)
      if (!matchTitulo && !matchDesc && !matchLugar && !matchCat) return false
    }

    if (categoriaActiva.value !== 'todas' && g.categoria !== categoriaActiva.value) {
      return false
    }

    if (filtroEstado.value === 'activos' && g.activo === false) return false
    if (filtroEstado.value === 'ocultos' && g.activo !== false) return false

    return true
  })
})

// Navegar a detalle de galería
function seleccionarGaleria(g) {
  galeriaSeleccionada.value = g
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// ──────────────────────────────────────────────
// GESTIÓN DE GALERÍA (ÁLBUM)
// ──────────────────────────────────────────────
function abrirModalNuevaGaleria() {
  editandoGaleriaId.value = null
  esNuevaCatGaleria.value = false
  nuevaCatGaleriaNombre.value = ''

  const maxOrden = galerias.value.reduce((max, g) => Math.max(max, g.orden || 0), 0)

  formGaleria.value = {
    titulo: '',
    descripcion: '',
    categoria: 'comunidad',
    categoriaLabel: 'Comunidad',
    portada: '',
    fecha: '',
    lugar: '',
    destacada: false,
    orden: maxOrden + 1,
    activo: true
  }

  modalGaleriaVisible.value = true
}

function abrirModalEditarGaleria(g) {
  editandoGaleriaId.value = g.id
  esNuevaCatGaleria.value = false
  nuevaCatGaleriaNombre.value = ''

  formGaleria.value = {
    titulo: g.titulo,
    descripcion: g.descripcion || '',
    categoria: g.categoria || 'comunidad',
    categoriaLabel: g.categoriaLabel || g.categoria,
    portada: g.portada || '',
    fecha: g.fecha || '',
    lugar: g.lugar || '',
    destacada: !!g.destacada,
    orden: g.orden || 1,
    activo: g.activo !== false
  }

  modalGaleriaVisible.value = true
}

function cerrarModalGaleria() {
  modalGaleriaVisible.value = false
  editandoGaleriaId.value = null
}

function triggerPortadaInput() {
  portadaInputRef.value?.click()
}

async function onPortadaSelected(e) {
  const file = e.target.files?.[0]
  if (!file) return

  try {
    const url = await galeriaService.subirImagen(file)
    formGaleria.value.portada = url
    notificar('Portada cargada con éxito')
  } catch (err) {
    console.error(err)
    notificar('Error al procesar la imagen', 'error')
  }
}

function alCambiarCatGaleria() {
  if (formGaleria.value.categoria === '__nueva__') {
    esNuevaCatGaleria.value = true
    nuevaCatGaleriaNombre.value = ''
  } else {
    esNuevaCatGaleria.value = false
    const match = categoriasDisponibles.value.find(c => c.key === formGaleria.value.categoria)
    formGaleria.value.categoriaLabel = match?.label || formGaleria.value.categoria
  }
}

function autoGenerarCatGaleria() {
  const slug = nuevaCatGaleriaNombre.value
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '')

  formGaleria.value.categoria = slug || 'personalizada'
  formGaleria.value.categoriaLabel = nuevaCatGaleriaNombre.value || 'Personalizada'
}

async function guardarGaleria() {
  if (!formGaleria.value.titulo.trim()) {
    notificar('Ingresa el título de la galería', 'error')
    return
  }

  if (esNuevaCatGaleria.value && nuevaCatGaleriaNombre.value.trim()) {
    autoGenerarCatGaleria()
  }

  guardando.value = true
  try {
    if (editandoGaleriaId.value) {
      await galeriaService.actualizarGaleria(editandoGaleriaId.value, formGaleria.value)
      notificar('Galería actualizada correctamente')
    } else {
      const nueva = await galeriaService.crearGaleria(formGaleria.value)
      notificar(`Galería "${nueva.titulo}" creada`)
    }
    cerrarModalGaleria()
    await cargarGalerias()
  } catch (err) {
    console.error(err)
    notificar('Error al guardar la galería', 'error')
  } finally {
    guardando.value = false
  }
}

async function toggleActivoGaleria(g) {
  try {
    const nuevoEstado = !g.activo
    await galeriaService.actualizarGaleria(g.id, { activo: nuevoEstado })
    g.activo = nuevoEstado
    notificar(nuevoEstado ? 'Galería ahora visible' : 'Galería ocultada de la web')
  } catch (err) {
    console.error(err)
  }
}

function confirmarEliminarGaleria(g) {
  galeriaAEliminar.value = g
}

async function ejecutarEliminarGaleria() {
  if (!galeriaAEliminar.value) return
  try {
    await galeriaService.eliminarGaleria(galeriaAEliminar.value.id)
    notificar('Galería eliminada con éxito')
    if (galeriaSeleccionada.value?.id === galeriaAEliminar.value.id) {
      galeriaSeleccionada.value = null
    }
    galeriaAEliminar.value = null
    await cargarGalerias()
  } catch (err) {
    console.error(err)
    notificar('Error al eliminar galería', 'error')
  }
}

// ──────────────────────────────────────────────
// GESTIÓN DE FOTOS DENTRO DE UNA GALERÍA
// ──────────────────────────────────────────────
function abrirModalNuevaFoto() {
  if (!galeriaSeleccionada.value) return

  editandoFotoId.value = null
  const fotosActuales = galeriaSeleccionada.value.fotos || []
  const maxOrden = fotosActuales.reduce((max, f) => Math.max(max, f.orden || 0), 0)

  formFoto.value = {
    titulo: '',
    desc: '',
    img: '',
    grande: false,
    orden: maxOrden + 1,
    activo: true
  }

  modalFotoVisible.value = true
}

function abrirModalEditarFoto(foto) {
  editandoFotoId.value = foto.id

  formFoto.value = {
    titulo: foto.titulo,
    desc: foto.desc || '',
    img: foto.img,
    grande: !!foto.grande,
    orden: foto.orden || 1,
    activo: foto.activo !== false
  }

  modalFotoVisible.value = true
}

function cerrarModalFoto() {
  modalFotoVisible.value = false
  editandoFotoId.value = null
}

function triggerFotoInput() {
  fotoInputRef.value?.click()
}

function triggerMultiFileInput() {
  if (subiendoBatch.value) return
  multiFileInputRef.value?.click()
}

function onDragLeave(e) {
  if (e.currentTarget && e.relatedTarget && !e.currentTarget.contains(e.relatedTarget)) {
    arrastrandoSobreZona.value = false
  }
}

async function procesarArchivosMultiples(files) {
  if (!galeriaSeleccionada.value) return
  const validFiles = Array.from(files).filter(f => f.type.startsWith('image/'))

  if (validFiles.length === 0) {
    notificar('Selecciona archivos de imagen válidos (JPG, PNG, WEBP)', 'error')
    return
  }

  subiendoBatch.value = true
  batchProgreso.value = {
    actual: 0,
    total: validFiles.length,
    porcentaje: 0
  }

  try {
    await galeriaService.subirMultiplesFotos(
      galeriaSeleccionada.value.id,
      validFiles,
      (actual, total) => {
        batchProgreso.value = {
          actual,
          total,
          porcentaje: Math.round((actual / total) * 100)
        }
      }
    )

    notificar(`¡${validFiles.length} fotografías agregadas con éxito al álbum!`)
    await cargarGalerias()
  } catch (err) {
    console.error('Error en subida múltiple:', err)
    notificar('Error al subir algunas fotografías', 'error')
  } finally {
    subiendoBatch.value = false
    arrastrandoSobreZona.value = false
  }
}

async function onDropMultiplesFotos(e) {
  arrastrandoSobreZona.value = false
  const files = e.dataTransfer?.files
  if (files && files.length > 0) {
    await procesarArchivosMultiples(files)
  }
}

async function onMultiFilesSelected(e) {
  const files = e.target.files
  if (files && files.length > 0) {
    await procesarArchivosMultiples(files)
    e.target.value = ''
  }
}

async function onFotoSelected(e) {
  const files = e.target.files
  if (!files || files.length === 0) return

  // Si seleccionó más de 1 archivo desde el modal, procesar en lote
  if (files.length > 1) {
    cerrarModalFoto()
    await procesarArchivosMultiples(files)
    e.target.value = ''
    return
  }

  const file = files[0]
  try {
    const url = await galeriaService.subirImagen(file)
    formFoto.value.img = url
    if (!formFoto.value.titulo) {
      const nombreBase = file.name.substring(0, file.name.lastIndexOf('.')) || file.name
      formFoto.value.titulo = nombreBase.replace(/[_-]+/g, ' ').trim()
    }
    notificar('Foto cargada')
  } catch (err) {
    console.error(err)
    notificar('Error cargando imagen', 'error')
  }
}

async function guardarFoto() {
  if (!galeriaSeleccionada.value) return
  if (!formFoto.value.titulo.trim() || !formFoto.value.img) {
    notificar('Completa el título y la imagen de la foto', 'error')
    return
  }

  guardando.value = true
  try {
    if (editandoFotoId.value) {
      await galeriaService.actualizarFoto(editandoFotoId.value, formFoto.value)
      notificar('Fotografía actualizada')
    } else {
      await galeriaService.agregarFoto(galeriaSeleccionada.value.id, formFoto.value)
      notificar('Nueva fotografía agregada al álbum')
    }
    cerrarModalFoto()
    await cargarGalerias()
  } catch (err) {
    console.error(err)
    notificar('Error al guardar foto', 'error')
  } finally {
    guardando.value = false
  }
}

async function toggleGrandeFoto(foto) {
  try {
    const nuevoTamano = !foto.grande
    await galeriaService.actualizarFoto(foto.id, { grande: nuevoTamano })
    foto.grande = nuevoTamano
    notificar(nuevoTamano ? 'Foto destacada (2 columnas)' : 'Foto cambiada a normal')
  } catch (err) {
    console.error(err)
  }
}

async function toggleActivoFoto(foto) {
  try {
    const nuevoEstado = !foto.activo
    await galeriaService.actualizarFoto(foto.id, { activo: nuevoEstado })
    foto.activo = nuevoEstado
    notificar(nuevoEstado ? 'Foto visible en la web' : 'Foto ocultada')
  } catch (err) {
    console.error(err)
  }
}

async function usarComoPortada(foto) {
  if (!galeriaSeleccionada.value) return
  try {
    await galeriaService.actualizarGaleria(galeriaSeleccionada.value.id, { portada: foto.img })
    galeriaSeleccionada.value.portada = foto.img
    notificar('Foto configurada como portada del álbum')
    await cargarGalerias()
  } catch (err) {
    console.error(err)
  }
}

async function moverFotoInterna(index, direccion) {
  if (!galeriaSeleccionada.value?.fotos) return
  const fotos = galeriaSeleccionada.value.fotos
  const nuevoIdx = index + direccion
  if (nuevoIdx < 0 || nuevoIdx >= fotos.length) return

  const temp = fotos[index]
  fotos[index] = fotos[nuevoIdx]
  fotos[nuevoIdx] = temp

  // Actualizar órdenes
  for (let i = 0; i < fotos.length; i++) {
    fotos[i].orden = i + 1
    await galeriaService.actualizarFoto(fotos[i].id, { orden: i + 1 })
  }
  notificar('Orden actualizado')
}

function confirmarEliminarFoto(foto) {
  fotoAEliminar.value = foto
}

async function ejecutarEliminarFoto() {
  if (!fotoAEliminar.value) return
  try {
    await galeriaService.eliminarFoto(fotoAEliminar.value.id)
    notificar('Foto eliminada del álbum')
    fotoAEliminar.value = null
    await cargarGalerias()
  } catch (err) {
    console.error(err)
    notificar('Error al eliminar foto', 'error')
  }
}

// Restablecer por defecto
function confirmarRestablecer() {
  mostrarConfirmarRestablecer.value = true
}

async function ejecutarRestablecer() {
  try {
    await galeriaService.restablecerPorDefecto()
    mostrarConfirmarRestablecer.value = false
    galeriaSeleccionada.value = null
    notificar('Galerías iniciales restablecidas')
    await cargarGalerias()
  } catch (err) {
    console.error(err)
    notificar('Error al restablecer galerías', 'error')
  }
}

function abrirLightbox(foto) {
  lightboxFoto.value = foto
}
</script>

<style scoped>
.galerias-admin {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

/* ═══════════════════════════════════════════
   HEADER & ACCIONES
   ═══════════════════════════════════════════ */
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  flex-wrap: wrap;
}

/* ═══════════════════════════════════════════
   BATCH MULTI-DROPZONE
   ═══════════════════════════════════════════ */
.batch-dropzone {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 2.5px dashed #cbd5e1;
  border-radius: 18px;
  padding: 30px 24px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  overflow: hidden;
}

.batch-dropzone:hover {
  border-color: #10b981;
  background: #f0fdf4;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.12);
}

.batch-dropzone.drag-over {
  border-color: #059669;
  background: #ecfdf5;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.25), 0 12px 32px rgba(16, 185, 129, 0.2);
  transform: scale(1.01);
}

.batch-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

.batch-icon-ring {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: #d1fae5;
  color: #059669;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
}

.batch-texts {
  flex: 1;
  min-width: 260px;
}

.batch-texts h4 {
  font-size: 16px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 4px;
}

.batch-texts p {
  font-size: 13.5px;
  color: #64748b;
  line-height: 1.4;
}

.btn-select-batch {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: #0f172a;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
}

.btn-select-batch:hover {
  background: #1e293b;
  transform: translateY(-1px);
}

/* Uploading Progress */
.batch-uploading {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 8px 0;
}

.batch-progress-header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.batch-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #cbd5e1;
  border-top-color: #10b981;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  flex-shrink: 0;
}

.batch-progress-texts h4 {
  font-size: 15px;
  font-weight: 700;
  color: #0f172a;
}

.batch-progress-texts p {
  font-size: 13px;
  color: #64748b;
  margin-top: 2px;
}

.batch-progress-bar {
  height: 8px;
  background: #e2e8f0;
  border-radius: 100px;
  overflow: hidden;
}

.batch-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
  border-radius: 100px;
  transition: width 0.3s ease;
}

.header-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  background: rgba(16, 185, 129, 0.12);
  color: #059669;
  border-radius: 100px;
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 8px;
}

.header-info h1 {
  font-size: 26px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.5px;
  margin-bottom: 6px;
}

.header-info p {
  font-size: 14px;
  color: #64748b;
  max-width: 650px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.35);
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: white;
  color: #0f172a;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: transparent;
  color: #64748b;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-outline:hover {
  color: #0f172a;
  background: #f8fafc;
  border-color: #cbd5e1;
}

/* ═══════════════════════════════════════════
   METRICS GRID
   ═══════════════════════════════════════════ */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.metric-card {
  background: white;
  padding: 20px;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.metric-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.metric-icon.bg-indigo { background: #e0e7ff; color: #4f46e5; }
.metric-icon.bg-emerald { background: #d1fae5; color: #059669; }
.metric-icon.bg-amber { background: #fef3c7; color: #d97706; }
.metric-icon.bg-blue { background: #e0f2fe; color: #0284c7; }

.metric-data {
  display: flex;
  flex-direction: column;
}

.metric-value {
  font-size: 24px;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.1;
}

.metric-label {
  font-size: 12.5px;
  color: #64748b;
  font-weight: 500;
  margin-top: 4px;
}

/* ═══════════════════════════════════════════
   CONTROLS BAR
   ═══════════════════════════════════════════ */
.controls-card {
  background: white;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.controls-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 280px;
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 18px;
  color: #94a3b8;
}

.search-input {
  width: 100%;
  padding: 10px 38px 10px 42px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  color: #1e293b;
  outline: none;
  transition: all 0.2s;
}

.search-input:focus {
  background: white;
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
}

.clear-search {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  font-size: 18px;
}

.quick-filters {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
}

.control-select {
  padding: 8px 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  color: #1e293b;
  outline: none;
  cursor: pointer;
}

.categorias-pills {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  border-top: 1px solid #f1f5f9;
  padding-top: 14px;
}

.cat-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border-radius: 100px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
}

.cat-pill:hover {
  border-color: #10b981;
  color: #10b981;
}

.cat-pill.active {
  background: #10b981;
  border-color: #10b981;
  color: white;
}

.pill-count {
  background: rgba(0, 0, 0, 0.08);
  padding: 2px 7px;
  border-radius: 100px;
  font-size: 11px;
}

.cat-pill.active .pill-count {
  background: rgba(255, 255, 255, 0.25);
  color: white;
}

/* ═══════════════════════════════════════════
   GALERÍAS CARDS GRID (NIVEL 1)
   ═══════════════════════════════════════════ */
.galerias-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
}

.galeria-card {
  background: white;
  border-radius: 18px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  transition: all 0.3s ease;
}

.galeria-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(0,0,0,0.08);
}

.galeria-card.destacada {
  border-color: #fcd34d;
}

.galeria-card.inactiva {
  opacity: 0.75;
  border-style: dashed;
}

.galeria-cover {
  position: relative;
  height: 200px;
  background: #0f172a;
  cursor: pointer;
  overflow: hidden;
}

.galeria-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}

.galeria-cover:hover img {
  transform: scale(1.05);
}

.cover-overlay {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: white;
  opacity: 0;
  transition: opacity 0.25s ease;
}

.galeria-cover:hover .cover-overlay {
  opacity: 1;
}

.cover-overlay ion-icon { font-size: 32px; }
.cover-overlay span { font-size: 13.5px; font-weight: 600; }

.cover-badges {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  gap: 6px;
  z-index: 2;
}

.badge-cat {
  padding: 4px 10px;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(8px);
  color: #86efac;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-star {
  padding: 4px 10px;
  background: rgba(217, 119, 6, 0.9);
  backdrop-filter: blur(8px);
  color: white;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.cover-photos-count {
  position: absolute;
  bottom: 12px;
  right: 12px;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(8px);
  color: white;
  padding: 4px 10px;
  border-radius: 100px;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

.galeria-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.galeria-meta-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.meta-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}

.galeria-title {
  font-size: 17px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 6px;
  cursor: pointer;
  transition: color 0.15s;
}

.galeria-title:hover {
  color: #059669;
}

.galeria-desc {
  font-size: 13px;
  color: #64748b;
  line-height: 1.5;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

/* Tira de miniaturas */
.mini-thumbs-strip {
  display: flex;
  gap: 6px;
  margin-bottom: 16px;
}

.mini-thumb {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  background: #0f172a;
}

.mini-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.2s;
}

.mini-thumb:hover img {
  transform: scale(1.1);
}

.mini-thumb-more {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background: #f1f5f9;
  color: #475569;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.galeria-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  border-top: 1px solid #f1f5f9;
  padding-top: 16px;
  margin-top: auto;
}

.btn-manage {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 14px;
  background: #ecfdf5;
  color: #059669;
  border: 1px solid #a7f3d0;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-manage:hover {
  background: #10b981;
  color: white;
  border-color: #10b981;
}

.action-icons {
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #64748b;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.15s;
}

.btn-icon:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.btn-icon.active {
  color: #059669;
}

.btn-icon.btn-edit:hover {
  background: #e0e7ff;
  color: #4338ca;
  border-color: #c7d2fe;
}

.btn-icon.btn-danger:hover {
  background: #fef2f2;
  color: #dc2626;
  border-color: #fecaca;
}

/* ═══════════════════════════════════════════
   DETALLE DE GALERÍA (NIVEL 2)
   ═══════════════════════════════════════════ */
.vista-detalle-galeria {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.breadcrumb-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  color: #334155;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-back:hover {
  background: #f8fafc;
  color: #0f172a;
}

.breadcrumb-path {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13.5px;
  color: #64748b;
}

.breadcrumb-path strong {
  color: #0f172a;
}

.galeria-hero-card {
  background: white;
  border-radius: 18px;
  border: 1px solid #e2e8f0;
  padding: 24px;
  display: grid;
  grid-template-columns: 240px 1fr auto;
  gap: 24px;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.03);
}

.hero-cover-wrap {
  width: 100%;
  height: 160px;
  border-radius: 14px;
  overflow: hidden;
  background: #0f172a;
}

.hero-cover-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.hero-tags {
  display: flex;
  gap: 6px;
  align-items: center;
}

.hero-info h2 {
  font-size: 22px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.3px;
}

.hero-info p {
  font-size: 13.5px;
  color: #64748b;
  line-height: 1.5;
}

.hero-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  font-size: 13px;
  color: #475569;
  font-weight: 500;
}

.hero-meta span {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.hero-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.fotos-section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e2e8f0;
}

.fotos-section-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
}

.fotos-section-header p {
  font-size: 13px;
  color: #64748b;
}

/* Grid de fotos dentro del álbum */
.fotos-album-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.foto-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  transition: all 0.3s ease;
}

.foto-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 24px rgba(0,0,0,0.08);
}

.foto-card.grande {
  grid-column: span 2;
}

.foto-card.inactiva {
  opacity: 0.72;
  border-style: dashed;
}

.foto-card-img {
  position: relative;
  height: 220px;
  overflow: hidden;
  cursor: pointer;
  background: #0f172a;
}

.foto-card.grande .foto-card-img {
  height: 260px;
}

.foto-card-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}

.foto-card-img:hover img {
  transform: scale(1.04);
}

.foto-card-overlay {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: white;
  opacity: 0;
  transition: opacity 0.25s ease;
}

.foto-card-img:hover .foto-card-overlay { opacity: 1; }
.foto-card-overlay ion-icon { font-size: 28px; }
.foto-card-overlay span { font-size: 13px; font-weight: 600; }

.foto-badges-top {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  gap: 6px;
  z-index: 2;
}

.badge-grande {
  padding: 4px 10px;
  background: rgba(217, 119, 6, 0.85);
  backdrop-filter: blur(8px);
  color: white;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.foto-status-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 10px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  backdrop-filter: blur(8px);
  z-index: 2;
}

.status-active {
  background: rgba(16, 185, 129, 0.9);
  color: white;
}

.status-hidden {
  background: rgba(100, 116, 139, 0.85);
  color: white;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: white;
}

.status-pill {
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 100px;
}

.foto-card-body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.foto-meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.foto-orden {
  font-size: 12px;
  font-weight: 700;
  color: #94a3b8;
}

.foto-order-btns {
  display: flex;
  gap: 4px;
}

.btn-order {
  border: 1px solid #e2e8f0;
  background: white;
  color: #64748b;
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.15s;
}

.btn-order:hover:not(:disabled) {
  border-color: #10b981;
  color: #10b981;
  background: #f0fdf4;
}

.btn-order:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.foto-titulo {
  font-size: 15px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.foto-desc {
  font-size: 12.5px;
  color: #64748b;
  line-height: 1.5;
  margin-bottom: 14px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.foto-card-actions {
  display: flex;
  align-items: center;
  gap: 6px;
  border-top: 1px solid #f1f5f9;
  padding-top: 12px;
  margin-top: auto;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 8px;
  border-radius: 8px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  font-size: 11.5px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
  flex: 1;
  justify-content: center;
}

.action-btn:hover { background: #f1f5f9; color: #0f172a; }
.action-btn.active { background: #ecfdf5; color: #059669; border-color: #a7f3d0; }
.action-btn.edit-btn:hover { background: #e0e7ff; color: #4338ca; border-color: #c7d2fe; }

.action-btn.delete-btn {
  flex: 0 0 32px;
  padding: 0;
  height: 32px;
  color: #94a3b8;
}

.action-btn.delete-btn:hover {
  background: #fef2f2;
  color: #dc2626;
  border-color: #fecaca;
}

/* ═══════════════════════════════════════════
   MODAL STYLES
   ═══════════════════════════════════════════ */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 1000;
}

.modal-box {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  animation: modalPop 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-lg { max-width: 900px; }
.modal-sm { max-width: 440px; padding: 24px; text-align: center; }

@keyframes modalPop {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-title-group ion-icon { font-size: 24px; color: #10b981; }
.modal-title-group h2 { font-size: 18px; font-weight: 700; color: #0f172a; }

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  border-radius: 6px;
  padding: 4px;
}

.btn-close:hover { background: #f1f5f9; color: #0f172a; }

.modal-body {
  padding: 24px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.modal-columns {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 24px;
}

.modal-col {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: #334155;
  display: block;
  margin-bottom: 4px;
}

.form-label.required::after {
  content: ' *';
  color: #ef4444;
}

.sub-label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  display: block;
  margin-bottom: 4px;
}

.form-input, .form-select, .form-textarea {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  font-size: 14px;
  color: #0f172a;
  outline: none;
  font-family: inherit;
  transition: all 0.2s;
}

.form-input:focus, .form-select:focus, .form-textarea:focus {
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
}

.form-textarea { resize: vertical; }

.upload-dropzone {
  border: 2px dashed #cbd5e1;
  border-radius: 14px;
  background: #f8fafc;
  min-height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.2s;
}

.upload-dropzone:hover {
  border-color: #10b981;
  background: #f0fdf4;
}

.hidden-file-input { display: none; }

.dropzone-placeholder {
  text-align: center;
  padding: 24px;
}

.drop-icon {
  font-size: 40px;
  color: #94a3b8;
  margin-bottom: 8px;
}

.drop-text { font-size: 13.5px; font-weight: 600; color: #334155; }
.drop-hint { font-size: 11.5px; color: #94a3b8; display: block; margin-top: 4px; }

.preview-container {
  width: 100%;
  height: 180px;
  position: relative;
}

.img-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.preview-change-overlay {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  opacity: 0;
  transition: opacity 0.2s;
}

.upload-dropzone:hover .preview-change-overlay { opacity: 1; }

.form-switch-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 12px 16px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
}

.switch-info {
  display: flex;
  flex-direction: column;
}

.switch-title { font-size: 13px; font-weight: 600; color: #1e293b; }
.switch-subtitle { font-size: 11.5px; color: #64748b; margin-top: 2px; }

.switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
  flex-shrink: 0;
}

.switch input { opacity: 0; width: 0; height: 0; }

.slider {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background-color: #cbd5e1;
  transition: 0.25s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.25s;
}

input:checked + .slider { background-color: #10b981; }
input:checked + .slider:before { transform: translateX(20px); }
.slider.round { border-radius: 34px; }
.slider.round:before { border-radius: 50%; }

.nueva-cat-box {
  margin-top: 10px;
  padding: 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn-cancel {
  padding: 10px 18px;
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  font-size: 13.5px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover { background: #f1f5f9; }

.btn-save {
  padding: 10px 22px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  border-radius: 10px;
  font-size: 13.5px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
  transition: all 0.2s;
}

.btn-save:hover:not(:disabled) {
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.35);
  transform: translateY(-1px);
}

.btn-save:disabled { opacity: 0.5; cursor: not-allowed; }

/* Alert Modals */
.modal-alert-icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin: 0 auto 16px;
}

.modal-alert-icon.delete { background: #fee2e2; color: #dc2626; }
.modal-alert-icon.warning { background: #fef3c7; color: #d97706; }

.modal-alert-title { font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 8px; }
.modal-alert-msg { font-size: 13.5px; color: #64748b; line-height: 1.5; margin-bottom: 24px; }
.modal-alert-actions { display: flex; gap: 12px; justify-content: center; }

.btn-danger-confirm {
  padding: 10px 18px;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-danger-confirm:hover { background: #b91c1c; }

.btn-warning-confirm {
  padding: 10px 18px;
  background: #d97706;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-warning-confirm:hover { background: #b45309; }

/* ═══════════════════════════════════════════
   LIGHTBOX
   ═══════════════════════════════════════════ */
.lightbox {
  position: fixed;
  inset: 0;
  background: rgba(5, 20, 8, 0.94);
  backdrop-filter: blur(8px);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.lb-close {
  position: absolute;
  top: 24px;
  right: 24px;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  border: none;
  color: white;
  font-size: 26px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.lb-close:hover { background: rgba(255, 255, 255, 0.3); }

.lb-content {
  max-width: 900px;
  width: 100%;
  background: #0f172a;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.lb-img-wrap {
  width: 100%;
  max-height: 520px;
  background: black;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lb-img-wrap img {
  width: 100%;
  max-height: 520px;
  object-fit: contain;
  display: block;
}

.lb-info {
  padding: 24px 28px;
}

.lb-info h3 { font-size: 20px; font-weight: 700; color: white; margin-bottom: 8px; }
.lb-info p { font-size: 14px; color: rgba(255, 255, 255, 0.7); line-height: 1.6; }

/* ═══════════════════════════════════════════
   EMPTY & LOADING STATES
   ═══════════════════════════════════════════ */
.loading-state, .empty-state {
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  padding: 60px 24px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.spinner {
  width: 38px;
  height: 38px;
  border: 3px solid #e2e8f0;
  border-top-color: #10b981;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
.spin { animation: spin 0.8s linear infinite; }

.empty-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #f1f5f9;
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  margin-bottom: 8px;
}

.empty-state h3 { font-size: 18px; font-weight: 700; color: #0f172a; }
.empty-state p { font-size: 14px; color: #64748b; max-width: 440px; margin-bottom: 8px; }

/* ═══════════════════════════════════════════
   TOAST
   ═══════════════════════════════════════════ */
.admin-toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  border-radius: 12px;
  color: white;
  font-size: 13.5px;
  font-weight: 600;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  z-index: 9999;
}

.admin-toast.success { background: #0f766e; }
.admin-toast.error { background: #be123c; }
.admin-toast ion-icon { font-size: 20px; }

.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(16px); }

/* Responsive */
@media (max-width: 1024px) {
  .galeria-hero-card {
    grid-template-columns: 1fr;
    text-align: center;
  }
  .hero-cover-wrap {
    height: 200px;
  }
  .hero-tags, .hero-meta {
    justify-content: center;
  }
  .fotos-album-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .modal-columns {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .galerias-cards-grid {
    grid-template-columns: 1fr;
  }
  .fotos-album-grid {
    grid-template-columns: 1fr;
  }
  .foto-card.grande {
    grid-column: span 1;
  }
  .controls-top {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
