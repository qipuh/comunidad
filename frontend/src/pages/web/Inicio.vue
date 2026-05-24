<template>
  <LayoutPublico>

    <!-- HERO con fondo e imagen, overlay degradado -->
    <section class="hero" :style="{ backgroundImage: `url('/uploads/img/inicio/01.png')` }">
      <div class="hero-overlay"></div>
      <div class="hero-inner">
        <div class="hero-text">
          <div class="hero-badge">
            <ion-icon name="location-outline"></ion-icon>
            Torata · Mariscal Nieto · Moquegua
          </div>
          <h1>Comunidad Campesina<br><span class="green">Tumilaca, Pocata,</span><br>Coscore y Tala</h1>
          <p>Territorio, organización y desarrollo sostenible al servicio de los Usuarios del valle de Tumilaca.</p>
          <div class="hero-btns">
            <button class="btn-primary" @click="nav('nosotros')">
              <ion-icon name="people-outline"></ion-icon> Conocer más
            </button>
            <button class="btn-secondary" @click="nav('contacto')">
              <ion-icon name="call-outline"></ion-icon> Contáctanos
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- STATS BAR -->
    <section class="stats-bar">
      <div class="stats-inner">
        <div class="stat" v-for="s in stats" :key="s.label">
          <div class="stat-icon"><ion-icon :name="s.icon"></ion-icon></div>
          <div>
            <strong>{{ s.value }}</strong>
            <span>{{ s.label }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- SOBRE NOSOTROS estilo Charit -->
    <section class="section sobre">
      <div class="container">
        <div class="sobre-grid">
          <div class="sobre-images">
            <img :src="'/uploads/img/inicio/cerro_baul.png'" alt="Cerro Baúl, hito ancestral del territorio" class="si-top" />
            <img :src="'/uploads/img/inicio/cementerio_pocata.png'" alt="Cementerio comunal de Pocata" class="si-bottom" />
            <div class="si-badge">
              <strong>77</strong>
              <span>años de historia</span>
            </div>
          </div>
          <div class="sobre-text">
            <span class="tag-green">Nuestra Comunidad</span>
            <h2>Una familia unida por la tierra y las tradiciones</h2>
            <p>En la Comunidad Campesina de Tumilaca, Pocata, Coscore y Tala (TPCT), cada Usuario es parte de una gran familia. Desde 1949, compartimos no solo la tierra, sino también sueños, luchas y celebraciones. Aquí, el trabajo colectivo y el respeto mutuo nos unen en un camino hacia un futuro sostenible.</p>
            <div class="sobre-stats">
              <div class="ss-item" v-for="s in sobreStats" :key="s.label">
                <strong>{{ s.value }}</strong>
                <span>{{ s.label }}</span>
              </div>
            </div>
            <button class="btn-primary" @click="nav('nosotros')">
              Únete a nuestra historia <ion-icon name="arrow-forward-outline"></ion-icon>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- PILARES -->
    <section class="section bg-mint pilares">
      <div class="container">
        <div class="section-head">
          <span class="tag-green">Lo que nos define</span>
          <h2>Nuestros pilares</h2>
        </div>
        <div class="pilares-grid">
          <div v-for="p in pilares" :key="p.key" class="pilar-card" @click="nav(p.key)">
            <div class="pilar-img">
              <img :src="p.img" :alt="p.titulo" />
            </div>
            <div class="pilar-body">
              <div class="pilar-icon"><ion-icon :name="p.icon"></ion-icon></div>
              <h3>{{ p.titulo }}</h3>
              <p>{{ p.desc }}</p>
              <span class="pilar-link">Ver más <ion-icon name="arrow-forward-outline"></ion-icon></span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- GALERÍA STRIP: 3 fotos full-width -->
    <section class="galeria-strip">
      <div class="gs-item" v-for="img in galeriaStrip" :key="img.alt" @click="nav('galeria')">
        <img :src="img.src" :alt="img.alt" />
        <div class="gs-label">{{ img.alt }}</div>
      </div>
    </section>

    <!-- NOTICIAS -->
    <section class="section bg-mint noticias-home">
      <div class="container">
        <div class="section-head">
          <span class="tag-green">Actualidad</span>
          <h2>Últimas noticias</h2>
        </div>
        <div class="noticias-grid">
          <div v-for="n in noticias" :key="n.titulo" class="noticia-card" @click="nav('noticias')">
            <div class="nc-img">
              <img :src="n.img" :alt="n.titulo" />
              <span class="nc-tipo">{{ n.tipo }}</span>
            </div>
            <div class="nc-body">
              <span class="nc-fecha"><ion-icon name="calendar-outline"></ion-icon> {{ n.fecha }}</span>
              <h4>{{ n.titulo }}</h4>
              <p>{{ n.resumen }}</p>
              <span class="nc-link">Leer más <ion-icon name="arrow-forward-outline"></ion-icon></span>
            </div>
          </div>
        </div>
        <div class="text-center mt-40">
          <button class="btn-outline-dark" @click="nav('noticias')">
            Ver todas las noticias <ion-icon name="newspaper-outline"></ion-icon>
          </button>
        </div>
      </div>
    </section>

    <!-- CTA ECOSER -->
    <section class="ecoser-cta">
      <div class="ecoser-cta-bg">
        <img src="https://images.unsplash.com/photo-1550290129-41b39a6fdfe8?w=1400&q=80" alt="ECOSER comunidad" />
        <div class="ecoser-overlay"></div>
      </div>
      <div class="container">
        <div class="ecoser-content">
          <span class="tag-light">Empresa Comunal</span>
          <h2>¿Necesitas los servicios de ECOSER?</h2>
          <p>Transporte, mano de obra local y apoyo logístico en el distrito de Torata. Moquegua – Perú.</p>
          <div class="ecoser-btns">
            <button class="btn-white" @click="nav('proyectos')">
              <ion-icon name="briefcase-outline"></ion-icon> Conocer ECOSER
            </button>
            <button class="btn-outline-white" @click="nav('contacto')">
              <ion-icon name="call-outline"></ion-icon> Contactar
            </button>
          </div>
        </div>
      </div>
    </section>

  </LayoutPublico>
</template>

<script setup>
import LayoutPublico from './LayoutPublico.vue'
import { useWebNav } from '../../composables/useWebNav'

const { navegar } = useWebNav()
function nav(p) { navegar(p) }

const stats = [
  { icon: 'calendar-outline', value: '1949',    label: 'Año de fundación' },
  { icon: 'trophy-outline',   value: '77 años', label: 'De historia comunal' },
  { icon: 'map-outline',      value: '4',       label: 'Anexos comunales' },
  { icon: 'people-outline',   value: '100+',    label: 'Usuarios activos' },
]

const sobreStats = [
  { value: '4',    label: 'Anexos territoriales' },
  { value: '1949', label: 'Año de fundación' },
  { value: '100+', label: 'Familias comuneras' },
]

const pilares = [
  {
    key: 'organizacion', icon: 'business-outline', titulo: 'Organización Comunal',
    desc: 'Estructura democrática y participativa liderada por la Asamblea General de Usuarios.',
    img: 'https://images.unsplash.com/photo-1519074598089-6436475c7f8f?w=600&q=80',
  },
  {
    key: 'territorio', icon: 'map-outline', titulo: 'Nuestro Territorio',
    desc: 'Extensas tierras en el valle de Tumilaca y zonas altoandinas del distrito de Torata.',
    img: 'https://images.unsplash.com/photo-1593460915132-fcb729cc4597?w=600&q=80',
  },
  {
    key: 'produccion', icon: 'leaf-outline', titulo: 'Desarrollo Productivo',
    desc: 'Producción agrícola y pecuaria como base del sustento de las familias comuneras.',
    img: 'https://images.unsplash.com/photo-1553550491-0895a24ffdac?w=600&q=80',
  },
  {
    key: 'proyectos', icon: 'construct-outline', titulo: 'Empresa ECOSER',
    desc: 'Brazo económico de la comunidad que genera empleo y presta servicios empresariales.',
    img: 'https://images.unsplash.com/photo-1536705284215-000a0c2f0406?w=600&q=80',
  },
]

const galeriaStrip = [
  { src: '/uploads/img/inicio/01.png',                alt: 'Nuestro territorio comunal' },
  { src: '/uploads/img/inicio/cerro_baul.png',        alt: 'Cerro Baúl · Patrimonio cultural' },
  { src: '/uploads/img/inicio/cementerio_pocata.png', alt: 'Cementerio comunal de Pocata' },
]

const noticias = [
  {
    tipo: 'Aniversario', fecha: 'Abril 2026',
    titulo: '77° Aniversario de la Comunidad TPCT',
    resumen: 'La comunidad celebra su 77° aniversario con actividades culturales, deportivas y asambleas comunales.',
    img: 'https://images.unsplash.com/photo-1589682449071-d13c27d1c298?w=600&q=80',
  },
  {
    tipo: 'Asamblea', fecha: 'Marzo 2026',
    titulo: 'Acuerdos de la Asamblea General Ordinaria',
    resumen: 'Se aprobaron los estados financieros del ejercicio 2025 y el plan de trabajo para el año en curso.',
    img: 'https://images.unsplash.com/photo-1519074598089-6436475c7f8f?w=600&q=80',
  },
  {
    tipo: 'ECOSER', fecha: 'Febrero 2026',
    titulo: 'ECOSER firma nuevo contrato de servicios',
    resumen: 'La empresa comunal suscribió un contrato generando 25 puestos de trabajo para Usuarios del valle.',
    img: 'https://images.unsplash.com/photo-1566793772361-1d5d9cefbd12?w=600&q=80',
  },
]
</script>

<style scoped>
.hero {
  min-height: 100vh; background-size: cover; background-position: center;
  display: flex; align-items: center; position: relative; overflow: hidden;
  padding-top: 70px;
}
.hero::before {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(5,30,8,0.4) 0%, rgba(5,30,8,0.85) 100%);
  z-index: 1;
}
.hero-inner {
  max-width: 1200px; margin: 0 auto; padding: 80px 24px;
  position: relative; z-index: 2; width: 100%;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 16px; background: white; border-radius: 100px;
  font-size: 13px; color: #16a34a; font-weight: 600; margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(22,163,74,0.15);
}
.hero-badge ion-icon { font-size: 15px; }
.hero-text h1 {
  font-size: clamp(2.2rem,4vw,3.4rem); font-weight: 800;
  color: white; line-height: 1.15; margin-bottom: 20px;
}
.green { color: #86efac; }
.hero-text p { font-size: 16px; color: rgba(255,255,255,0.85); line-height: 1.75; margin-bottom: 32px; max-width: 460px; }
.hero-btns { display: flex; gap: 14px; flex-wrap: wrap; }

.btn-primary {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 13px 28px; background: #16a34a; color: white;
  border: none; border-radius: 10px; font-size: 15px; font-weight: 700;
  cursor: pointer; transition: all 0.2s; font-family: inherit;
}
.btn-primary:hover { background: #15803d; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(22,163,74,0.35); }
.btn-secondary {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 13px 28px; background: white; color: #16a34a;
  border: 2px solid #16a34a; border-radius: 10px; font-size: 15px;
  font-weight: 700; cursor: pointer; transition: all 0.2s; font-family: inherit;
}
.btn-secondary:hover { background: #f0fdf4; }
.btn-outline-dark {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 12px 28px; background: white; color: #1a2e1a;
  border: 2px solid #1a2e1a; border-radius: 10px; font-size: 15px;
  font-weight: 700; cursor: pointer; transition: all 0.2s; font-family: inherit;
}
.btn-outline-dark:hover { background: #1a2e1a; color: white; }
.btn-white {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 13px 28px; background: white; color: #15803d;
  border: none; border-radius: 10px; font-size: 15px; font-weight: 700;
  cursor: pointer; transition: all 0.2s; font-family: inherit;
}
.btn-white:hover { background: #f0fdf4; }
.btn-outline-white {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 13px 28px; background: transparent; color: white;
  border: 2px solid rgba(255,255,255,0.5); border-radius: 10px;
  font-size: 15px; font-weight: 700; cursor: pointer;
  transition: all 0.2s; font-family: inherit;
}
.btn-outline-white:hover { background: rgba(255,255,255,0.15); }

.stats-bar { background: #0a1e0c; padding: 0 24px; box-shadow: 0 4px 24px rgba(0,0,0,0.06); }
.stats-inner {
  max-width: 1000px; margin: 0 auto;
  display: grid; grid-template-columns: repeat(4,1fr);
  border-left: 1px solid rgba(255,255,255,0.1);
}
.stat {
  display: flex; align-items: center; gap: 14px;
  padding: 28px 24px; border-right: 1px solid rgba(255,255,255,0.1);
}
.stat-icon {
  width: 48px; height: 48px; background: rgba(22,163,74,0.2); border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; color: #86efac; flex-shrink: 0;
}
.stat strong { display: block; font-size: 1.5rem; font-weight: 800; color: #86efac; }
.stat span { font-size: 12px; color: rgba(255,255,255,0.6); }

.section { padding: 100px 0; background: white; }
.section.bg-mint { background: white; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.section-head { text-align: center; margin-bottom: 56px; }
.section-head h2 { font-size: clamp(1.8rem,3vw,2.4rem); font-weight: 800; color: #1a2e1a; margin-top: 8px; }
.tag-green {
  display: inline-block; padding: 5px 16px; background: #dcfce7; color: #15803d;
  border-radius: 100px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;
}

.sobre-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 72px; align-items: center; }
.sobre-images { position: relative; height: 480px; }
.si-top {
  position: absolute; top: 0; left: 0; width: 58%; height: 300px;
  object-fit: cover; border-radius: 16px; z-index: 2;
  box-shadow: 0 8px 32px rgba(0,0,0,0.12);
}
.si-bottom {
  position: absolute; bottom: 0; right: 0; width: 65%; height: 300px;
  object-fit: cover; border-radius: 16px; z-index: 3;
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
}
.si-badge {
  position: absolute; bottom: 24px; left: 24px; z-index: 4;
  background: #16a34a; color: white; border-radius: 12px; padding: 14px 20px;
  text-align: center; box-shadow: 0 4px 16px rgba(22,163,74,0.4);
}
.si-badge strong { display: block; font-size: 2rem; font-weight: 800; line-height: 1; }
.si-badge span { font-size: 12px; color: rgba(255,255,255,0.85); }

.sobre-text { display: flex; flex-direction: column; gap: 20px; }
.sobre-text h2 { font-size: 2rem; font-weight: 800; color: #1a2e1a; line-height: 1.3; }
.sobre-text p { font-size: 15px; color: #4a5e4a; line-height: 1.8; }
.sobre-stats { display: flex; gap: 32px; padding: 20px 0; border-top: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0; }
.ss-item { text-align: center; }
.ss-item strong { display: block; font-size: 1.8rem; font-weight: 800; color: #16a34a; }
.ss-item span { font-size: 12px; color: #64748b; }

.pilares-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 24px; }
.pilar-card {
  background: #f8fafc; border-radius: 16px; overflow: hidden;
  cursor: pointer; transition: all 0.25s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.pilar-card:hover { transform: translateY(-6px); box-shadow: 0 16px 40px rgba(22,163,74,0.15); }
.pilar-img { height: 180px; overflow: hidden; }
.pilar-img img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s; }
.pilar-card:hover .pilar-img img { transform: scale(1.06); }
.pilar-body { padding: 20px; }
.pilar-icon {
  width: 44px; height: 44px; background: #dcfce7; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; color: #16a34a; margin-bottom: 12px;
}
.pilar-body h3 { font-size: 15px; font-weight: 700; color: #1a2e1a; margin-bottom: 8px; }
.pilar-body p { font-size: 13px; color: #64748b; line-height: 1.6; margin-bottom: 12px; }
.pilar-link { display: inline-flex; align-items: center; gap: 4px; font-size: 13px; color: #16a34a; font-weight: 600; }

.galeria-strip { display: grid; grid-template-columns: repeat(3,1fr); height: 320px; }
.gs-item { position: relative; overflow: hidden; cursor: pointer; }
.gs-item img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s; }
.gs-item:hover img { transform: scale(1.06); }
.gs-label {
  position: absolute; bottom: 0; left: 0; right: 0;
  padding: 16px; background: linear-gradient(to top, rgba(0,0,0,0.65) 0%, transparent);
  color: white; font-size: 14px; font-weight: 600;
  opacity: 0; transition: opacity 0.3s;
}
.gs-item:hover .gs-label { opacity: 1; }

.noticias-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 24px; }
.noticia-card {
  background: #f8fafc; border-radius: 16px; overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06); cursor: pointer; transition: all 0.25s;
}
.noticia-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.1); }
.nc-img { position: relative; height: 200px; }
.nc-img img { width: 100%; height: 100%; object-fit: cover; }
.nc-tipo {
  position: absolute; top: 12px; left: 12px;
  padding: 4px 12px; background: #16a34a; color: white;
  border-radius: 100px; font-size: 11px; font-weight: 700;
}
.nc-body { padding: 20px; display: flex; flex-direction: column; gap: 8px; }
.nc-fecha { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #94a3b8; }
.nc-body h4 { font-size: 16px; font-weight: 700; color: #1a2e1a; line-height: 1.4; }
.nc-body p { font-size: 13px; color: #64748b; line-height: 1.6; }
.nc-link { display: inline-flex; align-items: center; gap: 4px; font-size: 13px; color: #16a34a; font-weight: 600; }

.ecoser-cta { position: relative; overflow: hidden; min-height: 420px; display: flex; align-items: center; }
.ecoser-cta-bg { position: absolute; inset: 0; }
.ecoser-cta-bg img { width: 100%; height: 100%; object-fit: cover; }
.ecoser-overlay { position: absolute; inset: 0; background: rgba(5,30,8,0.85); }
.ecoser-content {
  position: relative; z-index: 2; color: white;
  padding: 80px 0; display: flex; flex-direction: column; gap: 16px; max-width: 600px;
}
.tag-light {
  display: inline-block; padding: 5px 16px;
  background: rgba(134,239,172,0.15); color: #86efac;
  border-radius: 100px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;
}
.ecoser-content h2 { font-size: clamp(1.8rem,3vw,2.4rem); font-weight: 800; }
.ecoser-content p { font-size: 15px; color: rgba(255,255,255,0.75); line-height: 1.8; }
.ecoser-btns { display: flex; gap: 14px; flex-wrap: wrap; margin-top: 8px; }
.text-center { text-align: center; }
.mt-40 { margin-top: 40px; }

@media (max-width: 1024px) {
  .pilares-grid { grid-template-columns: repeat(2,1fr); }
  .stats-inner { grid-template-columns: repeat(2,1fr); }
  .stats-inner { border-left: none; }
}
@media (max-width: 768px) {
  .sobre-grid { grid-template-columns: 1fr; }
  .sobre-images { display: none; }
  .noticias-grid { grid-template-columns: 1fr; }
  .galeria-strip { grid-template-columns: 1fr; height: auto; }
  .gs-item { height: 220px; }
  .pilares-grid { grid-template-columns: 1fr; }
  .stats-inner { grid-template-columns: 1fr 1fr; }
}
</style>
