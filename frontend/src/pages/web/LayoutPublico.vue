<template>
  <div class="site">

    <!-- HEADER -->
    <header class="header" :class="{ scrolled }">
      <div class="header-inner">
        <button class="brand" @click="nav('inicio')">
          <div class="brand-logo">
            <img :src="'/uploads/logo/logo.png'" alt="Logo" class="logo-img" />
          </div>
          <div class="brand-text">
            <span class="brand-name">Comunidad TPCT</span>
            <span class="brand-sub">Torata · Moquegua · Perú</span>
          </div>
        </button>

        <nav class="nav-desktop">
          <button class="nav-link" :class="{ active: pagina === 'inicio' }" @click="nav('inicio')">
            INICIO
          </button>

          <div class="nav-dropdown">
            <button class="nav-drop-btn">
              QUIÉNES SOMOS
              <ion-icon name="chevron-down-outline" class="chevron"></ion-icon>
            </button>
            <div class="nav-drop-content">
              <button class="drop-link" :class="{ active: pagina === 'nosotros' }"     @click="nav('nosotros')">NOSOTROS</button>
              <button class="drop-link" :class="{ active: pagina === 'organizacion' }" @click="nav('organizacion')">ORGANIZACIÓN</button>
              <button class="drop-link" :class="{ active: pagina === 'territorio' }"   @click="nav('territorio')">TERRITORIO</button>
            </div>
          </div>

          <button v-for="item in headerMenu" :key="item.key" class="nav-link" :class="{ active: pagina === item.key }" @click="nav(item.key)">
            {{ item.label }}
          </button>
        </nav>

        <div class="header-right">
          <button class="btn-admin" @click="goAdmin()">
            INTRANET
          </button>
          <button class="hamburger" @click="mobileOpen = !mobileOpen" aria-label="Menú">
            <ion-icon :name="mobileOpen ? 'close' : 'menu'"></ion-icon>
          </button>
        </div>
      </div>

      <!-- Mobile nav -->
      <div class="nav-mobile" :class="{ open: mobileOpen }">
        <button class="mobile-link" @click="nav('inicio')">INICIO</button>
        <div class="mobile-group">
          <div class="mobile-group-header">QUIÉNES SOMOS</div>
          <button class="mobile-link sub" @click="nav('nosotros')">NOSOTROS</button>
          <button class="mobile-link sub" @click="nav('organizacion')">ORGANIZACIÓN</button>
          <button class="mobile-link sub" @click="nav('territorio')">TERRITORIO</button>
        </div>
        <button v-for="item in headerMenu" :key="item.key" class="mobile-link" @click="nav(item.key)">
          {{ item.label }}
        </button>
        <button class="mobile-link admin-mobile" @click="goAdmin()">
          INTRANET
        </button>
      </div>
    </header>

    <!-- PAGE CONTENT -->
    <main><slot /></main>

    <!-- FOOTER -->
    <footer class="footer">
      <div class="container">
        <div class="footer-grid">
          <div class="footer-brand">
            <div class="footer-logo"><ion-icon name="leaf"></ion-icon></div>
            <h3>Comunidad Campesina TPCT</h3>
            <p>Tumilaca · Pocata · Coscore · Tala</p>
            <p class="footer-desc">Organización ancestral comprometida con el desarrollo sostenible y la defensa del territorio comunal.</p>
            <div class="footer-social">
              <a href="#" class="social-btn"><ion-icon name="logo-facebook"></ion-icon></a>
              <a href="#" class="social-btn"><ion-icon name="logo-whatsapp"></ion-icon></a>
              <a href="#" class="social-btn"><ion-icon name="mail-outline"></ion-icon></a>
            </div>
          </div>
          <div class="footer-nav">
            <h4>Páginas</h4>
            <button v-for="item in allMenu" :key="item.key" @click="nav(item.key)">{{ item.label }}</button>
          </div>
          <div class="footer-nav">
            <h4>Comunidad</h4>
            <a href="#">Actas Comunales</a>
            <a href="#">Empresa ECOSER</a>
            <a href="#">Convocatorias</a>
            <button @click="goAdmin()">Intranet</button>
          </div>
          <div class="footer-contact">
            <h4>Contacto</h4>
            <div class="fc-item"><ion-icon name="location-outline"></ion-icon><span>Distrito de Torata, Moquegua – Perú</span></div>
            <div class="fc-item"><ion-icon name="mail-outline"></ion-icon><span>---</span></div>
            <div class="fc-item"><ion-icon name="earth-outline"></ion-icon><span>https://comunidadcampesinatpct.com</span></div>
          </div>
        </div>
        <div class="footer-bottom">
          <p>© {{ year }} Comunidad Campesina de Tumilaca, Pocata, Coscore y Tala – Todos los derechos reservados</p>
        </div>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useWebNav } from '../../composables/useWebNav'

const { pagina, navegar, goAdmin } = useWebNav()
const scrolled = ref(false)
const mobileOpen = ref(false)
const year = new Date().getFullYear()

const allMenu = [
  { key: 'inicio',       label: 'Inicio',       icon: 'home-outline' },
  { key: 'nosotros',     label: 'Nosotros',     icon: 'people-outline' },
  { key: 'organizacion', label: 'Organización', icon: 'business-outline' },
  { key: 'territorio',   label: 'Territorio',   icon: 'map-outline' },
  { key: 'proyectos',    label: 'Proyectos',    icon: 'construct-outline' },
  { key: 'produccion',   label: 'Producción',   icon: 'leaf-outline' },
  { key: 'noticias',     label: 'Noticias',     icon: 'newspaper-outline' },
  { key: 'galeria',      label: 'Galería',      icon: 'images-outline' },
  { key: 'contacto',     label: 'Contacto',     icon: 'call-outline' },
]

const headerMenu = [
  { key: 'proyectos',  label: 'PROYECTOS',  icon: 'construct-outline' },
  { key: 'produccion', label: 'PRODUCCIÓN', icon: 'leaf-outline' },
  { key: 'noticias',   label: 'NOTICIAS',   icon: 'newspaper-outline' },
  { key: 'galeria',    label: 'GALERÍA',    icon: 'images-outline' },
  { key: 'contacto',   label: 'CONTACTO',   icon: 'call-outline' },
]

function nav(p) {
  navegar(p)
  mobileOpen.value = false
}

const onScroll = () => { scrolled.value = window.scrollY > 50 }
onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.site { display: flex; flex-direction: column; min-height: 100vh; }
main { flex: 1; }

.header {
  position: fixed; top: 0; left: 0; right: 0; z-index: 999;
  background: rgba(10,30,12,0.0); transition: all 0.35s ease;
  border-bottom: 1px solid transparent;
}
.header.scrolled {
  background: rgba(10,30,12,0.97);
  border-bottom-color: rgba(255,255,255,0.08);
  box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}
.header-inner {
  max-width: 1280px; margin: 0 auto;
  padding: 0 24px; height: 70px;
  display: flex; align-items: center; gap: 16px;
}
.brand {
  display: flex; align-items: center; gap: 10px;
  background: none; border: none; cursor: pointer; flex-shrink: 0;
}
.brand-logo {
  width: 42px; height: 42px;
  background: transparent;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
}
.logo-img {
  width: 100%; height: 100%; object-fit: contain;
}
.brand-text { display: flex; flex-direction: column; text-align: left; }
.brand-name { font-size: 15px; font-weight: 700; color: white; line-height: 1.2; }
.brand-sub  { font-size: 11px; color: rgba(255,255,255,0.6); }

.nav-desktop { flex: 1; display: flex; gap: 2px; justify-content: center; }
.nav-link {
  display: flex; align-items: center; gap: 5px;
  padding: 8px 14px; border-radius: 7px; border: none; background: none;
  color: rgba(255,255,255,0.8); font-size: 12px; font-weight: 600;
  white-space: nowrap; cursor: pointer; transition: all 0.2s; font-family: 'Inter', inherit;
  text-transform: uppercase; letter-spacing: 0.5px;
}
.nav-link:hover, .nav-link.active { background: rgba(255,255,255,0.14); color: #fff; }

.nav-dropdown { position: relative; }
.nav-drop-btn {
  display: flex; align-items: center; gap: 5px;
  padding: 7px 11px; border: none; background: none;
  color: rgba(255,255,255,0.8); cursor: pointer;
  font-size: 13px; font-weight: 500; font-family: inherit;
  transition: all 0.2s; border-radius: 7px;
}
.nav-drop-btn .chevron { font-size: 12px; transition: transform 0.2s; }
.nav-dropdown:hover .nav-drop-btn { background: rgba(255,255,255,0.1); color: white; }
.nav-dropdown:hover .chevron { transform: rotate(180deg); }
.nav-drop-content {
  position: absolute; top: 100%; left: 0; min-width: 200px;
  background: white; border: 1px solid #e2e8f0;
  border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  padding: 8px; display: flex; flex-direction: column; gap: 4px;
  opacity: 0; visibility: hidden; transform: translateY(10px);
  transition: all 0.2s cubic-bezier(0.16,1,0.3,1);
}
.nav-dropdown:hover .nav-drop-content { opacity: 1; visibility: visible; transform: translateY(0); }
.drop-link {
  padding: 10px 16px; color: #1e293b; text-align: left;
  background: none; border: none; font-size: 14px; font-weight: 500;
  border-radius: 8px; cursor: pointer; transition: all 0.2s; font-family: inherit; width: 100%;
}
.drop-link:hover, .drop-link.active { background: #f1f5f9; color: #16a34a; }

.header-right { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
.btn-admin {
  display: flex; align-items: center; gap: 6px; padding: 8px 16px;
  background: linear-gradient(135deg,#4f46e5,#7c3aed); color: white;
  border: none; border-radius: 8px; font-size: 13px; font-weight: 600;
  white-space: nowrap; cursor: pointer; transition: all 0.2s; font-family: inherit;
}
.btn-admin:hover { opacity: 0.9; transform: translateY(-1px); }
.btn-admin ion-icon { font-size: 15px; }
.hamburger {
  display: none; background: none; border: none;
  color: white; font-size: 26px; cursor: pointer; padding: 4px;
}

.nav-mobile {
  display: none; flex-direction: column; background: rgba(10,30,12,0.98);
  overflow: hidden; max-height: 0; transition: max-height 0.35s ease;
  border-top: 1px solid rgba(255,255,255,0.08);
}
.nav-mobile.open { max-height: 600px; }
.mobile-link {
  display: flex; align-items: center; gap: 12px; padding: 14px 24px;
  color: rgba(255,255,255,0.8); background: none; border: none;
  font-size: 15px; border-bottom: 1px solid rgba(255,255,255,0.05);
  cursor: pointer; transition: background 0.2s; font-family: inherit; text-align: left;
}
.mobile-link ion-icon { font-size: 20px; }
.mobile-link:hover { background: rgba(255,255,255,0.08); color: white; }
.mobile-group { padding: 10px 0; background: rgba(0,0,0,0.1); }
.mobile-group-header { padding: 8px 24px; font-size: 11px; font-weight: 700; color: #86efac; text-transform: uppercase; letter-spacing: 1px; }
.mobile-link.sub { padding-left: 48px; font-size: 14px; }
.admin-mobile { color: #a78bfa; }

/* FOOTER */
.footer { background: #0a1e0c; color: white; padding: 72px 0 0; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1.5fr; gap: 48px; padding-bottom: 48px; }
.footer-logo { width: 52px; height: 52px; background: linear-gradient(135deg,#16a34a,#15803d); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 28px; color: white; margin-bottom: 16px; }
.footer-brand h3 { font-size: 17px; font-weight: 700; color: #86efac; margin-bottom: 4px; }
.footer-brand > p { font-size: 13px; color: rgba(255,255,255,0.5); margin-bottom: 2px; }
.footer-desc { font-size: 13px; color: rgba(255,255,255,0.4); line-height: 1.7; margin-top: 12px; }
.footer-social { display: flex; gap: 10px; margin-top: 16px; }
.social-btn { width: 36px; height: 36px; background: rgba(255,255,255,0.08); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: rgba(255,255,255,0.7); font-size: 18px; text-decoration: none; transition: all 0.2s; }
.social-btn:hover { background: #16a34a; color: white; }
.footer-nav { display: flex; flex-direction: column; gap: 8px; }
.footer-nav h4 { font-size: 12px; font-weight: 700; color: #86efac; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
.footer-nav a, .footer-nav button { font-size: 14px; color: rgba(255,255,255,0.55); text-decoration: none; background: none; border: none; cursor: pointer; text-align: left; font-family: inherit; padding: 0; transition: color 0.2s; }
.footer-nav a:hover, .footer-nav button:hover { color: white; }
.footer-contact { display: flex; flex-direction: column; gap: 14px; }
.footer-contact h4 { font-size: 12px; font-weight: 700; color: #86efac; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
.fc-item { display: flex; align-items: flex-start; gap: 10px; font-size: 13px; color: rgba(255,255,255,0.55); }
.fc-item ion-icon { font-size: 16px; flex-shrink: 0; margin-top: 1px; color: #86efac; }
.footer-bottom { border-top: 1px solid rgba(255,255,255,0.08); padding: 24px 0; text-align: center; }
.footer-bottom p { font-size: 12px; color: rgba(255,255,255,0.3); }

@media (max-width: 1024px) {
  .nav-desktop { display: none; }
  .hamburger { display: flex; }
  .nav-mobile { display: flex; }
  .footer-grid { grid-template-columns: 1fr 1fr; gap: 32px; }
}
@media (max-width: 600px) {
  .btn-admin span { display: none; }
  .footer-grid { grid-template-columns: 1fr; }
}
</style>
