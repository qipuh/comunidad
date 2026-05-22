from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.usuario import Usuario
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import os
from pathlib import Path

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])

UPLOAD_DIR = Path("uploads/usuarios")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Schemas
class UsuarioCreateSchema(BaseModel):
    email: str
    username: str
    password: str
    nombres: str
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    numero_dni: str
    telefono: str
    rol: str = "usuario"

    class Config:
        from_attributes = True


class UsuarioUpdateSchema(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    numero_dni: Optional[str] = None
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    sexo: Optional[str] = None
    estado_civil: Optional[str] = None
    direccion: Optional[str] = None
    departamento: Optional[str] = None
    provincia: Optional[str] = None
    distrito: Optional[str] = None
    anexo: Optional[str] = None
    rol: Optional[str] = None
    estado: Optional[str] = None
    usar_reconocimiento_facial: Optional[bool] = None

    class Config:
        from_attributes = True


class ImportarConfirmadoSchema(BaseModel):
    usuarios: List[Dict[str, Any]]

    class Config:
        from_attributes = True


class UsuarioResponseSchema(BaseModel):
    id: int
    email: str
    username: str
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    numero_dni: Optional[str] = None
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    sexo: Optional[str] = None
    estado_civil: Optional[str] = None
    direccion: Optional[str] = None
    departamento: Optional[str] = None
    provincia: Optional[str] = None
    distrito: Optional[str] = None
    anexo: Optional[str] = None
    foto_url: Optional[str] = None
    foto_frontal: Optional[str] = None
    foto_lateral_izq: Optional[str] = None
    foto_lateral_der: Optional[str] = None
    usar_reconocimiento_facial: bool = False
    rol: str
    estado: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


def save_upload_file(file: UploadFile, filename_prefix: str, usuario_id: int) -> str:
    """Save uploaded file and return the path."""
    if not file or not file.filename:
        return None

    content = file.file.read()
    if not content:
        return None

    file_extension = Path(file.filename).suffix if file.filename else ".jpg"
    filename = f"{filename_prefix}_{usuario_id}_{int(datetime.now().timestamp())}{file_extension}"
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as f:
        f.write(content)

    return str(file_path)


# Rutas CRUD
@router.get("/")
async def listar_usuarios(
    limit: int = Query(50, ge=1, le=10000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Listar todos los usuarios"""
    try:
        usuarios = db.query(Usuario).order_by(Usuario.created_at.desc()).limit(limit).offset(offset).all()
        total = db.query(Usuario).count()

        data = []
        for u in usuarios:
            try:
                item = {
                    "id": u.id,
                    "email": u.email,
                    "username": u.username,
                    "nombres": u.nombres,
                    "apellido_paterno": u.apellido_paterno,
                    "apellido_materno": u.apellido_materno,
                    "nombre_completo": u.nombre_completo,
                    "numero_dni": u.numero_dni,
                    "num_padron": u.num_padron,
                    "telefono": u.telefono,
                    "fecha_nacimiento": u.fecha_nacimiento,
                    "sexo": u.sexo,
                    "estado_civil": u.estado_civil,
                    "direccion": u.direccion,
                    "departamento": u.departamento,
                    "provincia": u.provincia,
                    "distrito": u.distrito,
                    "anexo": u.anexo,
                    "foto_url": u.foto_url,
                    "foto_frontal": u.foto_frontal,
                    "foto_lateral_izq": u.foto_lateral_izq,
                    "foto_lateral_der": u.foto_lateral_der,
                    "usar_reconocimiento_facial": u.usar_reconocimiento_facial,
                    "rol": u.rol,
                    "estado": u.estado,
                    "fecha_inicio_cobranza": u.fecha_inicio_cobranza.isoformat() if u.fecha_inicio_cobranza else None,
                    "created_at": u.created_at.isoformat() if u.created_at else None,
                    "updated_at": u.updated_at.isoformat() if u.updated_at else None
                }
                data.append(item)
            except Exception as item_error:
                print(f"[ERROR] Error procesando usuario {u.id}: {item_error}")
                raise

        return {
            "success": True,
            "count": len(usuarios),
            "total": total,
            "limit": limit,
            "offset": offset,
            "data": data
        }
    except Exception as e:
        import traceback
        print(f"[ERROR] Error en listar_usuarios: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error listando usuarios: {str(e)}")


@router.post("/")
async def crear_usuario(
    numero_dni: str = Form(...),
    email: str = Form(None),
    username: str = Form(None),
    password: str = Form(None),
    nombres: str = Form(...),
    apellido_paterno: str = Form(None),
    apellido_materno: str = Form(None),
    telefono: str = Form(...),
    fecha_nacimiento: str = Form(None),
    sexo: str = Form(None),
    estado_civil: str = Form(None),
    direccion: str = Form(None),
    departamento: str = Form(None),
    provincia: str = Form(None),
    distrito: str = Form(None),
    anexo: str = Form(None),
    usar_reconocimiento_facial: bool = Form(False),
    rol: str = Form("usuario"),
    fecha_inicio_cobranza: Optional[str] = Form(None),
    foto_frontal: Optional[UploadFile] = File(None),
    foto_lateral_izq: Optional[UploadFile] = File(None),
    foto_lateral_der: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Crear un nuevo usuario con soporte para fotos y datos Factiliza"""
    # Usar DNI como email y username si no se proveen
    email_final = email or f"{numero_dni}@comunidad.local"
    username_final = username or numero_dni
    password_final = password or ""

    # Validar que no exista email duplicado
    usuario_existente = db.query(Usuario).filter(Usuario.email == email_final).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Validar que no exista username duplicado
    username_existente = db.query(Usuario).filter(Usuario.username == username_final).first()
    if username_existente:
        raise HTTPException(status_code=400, detail="El username ya está registrado")

    # Validar que no exista DNI duplicado
    dni_existente = db.query(Usuario).filter(Usuario.numero_dni == numero_dni).first()
    if dni_existente:
        raise HTTPException(status_code=400, detail="El DNI ya está registrado")

    fecha_inicio_cobranza_dt = None
    if fecha_inicio_cobranza:
        try:
            # Manejo flexible de formatos de fecha
            fecha_str = fecha_inicio_cobranza
            # Si es solo una fecha (YYYY-MM-DD), agregar hora
            if len(fecha_str) == 10:
                fecha_str = fecha_str + "T00:00:00"
            fecha_inicio_cobranza_dt = datetime.fromisoformat(fecha_str)
        except Exception as e:
            print(f"Error parseando fecha_inicio_cobranza: {e}, valor: {fecha_inicio_cobranza}")
            pass

    nuevo_usuario = Usuario(
        email=email_final,
        username=username_final,
        password_hash=password_final,
        numero_dni=numero_dni,
        nombres=nombres,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        telefono=telefono,
        fecha_nacimiento=fecha_nacimiento,
        sexo=sexo,
        estado_civil=estado_civil,
        direccion=direccion,
        departamento=departamento,
        provincia=provincia,
        distrito=distrito,
        anexo=anexo,
        usar_reconocimiento_facial=usar_reconocimiento_facial,
        rol=rol,
        estado="activo",
        fecha_inicio_cobranza=fecha_inicio_cobranza_dt
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    # Guardar fotos si se proporcionan
    if foto_frontal:
        nuevo_usuario.foto_frontal = save_upload_file(foto_frontal, "frontal", nuevo_usuario.id)
    if foto_lateral_izq:
        nuevo_usuario.foto_lateral_izq = save_upload_file(foto_lateral_izq, "lateral_izq", nuevo_usuario.id)
    if foto_lateral_der:
        nuevo_usuario.foto_lateral_der = save_upload_file(foto_lateral_der, "lateral_der", nuevo_usuario.id)

    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "success": True,
        "message": "Usuario creado exitosamente",
        "data": {
            "id": nuevo_usuario.id,
            "email": nuevo_usuario.email,
            "username": nuevo_usuario.username,
            "nombres": nuevo_usuario.nombres,
            "apellido_paterno": nuevo_usuario.apellido_paterno,
            "apellido_materno": nuevo_usuario.apellido_materno,
            "numero_dni": nuevo_usuario.numero_dni,
            "telefono": nuevo_usuario.telefono,
            "rol": nuevo_usuario.rol,
            "estado": nuevo_usuario.estado,
            "fecha_inicio_cobranza": nuevo_usuario.fecha_inicio_cobranza.isoformat() if nuevo_usuario.fecha_inicio_cobranza else None,
            "created_at": nuevo_usuario.created_at.isoformat() if nuevo_usuario.created_at else None
        }
    }


@router.get("/buscar")
async def buscar_usuarios(
    query: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Buscar usuarios por nombres, apellido_paterno o apellido_materno"""
    from sqlalchemy import or_

    search_term = f"%{query}%"
    usuarios = db.query(Usuario).filter(
        or_(
            Usuario.nombres.ilike(search_term),
            Usuario.apellido_paterno.ilike(search_term),
            Usuario.apellido_materno.ilike(search_term)
        )
    ).order_by(Usuario.apellido_paterno, Usuario.apellido_materno, Usuario.nombres).limit(50).all()

    data = []
    for u in usuarios:
        data.append({
            "id": u.id,
            "nombres": u.nombres,
            "apellido_paterno": u.apellido_paterno,
            "apellido_materno": u.apellido_materno,
            "nombre_completo": u.nombre_completo,
            "numero_dni": u.numero_dni,
            "email": u.email,
            "rol": u.rol,
            "estado": u.estado
        })

    return {
        "success": True,
        "count": len(usuarios),
        "data": data
    }


@router.get("/buscar/por-email")
async def buscar_por_email(
    email: str,
    db: Session = Depends(get_db)
):
    """Buscar usuario por email"""
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "success": True,
        "data": {
            "id": usuario.id,
            "email": usuario.email,
            "username": usuario.username,
            "nombres": usuario.nombres,
            "apellido_paterno": usuario.apellido_paterno,
            "apellido_materno": usuario.apellido_materno,
            "nombre_completo": usuario.nombre_completo,
            "rol": usuario.rol,
            "estado": usuario.estado
        }
    }


@router.get("/estadisticas/total")
async def obtener_estadisticas(db: Session = Depends(get_db)):
    """Obtener estadísticas de usuarios"""
    total_usuarios = db.query(Usuario).count()
    usuarios_activos = db.query(Usuario).filter(Usuario.estado == "activo").count()
    usuarios_inactivos = db.query(Usuario).filter(Usuario.estado == "inactivo").count()

    return {
        "success": True,
        "data": {
            "total_usuarios": total_usuarios,
            "usuarios_activos": usuarios_activos,
            "usuarios_inactivos": usuarios_inactivos,
            "porcentaje_activos": (usuarios_activos / total_usuarios * 100) if total_usuarios > 0 else 0
        }
    }


@router.get("/{usuario_id}")
async def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """Obtener detalles de un usuario específico"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "success": True,
        "data": {
            "id": usuario.id,
            "email": usuario.email,
            "username": usuario.username,
            "nombres": usuario.nombres,
            "apellido_paterno": usuario.apellido_paterno,
            "apellido_materno": usuario.apellido_materno,
            "nombre_completo": usuario.nombre_completo,
            "numero_dni": usuario.numero_dni,
            "telefono": usuario.telefono,
            "fecha_nacimiento": usuario.fecha_nacimiento,
            "sexo": usuario.sexo,
            "estado_civil": usuario.estado_civil,
            "direccion": usuario.direccion,
            "departamento": usuario.departamento,
            "provincia": usuario.provincia,
            "distrito": usuario.distrito,
            "anexo": usuario.anexo,
            "foto_url": usuario.foto_url,
            "foto_frontal": usuario.foto_frontal,
            "foto_lateral_izq": usuario.foto_lateral_izq,
            "foto_lateral_der": usuario.foto_lateral_der,
            "usar_reconocimiento_facial": usuario.usar_reconocimiento_facial,
            "rol": usuario.rol,
            "estado": usuario.estado,
            "fecha_inicio_cobranza": usuario.fecha_inicio_cobranza.isoformat() if usuario.fecha_inicio_cobranza else None,
            "created_at": usuario.created_at.isoformat() if usuario.created_at else None,
            "updated_at": usuario.updated_at.isoformat() if usuario.updated_at else None
        }
    }


@router.put("/{usuario_id}")
async def actualizar_usuario(
    usuario_id: int,
    email: Optional[str] = Form(None),
    username: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    nombres: Optional[str] = Form(None),
    apellido_paterno: Optional[str] = Form(None),
    apellido_materno: Optional[str] = Form(None),
    numero_dni: Optional[str] = Form(None),
    telefono: Optional[str] = Form(None),
    fecha_nacimiento: Optional[str] = Form(None),
    sexo: Optional[str] = Form(None),
    estado_civil: Optional[str] = Form(None),
    direccion: Optional[str] = Form(None),
    departamento: Optional[str] = Form(None),
    provincia: Optional[str] = Form(None),
    distrito: Optional[str] = Form(None),
    anexo: Optional[str] = Form(None),
    rol: Optional[str] = Form(None),
    estado: Optional[str] = Form(None),
    usar_reconocimiento_facial: Optional[bool] = Form(None),
    fecha_inicio_cobranza: Optional[str] = Form(None),
    foto_frontal: UploadFile = File(None),
    foto_lateral_izq: UploadFile = File(None),
    foto_lateral_der: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """Actualizar datos de un usuario"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Validar email único si se está actualizando
    if email and email != usuario.email:
        email_existente = db.query(Usuario).filter(Usuario.email == email).first()
        if email_existente:
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        usuario.email = email

    # Validar username único si se está actualizando
    if username and username != usuario.username:
        username_existente = db.query(Usuario).filter(Usuario.username == username).first()
        if username_existente:
            raise HTTPException(status_code=400, detail="El username ya está registrado")
        usuario.username = username

    # Validar DNI único si se está actualizando
    if numero_dni and numero_dni != usuario.numero_dni:
        dni_existente = db.query(Usuario).filter(Usuario.numero_dni == numero_dni).first()
        if dni_existente:
            raise HTTPException(status_code=400, detail="El DNI ya está registrado")
        usuario.numero_dni = numero_dni

    if nombres:
        usuario.nombres = nombres
    if apellido_paterno:
        usuario.apellido_paterno = apellido_paterno
    if apellido_materno:
        usuario.apellido_materno = apellido_materno
    if telefono:
        usuario.telefono = telefono
    if fecha_nacimiento:
        usuario.fecha_nacimiento = fecha_nacimiento
    if sexo:
        usuario.sexo = sexo
    if estado_civil:
        usuario.estado_civil = estado_civil
    if direccion:
        usuario.direccion = direccion
    if departamento:
        usuario.departamento = departamento
    if provincia:
        usuario.provincia = provincia
    if distrito:
        usuario.distrito = distrito
    if anexo:
        usuario.anexo = anexo
    if password:
        usuario.password_hash = password
    if rol:
        usuario.rol = rol
    if estado:
        usuario.estado = estado
    if usar_reconocimiento_facial is not None:
        usuario.usar_reconocimiento_facial = usar_reconocimiento_facial
    if fecha_inicio_cobranza:
        try:
            # Manejo flexible de formatos de fecha
            if isinstance(fecha_inicio_cobranza, str):
                fecha_str = fecha_inicio_cobranza
                # Si es solo una fecha (YYYY-MM-DD), agregar hora
                if len(fecha_str) == 10:
                    fecha_str = fecha_str + "T00:00:00"
                usuario.fecha_inicio_cobranza = datetime.fromisoformat(fecha_str)
            else:
                usuario.fecha_inicio_cobranza = fecha_inicio_cobranza
        except Exception as e:
            print(f"Error parseando fecha_inicio_cobranza: {e}, valor: {fecha_inicio_cobranza}")
            pass

    # Guardar fotos si se proporcionan
    if foto_frontal:
        usuario.foto_frontal = save_upload_file(foto_frontal, "frontal", usuario_id)
    if foto_lateral_izq:
        usuario.foto_lateral_izq = save_upload_file(foto_lateral_izq, "lateral_izq", usuario_id)
    if foto_lateral_der:
        usuario.foto_lateral_der = save_upload_file(foto_lateral_der, "lateral_der", usuario_id)

    usuario.updated_at = datetime.now()

    db.commit()
    db.refresh(usuario)

    return {
        "success": True,
        "message": "Usuario actualizado exitosamente",
        "data": {
            "id": usuario.id,
            "email": usuario.email,
            "username": usuario.username,
            "nombres": usuario.nombres,
            "apellido_paterno": usuario.apellido_paterno,
            "apellido_materno": usuario.apellido_materno,
            "numero_dni": usuario.numero_dni,
            "telefono": usuario.telefono,
            "rol": usuario.rol,
            "estado": usuario.estado,
            "fecha_inicio_cobranza": usuario.fecha_inicio_cobranza.isoformat() if usuario.fecha_inicio_cobranza else None,
            "updated_at": usuario.updated_at.isoformat() if usuario.updated_at else None
        }
    }


@router.delete("/{usuario_id}")
async def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un usuario"""
    try:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Primero eliminar cualquier referencia en ConfiguracionCampo
        from app.models.configuracion import ConfiguracionCampo
        db.query(ConfiguracionCampo).filter(ConfiguracionCampo.creado_por == usuario_id).delete()

        # Luego eliminar el usuario (sus relaciones con cascade se eliminarán automáticamente)
        db.delete(usuario)
        db.commit()

        return {
            "success": True,
            "message": "Usuario eliminado exitosamente"
        }
    except Exception as e:
        db.rollback()
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error eliminando usuario {usuario_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar usuario: {str(e)}"
        )


@router.post("/preview-excel")
async def preview_excel(
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Previsualizar usuarios desde archivo Excel sin crearlos"""
    try:
        from openpyxl import load_workbook
        from datetime import datetime as dt
        import logging

        logger = logging.getLogger(__name__)
        contenido = await archivo.read()

        import io
        wb = load_workbook(io.BytesIO(contenido))
        ws = wb.active

        filas = []
        resumen = {"validos": 0, "duplicados": 0, "errores": 0}

        for idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            # Saltar filas completamente vacías
            if not row or all(cell is None for cell in row):
                continue

            # Manejar filas con menos columnas - usar get seguro
            def get_cell(index, default=None):
                if index < len(row):
                    return row[index]
                return default

            estado = "error"
            motivo = None
            datos = {}

            try:
                # Mapeo: num_padron, APELLIDO PATERNO, APELLIDO MATERNO, NOMBRES, SEXO, DNI, F. NACIMIENTO, ESTADO CIVIL
                num_padron = get_cell(0, "") or ""
                apellido_paterno = get_cell(1, "") or ""
                apellido_materno = get_cell(2, "") or ""
                nombres = get_cell(3, "") or ""
                sexo = get_cell(4, "") or ""
                dni_raw = get_cell(5, "")
                fecha_nacimiento = get_cell(6)
                estado_civil = get_cell(7, "") or ""

                # Procesar DNI
                dni = str(dni_raw or "").strip() if dni_raw else ""

                # Determinar estado
                estado = "valido"
                motivo = None

                # Validar DNI
                if not dni:
                    estado = "error"
                    motivo = "DNI vacío"
                elif len(dni) != 8:
                    estado = "error"
                    motivo = f"DNI debe tener 8 dígitos (tiene {len(dni)})"
                elif not dni.isdigit():
                    estado = "error"
                    motivo = "DNI debe ser solo números"

                # Validar nombres
                if estado == "valido" and not nombres:
                    estado = "error"
                    motivo = "Nombres vacío"

                # Validar sexo
                if estado == "valido" and sexo:
                    sexo_upper = str(sexo).upper().strip()
                    if sexo_upper not in ["M", "F", "MASCULINO", "FEMENINO"]:
                        estado = "error"
                        motivo = f"Sexo inválido: '{sexo}' (debe ser M/F o Masculino/Femenino)"

                # Validar duplicado (pero marcar como duplicado si queremos actualizar)
                usuario_existente = None
                if estado == "valido":
                    usuario_existente = db.query(Usuario).filter(Usuario.numero_dni == dni).first()
                    if usuario_existente:
                        estado = "duplicado"
                        motivo = "DNI ya registrado (se puede actualizar)"

                # Procesar fecha
                fecha_nac_str = None
                if fecha_nacimiento:
                    try:
                        if isinstance(fecha_nacimiento, dt):
                            fecha_nac_str = fecha_nacimiento.strftime("%Y-%m-%d")
                        else:
                            fecha_nac_str = str(fecha_nacimiento).strip()
                            # Si es una fecha en texto, intentar parsearlo
                            if fecha_nac_str and len(fecha_nac_str) > 0:
                                fecha_nac_str = fecha_nac_str[:10]  # Tomar solo la parte de fecha
                    except:
                        fecha_nac_str = None

                datos = {
                    "num_padron": str(num_padron).strip(),
                    "apellido_paterno": str(apellido_paterno).strip(),
                    "apellido_materno": str(apellido_materno).strip(),
                    "nombres": str(nombres).strip(),
                    "sexo": str(sexo).strip() if sexo else "",
                    "dni": dni,
                    "fecha_nacimiento": fecha_nac_str,
                    "estado_civil": str(estado_civil).strip() if estado_civil else "",
                    "usuario_existente": usuario_existente is not None
                }

            except Exception as row_error:
                logger.error(f"Error procesando fila {idx}: {row_error}", exc_info=True)
                estado = "error"
                motivo = f"Error procesando: {str(row_error)[:50]}"
                datos = {}

            # Agregar fila al resultado
            filas.append({
                "fila": idx,
                "estado": estado,
                "motivo": motivo,
                "datos": datos
            })

            # Incrementar resumen
            if estado in resumen:
                resumen[estado] += 1

        return {
            "success": True,
            "filas": filas,
            "resumen": resumen
        }

    except Exception as e:
        logger.error(f"Error en preview-excel: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Error leyendo archivo: {str(e)[:200]}")


@router.post("/importar-confirmado")
async def importar_confirmado(
    datos: ImportarConfirmadoSchema,
    db: Session = Depends(get_db)
):
    """Importar usuarios que ya fueron validados - Crea nuevos y actualiza existentes"""
    try:
        usuarios_list = datos.usuarios

        if not isinstance(usuarios_list, list):
            raise HTTPException(status_code=400, detail="usuarios debe ser una lista")

        usuarios_creados = []
        usuarios_actualizados = []
        errores = []

        for idx, user_data in enumerate(usuarios_list):
            try:
                dni = str(user_data.get("dni", "")).strip()
                nombres = user_data.get("nombres", "")
                apellido_paterno = user_data.get("apellido_paterno", "")
                apellido_materno = user_data.get("apellido_materno", "")
                sexo = user_data.get("sexo", "")
                fecha_nacimiento = user_data.get("fecha_nacimiento")
                num_padron = user_data.get("num_padron", "")
                estado_civil = user_data.get("estado_civil", "")
                actualizar = user_data.get("actualizar", False)

                # Validación final (seguridad)
                if not dni or len(dni) != 8 or not dni.isdigit():
                    errores.append(f"Usuario {idx}: DNI inválido '{dni}'")
                    continue

                # Verificar si el usuario existe
                usuario_existente = db.query(Usuario).filter(Usuario.numero_dni == dni).first()

                if usuario_existente:
                    # Actualizar si está indicado o si es lo único que podemos hacer
                    if actualizar:
                        # Actualizar los datos del usuario
                        usuario_existente.nombres = nombres or usuario_existente.nombres
                        usuario_existente.apellido_paterno = apellido_paterno or usuario_existente.apellido_paterno
                        usuario_existente.apellido_materno = apellido_materno or usuario_existente.apellido_materno
                        usuario_existente.sexo = sexo or usuario_existente.sexo
                        usuario_existente.fecha_nacimiento = fecha_nacimiento or usuario_existente.fecha_nacimiento
                        usuario_existente.estado_civil = estado_civil or usuario_existente.estado_civil
                        if num_padron:
                            usuario_existente.num_padron = num_padron

                        db.flush()
                        nombre_completo = f"{usuario_existente.nombres} {usuario_existente.apellido_paterno}".strip()
                        usuarios_actualizados.append({
                            "id": usuario_existente.id,
                            "dni": dni,
                            "nombre": nombre_completo
                        })
                    else:
                        errores.append(f"Usuario {idx}: DNI {dni} ya registrado (no se actualiza)")
                else:
                    # Crear usuario nuevo
                    nuevo_usuario = Usuario(
                        numero_dni=dni,
                        nombres=nombres,
                        apellido_paterno=apellido_paterno,
                        apellido_materno=apellido_materno,
                        email=f"{dni}@comunidad.local",
                        username=dni,
                        password_hash=dni,
                        telefono="",
                        sexo=sexo if sexo else None,
                        fecha_nacimiento=fecha_nacimiento,
                        estado_civil=estado_civil if estado_civil else None,
                        num_padron=num_padron if num_padron else None,
                        rol="usuario",
                        estado="activo",
                        usar_reconocimiento_facial=False
                    )

                    db.add(nuevo_usuario)
                    db.flush()

                    nombre_completo = f"{nombres} {apellido_paterno}".strip()
                    usuarios_creados.append({
                        "id": nuevo_usuario.id,
                        "dni": dni,
                        "nombre": nombre_completo
                    })

            except Exception as e:
                errores.append(f"Usuario {idx}: {str(e)}")

        if usuarios_creados or usuarios_actualizados:
            db.commit()

        total_procesados = len(usuarios_creados) + len(usuarios_actualizados)
        return {
            "success": True,
            "usuarios_creados": usuarios_creados,
            "usuarios_actualizados": usuarios_actualizados,
            "errores": errores,
            "mensaje": f"Importación completada: {len(usuarios_creados)} creados, {len(usuarios_actualizados)} actualizados"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error importando: {str(e)}")


@router.post("/importar-excel")
async def importar_excel(
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Importar usuarios desde archivo Excel (sin validación previa)"""
    try:
        from openpyxl import load_workbook
        from datetime import datetime as dt

        contenido = await archivo.read()

        import io
        wb = load_workbook(io.BytesIO(contenido))
        ws = wb.active

        usuarios_creados = []
        errores = []

        for idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            try:
                # Mapeo: APELLIDO PATERNO, APELLIDO MATERNO, NOMBRES, SEXO, DNI, F. NACIMIENTO
                apellido_paterno = row[0] or "" if len(row) > 0 else ""
                apellido_materno = row[1] or "" if len(row) > 1 else ""
                nombres = row[2] or "" if len(row) > 2 else ""
                sexo = row[3] or "" if len(row) > 3 else ""
                dni = str(row[4] or "").strip() if len(row) > 4 else ""
                fecha_nacimiento = row[5] if len(row) > 5 else None

                if not dni or len(dni) != 8:
                    errores.append(f"Fila {idx}: DNI inválido '{dni}'")
                    continue

                if not nombres:
                    errores.append(f"Fila {idx}: Nombres vacío")
                    continue

                usuario_existente = db.query(Usuario).filter(Usuario.numero_dni == dni).first()
                if usuario_existente:
                    errores.append(f"Fila {idx}: DNI {dni} ya registrado")
                    continue

                fecha_nac_str = None
                if fecha_nacimiento:
                    try:
                        if isinstance(fecha_nacimiento, dt):
                            fecha_nac_str = fecha_nacimiento.strftime("%Y-%m-%d")
                        else:
                            fecha_nac_str = str(fecha_nacimiento)
                    except:
                        pass

                nuevo_usuario = Usuario(
                    numero_dni=dni,
                    nombres=nombres,
                    apellido_paterno=apellido_paterno,
                    apellido_materno=apellido_materno,
                    email=f"{dni}@comunidad.local",
                    username=dni,
                    password_hash=dni,
                    telefono="",
                    sexo=sexo if sexo else None,
                    fecha_nacimiento=fecha_nac_str,
                    rol="usuario",
                    estado="activo",
                    usar_reconocimiento_facial=False
                )

                db.add(nuevo_usuario)
                db.flush()

                nombre_completo = f"{nombres} {apellido_paterno}".strip()
                usuarios_creados.append({
                    "id": nuevo_usuario.id,
                    "dni": dni,
                    "nombre": nombre_completo
                })

            except Exception as e:
                errores.append(f"Fila {idx}: {str(e)}")

        if usuarios_creados:
            db.commit()

        return {
            "success": True,
            "mensaje": f"Se importaron {len(usuarios_creados)} usuarios",
            "usuarios_creados": usuarios_creados,
            "errores": errores,
            "total_filas_procesadas": len(usuarios_creados) + len(errores)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error importando archivo: {str(e)}")

@router.post("/vincular-fotos")
async def vincular_fotos(db: Session = Depends(get_db)):
    """Vincular automaticamente fotos frontales a los usuarios.
    Las fotos deben estar en uploads/usuarios/ nombradas por DNI (ej: 12345678.png)"""
    EXTENSIONES_PERMITIDAS = {'.png', '.jpg', '.jpeg', '.webp'}

    if not UPLOAD_DIR.exists():
        raise HTTPException(status_code=400, detail=f"Carpeta {UPLOAD_DIR} no existe")

    fotos_encontradas = [f for f in UPLOAD_DIR.glob("*") if f.is_file()]

    vinculados = 0
    no_encontrados = 0
    ya_vinculados = 0
    errores = 0

    for foto_path in fotos_encontradas:
        ext = foto_path.suffix.lower()
        if ext not in EXTENSIONES_PERMITIDAS:
            continue

        dni = foto_path.stem

        usuario = db.query(Usuario).filter(Usuario.numero_dni == dni).first()

        if not usuario:
            no_encontrados += 1
            continue

        ruta_relativa = f"uploads/usuarios/{foto_path.name}"

        if usuario.foto_frontal and usuario.foto_frontal != "":
            ya_vinculados += 1
            continue

        try:
            usuario.foto_frontal = ruta_relativa
            db.commit()
            vinculados += 1
        except Exception as e:
            db.rollback()
            errores += 1

    return {
        "success": True,
        "mensaje": f"Fotos vinculadas: {vinculados}, ya tenian foto: {ya_vinculados}, no encontrados: {no_encontrados}, errores: {errores}",
        "resumen": {
            "vinculados": vinculados,
            "ya_vinculados": ya_vinculados,
            "no_encontrados": no_encontrados,
            "errores": errores,
            "total_procesadas": len(fotos_encontradas)
        }
    }


@router.post("/vincular-fotos")
async def vincular_fotos(db: Session = Depends(get_db)):
    """Vincular automaticamente fotos frontales a los usuarios.
    Las fotos deben estar en uploads/usuarios/ nombradas por DNI (ej: 12345678.png)"""
    EXTENSIONES_PERMITIDAS = {'.png', '.jpg', '.jpeg', '.webp'}

    if not UPLOAD_DIR.exists():
        raise HTTPException(status_code=400, detail=f"Carpeta {UPLOAD_DIR} no existe")

    fotos_encontradas = [f for f in UPLOAD_DIR.glob("*") if f.is_file()]

    vinculados = 0
    no_encontrados = 0
    ya_vinculados = 0
    errores = 0

    for foto_path in fotos_encontradas:
        ext = foto_path.suffix.lower()
        if ext not in EXTENSIONES_PERMITIDAS:
            continue

        dni = foto_path.stem

        usuario = db.query(Usuario).filter(Usuario.numero_dni == dni).first()

        if not usuario:
            no_encontrados += 1
            continue

        ruta_relativa = f"uploads/usuarios/{foto_path.name}"

        if usuario.foto_frontal and usuario.foto_frontal != "":
            ya_vinculados += 1
            continue

        try:
            usuario.foto_frontal = ruta_relativa
            db.commit()
            vinculados += 1
        except Exception as e:
            db.rollback()
            errores += 1

    return {
        "success": True,
        "mensaje": f"Fotos vinculadas: {vinculados}, ya tenian foto: {ya_vinculados}, no encontrados: {no_encontrados}, errores: {errores}",
        "resumen": {
            "vinculados": vinculados,
            "ya_vinculados": ya_vinculados,
            "no_encontrados": no_encontrados,
            "errores": errores,
            "total_procesadas": len(fotos_encontradas)
        }
    }
