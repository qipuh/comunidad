# Guía de Importación Masiva de Usuarios

## 📋 Nueva Estructura de Importación

La importación de usuarios ahora soporta la siguiente estructura en Excel:

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `num_padron` | Texto | No | Número de padrón (identificador) |
| `apellido_paterno` | Texto | **Sí** | Apellido paterno |
| `apellido_materno` | Texto | **Sí** | Apellido materno |
| `nombres` | Texto | **Sí** | Nombres del usuario |
| `sexo` | Texto | No | M/F o Masculino/Femenino |
| `dni` | Texto | **Sí** | DNI de 8 dígitos (solo números) |
| `fecha_nacimiento` | Fecha | No | Formato DD/MM/YYYY o YYYY-MM-DD |
| `estado_civil` | Texto | No | Estado civil del usuario |

## 🚀 Pasos para Importar

### 1. Descargar Plantilla
- En la pantalla de Usuarios, haz clic en el botón **"Plantilla"**
- Se descargará un archivo Excel con:
  - Pestaña "Usuarios": Estructura con ejemplos
  - Pestaña "Instrucciones": Guía completa

### 2. Completar Datos
- Abre la plantilla en Excel
- Completa los datos siguiendo la estructura
- Asegúrate de que:
  - El DNI tiene exactamente 8 dígitos
  - El DNI es único (sin duplicados en el archivo)
  - Los campos obligatorios estén rellenados

### 3. Subir Archivo
- En Usuarios, haz clic en **"Importar"**
- Selecciona tu archivo Excel (.xlsx o .xls)

### 4. Revisar Previsualización

La aplicación mostrará una vista previa con:

**📊 Filtros disponibles:**
- **Todos** (📋): Todas las filas
- **Nuevos** (✅): Usuarios que se crearán
- **Actualizar** (⚠️): DNI existentes que se actualizarán
- **Errores** (❌): Filas con problemas

**Tabla con información completa:**
- Padrón, nombres, DNI, sexo, fecha nacimiento, estado civil
- Estado de cada fila
- Tooltip con descripción de errores

### 5. Seleccionar Usuarios
- Usa el checkbox en cada fila
- O usa "Seleccionar/deseleccionar todos"
- El contador muestra cuántas filas están seleccionadas

### 6. Confirmar Importación
- Haz clic en **"Importar"**
- Se abrirá un modal de confirmación mostrando:
  - Cantidad de usuarios nuevos a crear
  - Cantidad de usuarios a actualizar
- Confirma la operación

### 7. Resultado
- La aplicación mostrará:
  - ✅ Usuarios creados exitosamente
  - ↻ Usuarios actualizados
  - ❌ Errores (si los hay)

## ⚙️ Comportamiento Especial

### Usuarios Duplicados (DNI ya existe)

Cuando un DNI ya existe en el sistema:

1. Aparecerá como **"Actualizar"** (⚠️) en la previsualización
2. Puedes seleccionarlo para actualizar sus datos
3. Si lo importas, se actualizarán estos campos:
   - Nombres
   - Apellidos
   - Sexo
   - Fecha de nacimiento
   - Estado civil
   - Número de padrón

**Importante**: No se cambian:
- Contraseña
- Email
- Username
- Rol
- Estado (activo/inactivo)
- Fotos

### Creación de Nuevos Usuarios

Para usuarios nuevos (DNI no existe):

- Se crean con:
  - **Contraseña**: El mismo DNI (ejemplo: 12345678)
  - **Username**: El DNI
  - **Email**: DNI@comunidad.local
  - **Rol**: Usuario (se puede cambiar después)
  - **Estado**: Activo
  - **Reconocimiento facial**: Desactivado (se puede activar después)

## 🔍 Validaciones

El sistema valida automáticamente:

✅ **DNI válido**: 8 dígitos numéricos
✅ **Nombres no vacío**: Nombres obligatorios
✅ **Sexo**: M/F/Masculino/Femenino (si está presente)
✅ **Fechas**: Formato correcto (YYYY-MM-DD)
❌ **Duplicados**: DNI que ya existen (marcados para actualizar)

## 📝 Ejemplo de Archivo

```xlsx
num_padron | apellido_paterno | apellido_materno | nombres | sexo | dni      | fecha_nacimiento | estado_civil
-----------|------------------|------------------|---------|------|----------|------------------|-------------
P001       | García           | López            | Juan    | M    | 12345678 | 1990-01-15       | Soltero
P002       | Pérez            | Rodríguez        | María   | F    | 87654321 | 1988-06-20       | Casada
P003       | López            | Martínez         | Carlos  | M    | 11223344 | 1995-03-10       | Soltero
```

## 🛠️ Troubleshooting

**Error: DNI debe tener 8 dígitos**
- Verifica que el DNI tenga exactamente 8 números
- Sin guiones, espacios ni letras

**Error: DNI debe ser solo números**
- Asegúrate de que el campo solo contiene dígitos

**Error: Nombres vacío**
- El campo de nombres es obligatorio
- Completa todos los nombres

**Sexo inválido**
- Solo acepta: M, F, Masculino, Femenino
- Respeta mayúsculas/minúsculas

**Archivo no se carga**
- El archivo debe ser .xlsx o .xls
- No puede estar abierto en Excel
- Guárdalo primero

## 💡 Consejos

1. **Antes de importar**: Descarga la plantilla y úsala como base
2. **Verifica datos**: Revisa bien la previsualización antes de confirmar
3. **Bachés pequeños**: Si tienes muchos usuarios, importa en lotes
4. **Actualizar después**: Algunos campos (rol, estado) se pueden cambiar después si es necesario
5. **Contraseñas**: Los usuarios reciben DNI como contraseña inicial - recuérdales cambiarla

## 🔐 Seguridad

- ✅ El sistema valida todos los datos antes de importar
- ✅ No hay cambios en el servidor hasta que confirmes
- ✅ Puedes revisar exactamente qué se hará en la previsualización
- ✅ Los datos se protegen con el token de autenticación

---

**¿Preguntas?** Contacta al administrador del sistema.
