"""
Rutas para estadísticas del Dashboard.
Agrega datos de usuarios, cobranza, elecciones y pagos en un solo endpoint.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.db.database import get_db
from app.models.usuario import Usuario
from app.models.cobranza import Cuota, Pago, EstadoCuota, EstadoPago
from app.models.eleccion import Eleccion
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/estadisticas")
async def obtener_estadisticas_dashboard(db: Session = Depends(get_db)):
    """
    Endpoint consolidado de estadísticas para el Dashboard Home.
    Retorna KPIs, datos de gráficos y actividad reciente.
    """
    ahora = datetime.utcnow()
    inicio_mes = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    inicio_semana = ahora - timedelta(days=ahora.weekday())
    inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)

    # ═══════════════════════════════════════════════════════════════
    # USUARIOS
    # ═══════════════════════════════════════════════════════════════
    total_usuarios = db.query(Usuario).count()
    usuarios_activos = db.query(Usuario).filter(Usuario.estado == "activo").count()
    usuarios_este_mes = db.query(Usuario).filter(
        Usuario.created_at >= inicio_mes
    ).count()

    # Porcentaje de crecimiento (comparado con mes anterior)
    inicio_mes_anterior = (inicio_mes - timedelta(days=1)).replace(day=1)
    usuarios_mes_anterior = db.query(Usuario).filter(
        Usuario.created_at >= inicio_mes_anterior,
        Usuario.created_at < inicio_mes
    ).count()
    pct_crecimiento_usuarios = 0
    if usuarios_mes_anterior > 0:
        pct_crecimiento_usuarios = round(
            ((usuarios_este_mes - usuarios_mes_anterior) / usuarios_mes_anterior) * 100, 1
        )

    # ═══════════════════════════════════════════════════════════════
    # COBRANZA
    # ═══════════════════════════════════════════════════════════════
    # Total recaudado (pagos aprobados)
    total_recaudado = db.query(func.coalesce(func.sum(Pago.monto), 0)).filter(
        Pago.estado == EstadoPago.APROBADO
    ).scalar()

    # Recaudado esta semana
    recaudado_semana = db.query(func.coalesce(func.sum(Pago.monto), 0)).filter(
        Pago.estado == EstadoPago.APROBADO,
        Pago.fecha_aprobacion >= inicio_semana
    ).scalar()

    # Estado de cuotas
    total_cuotas = db.query(Cuota).count()
    cuotas_pagadas = db.query(Cuota).filter(Cuota.estado == EstadoCuota.PAGADA).count()
    cuotas_pendientes = db.query(Cuota).filter(Cuota.estado == EstadoCuota.PENDIENTE).count()
    cuotas_vencidas = db.query(Cuota).filter(Cuota.estado == EstadoCuota.VENCIDA).count()

    pct_pagado = round((cuotas_pagadas / total_cuotas * 100), 1) if total_cuotas > 0 else 0
    pct_pendiente = round((cuotas_pendientes / total_cuotas * 100), 1) if total_cuotas > 0 else 0
    pct_vencido = round((cuotas_vencidas / total_cuotas * 100), 1) if total_cuotas > 0 else 0

    # Pagos pendientes de aprobación
    pagos_pendientes = db.query(Pago).filter(
        Pago.estado == EstadoPago.PENDIENTE_APROBACION
    ).count()

    # ═══════════════════════════════════════════════════════════════
    # CARNETS (usuarios con foto)
    # ═══════════════════════════════════════════════════════════════
    carnets_emitidos = db.query(Usuario).filter(
        Usuario.foto_frontal.isnot(None)
    ).count()

    # ═══════════════════════════════════════════════════════════════
    # ELECCIONES / VOTACIONES
    # ═══════════════════════════════════════════════════════════════
    votaciones_activas = db.query(Eleccion).filter(Eleccion.estado == "activo").count()
    votaciones_cerradas = db.query(Eleccion).filter(Eleccion.estado == "cerrado").count()

    # ═══════════════════════════════════════════════════════════════
    # GRÁFICO: Cobranza mensual (últimos 6 meses)
    # ═══════════════════════════════════════════════════════════════
    cobranza_mensual = []
    meses_labels = []
    meses_nombres = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    for i in range(5, -1, -1):
        fecha_ref = ahora - timedelta(days=30 * i)
        mes = fecha_ref.month
        anio = fecha_ref.year
        meses_labels.append(meses_nombres[mes - 1])

        total_mes = db.query(func.coalesce(func.sum(Pago.monto), 0)).filter(
            Pago.estado == EstadoPago.APROBADO,
            extract('month', Pago.fecha_aprobacion) == mes,
            extract('year', Pago.fecha_aprobacion) == anio
        ).scalar()
        cobranza_mensual.append(float(total_mes))

    promedio_cobranza = round(sum(cobranza_mensual) / len(cobranza_mensual), 2) if cobranza_mensual else 0

    # ═══════════════════════════════════════════════════════════════
    # GRÁFICO: Usuarios nuevos por mes (últimos 6 meses)
    # ═══════════════════════════════════════════════════════════════
    usuarios_mensual = []
    usuarios_labels = []

    for i in range(5, -1, -1):
        fecha_ref = ahora - timedelta(days=30 * i)
        mes = fecha_ref.month
        anio = fecha_ref.year
        usuarios_labels.append(meses_nombres[mes - 1][:3])

        total_mes = db.query(func.count(Usuario.id)).filter(
            extract('month', Usuario.created_at) == mes,
            extract('year', Usuario.created_at) == anio
        ).scalar()
        usuarios_mensual.append(int(total_mes))

    # ═══════════════════════════════════════════════════════════════
    # ACTIVIDAD RECIENTE
    # ═══════════════════════════════════════════════════════════════
    actividad = []

    # Últimos usuarios creados
    ultimos_usuarios = db.query(Usuario).order_by(
        Usuario.created_at.desc()
    ).limit(3).all()
    for u in ultimos_usuarios:
        actividad.append({
            "titulo": f"Nuevo usuario: {u.nombre_completo}",
            "tiempo": _tiempo_relativo(u.created_at, ahora),
            "color": "#6366f1",
            "fecha": u.created_at.isoformat() if u.created_at else None
        })

    # Últimos pagos aprobados
    ultimos_pagos = db.query(Pago).filter(
        Pago.estado == EstadoPago.APROBADO
    ).order_by(Pago.fecha_aprobacion.desc()).limit(3).all()
    for p in ultimos_pagos:
        actividad.append({
            "titulo": f"Pago aprobado de S/. {p.monto:.2f}",
            "tiempo": _tiempo_relativo(p.fecha_aprobacion or p.created_at, ahora),
            "color": "#10b981",
            "fecha": (p.fecha_aprobacion or p.created_at).isoformat()
        })

    # Últimas elecciones creadas
    ultimas_elecciones = db.query(Eleccion).order_by(
        Eleccion.created_at.desc()
    ).limit(2).all()
    for e in ultimas_elecciones:
        estado_txt = "creada" if e.estado == "borrador" else ("iniciada" if e.estado == "activo" else "cerrada")
        actividad.append({
            "titulo": f"Elección {estado_txt}: {e.titulo}",
            "tiempo": _tiempo_relativo(e.created_at, ahora),
            "color": "#f59e0b",
            "fecha": e.created_at.isoformat()
        })

    # Ordenar por fecha más reciente
    actividad.sort(key=lambda x: x.get("fecha") or "", reverse=True)
    actividad = actividad[:6]  # máx 6 items

    # Limpiar campo fecha interno
    for item in actividad:
        item.pop("fecha", None)

    return {
        "success": True,
        "data": {
            # KPIs
            "usuarios_totales": total_usuarios,
            "usuarios_activos": usuarios_activos,
            "usuarios_nuevos_mes": usuarios_este_mes,
            "pct_crecimiento_usuarios": pct_crecimiento_usuarios,

            "cobranza_total": float(total_recaudado),
            "recaudado_semana": float(recaudado_semana),

            "carnets_emitidos": carnets_emitidos,

            "votaciones_activas": votaciones_activas,
            "votaciones_cerradas": votaciones_cerradas,

            "pagos_pendientes": pagos_pendientes,

            # Estado de cobranza (porcentajes)
            "cobranza_pct_pagado": pct_pagado,
            "cobranza_pct_pendiente": pct_pendiente,
            "cobranza_pct_vencido": pct_vencido,

            # Gráficos
            "grafico_cobranza": {
                "labels": meses_labels,
                "data": cobranza_mensual
            },
            "grafico_usuarios": {
                "labels": usuarios_labels,
                "data": usuarios_mensual
            },
            "promedio_cobranza": promedio_cobranza,

            # Actividad reciente
            "actividad_reciente": actividad
        }
    }


def _tiempo_relativo(fecha, ahora):
    """Calcula tiempo relativo: 'Hace X horas', 'Hace X días', etc."""
    if not fecha:
        return "Desconocido"
    diff = ahora - fecha
    segundos = diff.total_seconds()

    if segundos < 60:
        return "Hace un momento"
    elif segundos < 3600:
        mins = int(segundos / 60)
        return f"Hace {mins} {'minuto' if mins == 1 else 'minutos'}"
    elif segundos < 86400:
        horas = int(segundos / 3600)
        return f"Hace {horas} {'hora' if horas == 1 else 'horas'}"
    elif segundos < 604800:
        dias = int(segundos / 86400)
        return f"Hace {dias} {'día' if dias == 1 else 'días'}"
    elif segundos < 2592000:
        semanas = int(segundos / 604800)
        return f"Hace {semanas} {'semana' if semanas == 1 else 'semanas'}"
    else:
        meses = int(segundos / 2592000)
        return f"Hace {meses} {'mes' if meses == 1 else 'meses'}"
