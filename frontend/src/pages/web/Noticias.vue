<template>
  <LayoutPublico>
    <section class="page-hero" :style="{ backgroundImage: `url('https://images.unsplash.com/photo-1697729872733-24e9e8186a47?w=1800&q=80')` }">
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
          <article v-for="n in noticiasFiltradas" :key="n.id" class="noticia-card" :class="n.destacada ? 'destacada' : ''">
            <div class="nc-img">
              <img :src="n.img" :alt="n.titulo" />
              <span class="nc-cat" :class="n.tipo">{{ n.tipoLabel }}</span>
            </div>
            <div class="nc-body">
              <div class="nc-meta">
                <span><ion-icon name="calendar-outline"></ion-icon> {{ n.fecha }}</span>
              </div>
              <h3>{{ n.titulo }}</h3>
              <p>{{ n.resumen }}</p>
              <button class="nc-link">Leer más <ion-icon name="arrow-forward-outline"></ion-icon></button>
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
  { key: 'todos', label: 'Todos', icon: 'grid-outline' },
  { key: 'asamblea', label: 'Asambleas', icon: 'people-outline' },
  { key: 'proyecto', label: 'Proyectos', icon: 'construct-outline' },
  { key: 'ecoser', label: 'ECOSER', icon: 'briefcase-outline' },
]

const noticias = [
  {
    id: 1, tipo: 'asamblea', tipoLabel: 'Asamblea', destacada: true,
    titulo: 'Asamblea General Ordinaria – Marzo 2026',
    resumen: 'Se realizó la asamblea ordinaria con la participación de más de 120 Usuarios. Se aprobaron los estados financieros del ejercicio 2025 y el plan de trabajo para el presente año.',
    fecha: '15 de marzo, 2026',
    img: 'https://images.unsplash.com/photo-1519074598089-6436475c7f8f?w=700&q=80',
  },
  {
    id: 2, tipo: 'proyecto', tipoLabel: 'Proyecto',
    titulo: 'Avance del proyecto de mejora de canales de irrigación',
    resumen: 'La comunidad informa sobre el avance del 60% en la rehabilitación de los canales de irrigación del sector Tumilaca, beneficiando a más de 80 familias.',
    fecha: '28 de febrero, 2026',
    img: 'https://images.unsplash.com/photo-1553550491-0895a24ffdac?w=700&q=80',
  },
  {
    id: 3, tipo: 'ecoser', tipoLabel: 'ECOSER',
    titulo: 'ECOSER firma convenio de servicios con empresa minera',
    resumen: 'La empresa comunal ECOSER ha suscrito un nuevo contrato de prestación de servicios logísticos y provisión de personal, generando 25 puestos de trabajo para Usuarios.',
    fecha: '10 de febrero, 2026',
    img: 'https://images.unsplash.com/photo-1550290129-41b39a6fdfe8?w=700&q=80',
  },
  {
    id: 4, tipo: 'asamblea', tipoLabel: 'Asamblea',
    titulo: 'Convocatoria a Asamblea Extraordinaria',
    resumen: 'La Junta Directiva convoca a todos los Usuarios a una asamblea extraordinaria para tratar temas de interés colectivo relacionados con el territorio comunal.',
    fecha: '5 de enero, 2026',
    img: 'https://images.unsplash.com/photo-1589682449071-d13c27d1c298?w=700&q=80',
  },
  {
    id: 5, tipo: 'proyecto', tipoLabel: 'Proyecto',
    titulo: 'Inauguración de nuevo módulo de crianza de cuyes',
    resumen: 'Con el apoyo de la Junta Directiva, se inauguró un módulo comunal de crianza de cuyes en el anexo Pocata, como parte del programa de seguridad alimentaria.',
    fecha: '20 de diciembre, 2025',
    img: 'https://images.unsplash.com/photo-1730424508745-29ea708ae698?w=700&q=80',
  },
  {
    id: 6, tipo: 'ecoser', tipoLabel: 'ECOSER',
    titulo: 'Flota de ECOSER incorpora dos nuevas camionetas',
    resumen: 'ECOSER amplía su capacidad operativa con la adquisición de dos unidades 4x4, fortaleciendo el servicio de transporte en zonas de difícil acceso del distrito de Torata.',
    fecha: '1 de diciembre, 2025',
    img: 'https://images.unsplash.com/photo-1566793772361-1d5d9cefbd12?w=700&q=80',
  },
]

const noticiasFiltradas = computed(() =>
  filtroActivo.value === 'todos' ? noticias : noticias.filter(n => n.tipo === filtroActivo.value)
)

const comunicados = [
  { titulo: 'Acta de Asamblea General Ordinaria – Marzo 2026', fecha: '15/03/2026' },
  { titulo: 'Resolución N° 001-2026-JD: Aprobación Plan de Trabajo', fecha: '20/01/2026' },
  { titulo: 'Comunicado sobre acuerdos con empresa minera', fecha: '15/01/2026' },
  { titulo: 'Acta de Asamblea Extraordinaria – Diciembre 2025', fecha: '10/12/2025' },
  { titulo: 'Memoria Anual de la Comunidad 2025', fecha: '05/01/2026' },
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
</style>
