<template>
  <div class="web-publica">

    <!-- HEADER -->
    <header class="header" :class="{ scrolled: scrolled }">
      <div class="header-inner">
        <div class="brand">
          <div class="brand-logo">
            <img :src="'/uploads/logo/logo.png'" alt="Logo" class="logo-img" />
          </div>
          <div class="brand-text">
            <span class="brand-name">Comunidad Campesina TPCT</span>
            <span class="brand-sub">Tumilaca · Pocata · Coscore · Tala</span>
          </div>
        </div>

        <nav class="nav-desktop">
          <a href="#inicio" class="nav-link" @click.prevent="scrollTo('inicio')">Inicio</a>

          <!-- Dropdown Quienes Somos -->
          <div class="nav-dropdown">
            <button class="nav-drop-btn">
              Quienes Somos
              <ion-icon name="chevron-down-outline" class="chevron"></ion-icon>
            </button>
            <div class="nav-drop-content">
              <a href="#nosotros" class="drop-link" @click.prevent="scrollTo('nosotros')">Nosotros</a>
              <a href="#organizacion" class="drop-link" @click.prevent="scrollTo('organizacion')">Organización</a>
              <a href="#territorio" class="drop-link" @click.prevent="scrollTo('territorio')">Territorio</a>
            </div>
          </div>

          <a v-for="item in filteredHeaderItems" :key="item.id" :href="`#${item.id}`" class="nav-link" @click.prevent="scrollTo(item.id)">
            {{ item.label }}
          </a>
        </nav>

        <div class="header-actions">
          <a href="/admin" class="btn-admin" @click.prevent="irAdmin">
            <ion-icon name="lock-closed-outline"></ion-icon> Intranet
          </a>
          <button class="hamburger" @click="menuOpen = !menuOpen">
            <span></span><span></span><span></span>
          </button>
        </div>
      </div>

      <!-- Menú mobile -->
      <div class="nav-mobile" :class="{ open: menuOpen }">
        <a href="#inicio" class="nav-mobile-link" @click.prevent="scrollTo('inicio'); menuOpen = false">Inicio</a>

        <div class="mobile-group">
          <div class="mobile-group-header">Quienes Somos</div>
          <a href="#nosotros" class="nav-mobile-link sub" @click.prevent="scrollTo('nosotros'); menuOpen = false">Nosotros</a>
          <a href="#organizacion" class="nav-mobile-link sub" @click.prevent="scrollTo('organizacion'); menuOpen = false">Organización</a>
          <a href="#territorio" class="nav-mobile-link sub" @click.prevent="scrollTo('territorio'); menuOpen = false">Territorio</a>
        </div>

        <a v-for="item in filteredHeaderItems" :key="item.id" :href="`#${item.id}`" class="nav-mobile-link" @click.prevent="scrollTo(item.id); menuOpen = false">
          {{ item.label }}
        </a>
        <a href="#" class="nav-mobile-link admin-link" @click.prevent="irAdmin">
          <ion-icon name="lock-closed-outline"></ion-icon> Intranet
        </a>
      </div>
    </header>

    <!-- HERO -->
    <section id="inicio" class="hero">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <div class="hero-badge">Distrito de Torata · Moquegua · Perú</div>
        <h1>Comunidad Campesina de<br><span class="highlight">Tumilaca, Pocata,<br>Coscore y Tala</span></h1>
        <p>Territorio, organización y desarrollo sostenible<br>al servicio de nuestros Usuarios.</p>
        <div class="hero-buttons">
          <button @click="scrollTo('nosotros')" class="btn-primary-hero">Conocer más</button>
          <button @click="scrollTo('contacto')" class="btn-secondary-hero">Contáctanos</button>
        </div>
      </div>
      <div class="hero-scroll" @click="scrollTo('nosotros')">
        <ion-icon name="arrow-down-outline"></ion-icon>
      </div>
    </section>

    <!-- STATS -->
    <section class="stats-section">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-number">77</div>
            <div class="stat-label">Años de historia</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">4</div>
            <div class="stat-label">Anexos comunales</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">1949</div>
            <div class="stat-label">Año de fundación</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">∞</div>
            <div class="stat-label">Tradición viva</div>
          </div>
        </div>
      </div>
    </section>

    <!-- NOSOTROS -->
    <section id="nosotros" class="section">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">Nuestra identidad</span>
          <h2>Nosotros</h2>
          <p>Conoce la historia, misión y valores de nuestra comunidad</p>
        </div>

        <div class="nosotros-grid">
          <div class="historia-card">
            <div class="card-icon"><ion-icon name="document-text-outline"></ion-icon></div>
            <h3>Historia</h3>
            <p>La Comunidad Campesina de Tumilaca, Pocata, Coscore y Tala tiene sus raíces en antiguas formas de organización colectiva que han permitido a las familias del valle de Tumilaca conservar sus tierras, su cultura y sus formas de producción tradicional.</p>
            <p>Sus orígenes formales se remontan al año <strong>1949</strong>, consolidándose como una organización representativa de carácter territorial, social y cultural. En el año 2026, la comunidad celebró su <strong>77° aniversario</strong>.</p>
            <p>Está conformada por los anexos de Tumilaca, Pocata, Coscore y Tala, territorios que mantienen una profunda relación con la tierra y una identidad cultural sólida.</p>
          </div>

          <div class="valores-col">
            <div class="mv-card">
              <div class="card-icon"><ion-icon name="locate-outline"></ion-icon></div>
              <h3>Misión</h3>
              <p>Promover el desarrollo integral de la comunidad mediante la gestión responsable de sus recursos naturales, el fortalecimiento de la organización comunal y la promoción de actividades agroproductivas sostenibles.</p>
            </div>
            <div class="mv-card">
              <div class="card-icon"><ion-icon name="telescope-outline"></ion-icon></div>
              <h3>Visión</h3>
              <p>Ser una comunidad organizada, fortalecida y reconocida a nivel regional por su capacidad de gestión territorial, desarrollo productivo sostenible y preservación de sus valores culturales.</p>
            </div>
            <div class="mv-card">
              <div class="card-icon"><ion-icon name="star-outline"></ion-icon></div>
              <h3>Valores</h3>
              <div class="valores-lista">
                <span v-for="v in valores" :key="v" class="valor-tag">{{ v }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ORGANIZACIÓN -->
    <section id="organizacion" class="section bg-light">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">Estructura</span>
          <h2>Organización Comunal</h2>
          <p>Gobierno democrático y participativo al servicio de los Usuarios</p>
        </div>

        <div class="org-grid">
          <!-- Junta Directiva -->
          <div class="org-card principal">
            <div class="org-header">
              <h3><ion-icon name="business-outline"></ion-icon> Junta Directiva</h3>
            </div>
            <div class="directiva-lista">
              <div v-for="cargo in juntaDirectiva" :key="cargo.rol" class="directivo-item">
                <span class="cargo-rol">{{ cargo.rol }}</span>
                <span class="cargo-nombre">{{ cargo.nombre }}</span>
              </div>
            </div>
          </div>

          <!-- Comisiones -->
          <div class="org-card">
            <div class="org-header">
              <h3><ion-icon name="clipboard-outline"></ion-icon> Comisión de Negociación</h3>
            </div>
            <p class="comision-desc">Encargada de representar a la comunidad en procesos de diálogo y negociación con entidades públicas y privadas.</p>
            <ul class="comision-lista">
              <li>Paulina Paripanca</li>
              <li>Wilmer Rojas Garay</li>
              <li>Miguel Lazo</li>
              <li>Marco Centeno</li>
            </ul>
          </div>

          <!-- Anexos -->
          <div class="org-card">
            <div class="org-header">
              <h3><ion-icon name="location-outline"></ion-icon> Autoridades por Anexos</h3>
            </div>
            <div class="anexos-lista">
              <div v-for="anexo in anexos" :key="anexo" class="anexo-item">
                <span class="anexo-nombre">{{ anexo }}</span>
                <span class="anexo-status">En organización</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TERRITORIO -->
    <section id="territorio" class="section">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">Nuestra tierra</span>
          <h2>Nuestro Territorio</h2>
          <p>Valle de Tumilaca y zonas altoandinas del distrito de Torata</p>
        </div>

        <div class="territorio-grid">
          <div class="territorio-text">
            <p>La comunidad posee un amplio territorio ubicado en el valle de Tumilaca y zonas altoandinas del distrito de Torata, donde se desarrollan actividades agrícolas, ganaderas y de aprovechamiento de recursos naturales.</p>
            <p>El territorio comunal comprende diversos sectores y anexos, cada uno con características geográficas, productivas y culturales propias.</p>

            <div class="entorno-box">
              <h4><ion-icon name="briefcase-outline"></ion-icon> Entorno Económico y Productivo</h4>
              <p>En el ámbito territorial del distrito de Torata se desarrollan diversas actividades económicas, incluyendo proyectos mineros de gran envergadura como <strong>Quellaveco</strong> (Anglo American) y <strong>Cuajone</strong> (Southern Perú).</p>
              <p>La comunidad mantiene espacios de diálogo y coordinación con los distintos actores presentes en el territorio, en el marco del respeto a sus derechos colectivos.</p>
            </div>
          </div>

          <div class="territorio-mapa">
            <div class="mapa-placeholder">
              <div class="mapa-icon"><ion-icon name="map-outline"></ion-icon></div>
              <h4>Torata, Mariscal Nieto</h4>
              <p>Moquegua – Perú</p>
              <div class="anexos-chips">
                <span v-for="a in ['Tumilaca', 'Pocata', 'Coscore', 'Tala']" :key="a" class="chip">{{ a }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- PROYECTOS Y ECOSER -->
    <section id="proyectos" class="section bg-light">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">Desarrollo</span>
          <h2>Proyectos y Desarrollo</h2>
          <p>Iniciativas para el bienestar colectivo de los Usuarios</p>
        </div>

        <div class="lineas-grid">
          <div v-for="linea in lineas" :key="linea.titulo" class="linea-card">
            <div class="linea-icon"><ion-icon :name="linea.icono"></ion-icon></div>
            <h4>{{ linea.titulo }}</h4>
          </div>
        </div>

        <!-- ECOSER -->
        <div class="ecoser-card">
          <div class="ecoser-header">
            <div class="ecoser-logo"><ion-icon name="leaf-outline"></ion-icon> ECOSER</div>
            <span class="ecoser-tag">Empresa Comunal</span>
          </div>
          <div class="ecoser-grid">
            <div class="ecoser-desc">
              <h3>Empresa Comunal ECOSER</h3>
              <p>Brazo operativo y económico de la comunidad, orientado a la prestación de servicios y generación de oportunidades laborales para los Usuarios.</p>
              <div class="ecoser-objetivos">
                <div v-for="obj in ecoserObjetivos" :key="obj" class="obj-item">
                  <ion-icon name="checkmark-outline" class="obj-check"></ion-icon>
                  <span>{{ obj }}</span>
                </div>
              </div>
            </div>
            <div class="ecoser-servicios">
              <h4>Servicios</h4>
              <div class="servicios-grid">
                <div v-for="serv in ecoserServicios" :key="serv.nombre" class="servicio-item">
                  <ion-icon :name="serv.icono" class="serv-icon"></ion-icon>
                  <span>{{ serv.nombre }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- PRODUCCIÓN -->
    <section id="produccion" class="section">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">Actividades</span>
          <h2>Desarrollo Productivo</h2>
          <p>La base del sustento económico de las familias comuneras</p>
        </div>

        <div class="produccion-grid">
          <div class="prod-card">
            <div class="prod-header">
              <ion-icon name="leaf-outline" class="prod-icon"></ion-icon>
              <h3>Producción Agrícola</h3>
            </div>
            <div class="prod-items">
              <span v-for="p in agricola" :key="p" class="prod-tag">{{ p }}</span>
            </div>
          </div>
          <div class="prod-card">
            <div class="prod-header">
              <ion-icon name="paw-outline" class="prod-icon"></ion-icon>
              <h3>Producción Pecuaria</h3>
            </div>
            <div class="prod-items">
              <span v-for="p in pecuaria" :key="p" class="prod-tag">{{ p }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TRANSPARENCIA -->
    <section id="transparencia" class="section bg-light">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">Gestión abierta</span>
          <h2>Transparencia</h2>
          <p>Comprometidos con la rendición de cuentas a nuestros Usuarios</p>
        </div>
        <div class="transparencia-grid">
          <div v-for="doc in documentos" :key="doc.nombre" class="doc-card">
            <div class="doc-icon"><ion-icon :name="doc.icono"></ion-icon></div>
            <h4>{{ doc.nombre }}</h4>
          </div>
        </div>
      </div>
    </section>

    <!-- NOTICIAS -->
    <section id="noticias" class="section">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">Actualidad</span>
          <h2>Noticias y Comunicados</h2>
          <p>Mantente informado sobre las actividades de nuestra comunidad</p>
        </div>
        <div class="noticias-grid">
          <div v-for="noticia in noticias" :key="noticia.titulo" class="noticia-card">
            <div class="noticia-fecha">{{ noticia.fecha }}</div>
            <div class="noticia-tipo">{{ noticia.tipo }}</div>
            <h4>{{ noticia.titulo }}</h4>
            <p>{{ noticia.resumen }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CULTURA -->
    <section id="cultura" class="section bg-dark">
      <div class="container">
        <div class="section-header light">
          <span class="section-tag">Identidad</span>
          <h2>Cultura y Tradiciones</h2>
          <p>Expresiones que forman parte de nuestra identidad comunal</p>
        </div>
        <div class="cultura-grid">
          <div v-for="cult in cultura" :key="cult.titulo" class="cultura-card">
            <div class="cultura-icon"><ion-icon :name="cult.icono"></ion-icon></div>
            <h4>{{ cult.titulo }}</h4>
            <p>{{ cult.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CONVOCATORIAS -->
    <section id="convocatorias" class="section">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">Participa</span>
          <h2>Convocatorias y Oportunidades</h2>
          <p>Mantente al tanto de las actividades y oportunidades de la comunidad</p>
        </div>
        <div class="conv-grid">
          <div v-for="conv in convocatorias" :key="conv.tipo" class="conv-card">
            <div class="conv-icon"><ion-icon :name="conv.icono"></ion-icon></div>
            <h4>{{ conv.tipo }}</h4>
            <p>{{ conv.desc }}</p>
          </div>
        </div>
        <div class="conv-notice">
          <p><ion-icon name="megaphone-outline"></ion-icon> Para más información sobre convocatorias vigentes, contáctanos o visita nuestra sede.</p>
        </div>
      </div>
    </section>

    <!-- GALERÍA -->
    <section id="galeria" class="section bg-light">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">Imágenes</span>
          <h2>Galería</h2>
          <p>Paisajes, actividades y vida comunal</p>
        </div>
        <div class="galeria-grid">
          <div v-for="item in galeria" :key="item.label" class="galeria-item">
            <div class="galeria-placeholder"><ion-icon :name="item.icono"></ion-icon></div>
            <span>{{ item.label }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- CONTACTO -->
    <section id="contacto" class="section">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">Comunicación</span>
          <h2>Contacto</h2>
          <p>Estamos para atenderte</p>
        </div>
        <div class="contacto-grid">
          <div class="contacto-info">
            <div class="contacto-item">
              <ion-icon name="location-outline" class="contacto-icon"></ion-icon>
              <div>
                <strong>Dirección</strong>
                <p>Distrito de Torata, Provincia de Mariscal Nieto, Moquegua – Perú</p>
              </div>
            </div>
            <div class="contacto-item">
              <ion-icon name="call-outline" class="contacto-icon"></ion-icon>
              <div>
                <strong>Teléfono</strong>
                <p>Por definir</p>
              </div>
            </div>
            <div class="contacto-item">
              <ion-icon name="mail-outline" class="contacto-icon"></ion-icon>
              <div>
                <strong>Correo electrónico</strong>
                <p>comunidad.tpct@gmail.com</p>
              </div>
            </div>
            <div class="contacto-item">
              <ion-icon name="map-outline" class="contacto-icon"></ion-icon>
              <div>
                <strong>Ubicación</strong>
                <p>Valle de Tumilaca, Torata, Moquegua</p>
              </div>
            </div>
          </div>

          <form class="contacto-form" @submit.prevent="enviarContacto">
            <h3>Envíanos un mensaje</h3>
            <input v-model="form.nombre" type="text" placeholder="Tu nombre completo" required />
            <input v-model="form.email" type="email" placeholder="Tu correo electrónico" required />
            <input v-model="form.asunto" type="text" placeholder="Asunto" required />
            <textarea v-model="form.mensaje" placeholder="Tu mensaje..." rows="5" required></textarea>
            <button type="submit" class="btn-enviar">Enviar Mensaje</button>
          </form>
        </div>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="footer">
      <div class="container">
        <div class="footer-grid">
          <div class="footer-brand">
            <ion-icon name="leaf" class="footer-logo"></ion-icon>
            <h3>Comunidad Campesina TPCT</h3>
            <p>Tumilaca · Pocata · Coscore · Tala</p>
            <p class="footer-desc">Organización ancestral comprometida con el desarrollo sostenible y la defensa del territorio.</p>
          </div>
          <div class="footer-links">
            <h4>Navegación</h4>
            <a v-for="item in menuItems" :key="item.id" :href="`#${item.id}`" @click.prevent="scrollTo(item.id)">{{ item.label }}</a>
          </div>
          <div class="footer-links">
            <h4>Comunidad</h4>
            <a href="#">Actas Comunales</a>
            <a href="#">Comunicados</a>
            <a href="#">Empresa ECOSER</a>
            <a href="#" @click.prevent="irAdmin"><ion-icon name="lock-closed-outline"></ion-icon> Intranet</a>
          </div>
        </div>
        <div class="footer-bottom">
          <p>© {{ new Date().getFullYear() }} Comunidad Campesina de Tumilaca, Pocata, Coscore y Tala – Todos los derechos reservados</p>
        </div>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const emit = defineEmits(['ir-admin'])

const scrolled = ref(false)
const menuOpen = ref(false)

const form = ref({ nombre: '', email: '', asunto: '', mensaje: '' })

const menuItems = [
  { id: 'inicio', label: 'Inicio', header: true },
  { id: 'nosotros', label: 'Nosotros', header: false },
  { id: 'organizacion', label: 'Organización', header: false },
  { id: 'territorio', label: 'Territorio', header: false },
  { id: 'proyectos', label: 'Proyectos', header: true },
  { id: 'produccion', label: 'Producción', header: true },
  { id: 'noticias', label: 'Noticias', header: true },
  { id: 'cultura', label: 'Cultura', header: true },
  { id: 'contacto', label: 'Contacto', header: true },
]

const filteredHeaderItems = computed(() => menuItems.filter(item => item.header && item.id !== 'inicio'))

const valores = ['Transparencia', 'Solidaridad', 'Respeto', 'Trabajo colectivo', 'Identidad cultural', 'Defensa del territorio']

const juntaDirectiva = [
  { rol: 'Presidente', nombre: 'Marcos Santos García Nina' },
  { rol: 'Vicepresidente', nombre: 'Ramón Marca' },
  { rol: 'Secretario', nombre: 'Florentino Jesús Paripanca Ramos' },
  { rol: 'Tesorera', nombre: 'Lizet Yanira Coaila Gutierrez' },
  { rol: 'Fiscal', nombre: 'Máxima Concesa Cuaila Cuaila' },
  { rol: 'Vocal 1', nombre: 'Yonathan Michael Cabana Paripanca' },
  { rol: 'Vocal 2', nombre: 'Yasmin Miriam Flores Gutierrez' },
  { rol: 'Vocal 3', nombre: 'Tanislao Flores Copa' },
]

const anexos = ['Anexo Pocata', 'Anexo Coscore', 'Anexo Tala', 'Anexo Quebrada Honda']

const lineas = [
  { icono: 'leaf-outline', titulo: 'Desarrollo productivo' },
  { icono: 'construct-outline', titulo: 'Infraestructura comunal' },
  { icono: 'people-outline', titulo: 'Fortalecimiento organizacional' },
  { icono: 'briefcase-outline', titulo: 'Generación de empleo local' },
]

const ecoserObjetivos = [
  'Generar empleo local',
  'Brindar servicios a empresas públicas y privadas',
  'Fortalecer la economía comunal',
  'Promover la participación de los Usuarios',
]

const ecoserServicios = [
  { icono: 'car-outline', nombre: 'Alquiler de camionetas' },
  { icono: 'construct-outline', nombre: 'Provisión de mano de obra' },
  { icono: 'cube-outline', nombre: 'Apoyo logístico' },
  { icono: 'build-outline', nombre: 'Servicios diversos' },
]

const agricola = ['Fresas', 'Damasco', 'Palta', 'Manzana', 'Hortalizas']
const pecuaria = ['Caprinos', 'Producción de leche', 'Crianza de cuyes']

const documentos = [
  { icono: 'document-text-outline', nombre: 'Actas comunales' },
  { icono: 'megaphone-outline', nombre: 'Comunicados oficiales' },
  { icono: 'checkmark-done-outline', nombre: 'Acuerdos de asamblea' },
  { icono: 'folder-open-outline', nombre: 'Documentos institucionales' },
]

const noticias = [
  { fecha: 'Abril 2026', tipo: 'Asamblea', titulo: '77° Aniversario de la Comunidad Campesina TPCT', resumen: 'La comunidad celebra su 77° aniversario de fundación con actividades culturales y productivas.' },
  { fecha: 'Marzo 2026', tipo: 'Comunicado', titulo: 'Acuerdos de la Asamblea General Ordinaria', resumen: 'Se presentaron los acuerdos tomados en la última asamblea general de Usuarios.' },
  { fecha: 'Febrero 2026', tipo: 'Proyecto', titulo: 'Avances en el Proyecto de Infraestructura Comunal', resumen: 'Se informan los avances del proyecto de mejoramiento de infraestructura en los anexos.' },
]

const cultura = [
  { icono: 'calendar-outline', titulo: 'Festividades patronales', desc: 'Celebraciones tradicionales que reúnen a Usuarios y fortalecen los lazos comunitarios.' },
  { icono: 'people-outline', titulo: 'Actividades tradicionales', desc: 'Prácticas ancestrales transmitidas de generación en generación.' },
  { icono: 'restaurant-outline', titulo: 'Gastronomía local', desc: 'Sabores únicos del valle de Tumilaca con productos propios de la comunidad.' },
  { icono: 'leaf-outline', titulo: 'Prácticas agrícolas ancestrales', desc: 'Técnicas de cultivo tradicionales que conviven con métodos modernos.' },
]

const convocatorias = [
  { icono: 'briefcase-outline', tipo: 'Convocatorias laborales', desc: 'Oportunidades de empleo para Usuarios calificados en distintas áreas.' },
  { icono: 'business-outline', tipo: 'Asambleas comunales', desc: 'Reuniones ordinarias y extraordinarias donde participan todos los Usuarios.' },
  { icono: 'calendar-outline', tipo: 'Actividades y eventos', desc: 'Eventos culturales, deportivos y comunitarios programados.' },
  { icono: 'stats-chart-outline', tipo: 'Proyectos y gestiones', desc: 'Iniciativas de desarrollo en ejecución y convocatorias de participación.' },
]

const galeria = [
  { icono: 'mountain-outline', label: 'Paisajes' },
  { icono: 'people-outline', label: 'Actividades comunales' },
  { icono: 'balloon-outline', label: 'Festividades' },
  { icono: 'nutrition-outline', label: 'Producción agrícola' },
  { icono: 'home-outline', label: 'Infraestructura' },
  { icono: 'people-circle-outline', label: 'Organización' },
]

const scrollTo = (id) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}

const irAdmin = () => {
  emit('ir-admin')
}

const enviarContacto = () => {
  alert('Mensaje enviado. Nos comunicaremos contigo pronto.')
  form.value = { nombre: '', email: '', asunto: '', mensaje: '' }
}

const onScroll = () => {
  scrolled.value = window.scrollY > 60
}

onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
* { box-sizing: border-box; margin: 0; padding: 0; }

.web-publica {
  font-family: 'Segoe UI', system-ui, sans-serif;
  color: #1e293b;
  line-height: 1.6;
}

.web-publica ion-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
}

/* HEADER */
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: transparent;
  transition: all 0.3s;
}

.header.scrolled {
  background: rgba(15, 40, 20, 0.97);
  box-shadow: 0 2px 20px rgba(0,0,0,0.3);
}

.header-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.brand-logo {
  width: 44px;
  height: 44px;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-name {
  font-size: 15px;
  font-weight: 700;
  color: white;
  line-height: 1.2;
}

.brand-sub {
  font-size: 11px;
  color: rgba(255,255,255,0.7);
}

.nav-desktop {
  display: flex;
  gap: 4px;
  flex-wrap: nowrap;
}

.nav-link {
  padding: 8px 12px;
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  border-radius: 6px;
  transition: all 0.2s;
  white-space: nowrap;
}

.nav-link:hover {
  background: rgba(255,255,255,0.15);
  color: white;
}

/* Dropdown */
.nav-dropdown { position: relative; display: inline-block; }
.nav-drop-btn {
  display: flex; align-items: center; gap: 6px;
  padding: 8px 12px; color: rgba(255,255,255,0.85);
  background: none; border: none; font-size: 13px; font-weight: 500;
  cursor: pointer; font-family: inherit; border-radius: 6px;
  transition: all 0.2s;
}
.nav-drop-btn .chevron { font-size: 12px; transition: transform 0.2s; }
.nav-dropdown:hover .nav-drop-btn { background: rgba(255,255,255,0.15); color: white; }
.nav-dropdown:hover .chevron { transform: rotate(180deg); }

.nav-drop-content {
  position: absolute; top: 100%; left: 0; min-width: 200px;
  background: white; border: 1px solid #e2e8f0;
  border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  padding: 8px; display: flex; flex-direction: column; gap: 4px;
  opacity: 0; visibility: hidden; transform: translateY(10px);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.nav-dropdown:hover .nav-drop-content { opacity: 1; visibility: visible; transform: translateY(0); }

.drop-link {
  padding: 10px 16px; color: #1e293b;
  text-decoration: none; font-size: 14px; font-weight: 500;
  border-radius: 8px; transition: all 0.2s; text-align: left;
}
.drop-link:hover { background: #f1f5f9; color: #16a34a; }

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.btn-admin {
  padding: 8px 16px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  white-space: nowrap;
  transition: all 0.2s;
}

.btn-admin:hover {
  background: linear-gradient(135deg, #4338ca, #6d28d9);
  transform: translateY(-1px);
}

.hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
}

.hamburger span {
  display: block;
  width: 24px;
  height: 2px;
  background: white;
  border-radius: 2px;
}

.nav-mobile {
  display: none;
  flex-direction: column;
  background: rgba(15, 40, 20, 0.98);
  padding: 12px 24px;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.nav-mobile.open {
  max-height: 500px;
}

.nav-mobile-link {
  padding: 12px 0;
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  font-size: 15px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.nav-mobile-link.admin-link {
  color: #a78bfa;
  font-weight: 600;
}

.mobile-group { padding: 8px 0; background: rgba(0,0,0,0.2); }
.mobile-group-header {
  padding: 8px 24px; font-size: 11px; font-weight: 700;
  color: #4ade80; text-transform: uppercase; letter-spacing: 1px;
}
.nav-mobile-link.sub { padding-left: 44px; font-size: 14px; }

/* HERO */
.hero {
  min-height: 100vh;
  background: linear-gradient(160deg, #0f2814 0%, #1a4a22 40%, #2d6a35 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at center, transparent 0%, rgba(0,0,0,0.3) 100%);
}

.hero-content {
  position: relative;
  text-align: center;
  color: white;
  padding: 120px 24px 80px;
  max-width: 900px;
}

.hero-badge {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 100px;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 24px;
  backdrop-filter: blur(4px);
}

.hero-content h1 {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 20px;
  text-shadow: 0 2px 20px rgba(0,0,0,0.3);
}

.highlight {
  color: #86efac;
}

.hero-content p {
  font-size: clamp(1rem, 2vw, 1.25rem);
  color: rgba(255,255,255,0.8);
  margin-bottom: 40px;
}

.hero-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary-hero {
  padding: 14px 32px;
  background: #16a34a;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary-hero:hover {
  background: #15803d;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(22,163,74,0.4);
}

.btn-secondary-hero {
  padding: 14px 32px;
  background: rgba(255,255,255,0.15);
  color: white;
  border: 2px solid rgba(255,255,255,0.4);
  border-radius: 10px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  backdrop-filter: blur(4px);
  transition: all 0.2s;
}

.btn-secondary-hero:hover {
  background: rgba(255,255,255,0.25);
}

.hero-scroll {
  position: absolute;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  color: rgba(255,255,255,0.6);
  font-size: 24px;
  cursor: pointer;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(8px); }
}

/* STATS */
.stats-section {
  background: white;
  padding: 64px 0;
  border-bottom: 1px solid #e2e8f0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 32px;
  text-align: center;
}

.stat-item {}

.stat-number {
  font-size: 3rem;
  font-weight: 800;
  color: #16a34a;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  margin-top: 8px;
  font-weight: 500;
}

/* SECTIONS */
.section {
  padding: 96px 0;
}

.section.bg-light {
  background: #f8fafc;
}

.section.bg-dark {
  background: linear-gradient(160deg, #0f2814, #1a4a22);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-header.light h2,
.section-header.light p {
  color: white;
}

.section-tag {
  display: inline-block;
  padding: 4px 14px;
  background: white;
  color: #15803d;
  border: 1px solid #dcfce7;
  border-radius: 100px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 12px;
}

.section.bg-dark .section-tag {
  background: rgba(134, 239, 172, 0.15);
  color: #86efac;
}

.section-header h2 {
  font-size: clamp(1.8rem, 3vw, 2.5rem);
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 12px;
}

.section-header p {
  font-size: 16px;
  color: #64748b;
  max-width: 600px;
  margin: 0 auto;
}

/* NOSOTROS */
.nosotros-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.historia-card, .mv-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  border: 1px solid #e2e8f0;
}

.historia-card {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.valores-col {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.mv-card {
  padding: 24px;
}

.card-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.historia-card h3, .mv-card h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 12px;
}

.valores-lista {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.valor-tag {
  padding: 6px 14px;
  background: white;
  color: #15803d;
  border: 1px solid #dcfce7;
  border-radius: 100px;
  font-size: 13px;
  font-weight: 600;
}

/* ORGANIZACIÓN */
.org-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 24px;
}

.org-card {
  background: white;
  border-radius: 16px;
  padding: 28px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  border: 1px solid #e2e8f0;
}

.org-card.principal {
  border-top: 4px solid #16a34a;
}

.org-header {
  margin-bottom: 20px;
}

.org-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
}

.directiva-lista {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.directivo-item {
  display: flex;
  flex-direction: column;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
  border-left: 3px solid #16a34a;
}

.cargo-rol {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  color: #16a34a;
  letter-spacing: 0.5px;
}

.cargo-nombre {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-top: 2px;
}

.comision-desc {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 16px;
  line-height: 1.5;
}

.comision-lista {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.comision-lista li {
  padding: 8px 12px;
  background: #f8fafc;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
  border-left: 3px solid #4f46e5;
}

.anexos-lista {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.anexo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
}

.anexo-nombre {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.anexo-status {
  font-size: 11px;
  color: #64748b;
  background: #e2e8f0;
  padding: 2px 8px;
  border-radius: 100px;
}

/* TERRITORIO */
.territorio-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: start;
}

.territorio-text {
  display: flex;
  flex-direction: column;
  gap: 16px;
  font-size: 15px;
  color: #475569;
  line-height: 1.7;
}

.entorno-box {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.entorno-box h4 {
  font-size: 16px;
  font-weight: 700;
  color: #15803d;
  margin-bottom: 12px;
}

.entorno-box p {
  color: #374151;
  margin-bottom: 8px;
}

.territorio-mapa {
  display: flex;
  justify-content: center;
}

.mapa-placeholder {
  background: white;
  border: 2px dashed #e2e8f0;
  border-radius: 20px;
  padding: 60px 40px;
  text-align: center;
  width: 100%;
}

.mapa-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.mapa-placeholder h4 {
  font-size: 20px;
  font-weight: 700;
  color: #15803d;
  margin-bottom: 4px;
}

.mapa-placeholder p {
  color: #64748b;
  margin-bottom: 20px;
}

.anexos-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.chip {
  padding: 6px 16px;
  background: white;
  border: 1px solid #86efac;
  border-radius: 100px;
  font-size: 13px;
  font-weight: 600;
  color: #15803d;
}

/* PROYECTOS */
.lineas-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.linea-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.linea-icon {
  width: 60px;
  height: 60px;
  background: white;
  color: #16a34a;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin: 0 auto 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.linea-card h4 {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.ecoser-card {
  background: white;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

.ecoser-header {
  background: linear-gradient(135deg, #0f2814, #1a4a22);
  padding: 24px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.ecoser-logo {
  font-size: 24px;
  font-weight: 800;
  color: #86efac;
}

.ecoser-tag {
  padding: 4px 14px;
  background: rgba(134, 239, 172, 0.2);
  color: #86efac;
  border-radius: 100px;
  font-size: 12px;
  font-weight: 600;
}

.ecoser-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
}

.ecoser-desc {
  padding: 32px;
  border-right: 1px solid #e2e8f0;
}

.ecoser-desc h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 12px;
}

.ecoser-desc p {
  color: #64748b;
  margin-bottom: 20px;
  line-height: 1.6;
}

.ecoser-objetivos {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.obj-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 14px;
  color: #374151;
}

.obj-check {
  color: #16a34a;
  font-weight: 700;
  flex-shrink: 0;
}

.ecoser-servicios {
  padding: 32px;
}

.ecoser-servicios h4 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 20px;
}

.servicios-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.servicio-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 8px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
  color: #1e293b;
}

.serv-icon {
  width: 48px;
  height: 48px;
  background: white;
  color: #16a34a;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

/* PRODUCCIÓN */
.produccion-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.prod-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.prod-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.prod-icon {
  width: 64px;
  height: 64px;
  background: white;
  color: #16a34a;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
}

.prod-header h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
}

.prod-items {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.prod-tag {
  padding: 8px 18px;
  background: white;
  color: #15803d;
  border-radius: 100px;
  font-size: 14px;
  font-weight: 600;
  border: 1px solid #e2e8f0;
}

/* TRANSPARENCIA */
.transparencia-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.doc-card {
  background: white;
  border-radius: 16px;
  padding: 32px 24px;
  text-align: center;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  transition: all 0.2s;
}

.doc-card:hover {
  border-color: #86efac;
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(22,163,74,0.1);
}

.doc-icon {
  width: 72px;
  height: 72px;
  background: white;
  color: #16a34a;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  margin: 0 auto 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.doc-card h4 {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
}

/* NOTICIAS */
.noticias-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.noticia-card {
  background: white;
  border-radius: 16px;
  padding: 28px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  transition: all 0.2s;
}

.noticia-card:hover {
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}

.noticia-fecha {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 500;
  margin-bottom: 6px;
}

.noticia-tipo {
  display: inline-block;
  padding: 3px 10px;
  background: white;
  color: #15803d;
  border: 1px solid #dcfce7;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 700;
  margin-bottom: 12px;
}

.noticia-card h4 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 10px;
  line-height: 1.4;
}

.noticia-card p {
  font-size: 14px;
  color: #64748b;
  line-height: 1.6;
}

/* CULTURA */
.cultura-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.cultura-card {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 16px;
  padding: 32px 24px;
  text-align: center;
}

.cultura-icon {
  width: 72px;
  height: 72px;
  background: white;
  color: #4ade80;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  margin: 0 auto 20px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}

.cultura-card h4 {
  font-size: 16px;
  font-weight: 700;
  color: white;
  margin-bottom: 10px;
}

.cultura-card p {
  font-size: 13px;
  color: rgba(255,255,255,0.7);
  line-height: 1.6;
}

/* CONVOCATORIAS */
.conv-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.conv-card {
  background: white;
  border-radius: 16px;
  padding: 28px 24px;
  text-align: center;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.conv-icon {
  width: 64px;
  height: 64px;
  background: white;
  color: #16a34a;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin: 0 auto 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.conv-card h4 {
  font-size: 15px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.conv-card p {
  font-size: 13px;
  color: #64748b;
  line-height: 1.5;
}

.conv-notice {
  text-align: center;
  background: #eff6ff;
  border-radius: 12px;
  padding: 20px;
  color: #1e40af;
  font-size: 14px;
  font-weight: 500;
}

/* GALERÍA */
.galeria-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
}

.galeria-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.galeria-placeholder {
  width: 100%;
  aspect-ratio: 1;
  background: linear-gradient(135deg, #e2e8f0, #f1f5f9);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  border: 2px dashed #cbd5e1;
  transition: all 0.2s;
}

.galeria-placeholder:hover {
  border-color: #86efac;
  background: linear-gradient(135deg, #f0fdf4, #dcfce7);
}

.galeria-item span {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}

/* CONTACTO */
.contacto-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: start;
}

.contacto-info {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.contacto-item {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.contacto-icon {
  font-size: 24px;
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  background: white;
  color: #16a34a;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.contacto-item strong {
  display: block;
  font-size: 14px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.contacto-item p {
  font-size: 14px;
  color: #64748b;
}

.contacto-form {
  background: white;
  border-radius: 20px;
  padding: 36px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.contacto-form h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.contacto-form input,
.contacto-form textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  font-family: inherit;
  color: #1e293b;
  outline: none;
  transition: border-color 0.2s;
}

.contacto-form input:focus,
.contacto-form textarea:focus {
  border-color: #16a34a;
  box-shadow: 0 0 0 3px rgba(22,163,74,0.1);
}

.btn-enviar {
  padding: 14px;
  background: linear-gradient(135deg, #16a34a, #15803d);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-enviar:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(22,163,74,0.4);
}

/* FOOTER */
.footer {
  background: #0f2814;
  color: white;
  padding: 64px 0 0;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 48px;
  padding-bottom: 48px;
}

.footer-logo {
  font-size: 40px;
  display: block;
  margin-bottom: 12px;
}

.footer-brand h3 {
  font-size: 18px;
  font-weight: 700;
  color: #86efac;
  margin-bottom: 4px;
}

.footer-brand p {
  font-size: 14px;
  color: rgba(255,255,255,0.6);
  margin-bottom: 4px;
}

.footer-desc {
  margin-top: 12px;
  font-size: 13px;
  line-height: 1.6;
  color: rgba(255,255,255,0.5);
}

.footer-links {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.footer-links h4 {
  font-size: 13px;
  font-weight: 700;
  color: #86efac;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 8px;
}

.footer-links a {
  font-size: 14px;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  transition: color 0.2s;
}

.footer-links a:hover {
  color: white;
}

.footer-bottom {
  border-top: 1px solid rgba(255,255,255,0.1);
  padding: 24px 0;
  text-align: center;
}

.footer-bottom p {
  font-size: 13px;
  color: rgba(255,255,255,0.4);
}

/* RESPONSIVE */
@media (max-width: 1024px) {
  .nav-desktop { display: none; }
  .hamburger { display: flex; }
  .nav-mobile { display: flex; }
  .org-grid { grid-template-columns: 1fr; }
  .lineas-grid { grid-template-columns: repeat(2, 1fr); }
  .transparencia-grid { grid-template-columns: repeat(2, 1fr); }
  .cultura-grid { grid-template-columns: repeat(2, 1fr); }
  .conv-grid { grid-template-columns: repeat(2, 1fr); }
  .galeria-grid { grid-template-columns: repeat(3, 1fr); }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .footer-grid { grid-template-columns: 1fr 1fr; }
  .ecoser-grid { grid-template-columns: 1fr; }
  .ecoser-desc { border-right: none; border-bottom: 1px solid #e2e8f0; }
}

@media (max-width: 768px) {
  .section { padding: 64px 0; }
  .nosotros-grid { grid-template-columns: 1fr; }
  .territorio-grid { grid-template-columns: 1fr; }
  .produccion-grid { grid-template-columns: 1fr; }
  .noticias-grid { grid-template-columns: 1fr; }
  .contacto-grid { grid-template-columns: 1fr; }
  .servicios-grid { grid-template-columns: 1fr 1fr; }
  .btn-admin { display: none; }
  .footer-grid { grid-template-columns: 1fr; }
}

@media (max-width: 480px) {
  .galeria-grid { grid-template-columns: repeat(2, 1fr); }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
