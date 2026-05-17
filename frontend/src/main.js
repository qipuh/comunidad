import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { setMarca } from './composables/useMarca'

async function initializeApp() {
  try {
    // Cargar configuración de marca
    const response = await fetch('/api/admin/configuracion/marca')
    if (response.ok) {
      const marca = await response.json()
      setMarca(marca)

      // Actualizar document.title
      document.title = marca.nombre_pagina

      // Actualizar favicon
      if (marca.favicon_url) {
        const link = document.querySelector('link[rel="icon"]')
        if (link) {
          link.href = marca.favicon_url
        }
      }

      // Guardar en window para acceso global
      window.__MARCA__ = marca
    }
  } catch (error) {
    console.error('Error cargando configuración de marca:', error)
  }

  // Montar aplicación
  const app = createApp(App)
  app.use(router)
  app.mount('#app')
}

initializeApp()
