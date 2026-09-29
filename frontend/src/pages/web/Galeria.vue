<template>
  <LayoutPublico>
    <!-- Hero Principal -->
    <section
      class="page-hero"
      :style="{ backgroundImage: `url('${heroFondo}')` }"
    >
      <div class="ph-overlay"></div>

      <!-- Flechas en el Hero para navegar entre galerías si hay un álbum seleccionado -->
      <button
        v-if="albumActivo && galeriasActivas.length > 1"
        class="hero-nav-arrow hero-nav-prev"
        @click="irAAlbumAnterior"
        title="Álbum anterior"
      >
        <ion-icon name="chevron-back-outline"></ion-icon>
      </button>

      <div class="ph-content">
        <span class="ph-tag">
          <ion-icon name="images-outline"></ion-icon>
          {{ albumActivo ? (albumActivo.categoriaLabel || 'Álbum Seleccionado') : 'Galería Fotográfica' }}
        </span>
        <h1>{{ albumActivo ? albumActivo.titulo : 'Galería Fotográfica' }}</h1>
        <p>
          {{ albumActivo ? (albumActivo.descripcion || 'Colección de fotografías oficiales de la comunidad.') : 'Imágenes que reflejan la vida, el trabajo, las asambleas y la identidad de nuestra comunidad' }}
        </p>

        <!-- Metadata si hay álbum activo -->
        <div v-if="albumActivo" class="ph-meta-bar">
          <span v-if="albumActivo.fecha"><ion-icon name="calendar-outline"></ion-icon> {{ albumActivo.fecha }}</span>
          <span v-if="albumActivo.lugar"><ion-icon name="location-outline"></ion-icon> {{ albumActivo.lugar }}</span>
          <span><ion-icon name="camera-outline"></ion-icon> {{ fotosVisibles.length }} fotografías</span>
        </div>
      </div>

      <button
        v-if="albumActivo && galeriasActivas.length > 1"
        class="hero-nav-arrow hero-nav-next"
        @click="irAAlbumSiguiente"
        title="Siguiente álbum"
      >
        <ion-icon name="chevron-forward-outline"></ion-icon>
      </button>
    </section>

    <section class="section">
      <div class="container">
        <!-- Barra de Modos y Filtros -->
        <div class="galeria-header-toolbar">
          <!-- Filtros de Álbum / Categoría en Pills -->
          <div class="filtros">
            <button
              :class="['filtro-btn', { active: filtroActivo === 'todas' }]"
              @click="seleccionarFiltro('todas')"
            >
              <ion-icon name="images-outline"></ion-icon>
              <span>Todas las Fotos</span>
              <span class="pill-counter">({{ totalFotosCount }})</span>
            </button>

            <!-- Filtros por cada galería existente -->
            <button
              v-for="g in galeriasActivas"
              :key="g.id"
              :class="['filtro-btn', { active: filtroActivo === String(g.id) }]"
              @click="seleccionarFiltro(String(g.id))"
            >
              <span>{{ g.titulo }}</span>
              <span class="pill-counter">({{ (g.fotos || []).filter(f => f.activo !== false).length }})</span>
            </button>

            <!-- Botón para ver vista de Álbumes en tarjetas -->
            <button
              :class="['filtro-btn btn-albumes-view', { active: filtroActivo === '__albumes__' }]"
              @click="seleccionarFiltro('__albumes__')"
            >
              <ion-icon name="albums-outline"></ion-icon>
              <span>Ver por Álbumes</span>
            </button>
          </div>
        </div>

        <!-- ════════════════════════════════════════════════════════════════
             VISTA A: CUADRÍCULA DE FOTOGRAFÍAS (Muestra TODAS o las del Álbum)
             ════════════════════════════════════════════════════════════════ -->
        <div v-if="filtroActivo !== '__albumes__'">
          <!-- Barra de Navegación entre Galerías cuando hay un álbum activo -->
          <div v-if="albumActivo" class="galeria-nav-bar">
            <!-- Botón Álbum Anterior -->
            <button
              v-if="albumAnterior"
              class="gn-btn gn-prev"
              @click="seleccionarFiltro(String(albumAnterior.id))"
              :title="`Ir a: ${albumAnterior.titulo}`"
            >
              <ion-icon name="chevron-back-outline"></ion-icon>
              <div class="gn-btn-texts">
                <span class="gn-label">Álbum Anterior</span>
                <span class="gn-name">{{ albumAnterior.titulo }}</span>
              </div>
            </button>
            <div v-else class="gn-spacer"></div>

            <!-- Centro: Indicador del Álbum Actual y enlace a todas -->
            <div class="gn-center">
              <span class="gn-badge">
                <ion-icon name="folder-open-outline"></ion-icon>
                {{ albumActivo.titulo }}
              </span>
              <button class="gn-btn-all" @click="seleccionarFiltro('todas')">
                <ion-icon name="grid-outline"></ion-icon>
                Ver todas las fotos
              </button>
            </div>

            <!-- Botón Siguiente Álbum -->
            <button
              v-if="albumSiguiente"
              class="gn-btn gn-next"
              @click="seleccionarFiltro(String(albumSiguiente.id))"
              :title="`Ir a: ${albumSiguiente.titulo}`"
            >
              <div class="gn-btn-texts text-right">
                <span class="gn-label">Siguiente Álbum</span>
                <span class="gn-name">{{ albumSiguiente.titulo }}</span>
              </div>
              <ion-icon name="chevron-forward-outline"></ion-icon>
            </button>
            <div v-else class="gn-spacer"></div>
          </div>

          <!-- Grid de Fotos -->
          <div v-if="fotosVisibles.length > 0" class="galeria-grid">
            <div
              v-for="foto in fotosVisibles"
              :key="foto.id"
              class="foto-item"
              :class="foto.grande ? 'grande' : ''"
              @click="abrirFoto(foto)"
            >
              <img :src="foto.img" :alt="foto.titulo" loading="lazy" />
              <div class="foto-overlay">
                <ion-icon name="expand-outline"></ion-icon>
                <span class="foto-ov-titulo">{{ foto.titulo }}</span>
                <span v-if="foto.categoriaLabel" class="foto-ov-cat">{{ foto.categoriaLabel }}</span>
              </div>
            </div>
          </div>

          <!-- Navegación inferior entre galerías al pie de la cuadrícula -->
          <div v-if="albumActivo && galeriasActivas.length > 1" class="galeria-bottom-switcher">
            <div
              v-if="albumAnterior"
              class="gbs-card gbs-prev"
              @click="seleccionarFiltro(String(albumAnterior.id))"
            >
              <div class="gbs-arrow-icon"><ion-icon name="arrow-back-outline"></ion-icon></div>
              <img :src="albumAnterior.portada || '/uploads/img/web/2.png'" :alt="albumAnterior.titulo" />
              <div class="gbs-info">
                <span class="gbs-hint">Álbum Anterior</span>
                <h4 class="gbs-title">{{ albumAnterior.titulo }}</h4>
              </div>
            </div>

            <div
              v-if="albumSiguiente"
              class="gbs-card gbs-next"
              @click="seleccionarFiltro(String(albumSiguiente.id))"
            >
              <div class="gbs-info text-right">
                <span class="gbs-hint">Siguiente Álbum</span>
                <h4 class="gbs-title">{{ albumSiguiente.titulo }}</h4>
              </div>
              <img :src="albumSiguiente.portada || '/uploads/img/web/2.png'" :alt="albumSiguiente.titulo" />
              <div class="gbs-arrow-icon"><ion-icon name="arrow-forward-outline"></ion-icon></div>
            </div>
          </div>

          <div v-if="fotosVisibles.length === 0" class="empty-web-state">
            <ion-icon name="images-outline"></ion-icon>
            <h3>No hay fotografías disponibles en esta selección</h3>
            <p>Selecciona otra galería o haz clic en "Todas las Fotos".</p>
            <button class="filtro-btn active" @click="seleccionarFiltro('todas')">
              Ver Todas las Fotografías
            </button>
          </div>
        </div>

        <!-- ════════════════════════════════════════════════════════════════
             VISTA B: TARJETAS DE ÁLBUMES
             ════════════════════════════════════════════════════════════════ -->
        <div v-else>
          <div class="albumes-grid">
            <article
              v-for="galeria in galeriasActivas"
              :key="galeria.id"
              class="album-card"
              :class="{ destacada: galeria.destacada }"
              @click="seleccionarFiltro(String(galeria.id))"
            >
              <div class="ac-cover">
                <img :src="galeria.portada || '/uploads/img/web/2.png'" :alt="galeria.titulo" loading="lazy" />
                <div class="ac-overlay">
                  <span class="ac-view-btn">
                    <ion-icon name="images-outline"></ion-icon> Ver {{ (galeria.fotos || []).filter(f => f.activo !== false).length }} Fotos
                  </span>
                </div>
                <span class="ac-cat">{{ galeria.categoriaLabel || galeria.categoria }}</span>
                <span v-if="galeria.destacada" class="ac-destacada">
                  <ion-icon name="star"></ion-icon> Destacado
                </span>
                <span class="ac-count">
                  <ion-icon name="camera-outline"></ion-icon> {{ (galeria.fotos || []).filter(f => f.activo !== false).length }} fotos
                </span>
              </div>

              <div class="ac-body">
                <div class="ac-meta">
                  <span v-if="galeria.fecha"><ion-icon name="calendar-outline"></ion-icon> {{ galeria.fecha }}</span>
                  <span v-if="galeria.lugar"><ion-icon name="location-outline"></ion-icon> {{ galeria.lugar }}</span>
                </div>
                <h3>{{ galeria.titulo }}</h3>
                <p>{{ galeria.descripcion }}</p>
                <div class="ac-footer">
                  <span class="ac-link">
                    Abrir álbum <ion-icon name="arrow-forward-outline"></ion-icon>
                  </span>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>
    </section>

    <!-- ════════════════════════════════════════════════════════════════
         LIGHTBOX DE AMPLIACIÓN (SOLO FOTO Y FLECHAS DE NAVEGACIÓN)
         ════════════════════════════════════════════════════════════════ -->
    <div
      v-if="fotoActiva"
      class="lightbox"
      @click.self="cerrarLightbox"
    >
      <!-- Botón Cerrar -->
      <button class="lb-close" @click="cerrarLightbox" title="Cerrar (Esc)">
        <ion-icon name="close-outline"></ion-icon>
      </button>

      <!-- Contador discreto de fotos -->
      <div v-if="fotosVisibles.length > 1" class="lb-counter">
        {{ fotoActivaIndex + 1 }} / {{ fotosVisibles.length }}
      </div>

      <!-- Flecha Retroceder -->
      <button
        v-if="fotosVisibles.length > 1"
        class="lb-nav-arrow lb-prev"
        @click.stop="fotoAnterior"
        title="Foto anterior (←)"
        aria-label="Foto anterior"
      >
        <ion-icon name="chevron-back-outline"></ion-icon>
      </button>

      <!-- Contenedor solo de la fotografía (sin pie de foto) -->
      <div class="lb-photo-wrap" @click.stop>
        <img :src="fotoActiva.img" :alt="fotoActiva.titulo || 'Fotografía'" />
      </div>

      <!-- Flecha Avanzar -->
      <button
        v-if="fotosVisibles.length > 1"
        class="lb-nav-arrow lb-next"
        @click.stop="fotoSiguiente"
        title="Foto siguiente (→)"
        aria-label="Foto siguiente"
      >
        <ion-icon name="chevron-forward-outline"></ion-icon>
      </button>
    </div>
  </LayoutPublico>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import LayoutPublico from './LayoutPublico.vue'
import { galeriaService, GALERIAS_POR_DEFECTO } from '@/services/galeria.service'

const filtroActivo = ref('todas') // 'todas' | galeria.id | '__albumes__'
const galerias = ref(GALERIAS_POR_DEFECTO)
const fotoActiva = ref(null)

async function cargarDatos() {
  try {
    const res = await galeriaService.obtenerPublico()
    if (res.galerias && res.galerias.length > 0) {
      galerias.value = res.galerias
    }
  } catch (err) {
    console.warn('Cargando galerías locales:', err)
  }
}

function onGaleriasActualizadas() {
  cargarDatos()
}

// Navegación con teclado para el Lightbox
function onKeydown(e) {
  if (!fotoActiva.value) return
  if (e.key === 'ArrowLeft') {
    e.preventDefault()
    fotoAnterior()
  } else if (e.key === 'ArrowRight') {
    e.preventDefault()
    fotoSiguiente()
  } else if (e.key === 'Escape') {
    cerrarLightbox()
  }
}

onMounted(() => {
  cargarDatos()
  window.addEventListener('comunidad-galerias-actualizadas', onGaleriasActualizadas)
  window.addEventListener('keydown', onKeydown)
})

onUnmounted(() => {
  window.removeEventListener('comunidad-galerias-actualizadas', onGaleriasActualizadas)
  window.removeEventListener('keydown', onKeydown)
})

// Galerías activas
const galeriasActivas = computed(() => {
  return galerias.value.filter(g => g.activo !== false)
})

// Álbum seleccionado actualmente según filtroActivo
const albumActivo = computed(() => {
  if (filtroActivo.value === 'todas' || filtroActivo.value === '__albumes__') {
    return null
  }
  return galeriasActivas.value.find(g => String(g.id) === filtroActivo.value) || null
})

// Índice del álbum activo dentro de las galerías activas
const albumActivoIndex = computed(() => {
  if (!albumActivo.value) return -1
  return galeriasActivas.value.findIndex(g => String(g.id) === String(albumActivo.value.id))
})

// Álbum anterior
const albumAnterior = computed(() => {
  if (albumActivoIndex.value === -1 || galeriasActivas.value.length <= 1) return null
  const prevIdx = (albumActivoIndex.value - 1 + galeriasActivas.value.length) % galeriasActivas.value.length
  return galeriasActivas.value[prevIdx]
})

// Álbum siguiente
const albumSiguiente = computed(() => {
  if (albumActivoIndex.value === -1 || galeriasActivas.value.length <= 1) return null
  const nextIdx = (albumActivoIndex.value + 1) % galeriasActivas.value.length
  return galeriasActivas.value[nextIdx]
})

function irAAlbumAnterior() {
  if (albumAnterior.value) {
    seleccionarFiltro(String(albumAnterior.value.id))
  }
}

function irAAlbumSiguiente() {
  if (albumSiguiente.value) {
    seleccionarFiltro(String(albumSiguiente.value.id))
  }
}

// Imagen de fondo del Hero
const heroFondo = computed(() => {
  if (albumActivo.value?.portada) return albumActivo.value.portada
  return '/uploads/img/inicio/cerro_baul.png'
})

// Total de fotos en todas las galerías activas
const totalFotosCount = computed(() => {
  return galeriasActivas.value
    .reduce((acc, g) => acc + (g.fotos || []).filter(f => f.activo !== false).length, 0)
})

// Fotografías que se deben mostrar en la cuadrícula
const fotosVisibles = computed(() => {
  // Caso 1: Un álbum específico seleccionado
  if (albumActivo.value) {
    return (albumActivo.value.fotos || []).filter(f => f.activo !== false)
  }

  // Caso 2: 'todas': Unificar TODAS las fotos de todas las galerías activas
  const todas = []
  galeriasActivas.value.forEach(g => {
    (g.fotos || []).forEach(f => {
      if (f.activo !== false) {
        todas.push({
          ...f,
          galeriaOrden: g.orden || 0,
          categoria: g.categoria,
          categoriaLabel: f.categoriaLabel || g.categoriaLabel || g.titulo
        })
      }
    })
  })

  return todas.sort((a, b) => ((a.galeriaOrden || 0) - (b.galeriaOrden || 0)) || ((a.orden || 0) - (b.orden || 0)))
})

// Índice de la foto activa dentro de fotosVisibles para la navegación
const fotoActivaIndex = computed(() => {
  if (!fotoActiva.value) return -1
  return fotosVisibles.value.findIndex(f => String(f.id) === String(fotoActiva.value.id))
})

function seleccionarFiltro(val) {
  filtroActivo.value = val
  if (val !== '__albumes__' && val !== 'todas') {
    window.scrollTo({ top: 380, behavior: 'smooth' })
  }
}

function abrirFoto(foto) {
  fotoActiva.value = foto
}

function cerrarLightbox() {
  fotoActiva.value = null
}

function fotoAnterior() {
  if (fotosVisibles.value.length === 0) return
  const currentIdx = fotoActivaIndex.value
  const newIdx = (currentIdx - 1 + fotosVisibles.value.length) % fotosVisibles.value.length
  fotoActiva.value = fotosVisibles.value[newIdx]
}

function fotoSiguiente() {
  if (fotosVisibles.value.length === 0) return
  const currentIdx = fotoActivaIndex.value
  const newIdx = (currentIdx + 1) % fotosVisibles.value.length
  fotoActiva.value = fotosVisibles.value[newIdx]
}
</script>

<style scoped>
.page-hero {
  min-height: 52vh;
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  position: relative;
  transition: background-image 0.5s ease-in-out;
}

.ph-overlay {
  position: absolute;
  inset: 0;
  background: rgba(5, 20, 8, 0.74);
}

.ph-content {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
  padding: 120px 24px 70px;
  color: white;
  width: 100%;
}

.ph-tag {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  background: rgba(134, 239, 172, 0.15);
  color: #86efac;
  border-radius: 100px;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 14px;
}

.ph-content h1 {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 800;
  margin-bottom: 10px;
}

.ph-content p {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
  max-width: 750px;
  line-height: 1.5;
}

.ph-meta-bar {
  display: flex;
  gap: 20px;
  margin-top: 16px;
  font-size: 13.5px;
  color: #86efac;
  font-weight: 500;
}

.ph-meta-bar span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.section {
  padding: 70px 0 100px;
  background: white;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* ═══════════════════════════════════════════
   TOOLBAR DE FILTROS
   ═══════════════════════════════════════════ */
.galeria-header-toolbar {
  margin-bottom: 36px;
}

.filtros {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
}

.filtro-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 18px;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 100px;
  font-size: 13.5px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
}

.filtro-btn:hover {
  border-color: #16a34a;
  color: #16a34a;
}

.filtro-btn.active {
  background: #16a34a;
  color: white;
  border-color: #16a34a;
  box-shadow: 0 4px 12px rgba(22, 163, 74, 0.2);
}

.pill-counter {
  font-size: 12px;
  opacity: 0.85;
}

.btn-albumes-view {
  margin-left: auto;
  background: #f8fafc;
}

/* Flechas de navegación en el Hero */
.hero-nav-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: white;
  font-size: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.25s ease;
}

.hero-nav-arrow:hover {
  background: rgba(22, 163, 74, 0.9);
  border-color: #86efac;
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
}

.hero-nav-prev {
  left: 20px;
}

.hero-nav-next {
  right: 20px;
}

/* Barra superior de navegación entre galerías */
.galeria-nav-bar {
  background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
  border: 1px solid #bbf7d0;
  border-radius: 16px;
  padding: 12px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 28px;
  box-shadow: 0 4px 14px rgba(22, 163, 74, 0.05);
}

.gn-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: white;
  border: 1px solid #86efac;
  border-radius: 100px;
  padding: 7px 16px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  color: #166534;
  max-width: 280px;
  text-decoration: none;
}

.gn-btn:hover {
  background: #16a34a;
  color: white;
  border-color: #16a34a;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(22, 163, 74, 0.25);
}

.gn-btn:hover .gn-label {
  color: #dcfce7;
}

.gn-btn:hover .gn-name {
  color: white;
}

.gn-btn ion-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.gn-btn-texts {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  text-align: left;
}

.gn-btn-texts.text-right {
  text-align: right;
}

.gn-label {
  font-size: 10.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #15803d;
  transition: color 0.2s;
}

.gn-name {
  font-size: 13px;
  font-weight: 700;
  color: #0f172a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: color 0.2s;
}

.gn-center {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}

.gn-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: #dcfce7;
  color: #166534;
  border-radius: 100px;
  font-size: 13px;
  font-weight: 700;
}

.gn-btn-all {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: transparent;
  border: 1px dashed #16a34a;
  color: #16a34a;
  padding: 6px 14px;
  border-radius: 100px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.gn-btn-all:hover {
  background: #16a34a;
  color: white;
  border-style: solid;
}

.gn-spacer {
  width: 120px;
}

/* ═══════════════════════════════════════════
   GRID DE FOTOS (FOTO-ITEM)
   ═══════════════════════════════════════════ */
.galeria-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 240px;
  gap: 16px;
}

.foto-item {
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.foto-item.grande {
  grid-column: span 2;
}

.foto-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
  display: block;
}

.foto-item:hover img {
  transform: scale(1.05);
}

.foto-overlay {
  position: absolute;
  inset: 0;
  background: rgba(5, 20, 8, 0);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: white;
  transition: background 0.3s;
  padding: 16px;
}

.foto-item:hover .foto-overlay {
  background: rgba(5, 20, 8, 0.58);
}

.foto-overlay ion-icon {
  font-size: 32px;
  opacity: 0;
  transform: scale(0.7);
  transition: all 0.3s;
}

.foto-ov-titulo {
  font-size: 15px;
  font-weight: 700;
  opacity: 0;
  transition: opacity 0.3s;
  text-align: center;
}

.foto-ov-cat {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  color: #86efac;
  opacity: 0;
  transition: opacity 0.3s;
}

.foto-item:hover .foto-overlay ion-icon,
.foto-item:hover .foto-ov-titulo,
.foto-item:hover .foto-ov-cat {
  opacity: 1;
  transform: scale(1);
}

/* ═══════════════════════════════════════════
   GRID DE ÁLBUMES (CARDS)
   ═══════════════════════════════════════════ */
.albumes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 28px;
}

.album-card {
  background: white;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
}

.album-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.1);
  border-color: #a7f3d0;
}

.ac-cover {
  position: relative;
  height: 230px;
  background: #0f172a;
  overflow: hidden;
}

.ac-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
  display: block;
}

.album-card:hover .ac-cover img {
  transform: scale(1.06);
}

.ac-overlay {
  position: absolute;
  inset: 0;
  background: rgba(5, 20, 8, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.album-card:hover .ac-overlay {
  opacity: 1;
}

.ac-view-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 18px;
  background: white;
  color: #0f172a;
  border-radius: 100px;
  font-size: 13px;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.ac-cat {
  position: absolute;
  top: 14px;
  left: 14px;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(8px);
  color: #86efac;
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
}

.ac-destacada {
  position: absolute;
  top: 14px;
  right: 14px;
  background: rgba(217, 119, 6, 0.9);
  backdrop-filter: blur(8px);
  color: white;
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.ac-count {
  position: absolute;
  bottom: 14px;
  right: 14px;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(8px);
  color: white;
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

.ac-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.ac-meta {
  display: flex;
  gap: 14px;
  margin-bottom: 10px;
  font-size: 12.5px;
  color: #64748b;
  font-weight: 500;
}

.ac-meta span {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.ac-body h3 {
  font-size: 19px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 8px;
  line-height: 1.3;
}

.ac-body p {
  font-size: 13.5px;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 18px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.ac-footer {
  border-top: 1px solid #f1f5f9;
  padding-top: 14px;
}

.ac-link {
  font-size: 13.5px;
  font-weight: 700;
  color: #16a34a;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: gap 0.2s;
}

.album-card:hover .ac-link {
  gap: 10px;
}

/* Estado vacío */
.empty-web-state {
  text-align: center;
  padding: 70px 20px;
  color: #64748b;
}

.empty-web-state ion-icon {
  font-size: 52px;
  color: #cbd5e1;
  margin-bottom: 14px;
}

.empty-web-state h3 {
  font-size: 19px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.empty-web-state p {
  font-size: 14px;
  margin-bottom: 20px;
}

/* ═══════════════════════════════════════════
   CAMBIADOR INFERIOR DE GALERÍAS
   ═══════════════════════════════════════════ */
.galeria-bottom-switcher {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 48px;
  padding-top: 36px;
  border-top: 1px solid #e2e8f0;
}

.gbs-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.gbs-card:hover {
  background: white;
  border-color: #86efac;
  transform: translateY(-4px);
  box-shadow: 0 10px 24px rgba(22, 163, 74, 0.12);
}

.gbs-card.gbs-next {
  justify-content: flex-end;
}

.gbs-card img {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  object-fit: cover;
  flex-shrink: 0;
}

.gbs-arrow-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: white;
  border: 1px solid #cbd5e1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #16a34a;
  flex-shrink: 0;
  transition: all 0.2s;
}

.gbs-card:hover .gbs-arrow-icon {
  background: #16a34a;
  border-color: #16a34a;
  color: white;
}

.gbs-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow: hidden;
}

.gbs-info.text-right {
  text-align: right;
}

.gbs-hint {
  font-size: 11.5px;
  font-weight: 700;
  color: #16a34a;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.gbs-title {
  font-size: 15px;
  font-weight: 700;
  color: #0f172a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 0;
}

/* ═══════════════════════════════════════════
   LIGHTBOX PURA FOTOGRAFÍA CON FLECHAS
   ═══════════════════════════════════════════ */
.lightbox {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.96);
  backdrop-filter: blur(12px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  user-select: none;
}

.lb-close {
  position: absolute;
  top: 24px;
  right: 24px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 28px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  z-index: 1010;
}

.lb-close:hover {
  background: rgba(239, 68, 68, 0.85);
  border-color: #f87171;
  transform: scale(1.1);
}

.lb-counter {
  position: absolute;
  top: 28px;
  left: 28px;
  color: rgba(255, 255, 255, 0.85);
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 6px 16px;
  border-radius: 100px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.5px;
  z-index: 1010;
}

.lb-nav-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: white;
  font-size: 32px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 1010;
}

.lb-nav-arrow:hover {
  background: rgba(22, 163, 74, 0.9);
  border-color: #86efac;
  transform: translateY(-50%) scale(1.12);
  box-shadow: 0 0 24px rgba(34, 197, 94, 0.5);
}

.lb-prev {
  left: 28px;
}

.lb-next {
  right: 28px;
}

.lb-photo-wrap {
  max-width: 90vw;
  max-height: 88vh;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1005;
}

.lb-photo-wrap img {
  max-width: 88vw;
  max-height: 85vh;
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7);
  display: block;
  animation: lbFadeIn 0.25s ease-out;
}

@keyframes lbFadeIn {
  from { opacity: 0; transform: scale(0.97); }
  to { opacity: 1; transform: scale(1); }
}

@media (max-width: 768px) {
  .albumes-grid { grid-template-columns: 1fr; }
  .galeria-grid { grid-template-columns: repeat(2, 1fr); grid-auto-rows: 180px; }
  .foto-item.grande { grid-column: span 2; }
  .btn-albumes-view { margin-left: 0; }
  .galeria-nav-bar { flex-direction: column; align-items: stretch; }
  .gn-btn { max-width: 100%; justify-content: center; }
  .gn-spacer { display: none; }
  .galeria-bottom-switcher { grid-template-columns: 1fr; }
  .gbs-card.gbs-next { justify-content: flex-start; }
  .gbs-info.text-right { text-align: left; }
  .lb-prev { left: 12px; width: 44px; height: 44px; font-size: 24px; }
  .lb-next { right: 12px; width: 44px; height: 44px; font-size: 24px; }
  .hero-nav-arrow { display: none; }
}

@media (max-width: 480px) {
  .galeria-grid { grid-template-columns: 1fr; grid-auto-rows: 200px; }
  .foto-item.grande { grid-column: span 1; }
  .lb-close { top: 16px; right: 16px; width: 40px; height: 40px; font-size: 22px; }
  .lb-counter { top: 18px; left: 16px; font-size: 11px; padding: 4px 10px; }
}
</style>
