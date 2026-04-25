"""
Endpoints para validación de datos contra APIs externas.

Operaciones:
- POST /api/validaciones/consultar-dni - Consulta RENIEC
- POST /api/validaciones/consultar-ruc - Consulta Facturiza
- GET /api/validaciones/historial - Historial de consultas
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.models.configuracion import ConfiguracionCampo, IntegracionAPI, ConsultaExterna
from app.services.integracion_api_service import IntegracionAPIService
from pydantic import BaseModel

router = APIRouter(prefix="/api/validaciones", tags=["validaciones"])


class ConsultaDNIRequest(BaseModel):
    """Request para consultar DNI"""
    dni: str


class ConsultaRUCRequest(BaseModel):
    """Request para consultar RUC"""
    ruc: str


@router.post("/consultar-dni")
async def consultar_dni(
    request_data: ConsultaDNIRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Consulta RENIEC por DNI y retorna datos para auto-llenar formulario.

    Endpoint: POST /api/validaciones/consultar-dni
    Body: { "dni": "12345678" }

    Response:
    {
        "exitosa": true,
        "datos": {
            "nombre": "Juan Pérez García",
            "apellido_paterno": "Pérez",
            "apellido_materno": "García",
            "genero": "M",
            "fecha_nacimiento": "1990-05-15",
            "estado_civil": "Soltero"
        },
        "validado_externamente": true
    }
    """

    dni = request_data.dni

    # Validar formato DNI
    if not dni.isdigit() or len(dni) != 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="DNI debe ser 8 dígitos"
        )

    # Obtener configuración de campo documento_identidad
    config_dni = db.query(ConfiguracionCampo).filter_by(
        nombre_campo="documento_identidad"
    ).first()

    if not config_dni or not config_dni.api_integracion_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="RENIEC no está configurado para consultas de DNI"
        )

    # Obtener configuración de integración RENIEC
    integracion = db.query(IntegracionAPI).filter_by(
        id=config_dni.api_integracion_id
    ).first()

    if not integracion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integración RENIEC no encontrada"
        )

    if not integracion.activa:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RENIEC no está disponible en este momento"
        )

    # Consultar RENIEC
    service = IntegracionAPIService(db)
    resultado = service.consultar_reniec(dni, integracion)

    # Registrar consulta para auditoría
    ip_origen = request.client.host
    service.registrar_consulta(
        usuario_id=None,  # Aún no se registra
        integracion_id=integracion.id,
        tipo_consulta="documento",
        parametro=dni,
        respuesta=resultado,
        estado="exitosa" if resultado["exitosa"] else "fallida",
        ip_origen=ip_origen
    )

    if not resultado["exitosa"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error consultando RENIEC: {resultado.get('error')}"
        )

    return {
        "exitosa": True,
        "datos": resultado["datos"],
        "validado_externamente": True,
        "fuente": "RENIEC"
    }


@router.post("/consultar-ruc")
async def consultar_ruc(
    request_data: ConsultaRUCRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Consulta Facturiza por RUC y retorna datos de empresa.

    Endpoint: POST /api/validaciones/consultar-ruc
    Body: { "ruc": "20000000001" }

    Response:
    {
        "exitosa": true,
        "datos": {
            "razon_social": "Empresa SAC",
            "direccion": "Av. Principal 123",
            "representante_legal": "Juan Pérez",
            "actividad_economica": "Comercio",
            "estado_contribuyente": "Activo"
        },
        "validado_externamente": true
    }
    """

    ruc = request_data.ruc

    # Validar formato RUC
    if not ruc.isdigit() or len(ruc) != 11:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="RUC debe ser 11 dígitos"
        )

    # Obtener integración Facturiza
    integracion = db.query(IntegracionAPI).filter_by(
        tipo="facturiza",
        activa=True
    ).first()

    if not integracion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Facturiza no está configurado"
        )

    # Consultar Facturiza
    service = IntegracionAPIService(db)
    resultado = service.consultar_facturiza(ruc, integracion)

    # Registrar consulta
    ip_origen = request.client.host
    service.registrar_consulta(
        usuario_id=None,
        integracion_id=integracion.id,
        tipo_consulta="empresa",
        parametro=ruc,
        respuesta=resultado,
        estado="exitosa" if resultado["exitosa"] else "fallida",
        ip_origen=ip_origen
    )

    if not resultado["exitosa"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error consultando Facturiza: {resultado.get('error')}"
        )

    return {
        "exitosa": True,
        "datos": resultado["datos"],
        "validado_externamente": True,
        "fuente": "Facturiza"
    }


@router.get("/historial/{usuario_id}")
async def obtener_historial_consultas(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene historial de consultas realizadas por un usuario.

    Endpoint: GET /api/validaciones/historial/{usuario_id}

    Response:
    {
        "consultas": [
            {
                "id": 1,
                "tipo_consulta": "documento",
                "parametro": "12345678",
                "integracion": "RENIEC",
                "estado": "exitosa",
                "fecha": "2026-04-25T10:30:00",
                "campos_obtenidos": ["nombre", "apellido", "fecha_nacimiento"]
            }
        ]
    }
    """

    consultas = db.query(ConsultaExterna).filter_by(
        usuario_id=usuario_id
    ).order_by(ConsultaExterna.timestamp.desc()).all()

    resultado = {
        "consultas": [
            {
                "id": c.id,
                "tipo_consulta": c.tipo_consulta,
                "parametro": c.parametro_busqueda,
                "integracion": c.integracion.nombre if c.integracion else "Desconocida",
                "estado": c.estado,
                "fecha": c.timestamp.isoformat(),
                "campos_obtenidos": list(c.campos_mapeados.keys()) if c.campos_mapeados else [],
                "error": c.mensaje_error
            }
            for c in consultas
        ]
    }

    return resultado


@router.get("/probar-reniec")
async def probar_reniec(
    db: Session = Depends(get_db)
):
    """
    Endpoint de prueba: Verifica si RENIEC está disponible.
    Requiere permisos de administrador en producción.
    """

    integracion = db.query(IntegracionAPI).filter_by(
        tipo="reniec",
        activa=True
    ).first()

    if not integracion:
        return {
            "disponible": False,
            "error": "RENIEC no está configurado"
        }

    service = IntegracionAPIService(db)
    # Usar un DNI de prueba (si tienes acceso)
    resultado = service.consultar_reniec("00000001", integracion)

    return {
        "disponible": resultado["exitosa"],
        "error": resultado.get("error") if not resultado["exitosa"] else None,
        "datos_prueba": resultado.get("datos") if resultado["exitosa"] else None
    }


@router.get("/probar-facturiza")
async def probar_facturiza(
    db: Session = Depends(get_db)
):
    """
    Endpoint de prueba: Verifica si Facturiza está disponible.
    """

    integracion = db.query(IntegracionAPI).filter_by(
        tipo="facturiza",
        activa=True
    ).first()

    if not integracion:
        return {
            "disponible": False,
            "error": "Facturiza no está configurado"
        }

    service = IntegracionAPIService(db)
    # Usar un RUC de prueba
    resultado = service.consultar_facturiza("20000000001", integracion)

    return {
        "disponible": resultado["exitosa"],
        "error": resultado.get("error") if not resultado["exitosa"] else None,
        "datos_prueba": resultado.get("datos") if resultado["exitosa"] else None
    }
