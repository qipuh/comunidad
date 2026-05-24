<template>
  <LayoutPublico>
    <section class="page-hero" :style="{ backgroundImage: `url('/uploads/img/nosotros/comunidad.jpeg')` }">
      <div class="ph-overlay"></div>
      <div class="ph-content">
        <span class="ph-tag"><ion-icon name="people-outline"></ion-icon> Nosotros</span>
        <h1>Historia, Misión y Valores</h1>
        <p>Conoce la identidad de nuestra comunidad ancestral</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="historia-grid">
          <div class="historia-text">
            <span class="tag">Nuestros orígenes</span>
            <h2>Historia</h2>
            <p>La Comunidad Campesina de Tumilaca, Pocata, Coscore y Tala tiene sus raíces en antiguas formas de organización colectiva que han permitido a las familias del valle de Tumilaca conservar sus tierras, su cultura y sus formas de producción tradicional.</p>
            <p>Sus orígenes formales se remontan al año <strong>1949</strong>, consolidándose como una organización representativa de carácter territorial, social y cultural. En el año 2026, la comunidad celebró su <strong>77° aniversario</strong>.</p>
            <p>A lo largo del tiempo, la comunidad ha fortalecido su organización mediante asambleas generales, juntas directivas y mecanismos participativos, consolidando un modelo de gestión basado en la solidaridad, el respeto y la cooperación.</p>
            <p>Está conformada por los anexos de <strong>Tumilaca, Pocata, Coscore y Tala</strong>, territorios que mantienen una profunda relación con la tierra y una identidad cultural sólida.</p>
          </div>
          <div class="historia-imgs">
            <div class="hi-collage">
              <img :src="'/uploads/img/nosotros/tumilala.png'" alt="Anexo Tumilaca" class="hi-img-1" />
              <img :src="'/uploads/img/nosotros/tumilala2.png'" alt="Anexo Tumilaca - vista 2" class="hi-img-2" />
            </div>
            <div class="hi-stats">
              <div class="hi-stat" v-for="s in hitos" :key="s.label">
                <strong>{{ s.value }}</strong>
                <span>{{ s.label }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section bg-light">
      <div class="container">
        <div class="mv-grid">
          <div class="mv-card">
            <div class="mv-icon"><ion-icon name="flag-outline"></ion-icon></div>
            <h3>Misión</h3>
            <p>Promover el desarrollo integral de la comunidad mediante la gestión responsable de sus recursos naturales, el fortalecimiento de la organización comunal y la promoción de actividades agroproductivas sostenibles.</p>
          </div>
          <div class="mv-card">
            <div class="mv-icon"><ion-icon name="eye-outline"></ion-icon></div>
            <h3>Visión</h3>
            <p>Ser una comunidad organizada, fortalecida y reconocida a nivel regional por su capacidad de gestión territorial, desarrollo productivo sostenible y preservación de sus valores culturales.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head">
          <span class="tag">Lo que nos define</span>
          <h2>Nuestros Valores</h2>
        </div>
        <div class="valores-grid">
          <div v-for="v in valores" :key="v.nombre" class="valor-card">
            <ion-icon :name="v.icon"></ion-icon>
            <h4>{{ v.nombre }}</h4>
            <p>{{ v.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section bg-dark">
      <div class="container">
        <div class="compromiso-box">
          <ion-icon name="shield-checkmark-outline"></ion-icon>
          <h2>Nuestro Compromiso</h2>
          <p>La comunidad reafirma su compromiso con la defensa de su territorio, el fortalecimiento de su organización comunal y la construcción de un desarrollo sostenible basado en sus propios valores y capacidades.</p>
          <button class="btn-green" @click="navegar('contacto')">Contáctanos <ion-icon name="arrow-forward-outline"></ion-icon></button>
        </div>
      </div>
    </section>
  </LayoutPublico>
</template>

<script setup>
import LayoutPublico from './LayoutPublico.vue'
import { useWebNav } from '../../composables/useWebNav'
const { navegar } = useWebNav()

const hitos = [
  { value: '1949', label: 'Año de fundación' },
  { value: '77', label: 'Años de historia' },
  { value: '4', label: 'Anexos territoriales' },
]

const valores = [
  { icon: 'eye-outline', nombre: 'Transparencia', desc: 'Gestión abierta y honesta con nuestros Usuarios.' },
  { icon: 'heart-outline', nombre: 'Solidaridad', desc: 'Apoyo mutuo como base de nuestra organización.' },
  { icon: 'thumbs-up-outline', nombre: 'Respeto', desc: 'Reconocemos la dignidad de cada Usuario y familia.' },
  { icon: 'people-outline', nombre: 'Trabajo colectivo', desc: 'La fuerza de la comunidad está en la unión.' },
  { icon: 'ribbon-outline', nombre: 'Identidad cultural', desc: 'Preservamos nuestras tradiciones y saberes ancestrales.' },
  { icon: 'shield-outline', nombre: 'Defensa del territorio', desc: 'Protegemos nuestras tierras para las futuras generaciones.' },
]
</script>

<style scoped>
.page-hero {
  min-height: 55vh; background-size: cover; background-position: center;
  display: flex; align-items: center; position: relative;
}
.ph-overlay { position: absolute; inset: 0; background: rgba(5,20,8,0.78); }
.ph-content {
  position: relative; z-index: 2; max-width: 1200px; margin: 0 auto; padding: 120px 24px 80px;
  color: white;
}
.ph-tag {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 16px; background: rgba(134,239,172,0.15); color: #86efac;
  border-radius: 100px; font-size: 13px; font-weight: 600; margin-bottom: 16px;
}
.ph-content h1 { font-size: clamp(2rem,4vw,3rem); font-weight: 800; margin-bottom: 10px; }
.ph-content p { font-size: 16px; color: rgba(255,255,255,0.7); }

.section { padding: 96px 0; background: white; }
.section.bg-light { background: white; }
.section.bg-dark { background: linear-gradient(160deg,#0a1e0c,#0f2814); }
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.section-head { text-align: center; margin-bottom: 56px; }
.section-head h2 { font-size: 2.2rem; font-weight: 800; color: #1a2e1a; }
.tag {
  display: inline-block; padding: 4px 14px; background: #dcfce7; color: #15803d;
  border-radius: 100px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;
}

.historia-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: start; }
.historia-text { display: flex; flex-direction: column; gap: 16px; }
.historia-text h2 { font-size: 2rem; font-weight: 800; color: #1a2e1a; }
.historia-text p { font-size: 15px; color: #4a5e4a; line-height: 1.8; }
.hi-collage {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  grid-template-rows: 180px 180px;
  gap: 12px;
  margin-bottom: 16px;
}
.hi-img-1 {
  grid-row: 1 / span 2;
  width: 100%; height: 100%;
  object-fit: cover; border-radius: 20px;
  box-shadow: 0 8px 28px rgba(0,0,0,0.12);
}
.hi-img-2 {
  width: 100%; height: 100%;
  object-fit: cover; border-radius: 16px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
  grid-row: 1 / span 2;
  align-self: center;
  height: 280px;
  margin-top: 40px;
}
.hi-stats { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; }
.hi-stat {
  background: #dcfce7; border: 1px solid #86efac; border-radius: 12px;
  padding: 16px; text-align: center;
}
.hi-stat strong { display: block; font-size: 1.8rem; font-weight: 800; color: #16a34a; }
.hi-stat span { font-size: 12px; color: #4a5e4a; }

.mv-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
.mv-card {
  background: #f8fafc; border-radius: 20px; padding: 40px;
  border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.mv-icon {
  width: 60px; height: 60px; background: #dcfce7; border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 28px; color: #16a34a; margin-bottom: 20px;
}
.mv-card h3 { font-size: 1.4rem; font-weight: 700; color: #1e293b; margin-bottom: 12px; }
.mv-card p { font-size: 15px; color: #475569; line-height: 1.75; }

.valores-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 24px; }
.valor-card {
  background: white; border-radius: 16px; padding: 28px;
  border: 1px solid #e2e8f0; transition: all 0.2s;
}
.valor-card:hover { border-color: #86efac; transform: translateY(-4px); box-shadow: 0 8px 24px rgba(22,163,74,0.1); }
.valor-card ion-icon { font-size: 32px; color: #16a34a; margin-bottom: 12px; }
.valor-card h4 { font-size: 16px; font-weight: 700; color: #1e293b; margin-bottom: 8px; }
.valor-card p { font-size: 13px; color: #64748b; line-height: 1.6; }

.compromiso-box {
  text-align: center; color: white; max-width: 700px; margin: 0 auto;
  display: flex; flex-direction: column; align-items: center; gap: 20px;
}
.compromiso-box ion-icon { font-size: 60px; color: #86efac; }
.compromiso-box h2 { font-size: 2rem; font-weight: 800; }
.compromiso-box p { font-size: 16px; color: rgba(255,255,255,0.75); line-height: 1.8; }
.btn-green {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 12px 28px; background: #16a34a; color: white;
  border: none; border-radius: 10px; font-size: 15px; font-weight: 700;
  text-decoration: none; cursor: pointer; font-family: inherit; transition: all 0.2s;
}
.btn-green:hover { background: #15803d; }

@media (max-width: 768px) {
  .historia-grid, .mv-grid { grid-template-columns: 1fr; }
  .valores-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 480px) {
  .valores-grid { grid-template-columns: 1fr; }
}
</style>
