"""
Seeder para agregar conceptos de pago de ejemplo
"""
from app.db.database import SessionLocal
from app.models.cobranza import ConceptoPago, TipoConcepto, Recurrencia
from datetime import datetime

db = SessionLocal()

try:
    # Verificar si ya existen conceptos
    conceptos_existentes = db.query(ConceptoPago).count()
    if conceptos_existentes > 0:
        print(f"Ya existen {conceptos_existentes} conceptos de pago")
        db.close()
        exit()

    # Crear conceptos de pago
    conceptos = [
        ConceptoPago(
            nombre="Cuota Mensual",
            descripcion="Cuota mensual de afiliación",
            monto=50.0,
            tipo=TipoConcepto.CUOTA,
            recurrencia=Recurrencia.MENSUAL,
            dia_cobro=5,
            cada_n_periodos=1,
            fecha_inicio=datetime(2026, 1, 1),
            activo=True
        ),
        ConceptoPago(
            nombre="Derecho de Admisión",
            descripcion="Pago único por afiliación",
            monto=100.0,
            tipo=TipoConcepto.DERECHO,
            recurrencia=Recurrencia.MENSUAL,
            fecha_inicio=datetime(2026, 1, 1),
            activo=True
        ),
        ConceptoPago(
            nombre="Multa por Inasistencia",
            descripcion="Multa por no asistir a asambleas",
            monto=25.0,
            tipo=TipoConcepto.MULTA,
            recurrencia=Recurrencia.MENSUAL,
            fecha_inicio=datetime(2026, 1, 1),
            activo=True
        ),
        ConceptoPago(
            nombre="Cuota Bimestral Especial",
            descripcion="Cuota especial cada dos meses",
            monto=75.0,
            tipo=TipoConcepto.CUOTA,
            recurrencia=Recurrencia.BIMESTRAL,
            dia_cobro=15,
            cada_n_periodos=1,
            fecha_inicio=datetime(2026, 1, 1),
            activo=True
        ),
    ]

    db.add_all(conceptos)
    db.commit()

    print(f"Se crearon {len(conceptos)} conceptos de pago:")
    for concepto in conceptos:
        print(f"  - {concepto.nombre} ({concepto.tipo.value}): S/ {concepto.monto}")

except Exception as e:
    print(f"Error: {e}")
    db.rollback()
finally:
    db.close()
