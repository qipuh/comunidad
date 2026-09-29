<template>
  <LayoutPublico>
    <section class="page-hero" :style="{ backgroundImage: `url('/uploads/img/variadas/cueva.png')` }">
      <div class="ph-overlay"></div>
      <div class="ph-content">
        <span class="ph-tag"><ion-icon name="newspaper-outline"></ion-icon> Noticias</span>
        <h1>Noticias y Comunicados</h1>
        <p>Mantente informado sobre las actividades y decisiones de la comunidad</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="filtros">
          <button v-for="f in filtros" :key="f.key" :class="['filtro-btn', { active: filtroActivo === f.key }]" @click="filtroActivo = f.key">
            <ion-icon :name="f.icon"></ion-icon> {{ f.label }}
          </button>
        </div>

        <div class="noticias-grid">
          <article
            v-for="n in noticiasFiltradas" :key="n.id"
            class="noticia-card" :class="n.destacada ? 'destacada' : ''"
            :style="n.detalle ? 'cursor:pointer' : ''"
            @click="n.detalle && navegar(n.detalle)"
          >
            <div class="nc-img">
              <img :src="n.img" :alt="n.titulo" />
              <span class="nc-cat" :class="n.tipo">{{ n.tipoLabel }}</span>
            </div>
            <div class="nc-body">
              <h3>{{ n.titulo }}</h3>
              <p>{{ n.resumen }}</p>
              <button v-if="n.detalle" class="nc-link" @click.stop="navegar(n.detalle)">
                Leer más <ion-icon name="arrow-forward-outline"></ion-icon>
              </button>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="section bg-light">
      <div class="container">
        <div class="comunicados-box">
          <div class="com-header">
            <ion-icon name="document-text-outline"></ion-icon>
            <div>
              <h2>Comunicados Oficiales</h2>
              <p>Documentos y resoluciones de la Junta Directiva</p>
            </div>
          </div>
          <div class="comunicados-lista">
            <div v-for="c in comunicados" :key="c.titulo" class="comunicado-item">
              <ion-icon name="document-outline"></ion-icon>
              <div class="ci-info">
                <strong>{{ c.titulo }}</strong>
                <span>{{ c.fecha }}</span>
              </div>
              <button class="ci-btn"><ion-icon name="download-outline"></ion-icon></button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section bg-dark">
      <div class="container">
        <div class="suscripcion-box">
          <ion-icon name="notifications-outline"></ion-icon>
          <h2>Mantente Informado</h2>
          <p>Las noticias y comunicados oficiales se publican a través de los canales de la comunidad. Participa en las asambleas para estar al tanto de las últimas decisiones.</p>
          <button class="btn-green" @click="navegar('contacto')">
            <ion-icon name="mail-outline"></ion-icon> Contactar a la directiva
          </button>
        </div>
      </div>
    </section>
  </LayoutPublico>
</template>

<script setup>
import { ref, computed } from 'vue'
import LayoutPublico from './LayoutPublico.vue'
import { useWebNav } from '../../composables/useWebNav'
const { navegar } = useWebNav()

const filtroActivo = ref('todos')

const filtros = [
  { key: 'todos',        label: 'Todos',         icon: 'grid-outline' },
  { key: 'asamblea',    label: 'Asambleas',      icon: 'people-outline' },
  { key: 'convocatoria', label: 'Convocatorias', icon: 'megaphone-outline' },
]

const noticias = [
  {
    id: 1, tipo: 'asamblea', tipoLabel: 'Asamblea', destacada: true,
    titulo: 'Acuerdos de la Asamblea General Ordinaria',
    resumen: 'El día 24 de mayo de 2026, la Comunidad Campesina Tumilaca, Pocata, Coscore y Tala celebró su Asamblea General',
    img: '/uploads/img/asamblea/1.jpeg',
    detalle: 'asamblea-mayo-2026',
  },
  {
    id: 2, tipo: 'convocatoria', tipoLabel: 'Convocatoria',
    titulo: 'Convocatoria a Asamblea Extraordinaria',
    resumen: 'La Junta Directiva convoca a todos los Usuarios a una asamblea extraordinaria para tratar temas de interés colectivo relacionados con el territorio comunal.',
    img: '/uploads/img/asamblea/convocatorias/a.jpeg',
    detalle: 'convocatoria-extraordinaria',
  },
]

const noticiasFiltradas = computed(() =>
  filtroActivo.value === 'todos' ? noticias : noticias.filter(n => n.tipo === filtroActivo.value)
)

const comunicados = [
  { titulo: 'Acta de Asamblea General Ordinaria – Mayo 2026', fecha: '24/05/2026' },
  { titulo: 'Convocatoria a Asamblea Extraordinaria', fecha: '05/01/2026' },
]

const presidentes = [
  { periodo: '1991–1992', nombre: 'Ramón Jesús Marca' },
  { periodo: '1993–1994', nombre: 'Guillermo Mamani Mamani' },
  { periodo: '1995–2002', nombre: 'Mercedes Marca Fernández' },
  { periodo: '2003–2004', nombre: 'Juvencio Ricardo Flores Flores' },
  { periodo: '2007–2008', nombre: 'Asencio Cornelio Centeno Coaila' },
  { periodo: '2009–2010', nombre: 'Eugenio Coayla Arias' },
  { periodo: '2011–2014', nombre: 'Germán Fidel Coaila García' },
  { periodo: '2015–2016', nombre: 'Irenio Eladio Peñaloza Gutiérrez' },
  { periodo: '2017–2018', nombre: 'Juvencio Ricardo Flores Flores' },
  { periodo: '2019–2020', nombre: 'Rubén Benedicto Centeno Soto' },
  { periodo: '2021–2022', nombre: 'Dionilde Flora Flores Calizaya' },
  { periodo: '2023–2024', nombre: 'Ivan Bruno Mendoza Venancio' },
  { periodo: '2025–2026', nombre: 'Marcos García Nina' },
]
</script>

<style scoped>
.page-hero { min-height: 55vh; background-size: cover; background-position: center; display: flex; align-items: center; position: relative; }
.ph-overlay { position: absolute; inset: 0; background: rgba(5,20,8,0.75); }
.ph-content { position: relative; z-index: 2; max-width: 1200px; margin: 0 auto; padding: 120px 24px 80px; color: white; }
.ph-tag { display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; background: rgba(134,239,172,0.15); color: #86efac; border-radius: 100px; font-size: 13px; font-weight: 600; margin-bottom: 16px; }
.ph-content h1 { font-size: clamp(2rem,4vw,3rem); font-weight: 800; margin-bottom: 10px; }
.ph-content p { font-size: 16px; color: rgba(255,255,255,0.7); }

.section { padding: 96px 0; background: white; }
.section.bg-light { background: #0a1e0c; }
.section.bg-dark { background: linear-gradient(160deg,#0a1e0c,#0f2814); }
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }

.filtros { display: flex; gap: 12px; margin-bottom: 48px; flex-wrap: wrap; }
.filtro-btn { display: inline-flex; align-items: center; gap: 8px; padding: 8px 20px; border: 1px solid #e2e8f0; background: white; border-radius: 100px; font-size: 14px; font-weight: 600; color: #64748b; cursor: pointer; transition: all 0.2s; }
.filtro-btn:hover { border-color: #16a34a; color: #16a34a; }
.filtro-btn.active { background: #16a34a; color: white; border-color: #16a34a; }

.noticias-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 28px; }
.noticia-card { background: white; border-radius: 16px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: all 0.25s; }
.noticia-card:hover { transform: translateY(-4px); box-shadow: 0 16px 40px rgba(0,0,0,0.1); }
.noticia-card.destacada { grid-column: span 3; display: grid; grid-template-columns: 420px 1fr; }
.nc-img { position: relative; }
.nc-img img { width: 100%; height: 220px; object-fit: cover; display: block; }
.noticia-card.destacada .nc-img img { height: 100%; min-height: 280px; }
.nc-cat { position: absolute; top: 14px; left: 14px; padding: 4px 12px; border-radius: 100px; font-size: 11px; font-weight: 700; text-transform: uppercase; }
.nc-cat.asamblea { background: #dbeafe; color: #1d4ed8; }
.nc-cat.convocatoria { background: #fef3c7; color: #92400e; }
.nc-cat.proyecto { background: #dcfce7; color: #15803d; }
.nc-cat.ecoser { background: #fef3c7; color: #92400e; }
.nc-body { padding: 24px; display: flex; flex-direction: column; gap: 12px; }
.nc-meta { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #94a3b8; }
.nc-meta ion-icon { font-size: 14px; }
.nc-body h3 { font-size: 17px; font-weight: 700; color: #1e293b; line-height: 1.4; }
.noticia-card.destacada .nc-body h3 { font-size: 22px; }
.nc-body p { font-size: 14px; color: #64748b; line-height: 1.7; flex: 1; }
.nc-link { display: inline-flex; align-items: center; gap: 6px; color: #16a34a; font-size: 14px; font-weight: 600; background: none; border: none; cursor: pointer; padding: 0; }

.comunicados-box { background: #0f2814; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); overflow: hidden; }
.com-header { display: flex; align-items: center; gap: 20px; padding: 28px 32px; border-bottom: 1px solid rgba(255,255,255,0.1); background: transparent; }
.com-header ion-icon { font-size: 40px; color: #86efac; flex-shrink: 0; }
.com-header h2 { font-size: 1.4rem; font-weight: 800; color: white; margin-bottom: 4px; }
.com-header p { font-size: 14px; color: rgba(255,255,255,0.6); }
.comunicados-lista { padding: 8px 0; }
.comunicado-item { display: flex; align-items: center; gap: 16px; padding: 16px 32px; border-bottom: 1px solid rgba(255,255,255,0.08); transition: background 0.2s; }
.comunicado-item:last-child { border-bottom: none; }
.comunicado-item:hover { background: rgba(255,255,255,0.05); }
.comunicado-item > ion-icon { font-size: 24px; color: #86efac; flex-shrink: 0; }
.ci-info { flex: 1; }
.ci-info strong { display: block; font-size: 15px; color: white; margin-bottom: 2px; }
.ci-info span { font-size: 12px; color: rgba(255,255,255,0.6); }
.ci-btn { width: 36px; height: 36px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); background: transparent; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; color: #86efac; font-size: 18px; flex-shrink: 0; }
.ci-btn:hover { background: #16a34a; color: white; border-color: #16a34a; }

.suscripcion-box { text-align: center; color: white; max-width: 700px; margin: 0 auto; display: flex; flex-direction: column; align-items: center; gap: 20px; }
.suscripcion-box ion-icon { font-size: 64px; color: #86efac; }
.suscripcion-box h2 { font-size: 2rem; font-weight: 800; }
.suscripcion-box p { font-size: 16px; color: rgba(255,255,255,0.75); line-height: 1.8; }
.btn-green { display: inline-flex; align-items: center; gap: 8px; padding: 12px 28px; background: #16a34a; color: white; border: none; border-radius: 10px; font-size: 15px; font-weight: 700; text-decoration: none; cursor: pointer; font-family: inherit; transition: all 0.2s; }
.btn-green:hover { background: #15803d; }

@media (max-width: 1024px) { .noticias-grid { grid-template-columns: repeat(2,1fr); } .noticia-card.destacada { grid-column: span 2; } }
@media (max-width: 768px) { .noticias-grid { grid-template-columns: 1fr; } .noticia-card.destacada { grid-column: span 1; grid-template-columns: 1fr; } }

/* BANDERA */
.section-head { text-align: center; margin-bottom: 48px; }
.section-head h2 { font-size: 2rem; font-weight: 800; color: #1a2e1a; }
.tag-green { display: inline-block; padding: 4px 14px; background: #dcfce7; color: #15803d; border-radius: 100px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }

.bandera-grid { display: grid; grid-template-columns: 300px 1fr; gap: 48px; align-items: start; margin-bottom: 48px; }
.bandera-svg { width: 200px; border: 2px solid #ddd; border-radius: 4px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.15); }
.franja { width: 100%; height: 90px; display: flex; align-items: center; justify-content: center; }
.franja.amarilla { background: #FFD700; }
.franja.roja { background: #CC0000; }
.silueta { font-size: 48px; color: #1a1a1a; }
.bandera-dim { font-size: 12px; color: #64748b; margin-top: 10px; text-align: center; }

.bandera-colores { display: flex; flex-direction: column; gap: 20px; }
.color-item { display: flex; align-items: flex-start; gap: 16px; }
.color-dot { width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0; margin-top: 2px; }
.color-dot.rojo { background: #CC0000; }
.color-dot.amarillo { background: #FFD700; border: 1px solid #ddd; }
.color-dot.negro { background: #1a1a1a; }
.color-item strong { display: block; font-size: 15px; color: #1a2e1a; margin-bottom: 4px; }
.color-item p { font-size: 14px; color: #475569; line-height: 1.6; margin: 0; }

.historia-bandera { background: #f0fdf4; border-left: 4px solid #1aa86a; border-radius: 0 12px 12px 0; padding: 24px 28px; display: flex; flex-direction: column; gap: 12px; }
.historia-bandera h3 { display: flex; align-items: center; gap: 8px; font-size: 18px; font-weight: 700; color: #1a2e1a; margin-bottom: 4px; }
.historia-bandera h3 ion-icon { color: #1aa86a; font-size: 20px; }
.historia-bandera p { font-size: 15px; color: #374151; line-height: 1.8; margin: 0; }

/* RESEÑA */
.resena-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; }
.resena-texto { display: flex; flex-direction: column; gap: 16px; }
.resena-texto p { font-size: 15px; color: #374151; line-height: 1.8; }
.resena-presidentes h3 { display: flex; align-items: center; gap: 8px; font-size: 18px; font-weight: 700; color: #1a2e1a; margin-bottom: 20px; }
.resena-presidentes h3 ion-icon { color: #1aa86a; }
.presidentes-lista { display: flex; flex-direction: column; gap: 8px; }
.presidente-item { display: flex; align-items: center; gap: 12px; padding: 10px 14px; background: white; border-radius: 8px; border: 1px solid #e2e8f0; }
.p-periodo { font-size: 12px; font-weight: 700; color: #1aa86a; white-space: nowrap; min-width: 80px; }
.p-nombre { font-size: 14px; color: #1e293b; font-weight: 500; }

@media (max-width: 768px) {
  .bandera-grid, .resena-grid { grid-template-columns: 1fr; }
  .bandera-svg { margin: 0 auto; }
}
</style>
