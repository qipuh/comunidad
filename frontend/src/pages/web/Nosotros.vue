<template>
  <LayoutPublico>
    <section class="page-hero" :style="{ backgroundImage: `url('/uploads/img/variadas/coscore-bajo-2.png')` }">
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
            <img :src="'/uploads/logo/logo.png'" alt="Comunidad TPCT Torata · Moquegua · Perú" style="width: 150px;" />
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

    <!-- BANDERA COMUNAL -->
    <section class="section bg-light">
      <div class="container">
        <div class="section-head">
          <span class="tag">Identidad comunal</span>
          <h2>Bandera Comunal</h2>
        </div>
        <div class="bandera-grid">
          <div class="bandera-visual">
            <img :src="'/uploads/logo/logo.png'" alt="Bandera de la Comunidad Campesina TPCT" class="bandera-svg" />
          </div>
          <div class="bandera-info">
            <div class="bandera-colores">
              <div class="color-item">
                <div class="color-dot rojo"></div>
                <div><strong>Color Rojo</strong><p>Demuestra la fuerza, valentía y generosidad de nuestra gente.</p></div>
              </div>
              <div class="color-item">
                <div class="color-dot amarillo"></div>
                <div><strong>Color Amarillo</strong><p>Demuestra la inmensidad de nuestro territorio y ubérrimos valles.</p></div>
              </div>
              <div class="color-item">
                <div class="color-dot negro"></div>
                <div><strong>Silueta Humana</strong><p>Inspirada en las pinturas rupestres de la Cueva de Coscore (más de 12,000 A.C.), representa a los primeros caminantes en nuestra tierra.</p></div>
              </div>
            </div>
            <div class="historia-bandera">
              <p>En gran Asamblea General realizada en la <strong>Plaza de Coscore el 15 de noviembre de 2015</strong>, con asistencia de 195 comuneros, la propuesta fue <strong>aprobada por unanimidad</strong>. Los colores negro, rojo y amarillo son los colores originarios usados por nuestros antepasados.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- RESEÑA HISTÓRICA -->
    <section class="section">
      <div class="container">
        <div class="section-head">
          <span class="tag">Nuestra historia</span>
          <h2>Reseña Histórica</h2>
        </div>
        <div class="resena-grid">
          <div class="resena-texto">
            <p>Los criadores de ganado de Moquegua, Tumilaca, Pocata, Coscore, Torata, Tala y Asana compraron los terrenos denominados ancestralmente <strong>Los Altos y Pastales de Coscore</strong>, según Escrituras Públicas del 4 de mayo de 1894 y 21 de setiembre de 1929.</p>
            <p>El <strong>7 de setiembre de 1949</strong>, mediante Resolución Suprema, siendo Presidente de la República el General Manuel A. Odría, se reconoció oficialmente la <strong>Comunidad de Indígenas Tumilaca – Pocata – Coscore – Tala</strong>. En 1969, bajo el gobierno del General Juan Velasco Alvarado, pasó a denominarse Comunidad Campesina. En 1993 perfeccionó sus títulos mediante la Ley de Deslinde y Titulación.</p>
            <p>En el ámbito de la Comunidad se encuentran Pocata, Coscore, Tala, Cocotea, Quebrada Honda, Calientes y Chibaya, así como toda el área de los ancestrales <strong>Los Altos y Pastales de Coscore</strong>.</p>
            <p class="vivacomunidad">¡VIVA LA COMUNIDAD CAMPESINA!</p>
          </div>
          <div class="resena-presidentes">
            <h3><ion-icon name="people-outline"></ion-icon> Presidentes Comunales</h3>
            <div class="presidentes-lista">
              <div v-for="p in presidentes" :key="p.nombre" class="presidente-item">
                <span class="p-periodo">{{ p.periodo }}</span>
                <span class="p-nombre">{{ p.nombre }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- JUNTAS DIRECTIVAS -->
    <section class="section">
      <div class="container">
        <div class="section-head">
          <span class="tag">Gobierno comunal</span>
          <h2>Juntas Directivas</h2>
          <p class="section-sub">Registro histórico de juntas directivas según Partida Registral N° 11001608 · SUNARP Zona Registral XIII, Oficina Registral Moquegua.</p>
        </div>

        <div class="jd-stats">
          <div class="jd-stat"><strong>13</strong><span>Períodos registrados</span></div>
          <div class="jd-stat"><strong>25</strong><span>Años de historia</span></div>
          <div class="jd-stat"><strong>11001608</strong><span>Partida SUNARP</span></div>
        </div>

        <div class="jd-vigente">
          <div class="jd-vigente-head">
            <span class="jd-badge">En ejercicio</span>
            <span class="jd-vigente-periodo">01 enero 2025 — 31 diciembre 2026</span>
          </div>
          <div class="jd-vigente-grid">
            <div
              v-for="(m, i) in juntaVigente"
              :key="m.cargo"
              class="jd-vigente-item"
              :class="{ 'jd-vigente-pres': i === 0 }"
            >
              <span class="jd-cargo-label">{{ m.cargo }}</span>
              <span class="jd-cargo-nombre">{{ m.nombre }}</span>
            </div>
          </div>
        </div>

        <div class="jd-timeline">
          <div class="jd-period" v-for="(p, idx) in juntasHistoricas" :key="p.periodo">
            <button type="button" class="jd-period-head" @click="toggleJunta(idx)">
              <span class="jd-period-left">
                <span class="jd-dot" :class="{ nula: p.nula }"></span>
                <span class="jd-period-textos">
                  <span class="jd-period-title">Período {{ p.periodo }}</span>
                  <span class="jd-period-pres">{{ p.pres }}</span>
                </span>
              </span>
              <ion-icon name="chevron-down-outline" class="jd-chevron" :class="{ open: abiertos.includes(idx) }"></ion-icon>
            </button>
            <div class="jd-period-body" v-show="abiertos.includes(idx)">
              <div v-if="p.nula" class="jd-nula">
                <ion-icon name="alert-circle-outline"></ion-icon> Período declarado nulo por resolución judicial
              </div>
              <div v-if="p.obs && !p.nula" class="jd-obs">{{ p.obs }}</div>
              <table class="jd-table">
                <tbody>
                  <tr v-for="(m, j) in p.miembros" :key="m[0]" :class="{ 'jd-pres-row': j === 0 }">
                    <td class="jd-td-cargo">{{ m[0] }}</td>
                    <td class="jd-td-nombre">{{ m[1] }}</td>
                  </tr>
                </tbody>
              </table>
              <span class="jd-asiento">Asiento registral: {{ p.asiento }}</span>
            </div>
          </div>
        </div>

        <p class="jd-footer-note">
          Fuente: Certificado Literal · Partida Registral N° 11001608<br />
          SUNARP Zona Registral XIII · Oficina Registral Moquegua
        </p>
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
import { ref } from 'vue'
import LayoutPublico from './LayoutPublico.vue'
import { useWebNav } from '../../composables/useWebNav'
const { navegar } = useWebNav()

const juntaVigente = [
  { cargo: 'Presidente', nombre: 'Marcos Santos García Nina' },
  { cargo: 'Vicepresidente', nombre: 'Ramón Marca' },
  { cargo: 'Secretario', nombre: 'Florentino Jesús Paripanca Ramos' },
  { cargo: 'Tesorero', nombre: 'Lizet Yanira Coaila Gutiérrez' },
  { cargo: 'Fiscal', nombre: 'Máxima Concesa Cuaila Cuaila' },
  { cargo: 'Vocal 1', nombre: 'Yonathan Michael Cabana Paripanca' },
  { cargo: 'Vocal 2', nombre: 'Yasmín Miriam Flores Gutiérrez' },
  { cargo: 'Vocal 3', nombre: 'Tanislao Rubén Flores Copa' },
]

const juntasHistoricas = [
  { periodo: '2023 – 2024', asiento: 'A000044', pres: 'Iván Bruno Mendoza Venancio', nula: false, miembros: [
    ['Presidente', 'Iván Bruno Mendoza Venancio'],
    ['Vicepresidente', 'Marcos Santos García Nina'],
    ['Secretaria', 'Lidia Reyna Flores Cacallica'],
    ['Tesorero', 'Leonardo Nicomedes Centeno García'],
    ['Fiscal', 'Gladys Verónica Zeballos Fernández'],
    ['Vocal 1', 'Néstor Pedro Coaila García'],
    ['Vocal 2', 'Rossy Karina Quispe Motocanchi'],
    ['Vocal 3', 'Hilario Rafael Cabana Cuaila'],
  ] },
  { periodo: '2021 – 2022', asiento: 'A000042', pres: 'Dionilde Flora Flores Calizaya', nula: false, miembros: [
    ['Presidenta', 'Dionilde Flora Flores Calizaya'],
    ['Vicepresidente', 'Héctor Jesús Centeno Quispe'],
    ['Secretaria', 'Nancy Genoveva Marca Gutiérrez'],
    ['Tesorero', 'Eli Florentino García Nina'],
    ['Fiscal', 'José Manuel García Condori'],
    ['Vocal 1', 'Iván Bruno Mendoza Venancio'],
    ['Vocal 2', 'Josselin Heydi Gutiérrez García'],
    ['Vocal 3', 'Pedro Daniel Gutiérrez Venancio'],
  ] },
  { periodo: '2019 – 2020', asiento: 'A000038', pres: 'Rubén Benedicto Centeno Soto', nula: false, miembros: [
    ['Presidente', 'Rubén Benedicto Centeno Soto'],
    ['Vicepresidenta', 'Dionilde Flora Flores Calizaya'],
    ['Secretaria', 'Máxima Concesa Cuaila Cuaila'],
    ['Tesorera', 'Paulina Faustina Paripanca Ramos'],
    ['Fiscal', 'Agustín Factor Flores Flores'],
    ['Vocal 1', 'Gregorio Florentino García Heredia'],
    ['Vocal 2', 'Patricia Lidia Flores Gutiérrez'],
    ['Vocal 3', 'Leonir Juan Gutiérrez Venancio'],
  ] },
  { periodo: '2017 – 2018', asiento: 'A000037', pres: 'Juvencio Ricardo Flores Flores', nula: false, miembros: [
    ['Presidente', 'Juvencio Ricardo Flores Flores'],
    ['Vicepresidente', 'Marcelo Julián Gutiérrez Mamani'],
    ['Secretaria', 'Erica Lucila Paripanca Cabana'],
    ['Tesorero', 'Rubén Benedicto Centeno Soto'],
    ['Fiscal', 'Tanislao Rubén Flores Copa'],
    ['Vocal 1', 'Beatriz Vanessa García Gutiérrez'],
    ['Vocal 2', 'Lidia Reyna Flores Cacallica'],
    ['Vocal 3', 'Ismael Francisco Acahuana Heredia'],
  ] },
  { periodo: '2015 – 2016', asiento: 'A000033', pres: 'Irenio Eladio Peñaloza Gutiérrez', nula: false, miembros: [
    ['Presidente', 'Irenio Eladio Peñaloza Gutiérrez'],
    ['Vicepresidente', 'Asencio Cornelio Centeno Coaila'],
    ['Secretario', 'David Lucio Marca Arambulo'],
    ['Tesorera', 'Gladys Verónica Zeballos Fernández'],
    ['Fiscal', 'José Manuel García Condori'],
    ['Vocal 1', 'José Bernardo Cuaila Coayla'],
    ['Vocal 2', 'Elida Agripina Coaila Llica'],
    ['Vocal 3', 'Ricardo Julián Cuaila Gutiérrez'],
  ] },
  { periodo: '2013 – 2014', asiento: 'A000032', pres: 'Germán Fidel Coaila García', nula: false, miembros: [
    ['Presidente', 'Germán Fidel Coaila García'],
    ['Vicepresidenta', 'Betty Ruth Mendoza Venancio'],
    ['Secretario', 'Francisco Vidal Acahuana Heredia'],
    ['Tesorera', 'Claudia Julia Mamani Gutiérrez'],
    ['Fiscal', 'Juan Fermín Marca Peñaloza'],
    ['Vocal 1', 'Elías Enrique Cuaila Gutiérrez'],
    ['Vocal 2', 'Agustín Rufino Llica Copa'],
    ['Vocal 3', 'Arcadio Paripanca Ramos'],
  ] },
  { periodo: '2011 – 2012', asiento: 'A000030', pres: 'Germán Fidel Coaila García', nula: false, miembros: [
    ['Presidente', 'Germán Fidel Coaila García'],
    ['Vicepresidente', 'Agustín Factor Flores Flores'],
    ['Secretaria', 'Claudia Julia Mamani Gutiérrez'],
    ['Tesorera', 'Gumercinda Julia Maldonado'],
    ['Fiscal', 'Juan Fermín Marca Peñaloza'],
    ['Vocal 1', 'José Carlos Mamani Yupanqui'],
    ['Vocal 2', 'Francisco Vidal Acahuana Heredia'],
    ['Vocal 3', 'Gregorio García Heredia'],
  ] },
  { periodo: '2009 – 2010', asiento: 'A000025', pres: 'Eugenio Zacarías Cuayla Arias', nula: false, miembros: [
    ['Presidente', 'Eugenio Zacarías Cuayla Arias'],
    ['Vicepresidente', 'Arsenio Domingo Fernández Gutiérrez'],
    ['Secretaria', 'Elida Agripina Coaila Llica'],
    ['Tesorero', 'Ricardo Julián Cuaila Gutiérrez'],
    ['Fiscal', 'Juvencio Ricardo Flores Flores'],
    ['Vocal 1', 'Hipólito Casiano Centeno Mamani'],
    ['Vocal 2', 'Jacinto Manuel Marca García'],
    ['Vocal 3', 'Silverio Agustín Gutiérrez García'],
  ] },
  { periodo: '2007 – 2008', asiento: 'A000021', pres: 'Asencio Cornelio Centeno Coaila', nula: false,
    obs: 'El secretario Víctor Martín Nina Copa renunció durante el período y fue reemplazado por Amparo Verónica Gutiérrez Flores.',
    miembros: [
      ['Presidente', 'Asencio Cornelio Centeno Coaila'],
      ['Vicepresidente', 'Genaro Flores Álvarez'],
      ['Secretario', 'Víctor Martín Nina Copa'],
      ['Tesorero', 'Irenio Eladio Peñaloza Gutiérrez'],
      ['Fiscal', 'Agustín Facto Flores Flores'],
      ['Vocal 1', 'Agustín Pare Miranda'],
      ['Vocal 2', 'Darío Agustín Mamani Vilca'],
      ['Vocal 3', 'Wilson Román Calizaya Venancio'],
    ] },
  { periodo: '2005 – 2006', asiento: 'A000018', pres: 'Juvencio Ricardo Flores Flores', nula: false, miembros: [
    ['Presidente', 'Juvencio Ricardo Flores Flores'],
    ['Vicepresidente', 'Guilson Román Calizaya Venancio'],
    ['Secretaria', 'Claudia Julia Mamani Gutiérrez'],
    ['Tesorero', 'José García Condori'],
    ['Fiscal', 'Javier Coaila Coaila'],
    ['Vocal 1', 'Gregorio García Heredia'],
    ['Vocal 2', 'Tonislao Flores Copa'],
    ['Vocal 3', 'Cipriano Marco Gutiérrez'],
  ] },
  { periodo: '2003 – 2004', asiento: 'A000017', pres: 'Juvencio Ricardo Flores Flores', nula: false, miembros: [
    ['Presidente', 'Juvencio Ricardo Flores Flores'],
    ['Vicepresidente', 'Guilson Calizaya Venancio'],
    ['Secretario', 'Nicolás Mamani Flores'],
    ['Tesorero', 'José García Condori'],
    ['Fiscal', 'Javier Cuayla Cuayla'],
    ['Vocal 1', 'Tanislao Flores Copa'],
    ['Vocal 2', 'Gregorio García Heredia'],
    ['Vocal 3', 'Cipriana Marca Gutiérrez'],
  ] },
  { periodo: '2001 – 2002', asiento: 'A00012', pres: 'Mercedes Marca Fernández', nula: true,
    obs: 'Declarada nula y sin efecto por resolución judicial (2° Juzgado Mixto de Mariscal Nieto, diciembre de 2002).',
    miembros: [
      ['Presidenta', 'Mercedes Marca Fernández'],
      ['Vicepresidente', 'Acencio Cornelio Centeno Cuayla'],
      ['Secretario', 'Alvin Marca Copa'],
      ['Tesorera', 'Eugenia Nina Copa'],
      ['Fiscal', 'Juan Marca Peñaloza'],
      ['Vocal 1', 'Carlos Flores Torres'],
      ['Vocal 2', 'Sabino Flores Flores'],
      ['Vocal 3', 'Alberto Venancio Venegas'],
    ] },
]

const abiertos = ref([])
function toggleJunta(idx) {
  const i = abiertos.value.indexOf(idx)
  if (i === -1) abiertos.value.push(idx)
  else abiertos.value.splice(i, 1)
}

const hitos = [
  { value: '1949', label: 'Año de fundación' },
  { value: '77', label: 'Años de historia' },
  { value: '4', label: 'Anexos territoriales' },
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

/* BANDERA */
.bandera-grid { display: grid; grid-template-columns: 260px 1fr; gap: 48px; align-items: start; }
.bandera-svg { width: 200px; border: 2px solid #ddd; border-radius: 4px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.15); }
.franja { width: 100%; height: 90px; display: flex; align-items: center; justify-content: center; }
.franja.amarilla { background: #FFD700; }
.franja.roja { background: #CC0000; }
.silueta { font-size: 52px; color: #1a1a1a; }
.bandera-dim { font-size: 12px; color: #64748b; margin-top: 10px; text-align: center; line-height: 1.5; }
.bandera-colores { display: flex; flex-direction: column; gap: 18px; margin-bottom: 20px; }
.color-item { display: flex; align-items: flex-start; gap: 14px; }
.color-dot { width: 28px; height: 28px; border-radius: 50%; flex-shrink: 0; margin-top: 2px; }
.color-dot.rojo { background: #CC0000; }
.color-dot.amarillo { background: #FFD700; border: 1px solid #ccc; }
.color-dot.negro { background: #1a1a1a; }
.color-item strong { display: block; font-size: 14px; color: #1a2e1a; margin-bottom: 3px; }
.color-item p { font-size: 13px; color: #475569; line-height: 1.6; margin: 0; }
.historia-bandera { background: #f0fdf4; border-left: 4px solid #1aa86a; border-radius: 0 10px 10px 0; padding: 16px 20px; }
.historia-bandera p { font-size: 14px; color: #374151; line-height: 1.7; margin: 0; }

/* RESEÑA */
.resena-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; }

/* JUNTAS DIRECTIVAS */
.section-sub { max-width: 640px; margin: 8px auto 0; font-size: 14px; color: #64748b; line-height: 1.6; }
.jd-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; max-width: 640px; margin: 0 auto 40px; }
.jd-stat { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; text-align: center; }
.jd-stat strong { display: block; font-size: 1.6rem; font-weight: 800; color: #16a34a; }
.jd-stat span { font-size: 12px; color: #64748b; }

.jd-vigente { background: #dcfce7; border: 1.5px solid #16a34a; border-radius: 16px; padding: 28px; margin-bottom: 40px; }
.jd-vigente-head { display: flex; align-items: center; gap: 14px; margin-bottom: 20px; flex-wrap: wrap; }
.jd-badge { background: #16a34a; color: #fff; font-size: 12px; font-weight: 700; padding: 4px 14px; border-radius: 100px; }
.jd-vigente-periodo { font-size: 15px; font-weight: 700; color: #14532d; }
.jd-vigente-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.jd-vigente-item { display: flex; flex-direction: column; gap: 2px; background: rgba(255,255,255,0.6); border-radius: 10px; padding: 12px 14px; }
.jd-vigente-item.jd-vigente-pres { grid-column: 1 / -1; background: rgba(255,255,255,0.9); border: 1px solid #16a34a; }
.jd-cargo-label { font-size: 11px; font-weight: 700; color: #16a34a; text-transform: uppercase; letter-spacing: 0.04em; }
.jd-cargo-nombre { font-size: 14px; color: #14532d; font-weight: 500; }

.jd-timeline { display: flex; flex-direction: column; gap: 12px; margin-bottom: 32px; }
.jd-period { border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; background: #fff; }
.jd-period-head {
  width: 100%; display: flex; align-items: center; justify-content: space-between;
  padding: 16px 18px; background: #f8fafc; border: none; cursor: pointer; font-family: inherit; text-align: left;
}
.jd-period-head:hover { background: #f1f5f9; }
.jd-period-left { display: flex; align-items: center; gap: 12px; }
.jd-dot { width: 9px; height: 9px; border-radius: 50%; background: #16a34a; flex-shrink: 0; }
.jd-dot.nula { background: #dc2626; }
.jd-period-textos { display: flex; flex-direction: column; }
.jd-period-title { font-size: 15px; font-weight: 700; color: #1a2e1a; }
.jd-period-pres { font-size: 13px; color: #64748b; }
.jd-chevron { font-size: 18px; color: #94a3b8; transition: transform 0.2s; }
.jd-chevron.open { transform: rotate(180deg); }

.jd-period-body { padding: 14px 18px 20px; border-top: 1px solid #e2e8f0; }
.jd-nula { background: #fee2e2; border: 1px solid #fca5a5; border-radius: 8px; padding: 8px 12px; font-size: 13px; color: #991b1b; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
.jd-obs { font-size: 13px; color: #854d0b; background: #fef3c7; border-radius: 8px; padding: 8px 12px; margin-bottom: 12px; }

.jd-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.jd-table td { padding: 8px 6px; border-bottom: 1px solid #f1f5f9; }
.jd-table tr:last-child td { border-bottom: none; }
.jd-td-cargo { color: #64748b; width: 40%; }
.jd-td-nombre { color: #1a2e1a; }
.jd-pres-row td { background: #f0fdf4; }
.jd-pres-row .jd-td-cargo { color: #16a34a; font-weight: 600; }
.jd-pres-row .jd-td-nombre { font-weight: 600; color: #14532d; }
.jd-asiento { display: inline-block; font-size: 11px; color: #94a3b8; background: #f8fafc; border-radius: 6px; padding: 3px 8px; margin-top: 10px; }

.jd-footer-note { font-size: 12px; color: #94a3b8; text-align: center; padding-top: 20px; border-top: 1px solid #e2e8f0; line-height: 1.6; }

@media (max-width: 768px) {
  .jd-vigente-grid { grid-template-columns: 1fr; }
  .jd-stats { grid-template-columns: 1fr; }
}

@media (max-width: 1024px) {
  .historia-grid { gap: 40px; }
  .bandera-grid { grid-template-columns: 200px 1fr; gap: 32px; }
  .resena-grid { gap: 32px; }
  .valores-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .section { padding: 60px 0; }
  .historia-grid { grid-template-columns: 1fr; gap: 32px; }
  .hi-collage { grid-template-columns: 1fr 1fr; grid-template-rows: 180px; }
  .hi-img-1 { grid-row: auto; }
  .hi-img-2 { grid-row: auto; height: 180px; margin-top: 0; }
  .hi-stats { grid-template-columns: repeat(3, 1fr); }
  .mv-grid { grid-template-columns: 1fr; gap: 20px; }
  .mv-card { padding: 28px 20px; }
  .valores-grid { grid-template-columns: 1fr 1fr; gap: 16px; }
  .bandera-grid { grid-template-columns: 1fr; gap: 24px; }
  .bandera-visual { display: flex; flex-direction: column; align-items: center; }
  .bandera-svg { width: 180px; }
  .resena-grid { grid-template-columns: 1fr; gap: 32px; }
  .presidentes-lista { max-height: none; }
  .section-head h2 { font-size: 1.6rem; }
  .ph-content h1 { font-size: 1.8rem; }
}

@media (max-width: 480px) {
  .section { padding: 48px 0; }
  .valores-grid { grid-template-columns: 1fr; }
  .hi-collage { grid-template-columns: 1fr; grid-template-rows: 200px 160px; }
  .hi-stats { grid-template-columns: 1fr 1fr; }
  .hi-stat:last-child { grid-column: span 2; }
  .mv-card { padding: 24px 16px; }
  .compromiso-box h2 { font-size: 1.5rem; }
  .color-item { gap: 10px; }
  .presidente-item { flex-wrap: wrap; gap: 4px; }
  .p-periodo { min-width: auto; }
}
.resena-texto { display: flex; flex-direction: column; gap: 16px; }
.resena-texto p { font-size: 15px; color: #374151; line-height: 1.8; }
.vivacomunidad { font-weight: 800; color: #15803d; font-size: 16px; text-align: center; padding: 12px; background: #dcfce7; border-radius: 8px; }
.resena-presidentes h3 { display: flex; align-items: center; gap: 8px; font-size: 17px; font-weight: 700; color: #1a2e1a; margin-bottom: 16px; }
.resena-presidentes h3 ion-icon { color: #1aa86a; }
.presidentes-lista { display: flex; flex-direction: column; gap: 6px; max-height: 420px; overflow-y: auto; }
.presidente-item { display: flex; align-items: center; gap: 12px; padding: 9px 14px; background: white; border-radius: 8px; border: 1px solid #e2e8f0; }
.p-periodo { font-size: 12px; font-weight: 700; color: #1aa86a; white-space: nowrap; min-width: 80px; }
.p-nombre { font-size: 13px; color: #1e293b; font-weight: 500; }
</style>
