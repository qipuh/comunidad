#!/usr/bin/env python3
"""
Script para testing rápido del sistema dinámico
Ejecutar: python test_api.py
"""

import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000"
ADMIN_TOKEN = "YOUR_ADMIN_TOKEN"  # Cambiar por token válido
USER_TOKEN = "YOUR_USER_TOKEN"    # Cambiar por token válido

class APITester:
    def __init__(self, base_url: str, admin_token: str = None, user_token: str = None):
        self.base_url = base_url
        self.admin_token = admin_token
        self.user_token = user_token
        self.session = requests.Session()

    def print_result(self, title: str, response, expected_status: int = 200):
        """Imprime resultado de request"""
        status = "✅" if response.status_code == expected_status else "❌"
        print(f"\n{status} {title}")
        print(f"   Status: {response.status_code}")
        try:
            print(f"   Response: {json.dumps(response.json(), indent=2)[:200]}...")
        except:
            print(f"   Response: {response.text[:200]}")

    # ════════════════════════════════════════════════════════════════
    # ADMIN ENDPOINTS
    # ════════════════════════════════════════════════════════════════

    def crear_integracion_reniec(self):
        """1️⃣ Crear integración RENIEC"""
        url = f"{self.base_url}/api/admin/integraciones-api"
        headers = {
            "Authorization": f"Bearer {self.admin_token}",
            "Content-Type": "application/json"
        }
        data = {
            "nombre": "RENIEC",
            "descripcion": "Consulta de DNI en Perú",
            "tipo": "reniec",
            "endpoint_url": "https://api.reniec.gob.pe/dni/",
            "auth_type": "bearer",
            "auth_token": "test_token_reniec",
            "activa": True,
            "timeout_segundos": 30,
            "max_reintentos": 3
        }
        response = self.session.post(url, json=data, headers=headers)
        self.print_result("Crear integración RENIEC", response, 201)
        return response.json().get("id") if response.status_code == 201 else None

    def crear_integracion_facturiza(self):
        """2️⃣ Crear integración Facturiza"""
        url = f"{self.base_url}/api/admin/integraciones-api"
        headers = {
            "Authorization": f"Bearer {self.admin_token}",
            "Content-Type": "application/json"
        }
        data = {
            "nombre": "Facturiza",
            "descripcion": "Consulta de RUC en Perú",
            "tipo": "facturiza",
            "endpoint_url": "https://api.facturiza.com/",
            "auth_type": "api_key",
            "auth_token": "test_api_key_facturiza",
            "activa": True
        }
        response = self.session.post(url, json=data, headers=headers)
        self.print_result("Crear integración Facturiza", response, 201)
        return response.json().get("id") if response.status_code == 201 else None

    def listar_integraciones(self):
        """3️⃣ Listar integraciones"""
        url = f"{self.base_url}/api/admin/integraciones-api"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = self.session.get(url, headers=headers)
        self.print_result("Listar integraciones", response)
        return response.json() if response.status_code == 200 else []

    def probar_integracion(self, integration_id: int):
        """4️⃣ Probar integración"""
        url = f"{self.base_url}/api/admin/integraciones-api/{integration_id}/probar"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = self.session.post(url, headers=headers)
        self.print_result(f"Probar integración {integration_id}", response)
        return response.json() if response.status_code == 200 else None

    def crear_campo_dni(self, api_integracion_id: int):
        """5️⃣ Crear campo DNI con API"""
        url = f"{self.base_url}/api/admin/configuracion/campos"
        headers = {
            "Authorization": f"Bearer {self.admin_token}",
            "Content-Type": "application/json"
        }
        data = {
            "nombre_campo": "documento_identidad",
            "etiqueta": "Documento de Identidad",
            "descripcion": "DNI, cédula o pasaporte",
            "tipo_dato": "string",
            "es_obligatorio": True,
            "expresion_regex": "^[0-9]{8}$",
            "posicion": 1,
            "api_integracion_id": api_integracion_id,
            "campo_mapa_api": "dni",
            "mostrar_en_registro": True,
            "mostrar_en_perfil": True,
            "mostrar_en_reportes": True
        }
        response = self.session.post(url, json=data, headers=headers)
        self.print_result("Crear campo DNI con API", response, 201)
        return response.json().get("id") if response.status_code == 201 else None

    def crear_campo_nombre(self):
        """6️⃣ Crear campo Nombre sin API"""
        url = f"{self.base_url}/api/admin/configuracion/campos"
        headers = {
            "Authorization": f"Bearer {self.admin_token}",
            "Content-Type": "application/json"
        }
        data = {
            "nombre_campo": "nombre_completo",
            "etiqueta": "Nombre Completo",
            "tipo_dato": "string",
            "es_obligatorio": True,
            "posicion": 2,
            "mostrar_en_registro": True,
            "mostrar_en_perfil": True,
            "mostrar_en_reportes": True
        }
        response = self.session.post(url, json=data, headers=headers)
        self.print_result("Crear campo Nombre", response, 201)
        return response.json().get("id") if response.status_code == 201 else None

    def listar_campos(self):
        """7️⃣ Listar campos"""
        url = f"{self.base_url}/api/admin/configuracion/campos"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = self.session.get(url, headers=headers)
        self.print_result("Listar campos", response)
        return response.json() if response.status_code == 200 else []

    def obtener_estadisticas(self):
        """8️⃣ Obtener estadísticas"""
        url = f"{self.base_url}/api/admin/estadisticas/consultas"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = self.session.get(url, headers=headers)
        self.print_result("Obtener estadísticas", response)
        return response.json() if response.status_code == 200 else None

    # ════════════════════════════════════════════════════════════════
    # USER ENDPOINTS (Sin autenticación)
    # ════════════════════════════════════════════════════════════════

    def consultar_dni(self, dni: str = "12345678"):
        """9️⃣ Consultar DNI (usuario)"""
        url = f"{self.base_url}/api/validaciones/consultar-dni"
        headers = {"Content-Type": "application/json"}
        data = {"dni": dni}
        response = self.session.post(url, json=data, headers=headers)
        self.print_result(f"Consultar DNI {dni}", response)
        return response.json() if response.status_code == 200 else None

    def consultar_ruc(self, ruc: str = "12345678901"):
        """🔟 Consultar RUC (usuario)"""
        url = f"{self.base_url}/api/validaciones/consultar-ruc"
        headers = {"Content-Type": "application/json"}
        data = {"ruc": ruc}
        response = self.session.post(url, json=data, headers=headers)
        self.print_result(f"Consultar RUC {ruc}", response)
        return response.json() if response.status_code == 200 else None

    def probar_reniec(self):
        """1️⃣1️⃣ Probar disponibilidad RENIEC"""
        url = f"{self.base_url}/api/validaciones/probar-reniec"
        response = self.session.get(url)
        self.print_result("Probar RENIEC disponible", response)
        return response.json() if response.status_code == 200 else None

    def probar_facturiza(self):
        """1️⃣2️⃣ Probar disponibilidad Facturiza"""
        url = f"{self.base_url}/api/validaciones/probar-facturiza"
        response = self.session.get(url)
        self.print_result("Probar Facturiza disponible", response)
        return response.json() if response.status_code == 200 else None

    def obtener_historial(self, usuario_id: int = 1):
        """1️⃣3️⃣ Obtener historial usuario"""
        url = f"{self.base_url}/api/validaciones/historial/{usuario_id}"
        headers = {"Authorization": f"Bearer {self.user_token}"}
        response = self.session.get(url, headers=headers)
        self.print_result(f"Obtener historial usuario {usuario_id}", response)
        return response.json() if response.status_code == 200 else None

    def guardar_registro(self, datos: dict):
        """1️⃣4️⃣ Guardar registro dinámico"""
        url = f"{self.base_url}/api/usuarios/registro-dinamico"
        headers = {
            "Authorization": f"Bearer {self.user_token}",
            "Content-Type": "application/json"
        }
        response = self.session.post(url, json=datos, headers=headers)
        self.print_result("Guardar registro dinámico", response, 201)
        return response.json() if response.status_code == 201 else None


def main():
    """Flujo completo de testing"""

    print("\n" + "="*70)
    print("🧪 TESTING SISTEMA DINÁMICO")
    print("="*70)

    # Inicializar tester
    tester = APITester(BASE_URL, ADMIN_TOKEN, USER_TOKEN)

    print("\n📋 ADMIN: Crear Integraciones")
    print("-" * 70)

    api_id_1 = tester.crear_integracion_reniec()
    api_id_2 = tester.crear_integracion_facturiza()

    print("\n📋 ADMIN: Listar Integraciones")
    print("-" * 70)
    tester.listar_integraciones()

    print("\n📋 ADMIN: Probar Integraciones")
    print("-" * 70)
    if api_id_1:
        tester.probar_integracion(api_id_1)

    print("\n📋 ADMIN: Crear Campos Dinámicos")
    print("-" * 70)
    campo_id_1 = tester.crear_campo_dni(api_id_1 or 1)
    campo_id_2 = tester.crear_campo_nombre()

    print("\n📋 ADMIN: Listar Campos")
    print("-" * 70)
    tester.listar_campos()

    print("\n📋 ADMIN: Estadísticas")
    print("-" * 70)
    tester.obtener_estadisticas()

    print("\n👤 USUARIO: Consultas sin Autenticación")
    print("-" * 70)
    tester.consultar_dni()
    tester.consultar_ruc()
    tester.probar_reniec()
    tester.probar_facturiza()

    print("\n👤 USUARIO: Historial y Registro")
    print("-" * 70)
    tester.obtener_historial()
    tester.guardar_registro({
        "documento_identidad": "12345678",
        "nombre_completo": "Juan Pérez García"
    })

    print("\n" + "="*70)
    print("✅ TESTING COMPLETADO")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
