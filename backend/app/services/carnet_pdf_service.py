"""
Servicio para generar PDFs de carnets de alta calidad usando Playwright (Chromium headless).
Renderiza el HTML/CSS exacto del template y genera PDFs vectoriales.
"""

import base64
import io
import mimetypes
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import qrcode
from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.sync_api import sync_playwright

from app.models.usuario import Usuario


BACKEND_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = BACKEND_ROOT / "app" / "templates"

_jinja_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html"]),
)


def _file_to_data_uri(ruta: Optional[str]) -> Optional[str]:
    """Convierte una ruta (relativa al backend) a data URI base64."""
    if not ruta:
        return None

    ruta_limpia = ruta.lstrip("/")
    posibles = [
        BACKEND_ROOT / ruta_limpia,
        BACKEND_ROOT / "uploads" / Path(ruta_limpia).name,
    ]
    archivo = next((p for p in posibles if p.exists() and p.is_file()), None)
    if not archivo:
        return None

    mime, _ = mimetypes.guess_type(str(archivo))
    if not mime:
        mime = "image/png"
    contenido = archivo.read_bytes()
    return f"data:{mime};base64,{base64.b64encode(contenido).decode('ascii')}"


def _qr_png_data_uri(texto: str, box_size: int = 6, border: int = 1) -> str:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(texto)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('ascii')}"


def _numero_carnet(usuario: Usuario) -> str:
    """Replica la logica de obtenerNumeroCarnet del frontend."""
    padron_raw = usuario.num_padron or str(usuario.id).zfill(3)
    solo_numeros = re.sub(r"\D", "", padron_raw) or "0"
    num = int(solo_numeros)
    if num < 1000:
        padron_fmt = str(num).zfill(4)
    else:
        padron_fmt = str(num)
    dni = usuario.numero_dni or ""
    return f"{padron_fmt}{dni}"


def _formatear_fecha(d: datetime) -> str:
    return d.strftime("%d/%m/%Y")


def _construir_contexto(usuarios: List[Usuario], config_carnet) -> dict:
    hoy = datetime.utcnow()
    try:
        caducidad = datetime(hoy.year + 4, hoy.month, hoy.day)
    except ValueError:
        caducidad = datetime(hoy.year + 4, 3, 1)

    config_ctx = {
        "nombre_comunidad": getattr(config_carnet, "nombre_comunidad", "") or "",
        "subtitulo": getattr(config_carnet, "subtitulo", "") or "",
        "resolucion": getattr(config_carnet, "resolucion", "") or "",
        "nombre_corto": getattr(config_carnet, "nombre_corto", "") or "CC.TPCT",
        "url_qr": getattr(config_carnet, "url_qr", None),
        "bandera_data": _file_to_data_uri(getattr(config_carnet, "bandera_url", None)),
        "escudo_data": _file_to_data_uri(getattr(config_carnet, "escudo_url", None)),
        "fondo_anverso_data": _file_to_data_uri(getattr(config_carnet, "fondo_anverso_url", None)),
        "fondo_reverso_data": _file_to_data_uri(getattr(config_carnet, "fondo_reverso_url", None)),
        "firma_secretario_data": _file_to_data_uri(getattr(config_carnet, "firma_secretario_url", None)),
        "firma_presidente_data": _file_to_data_uri(getattr(config_carnet, "firma_presidente_url", None)),
    }

    qr_url_data = _qr_png_data_uri(config_ctx["url_qr"]) if config_ctx["url_qr"] else None

    carnets = []
    for u in usuarios:
        numero = _numero_carnet(u)
        apellidos = " ".join(filter(None, [u.apellido_paterno, u.apellido_materno])).strip().upper()
        nombres = (u.nombres or "").strip().upper()
        carnets.append({
            "numero_carnet": numero,
            "numero_dni": u.numero_dni or "",
            "apellidos": apellidos,
            "nombres": nombres,
            "estado_civil": u.estado_civil or "-",
            "fecha_nacimiento": u.fecha_nacimiento or "-",
            "anexo": u.anexo or "-",
            "fecha_emision": _formatear_fecha(hoy),
            "fecha_caducidad": _formatear_fecha(caducidad),
            "foto_data": _file_to_data_uri(u.foto_frontal),
            "qr_data": _qr_png_data_uri(numero),
            "qr_url_data": qr_url_data,
        })

    return {"carnets": carnets, "config": config_ctx}


def _renderizar_html(usuarios: List[Usuario], config_carnet) -> str:
    template = _jinja_env.get_template("carnet.html")
    contexto = _construir_contexto(usuarios, config_carnet)
    return template.render(**contexto)


def _html_a_pdf(html: str) -> bytes:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page()
            page.set_content(html, wait_until="networkidle")
            return page.pdf(
                width="1012px",
                height="288px",
                print_background=True,
                margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                prefer_css_page_size=True,
            )
        finally:
            browser.close()


def generar_pdf_carnets(usuarios: List[Usuario], config_carnet) -> bytes:
    """Genera un PDF con un carnet por pagina para cada usuario.
    Usa sync_playwright; el endpoint debe llamarlo en un thread separado
    (anyio.to_thread o starlette run_in_threadpool) para no bloquear el event loop.
    """
    if not usuarios:
        raise ValueError("No hay usuarios para generar carnets")
    html = _renderizar_html(usuarios, config_carnet)
    return _html_a_pdf(html)
