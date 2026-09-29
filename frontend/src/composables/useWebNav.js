import { ref } from 'vue'

const PAGINAS_VALIDAS = [
  'inicio', 'nosotros', 'organizacion', 'territorio',
  'proyectos', 'produccion', 'noticias', 'galeria', 'contacto',
  'asamblea-mayo-2026',
  'convocatoria-extraordinaria'
]

function paginaDesdeUrl() {
  const path = (window.location.pathname || '/').replace(/^\/+|\/+$/g, '')
  if (!path) return 'inicio'
  return PAGINAS_VALIDAS.includes(path) ? path : 'inicio'
}

const pagina = ref(paginaDesdeUrl())
const irAdmin = ref(null)

// Sincronizar al usar back/forward del navegador
if (typeof window !== 'undefined') {
  window.addEventListener('popstate', () => {
    pagina.value = paginaDesdeUrl()
  })
}

export function useWebNav() {
  function navegar(p) {
    pagina.value = p
    const path = p === 'inicio' ? '/' : `/${p}`
    if (window.location.pathname !== path) {
      window.history.pushState({}, '', path)
    }
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  function setIrAdmin(fn) {
    irAdmin.value = fn
  }

  function goAdmin() {
    if (irAdmin.value) irAdmin.value()
  }

  return { pagina, navegar, goAdmin, setIrAdmin }
}
