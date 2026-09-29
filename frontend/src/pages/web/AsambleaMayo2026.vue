<template>
  <LayoutPublico>

    <!-- HERO -->
    <section class="detalle-hero">
      <div class="detalle-hero-inner">
        <span class="tag-green">Asamblea</span>
        <h1>Acuerdos de la Asamblea General Ordinaria</h1>
        <div class="detalle-meta">
          <span><ion-icon name="calendar-outline"></ion-icon> 24 de mayo de 2026</span>
          <span><ion-icon name="location-outline"></ion-icon> Sede Comunal, Tumilaca</span>
        </div>
        <button class="btn-volver" @click="nav('noticias')">
          <ion-icon name="arrow-back-outline"></ion-icon> Volver a noticias
        </button>
      </div>
    </section>

    <!-- CONTENIDO -->
    <section class="detalle-body">
      <div class="container-narrow">

        <div class="detalle-intro">
          <p>
            El día <strong>24 de mayo de 2026</strong>, la Comunidad Campesina Tumilaca, Pocata, Coscore y Tala
            celebró su <strong>Asamblea General Ordinaria</strong> con la participación de usuarios empadronados
            de los diferentes anexos del territorio comunal.
          </p>
        </div>

        <!--div class="detalle-seccion">
          <h2><ion-icon name="checkmark-circle-outline"></ion-icon> Acuerdos adoptados</h2>
          <ul class="acuerdos-lista">
            <li>Aprobación de los estados financieros del ejercicio 2025.</li>
            <li>Aprobación del plan de trabajo y presupuesto para el año 2026.</li>
            <li>Ratificación de la junta directiva en sus funciones.</li>
            <li>Aprobación de gestiones ante entidades del Estado para titulación de tierras comunales.</li>
            <li>Reconocimiento de nuevos comuneros calificados conforme al padrón actualizado.</li>
          </ul>
        </div-->

        <!-- GALERÍA -->
        <div class="detalle-seccion">
          <h2><ion-icon name="images-outline"></ion-icon> Galería fotográfica</h2>
          <div class="galeria-grid">
            <div
              v-for="(foto, idx) in fotos"
              :key="idx"
              class="galeria-item"
              @click="abrirLightbox(idx)"
            >
              <img :src="foto.src" :alt="foto.alt" />
              <div class="galeria-overlay">
                <ion-icon name="expand-outline"></ion-icon>
              </div>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- LIGHTBOX -->
    <div v-if="lightboxAbierto" class="lightbox" @click.self="cerrarLightbox">
      <button class="lb-close" @click="cerrarLightbox">
        <ion-icon name="close-outline"></ion-icon>
      </button>
      <button class="lb-prev" @click="lbPrev">
        <ion-icon name="chevron-back-outline"></ion-icon>
      </button>
      <div class="lb-content">
        <img :src="fotos[lbIndex].src" :alt="fotos[lbIndex].alt" />
        <p class="lb-caption">{{ fotos[lbIndex].alt }}</p>
      </div>
      <button class="lb-next" @click="lbNext">
        <ion-icon name="chevron-forward-outline"></ion-icon>
      </button>
    </div>

  </LayoutPublico>
</template>

<script setup>
import { ref } from 'vue'
import LayoutPublico from './LayoutPublico.vue'
import { useWebNav } from '../../composables/useWebNav'

const { navegar } = useWebNav()
function nav(p) { navegar(p) }

const fotos = [
  { src: '/uploads/img/asamblea/1.jpeg', alt: 'Asamblea General Ordinaria — Mayo 2026' },
  { src: '/uploads/img/asamblea/2.jpeg', alt: 'Participación de comuneros en la asamblea' },
  { src: '/uploads/img/asamblea/3.jpeg', alt: 'Votación de acuerdos comunales' },
]

const lightboxAbierto = ref(false)
const lbIndex = ref(0)

function abrirLightbox(idx) {
  lbIndex.value = idx
  lightboxAbierto.value = true
}

function cerrarLightbox() {
  lightboxAbierto.value = false
}

function lbPrev() {
  lbIndex.value = (lbIndex.value - 1 + fotos.length) % fotos.length
}

function lbNext() {
  lbIndex.value = (lbIndex.value + 1) % fotos.length
}
</script>

<style scoped>
/* HERO */
.detalle-hero {
  background: linear-gradient(135deg, #1a3c2e 0%, #0f5132 60%, #1aa86a 100%);
  padding: 120px 24px 60px;
  color: white;
}

.detalle-hero-inner {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.tag-green {
  display: inline-block;
  background: rgba(255,255,255,0.15);
  color: #a7f3d0;
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.5px;
  width: fit-content;
}

.detalle-hero h1 {
  font-size: clamp(24px, 4vw, 40px);
  font-weight: 800;
  line-height: 1.2;
  margin: 0;
}

.detalle-meta {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  font-size: 14px;
  color: rgba(255,255,255,0.8);
}

.detalle-meta span {
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-volver {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.3);
  color: white;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  width: fit-content;
  margin-top: 8px;
}

.btn-volver:hover {
  background: rgba(255,255,255,0.25);
}

/* CUERPO */
.detalle-body {
  padding: 60px 24px 80px;
  background: #f9fafb;
}

.container-narrow {
  max-width: 860px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 48px;
}

.detalle-intro p {
  font-size: 17px;
  line-height: 1.8;
  color: #374151;
}

.detalle-seccion h2 {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 22px;
  font-weight: 700;
  color: #1a3c2e;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #d1fae5;
}

.detalle-seccion h2 ion-icon {
  color: #1aa86a;
  font-size: 24px;
}

/* ACUERDOS */
.acuerdos-lista {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.acuerdos-lista li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 15px;
  color: #374151;
  line-height: 1.6;
  padding: 14px 18px;
  background: white;
  border-radius: 8px;
  border-left: 3px solid #1aa86a;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

.acuerdos-lista li::before {
  content: '✓';
  color: #1aa86a;
  font-weight: 700;
  flex-shrink: 0;
  margin-top: 1px;
}

/* GALERÍA */
.galeria-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}

.galeria-item {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  aspect-ratio: 4/3;
  background: #e5e7eb;
}

.galeria-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.galeria-item:hover img {
  transform: scale(1.05);
}

.galeria-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
  color: white;
  font-size: 32px;
}

.galeria-item:hover .galeria-overlay {
  opacity: 1;
}

/* LIGHTBOX */
.lightbox {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.92);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lb-content {
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.lb-content img {
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
  border-radius: 4px;
}

.lb-caption {
  color: rgba(255,255,255,0.7);
  font-size: 14px;
  text-align: center;
}

.lb-close, .lb-prev, .lb-next {
  position: absolute;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  color: white;
  cursor: pointer;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  transition: background 0.2s;
}

.lb-close { top: 20px; right: 20px; }
.lb-prev  { left: 20px; top: 50%; transform: translateY(-50%); }
.lb-next  { right: 20px; top: 50%; transform: translateY(-50%); }

.lb-close:hover, .lb-prev:hover, .lb-next:hover {
  background: rgba(255,255,255,0.25);
}
</style>
