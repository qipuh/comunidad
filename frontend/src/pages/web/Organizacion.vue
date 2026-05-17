<template>
  <LayoutPublico>
    <section class="page-hero" :style="{ backgroundImage: `url('https://images.unsplash.com/photo-1519074598089-6436475c7f8f?w=1800&q=80')` }">
      <div class="ph-overlay"></div>
      <div class="ph-content">
        <span class="ph-tag"><ion-icon name="business-outline"></ion-icon> Organización</span>
        <h1>Organización Comunal</h1>
        <p>Gobierno democrático y participativo al servicio de los comuneros</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="intro-org">
          <p>La Comunidad Campesina TPCT cuenta con una estructura organizativa basada en principios democráticos y participativos, donde la <strong>Asamblea General de Comuneros</strong> constituye la máxima instancia de decisión.</p>
        </div>

        <!-- Junta Directiva -->
        <div class="section-head">
          <span class="tag">Autoridades 2024–2026</span>
          <h2>Junta Directiva</h2>
        </div>

        <!-- Presidente destacado -->
        <div class="presidente-card">
          <div class="pres-img">
            <img src="https://images.unsplash.com/photo-1568805778734-f0a5a77d7272?w=400&q=80" alt="Presidente" />
          </div>
          <div class="pres-info">
            <span class="pres-cargo">Presidente</span>
            <h2>Marcos Santos García Nina</h2>
            <p>Presidente de la Comunidad Campesina de Tumilaca, Pocata, Coscore y Tala para el período 2024–2026. Comprometido con la defensa del territorio y el desarrollo integral de los comuneros.</p>
            <div class="pres-badges">
              <span><ion-icon name="location-outline"></ion-icon> Torata, Moquegua</span>
              <span><ion-icon name="calendar-outline"></ion-icon> Período 2024–2026</span>
            </div>
          </div>
        </div>

        <!-- Resto de directiva -->
        <div class="directiva-grid">
          <div v-for="d in directiva" :key="d.rol" class="directivo-card">
            <div class="d-avatar">{{ d.nombre.charAt(0) }}</div>
            <div class="d-info">
              <span class="d-rol">{{ d.rol }}</span>
              <strong>{{ d.nombre }}</strong>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section bg-light">
      <div class="container">
        <div class="section-head">
          <span class="tag">Comisiones</span>
          <h2>Comisión de Negociación</h2>
        </div>
        <div class="comision-card">
          <div class="comision-desc">
            <ion-icon name="people-circle-outline"></ion-icon>
            <h3>Función</h3>
            <p>Encargada de representar a la comunidad en procesos de diálogo y negociación con entidades públicas y privadas, velando por los intereses colectivos de los comuneros.</p>
          </div>
          <div class="comision-miembros">
            <h3>Integrantes</h3>
            <div class="miembros-lista">
              <div v-for="m in comision" :key="m" class="miembro-item">
                <div class="m-avatar">{{ m.charAt(0) }}</div>
                <span>{{ m }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head">
          <span class="tag">Estructura territorial</span>
          <h2>Autoridades por Anexos</h2>
        </div>
        <div class="anexos-grid">
          <div v-for="a in anexos" :key="a.nombre" class="anexo-card">
            <div class="anexo-header">
              <ion-icon name="location-outline"></ion-icon>
              <h3>{{ a.nombre }}</h3>
            </div>
            <div class="cargos-lista">
              <div v-for="c in cargosAnexo" :key="c" class="cargo-row">
                <span class="cargo-label">{{ c }}</span>
                <span class="cargo-vacio">Por designar</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section bg-dark">
      <div class="container">
        <div class="asamblea-box">
          <ion-icon name="people-outline"></ion-icon>
          <h2>Asamblea General de Comuneros</h2>
          <p>La Asamblea General es la máxima autoridad de la comunidad. Todos los comuneros debidamente inscritos participan con voz y voto en la toma de decisiones trascendentales.</p>
        </div>
      </div>
    </section>
  </LayoutPublico>
</template>

<script setup>
import LayoutPublico from './LayoutPublico.vue'

const directiva = [
  { rol: 'Vicepresidente', nombre: 'Ramón Marca' },
  { rol: 'Secretario', nombre: 'Florentino Jesús Paripanca Ramos' },
  { rol: 'Tesorera', nombre: 'Lizet Yanira Coaila Gutierrez' },
  { rol: 'Fiscal', nombre: 'Máxima Concesa Cuaila Cuaila' },
  { rol: 'Vocal 1', nombre: 'Yonathan Michael Cabana Paripanca' },
  { rol: 'Vocal 2', nombre: 'Yasmin Miriam Flores Gutierrez' },
  { rol: 'Vocal 3', nombre: 'Tanislao Flores Copa' },
]

const comision = ['Paulina Paripanca', 'Wilmer Rojas Garay', 'Miguel Lazo', 'Marco Centeno']

const anexos = [
  { nombre: 'Anexo Pocata' }, { nombre: 'Anexo Coscore' },
  { nombre: 'Anexo Tala' }, { nombre: 'Anexo Quebrada Honda' },
]

const cargosAnexo = ['Presidente', 'Vicepresidente', 'Tesorero', 'Fiscal']
</script>

<style scoped>
.page-hero { min-height: 50vh; background-size: cover; background-position: center; display: flex; align-items: center; position: relative; }
.ph-overlay { position: absolute; inset: 0; background: rgba(5,20,8,0.78); }
.ph-content { position: relative; z-index: 2; max-width: 1200px; margin: 0 auto; padding: 120px 24px 80px; color: white; }
.ph-tag { display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; background: rgba(134,239,172,0.15); color: #86efac; border-radius: 100px; font-size: 13px; font-weight: 600; margin-bottom: 16px; }
.ph-content h1 { font-size: clamp(2rem,4vw,3rem); font-weight: 800; margin-bottom: 10px; }
.ph-content p { font-size: 16px; color: rgba(255,255,255,0.7); }

.section { padding: 80px 0; background: white; }
.section.bg-light { background: white; }
.section.bg-dark { background: linear-gradient(160deg,#0a1e0c,#0f2814); }
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.section-head { text-align: center; margin-bottom: 48px; }
.section-head h2 { font-size: 2rem; font-weight: 800; color: #1a2e1a; }
.tag { display: inline-block; padding: 4px 14px; background: #dcfce7; color: #15803d; border-radius: 100px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }

.intro-org { max-width: 800px; margin: 0 auto 60px; text-align: center; font-size: 16px; color: #475569; line-height: 1.8; }

.presidente-card {
  display: grid; grid-template-columns: 280px 1fr; gap: 48px;
  background: white; border-radius: 20px; overflow: hidden;
  border: 1px solid #e2e8f0; box-shadow: 0 4px 16px rgba(0,0,0,0.07);
  margin-bottom: 40px;
}
.pres-img { height: 320px; overflow: hidden; }
.pres-img img { width: 100%; height: 100%; object-fit: cover; }
.pres-info { padding: 40px 40px 40px 0; display: flex; flex-direction: column; gap: 14px; }
.pres-cargo { display: inline-block; padding: 4px 14px; background: #dcfce7; color: #15803d; border-radius: 100px; font-size: 12px; font-weight: 700; width: fit-content; }
.pres-info h2 { font-size: 1.8rem; font-weight: 800; color: #1e293b; }
.pres-info p { font-size: 15px; color: #64748b; line-height: 1.7; }
.pres-badges { display: flex; gap: 16px; flex-wrap: wrap; }
.pres-badges span { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #64748b; }
.pres-badges ion-icon { color: #16a34a; }

.directiva-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; }
.directivo-card {
  display: flex; align-items: center; gap: 14px;
  background: white; border-radius: 12px; padding: 16px 20px;
  border: 1px solid #e2e8f0; transition: all 0.2s;
}
.directivo-card:hover { border-color: #86efac; box-shadow: 0 4px 12px rgba(22,163,74,0.1); }
.d-avatar {
  width: 44px; height: 44px; border-radius: 50%;
  background: linear-gradient(135deg,#16a34a,#15803d);
  display: flex; align-items: center; justify-content: center;
  color: white; font-size: 18px; font-weight: 700; flex-shrink: 0;
}
.d-rol { font-size: 11px; font-weight: 700; text-transform: uppercase; color: #16a34a; letter-spacing: 0.5px; }
.d-info strong { display: block; font-size: 14px; color: #1e293b; margin-top: 2px; }

.comision-card {
  display: grid; grid-template-columns: 1fr 1fr; gap: 0;
  background: white; border-radius: 20px; overflow: hidden;
  border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.comision-desc {
  padding: 40px; background: linear-gradient(135deg,#0a1e0c,#16a34a);
  color: white; display: flex; flex-direction: column; gap: 16px;
}
.comision-desc ion-icon { font-size: 48px; color: #86efac; }
.comision-desc h3 { font-size: 1.4rem; font-weight: 700; }
.comision-desc p { font-size: 15px; color: rgba(255,255,255,0.8); line-height: 1.7; }
.comision-miembros { padding: 40px; }
.comision-miembros h3 { font-size: 1.2rem; font-weight: 700; color: #1e293b; margin-bottom: 24px; }
.miembros-lista { display: flex; flex-direction: column; gap: 14px; }
.miembro-item { display: flex; align-items: center; gap: 14px; }
.m-avatar {
  width: 44px; height: 44px; border-radius: 50%;
  background: #dcfce7; color: #15803d;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; font-weight: 700; flex-shrink: 0;
}
.miembro-item span { font-size: 15px; font-weight: 600; color: #1e293b; }

.anexos-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 24px; }
.anexo-card { background: white; border-radius: 16px; border: 1px solid #e2e8f0; overflow: hidden; }
.anexo-header {
  display: flex; align-items: center; gap: 10px;
  padding: 20px 24px; background: #f0fdf4; border-bottom: 1px solid #bbf7d0;
}
.anexo-header ion-icon { font-size: 22px; color: #16a34a; }
.anexo-header h3 { font-size: 17px; font-weight: 700; color: #1e293b; }
.cargos-lista { padding: 20px 24px; display: flex; flex-direction: column; gap: 10px; }
.cargo-row { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #f1f5f9; }
.cargo-label { font-size: 14px; font-weight: 600; color: #1e293b; }
.cargo-vacio { font-size: 12px; color: #94a3b8; background: #f1f5f9; padding: 2px 10px; border-radius: 100px; }

.asamblea-box { text-align: center; color: white; max-width: 700px; margin: 0 auto; display: flex; flex-direction: column; align-items: center; gap: 20px; }
.asamblea-box ion-icon { font-size: 64px; color: #86efac; }
.asamblea-box h2 { font-size: 2rem; font-weight: 800; }
.asamblea-box p { font-size: 16px; color: rgba(255,255,255,0.75); line-height: 1.8; }

@media (max-width: 768px) {
  .presidente-card { grid-template-columns: 1fr; }
  .pres-img { height: 250px; }
  .pres-info { padding: 28px; }
  .directiva-grid { grid-template-columns: 1fr; }
  .comision-card { grid-template-columns: 1fr; }
  .anexos-grid { grid-template-columns: 1fr; }
}
</style>
