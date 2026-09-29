"""
Rutas para la gestión de Galerías (Álbumes) y Fotografías Comunitarias.
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
import os
import secrets
import re

from app.db.database import get_db
from app.models.galeria import Galeria, FotoGaleria
from app.models.usuario import Usuario
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/galeria", tags=["Galeria"])

# ==================== DATOS POR DEFECTO INICIALES ====================

DEFAULT_GALERIAS = [
    {
        "id": 1,
        "titulo": "Identidad y Tradición Comunal",
        "slug": "identidad-y-tradicion-comunal",
        "descripcion": "Vivencias, costumbres, vestimentas típicas y la rica herencia cultural de nuestra comunidad.",
        "categoria": "comunidad",
        "categoria_label": "Comunidad",
        "portada": "/uploads/img/web/2.png",
        "fecha": "2026",
        "lugar": "Cerro Baúl / Moquegua",
        "destacada": True,
        "orden": 1,
        "activo": True,
        "fotos": [
            {
                "titulo": "Identidad comunal",
                "desc": "Mujeres de la comunidad con vestimenta tradicional frente al Cerro Baúl, símbolo del territorio.",
                "categoria": "comunidad",
                "categoria_label": "Comunidad",
                "grande": True,
                "img": "/uploads/img/web/2.png",
                "orden": 1,
                "activo": True
            },
            {
                "titulo": "Anexo Tumilaca",
                "desc": "Vista del anexo de Tumilaca, corazón productivo del valle.",
                "categoria": "comunidad",
                "categoria_label": "Comunidad",
                "grande": False,
                "img": "/uploads/img/nosotros/tumilala.png",
                "orden": 2,
                "activo": True
            },
            {
                "titulo": "Tumilaca en acción",
                "desc": "Actividades cotidianas de los Usuarios en el anexo de Tumilaca.",
                "categoria": "comunidad",
                "categoria_label": "Comunidad",
                "grande": False,
                "img": "/uploads/img/nosotros/tumilala2.png",
                "orden": 3,
                "activo": True
            },
            {
                "titulo": "Plaza de Moquegua",
                "desc": "Centro histórico de la ciudad de Moquegua, capital de la región.",
                "categoria": "comunidad",
                "categoria_label": "Comunidad",
                "grande": False,
                "img": "/uploads/img/web/1.jpeg",
                "orden": 4,
                "activo": True
            }
        ]
    },
    {
        "id": 2,
        "titulo": "Territorio y Paisajes Ancestrales",
        "slug": "territorio-y-paisajes-ancestrales",
        "descripcion": "Panorámicas de nuestros cerros tutelares, valles agrícolas, cementerios históricos y fauna andina.",
        "categoria": "territorio",
        "categoria_label": "Territorio",
        "portada": "/uploads/img/inicio/cerro_baul.png",
        "fecha": "2026",
        "lugar": "Distrito de Torata",
        "destacada": True,
        "orden": 2,
        "activo": True,
        "fotos": [
            {
                "titulo": "Cerro Baúl",
                "desc": "Hito arqueológico y cultural emblemático del territorio comunal.",
                "categoria": "territorio",
                "categoria_label": "Territorio",
                "grande": True,
                "img": "/uploads/img/inicio/cerro_baul.png",
                "orden": 1,
                "activo": True
            },
            {
                "titulo": "Cementerio de Pocata",
                "desc": "Cementerio comunal histórico del anexo Pocata.",
                "categoria": "territorio",
                "categoria_label": "Territorio",
                "grande": False,
                "img": "/uploads/img/inicio/cementerio_pocata.png",
                "orden": 2,
                "activo": True
            },
            {
                "titulo": "Vista del valle",
                "desc": "Panorámica del territorio comunal en el distrito de Torata.",
                "categoria": "territorio",
                "categoria_label": "Territorio",
                "grande": False,
                "img": "/uploads/img/inicio/01.png",
                "orden": 3,
                "activo": True
            },
            {
                "titulo": "Fauna andina",
                "desc": "Llama andina, parte del patrimonio ganadero del altiplano comunal.",
                "categoria": "territorio",
                "categoria_label": "Territorio",
                "grande": False,
                "img": "/uploads/img/web/4.jpeg",
                "orden": 4,
                "activo": True
            }
        ]
    },
    {
        "id": 3,
        "titulo": "Trabajo Agrícola y ECOSER",
        "slug": "trabajo-agricola-y-ecoser",
        "descripcion": "Labores del campo y los servicios empresariales que brinda nuestra empresa comunal ECOSER.",
        "categoria": "actividades",
        "categoria_label": "Actividades",
        "portada": "/uploads/img/web/3.jpeg",
        "fecha": "2026",
        "lugar": "Valle y Operaciones",
        "destacada": False,
        "orden": 3,
        "activo": True,
        "fotos": [
            {
                "titulo": "Trabajo agrícola",
                "desc": "Producción agrícola en el valle, sustento de las familias comuneras.",
                "categoria": "actividades",
                "categoria_label": "Actividades",
                "grande": True,
                "img": "/uploads/img/web/3.jpeg",
                "orden": 1,
                "activo": True
            },
            {
                "titulo": "ECOSER en operaciones",
                "desc": "Trabajos de la empresa comunal ECOSER en el territorio.",
                "categoria": "actividades",
                "categoria_label": "Actividades",
                "grande": False,
                "img": "/uploads/img/ecoser/01.png",
                "orden": 2,
                "activo": True
            },
            {
                "titulo": "Equipo ECOSER",
                "desc": "Mano de obra local capacitada para servicios diversos.",
                "categoria": "actividades",
                "categoria_label": "Actividades",
                "grande": False,
                "img": "/uploads/img/ecoser/02.png",
                "orden": 3,
                "activo": True
            },
            {
                "titulo": "Servicios al territorio",
                "desc": "ECOSER brindando servicios a la comunidad y empresas de la zona.",
                "categoria": "actividades",
                "categoria_label": "Actividades",
                "grande": False,
                "img": "/uploads/img/ecoser/03.png",
                "orden": 4,
                "activo": True
            }
        ]
    }
]


def generar_slug(texto: str) -> str:
    texto = texto.lower().strip()
    texto = re.sub(r'[áàäâ]', 'a', texto)
    texto = re.sub(r'[éèëê]', 'e', texto)
    texto = re.sub(r'[íìïî]', 'i', texto)
    texto = re.sub(r'[óòöô]', 'o', texto)
    texto = re.sub(r'[úùüû]', 'u', texto)
    texto = re.sub(r'[ñ]', 'n', texto)
    texto = re.sub(r'[^a-z0-9]+', '-', texto)
    return texto.strip('-')


def asegurar_datos_iniciales(db: Session):
    """Siembra galerías iniciales si la base de datos está vacía."""
    count = db.query(Galeria).count()
    if count == 0:
        for g_data in DEFAULT_GALERIAS:
            fotos_data = g_data.get("fotos", [])
            galeria = Galeria(
                titulo=g_data["titulo"],
                slug=g_data.get("slug") or generar_slug(g_data["titulo"]),
                descripcion=g_data.get("descripcion", ""),
                categoria=g_data.get("categoria", "comunidad"),
                categoria_label=g_data.get("categoria_label", "Comunidad"),
                portada=g_data.get("portada", ""),
                fecha=g_data.get("fecha", ""),
                lugar=g_data.get("lugar", ""),
                destacada=g_data.get("destacada", False),
                orden=g_data.get("orden", 1),
                activo=g_data.get("activo", True)
            )
            db.add(galeria)
            db.commit()
            db.refresh(galeria)

            for f_data in fotos_data:
                foto = FotoGaleria(
                    galeria_id=galeria.id,
                    titulo=f_data["titulo"],
                    desc=f_data.get("desc", ""),
                    categoria=galeria.categoria,
                    categoria_label=galeria.categoria_label,
                    img=f_data["img"],
                    grande=f_data.get("grande", False),
                    orden=f_data.get("orden", 1),
                    activo=f_data.get("activo", True)
                )
                db.add(foto)
            db.commit()


# ==================== SCHEMAS ====================

class GaleriaCreate(BaseModel):
    titulo: str
    descripcion: Optional[str] = ""
    categoria: Optional[str] = "comunidad"
    categoria_label: Optional[str] = "Comunidad"
    portada: Optional[str] = ""
    fecha: Optional[str] = ""
    lugar: Optional[str] = ""
    destacada: Optional[bool] = False
    orden: Optional[int] = 0
    activo: Optional[bool] = True


class GaleriaUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    categoria_label: Optional[str] = None
    portada: Optional[str] = None
    fecha: Optional[str] = None
    lugar: Optional[str] = None
    destacada: Optional[bool] = None
    orden: Optional[int] = None
    activo: Optional[bool] = None


class FotoCreate(BaseModel):
    galeria_id: int
    titulo: str
    desc: Optional[str] = ""
    img: str
    grande: Optional[bool] = False
    orden: Optional[int] = 0
    activo: Optional[bool] = True


class FotoUpdate(BaseModel):
    titulo: Optional[str] = None
    desc: Optional[str] = None
    img: Optional[str] = None
    grande: Optional[bool] = None
    orden: Optional[int] = None
    activo: Optional[bool] = None


# ==================== RUTAS PÚBLICAS ====================

@router.get("")
@router.get("/publico")
async def listar_galerias_publico(
    categoria: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Lista las galerías/álbumes activos con el conteo de fotos e información general.
    """
    asegurar_datos_iniciales(db)

    query = db.query(Galeria).filter(Galeria.activo == True)
    if categoria and categoria != "todas":
        query = query.filter(Galeria.categoria == categoria)

    galerias = query.order_by(Galeria.orden.asc(), Galeria.id.asc()).all()

    # Categorías disponibles
    todas = db.query(Galeria).filter(Galeria.activo == True).all()
    cat_map = {}
    for g in todas:
        if g.categoria and g.categoria not in cat_map:
            cat_map[g.categoria] = g.categoria_label or g.categoria.capitalize()

    filtros = [{"key": "todas", "label": "Todas"}]
    for k, v in cat_map.items():
        filtros.append({"key": k, "label": v})

    resultado = []
    for g in galerias:
        fotos_db = db.query(FotoGaleria).filter(FotoGaleria.galeria_id == g.id, FotoGaleria.activo == True).order_by(FotoGaleria.orden.asc(), FotoGaleria.id.asc()).all()
        fotos_list = [{
            "id": f.id,
            "galeria_id": f.galeria_id,
            "titulo": f.titulo,
            "desc": f.desc,
            "categoria": f.categoria,
            "categoriaLabel": f.categoria_label,
            "img": f.img,
            "grande": f.grande,
            "orden": f.orden,
            "activo": f.activo
        } for f in fotos_db]

        # Si no tiene portada explícita, usar la primera foto
        portada = g.portada
        if not portada and len(fotos_list) > 0:
            portada = fotos_list[0]["img"]

        resultado.append({
            "id": g.id,
            "titulo": g.titulo,
            "slug": g.slug,
            "descripcion": g.descripcion,
            "categoria": g.categoria,
            "categoriaLabel": g.categoria_label,
            "portada": portada or "/uploads/img/web/2.png",
            "fecha": g.fecha,
            "lugar": g.lugar,
            "destacada": g.destacada,
            "orden": g.orden,
            "totalFotos": len(fotos_list),
            "fotos": fotos_list
        })

    return {
        "success": True,
        "total": len(resultado),
        "filtros": filtros,
        "galerias": resultado
    }


@router.get("/detalle/{id_o_slug}")
async def obtener_galeria_detalle(
    id_o_slug: str,
    db: Session = Depends(get_db)
):
    """
    Obtiene una galería específica con todas sus fotos activas.
    """
    asegurar_datos_iniciales(db)

    galeria = None
    if id_o_slug.isdigit():
        galeria = db.query(Galeria).filter(Galeria.id == int(id_o_slug)).first()
    if not galeria:
        galeria = db.query(Galeria).filter(Galeria.slug == id_o_slug).first()

    if not galeria:
        raise HTTPException(status_code=404, detail="Galería no encontrada")

    fotos = db.query(FotoGaleria).filter(
        FotoGaleria.galeria_id == galeria.id,
        FotoGaleria.activo == True
    ).order_by(FotoGaleria.orden.asc(), FotoGaleria.id.asc()).all()

    return {
        "success": True,
        "galeria": {
            "id": galeria.id,
            "titulo": galeria.titulo,
            "slug": galeria.slug,
            "descripcion": galeria.descripcion,
            "categoria": galeria.categoria,
            "categoriaLabel": galeria.categoria_label,
            "portada": galeria.portada,
            "fecha": galeria.fecha,
            "lugar": galeria.lugar,
            "destacada": galeria.destacada
        },
        "fotos": [
            {
                "id": f.id,
                "titulo": f.titulo,
                "desc": f.desc,
                "img": f.img,
                "grande": f.grande,
                "orden": f.orden
            }
            for f in fotos
        ]
    }


# ==================== RUTAS ADMINISTRACIÓN ====================

@router.get("/admin/todas")
async def listar_galerias_admin(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista todas las galerías con sus fotos y estadísticas para el panel admin."""
    if usuario.rol not in ["admin", "editor", "moderator"]:
        raise HTTPException(status_code=403, detail="No autorizado")

    asegurar_datos_iniciales(db)

    galerias = db.query(Galeria).order_by(Galeria.orden.asc(), Galeria.id.asc()).all()

    lista = []
    for g in galerias:
        fotos = db.query(FotoGaleria).filter(FotoGaleria.galeria_id == g.id).order_by(FotoGaleria.orden.asc()).all()
        lista.append({
            "id": g.id,
            "titulo": g.titulo,
            "slug": g.slug,
            "descripcion": g.descripcion,
            "categoria": g.categoria,
            "categoriaLabel": g.categoria_label,
            "portada": g.portada,
            "fecha": g.fecha,
            "lugar": g.lugar,
            "destacada": g.destacada,
            "orden": g.orden,
            "activo": g.activo,
            "totalFotos": len(fotos),
            "fotos": [
                {
                    "id": f.id,
                    "galeria_id": f.galeria_id,
                    "titulo": f.titulo,
                    "desc": f.desc,
                    "img": f.img,
                    "grande": f.grande,
                    "orden": f.orden,
                    "activo": f.activo
                }
                for f in fotos
            ]
        })

    return {"success": True, "galerias": lista}


@router.post("/admin/galeria")
async def crear_galeria(
    datos: GaleriaCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crea una nueva galería/álbum."""
    if usuario.rol not in ["admin", "editor"]:
        raise HTTPException(status_code=403, detail="No autorizado")

    orden = datos.orden
    if not orden:
        orden = db.query(Galeria).count() + 1

    slug = generar_slug(datos.titulo)
    categoria_label = datos.categoria_label or datos.categoria.capitalize()

    nueva = Galeria(
        titulo=datos.titulo.strip(),
        slug=slug,
        descripcion=datos.descripcion.strip() if datos.descripcion else "",
        categoria=datos.categoria.strip().lower() if datos.categoria else "comunidad",
        categoria_label=categoria_label,
        portada=datos.portada.strip() if datos.portada else "",
        fecha=datos.fecha.strip() if datos.fecha else "",
        lugar=datos.lugar.strip() if datos.lugar else "",
        destacada=bool(datos.destacada),
        orden=orden,
        activo=bool(datos.activo)
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return {
        "success": True,
        "mensaje": f"Galería '{nueva.titulo}' creada con éxito",
        "galeria": {
            "id": nueva.id,
            "titulo": nueva.titulo,
            "slug": nueva.slug,
            "descripcion": nueva.descripcion,
            "categoria": nueva.categoria,
            "categoriaLabel": nueva.categoria_label,
            "portada": nueva.portada,
            "fecha": nueva.fecha,
            "lugar": nueva.lugar,
            "destacada": nueva.destacada,
            "orden": nueva.orden,
            "activo": nueva.activo,
            "totalFotos": 0,
            "fotos": []
        }
    }


@router.put("/admin/galeria/{galeria_id}")
async def actualizar_galeria(
    galeria_id: int,
    datos: GaleriaUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualiza una galería."""
    if usuario.rol not in ["admin", "editor"]:
        raise HTTPException(status_code=403, detail="No autorizado")

    galeria = db.query(Galeria).filter(Galeria.id == galeria_id).first()
    if not galeria:
        raise HTTPException(status_code=404, detail="Galería no encontrada")

    if datos.titulo is not None:
        galeria.titulo = datos.titulo.strip()
        galeria.slug = generar_slug(galeria.titulo)
    if datos.descripcion is not None:
        galeria.descripcion = datos.descripcion.strip()
    if datos.categoria is not None:
        galeria.categoria = datos.categoria.strip().lower()
    if datos.categoria_label is not None:
        galeria.categoria_label = datos.categoria_label.strip()
    if datos.portada is not None:
        galeria.portada = datos.portada.strip()
    if datos.fecha is not None:
        galeria.fecha = datos.fecha.strip()
    if datos.lugar is not None:
        galeria.lugar = datos.lugar.strip()
    if datos.destacada is not None:
        galeria.destacada = bool(datos.destacada)
    if datos.orden is not None:
        galeria.orden = datos.orden
    if datos.activo is not None:
        galeria.activo = bool(datos.activo)

    galeria.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(galeria)

    return {"success": True, "mensaje": "Galería actualizada", "galeria": galeria}


@router.delete("/admin/galeria/{galeria_id}")
async def eliminar_galeria(
    galeria_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Elimina una galería y todas sus fotos."""
    if usuario.rol not in ["admin", "editor"]:
        raise HTTPException(status_code=403, detail="No autorizado")

    galeria = db.query(Galeria).filter(Galeria.id == galeria_id).first()
    if not galeria:
        raise HTTPException(status_code=404, detail="Galería no encontrada")

    db.delete(galeria)
    db.commit()

    return {"success": True, "mensaje": "Galería eliminada correctamente"}


# ==================== GESTIÓN DE FOTOS DENTRO DE GALERÍAS ====================

@router.post("/admin/fotos")
async def agregar_foto(
    datos: FotoCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Agrega una foto a una galería específica."""
    if usuario.rol not in ["admin", "editor"]:
        raise HTTPException(status_code=403, detail="No autorizado")

    galeria = db.query(Galeria).filter(Galeria.id == datos.galeria_id).first()
    if not galeria:
        raise HTTPException(status_code=404, detail="Galería asociada no encontrada")

    orden = datos.orden
    if not orden:
        orden = db.query(FotoGaleria).filter(FotoGaleria.galeria_id == datos.galeria_id).count() + 1

    nueva_foto = FotoGaleria(
        galeria_id=datos.galeria_id,
        titulo=datos.titulo.strip(),
        desc=datos.desc.strip() if datos.desc else "",
        categoria=galeria.categoria,
        categoria_label=galeria.categoria_label,
        img=datos.img.strip(),
        grande=bool(datos.grande),
        orden=orden,
        activo=bool(datos.activo)
    )

    db.add(nueva_foto)

    # Si la galería no tiene portada, asignarle esta primera foto
    if not galeria.portada:
        galeria.portada = nueva_foto.img

    db.commit()
    db.refresh(nueva_foto)

    return {
        "success": True,
        "mensaje": "Foto agregada a la galería",
        "foto": {
            "id": nueva_foto.id,
            "galeria_id": nueva_foto.galeria_id,
            "titulo": nueva_foto.titulo,
            "desc": nueva_foto.desc,
            "img": nueva_foto.img,
            "grande": nueva_foto.grande,
            "orden": nueva_foto.orden,
            "activo": nueva_foto.activo
        }
    }


@router.put("/admin/fotos/{foto_id}")
async def actualizar_foto(
    foto_id: int,
    datos: FotoUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualiza una fotografía."""
    if usuario.rol not in ["admin", "editor"]:
        raise HTTPException(status_code=403, detail="No autorizado")

    foto = db.query(FotoGaleria).filter(FotoGaleria.id == foto_id).first()
    if not foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")

    if datos.titulo is not None:
        foto.titulo = datos.titulo.strip()
    if datos.desc is not None:
        foto.desc = datos.desc.strip()
    if datos.img is not None:
        foto.img = datos.img.strip()
    if datos.grande is not None:
        foto.grande = bool(datos.grande)
    if datos.orden is not None:
        foto.orden = datos.orden
    if datos.activo is not None:
        foto.activo = bool(datos.activo)

    foto.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(foto)

    return {"success": True, "mensaje": "Foto actualizada", "foto": foto}


@router.delete("/admin/fotos/{foto_id}")
async def eliminar_foto(
    foto_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Elimina una fotografía."""
    if usuario.rol not in ["admin", "editor"]:
        raise HTTPException(status_code=403, detail="No autorizado")

    foto = db.query(FotoGaleria).filter(FotoGaleria.id == foto_id).first()
    if not foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")

    db.delete(foto)
    db.commit()

    return {"success": True, "mensaje": "Foto eliminada"}


@router.post("/admin/upload")
async def subir_imagen_galeria(
    file: UploadFile = File(...),
    usuario: Usuario = Depends(get_current_user)
):
    """Sube una imagen al servidor para las galerías o fotos."""
    if usuario.rol not in ["admin", "editor"]:
        raise HTTPException(status_code=403, detail="No autorizado")

    ext = os.path.splitext(file.filename)[1].lower() if file.filename else ".jpg"
    if ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
        raise HTTPException(status_code=400, detail="Formato no permitido (use JPG, PNG, WEBP)")

    upload_dir = "uploads/galeria"
    os.makedirs(upload_dir, exist_ok=True)

    token = secrets.token_hex(8)
    filename = f"img_{token}{ext}"
    file_path = os.path.join(upload_dir, filename)

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    url_relativa = f"/uploads/galeria/{filename}"
    return {
        "success": True,
        "url": url_relativa,
        "filename": filename,
        "mensaje": "Imagen subida exitosamente"
    }


@router.post("/admin/fotos/batch")
async def subir_fotos_batch(
    galeria_id: int = Query(...),
    files: List[UploadFile] = File(...),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Sube múltiples fotografías a la vez a una galería específica."""
    if usuario.rol not in ["admin", "editor"]:
        raise HTTPException(status_code=403, detail="No autorizado")

    galeria = db.query(Galeria).filter(Galeria.id == galeria_id).first()
    if not galeria:
        raise HTTPException(status_code=404, detail="Galería no encontrada")

    upload_dir = "uploads/galeria"
    os.makedirs(upload_dir, exist_ok=True)

    fotos_creadas = []
    max_orden = db.query(FotoGaleria).filter(FotoGaleria.galeria_id == galeria_id).count()

    for idx, file in enumerate(files):
        ext = os.path.splitext(file.filename)[1].lower() if file.filename else ".jpg"
        if ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
            continue

        token = secrets.token_hex(8)
        filename = f"img_{token}{ext}"
        file_path = os.path.join(upload_dir, filename)

        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        url_relativa = f"/uploads/galeria/{filename}"

        nombre_base = os.path.splitext(file.filename)[0] if file.filename else "Fotografía"
        titulo_limpio = nombre_base.replace("_", " ").replace("-", " ").strip()
        if not titulo_limpio:
            titulo_limpio = f"Fotografía {idx + 1}"

        max_orden += 1
        nueva_foto = FotoGaleria(
            galeria_id=galeria.id,
            titulo=titulo_limpio,
            desc="",
            categoria=galeria.categoria,
            categoria_label=galeria.categoria_label,
            img=url_relativa,
            grande=False,
            orden=max_orden,
            activo=True
        )
        db.add(nueva_foto)
        fotos_creadas.append(nueva_foto)

    if not galeria.portada and fotos_creadas:
        galeria.portada = fotos_creadas[0].img

    db.commit()

    return {
        "success": True,
        "mensaje": f"{len(fotos_creadas)} fotografías agregadas a la galería",
        "total": len(fotos_creadas)
    }


@router.post("/admin/restablecer-defaults")
async def restablecer_defaults(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Restablece las galerías institucionales iniciales con sus fotos."""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede restablecer")

    db.query(FotoGaleria).delete()
    db.query(Galeria).delete()
    db.commit()

    asegurar_datos_iniciales(db)
    return {"success": True, "mensaje": "Galerías iniciales restablecidas con éxito"}
