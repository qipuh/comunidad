<template>
  <LayoutPublico>
    <section class="page-hero" :style="{ backgroundImage: `url('https://images.unsplash.com/photo-1593460915132-fcb729cc4597?w=1800&q=80')` }">
      <div class="ph-overlay"></div>
      <div class="ph-content">
        <span class="ph-tag"><ion-icon name="map-outline"></ion-icon> Territorio</span>
        <h1>Nuestro Territorio</h1>
        <p>Valle de Tumilaca y zonas altoandinas del distrito de Torata</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="territorio-grid">
          <div class="ter-text">
            <span class="tag">Nuestra tierra</span>
            <h2>Un territorio vivo y productivo</h2>
            <p>La comunidad posee un amplio territorio ubicado en el valle de Tumilaca y zonas altoandinas del distrito de Torata, donde se desarrollan actividades agrícolas, ganaderas y de aprovechamiento de recursos naturales.</p>
            <p>El territorio comunal comprende diversos sectores y anexos, cada uno con características geográficas, productivas y culturales propias.</p>
            <div class="ter-datos">
              <div v-for="d in datos" :key="d.label" class="ter-dato">
                <ion-icon :name="d.icon"></ion-icon>
                <div>
                  <strong>{{ d.valor }}</strong>
                  <span>{{ d.label }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="ter-img-wrap">
            <img src="https://images.unsplash.com/photo-1570219870023-102f3a8b5b0e?w=800&q=80" alt="Territorio comunal" />
          </div>
        </div>
      </div>
    </section>

    <section class="section bg-light">
      <div class="container">
        <div class="section-head">
          <span class="tag">Los 4 anexos</span>
          <h2>Sectores del Territorio</h2>
        </div>
        <div class="anexos-cards">
          <div v-for="a in anexos" :key="a.nombre" class="anexo-card">
            <img :src="a.img" :alt="a.nombre" />
            <div class="ac-body">
              <h3>{{ a.nombre }}</h3>
              <p>{{ a.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="entorno-grid">
          <div class="entorno-text">
            <span class="tag">Contexto económico</span>
            <h2>Entorno Económico y Productivo</h2>
            <p>En el ámbito territorial del distrito de Torata y zonas de influencia de la comunidad, se desarrollan diversas actividades económicas, incluyendo aquellas vinculadas al sector minero, con presencia de proyectos de gran envergadura:</p>
            <div class="proyectos-mineros">
              <div class="pm-card" v-for="p in mineros" :key="p.nombre">
                <ion-icon name="diamond-outline"></ion-icon>
                <div>
                  <strong>{{ p.nombre }}</strong>
                  <span>{{ p.empresa }}</span>
                </div>
              </div>
            </div>
            <p>La comunidad mantiene espacios de diálogo y coordinación con los distintos actores presentes en el territorio, en el marco del respeto a sus derechos colectivos y la búsqueda de oportunidades para el desarrollo sostenible.</p>
          </div>
          <div class="entorno-img">
            <img src="https://images.unsplash.com/photo-1553550491-0895a24ffdac?w=800&q=80" alt="Entorno productivo" />
          </div>
        </div>
      </div>
    </section>
  </LayoutPublico>
</template>

<script setup>
import LayoutPublico from './LayoutPublico.vue'

const datos = [
  { icon: 'location-outline', valor: 'Torata', label: 'Distrito' },
  { icon: 'map-outline', valor: 'Mariscal Nieto', label: 'Provincia' },
  { icon: 'earth-outline', valor: 'Moquegua', label: 'Región' },
  { icon: 'layers-outline', valor: '4 anexos', label: 'Sectores territoriales' },
]

const anexos = [
  { nombre: 'Tumilaca', desc: 'Sector principal del territorio comunal, ubicado en el valle del mismo nombre con condiciones favorables para la agricultura.', img: 'https://images.unsplash.com/photo-1697729872733-24e9e8186a47?w=600&q=80' },
  { nombre: 'Pocata', desc: 'Sector comunal con actividades agropecuarias tradicionales y organización propia para la gestión territorial.', img: 'https://images.unsplash.com/photo-1589682449071-d13c27d1c298?w=600&q=80' },
  { nombre: 'Coscore', desc: 'Zona altoandina con potencial ganadero y actividades de aprovechamiento de recursos naturales propios de la sierra.', img: 'https://images.unsplash.com/photo-1536705284215-000a0c2f0406?w=600&q=80' },
  { nombre: 'Tala', desc: 'Anexo comunal con tradición agrícola y vínculos culturales profundos con la tierra y sus recursos naturales.', img: 'https://images.unsplash.com/photo-1566793772361-1d5d9cefbd12?w=600&q=80' },
]

const mineros = [
  { nombre: 'Proyecto Quellaveco', empresa: 'Anglo American' },
  { nombre: 'Proyecto Cuajone', empresa: 'Southern Perú' },
]
</script>

<style scoped>
.page-hero { min-height: 55vh; background-size: cover; background-position: center; display: flex; align-items: center; position: relative; }
.ph-overlay { position: absolute; inset: 0; background: rgba(5,20,8,0.75); }
.ph-content { position: relative; z-index: 2; max-width: 1200px; margin: 0 auto; padding: 120px 24px 80px; color: white; }
.ph-tag { display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; background: rgba(134,239,172,0.15); color: #86efac; border-radius: 100px; font-size: 13px; font-weight: 600; margin-bottom: 16px; }
.ph-content h1 { font-size: clamp(2rem,4vw,3rem); font-weight: 800; margin-bottom: 10px; }
.ph-content p { font-size: 16px; color: rgba(255,255,255,0.7); }

.section { padding: 96px 0; }
.section.bg-light { background: #f8fafc; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.section-head { text-align: center; margin-bottom: 56px; }
.section-head h2 { font-size: 2rem; font-weight: 800; color: #1a2e1a; }
.tag { display: inline-block; padding: 4px 14px; background: #dcfce7; color: #15803d; border-radius: 100px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }

.territorio-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center; }
.ter-text { display: flex; flex-direction: column; gap: 16px; }
.ter-text h2 { font-size: 2rem; font-weight: 800; color: #1a2e1a; }
.ter-text p { font-size: 15px; color: #4a5e4a; line-height: 1.8; }
.ter-datos { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 8px; }
.ter-dato { display: flex; align-items: center; gap: 12px; background: #dcfce7; border-radius: 10px; padding: 14px; }
.ter-dato ion-icon { font-size: 24px; color: #16a34a; flex-shrink: 0; }
.ter-dato strong { display: block; font-size: 15px; font-weight: 700; color: #1a2e1a; }
.ter-dato span { font-size: 12px; color: #4a5e4a; }
.ter-img-wrap img { width: 100%; height: 480px; object-fit: cover; border-radius: 20px; }

.anexos-cards { display: grid; grid-template-columns: repeat(2,1fr); gap: 24px; }
.anexo-card { background: #f8fafc; border-radius: 16px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.anexo-card img { width: 100%; height: 200px; object-fit: cover; }
.ac-body { padding: 24px; }
.ac-body h3 { font-size: 18px; font-weight: 700; color: #1a2e1a; margin-bottom: 8px; }
.ac-body p { font-size: 14px; color: #4a5e4a; line-height: 1.7; }

.entorno-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center; }
.entorno-text { display: flex; flex-direction: column; gap: 16px; }
.entorno-text h2 { font-size: 2rem; font-weight: 800; color: #1a2e1a; }
.entorno-text p { font-size: 15px; color: #4a5e4a; line-height: 1.8; }
.proyectos-mineros { display: flex; flex-direction: column; gap: 12px; }
.pm-card { display: flex; align-items: center; gap: 14px; padding: 16px 20px; background: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0; }
.pm-card ion-icon { font-size: 28px; color: #4f46e5; flex-shrink: 0; }
.pm-card strong { display: block; font-size: 15px; color: #1e293b; }
.pm-card span { font-size: 13px; color: #64748b; }
.entorno-img img { width: 100%; height: 400px; object-fit: cover; border-radius: 20px; }

@media (max-width: 768px) {
  .territorio-grid, .entorno-grid { grid-template-columns: 1fr; }
  .anexos-cards { grid-template-columns: 1fr; }
  .ter-datos { grid-template-columns: 1fr 1fr; }
}
</style>
