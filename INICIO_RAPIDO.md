# 🚀 INICIO RÁPIDO - Backend + Frontend

**Tu desarrollo está listo para empezar. Sigue estos pasos.**

---

## 📋 Paso 1: Iniciar Backend (2 minutos)

### Windows:
```bash
cd backend
run.bat
```

### macOS/Linux:
```bash
cd backend
bash run.sh
```

### Resultado esperado:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

✅ **Backend está corriendo en http://localhost:8000**

---

## 📋 Paso 2: Iniciar Frontend (2 minutos)

### En otra terminal:
```bash
cd frontend
npm install  # Primera vez solo
npm run dev
```

### Resultado esperado:
```
VITE v4.x.x  ready in 123 ms

➜  Local:   http://localhost:5173/
```

✅ **Frontend está corriendo en http://localhost:5173**

---

## 🧪 Paso 3: Verificar que Funciona

### Opción A: cURL
```bash
curl http://localhost:8000/api/health
# Resultado: {"status": "healthy", ...}
```

### Opción B: Swagger UI
Abre en navegador:
```
http://localhost:8000/docs
```

### Opción C: ReDoc
```
http://localhost:8000/redoc
```

---

## 🎯 Ahora Tienes:

**Backend:**
- ✅ FastAPI en puerto 8000
- ✅ Base de datos SQLite lista
- ✅ 12+ endpoints REST disponibles
- ✅ Documentación automática (Swagger)
- ✅ Health check: http://localhost:8000/api/health

**Frontend:**
- ✅ Vue.js en puerto 5173
- ✅ Conectado a backend automáticamente
- ✅ Hot reload habilitado
- ✅ Componentes dinámicos listos

---

## 📡 Endpoints Principales

### Para Usuarios (sin autenticación)
```bash
# Consultar DNI
curl -X POST http://localhost:8000/api/validaciones/consultar-dni \
     -H "Content-Type: application/json" \
     -d '{"dni": "12345678"}'

# Consultar RUC
curl -X POST http://localhost:8000/api/validaciones/consultar-ruc \
     -H "Content-Type: application/json" \
     -d '{"ruc": "12345678901"}'

# Verificar disponibilidad RENIEC
curl http://localhost:8000/api/validaciones/probar-reniec

# Verificar disponibilidad Facturiza
curl http://localhost:8000/api/validaciones/probar-facturiza
```

### Para Administrador (con token)
```bash
# Listar campos configurables
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8000/api/admin/configuracion/campos

# Listar integraciones API
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8000/api/admin/integraciones-api

# Crear campo dinámico
curl -X POST http://localhost:8000/api/admin/configuracion/campos \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "nombre_campo": "documento_identidad",
       "etiqueta": "DNI",
       "tipo_dato": "string",
       "es_obligatorio": true
     }'
```

---

## 📂 Documentación de Referencia

| Necesito... | Abre |
|-----------|------|
| Guía completa backend | [BACKEND_SETUP.md](BACKEND_SETUP.md) |
| Estado actual del backend | [ESTADO_BACKEND.md](ESTADO_BACKEND.md) |
| Todos los endpoints | [ENDPOINTS_EJEMPLOS.md](ENDPOINTS_EJEMPLOS.md) |
| Modelos de datos | [MODELOS_DATOS.md](MODELOS_DATOS.md) |
| Arquitectura del sistema | [ARQUITECTURA.md](ARQUITECTURA.md) |
| Cómo personalizar campos | [CAMPOS_PERSONALIZADOS.md](CAMPOS_PERSONALIZADOS.md) |
| Componentes Vue listos | [COMPONENTES_DINAMICOS.md](COMPONENTES_DINAMICOS.md) |
| Guía de transición | [GUIA_TRANSICION_DINAMICA.md](GUIA_TRANSICION_DINAMICA.md) |

---

## 🧪 Ejecutar Tests

### Suite de Tests Completa (Python)
```bash
cd backend
python test_api.py
```

### Tests con Docker
```bash
docker-compose -f docker-compose.testing.yml up
```

### Prueba Manual en Postman
1. Abre Postman
2. Importa: http://localhost:8000/docs
3. Prueba los endpoints

---

## 🔧 Troubleshooting Rápido

### Backend no inicia
```bash
# Verifica Python
python --version  # Debe ser 3.10+

# Reinstala dependencias
pip install -r requirements.txt

# Prueba manualmente
python -m uvicorn main:app --reload
```

### Frontend no conecta al backend
```bash
# Verifica CORS en main.py
# Debe incluir: "http://localhost:5173"

# Verifica que backend está corriendo
curl http://localhost:8000/api/health
```

### Puerto 8000 ya está en uso
```bash
# Cambia el puerto
python -m uvicorn main:app --port 8001 --reload
```

### Base de datos corrupta
```bash
# Elimina y recrea
rm backend/comunidad.db
python -c "from app.db.database import init_db; init_db()"
```

---

## 🎯 Tu Workflow de Desarrollo

### Diario:
1. Terminal 1: Backend
   ```bash
   cd backend && run.bat  # o bash run.sh
   ```

2. Terminal 2: Frontend
   ```bash
   cd frontend && npm run dev
   ```

3. Abre navegador: http://localhost:5173

4. Código en VS Code (editando ambos backends)

5. Test en Swagger: http://localhost:8000/docs

---

## 📊 Estructura de Directorios

```
comunidad/
├── backend/              ← Tu responsabilidad en setup
│   ├── main.py
│   ├── app/
│   │   ├── models/       ← Modelos SQLAlchemy
│   │   ├── routes/       ← Endpoints REST
│   │   ├── services/     ← Lógica de negocio
│   │   └── db/           ← Config base datos
│   ├── run.bat
│   ├── run.sh
│   └── requirements.txt
│
├── frontend/             ← Tu responsabilidad en desarrollo
│   ├── src/
│   │   ├── components/   ← Componentes Vue
│   │   ├── views/        ← Páginas
│   │   └── services/     ← API calls
│   ├── package.json
│   └── vite.config.js
│
└── [docs]/               ← Toda la documentación
    ├── README.md
    ├── ENDPOINTS_EJEMPLOS.md
    ├── MODELOS_DATOS.md
    └── ...
```

---

## ✨ Checklist para Empezar

- [ ] Backend corriendo en puerto 8000
- [ ] Frontend corriendo en puerto 5173
- [ ] curl http://localhost:8000/api/health responde
- [ ] Swagger UI visible en http://localhost:8000/docs
- [ ] Base de datos comunidad.db creada
- [ ] npm install completado en frontend
- [ ] VS Code abierto con ambos directorios

---

## 🎁 Qué Tienes Incluido

**Backend:**
- FastAPI completamente configurado
- 5 modelos de base de datos
- 12+ endpoints REST
- Sistema de validación
- Integración con APIs externas
- Logging y auditoría
- Documentación automática

**Frontend:**
- Vue.js 3 Composition API
- Vite (bundler rápido)
- Componentes dinámicos
- Servicios API
- Hot reload

**Documentación:**
- 15+ archivos de spec técnica
- Ejemplos de código
- Guías paso a paso
- Troubleshooting

---

## 🚀 Próximo Paso

```bash
# En una terminal:
cd backend && run.bat

# En otra terminal:
cd frontend && npm run dev

# En navegador:
http://localhost:5173
```

**¡Listo para empezar el desarrollo!**

---

*Guía generada: 2026-04-25*
*Backend: ✅ Completado y Corriendo*
*Frontend: ⏳ Listo para tus cambios*
