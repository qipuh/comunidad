# Frontend - Comunidad

Vue.js 3 + Vite frontend para el sistema de gestión comunitaria.

## Inicio Rápido

### Windows
```bash
run.bat
```

### Unix/macOS
```bash
bash run.sh
```

### Manual
```bash
npm install
npm run dev
```

El servidor de desarrollo estará en: **http://localhost:5173**

## Características

- ✅ Vue.js 3 Composition API
- ✅ Vite (bundler rápido)
- ✅ Componentes dinámicos ya creados
- ✅ Integración con backend API (http://localhost:8000)
- ✅ Hot reload habilitado
- ✅ Proxy para API requests

## Estructura

```
src/
├── main.js              - Punto de entrada
├── App.vue              - Componente raíz
├── components/
│   ├── RegistroDinamico.vue      - Formulario dinámico
│   └── admin/
│       ├── ConfiguradorCampos.vue - Gestión de campos
│       └── ConfiguradorAPIs.vue   - Gestión de APIs
└── services/
    ├── validaciones.service.ts    - API calls para validaciones
    └── configuracion.service.ts   - API calls para configuración
```

## Scripts

```bash
# Desarrollo
npm run dev

# Build para producción
npm run build

# Preview de build
npm run preview
```

## Conectar al Backend

El frontend se conecta automáticamente al backend en **http://localhost:8000**.

El archivo `vite.config.js` configura un proxy para las requests a `/api`:
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true
  }
}
```

Entonces puedes hacer requests a:
```javascript
// En lugar de: http://localhost:8000/api/validaciones/consultar-dni
fetch('/api/validaciones/consultar-dni')
```

## Componentes Disponibles

### RegistroDinamico.vue
Formulario que se genera dinámicamente basado en la configuración del backend.
- Valida campos en cliente
- Auto-completa campos desde APIs
- Muestra barra de progreso
- Envía datos al backend

### ConfiguradorCampos.vue
Interfaz para administradores para gestionar campos dinámicos.
- CRUD de campos
- Modal para formularios
- Validación en tiempo real

### ConfiguradorAPIs.vue
Interfaz para administradores para gestionar integraciones API.
- CRUD de APIs externas
- Test de conexión
- Gestión de credenciales

## Servicios API

### validaciones.service.ts
```javascript
import { consultarDNI, consultarRUC } from './services/validaciones.service'

// Consultar DNI
const resultado = await consultarDNI('12345678')

// Consultar RUC
const resultado = await consultarRUC('12345678901')
```

### configuracion.service.ts
```javascript
import { obtenerCampos, crearCampo, obtenerAPIs } from './services/configuracion.service'

// Obtener campos
const campos = await obtenerCampos()

// Crear campo
await crearCampo({
  nombre_campo: 'documento',
  tipo_dato: 'string',
  es_obligatorio: true
})

// Obtener APIs
const apis = await obtenerAPIs()
```

## Desarrollo

### Agregar nuevos componentes
1. Crea archivo en `src/components/`
2. Importa en `App.vue`
3. Usa en template

### Agregar nuevos servicios
1. Crea archivo en `src/services/`
2. Exporta funciones que hacen fetch
3. Importa en componentes que lo necesiten

### Debugging
- Abre DevTools: F12 (Chrome/Firefox)
- Usa Vue DevTools extension
- Checkea console para errores

## Troubleshooting

### "Cannot GET /"
- Asegúrate de que npm run dev está corriendo
- Verifica que estés en puerto 5173

### "CORS error"
- Verifica que backend está en puerto 8000
- Checkea que CORS está habilitado en backend

### Components no carga
- Verifica que imports están correctos
- Checkea console para errores

## Dependencias

- **vue@^3.4.0** - Framework
- **axios@^1.6.0** - HTTP client (si lo necesitas)
- **vite@^5.0.0** - Bundler
- **@vitejs/plugin-vue** - Plugin para Vite

## Próximos Pasos

1. Edita componentes en `src/components/`
2. Modifica App.vue para agregar más vistas
3. Agrega nuevos servicios en `src/services/`
4. Build para producción: `npm run build`

## Documentación

Ver documentación principal: [../INICIO_RAPIDO.md](../INICIO_RAPIDO.md)
