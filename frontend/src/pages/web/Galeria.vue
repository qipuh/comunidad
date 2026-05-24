<template>
  <LayoutPublico>
    <section class="page-hero" :style="{ backgroundImage: `url('/uploads/img/inicio/cerro_baul.png')` }">
      <div class="ph-overlay"></div>
      <div class="ph-content">
        <span class="ph-tag"><ion-icon name="images-outline"></ion-icon> Galería</span>
        <h1>Galería Fotográfica</h1>
        <p>Imágenes que reflejan la vida, el trabajo y la identidad de nuestra comunidad</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="filtros">
          <button v-for="f in filtros" :key="f.key" :class="['filtro-btn', { active: filtroActivo === f.key }]" @click="filtroActivo = f.key">
            {{ f.label }}
          </button>
        </div>

        <div class="galeria-grid">
          <div v-for="foto in fotosFiltradas" :key="foto.id" class="foto-item" :class="foto.grande ? 'grande' : ''" @click="abrirFoto(foto)">
            <img :src="foto.img" :alt="foto.titulo" />
            <div class="foto-overlay">
              <ion-icon name="expand-outline"></ion-icon>
              <span>{{ foto.titulo }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Lightbox -->
    <div v-if="fotoActiva" class="lightbox" @click.self="fotoActiva = null">
      <button class="lb-close" @click="fotoActiva = null"><ion-icon name="close-outline"></ion-icon></button>
      <div class="lb-content">
        <img :src="fotoActiva.img" :alt="fotoActiva.titulo" />
        <div class="lb-info">
          <span class="lb-cat">{{ fotoActiva.categoriaLabel }}</span>
          <h3>{{ fotoActiva.titulo }}</h3>
          <p>{{ fotoActiva.desc }}</p>
        </div>
      </div>
    </div>
  </LayoutPublico>
</template>

<script setup>
import { ref, computed } from 'vue'
import LayoutPublico from './LayoutPublico.vue'

const filtroActivo = ref('todas')
const fotoActiva = ref(null)

const filtros = [
  { key: 'todas',       label: 'Todas' },
  { key: 'comunidad',   label: 'Comunidad' },
  { key: 'territorio',  label: 'Territorio' },
  { key: 'actividades', label: 'Actividades' },
]

const fotos = [
  // COMUNIDAD
  { id: 1, categoria: 'comunidad', categoriaLabel: 'Comunidad', grande: true,
    titulo: 'Nuestra Comunidad TPCT', desc: 'Familias comuneras unidas por la tierra y las tradiciones del valle de Tumilaca.',
    img: '/uploads/img/nosotros/comunidad.jpeg' },
  { id: 2, categoria: 'comunidad', categoriaLabel: 'Comunidad',
    titulo: 'Anexo Tumilaca', desc: 'Vista del anexo de Tumilaca, corazón productivo del valle.',
    img: '/uploads/img/nosotros/tumilala.png' },
  { id: 3, categoria: 'comunidad', categoriaLabel: 'Comunidad',
    titulo: 'Tumilaca en acción', desc: 'Actividades cotidianas de los Usuarios en el anexo de Tumilaca.',
    img: '/uploads/img/nosotros/tumilala2.png' },

  // TERRITORIO
  { id: 4, categoria: 'territorio', categoriaLabel: 'Territorio', grande: true,
    titulo: 'Cerro Baúl', desc: 'Hito arqueológico y cultural emblemático del territorio comunal.',
    img: '/uploads/img/inicio/cerro_baul.png' },
  { id: 5, categoria: 'territorio', categoriaLabel: 'Territorio',
    titulo: 'Cementerio de Pocata', desc: 'Cementerio comunal histórico del anexo Pocata.',
    img: '/uploads/img/inicio/cementerio_pocata.png' },
  { id: 6, categoria: 'territorio', categoriaLabel: 'Territorio',
    titulo: 'Vista del valle', desc: 'Panorámica del territorio comunal en el distrito de Torata.',
    img: '/uploads/img/inicio/01.png' },
  { id: 7, categoria: 'territorio', categoriaLabel: 'Territorio',
    titulo: 'Paisaje comunal', desc: 'Diversidad geográfica del territorio de la comunidad TPCT.',
    img: '/uploads/img/heroimage.jpeg' },

  // ACTIVIDADES — ECOSER
  { id: 8, categoria: 'actividades', categoriaLabel: 'Actividades',
    titulo: 'ECOSER en operaciones', desc: 'Trabajos de la empresa comunal ECOSER en el territorio.',
    img: '/uploads/img/ecoser/01.png' },
  { id: 9, categoria: 'actividades', categoriaLabel: 'Actividades',
    titulo: 'Equipo ECOSER', desc: 'Mano de obra local capacitada para servicios diversos.',
    img: '/uploads/img/ecoser/02.png' },
  { id: 10, categoria: 'actividades', categoriaLabel: 'Actividades', grande: true,
    titulo: 'Servicios al territorio', desc: 'ECOSER brindando servicios a la comunidad y empresas de la zona.',
    img: '/uploads/img/ecoser/03.png' },
]

const fotosFiltradas = computed(() =>
  filtroActivo.value === 'todas' ? fotos : fotos.filter(f => f.categoria === filtroActivo.value)
)

function abrirFoto(foto) {
  fotoActiva.value = foto
}
</script>

<style scoped>
.page-hero { min-height: 55vh; background-size: cover; background-position: center; display: flex; align-items: center; position: relative; }
.ph-overlay { position: absolute; inset: 0; background: rgba(5,20,8,0.72); }
.ph-content { position: relative; z-index: 2; max-width: 1200px; margin: 0 auto; padding: 120px 24px 80px; color: white; }
.ph-tag { display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; background: rgba(134,239,172,0.15); color: #86efac; border-radius: 100px; font-size: 13px; font-weight: 600; margin-bottom: 16px; }
.ph-content h1 { font-size: clamp(2rem,4vw,3rem); font-weight: 800; margin-bottom: 10px; }
.ph-content p { font-size: 16px; color: rgba(255,255,255,0.7); }

.section { padding: 96px 0; background: white; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }

.filtros { display: flex; gap: 10px; margin-bottom: 48px; flex-wrap: wrap; }
.filtro-btn { padding: 8px 20px; border: 1px solid #e2e8f0; background: white; border-radius: 100px; font-size: 14px; font-weight: 600; color: #64748b; cursor: pointer; transition: all 0.2s; }
.filtro-btn:hover { border-color: #16a34a; color: #16a34a; }
.filtro-btn.active { background: #16a34a; color: white; border-color: #16a34a; }

.galeria-grid { display: grid; grid-template-columns: repeat(3,1fr); grid-auto-rows: 240px; gap: 16px; }
.foto-item { border-radius: 14px; overflow: hidden; cursor: pointer; position: relative; }
.foto-item.grande { grid-column: span 2; }
.foto-item img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s; display: block; }
.foto-item:hover img { transform: scale(1.05); }
.foto-overlay { position: absolute; inset: 0; background: rgba(5,20,8,0); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; color: white; transition: background 0.3s; }
.foto-item:hover .foto-overlay { background: rgba(5,20,8,0.55); }
.foto-overlay ion-icon { font-size: 32px; opacity: 0; transform: scale(0.7); transition: all 0.3s; }
.foto-overlay span { font-size: 15px; font-weight: 600; opacity: 0; transition: opacity 0.3s; text-align: center; padding: 0 16px; }
.foto-item:hover .foto-overlay ion-icon,
.foto-item:hover .foto-overlay span { opacity: 1; transform: scale(1); }

.lightbox { position: fixed; inset: 0; background: rgba(0,0,0,0.92); z-index: 1000; display: flex; align-items: center; justify-content: center; padding: 24px; }
.lb-close { position: absolute; top: 24px; right: 24px; width: 44px; height: 44px; border-radius: 50%; background: rgba(255,255,255,0.15); border: none; color: white; font-size: 24px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.lb-content { max-width: 900px; width: 100%; background: #1e293b; border-radius: 20px; overflow: hidden; }
.lb-content img { width: 100%; max-height: 560px; object-fit: cover; display: block; }
.lb-info { padding: 24px 28px; }
.lb-cat { display: inline-block; padding: 3px 12px; background: rgba(134,239,172,0.15); color: #86efac; border-radius: 100px; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 10px; }
.lb-info h3 { font-size: 20px; font-weight: 700; color: white; margin-bottom: 8px; }
.lb-info p { font-size: 14px; color: rgba(255,255,255,0.65); line-height: 1.7; }

@media (max-width: 768px) { .galeria-grid { grid-template-columns: repeat(2,1fr); grid-auto-rows: 180px; } .foto-item.grande { grid-column: span 2; } }
@media (max-width: 480px) { .galeria-grid { grid-template-columns: 1fr; grid-auto-rows: 200px; } .foto-item.grande { grid-column: span 1; } }
</style>
