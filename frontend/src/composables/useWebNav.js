import { ref } from 'vue'

const pagina = ref('inicio')
const irAdmin = ref(null)

export function useWebNav() {
  function navegar(p) {
    pagina.value = p
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
