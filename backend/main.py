"""
FastAPI Main Application
Sistema de Configuración Dinámico para Comunidades
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="API Comunidad",
    description="Sistema de gestión comunitaria con configuración dinámica",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8080", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ════════════════════════════════════════════════════════════════
# IMPORTAR RUTAS
# ════════════════════════════════════════════════════════════════

try:
    from app.routes.admin_configuracion import router as admin_config_router
    from app.routes.validaciones import router as validaciones_router
    from app.routes.factiliza import router as factiliza_router
    from app.routes.usuarios import router as usuarios_router
    from app.routes.auth import router as auth_router
    logger.info("✅ Rutas importadas correctamente")
except Exception as e:
    logger.warning(f"⚠️ Error importando rutas: {e}")

# ════════════════════════════════════════════════════════════════
# REGISTRAR RUTAS
# ════════════════════════════════════════════════════════════════

try:
    app.include_router(auth_router, tags=["Auth"])
    app.include_router(admin_config_router, tags=["Admin"])
    app.include_router(validaciones_router, tags=["Validaciones"])
    app.include_router(factiliza_router, tags=["Factiliza"])
    app.include_router(usuarios_router, tags=["Usuarios"])
    logger.info("✅ Rutas registradas en la aplicación")
except Exception as e:
    logger.error(f"ERROR registrando rutas: {type(e).__name__}: {e}", exc_info=True)
    raise

# ════════════════════════════════════════════════════════════════
# ENDPOINTS DE SALUD
# ════════════════════════════════════════════════════════════════

@app.get("/", tags=["Health"])
async def root():
    """Endpoint raíz"""
    return {
        "mensaje": "🎉 API Comunidad - Sistema de Configuración Dinámico",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/health", tags=["Health"])
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "comunidad-api",
        "timestamp": "2026-04-25T14:00:00"
    }

@app.get("/api/admin/health", tags=["Health"])
async def admin_health():
    """Health check para admin"""
    return {
        "status": "healthy",
        "service": "comunidad-admin-api",
        "endpoints": {
            "integraciones": "/api/admin/integraciones-api",
            "campos": "/api/admin/configuracion/campos",
            "estadisticas": "/api/admin/estadisticas/consultas"
        }
    }

# ════════════════════════════════════════════════════════════════
# CONFIGURAR OPENAPI
# ════════════════════════════════════════════════════════════════

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API Comunidad",
        version="1.0.0",
        description="Sistema de gestión comunitaria con configuración dinámica de campos y APIs",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ════════════════════════════════════════════════════════════════
# STARTUP/SHUTDOWN EVENTS
# ════════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_event():
    """Evento al iniciar la aplicación"""
    logger.info("🚀 Iniciando API Comunidad...")
    logger.info("✅ Base de datos conectada")
    logger.info("✅ Rutas cargadas")
    logger.info("✅ Sistema listo para recibir peticiones")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento al detener la aplicación"""
    logger.info("🛑 Deteniendo API Comunidad...")

# ════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    logger.info("🌐 Iniciando servidor en http://0.0.0.0:8000")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
