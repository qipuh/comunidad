"""
Gestor de tareas asincrónicas para exportación de carnets.
Limita a máximo 2 Playwright simultáneos para no saturar servidor.
Rastrea progreso en tiempo real.
"""

import uuid
import threading
import logging
from datetime import datetime, timedelta
from typing import Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class EstadoTarea(str, Enum):
    PENDIENTE = "pendiente"
    PROCESANDO = "procesando"
    COMPLETADA = "completada"
    ERROR = "error"
    CANCELADA = "cancelada"


@dataclass
class EstadoProgreso:
    """Estado actual de una exportación."""
    task_id: str
    estado: EstadoTarea
    carnets_procesados: int = 0
    total_carnets: int = 0
    porcentaje: int = 0
    mensaje: str = ""
    pdf_bytes: Optional[bytes] = None
    error: Optional[str] = None
    creada_en: datetime = None
    completada_en: Optional[datetime] = None
    cancelar: bool = False

    def __post_init__(self):
        if self.creada_en is None:
            self.creada_en = datetime.utcnow()

    def to_dict(self):
        """Retorna dict serializable (sin pdf_bytes)."""
        d = asdict(self)
        d['estado'] = self.estado.value
        d['creada_en'] = self.creada_en.isoformat() if self.creada_en else None
        d['completada_en'] = self.completada_en.isoformat() if self.completada_en else None
        d.pop('pdf_bytes', None)  # No serializar PDF
        return d


class GestorTareas:
    """
    Gestor thread-safe de tareas.
    - Máximo 2 workers simultáneos (para 4-core server)
    - Rastrea progreso
    - Auto-limpia tareas antiguas (>24h)
    """

    def __init__(self, max_workers: int = 2):
        self.max_workers = max_workers
        self.tareas: dict[str, EstadoProgreso] = {}
        self.lock = threading.Lock()
        self.active_workers = 0
        self.queue: list[tuple[str, Callable]] = []

    def crear_tarea(self, total_carnets: int) -> str:
        """Crea una nueva tarea y retorna su ID."""
        task_id = str(uuid.uuid4())
        with self.lock:
            self.tareas[task_id] = EstadoProgreso(
                task_id=task_id,
                estado=EstadoTarea.PENDIENTE,
                total_carnets=total_carnets,
                mensaje="En cola de espera..."
            )
        return task_id

    def obtener_estado(self, task_id: str) -> Optional[EstadoProgreso]:
        """Obtiene el estado actual de una tarea."""
        with self.lock:
            return self.tareas.get(task_id)

    def actualizar_progreso(self, task_id: str, carnets_procesados: int, mensaje: str = ""):
        """Actualiza el progreso de una tarea en ejecución."""
        with self.lock:
            if task_id in self.tareas:
                tarea = self.tareas[task_id]
                tarea.carnets_procesados = carnets_procesados
                if tarea.total_carnets > 0:
                    tarea.porcentaje = int((carnets_procesados / tarea.total_carnets) * 100)
                if mensaje:
                    tarea.mensaje = mensaje

    def marcar_completada(self, task_id: str, pdf_bytes: bytes):
        """Marca una tarea como completada."""
        with self.lock:
            if task_id in self.tareas:
                tarea = self.tareas[task_id]
                tarea.estado = EstadoTarea.COMPLETADA
                tarea.pdf_bytes = pdf_bytes
                tarea.carnets_procesados = tarea.total_carnets
                tarea.porcentaje = 100
                tarea.mensaje = "¡PDF listo para descargar!"
                tarea.completada_en = datetime.utcnow()

    def marcar_error(self, task_id: str, error: str):
        """Marca una tarea con error."""
        with self.lock:
            if task_id in self.tareas:
                tarea = self.tareas[task_id]
                tarea.estado = EstadoTarea.ERROR
                tarea.error = error
                tarea.mensaje = f"Error: {error}"
                tarea.completada_en = datetime.utcnow()

    def cancelar_tarea(self, task_id: str) -> bool:
        """Solicita cancelación de una tarea en curso. Retorna True si se pudo marcar."""
        with self.lock:
            tarea = self.tareas.get(task_id)
            if tarea and tarea.estado in (EstadoTarea.PENDIENTE, EstadoTarea.PROCESANDO):
                tarea.cancelar = True
                tarea.estado = EstadoTarea.CANCELADA
                tarea.mensaje = "Cancelado por el usuario"
                tarea.completada_en = datetime.utcnow()
                return True
            return False

    def debe_cancelar(self, task_id: str) -> bool:
        """El thread worker llama esto entre carnets para saber si debe abortar."""
        with self.lock:
            tarea = self.tareas.get(task_id)
            return tarea.cancelar if tarea else False

    def ejecutar_tarea(self, task_id: str, funcion: Callable):
        """Ejecuta una función en un thread worker con control de concurrencia."""
        def worker():
            try:
                with self.lock:
                    self.active_workers += 1
                    if task_id in self.tareas:
                        self.tareas[task_id].estado = EstadoTarea.PROCESANDO
                        self.tareas[task_id].mensaje = "Iniciando..."

                logger.info(f"🚀 Iniciando tarea {task_id}")

                # Callback wrapper que añade task_id automáticamente.
                # La firma para el servicio es: callback(procesados, mensaje)
                def callback_progreso(procesados, mensaje=""):
                    self.actualizar_progreso(task_id, procesados, mensaje)

                resultado = funcion(task_id, callback_progreso)
                logger.info(f"✅ Tarea {task_id} generó {len(resultado) if resultado else 0} bytes")

                # Marcar completada
                self.marcar_completada(task_id, resultado)

            except Exception as e:
                import traceback
                error_msg = str(e) or type(e).__name__
                logger.error(f"❌ Error en tarea {task_id}: {error_msg}")
                logger.error(traceback.format_exc())
                self.marcar_error(task_id, error_msg)
            finally:
                with self.lock:
                    self.active_workers -= 1
                self._procesar_siguiente_en_cola()

        # Esperar si hay demasiados workers
        while True:
            with self.lock:
                if self.active_workers < self.max_workers:
                    thread = threading.Thread(target=worker, daemon=True)
                    thread.start()
                    return
            # Esperar un poco antes de reintentar
            threading.Event().wait(0.1)

    def obtener_pdf(self, task_id: str) -> Optional[bytes]:
        """Obtiene el PDF de una tarea completada."""
        with self.lock:
            tarea = self.tareas.get(task_id)
            return tarea.pdf_bytes if tarea and tarea.estado == EstadoTarea.COMPLETADA else None

    def limpiar_tareas_antiguas(self, horas: int = 24):
        """Limpia tareas completadas/error más antiguas que N horas."""
        now = datetime.utcnow()
        with self.lock:
            a_eliminar = [
                task_id for task_id, tarea in self.tareas.items()
                if tarea.completada_en and (now - tarea.completada_en) > timedelta(hours=horas)
            ]
            for task_id in a_eliminar:
                del self.tareas[task_id]

    def _procesar_siguiente_en_cola(self):
        """Procesa la siguiente tarea en cola si hay workers disponibles."""
        with self.lock:
            if self.queue and self.active_workers < self.max_workers:
                task_id, funcion = self.queue.pop(0)
                # Reintentar ejecutar (sin recursión directa)
                threading.Thread(
                    target=self.ejecutar_tarea,
                    args=(task_id, funcion),
                    daemon=True
                ).start()


# Instancia global
_gestor_tareas = GestorTareas(max_workers=2)


def get_gestor_tareas() -> GestorTareas:
    """Obtiene la instancia global del gestor de tareas."""
    return _gestor_tareas
