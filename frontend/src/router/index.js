import { createRouter, createWebHashHistory } from 'vue-router'
import authService from '../services/auth.service'

// Views del dashboard
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

const routes = [
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardHome,
    meta: { requiresAuth: true },
  },
  {
    path: '/usuarios',
    name: 'usuarios',
    component: UsuariosView,
    meta: { requiresAuth: true },
  },
  {
    path: '/usuarios/:id',
    name: 'usuario-perfil',
    component: UsuarioPerfilView,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/configuracion',
    name: 'configuracion',
    component: ConfiguracionView,
    meta: { requiresAuth: true },
  },
  {
    path: '/configuracion/marca',
    name: 'marca',
    component: MarcaView,
    meta: { requiresAuth: true },
  },
  {
    path: '/reportes',
    name: 'reportes',
    component: ReportesView,
    meta: { requiresAuth: true },
  },
  {
    path: '/integraciones',
    name: 'integraciones',
    component: IntegracionesView,
    meta: { requiresAuth: true },
  },
  {
    path: '/cobranza',
    name: 'cobranza',
    component: CobranzaView,
    meta: { requiresAuth: true },
  },
  {
    path: '/config-cobranza',
    name: 'config-cobranza',
    component: ConfiguracionCobranzaView,
    meta: { requiresAuth: true },
  },
  {
    path: '/operaciones',
    name: 'operaciones',
    component: OperacionesView,
    meta: { requiresAuth: true },
  },
  {
    path: '/elecciones',
    name: 'elecciones',
    component: EleccionesView,
    meta: { requiresAuth: true },
  },
  {
    path: '/elecciones/:id',
    name: 'eleccion-detalle',
    component: EleccionDetalleView,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/votacion',
    name: 'votacion',
    component: VotacionView,
    meta: { requiresAuth: true },
  },
  {
    path: '/reuniones',
    name: 'reuniones',
    component: ReunionesView,
    meta: { requiresAuth: true },
  },
  {
    path: '/carnets',
    name: 'carnets',
    component: CarnetsView,
    meta: { requiresAuth: true },
  },
  // Ruta comodín → redirige al dashboard
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard',
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

// Guard global: si la ruta requiere auth y no está autenticado, redirige a '/'
// El login lo controla App.vue con v-if, así que simplemente dejamos pasar
// (App.vue ya muestra Login si no está autenticado)
router.beforeEach((to) => {
  if (to.meta.requiresAuth && !authService.estaAutenticado()) {
    // No hay ruta de login separada; App.vue gestiona el v-if
    return false
  }
})

export default router
