"""
Servicio para consultar APIs externas (RENIEC, Facturiza, SUNAT, etc.)
y mapear respuestas a campos del sistema.

Funcionalidades:
- Consultar diferentes tipos de APIs
- Manejar reintentos automáticos
- Encriptar/desencriptar tokens
- Registrar auditoría de consultas
- Mapear respuestas a campos locales
"""

import requests
import json
import logging
from typing import Dict, Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
from cryptography.fernet import Fernet
import os

logger = logging.getLogger(__name__)


class IntegracionAPIService:
    """Servicio para consultar APIs externas"""

    def __init__(self, db: Session, encryption_key: Optional[str] = None):
        self.db = db
        self.encryption_key = encryption_key or os.getenv("ENCRYPTION_KEY")

    def desencriptar_token(self, token_encriptado: str) -> str:
        """Desencriptar token almacenado"""
        if not self.encryption_key:
            return token_encriptado
        try:
            cipher = Fernet(self.encryption_key.encode())
            return cipher.decrypt(token_encriptado.encode()).decode()
        except Exception as e:
            logger.error(f"Error desencriptando token: {str(e)}")
            return token_encriptado

    def encriptar_token(self, token: str) -> str:
        """Encriptar token antes de guardar"""
        if not self.encryption_key:
            return token
        try:
            cipher = Fernet(self.encryption_key.encode())
            return cipher.encrypt(token.encode()).decode()
        except Exception as e:
            logger.error(f"Error encriptando token: {str(e)}")
            return token

    def consultar_reniec(self, dni: str, integracion) -> Dict:
        """
        Consulta RENIEC por DNI.

        Args:
            dni: Número de documento (8 dígitos)
            integracion: Objeto IntegracionAPI con configuración

        Returns:
            {
                "exitosa": bool,
                "datos": {...} o None,
                "error": str o None
            }
        """
        try:
            if not integracion.activa:
                return {
                    "exitosa": False,
                    "error": "Integración RENIEC desactivada",
                    "datos": None
                }

            # Desencriptar token
            token = self.desencriptar_token(integracion.auth_token)

            # Validar formato DNI
            if not dni.isdigit() or len(dni) != 8:
                return {
                    "exitosa": False,
                    "error": "DNI debe ser 8 dígitos",
                    "datos": None
                }

            # Construir URL
            url = f"{integracion.endpoint_url}{dni}"
            headers = {"Authorization": f"Bearer {token}"}

            logger.info(f"Consultando RENIEC para DNI: {dni}")

            # Realizar consulta con reintentos
            response = None
            for intento in range(integracion.max_reintentos):
                try:
                    response = requests.get(
                        url,
                        headers=headers,
                        timeout=integracion.timeout_segundos
                    )
                    response.raise_for_status()
                    break
                except requests.exceptions.Timeout:
                    if intento == integracion.max_reintentos - 1:
                        raise
                    logger.warning(f"Timeout en intento {intento + 1}/{integracion.max_reintentos}")
                    continue
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code >= 500 and intento < integracion.max_reintentos - 1:
                        logger.warning(f"Error 5xx en intento {intento + 1}, reintentando...")
                        continue
                    raise

            datos = response.json()

            # Mapear respuesta RENIEC
            datos_mapeados = {
                "nombre": datos.get("nombres"),
                "apellido_paterno": datos.get("apellido_paterno"),
                "apellido_materno": datos.get("apellido_materno"),
                "genero": datos.get("genero"),
                "fecha_nacimiento": datos.get("fecha_nacimiento"),
                "estado_civil": datos.get("estado_civil"),
                "fotografia_url": datos.get("fotografia_url")
            }

            # Remover valores None
            datos_mapeados = {k: v for k, v in datos_mapeados.items() if v is not None}

            logger.info(f"✓ Consulta RENIEC exitosa para DNI: {dni}")

            return {
                "exitosa": True,
                "datos": datos_mapeados,
                "respuesta_original": datos
            }

        except requests.exceptions.Timeout:
            error_msg = f"Timeout ({integracion.timeout_segundos}s) consultando RENIEC"
            logger.error(error_msg)
            return {"exitosa": False, "error": error_msg, "datos": None}

        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP {e.response.status_code}: {e.response.text}"
            logger.error(f"Error HTTP consultando RENIEC: {error_msg}")
            return {"exitosa": False, "error": error_msg, "datos": None}

        except requests.exceptions.RequestException as e:
            error_msg = f"Error de conexión: {str(e)}"
            logger.error(error_msg)
            return {"exitosa": False, "error": error_msg, "datos": None}

        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            logger.error(error_msg)
            return {"exitosa": False, "error": error_msg, "datos": None}

    def consultar_facturiza(self, ruc: str, integracion) -> Dict:
        """
        Consulta Facturiza por RUC.

        Args:
            ruc: Número de RUC (11 dígitos)
            integracion: Objeto IntegracionAPI

        Returns:
            {
                "exitosa": bool,
                "datos": {...} o None,
                "error": str o None
            }
        """
        try:
            if not integracion.activa:
                return {
                    "exitosa": False,
                    "error": "Integración Facturiza desactivada",
                    "datos": None
                }

            # Validar RUC
            if not ruc.isdigit() or len(ruc) != 11:
                return {
                    "exitosa": False,
                    "error": "RUC debe ser 11 dígitos",
                    "datos": None
                }

            # Desencriptar token
            api_key = self.desencriptar_token(integracion.auth_token)

            # Construir request
            url = integracion.endpoint_url
            headers = {"X-API-Key": api_key}
            payload = {"ruc": ruc}

            logger.info(f"Consultando Facturiza para RUC: {ruc}")

            # Realizar consulta con reintentos
            response = None
            for intento in range(integracion.max_reintentos):
                try:
                    response = requests.post(
                        url,
                        json=payload,
                        headers=headers,
                        timeout=integracion.timeout_segundos
                    )
                    response.raise_for_status()
                    break
                except requests.exceptions.Timeout:
                    if intento == integracion.max_reintentos - 1:
                        raise
                    logger.warning(f"Timeout en intento {intento + 1}/{integracion.max_reintentos}")
                    continue
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code >= 500 and intento < integracion.max_reintentos - 1:
                        logger.warning(f"Error 5xx en intento {intento + 1}, reintentando...")
                        continue
                    raise

            datos = response.json()

            # Mapear respuesta Facturiza
            datos_mapeados = {
                "razon_social": datos.get("razon_social"),
                "direccion": datos.get("direccion"),
                "representante_legal": datos.get("representante_legal"),
                "actividad_economica": datos.get("actividad_economica"),
                "estado_contribuyente": datos.get("estado_contribuyente"),
                "fecha_inscripcion": datos.get("fecha_inscripcion")
            }

            datos_mapeados = {k: v for k, v in datos_mapeados.items() if v is not None}

            logger.info(f"✓ Consulta Facturiza exitosa para RUC: {ruc}")

            return {
                "exitosa": True,
                "datos": datos_mapeados,
                "respuesta_original": datos
            }

        except requests.exceptions.Timeout:
            error_msg = f"Timeout ({integracion.timeout_segundos}s) consultando Facturiza"
            logger.error(error_msg)
            return {"exitosa": False, "error": error_msg, "datos": None}

        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP {e.response.status_code}"
            logger.error(f"Error HTTP en Facturiza: {error_msg}")
            return {"exitosa": False, "error": error_msg, "datos": None}

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.error(f"Error en Facturiza: {error_msg}")
            return {"exitosa": False, "error": error_msg, "datos": None}

    def consultar_api_custom(self, parametro: str, integracion) -> Dict:
        """
        Consulta API personalizada.

        Soporta diferentes métodos y auth types.
        """
        try:
            if not integracion.activa:
                return {
                    "exitosa": False,
                    "error": "Integración desactivada",
                    "datos": None
                }

            url = integracion.endpoint_url
            token = self.desencriptar_token(integracion.auth_token)

            # Construir headers según auth type
            headers = {}
            if integracion.auth_type.value == "bearer":
                headers["Authorization"] = f"Bearer {token}"
            elif integracion.auth_type.value == "api_key":
                headers["X-API-Key"] = token
            elif integracion.auth_type.value == "basic":
                import base64
                encoded = base64.b64encode(token.encode()).decode()
                headers["Authorization"] = f"Basic {encoded}"

            logger.info(f"Consultando API custom: {url}")

            # Realizar consulta
            response = requests.get(
                url,
                params={"q": parametro},
                headers=headers,
                timeout=integracion.timeout_segundos
            )
            response.raise_for_status()

            datos = response.json()

            return {
                "exitosa": True,
                "datos": datos,
                "respuesta_original": datos
            }

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.error(error_msg)
            return {"exitosa": False, "error": error_msg, "datos": None}

    def registrar_consulta(
        self,
        usuario_id: Optional[int],
        integracion_id: int,
        tipo_consulta: str,
        parametro: str,
        respuesta: Dict,
        estado: str,
        ip_origen: Optional[str] = None
    ):
        """
        Registra consulta realizada a API externa para auditoría.

        Args:
            usuario_id: ID del usuario (puede ser None si aún no se registra)
            integracion_id: ID de la integración usada
            tipo_consulta: Tipo ("documento", "empresa", etc.)
            parametro: Valor buscado (DNI, RUC, etc.)
            respuesta: Respuesta de la API o error
            estado: "exitosa" o "fallida"
            ip_origen: IP del cliente
        """
        from app.models.configuracion import ConsultaExterna

        try:
            consulta = ConsultaExterna(
                usuario_id=usuario_id,
                integracion_api_id=integracion_id,
                tipo_consulta=tipo_consulta,
                parametro_busqueda=parametro,
                respuesta_json=respuesta.get("respuesta_original") if estado == "exitosa" else None,
                campos_mapeados=respuesta.get("datos") if estado == "exitosa" else None,
                estado=estado,
                mensaje_error=respuesta.get("error") if estado == "fallida" else None,
                ip_origen=ip_origen
            )
            self.db.add(consulta)
            self.db.commit()
            logger.info(f"Consulta registrada: {tipo_consulta} - {estado}")
            return consulta
        except Exception as e:
            logger.error(f"Error registrando consulta: {str(e)}")
            self.db.rollback()
            return None
