<template>
  <LayoutPublico>
    <section class="page-hero" :style="{ backgroundImage: `url('https://images.unsplash.com/photo-1553550491-0895a24ffdac?w=1800&q=80')` }">
      <div class="ph-overlay"></div>
      <div class="ph-content">
        <span class="ph-tag"><ion-icon name="leaf-outline"></ion-icon> Producción</span>
        <h1>Desarrollo Productivo</h1>
        <p>La base del sustento económico de las familias comuneras</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="intro-prod">
          <p>Las principales actividades económicas de la comunidad incluyen producción agrícola y pecuaria, que constituyen la base del sustento de las familias comuneras y fortalecen la economía local.</p>
        </div>

        <div class="prod-section">
          <div class="prod-header">
            <ion-icon name="nutrition-outline"></ion-icon>
            <div>
              <h2>Producción Agrícola</h2>
              <p>Cultivos tradicionales del valle de Tumilaca</p>
            </div>
          </div>
          <div class="prod-grid">
            <div v-for="p in agricola" :key="p.nombre" class="prod-card">
              <img :src="p.img" :alt="p.nombre" />
              <div class="pc-body">
                <h3>{{ p.nombre }}</h3>
                <p>{{ p.desc }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="prod-section">
          <div class="prod-header">
            <ion-icon name="paw-outline"></ion-icon>
            <div>
              <h2>Producción Pecuaria</h2>
              <p>Crianza de animales en zonas altoandinas</p>
            </div>
          </div>
          <div class="prod-grid tres">
            <div v-for="p in pecuaria" :key="p.nombre" class="prod-card">
              <img :src="p.img" :alt="p.nombre" />
              <div class="pc-body">
                <h3>{{ p.nombre }}</h3>
                <p>{{ p.desc }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section bg-dark">
      <div class="container">
        <div class="sostenible-box">
          <ion-icon name="earth-outline"></ion-icon>
          <h2>Agricultura Sostenible</h2>
          <p>La comunidad combina técnicas de cultivo ancestrales con prácticas modernas, priorizando el cuidado del medio ambiente y la preservación de los recursos naturales para las generaciones futuras.</p>
        </div>
      </div>
    </section>
  </LayoutPublico>
</template>

<script setup>
import LayoutPublico from './LayoutPublico.vue'

const agricola = [
  { nombre: 'Fresas', desc: 'Cultivo emblemático del valle de Tumilaca, producción de alta calidad para mercados locales y regionales.', img: 'https://images.unsplash.com/photo-1730424508745-29ea708ae698?w=600&q=80' },
  { nombre: 'Damasco', desc: 'Fruta de hueso tradicional de los valles moqueguanos, de sabor intenso y dulce característico.', img: 'https://images.unsplash.com/photo-1536705284215-000a0c2f0406?w=600&q=80' },
  { nombre: 'Palta', desc: 'Aguacate andino de alta demanda, cultivado en las laderas del valle de Tumilaca con técnicas tradicionales.', img: 'https://images.unsplash.com/photo-1566793772361-1d5d9cefbd12?w=600&q=80' },
  { nombre: 'Manzana', desc: 'Manzana serrana de variedades locales, cultivada en altitudes que garantizan su calidad y sabor.', img: 'https://images.unsplash.com/photo-1570219870023-102f3a8b5b0e?w=600&q=80' },
  { nombre: 'Hortalizas', desc: 'Producción diversificada de hortalizas para consumo local y abastecimiento de mercados cercanos.', img: 'https://images.unsplash.com/photo-1589682449071-d13c27d1c298?w=600&q=80' },
]

const pecuaria = [
  { nombre: 'Caprinos', desc: 'Crianza de cabras adaptadas al entorno andino, aprovechando los pastizales naturales del territorio.', img: 'https://images.unsplash.com/photo-1697729872733-24e9e8186a47?w=600&q=80' },
  { nombre: 'Producción de Leche', desc: 'Obtención de leche fresca de alta calidad para consumo familiar y elaboración de derivados lácteos.', img: 'https://images.unsplash.com/photo-1593460915132-fcb729cc4597?w=600&q=80' },
  { nombre: 'Crianza de Cuyes', desc: 'Actividad pecuaria ancestral andina, fuente importante de proteínas y de ingresos económicos para las familias.', img: 'https://images.unsplash.com/photo-1568805778734-f0a5a77d7272?w=600&q=80' },
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
.section.bg-dark { background: linear-gradient(160deg,#0a1e0c,#0f2814); }
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }

.intro-prod { max-width: 800px; margin: 0 auto 72px; text-align: center; font-size: 16px; color: #4a5e4a; line-height: 1.8; }

.prod-section { margin-bottom: 72px; }
.prod-header { display: flex; align-items: center; gap: 20px; margin-bottom: 36px; padding-bottom: 20px; border-bottom: 2px solid #e2e8f0; }
.prod-header ion-icon { font-size: 48px; color: #16a34a; flex-shrink: 0; }
.prod-header h2 { font-size: 1.8rem; font-weight: 800; color: #1a2e1a; margin-bottom: 4px; }
.prod-header p { font-size: 14px; color: #4a5e4a; }

.prod-grid { display: grid; grid-template-columns: repeat(5,1fr); gap: 20px; }
.prod-grid.tres { grid-template-columns: repeat(3,1fr); }
.prod-card { background: #f8fafc; border-radius: 14px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: all 0.25s; }
.prod-card:hover { transform: translateY(-4px); box-shadow: 0 12px 28px rgba(0,0,0,0.1); }
.prod-card img { width: 100%; height: 160px; object-fit: cover; }
.pc-body { padding: 16px; }
.pc-body h3 { font-size: 15px; font-weight: 700; color: #1a2e1a; margin-bottom: 6px; }
.pc-body p { font-size: 12px; color: #4a5e4a; line-height: 1.6; }

.sostenible-box { text-align: center; color: white; max-width: 700px; margin: 0 auto; display: flex; flex-direction: column; align-items: center; gap: 20px; }
.sostenible-box ion-icon { font-size: 64px; color: #86efac; }
.sostenible-box h2 { font-size: 2rem; font-weight: 800; }
.sostenible-box p { font-size: 16px; color: rgba(255,255,255,0.75); line-height: 1.8; }

@media (max-width: 1024px) { .prod-grid { grid-template-columns: repeat(3,1fr); } }
@media (max-width: 768px) { .prod-grid, .prod-grid.tres { grid-template-columns: repeat(2,1fr); } }
@media (max-width: 480px) { .prod-grid, .prod-grid.tres { grid-template-columns: 1fr; } }
</style>
