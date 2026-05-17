"""
Endpoints para administración de configuración de campos e integraciones API.

Panel Admin:
- GET /api/admin/configuracion/campos - Listar campos
- POST /api/admin/configuracion/campos - Crear campo
- PUT /api/admin/configuracion/campos/{id} - Editar campo
- DELETE /api/admin/configuracion/campos/{id} - Eliminar campo

- GET /api/admin/integraciones-api - Listar integraciones
- POST /api/admin/integraciones-api - Crear integración
- PUT /api/admin/integraciones-api/{id} - Editar integración
- DELETE /api/admin/integraciones-api/{id} - Eliminar integración
- POST /api/admin/integraciones-api/{id}/probar - Probar integración
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.db.database import get_db
from app.models.configuracion import (
    ConfiguracionCampo, IntegracionAPI, ConsultaExterna, ConfiguracionMarca,
    TipoDatoEnum, TipoAPIEnum, AuthTypeEnum
)
from app.services.integracion_api_service import IntegracionAPIService
from app.models.usuario import Usuario, RolEnum
from app.utils.auth import get_current_user
from fastapi import UploadFile, File, Query
from datetime import datetime as dt
import os
import secrets

router = APIRouter(prefix="/api/admin", tags=["admin"])


# ============================================================================
# SCHEMAS PYDANTIC
# ============================================================================

class ConfiguracionCampoCreate(BaseModel):
    """Schema para crear/editar campo"""
    nombre_campo: str
    etiqueta: str
    descripcion: Optional[str] = None
    tipo_dato: str
    es_obligatorio: bool = False
    expresion_regex: Optional[str] = None
    valores_enum: Optional[List[str]] = None
    posicion: int = 0
    api_integracion_id: Optional[int] = None
    campo_mapa_api: Optional[str] = None
    mostrar_en_registro: bool = True
    mostrar_en_perfil: bool = True
    mostrar_en_reportes: bool = True


class ConfiguracionCampoResponse(BaseModel):
    """Schema para respuesta de campo"""
    id: int
    nombre_campo: str
    etiqueta: str
    tipo_dato: str
    es_obligatorio: bool
    posicion: int
    api_integracion_id: Optional[int]
    mostrar_en_registro: bool

    class Config:
        from_attributes = True


class IntegracionAPICreate(BaseModel):
    """Schema para crear/editar integración"""
    nombre: str
    descripcion: Optional[str] = None
    tipo: str
    endpoint_url: str
    auth_type: str
    auth_token: str
    activa: bool = True
    timeout_segundos: int = 30
    max_reintentos: int = 3


class IntegracionAPIResponse(BaseModel):
    """Schema para respuesta de integración"""
    id: int
    nombre: str
    tipo: str
    endpoint_url: str
    auth_type: str
    activa: bool
    timeout_segundos: int
    max_reintentos: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# HELPERS
# ============================================================================

def requiere_admin(current_user: Usuario = Depends(get_current_user)):
    """Verifica que el usuario sea administrador"""
    if current_user.rol != RolEnum.ADMINISTRADOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requiere permisos de administrador"
        )
    return current_user


# ============================================================================
# ENDPOINTS: CAMPOS
# ============================================================================

@router.get("/configuracion/campos", response_model=List[ConfiguracionCampoResponse])
async def listar_campos(
    db: Session = Depends(get_db),
    admin = Depends(requiere_admin)
):
    """
    Listar todos los campos configurados.
    """
    campos = db.query(ConfiguracionCampo).order_by(ConfiguracionCampo.posicion).all()
    return campos


@router.post("/configuracion/campos")
async def crear_campo(
    campo_data: ConfiguracionCampoCreate,
    db: Session = Depends(get_db),
    admin = Depends(requiere_admin)
):
    """
    Crear nuevo campo.
    """
    # Validar que nombre_campo sea único
    existente = db.query(ConfiguracionCampo).filter_by(
        nombre_campo=campo_data.nombre_campo
    ).first()

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Campo con ese nombre ya existe"
        )

    # Validar tipo de dato
    try:
        TipoDatoEnum[campo_data.tipo_dato.upper()]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de dato inválido: {campo_data.tipo_dato}"
        )

    # Crear campo
    nuevo_campo = ConfiguracionCampo(
        nombre_campo=campo_data.nombre_campo,
        etiqueta=campo_data.etiqueta,
        descripcion=campo_data.descripcion,
        tipo_dato=campo_data.tipo_dato,
        es_obligatorio=campo_data.es_obligatorio,
        expresion_regex=campo_data.expresion_regex,
        valores_enum=campo_data.valores_enum,
        posicion=campo_data.posicion,
        api_integracion_id=campo_data.api_integracion_id,
        campo_mapa_api=campo_data.campo_mapa_api,
        mostrar_en_registro=campo_data.mostrar_en_registro,
        mostrar_en_perfil=campo_data.mostrar_en_perfil,
        mostrar_en_reportes=campo_data.mostrar_en_reportes,
        creado_por=admin.id
    )

    db.add(nuevo_campo)
    db.commit()
    db.refresh(nuevo_campo)

    return {
        "id": nuevo_campo.id,
        "nombre_campo": nuevo_campo.nombre_campo,
        "etiqueta": nuevo_campo.etiqueta,
        "mensaje": "Campo creado exitosamente"
    }


@router.put("/configuracion/campos/{campo_id}")
async def editar_campo(
    campo_id: int,
    campo_data: ConfiguracionCampoCreate,
    db: Session = Depends(get_db),
    admin = Depends(requiere_admin)
):
    """
    Editar campo existente.
    """
    campo = db.query(ConfiguracionCampo).filter_by(id=campo_id).first()

    if not campo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campo no encontrado"
        )

    # Actualizar campos
    campo.etiqueta = campo_data.etiqueta
    campo.descripcion = campo_data.descripcion
    campo.tipo_dato = campo_data.tipo_dato
    campo.es_obligatorio = campo_data.es_obligatorio
    campo.expresion_regex = campo_data.expresion_regex
    campo.valores_enum = campo_data.valores_enum
    campo.posicion = campo_data.posicion
    campo.api_integracion_id = campo_data.api_integracion_id
    campo.campo_mapa_api = campo_data.campo_mapa_api
    campo.mostrar_en_registro = campo_data.mostrar_en_registro
    campo.mostrar_en_perfil = campo_data.mostrar_en_perfil
    campo.mostrar_en_reportes = campo_data.mostrar_en_reportes
    campo.updated_at = datetime.utcnow()

    db.commit()

    return {
        "id": campo.id,
        "mensaje": "Campo actualizado exitosamente"
    }


@router.delete("/configuracion/campos/{campo_id}")
async def eliminar_campo(
    campo_id: int,
    db: Session = Depends(get_db),
    admin = Depends(requiere_admin)
):
    """
    Eliminar campo.
    """
    campo = db.query(ConfiguracionCampo).filter_by(id=campo_id).first()

    if not campo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campo no encontrado"
        )

    db.delete(campo)
    db.commit()

    return {
        "mensaje": "Campo eliminado exitosamente"
    }


# ============================================================================
# ENDPOINTS: INTEGRACIONES API
# ============================================================================

@router.get("/integraciones-api", response_model=List[IntegracionAPIResponse])
async def listar_integraciones(
    db: Session = Depends(get_db),
    admin = Depends(requiere_admin)
):
    """
    Listar todas las integraciones API.
    """
    integraciones = db.query(IntegracionAPI).all()
    return integraciones


@router.post("/integraciones-api")
async def crear_integracion(
    api_data: IntegracionAPICreate,
    db: Session = Depends(get_db),
    admin = Depends(requiere_admin)
):
    """
    Crear nueva integración API.
    """
    # Validar que nombre sea único
    existente = db.query(IntegracionAPI).filter_by(nombre=api_data.nombre).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Integración con ese nombre ya existe"
        )

    # Validar tipo
    try:
        TipoAPIEnum[api_data.tipo.upper()]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de API inválido"
        )

    # Encriptar token
    service = IntegracionAPIService(db)
    token_encriptado = service.encriptar_token(api_data.auth_token)

    # Crear integración
    nueva_integracion = IntegracionAPI(
        nombre=api_data.nombre,
        descripcion=api_data.descripcion,
        tipo=api_data.tipo,
        endpoint_url=api_data.endpoint_url,
        auth_type=api_data.auth_type,
        auth_token=token_encriptado,
        activa=api_data.activa,
        timeout_segundos=api_data.timeout_segundos,
        max_reintentos=api_data.max_reintentos
    )

    db.add(nueva_integracion)
    db.commit()
    db.refresh(nueva_integracion)

    return {
        "id": nueva_integracion.id,
        "nombre": nueva_integracion.nombre,
        "tipo": nueva_integracion.tipo,
        "mensaje": "Integración creada exitosamente"
    }


@router.put("/integraciones-api/{api_id}")
async def editar_integracion(
    api_id: int,
    api_data: IntegracionAPICreate,
    db: Session = Depends(get_db),
    admin = Depends(requiere_admin)
):
    """
    Editar integración API.
    """
    integracion = db.query(IntegracionAPI).filter_by(id=api_id).first()

    if not integracion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integración no encontrada"
        )

    # Encriptar token si cambió
    service = IntegracionAPIService(db)
    token_encriptado = service.encriptar_token(api_data.auth_token)

    integracion.nombre = api_data.nombre
    integracion.descripcion = api_data.descripcion
    integracion.endpoint_url = api_data.endpoint_url
    integracion.auth_type = api_data.auth_type
    integracion.auth_token = token_encriptado
    integracion.activa = api_data.activa
    integracion.timeout_segundos = api_data.timeout_segundos
    integracion.max_reintentos = api_data.max_reintentos
    integracion.updated_at = datetime.utcnow()

    db.commit()

    return {
        "id": integracion.id,
        "mensaje": "Integración actualizada exitosamente"
    }


@router.delete("/integraciones-api/{api_id}")
async def eliminar_integracion(
    api_id: int,
    db: Session = Depends(get_db),
    admin = Depends(requiere_admin)
):
    """
    Eliminar integración API.
    """
    integracion = db.query(IntegracionAPI).filter_by(id=api_id).first()

    if not integracion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integración no encontrada"
        )

    db.delete(integracion)
    db.commit()

    return {
        "mensaje": "Integración eliminada exitosamente"
    }


@router.post("/integraciones-api/{api_id}/probar")
async def probar_integracion(
    api_id: int,
    db: Session = Depends(get_db),
    admin = Depends(requiere_admin)
):
    """
    Probar conexión a una integración API.
    """
    integracion = db.query(IntegracionAPI).filter_by(id=api_id).first()

    if not integracion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integración no encontrada"
        )

    if not integracion.activa:
        return {
            "disponible": False,
            "error": "Integración desactivada"
        }

    service = IntegracionAPIService(db)

    # Usar valores de prueba según tipo
    if integracion.tipo == "reniec":
        resultado = service.consultar_reniec("00000001", integracion)
    elif integracion.tipo == "facturiza":
        resultado = service.consultar_facturiza("20000000001", integracion)
    else:
        resultado = service.consultar_api_custom("test", integracion)

    return {
        "disponible": resultado["exitosa"],
        "error": resultado.get("error"),
        "datos": resultado.get("datos") if resultado["exitosa"] else None
    }


# ============================================================================
# ENDPOINTS: ESTADÍSTICAS Y AUDITORÍA
# ============================================================================

@router.get("/estadisticas/consultas")
async def estadisticas_consultas(
    db: Session = Depends(get_db),
    admin = Depends(requiere_admin)
):
    """
    Obtener estadísticas de consultas a APIs.
    """
    total_consultas = db.query(ConsultaExterna).count()
    exitosas = db.query(ConsultaExterna).filter_by(estado="exitosa").count()
    fallidas = db.query(ConsultaExterna).filter_by(estado="fallida").count()

    # Por tipo de integración
    por_tipo = db.query(
        IntegracionAPI.nombre,
        func.count(ConsultaExterna.id).label("total")
    ).outerjoin(
        ConsultaExterna,
        IntegracionAPI.id == ConsultaExterna.integracion_api_id
    ).group_by(IntegracionAPI.nombre).all()

    return {
        "total_consultas": total_consultas,
        "exitosas": exitosas,
        "fallidas": fallidas,
        "tasa_exito": round((exitosas / total_consultas * 100) if total_consultas > 0 else 0, 2),
        "por_integracion": [
            {"nombre": tipo, "total": total}
            for tipo, total in por_tipo
        ]
    }


# Importar func para query
from sqlalchemy import func


# ============================================================================
# ENDPOINTS: CONFIGURACIÓN DEL CARNET Usuario
# ============================================================================

from app.models.configuracion import ConfiguracionCarnet
from fastapi import File, UploadFile, Query
from pathlib import Path
from datetime import datetime as dt
import os


class ConfiguracionCarnetResponse(BaseModel):
    """Schema para respuesta de configuración del carnet"""
    nombre_comunidad: str
    subtitulo: str
    resolucion: str
    nombre_corto: str
    bandera_url: Optional[str] = None
    escudo_url: Optional[str] = None
    fondo_anverso_url: Optional[str] = None
    fondo_reverso_url: Optional[str] = None

    class Config:
        from_attributes = True


@router.get("/configuracion/carnet")
async def obtener_config_carnet(db: Session = Depends(get_db)):
    """
    Obtener configuración actual del carnet (público, sin autenticación).
    Si no existe, devuelve valores por defecto.
    """
    try:
        config = db.query(ConfiguracionCarnet).first()

        if not config:
            # Crear registro por defecto
            config = ConfiguracionCarnet()
            db.add(config)
            db.commit()
            db.refresh(config)

        return {
            "nombre_comunidad": config.nombre_comunidad,
            "subtitulo": config.subtitulo,
            "resolucion": config.resolucion,
            "nombre_corto": getattr(config, 'nombre_corto', 'CC.TPCT'),
            "bandera_url": config.bandera_url,
            "escudo_url": config.escudo_url,
            "fondo_anverso_url": config.fondo_anverso_url,
            "fondo_reverso_url": config.fondo_reverso_url,
            "firma_secretario_url": getattr(config, 'firma_secretario_url', None),
            "firma_presidente_url": getattr(config, 'firma_presidente_url', None),
            "url_qr": getattr(config, 'url_qr', None)
        }
    except Exception as e:
        # Si hay error (ej: columna no existe), devolver valores por defecto
        return {
            "nombre_comunidad": "COMUNIDAD CAMPESINA",
            "subtitulo": "TUMILACA, POCATA, COSCORE Y TALA",
            "resolucion": "RESOLUCIÓN SUPREMA 07 SET 1949",
            "nombre_corto": "CC.TPCT",
            "bandera_url": None,
            "escudo_url": None,
            "fondo_anverso_url": None,
            "fondo_reverso_url": None,
            "firma_secretario_url": None,
            "firma_presidente_url": None,
            "url_qr": None
        }


@router.put("/configuracion/carnet")
async def actualizar_config_carnet(
    nombre_comunidad: str = Query(...),
    subtitulo: str = Query(...),
    resolucion: str = Query(...),
    nombre_corto: str = Query(...),
    url_qr: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Actualizar textos de la configuración del carnet.
    """
    try:
        # Usar raw query para evitar problemas con columnas faltantes
        config = db.query(ConfiguracionCarnet).first()

        if not config:
            config = ConfiguracionCarnet(
                nombre_comunidad=nombre_comunidad,
                subtitulo=subtitulo,
                resolucion=resolucion,
                nombre_corto=nombre_corto,
                url_qr=url_qr
            )
            db.add(config)
        else:
            config.nombre_comunidad = nombre_comunidad
            config.subtitulo = subtitulo
            config.resolucion = resolucion
            try:
                config.nombre_corto = nombre_corto
            except:
                pass
            try:
                config.url_qr = url_qr
            except:
                pass

        config.updated_at = dt.utcnow()
        db.commit()
        db.refresh(config)

        return {
            "success": True,
            "mensaje": "Configuración actualizada"
        }
    except Exception as e:
        db.rollback()
        import traceback
        error_detail = str(e)
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error actualizando configuración: {error_detail}"
        )


@router.post("/configuracion/carnet/upload")
async def upload_imagen_carnet(
    tipo: str = Query(..., description="bandera | escudo | fondo_anverso | fondo_reverso | firma_secretario | firma_presidente"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Subir imagen para el carnet.
    tipo: bandera (anverso top-left), escudo (reverso), fondo_anverso, fondo_reverso, firma_secretario, firma_presidente
    """
    try:
        tipos_validos = ["bandera", "escudo", "fondo_anverso", "fondo_reverso", "firma_secretario", "firma_presidente"]
        if tipo not in tipos_validos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo inválido. Use: {', '.join(tipos_validos)}"
            )

        # Crear directorio si no existe
        import os
        os.makedirs("uploads/comunidad", exist_ok=True)

        # Guardar archivo
        file_content = await file.read()
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
        timestamp = int(dt.utcnow().timestamp())
        filename = f"{tipo}_{timestamp}{file_extension}"
        file_path = os.path.join("uploads/comunidad", filename)

        with open(file_path, "wb") as f:
            f.write(file_content)

        # Actualizar config
        config = db.query(ConfiguracionCarnet).first()
        if not config:
            config = ConfiguracionCarnet()
            db.add(config)

        # Mapear tipo a campo
        campo_map = {
            "bandera": "bandera_url",
            "escudo": "escudo_url",
            "fondo_anverso": "fondo_anverso_url",
            "fondo_reverso": "fondo_reverso_url",
            "firma_secretario": "firma_secretario_url",
            "firma_presidente": "firma_presidente_url"
        }

        url_relativa = f"/uploads/comunidad/{filename}"
        setattr(config, campo_map[tipo], url_relativa)
        config.updated_at = dt.utcnow()

        db.commit()
        db.refresh(config)

        return {
            "success": True,
            "tipo": tipo,
            "url": url_relativa,
            "mensaje": f"Imagen {tipo} subida exitosamente"
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = str(e)
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al subir imagen: {error_detail}"
        )


# ============================================================================
# ENDPOINTS MARCA BLANCA (WHITE LABEL)
# ============================================================================

@router.get("/configuracion/marca")
async def obtener_marca(db: Session = Depends(get_db)):
    """Obtiene configuración de marca blanca (público, sin autenticación)"""
    config = db.query(ConfiguracionMarca).filter_by(id=1).first()

    if not config:
        # Retornar defaults
        return {
            "id": 1,
            "nombre_pagina": "Comunidad",
            "subtitulo": "Sistema de Gestión",
            "nombre_corto": "COM",
            "logo_url": None,
            "favicon_url": None,
            "color_primario": "#4f46e5"
        }

    return {
        "id": config.id,
        "nombre_pagina": config.nombre_pagina,
        "subtitulo": config.subtitulo,
        "nombre_corto": config.nombre_corto,
        "logo_url": config.logo_url,
        "favicon_url": config.favicon_url,
        "color_primario": config.color_primario
    }


class MarcaUpdate(BaseModel):
    nombre_pagina: Optional[str] = None
    subtitulo: Optional[str] = None
    nombre_corto: Optional[str] = None
    color_primario: Optional[str] = None


@router.put("/configuracion/marca")
async def actualizar_marca(
    datos: MarcaUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualiza configuración de marca blanca (admin only)"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede actualizar marca")

    config = db.query(ConfiguracionMarca).filter_by(id=1).first()

    if not config:
        config = ConfiguracionMarca(id=1)
        db.add(config)

    if datos.nombre_pagina:
        config.nombre_pagina = datos.nombre_pagina
    if datos.subtitulo:
        config.subtitulo = datos.subtitulo
    if datos.nombre_corto:
        config.nombre_corto = datos.nombre_corto
    if datos.color_primario:
        config.color_primario = datos.color_primario

    config.updated_at = dt.utcnow()
    db.commit()
    db.refresh(config)

    return {
        "success": True,
        "id": config.id,
        "nombre_pagina": config.nombre_pagina,
        "subtitulo": config.subtitulo,
        "nombre_corto": config.nombre_corto,
        "color_primario": config.color_primario
    }


@router.post("/configuracion/marca/upload")
async def subir_marca_imagen(
    tipo: str = Query(..., description="logo o favicon"),
    file: UploadFile = File(...),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Sube logo o favicon (admin only)"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede subir imágenes")

    if tipo not in ["logo", "favicon"]:
        raise HTTPException(status_code=400, detail="Tipo debe ser 'logo' o 'favicon'")

    # Crear directorio si no existe
    os.makedirs("uploads/marca", exist_ok=True)

    # Guardar archivo
    file_content = await file.read()
    filename = f"{tipo}_{secrets.token_hex(8)}{os.path.splitext(file.filename)[1]}"
    file_path = f"uploads/marca/{filename}"

    with open(file_path, "wb") as f:
        f.write(file_content)

    # Actualizar config
    config = db.query(ConfiguracionMarca).filter_by(id=1).first()
    if not config:
        config = ConfiguracionMarca(id=1)
        db.add(config)

    url_relativa = f"/uploads/marca/{filename}"

    if tipo == "logo":
        config.logo_url = url_relativa
    elif tipo == "favicon":
        config.favicon_url = url_relativa

    config.updated_at = dt.utcnow()
    db.commit()
    db.refresh(config)

    return {
        "success": True,
        "tipo": tipo,
        "url": url_relativa,
        "mensaje": f"{tipo.capitalize()} subido exitosamente"
    }
