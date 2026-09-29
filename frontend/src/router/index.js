import { createRouter, createWebHistory } from 'vue-router'
import authService from '../services/auth.service'

// Views del dashboard (admin)
import DashboardHome from '../components/dashboard/DashboardHome.vue'
import UsuariosView from '../components/dashboard/UsuariosView.vue'
import ConfiguracionView from '../components/dashboard/ConfiguracionView.vue'
import MarcaView from '../components/dashboard/MarcaView.vue'
import ReportesView from '../components/dashboard/ReportesView.vue'
import IntegracionesView from '../components/dashboard/IntegracionesView.vue'
import CobranzaView from '../components/dashboard/CobranzaView.vue'
import ConfiguracionCobranzaView from '../components/dashboard/ConfiguracionCobranzaView.vue'
import OperacionesView from '../components/dashboard/OperacionesView.vue'
import EleccionesView from '../components/dashboard/EleccionesView.vue'
import EleccionDetalleView from '../components/dashboard/EleccionDetalleView.vue'
import VotacionView from '../components/dashboard/VotacionView.vue'
import CarnetsView from '../components/dashboard/CarnetsView.vue'
import ReunionesView from '../components/dashboard/ReunionesView.vue'
import UsuarioPerfilView from '../components/dashboard/UsuarioPerfilView.vue'
import GaleriaView from '../components/dashboard/GaleriaView.vue'
// Vista exclusiva para rol usuario
import UsuarioPanelView from '../components/dashboard/UsuarioPanelView.vue'

const esAdmin = () => {
  const u = authService.obtenerUsuario()
  return u?.rol === 'admin' || u?.rol === 'editor' || u?.rol === 'moderator'
}

const routes = [
  {
    path: '/',
    redirect: () => esAdmin() ? '/dashboard' : '/mi-panel',
  },
  // ── Ruta panel usuario comunero ──────────────────────────────
  {
    path: '/mi-panel',
    name: 'mi-panel',
    component: UsuarioPanelView,
    meta: { requiresAuth: true, soloUsuario: true },
  },
  {
    path: '/votacion',
    name: 'votacion',
    component: VotacionView,
    meta: { requiresAuth: true },
  },
  // ── Rutas exclusivas admin ───────────────────────────────────
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardHome,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/usuarios',
    name: 'usuarios',
    component: UsuariosView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/usuarios/:id',
    name: 'usuario-perfil',
    component: UsuarioPerfilView,
    props: true,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/configuracion',
    name: 'configuracion',
    component: ConfiguracionView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/configuracion/marca',
    name: 'marca',
    component: MarcaView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/reportes',
    name: 'reportes',
    component: ReportesView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/integraciones',
    name: 'integraciones',
    component: IntegracionesView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/cobranza',
    name: 'cobranza',
    component: CobranzaView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/config-cobranza',
    name: 'config-cobranza',
    component: ConfiguracionCobranzaView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/operaciones',
    name: 'operaciones',
    component: OperacionesView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/elecciones',
    name: 'elecciones',
    component: EleccionesView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/elecciones/:id',
    name: 'eleccion-detalle',
    component: EleccionDetalleView,
    props: true,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/reuniones',
    name: 'reuniones',
    component: ReunionesView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/carnets',
    name: 'carnets',
    component: CarnetsView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/galerias',
    name: 'galerias',
    component: GaleriaView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  // Comodín
  {
    path: '/:pathMatch(.*)*',
    redirect: () => esAdmin() ? '/dashboard' : '/mi-panel',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !authService.estaAutenticado()) {
    return false
  }
  // Ruta solo para admin: si es usuario comunero, redirige a su panel
  if (to.meta.requiresAdmin && !esAdmin()) {
    return '/mi-panel'
  }
  // Ruta solo para usuario: si es admin, redirige al dashboard
  if (to.meta.soloUsuario && esAdmin()) {
    return '/dashboard'
  }
})

export default router
