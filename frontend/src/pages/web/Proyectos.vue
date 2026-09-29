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

        <!-- Clientes -->
        <div class="clientes-block">
          <span class="clientes-tag">Trabajamos con</span>
          <h3>Nuestros clientes</h3>
          <p>ECOSER presta servicios a las principales empresas mineras que operan en la región Moquegua.</p>
          <div class="clientes-logos">
            <div class="cliente-logo">
              <img :src="'/uploads/img/clientes/2222.png'" alt="Anglo American" />
            </div>
            <div class="cliente-logo">
              <img :src="'/uploads/img/clientes/southern-peru.jpg'" alt="Southern Perú" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section bg-light">
      <div class="container">
        <div class="section-head">
          <span class="tag">ECOSER en cifras</span>
          <h2>Nuestra Empresa Comunal</h2>
        </div>

        <div class="ec-catalogo-grid">
          <div
            v-for="s in catalogoServicios"
            :key="s.nombre"
            class="ec-cat-card"
            :class="{ 'ec-cat-destacado': s.destacado, 'ec-cat-img': s.img }"
          >
            <img v-if="s.img" :src="s.img" :alt="s.nombre" class="ec-cat-img-el" />
            <div class="ec-cat-body">
              <span v-if="s.destacado" class="ec-nuevo-tag">Servicio destacado</span>
              <div class="ec-cat-icon"><ion-icon :name="s.icon"></ion-icon></div>
              <h4>{{ s.nombre }}</h4>
              <p>{{ s.desc }}</p>
            </div>
          </div>
        </div>

        <div class="ec-consejo">
          <div class="ec-periodo-card" v-for="(c, idx) in consejoAdministracion" :key="c.periodo">
            <button
              type="button"
              class="ec-periodo-head"
              :class="c.vigente ? 'vigente' : 'anterior'"
              @click="toggleConsejo(idx)"
            >
              <span class="ec-periodo-tag">
                <span class="ec-tag-badge" :class="c.vigente ? 'vigente' : 'anterior'">
                  {{ c.vigente ? 'En ejercicio' : 'Período anterior' }}
                </span>
                <span class="ec-periodo-titulo" :class="c.vigente ? 'vigente' : 'anterior'">{{ c.periodo }}</span>
              </span>
              <ion-icon
                name="chevron-down-outline"
                class="ec-chevron"
                :class="[c.vigente ? 'vigente' : 'anterior', { open: consejoAbiertos.includes(idx) }]"
              ></ion-icon>
            </button>
            <div class="ec-periodo-body" v-show="consejoAbiertos.includes(idx)">
              <div class="ec-dir-grid">
                <div
                  v-for="(m, i) in c.miembros"
                  :key="m.cargo"
                  class="ec-dir-item"
                  :class="{ dg: i === 0 }"
                >
                  <div class="ec-dir-cargo">{{ m.cargo }}</div>
                  <div class="ec-dir-nombre">{{ m.nombre }}</div>
                </div>
              </div>
              <div v-if="c.asiento" class="ec-asiento-ref">
                <ion-icon name="document-text-outline"></ion-icon>
                Inscrito en Asiento {{ c.asiento }} · Partida Registral N° 11001608
              </div>
            </div>
          </div>
        </div>

        <div class="ec-registro-strip">
          <ion-icon name="business-outline"></ion-icon>
          <span>Empresa constituida por Escritura Pública N° 080 del 21/01/2020 · Notario Oscar Valencia Huisa, Moquegua · Inscrita en Partida Registral N° 11001608 · SUNARP Zona Registral XIII.</span>
        </div>

        <p class="ec-footer-note">
          ECOSER TPCT es una empresa de propiedad colectiva de los comuneros de Tumilaca, Pocata, Coscore y Tala.<br />
          Todos los beneficios se reinvierten en el desarrollo de la comunidad.
        </p>

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
  { tipo: 'imagen', src: '/uploads/img/ecoser/02.png', titulo: 'Equipo ECOSER' },
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

const catalogoServicios = [
  { icon: 'bonfire-outline', nombre: 'Apoyo a exploración minera', desc: 'Construcción e implementación de campamentos para exploraciones. Apoyo logístico integral y suministro de personal comunal para trabajos de geofísica y actividades de campo.', destacado: true, img: '/uploads/img/ecoser/apoyologistico.jpeg' },
  { icon: 'construct-outline', nombre: 'Obras civiles y construcción', desc: 'Edificaciones, vías, canales, obras de saneamiento y proyectos de infraestructura en general.', img: '/uploads/img/ecoser/3.jpeg' },
  { icon: 'diamond-outline', nombre: 'Minería y laboratorio', desc: 'Actividades de cateo, exploración y explotación minera. Análisis de suelos, concretos y asfaltos.' },
  { icon: 'car-outline', nombre: 'Transporte', desc: 'Transporte público de pasajeros y carga de concentrados y minerales a nivel local, regional y nacional.', img: '/uploads/img/variadas/tala2.png' },
  { icon: 'cog-outline', nombre: 'Mantenimiento industrial', desc: 'Mantenimiento de plantas, equipos y maquinaria. Limpieza industrial y operación de instalaciones.' },
  { icon: 'leaf-outline', nombre: 'Agroindustria', desc: 'Crianza de ganado, cultivos, procesamiento de productos agrícolas y comercialización agropecuaria.' },
  { icon: 'stats-chart-outline', nombre: 'Consultoría', desc: 'Formulación y ejecución de proyectos de inversión. Consultoría social, ambiental y de ingeniería.' },
  { icon: 'water-outline', nombre: 'Combustibles y energía', desc: 'Distribución de GLP y GNV. Estaciones de servicio y venta de lubricantes e hidrocarburos.' },
  { icon: 'hammer-outline', nombre: 'Servicios generales', desc: 'Mecánica, electricidad, carpintería, limpieza industrial y mantenimiento de espacios comunes.', img: '/uploads/img/ecoser/2.jpeg' },
]

const consejoAdministracion = [
  {
    periodo: 'Mayo 2026 — Mayo 2028',
    vigente: true,
    asiento: null,
    miembros: [
      { cargo: 'Director general', nombre: 'Miguel Ángel Lazo Coayla' },
      { cargo: 'Subdirectora general', nombre: 'Dionilde Flora Flores Calizaya' },
      { cargo: 'Sec. de actas y archivo', nombre: 'Patricia Lidia Flores Gutiérrez' },
      { cargo: 'Director de economía', nombre: 'David Lucio Marca Arambulo' },
      { cargo: 'Vocal', nombre: 'Marco Antonio Centeno Quispe' },
      { cargo: 'Fiscal', nombre: 'Germán Fidel Coaila García' },
    ],
  },
  {
    periodo: 'Mayo 2023 — Mayo 2026',
    vigente: false,
    asiento: 'A000043',
    miembros: [
      { cargo: 'Director general', nombre: 'Rubén Benedicto Centeno Soto' },
      { cargo: 'Subdirector general', nombre: 'Marcelo Julián Gutiérrez Mamani' },
      { cargo: 'Sec. de actas y archivos', nombre: 'Angélica Vilma Paripanca Ramos' },
      { cargo: 'Director de economía', nombre: 'Yonathan Michael Cabana Paripanca' },
      { cargo: 'Vocal', nombre: 'Candelaria Hilda Cabana Cuaila' },
      { cargo: 'Fiscal', nombre: 'José Bernardo Cuaila Coayla' },
    ],
  },
]

const consejoAbiertos = ref([0])
function toggleConsejo(idx) {
  const i = consejoAbiertos.value.indexOf(idx)
  if (i === -1) consejoAbiertos.value.push(idx)
  else consejoAbiertos.value.splice(i, 1)
}
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

.clientes-block {
  margin-top: 56px;
  padding: 40px 32px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 20px;
  text-align: center;
  color: white;
}
.clientes-tag {
  display: inline-block; padding: 4px 14px;
  background: rgba(134,239,172,0.15); color: #86efac;
  border-radius: 100px; font-size: 11px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;
}
.clientes-block h3 { font-size: 1.5rem; font-weight: 700; margin-bottom: 8px; }
.clientes-block p { font-size: 14px; color: rgba(255,255,255,0.7); max-width: 600px; margin: 0 auto 28px; line-height: 1.6; }
.clientes-logos {
  display: flex; justify-content: center; align-items: center;
  gap: 48px; flex-wrap: wrap;
}
.cliente-logo {
  display: flex; flex-direction: column; align-items: center; gap: 10px;
  background: white; border-radius: 14px; padding: 20px 28px;
  min-width: 200px; transition: transform 0.2s, box-shadow 0.2s;
}
.cliente-logo:hover { transform: translateY(-4px); box-shadow: 0 12px 28px rgba(0,0,0,0.25); }
.cliente-logo img { max-height: 60px; max-width: 180px; object-fit: contain; }
.cliente-logo span { font-size: 12px; font-weight: 600; color: #0a1e0c; text-transform: uppercase; letter-spacing: 0.5px; }

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
  .galeria-grid { grid-template-columns: repeat(2, 1fr); }
  .cta-ecoser { padding: 32px 24px; }
}
@media (max-width: 480px) {
  .lineas-grid { grid-template-columns: 1fr; }
  .galeria-grid { grid-template-columns: 1fr; }
}

.ec-catalogo-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 48px; }
.ec-cat-card { position: relative; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; overflow: hidden; }
.ec-cat-card.ec-cat-destacado { border: 1.5px solid #b45309; background: #fffbf0; }
.ec-cat-card.ec-cat-img { padding: 0; display: flex; flex-direction: column; }
.ec-cat-img-el { width: 100%; height: 160px; object-fit: cover; }
.ec-cat-card.ec-cat-img .ec-cat-body { padding: 20px; }
.ec-nuevo-tag { display: inline-block; font-size: 11px; font-weight: 700; background: #fef3c7; color: #7c3d12; border-radius: 6px; padding: 2px 10px; margin-bottom: 10px; }
.ec-cat-icon { width: 44px; height: 44px; border-radius: 10px; background: #dcfce7; display: flex; align-items: center; justify-content: center; font-size: 22px; color: #16a34a; margin-bottom: 14px; }
.ec-cat-card.ec-cat-destacado .ec-cat-icon { background: #ffedd5; color: #9a3412; }
.ec-cat-card h4 { font-size: 15px; font-weight: 700; color: #1a2e1a; margin-bottom: 6px; }
.ec-cat-card p { font-size: 13px; color: #64748b; line-height: 1.6; }

/* ECOSER: CONSEJO DE ADMINISTRACIÓN */
.ec-consejo { display: flex; flex-direction: column; gap: 12px; margin-bottom: 32px; }
.ec-periodo-card { border: 1px solid #e2e8f0; border-radius: 14px; overflow: hidden; background: #fff; }
.ec-periodo-head { width: 100%; display: flex; align-items: center; justify-content: space-between; padding: 14px 18px; border: none; cursor: pointer; font-family: inherit; text-align: left; }
.ec-periodo-head.vigente { background: #16a34a; }
.ec-periodo-head.anterior { background: #f1f5f9; }
.ec-periodo-tag { display: flex; align-items: center; gap: 10px; }
.ec-tag-badge { font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 100px; }
.ec-tag-badge.vigente { background: rgba(255,255,255,0.2); color: #dcfce7; }
.ec-tag-badge.anterior { background: #e2e8f0; color: #64748b; }
.ec-periodo-titulo { font-size: 14px; font-weight: 700; }
.ec-periodo-titulo.vigente { color: #fff; }
.ec-periodo-titulo.anterior { color: #1a2e1a; }
.ec-chevron { font-size: 18px; transition: transform 0.2s; }
.ec-chevron.vigente { color: rgba(255,255,255,0.8); }
.ec-chevron.anterior { color: #94a3b8; }
.ec-chevron.open { transform: rotate(180deg); }

.ec-periodo-body { padding: 16px 18px 20px; border-top: 1px solid #e2e8f0; background: #fff; }
.ec-dir-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.ec-dir-item { background: #f8fafc; border-radius: 10px; padding: 12px 14px; }
.ec-dir-item.dg { grid-column: 1 / -1; background: #dcfce7; border: 1px solid #16a34a; }
.ec-dir-cargo { font-size: 11px; font-weight: 700; color: #16a34a; text-transform: uppercase; letter-spacing: 0.04em; }
.ec-dir-nombre { font-size: 14px; color: #1a2e1a; margin-top: 2px; }
.ec-asiento-ref { font-size: 12px; color: #94a3b8; margin-top: 14px; display: flex; align-items: center; gap: 6px; }

.ec-registro-strip { display: flex; align-items: flex-start; gap: 12px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 18px; margin-bottom: 24px; }
.ec-registro-strip ion-icon { font-size: 20px; color: #16a34a; flex-shrink: 0; margin-top: 1px; }
.ec-registro-strip span { font-size: 13px; color: #64748b; line-height: 1.6; }

.ec-footer-note { font-size: 12px; color: #94a3b8; text-align: center; line-height: 1.6; padding-top: 16px; border-top: 1px solid #e2e8f0; }

@media (max-width: 1024px) {
  .ec-catalogo-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .ec-dir-grid { grid-template-columns: 1fr; }
}
@media (max-width: 480px) {
  .ec-catalogo-grid { grid-template-columns: 1fr; }
}
</style>
