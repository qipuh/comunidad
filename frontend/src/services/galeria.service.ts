/**
 * Servicio para la gestión de Galerías (Álbumes) y Fotografías.
 * Soporta API y sincronización reactiva en LocalStorage.
 */
import api from './api'
import { getFromDB, saveToDB, optimizarImagen } from './dbStorage'

export interface FotoItem {
  id: number | string
  galeria_id?: number | string
  titulo: string
  desc: string
  img: string
  grande: boolean
  orden: number
  activo: boolean
}

export interface GaleriaItem {
  id: number | string
  titulo: string
  slug: string
  descripcion: string
  categoria: string
  categoriaLabel: string
  portada: string
  fecha: string
  lugar: string
  destacada: boolean
  orden: number
  activo: boolean
  totalFotos?: number
  fotos: FotoItem[]
}

export interface CategoriaItem {
  key: string
  label: string
}

const STORAGE_KEY = 'comunidad_galerias_colecciones_v2'

export const GALERIAS_POR_DEFECTO: GaleriaItem[] = [
  {
    id: 1,
    titulo: 'Identidad y Tradición Comunal',
    slug: 'identidad-y-tradicion-comunal',
    descripcion: 'Vivencias, costumbres, vestimentas típicas y la rica herencia cultural de nuestra comunidad.',
    categoria: 'comunidad',
    categoriaLabel: 'Comunidad',
    portada: '/uploads/img/web/2.png',
    fecha: '2026',
    lugar: 'Cerro Baúl / Moquegua',
    destacada: true,
    orden: 1,
    activo: true,
    fotos: [
      {
        id: 101,
        galeria_id: 1,
        titulo: 'Identidad comunal',
        desc: 'Mujeres de la comunidad con vestimenta tradicional frente al Cerro Baúl, símbolo del territorio.',
        grande: true,
        img: '/uploads/img/web/2.png',
        orden: 1,
        activo: true
      },
      {
        id: 102,
        galeria_id: 1,
        titulo: 'Anexo Tumilaca',
        desc: 'Vista del anexo de Tumilaca, corazón productivo del valle.',
        grande: false,
        img: '/uploads/img/nosotros/tumilala.png',
        orden: 2,
        activo: true
      },
      {
        id: 103,
        galeria_id: 1,
        titulo: 'Tumilaca en acción',
        desc: 'Actividades cotidianas de los Usuarios en el anexo de Tumilaca.',
        grande: false,
        img: '/uploads/img/nosotros/tumilala2.png',
        orden: 3,
        activo: true
      },
      {
        id: 104,
        galeria_id: 1,
        titulo: 'Plaza de Moquegua',
        desc: 'Centro histórico de la ciudad de Moquegua, capital de la región.',
        grande: false,
        img: '/uploads/img/web/1.jpeg',
        orden: 4,
        activo: true
      }
    ]
  },
  {
    id: 2,
    titulo: 'Territorio y Paisajes Ancestrales',
    slug: 'territorio-y-paisajes-ancestrales',
    descripcion: 'Panorámicas de nuestros cerros tutelares, valles agrícolas, cementerios históricos y fauna andina.',
    categoria: 'territorio',
    categoriaLabel: 'Territorio',
    portada: '/uploads/img/inicio/cerro_baul.png',
    fecha: '2026',
    lugar: 'Distrito de Torata',
    destacada: true,
    orden: 2,
    activo: true,
    fotos: [
      {
        id: 201,
        galeria_id: 2,
        titulo: 'Cerro Baúl',
        desc: 'Hito arqueológico y cultural emblemático del territorio comunal.',
        grande: true,
        img: '/uploads/img/inicio/cerro_baul.png',
        orden: 1,
        activo: true
      },
      {
        id: 202,
        galeria_id: 2,
        titulo: 'Cementerio de Pocata',
        desc: 'Cementerio comunal histórico del anexo Pocata.',
        grande: false,
        img: '/uploads/img/inicio/cementerio_pocata.png',
        orden: 2,
        activo: true
      },
      {
        id: 203,
        galeria_id: 2,
        titulo: 'Vista del valle',
        desc: 'Panorámica del territorio comunal en el distrito de Torata.',
        grande: false,
        img: '/uploads/img/inicio/01.png',
        orden: 3,
        activo: true
      },
      {
        id: 204,
        galeria_id: 2,
        titulo: 'Fauna andina',
        desc: 'Llama andina, parte del patrimonio ganadero del altiplano comunal.',
        grande: false,
        img: '/uploads/img/web/4.jpeg',
        orden: 4,
        activo: true
      }
    ]
  },
  {
    id: 3,
    titulo: 'Trabajo Agrícola y ECOSER',
    slug: 'trabajo-agricola-y-ecoser',
    descripcion: 'Labores del campo y los servicios empresariales que brinda nuestra empresa comunal ECOSER.',
    categoria: 'actividades',
    categoriaLabel: 'Actividades',
    portada: '/uploads/img/web/3.jpeg',
    fecha: '2026',
    lugar: 'Valle y Operaciones',
    destacada: false,
    orden: 3,
    activo: true,
    fotos: [
      {
        id: 301,
        galeria_id: 3,
        titulo: 'Trabajo agrícola',
        desc: 'Producción agrícola en el valle, sustento de las familias comuneras.',
        grande: true,
        img: '/uploads/img/web/3.jpeg',
        orden: 1,
        activo: true
      },
      {
        id: 302,
        galeria_id: 3,
        titulo: 'ECOSER en operaciones',
        desc: 'Trabajos de la empresa comunal ECOSER en el territorio.',
        grande: false,
        img: '/uploads/img/ecoser/01.png',
        orden: 2,
        activo: true
      },
      {
        id: 303,
        galeria_id: 3,
        titulo: 'Equipo ECOSER',
        desc: 'Mano de obra local capacitada para servicios diversos.',
        grande: false,
        img: '/uploads/img/ecoser/02.png',
        orden: 3,
        activo: true
      },
      {
        id: 304,
        galeria_id: 3,
        titulo: 'Servicios al territorio',
        desc: 'ECOSER brindando servicios a la comunidad y empresas de la zona.',
        grande: false,
        img: '/uploads/img/ecoser/03.png',
        orden: 4,
        activo: true
      }
    ]
  }
]

export const CATEGORIAS_PREDEFINIDAS: CategoriaItem[] = [
  { key: 'comunidad', label: 'Comunidad' },
  { key: 'territorio', label: 'Territorio' },
  { key: 'actividades', label: 'Actividades' },
  { key: 'asambleas', label: 'Asambleas y Eventos' },
  { key: 'faenas', label: 'Faenas Comunales' },
  { key: 'patrimonio', label: 'Patrimonio y Cultura' },
  { key: 'proyectos', label: 'Proyectos y Obras' }
]

let cacheGalerias: GaleriaItem[] | null = null

/**
 * Obtiene las galerías locales garantizando carga desde IndexedDB (sin límites de 5MB)
 */
export async function getLocalGaleriasAsync(): Promise<GaleriaItem[]> {
  if (cacheGalerias && Array.isArray(cacheGalerias) && cacheGalerias.length > 0) {
    return cacheGalerias
  }

  // 1. Prioridad: Leer de IndexedDB
  try {
    const dbData = await getFromDB<GaleriaItem[]>(STORAGE_KEY)
    if (dbData && Array.isArray(dbData) && dbData.length > 0) {
      cacheGalerias = dbData
      try { localStorage.removeItem(STORAGE_KEY) } catch {}
      return dbData
    }
  } catch (err) {
    console.warn('Error leyendo galerías desde IndexedDB:', err)
  }

  // 2. Si IndexedDB está vacío, intentar migrar desde localStorage
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const parsed = JSON.parse(raw)
      if (Array.isArray(parsed) && parsed.length > 0) {
        cacheGalerias = parsed
        await saveToDB(STORAGE_KEY, parsed)
        try { localStorage.removeItem(STORAGE_KEY) } catch {}
        return parsed
      }
    }
  } catch (e) {
    console.warn('Error migrando localStorage:', e)
  }

  // 3. Si no hay datos previos, inicializar con las galerías por defecto
  const inicial = JSON.parse(JSON.stringify(GALERIAS_POR_DEFECTO))
  cacheGalerias = inicial
  await saveToDB(STORAGE_KEY, inicial)
  try { localStorage.removeItem(STORAGE_KEY) } catch {}
  return inicial
}

function getLocalGalerias(): GaleriaItem[] {
  if (cacheGalerias && Array.isArray(cacheGalerias) && cacheGalerias.length > 0) {
    return cacheGalerias
  }
  return JSON.parse(JSON.stringify(GALERIAS_POR_DEFECTO))
}

async function setLocalGalerias(galerias: GaleriaItem[]): Promise<void> {
  cacheGalerias = galerias

  // 1. Guardar en IndexedDB (soporta gigabytes sin cuota de 5MB)
  await saveToDB(STORAGE_KEY, galerias)

  // 2. Limpiar localStorage para nunca saturar los 5MB de cuota del navegador
  try {
    localStorage.removeItem(STORAGE_KEY)
  } catch {}

  window.dispatchEvent(new CustomEvent('comunidad-galerias-actualizadas', { detail: galerias }))
}

// Inicializar en segundo plano
if (typeof window !== 'undefined') {
  getLocalGaleriasAsync().then(data => {
    window.dispatchEvent(new CustomEvent('comunidad-galerias-actualizadas', { detail: data }))
  }).catch(() => {})
}

export const galeriaService = {
  /**
   * Obtiene la lista de galerías (álbumes) para la web pública
   */
  async obtenerPublico(categoria?: string): Promise<{ galerias: GaleriaItem[]; filtros: CategoriaItem[] }> {
    try {
      const params = categoria && categoria !== 'todas' ? { categoria } : {}
      const res = await api.get('/galeria/publico', { params })
      if (res.data?.success && Array.isArray(res.data?.galerias)) {
        return {
          galerias: res.data.galerias,
          filtros: res.data.filtros || []
        }
      }
    } catch {
      // Fallback
    }

    const todas = await getLocalGaleriasAsync()
    const activas = todas
      .filter(g => g.activo !== false)
      .sort((a, b) => (a.orden || 0) - (b.orden || 0))

    const filtradas = (!categoria || categoria === 'todas')
      ? activas
      : activas.filter(g => g.categoria === categoria)

    const catMap = new Map<string, string>()
    todas.forEach(g => {
      if (g.categoria && !catMap.has(g.categoria)) {
        catMap.set(g.categoria, g.categoriaLabel || g.categoria)
      }
    })

    const filtros: CategoriaItem[] = [{ key: 'todas', label: 'Todas' }]
    catMap.forEach((label, key) => filtros.push({ key, label }))

    return {
      galerias: filtradas.map(g => ({
        ...g,
        totalFotos: (g.fotos || []).filter(f => f.activo !== false).length,
        portada: g.portada || (g.fotos && g.fotos[0]?.img) || '/uploads/img/web/2.png'
      })),
      filtros
    }
  },

  /**
   * Obtiene el detalle de una galería con sus fotos para la web
   */
  async obtenerGaleriaDetalle(idOrSlug: string | number): Promise<{ galeria: GaleriaItem; fotos: FotoItem[] } | null> {
    try {
      const res = await api.get(`/galeria/detalle/${idOrSlug}`)
      if (res.data?.success && res.data?.galeria) {
        return {
          galeria: res.data.galeria,
          fotos: res.data.fotos || []
        }
      }
    } catch {
      // Fallback
    }

    const todas = await getLocalGaleriasAsync()
    const found = todas.find(g => String(g.id) === String(idOrSlug) || g.slug === String(idOrSlug))
    if (!found) return null

    const fotosActivas = (found.fotos || [])
      .filter(f => f.activo !== false)
      .sort((a, b) => (a.orden || 0) - (b.orden || 0))

    return {
      galeria: found,
      fotos: fotosActivas
    }
  },

  /**
   * Obtiene todas las galerías completas para el panel de administración
   */
  async obtenerAdmin(): Promise<GaleriaItem[]> {
    try {
      const res = await api.get('/galeria/admin/todas')
      if (res.data?.success && Array.isArray(res.data?.galerias)) {
        await setLocalGalerias(res.data.galerias)
        return res.data.galerias
      }
    } catch {
      // Fallback
    }
    return await getLocalGaleriasAsync()
  },

  /**
   * Crea una nueva Galería (Álbum)
   */
  async crearGaleria(datos: Partial<GaleriaItem>): Promise<GaleriaItem> {
    const localList = await getLocalGaleriasAsync()
    const nuevoId = Date.now()
    const maxOrden = localList.reduce((max, g) => Math.max(max, g.orden || 0), 0)

    const nueva: GaleriaItem = {
      id: nuevoId,
      titulo: datos.titulo || 'Nueva Galería',
      slug: (datos.titulo || 'galeria').toLowerCase().replace(/\s+/g, '-'),
      descripcion: datos.descripcion || '',
      categoria: datos.categoria || 'comunidad',
      categoriaLabel: datos.categoriaLabel || 'Comunidad',
      portada: datos.portada || '',
      fecha: datos.fecha || '',
      lugar: datos.lugar || '',
      destacada: !!datos.destacada,
      orden: datos.orden || (maxOrden + 1),
      activo: datos.activo !== undefined ? datos.activo : true,
      totalFotos: 0,
      fotos: []
    }

    try {
      const res = await api.post('/galeria/admin/galeria', {
        titulo: nueva.titulo,
        descripcion: nueva.descripcion,
        categoria: nueva.categoria,
        categoria_label: nueva.categoriaLabel,
        portada: nueva.portada,
        fecha: nueva.fecha,
        lugar: nueva.lugar,
        destacada: nueva.destacada,
        orden: nueva.orden,
        activo: nueva.activo
      })
      if (res.data?.success && res.data?.galeria) {
        nueva.id = res.data.galeria.id
      }
    } catch {
      // Fallback
    }

    localList.push(nueva)
    await setLocalGalerias(localList)
    return nueva
  },

  /**
   * Actualiza los datos de una Galería
   */
  async actualizarGaleria(id: string | number, cambios: Partial<GaleriaItem>): Promise<GaleriaItem> {
    const localList = await getLocalGaleriasAsync()
    const idx = localList.findIndex(g => String(g.id) === String(id))
    if (idx === -1) throw new Error('Galería no encontrada')

    const actual = localList[idx]
    const actualizada = { ...actual, ...cambios }

    try {
      await api.put(`/galeria/admin/galeria/${id}`, {
        titulo: actualizada.titulo,
        descripcion: actualizada.descripcion,
        categoria: actualizada.categoria,
        categoria_label: actualizada.categoriaLabel,
        portada: actualizada.portada,
        fecha: actualizada.fecha,
        lugar: actualizada.lugar,
        destacada: actualizada.destacada,
        orden: actualizada.orden,
        activo: actualizada.activo
      })
    } catch {
      // Fallback
    }

    localList[idx] = actualizada
    await setLocalGalerias(localList)
    return actualizada
  },

  /**
   * Elimina una Galería y todas sus fotos
   */
  async eliminarGaleria(id: string | number): Promise<boolean> {
    try {
      await api.delete(`/galeria/admin/galeria/${id}`)
    } catch {
      // Fallback
    }

    const localList = await getLocalGaleriasAsync()
    const filtradas = localList.filter(g => String(g.id) !== String(id))
    await setLocalGalerias(filtradas)
    return true
  },

  /**
   * Agrega una foto a una galería específica
   */
  async agregarFoto(galeriaId: string | number, fotoData: Partial<FotoItem>): Promise<FotoItem> {
    const localList = await getLocalGaleriasAsync()
    const galeria = localList.find(g => String(g.id) === String(galeriaId))
    if (!galeria) throw new Error('Galería no encontrada')

    if (!galeria.fotos) galeria.fotos = []
    const nuevoFotoId = Date.now()
    const maxOrden = galeria.fotos.reduce((max, f) => Math.max(max, f.orden || 0), 0)

    const nuevaFoto: FotoItem = {
      id: nuevoFotoId,
      galeria_id: galeriaId,
      titulo: fotoData.titulo || 'Fotografía',
      desc: fotoData.desc || '',
      img: fotoData.img || '',
      grande: !!fotoData.grande,
      orden: fotoData.orden || (maxOrden + 1),
      activo: fotoData.activo !== undefined ? fotoData.activo : true
    }

    try {
      const res = await api.post('/galeria/admin/fotos', {
        galeria_id: Number(galeriaId),
        titulo: nuevaFoto.titulo,
        desc: nuevaFoto.desc,
        img: nuevaFoto.img,
        grande: nuevaFoto.grande,
        orden: nuevaFoto.orden,
        activo: nuevaFoto.activo
      })
      if (res.data?.success && res.data?.foto) {
        nuevaFoto.id = res.data.foto.id
      }
    } catch {
      // Fallback
    }

    galeria.fotos.push(nuevaFoto)
    if (!galeria.portada) {
      galeria.portada = nuevaFoto.img
    }

    await setLocalGalerias(localList)
    return nuevaFoto
  },

  /**
   * Actualiza una foto dentro de una galería
   */
  async actualizarFoto(fotoId: string | number, cambios: Partial<FotoItem>): Promise<FotoItem> {
    const localList = await getLocalGaleriasAsync()
    let fotoActualizada: FotoItem | null = null

    for (const g of localList) {
      if (g.fotos) {
        const fIdx = g.fotos.findIndex(f => String(f.id) === String(fotoId))
        if (fIdx !== -1) {
          g.fotos[fIdx] = { ...g.fotos[fIdx], ...cambios }
          fotoActualizada = g.fotos[fIdx]
          break
        }
      }
    }

    if (!fotoActualizada) throw new Error('Foto no encontrada')

    try {
      await api.put(`/galeria/admin/fotos/${fotoId}`, {
        titulo: fotoActualizada.titulo,
        desc: fotoActualizada.desc,
        img: fotoActualizada.img,
        grande: fotoActualizada.grande,
        orden: fotoActualizada.orden,
        activo: fotoActualizada.activo
      })
    } catch {
      // Fallback
    }

    await setLocalGalerias(localList)
    return fotoActualizada
  },

  /**
   * Elimina una foto de una galería
   */
  async eliminarFoto(fotoId: string | number): Promise<boolean> {
    try {
      await api.delete(`/galeria/admin/fotos/${fotoId}`)
    } catch {
      // Fallback
    }

    const localList = await getLocalGaleriasAsync()
    for (const g of localList) {
      if (g.fotos) {
        g.fotos = g.fotos.filter(f => String(f.id) !== String(fotoId))
      }
    }

    await setLocalGalerias(localList)
    return true
  },

  /**
   * Sube una imagen optimizada
   */
  async subirImagen(file: File): Promise<string> {
    try {
      const formData = new FormData()
      formData.append('file', file)
      const res = await api.post('/galeria/admin/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      if (res.data?.success && res.data?.url) {
        return res.data.url
      }
    } catch {
      // Fallback
    }

    // Comprime y optimiza la imagen localmente para almacenamiento masivo
    return await optimizarImagen(file, 1400, 0.8)
  },

  /**
   * Obtiene todas las fotos activas de todas las galerías activas
   */
  async obtenerTodasLasFotos(): Promise<FotoItem[]> {
    const { galerias } = await this.obtenerPublico()
    const todas: FotoItem[] = []
    galerias.forEach(g => {
      if (g.fotos && Array.isArray(g.fotos)) {
        g.fotos.forEach(f => {
          if (f.activo !== false) {
            todas.push({
              ...f,
              categoria: g.categoria,
              categoriaLabel: g.categoriaLabel || g.titulo
            })
          }
        })
      }
    })
    return todas
  },

  /**
   * Sube múltiples fotos en lote a una galería
   */
  async subirMultiplesFotos(
    galeriaId: string | number,
    files: File[],
    onProgress?: (actual: number, total: number) => void
  ): Promise<FotoItem[]> {
    const total = files.length
    const fotosAgregadas: FotoItem[] = []

    // 1. Intentar endpoint batch si está disponible
    try {
      const formData = new FormData()
      files.forEach(f => formData.append('files', f))
      const res = await api.post(`/galeria/admin/fotos/batch?galeria_id=${galeriaId}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      if (res.data?.success) {
        const adminGalerias = await this.obtenerAdmin()
        const g = adminGalerias.find(item => String(item.id) === String(galeriaId))
        return g?.fotos || []
      }
    } catch {
      // Fallback a almacenamiento local masivo
    }

    // 2. Cargar la lista completa actualizada desde IndexedDB
    const localList = await getLocalGaleriasAsync()
    const galeria = localList.find(g => String(g.id) === String(galeriaId))
    if (!galeria) throw new Error('Galería no encontrada')

    if (!galeria.fotos) galeria.fotos = []
    let maxOrden = galeria.fotos.reduce((max, f) => Math.max(max, f.orden || 0), 0)

    // 3. Procesar y optimizar cada imagen
    for (let i = 0; i < files.length; i++) {
      const file = files[i]
      if (onProgress) onProgress(i + 1, total)

      try {
        const url = await this.subirImagen(file)
        const nombreBase = file.name.substring(0, file.name.lastIndexOf('.')) || file.name
        const tituloLimpio = nombreBase.replace(/[_-]+/g, ' ').trim() || `Fotografía ${galeria.fotos.length + 1}`
        maxOrden++

        const nueva: FotoItem = {
          id: Date.now() + i,
          galeria_id: galeriaId,
          titulo: tituloLimpio,
          desc: '',
          img: url,
          grande: false,
          orden: maxOrden,
          activo: true
        }

        galeria.fotos.push(nueva)
        if (!galeria.portada) {
          galeria.portada = nueva.img
        }
        fotosAgregadas.push(nueva)
      } catch (err) {
        console.error('Error procesando archivo:', file.name, err)
      }
    }

    // 4. Guardar TODO el conjunto en IndexedDB de UNA SOLA VEZ
    await setLocalGalerias(localList)

    return fotosAgregadas
  },

  /**
   * Restablece galerías por defecto
   */
  async restablecerPorDefecto(): Promise<GaleriaItem[]> {
    try {
      await api.post('/galeria/admin/restablecer-defaults')
    } catch {
      // Fallback
    }

    const inicial = JSON.parse(JSON.stringify(GALERIAS_POR_DEFECTO))
    await setLocalGalerias(inicial)
    return inicial
  }
}
