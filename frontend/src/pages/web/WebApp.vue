<template>
  <component :is="componentes[pagina] || componentes.inicio" />
</template>

<script setup>
import { useWebNav } from '../../composables/useWebNav'
import Inicio       from './Inicio.vue'
import Nosotros     from './Nosotros.vue'
import Organizacion from './Organizacion.vue'
import Territorio   from './Territorio.vue'
import Proyectos    from './Proyectos.vue'
import Produccion   from './Produccion.vue'
import Noticias     from './Noticias.vue'
import Galeria      from './Galeria.vue'
import Contacto     from './Contacto.vue'

const { pagina } = useWebNav()

const componentes = {
  inicio: Inicio,
  nosotros: Nosotros,
  organizacion: Organizacion,
  territorio: Territorio,
  proyectos: Proyectos,
  produccion: Produccion,
  noticias: Noticias,
  galeria: Galeria,
  contacto: Contacto,
}
</script>
