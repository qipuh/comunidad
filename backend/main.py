"""
FastAPI Main Application
Sistema de Configuración Dinámico para Comunidades
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:5174,http://localhost:3000,http://localhost:8080"
).split(",")

# Crear aplicación FastAPI
app = FastAPI(
    title="API Comunidad",
    description="Sistema de gestión comunitaria con configuración dinámica",
    version="1.0.0",
    redirect_slashes=True
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir uploads de fotos
os.makedirs("uploads/usuarios", exist_ok=True)
os.makedirs("uploads/elecciones/votos", exist_ok=True)
os.makedirs("uploads/comunidad", exist_ok=True)
os.makedirs("uploads/marca", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ════════════════════════════════════════════════════════════════
# IMPORTAR RUTAS
# ════════════════════════════════════════════════════════════════

try:
    from app.routes.admin_configuracion import router as admin_config_router
    from app.routes.validaciones import router as validaciones_router
    from app.routes.factiliza import router as factiliza_router
    from app.routes.usuarios import router as usuarios_router
    from app.routes.plantilla import router as plantilla_router
    from app.routes.auth import router as auth_router
    from app.routes.cobranza import router as cobranza_router
    from app.routes.elecciones import router as elecciones_router
    from app.routes.reuniones import router as reuniones_router
    from app.routes.dashboard import router as dashboard_router
    from app.routes.carnets import router as carnets_router
    logger.info("✅ Rutas importadas correctamente")
except Exception as e:
    logger.error(f"❌ Error importando rutas: {type(e).__name__}: {e}", exc_info=True)
    raise

# ════════════════════════════════════════════════════════════════
# REGISTRAR RUTAS
# ════════════════════════════════════════════════════════════════

try:
    app.include_router(auth_router, tags=["Auth"])
    app.include_router(admin_config_router, tags=["Admin"])
    app.include_router(validaciones_router, tags=["Validaciones"])
    app.include_router(factiliza_router, tags=["Factiliza"])
    app.include_router(plantilla_router, tags=["Plantilla"])
    app.include_router(usuarios_router, tags=["Usuarios"])
    app.include_router(cobranza_router, tags=["Cobranza"])
    app.include_router(elecciones_router, tags=["Elecciones"])
    app.include_router(reuniones_router, tags=["Reuniones"])
    app.include_router(dashboard_router, tags=["Dashboard"])
    app.include_router(carnets_router, tags=["Carnets"])
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
    try:
        from app.db.database import init_db
        init_db()
        logger.info("✅ Base de datos inicializada")
    except Exception as e:
        logger.error(f"❌ Error inicializando BD: {e}", exc_info=True)
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
    logger.info("Iniciando servidor en http://127.0.0.1:4242")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=4242,
        reload=True,
        log_level="info"
    )
