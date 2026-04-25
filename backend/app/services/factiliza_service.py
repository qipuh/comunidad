import requests
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from sqlalchemy.orm import Session
from app.models.factiliza import FactilizaConfiguracion, FactilizaConsultaDNI, FactilizaLog

logger = logging.getLogger(__name__)


class FactilizaService:
    def __init__(self, db: Session):
        self.db = db

    def get_configuracion(self) -> Optional[FactilizaConfiguracion]:
        """Obtener configuración actual de Factiliza"""
        return self.db.query(FactilizaConfiguracion).first()

    def actualizar_configuracion(
        self,
        endpoint_url: str = None,
        auth_token: str = None,
        timeout_segundos: int = None,
        max_reintentos: int = None
    ) -> FactilizaConfiguracion:
        """Actualizar configuración de Factiliza"""
        config = self.get_configuracion()

        if not config:
            config = FactilizaConfiguracion(
                endpoint_url=endpoint_url or "https://api.factiliza.com",
                auth_token=auth_token or "",
                timeout_segundos=timeout_segundos or 30,
                max_reintentos=max_reintentos or 3
            )
            self.db.add(config)
        else:
            if endpoint_url:
                config.endpoint_url = endpoint_url
            if auth_token:
                config.auth_token = auth_token
            if timeout_segundos:
                config.timeout_segundos = timeout_segundos
            if max_reintentos:
                config.max_reintentos = max_reintentos

        self.db.commit()
        self.db.refresh(config)
        return config

    def test_conexion(self) -> Dict:
        """Probar conexión con Factiliza"""
        config = self.get_configuracion()

        if not config or not config.auth_token:
            return {
                "success": False,
                "message": "Factiliza no está configurado",
                "timestamp": datetime.now().isoformat()
            }

        try:
            headers = {
                "Authorization": f"Bearer {config.auth_token}",
                "Content-Type": "application/json"
            }

            response = requests.get(
                f"{config.endpoint_url}/health",
                headers=headers,
                timeout=config.timeout_segundos
            )

            self._registrar_log("health_check", None, "success", "", response.elapsed.total_seconds() * 1000)

            return {
                "success": response.status_code == 200,
                "message": "Conexión exitosa" if response.status_code == 200 else "Error de conexión",
                "status_code": response.status_code,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self._registrar_log("health_check", None, "error", str(e), 0)
            return {
                "success": False,
                "message": f"Error en conexión: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def consultar_dni(self, numero_dni: str) -> Dict:
        """Consultar DNI y obtener datos de la persona"""
        config = self.get_configuracion()

        if not config or not config.auth_token:
            return {"success": False, "message": "Factiliza no está configurado"}

        try:
            headers = {
                "Authorization": f"Bearer {config.auth_token}",
                "Content-Type": "application/json"
            }

            # La URL ya contiene el path completo con {dni} o es la base
            # Soportamos: "https://api.factiliza.com/v1/dni/info/{dni}" o "https://api.factiliza.com/v1"
            endpoint_url = config.endpoint_url
            if "{dni}" in endpoint_url:
                url = endpoint_url.replace("{dni}", numero_dni)
            else:
                # Remover trailing slash y agregar path estándar
                url = f"{endpoint_url.rstrip('/')}/dni/info/{numero_dni}"

            inicio = datetime.now()
            response = requests.get(
                url,
                headers=headers,
                timeout=config.timeout_segundos
            )
            tiempo_ms = (datetime.now() - inicio).total_seconds() * 1000

            if response.status_code == 200:
                respuesta = response.json()

                # La API de Factiliza devuelve los datos dentro de "data"
                datos = respuesta.get("data", respuesta)

                nombre_completo = datos.get("nombre_completo") or (
                    f"{datos.get('nombres', '')} {datos.get('apellido_paterno', '')} {datos.get('apellido_materno', '')}".strip()
                )

                # Guardar consulta en base de datos
                consulta = FactilizaConsultaDNI(
                    numero_dni=numero_dni,
                    nombre_completo=nombre_completo,
                    fecha_nacimiento=str(datos.get("fecha_nacimiento")) if datos.get("fecha_nacimiento") else None,
                    sexo=datos.get("sexo"),
                    direccion=datos.get("direccion_completa") or datos.get("direccion"),
                    departamento=datos.get("departamento"),
                    provincia=datos.get("provincia"),
                    distrito=datos.get("distrito"),
                    estado_civil=datos.get("estado_civil"),
                    edad=datos.get("edad"),
                    respuesta_api=respuesta,
                    estado="Exitosa"
                )
                self.db.add(consulta)
                self.db.commit()
                self.db.refresh(consulta)

                self._registrar_log("consultar_dni", numero_dni, "success", "", tiempo_ms)

                return {
                    "success": True,
                    "id": consulta.id,
                    "message": "Consulta exitosa",
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
                        "edad": consulta.edad
                    }
                }
            else:
                error_msg = response.text
                self._registrar_log("consultar_dni", numero_dni, "error", error_msg, tiempo_ms)
                return {
                    "success": False,
                    "message": f"Error: {error_msg}",
                    "status_code": response.status_code
                }

        except Exception as e:
            self._registrar_log("consultar_dni", numero_dni, "error", str(e), 0)
            return {
                "success": False,
                "message": f"Error al consultar DNI: {str(e)}"
            }

    def obtener_consulta(self, id_consulta: int) -> Optional[FactilizaConsultaDNI]:
        """Obtener detalles de una consulta anterior"""
        return self.db.query(FactilizaConsultaDNI).filter(
            FactilizaConsultaDNI.id == id_consulta
        ).first()

    def listar_historial(self, limit: int = 50, offset: int = 0) -> List[FactilizaConsultaDNI]:
        """Listar historial de consultas"""
        return self.db.query(FactilizaConsultaDNI).order_by(
            FactilizaConsultaDNI.created_at.desc()
        ).limit(limit).offset(offset).all()

    def obtener_estadisticas(self) -> Dict:
        """Obtener estadísticas de consultas"""
        total_consultas = self.db.query(FactilizaConsultaDNI).count()
        consultas_exitosas = self.db.query(FactilizaConsultaDNI).filter(
            FactilizaConsultaDNI.estado == "Exitosa"
        ).count()

        return {
            "total_consultas": total_consultas,
            "consultas_exitosas": consultas_exitosas,
            "tasa_exito": (consultas_exitosas / total_consultas * 100) if total_consultas > 0 else 0,
            "timestamp": datetime.now().isoformat()
        }

    def _registrar_log(
        self,
        tipo_operacion: str,
        numero_dni: str = None,
        estado: str = "success",
        error: str = "",
        tiempo_ms: float = 0
    ):
        """Registrar operación en log"""
        try:
            log = FactilizaLog(
                tipo_operacion=tipo_operacion,
                numero_dni=numero_dni,
                estado=estado,
                mensaje=f"Operación {tipo_operacion} completada",
                tiempo_respuesta_ms=int(tiempo_ms),
                error=error if error else None
            )
            self.db.add(log)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error registrando log: {str(e)}")
