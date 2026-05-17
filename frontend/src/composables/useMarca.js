import { reactive } from 'vue'

const marca = reactive({
  nombre_pagina: 'Comunidad',
  subtitulo: 'Sistema de Gestión',
  nombre_corto: 'COM',
  logo_url: null,
  favicon_url: null,
  color_primario: '#4f46e5'
})

export function useMarca() {
  return marca
}

export function setMarca(data) {
  Object.assign(marca, data)
}
