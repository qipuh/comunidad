<template>
  <LayoutPublico>
    <section class="page-hero" :style="{ backgroundImage: `url('/uploads/img/ecoser/01.png')` }">
      <div class="ph-overlay"></div>
      <div class="ph-content">
        <span class="ph-tag"><ion-icon name="construct-outline"></ion-icon> Proyectos</span>
        <h1>Proyectos y Empresa ECOSER</h1>
        <p>Iniciativas para el desarrollo integral de nuestra comunidad</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head">
          <span class="tag">Nuestras líneas</span>
          <h2>Líneas de Intervención</h2>
        </div>
        <div class="lineas-grid">
          <div v-for="l in lineas" :key="l.titulo" class="linea-card">
            <ion-icon :name="l.icon"></ion-icon>
            <h3>{{ l.titulo }}</h3>
            <p>{{ l.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section bg-dark">
      <div class="container">
        <div class="ecoser-hero">
          <div class="ecoser-badge">Empresa Comunal</div>
          <h2>🌿 ECOSER</h2>
          <p>Brazo operativo y económico de la Comunidad Campesina TPCT, orientado a la prestación de servicios y generación de oportunidades laborales para los Usuarios.</p>
        </div>
        <div class="ecoser-grid">
          <div class="eco-col">
            <h3>Objetivos</h3>
            <div class="eco-lista">
              <div v-for="o in objetivos" :key="o" class="eco-item">
                <ion-icon name="checkmark-circle-outline"></ion-icon>
                <span>{{ o }}</span>
              </div>
            </div>
          </div>
          <div class="eco-col">
            <h3>Ventajas</h3>
            <div class="eco-lista">
              <div v-for="v in ventajas" :key="v" class="eco-item">
                <ion-icon name="star-outline"></ion-icon>
                <span>{{ v }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section bg-light">
      <div class="container">
        <div class="section-head">
          <span class="tag">Lo que ofrecemos</span>
          <h2>Servicios ECOSER</h2>
        </div>
        <div class="servicios-grid">
          <div v-for="s in servicios" :key="s.nombre" class="servicio-card">
            <img :src="s.img" :alt="s.nombre" />
            <div class="sc-body">
              <ion-icon :name="s.icon"></ion-icon>
              <h3>{{ s.nombre }}</h3>
              <p>{{ s.desc }}</p>
            </div>
          </div>
        </div>
        <div class="ecoser-galeria">
          <div class="section-head">
            <span class="tag">ECOSER en acción</span>
            <h2>Galería de Operaciones</h2>
          </div>
          <div class="galeria-grid">
            <div v-for="item in galeriaEcoser" :key="item.src" class="galeria-item" :class="{ 'is-video': item.tipo === 'video' }" @click="abrirMedia(item)">
              <img v-if="item.tipo === 'imagen'" :src="item.src" :alt="item.titulo" />
              <video v-else :src="item.src" muted preload="metadata" playsinline></video>
              <div class="gi-overlay">
                <ion-icon :name="item.tipo === 'video' ? 'play-circle-outline' : 'expand-outline'"></ion-icon>
                <span>{{ item.titulo }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="cta-ecoser">
          <h3>¿Tu empresa necesita nuestros servicios?</h3>
          <p>Contamos con mano de obra local, conocimiento del territorio y organización comunal consolidada.</p>
          <button class="btn-green" @click="navegar('contacto')">
            <ion-icon name="call-outline"></ion-icon> Contactar a ECOSER
          </button>
        </div>

        <!-- Lightbox -->
        <div v-if="mediaAbierto" class="lightbox" @click.self="mediaAbierto = null">
          <button class="lb-close" @click="mediaAbierto = null"><ion-icon name="close-outline"></ion-icon></button>
          <img v-if="mediaAbierto.tipo === 'imagen'" :src="mediaAbierto.src" :alt="mediaAbierto.titulo" />
          <video v-else :src="mediaAbierto.src" controls autoplay playsinline></video>
        </div>
      </div>
    </section>
  </LayoutPublico>
</template>

<script setup>
import { ref } from 'vue'
import LayoutPublico from './LayoutPublico.vue'
import { useWebNav } from '../../composables/useWebNav'
const { navegar } = useWebNav()

const mediaAbierto = ref(null)
const abrirMedia = (item) => { mediaAbierto.value = item }

const galeriaEcoser = [
  { tipo: 'imagen', src: '/uploads/img/ecoser/01.png', titulo: 'Operaciones en campo' },
  { tipo: 'imagen', src: '/uploads/img/ecoser/02.png', titulo: 'Equipo ECOSER' },
  { tipo: 'imagen', src: '/uploads/img/ecoser/03.png', titulo: 'Servicio a la comunidad' },
  { tipo: 'video',  src: '/uploads/img/ecoser/01.mov', titulo: 'Video: trabajos en territorio' },
  { tipo: 'video',  src: '/uploads/img/ecoser/02.mov', titulo: 'Video: ECOSER en acción' },
]

const lineas = [
  { icon: 'leaf-outline', titulo: 'Desarrollo productivo', desc: 'Impulso a las actividades agrícolas y pecuarias como base de la economía familiar comunal.' },
  { icon: 'construct-outline', titulo: 'Infraestructura comunal', desc: 'Mejoramiento y construcción de obras de infraestructura para los Usuarios y sus familias.' },
  { icon: 'people-outline', titulo: 'Fortalecimiento organizacional', desc: 'Capacitación, asesoría y desarrollo de capacidades para líderes y Usuarios.' },
  { icon: 'briefcase-outline', titulo: 'Generación de empleo local', desc: 'Creación de oportunidades laborales para los Usuarios dentro del territorio.' },
]

const objetivos = [
  'Generar empleo local para los Usuarios',
  'Brindar servicios a empresas públicas y privadas',
  'Fortalecer la economía comunal',
  'Promover la participación de los Usuarios',
]

const ventajas = [
  'Conocimiento profundo del territorio',
  'Organización comunal consolidada',
  'Mano de obra local disponible',
  'Cumplimiento de acuerdos comunales',
]

const servicios = [
  { icon: 'car-outline', nombre: 'Alquiler de camionetas', desc: 'Flota de vehículos para transporte de personal y equipos en zonas de difícil acceso del distrito de Torata.', img: '/uploads/img/variadas/tala2.png' },
  { icon: 'people-outline', nombre: 'Provisión de mano de obra', desc: 'Personal Usuario capacitado para labores de campo, construcción y operaciones en general.', img: '/uploads/img/variadas/tumilaca.png' },
  { icon: 'cube-outline', nombre: 'Apoyo logístico', desc: 'Soporte integral en operaciones, abastecimiento y coordinación logística en el territorio comunal.', img: '/uploads/img/variadas/1.png' },
  { icon: 'settings-outline', nombre: 'Servicios diversos', desc: 'Atención a requerimientos específicos de empresas e instituciones que operan en la zona de influencia.', img: '/uploads/img/variadas/2.png' },
]
</script>

<style scoped>
.page-hero { min-height: 55vh; background-size: cover; background-position: center; display: flex; align-items: center; position: relative; }
.ph-overlay { position: absolute; inset: 0; background: rgba(5,20,8,0.78); }
.ph-content { position: relative; z-index: 2; max-width: 1200px; margin: 0 auto; padding: 120px 24px 80px; color: white; }
.ph-tag { display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; background: rgba(134,239,172,0.15); color: #86efac; border-radius: 100px; font-size: 13px; font-weight: 600; margin-bottom: 16px; }
.ph-content h1 { font-size: clamp(2rem,4vw,3rem); font-weight: 800; margin-bottom: 10px; }
.ph-content p { font-size: 16px; color: rgba(255,255,255,0.7); }

.section { padding: 96px 0; background: white; }
.section.bg-light { background: white; }
.section.bg-dark { background: linear-gradient(160deg,#0a1e0c,#0f2814); }
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.section-head { text-align: center; margin-bottom: 56px; }
.section-head h2 { font-size: 2rem; font-weight: 800; color: #1a2e1a; }
.tag { display: inline-block; padding: 4px 14px; background: #dcfce7; color: #15803d; border-radius: 100px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }

.lineas-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 24px; }
.linea-card { background: #f8fafc; border-radius: 16px; padding: 28px; border: 1px solid #e2e8f0; text-align: center; transition: all 0.2s; }
.linea-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.08); border-color: #86efac; }
.linea-card ion-icon { font-size: 40px; color: #16a34a; margin-bottom: 16px; }
.linea-card h3 { font-size: 16px; font-weight: 700; color: #1a2e1a; margin-bottom: 10px; }
.linea-card p { font-size: 13px; color: #4a5e4a; line-height: 1.6; }

.ecoser-hero { text-align: center; color: white; margin-bottom: 56px; }
.ecoser-badge { display: inline-block; padding: 4px 14px; background: rgba(134,239,172,0.15); color: #86efac; border-radius: 100px; font-size: 12px; font-weight: 700; margin-bottom: 12px; }
.ecoser-hero h2 { font-size: 2.5rem; font-weight: 800; margin-bottom: 16px; }
.ecoser-hero p { font-size: 16px; color: rgba(255,255,255,0.75); max-width: 700px; margin: 0 auto; line-height: 1.8; }

.ecoser-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
.eco-col { background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.12); border-radius: 16px; padding: 32px; }
.eco-col h3 { font-size: 18px; font-weight: 700; color: #86efac; margin-bottom: 20px; }
.eco-lista { display: flex; flex-direction: column; gap: 14px; }
.eco-item { display: flex; align-items: flex-start; gap: 12px; color: rgba(255,255,255,0.85); font-size: 15px; }
.eco-item ion-icon { font-size: 20px; color: #86efac; flex-shrink: 0; margin-top: 2px; }

.servicios-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 24px; margin-bottom: 48px; }
.servicio-card { background: #f8fafc; border-radius: 16px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.servicio-card img { width: 100%; height: 200px; object-fit: cover; }
.sc-body { padding: 24px; }
.sc-body ion-icon { font-size: 28px; color: #16a34a; margin-bottom: 10px; }
.sc-body h3 { font-size: 18px; font-weight: 700; color: #1a2e1a; margin-bottom: 8px; }
.sc-body p { font-size: 14px; color: #4a5e4a; line-height: 1.7; }

.ecoser-galeria { margin: 0 0 56px; }
.ecoser-galeria .section-head { margin-bottom: 32px; }
.galeria-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.galeria-item {
  position: relative; aspect-ratio: 4/3; border-radius: 14px; overflow: hidden;
  cursor: pointer; background: #e5e7eb; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}
.galeria-item:hover { transform: translateY(-3px); box-shadow: 0 12px 24px rgba(0,0,0,0.15); }
.galeria-item img, .galeria-item video { width: 100%; height: 100%; object-fit: cover; display: block; }
.gi-overlay {
  position: absolute; inset: 0; display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 8px; color: white;
  background: linear-gradient(180deg, transparent 40%, rgba(0,0,0,0.7));
  opacity: 0; transition: opacity 0.2s;
}
.galeria-item:hover .gi-overlay { opacity: 1; }
.galeria-item.is-video .gi-overlay { opacity: 1; background: linear-gradient(180deg, transparent 30%, rgba(0,0,0,0.55)); }
.gi-overlay ion-icon { font-size: 48px; }
.galeria-item.is-video .gi-overlay ion-icon { font-size: 64px; filter: drop-shadow(0 2px 8px rgba(0,0,0,0.4)); }
.gi-overlay span { font-size: 13px; font-weight: 600; padding: 0 12px; text-align: center; }

.lightbox {
  position: fixed; inset: 0; background: rgba(0,0,0,0.92); z-index: 9999;
  display: flex; align-items: center; justify-content: center; padding: 24px;
}
.lightbox img, .lightbox video {
  max-width: 95vw; max-height: 90vh; border-radius: 8px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.lb-close {
  position: absolute; top: 20px; right: 20px; width: 44px; height: 44px;
  background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.25);
  border-radius: 50%; color: white; font-size: 24px; cursor: pointer;
  display: flex; align-items: center; justify-content: center; transition: background 0.2s;
}
.lb-close:hover { background: rgba(255,255,255,0.25); }

.cta-ecoser { background: linear-gradient(135deg,#0a1e0c,#16a34a); border-radius: 20px; padding: 48px; text-align: center; color: white; display: flex; flex-direction: column; align-items: center; gap: 16px; }
.cta-ecoser h3 { font-size: 1.6rem; font-weight: 800; }
.cta-ecoser p { font-size: 15px; color: rgba(255,255,255,0.8); max-width: 600px; line-height: 1.7; }
.btn-green { display: inline-flex; align-items: center; gap: 8px; padding: 12px 28px; background: white; color: #15803d; border: none; border-radius: 10px; font-size: 15px; font-weight: 700; text-decoration: none; cursor: pointer; font-family: inherit; transition: all 0.2s; }
.btn-green:hover { background: #f0fdf4; }

@media (max-width: 768px) {
  .lineas-grid { grid-template-columns: repeat(2,1fr); }
  .ecoser-grid { grid-template-columns: 1fr; }
  .servicios-grid { grid-template-columns: 1fr; }
  .galeria-grid { grid-template-columns: repeat(2, 1fr); }
  .cta-ecoser { padding: 32px 24px; }
}
@media (max-width: 480px) {
  .lineas-grid { grid-template-columns: 1fr; }
  .galeria-grid { grid-template-columns: 1fr; }
}
</style>
