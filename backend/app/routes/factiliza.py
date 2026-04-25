from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.factiliza_service import FactilizaService
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/integraciones/factiliza", tags=["factiliza"])


# Schemas
class FactilizaConfigSchema(BaseModel):
    endpoint_url: Optional[str] = None
    auth_token: Optional[str] = None
    timeout_segundos: Optional[int] = None
    max_reintentos: Optional[int] = None

    class Config:
        from_attributes = True


class ConsultarDNISchema(BaseModel):
    numero_dni: str

    class Config:
        from_attributes = True


# Rutas
@router.get("/config")
async def obtener_configuracion(db: Session = Depends(get_db)):
    """Obtener configuración actual de Factiliza"""
    service = FactilizaService(db)
    config = service.get_configuracion()

    if not config:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")

    return {
        "endpoint_url": config.endpoint_url,
        "timeout_segundos": config.timeout_segundos,
        "max_reintentos": config.max_reintentos,
        "activa": config.activa,
        "token_configurado": bool(config.auth_token)
    }


@router.post("/config")
async def actualizar_configuracion(
    config_data: FactilizaConfigSchema,
    db: Session = Depends(get_db)
):
    """Actualizar configuración de Factiliza"""
    service = FactilizaService(db)

    config = service.actualizar_configuracion(
        endpoint_url=config_data.endpoint_url,
        auth_token=config_data.auth_token,
        timeout_segundos=config_data.timeout_segundos,
        max_reintentos=config_data.max_reintentos
    )

    return {
        "success": True,
        "message": "Configuración actualizada exitosamente",
        "endpoint_url": config.endpoint_url,
        "timeout_segundos": config.timeout_segundos,
        "max_reintentos": config.max_reintentos
    }


@router.get("/test")
async def test_conexion(db: Session = Depends(get_db)):
    """Probar conexión con Factiliza"""
    service = FactilizaService(db)
    result = service.test_conexion()
    return result


@router.post("/consultar-dni")
async def consultar_dni(
    data: ConsultarDNISchema,
    db: Session = Depends(get_db)
):
    """Consultar DNI y obtener datos de la persona"""
    service = FactilizaService(db)
    result = service.consultar_dni(data.numero_dni)
    return result


@router.get("/historial")
async def listar_historial(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Listar historial de consultas de DNI"""
    service = FactilizaService(db)
    consultas = service.listar_historial(limit=limit, offset=offset)

    return {
        "success": True,
        "count": len(consultas),
        "limit": limit,
        "offset": offset,
        "data": [
            {
                "id": c.id,
                "numero_dni": c.numero_dni,
                "nombre_completo": c.nombre_completo,
                "estado": c.estado,
                "fecha": c.created_at.isoformat()
            }
            for c in consultas
        ]
    }


@router.get("/consultas/{consulta_id}")
async def obtener_consulta(
    consulta_id: int,
    db: Session = Depends(get_db)
):
    """Obtener detalles de una consulta anterior"""
    service = FactilizaService(db)
    consulta = service.obtener_consulta(consulta_id)

    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")

    return {
        "success": True,
        "data": {
            "id": consulta.id,
            "numero_dni": consulta.numero_dni,
            "nombre_completo": consulta.nombre_completo,
            "fecha_nacimiento": consulta.fecha_nacimiento,
            "sexo": consulta.sexo,
            "direccion": consulta.direccion,
            "departamento": consulta.departamento,
            "provincia": consulta.provincia,
            "distrito": consulta.distrito,
            "estado_civil": consulta.estado_civil,
            "edad": consulta.edad,
            "estado": consulta.estado,
            "created_at": consulta.created_at.isoformat()
        }
    }


@router.get("/estadisticas")
async def obtener_estadisticas(db: Session = Depends(get_db)):
    """Obtener estadísticas de consultas de DNI"""
    service = FactilizaService(db)
    stats = service.obtener_estadisticas()
    return {
        "success": True,
        "data": stats
    }


@router.get("/health")
async def health_check():
    """Health check de la integración"""
    return {
        "status": "healthy",
        "service": "factiliza-integration",
        "timestamp": "2026-04-25T00:00:00"
    }
