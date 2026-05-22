from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
from datetime import datetime
from typing import Optional, List
from concurrent.futures import ThreadPoolExecutor
from app.db.database import get_db
from app.models.usuario import Usuario
from app.models.configuracion import ConfiguracionCarnet
from app.services.carnet_pdf_service import generar_pdf_carnets
from app.services.carnet_task_manager import get_gestor_tareas, EstadoProgreso

router = APIRouter(prefix="/api/carnets", tags=["carnets"])

EXTENSIONES_PERMITIDAS = {'.png', '.jpg', '.jpeg', '.webp'}
UPLOAD_DIR = Path("uploads/usuarios")

# ThreadPool para Playwright (sin event loop de asyncio)
_thread_pool = ThreadPoolExecutor(max_workers=2, thread_name_prefix="playwright")


@router.get("/exportar-pdf")
def exportar_pdf(
    limit: int = Query(200, ge=1, le=2000, description="Cantidad de carnets a generar"),
    offset: int = Query(0, ge=0, description="Desde qué usuario empezar"),
    todos: bool = Query(False, description="Si es True, ignora limit y genera todos"),
    db: Session = Depends(get_db),
):
    """
    Genera un PDF vectorial con los carnets usando Chromium headless (Playwright).
    Calidad superior al render canvas-a-imagen del frontend.
    """
    query = db.query(Usuario).order_by(Usuario.id.asc())

    if todos:
        usuarios = query.all()
    else:
        usuarios = query.offset(offset).limit(limit).all()

    if not usuarios:
        raise HTTPException(status_code=404, detail="No hay usuarios en el rango solicitado")

    config = db.query(ConfiguracionCarnet).first()
    if not config:
        config = ConfiguracionCarnet()

    # Precargar atributos antes de pasarlos al thread
    for u in usuarios:
        _ = u.id, u.numero_dni, u.nombres, u.apellido_paterno, u.apellido_materno
        _ = u.estado_civil, u.fecha_nacimiento, u.anexo, u.num_padron, u.foto_frontal

    _ = config.nombre_comunidad, config.resolucion, config.nombre_corto, config.url_qr
    _ = config.bandera_url, config.escudo_url, config.fondo_anverso_url, config.fondo_reverso_url
    _ = config.firma_secretario_url, config.firma_presidente_url

    try:
        # Ejecutar en thread pool separado (sin event loop asyncio)
        pdf_bytes = _thread_pool.submit(generar_pdf_carnets, usuarios, config).result()
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generando PDF: {e}")

    if todos:
        nombre = f"carnets-todos-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.pdf"
    else:
        nombre = f"carnets-{offset + 1}-{offset + len(usuarios)}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nombre}"'},
    )


@router.get("/exportar-pdf-individual/{usuario_id}")
def exportar_pdf_individual(usuario_id: int, db: Session = Depends(get_db)):
    """Genera el PDF de un solo carnet."""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    config = db.query(ConfiguracionCarnet).first()
    if not config:
        config = ConfiguracionCarnet()

    # Precargar atributos
    _ = usuario.id, usuario.numero_dni, usuario.nombres, usuario.apellido_paterno, usuario.apellido_materno
    _ = usuario.estado_civil, usuario.fecha_nacimiento, usuario.anexo, usuario.num_padron, usuario.foto_frontal
    _ = config.nombre_comunidad, config.resolucion, config.nombre_corto, config.url_qr
    _ = config.bandera_url, config.escudo_url, config.fondo_anverso_url, config.fondo_reverso_url
    _ = config.firma_secretario_url, config.firma_presidente_url

    try:
        # Ejecutar en thread pool separado
        pdf_bytes = _thread_pool.submit(generar_pdf_carnets, [usuario], config).result()
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generando PDF: {e}")

    nombre = f"carnet-{usuario.numero_dni or usuario.id}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nombre}"'},
    )


@router.post("/exportar-async")
def exportar_async(
    limit: int = Query(200, ge=1, le=2000),
    offset: int = Query(0, ge=0),
    todos: bool = Query(False),
    db: Session = Depends(get_db),
):
    """
    Inicia una exportación asincrónica de carnets.
    Retorna task_id para trackear progreso.
    Máximo 2 exportaciones simultáneos en el servidor.
    """
    query = db.query(Usuario).order_by(Usuario.id.asc())

    if todos:
        usuarios_raw = query.all()
    else:
        usuarios_raw = query.offset(offset).limit(limit).all()

    if not usuarios_raw:
        raise HTTPException(status_code=404, detail="No hay usuarios en el rango solicitado")

    config_raw = db.query(ConfiguracionCarnet).first()
    if not config_raw:
        config_raw = ConfiguracionCarnet()

    # Forzar carga de todos los atributos AQUÍ (antes de pasar a thread)
    # Acceder a todos los atributos para que se carguen desde la DB
    usuarios = usuarios_raw
    for u in usuarios:
        _ = u.id, u.numero_dni, u.nombres, u.apellido_paterno, u.apellido_materno
        _ = u.estado_civil, u.fecha_nacimiento, u.anexo, u.num_padron, u.foto_frontal

    config = config_raw
    _ = config.nombre_comunidad, config.resolucion, config.nombre_corto, config.url_qr
    _ = config.bandera_url, config.escudo_url, config.fondo_anverso_url, config.fondo_reverso_url
    _ = config.firma_secretario_url, config.firma_presidente_url

    # Crear tarea
    gestor = get_gestor_tareas()
    task_id = gestor.crear_tarea(len(usuarios))

    # Función que ejecutará en thread (captura usuarios y config del closure)
    def generar_en_thread(task_id_local: str, callback):
        # Los atributos ya están cargados, no hay lazy loading
        return generar_pdf_carnets(usuarios, config, callback=callback)

    # Ejecutar en background (con límite de workers)
    gestor.ejecutar_tarea(task_id, generar_en_thread)

    return {
        "task_id": task_id,
        "estado": "pendiente",
        "mensaje": "Exportación encolada"
    }


@router.get("/tarea/{task_id}")
def obtener_estado_tarea(task_id: str):
    """Obtiene el estado actual de una exportación."""
    gestor = get_gestor_tareas()
    tarea = gestor.obtener_estado(task_id)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    return tarea.to_dict()


@router.get("/descargar/{task_id}")
def descargar_pdf_tarea(task_id: str):
    """Descarga el PDF de una tarea completada."""
    gestor = get_gestor_tareas()
    tarea = gestor.obtener_estado(task_id)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    if tarea.estado.value != "completada":
        raise HTTPException(
            status_code=400,
            detail=f"PDF no está listo. Estado actual: {tarea.estado.value}"
        )

    pdf_bytes = gestor.obtener_pdf(task_id)
    if not pdf_bytes:
        raise HTTPException(status_code=500, detail="Error: PDF no encontrado en caché")

    # Determinar nombre
    if tarea.total_carnets == 1:
        nombre = f"carnet.pdf"
    else:
        nombre = f"carnets-{tarea.total_carnets}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nombre}"'},
    )


@router.post("/vincular-fotos")
def vincular_fotos(db: Session = Depends(get_db)):
    """Vincula automáticamente las fotos frontales a usuarios por DNI"""

    if not UPLOAD_DIR.exists():
        return {
            "success": False,
            "error": f"Carpeta {UPLOAD_DIR} no existe",
            "resumen": {
                "vinculados": 0,
                "ya_vinculados": 0,
                "no_encontrados": 0,
                "errores": 0,
                "total": 0
            }
        }

    fotos_encontradas = list(UPLOAD_DIR.glob("*"))

    vinculados = 0
    no_encontrados = 0
    ya_vinculados = 0
    errores = 0
    detalles = []

    for foto_path in fotos_encontradas:
        if not foto_path.is_file():
            continue

        ext = foto_path.suffix.lower()
        if ext not in EXTENSIONES_PERMITIDAS:
            continue

        # Extraer DNI del nombre del archivo
        dni = foto_path.stem

        # Buscar usuario
        usuario = db.query(Usuario).filter(Usuario.numero_dni == dni).first()

        if not usuario:
            detalles.append({
                "dni": dni,
                "estado": "no_encontrado",
                "mensaje": "Usuario no encontrado"
            })
            no_encontrados += 1
            continue

        # Ruta relativa para almacenar
        ruta_relativa = f"uploads/usuarios/{foto_path.name}"

        # Verificar si ya tiene foto frontal
        if usuario.foto_frontal and usuario.foto_frontal != "":
            detalles.append({
                "dni": dni,
                "nombre": usuario.nombre_completo,
                "estado": "ya_vinculada",
                "mensaje": "Ya tiene foto frontal"
            })
            ya_vinculados += 1
            continue

        try:
            # Actualizar
            usuario.foto_frontal = ruta_relativa
            db.commit()
            detalles.append({
                "dni": dni,
                "nombre": usuario.nombre_completo,
                "estado": "vinculada",
                "mensaje": "Foto vinculada correctamente"
            })
            vinculados += 1
        except Exception as e:
            db.rollback()
            detalles.append({
                "dni": dni,
                "estado": "error",
                "mensaje": f"Error al vincular: {str(e)}"
            })
            errores += 1

    total = vinculados + ya_vinculados + no_encontrados + errores

    return {
        "success": True,
        "resumen": {
            "vinculados": vinculados,
            "ya_vinculados": ya_vinculados,
            "no_encontrados": no_encontrados,
            "errores": errores,
            "total": total
        },
        "detalles": detalles if len(detalles) <= 100 else detalles[:100]  # Limitar a 100 para no sobrecargar
    }


@router.post("/cargar-fotos")
async def cargar_fotos(archivos: list[UploadFile] = File(...)):
    """Carga fotos directamente a uploads/usuarios/ usando el nombre del archivo como DNI"""

    # Crear directorio si no existe
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    cargadas = 0
    errores = 0
    detalles = []

    for archivo in archivos:
        try:
            # Validar extensión
            ext = Path(archivo.filename).suffix.lower()
            if ext not in EXTENSIONES_PERMITIDAS:
                detalles.append({
                    "archivo": archivo.filename,
                    "estado": "error",
                    "mensaje": f"Extensión no permitida: {ext}"
                })
                errores += 1
                continue

            # Guardar archivo
            ruta_archivo = UPLOAD_DIR / archivo.filename

            with open(ruta_archivo, "wb") as buffer:
                shutil.copyfileobj(archivo.file, buffer)

            detalles.append({
                "archivo": archivo.filename,
                "estado": "cargado",
                "mensaje": "Foto cargada correctamente"
            })
            cargadas += 1

        except Exception as e:
            detalles.append({
                "archivo": archivo.filename,
                "estado": "error",
                "mensaje": f"Error: {str(e)}"
            })
            errores += 1

    return {
        "success": True,
        "resumen": {
            "cargadas": cargadas,
            "errores": errores,
            "total": len(archivos)
        },
        "detalles": detalles,
        "mensaje": f"✅ {cargadas} foto(s) cargada(s) exitosamente. Ahora puedes hacer clic en 'Vincular Fotos' para asociarlas a los usuarios."
    }
