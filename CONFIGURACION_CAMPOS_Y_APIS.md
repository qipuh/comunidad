# ⚙️ Configuración Dinámmica de Campos e Integración con APIs Externas

**Módulo avanzado:** Sistema configurable para definir campos del registro de usuario e integración con APIs de consulta de datos (RENIEC, Facturiza, etc.).

---

## 🎯 Objetivo

Permitir que los **administradores**:
1. **Definir dinámicamente** qué campos se mostrarán en el registro
2. **Asignar tipo de dato** a cada campo (String, Number, Date, Enum, etc.)
3. **Hacer campos obligatorios u opcionales**
4. **Conectar APIs externas** para auto-llenar datos (RENIEC, Facturiza, etc.)
5. **Validar datos** contra fuentes oficiales
6. **Guardar historial** de validaciones

---

## 📊 Nueva Arquitectura de Datos

### Tabla: ConfiguracionCampo
```
ConfiguracionCampo
├─ id (PK)
├─ nombre_campo (único)          # "documento_identidad", "numero_casa"
├─ etiqueta                      # "Documento de Identidad", "Número de Casa"
├─ tipo_dato (enum)              # "string", "number", "date", "enum", "boolean", "email"
├─ es_obligatorio                # true/false
├─ posicion                       # orden en formulario (1, 2, 3...)
├─ expresion_regex               # /^\d{8}$/ para validación
├─ valores_enum (JSON)           # ["opción1", "opción2"] si tipo_dato="enum"
├─ api_integracion_id (FK)       # Link a integración externa
├─ campo_mapa_api                # Campo en API remota (ej: "dni" en RENIEC)
├─ mostrar_en_registro           # true/false - mostrar en formulario
├─ mostrar_en_perfil             # true/false - visible después del registro
├─ mostrar_en_reportes           # true/false - incluir en reportes
├─ creado_por                    # Usuario admin que lo creó
├─ created_at
└─ updated_at
```

### Tabla: IntegracionAPI
```
IntegracionAPI
├─ id (PK)
├─ nombre                        # "RENIEC", "Facturiza", "Custom"
├─ tipo (enum)                   # "reniec", "facturiza", "custom", "sunat"
├─ endpoint_url                  # URL base de la API
├─ auth_type (enum)              # "bearer", "api_key", "oauth2", "basic"
├─ auth_token                    # Token/API Key (encriptado)
├─ descripcion
├─ activa (bool)
├─ timeout_segundos
├─ max_reintentos
├─ created_at
└─ updated_at
```

### Tabla: ConsultaExterna
```
ConsultaExterna
├─ id (PK)
├─ usuario_id (FK)
├─ integracion_api_id (FK)
├─ tipo_consulta                 # "documento", "empresa", "domicilio"
├─ parametro_busqueda            # El valor buscado (DNI, RUC, etc.)
├─ respuesta_json                # Datos retornados por API
├─ campos_mapeados (JSON)        # Qué campos se auto-llenaron
├─ estado                         # "exitosa", "fallida", "pendiente"
├─ mensaje_error                 # Si falló
├─ timestamp
└─ ip_origen
```

### Tabla: CampoUsuario (Flexible)
```
CampoUsuario
├─ id (PK)
├─ usuario_id (FK)
├─ configuracion_campo_id (FK)   # Link a ConfiguracionCampo
├─ valor                         # El valor del campo (como string)
├─ fue_validado_externamente     # true si viene de API
├─ fuente_externa_id (FK)        # Link a ConsultaExterna si aplica
├─ created_at
└─ updated_at
```

---

## 🔌 Integraciones Soportadas

### 1. RENIEC (Perú)
```
Endpoint: https://api.reniec.gob.pe/dni/[dni]
Método: GET
Auth: Bearer token

Campos disponibles:
├─ nombres
├─ apellido_paterno
├─ apellido_materno
├─ genero
├─ fecha_nacimiento
├─ estado_civil
└─ fotografia_url
```

### 2. Facturiza (Facturación)
```
Endpoint: https://api.facturiza.com/consultas/ruc
Método: POST
Auth: API Key

Campos disponibles:
├─ razon_social
├─ direccion
├─ representante_legal
├─ actividad_economica
├─ estado_contribuyente
└─ fecha_inscripcion
```

### 3. SUNAT (RUC - Perú)
```
Endpoint: https://ws.sunat.gob.pe/cl-ti-itconfigserv/jaxwsservice/getStatus
Método: SOAP
Auth: Certificado digital

Campos disponibles:
├─ nombre_completo
├─ razon_social
├─ estado
├─ domicilio_fisico
└─ domicilio_fiscal
```

### 4. Custom API
```
Endpoint: Personalizable
Método: GET/POST (configurable)
Auth: Bearer, API Key, Basic, OAuth2

Mapeo: Configurable por administrador
```

---

## 🏗️ Arquitectura del Módulo

```
ADMIN PANEL (Vue.js)
├─ ConfiguradorCampos.vue
│  ├─ Crear/editar campo
│  ├─ Seleccionar tipo de dato
│  ├─ Asignar API externa (opcional)
│  ├─ Validar expresión regex
│  └─ Guardar orden en formulario
│
├─ ConfiguradorAPIs.vue
│  ├─ Crear integración
│  ├─ Probar conexión
│  ├─ Mapear campos
│  └─ Guardar credenciales (encriptadas)
│
└─ HistorialValidaciones.vue
   ├─ Ver consultas realizadas
   ├─ Resultado de validaciones
   └─ Errores y reintentos


BACKEND (FastAPI)
├─ services/
│  ├─ configuracion_campos_service.py
│  ├─ integracion_api_service.py
│  ├─ validacion_externa_service.py
│  └─ mapeo_campos_service.py
│
├─ routes/
│  ├─ configuracion_campos.py
│  ├─ integraciones_api.py
│  ├─ validaciones.py
│  └─ admin.py
│
└─ clients/
   ├─ reniec_client.py
   ├─ facturiza_client.py
   ├─ sunat_client.py
   └─ custom_api_client.py
```

---

## 📝 Flujo de Uso

### Escenario 1: Administrador Configura Campos

```
1. Admin abre ConfiguradorCampos
   ├─ Nombre: "documento_identidad"
   ├─ Etiqueta: "Documento de Identidad"
   ├─ Tipo: "string"
   ├─ Obligatorio: true
   ├─ Regex: ^[0-9]{8}$
   └─ API: RENIEC

2. Admin abre ConfiguradorAPIs
   ├─ Nombre: "RENIEC"
   ├─ Endpoint: https://api.reniec.gob.pe/dni/
   ├─ Auth: Bearer token
   ├─ Token: ****** (encriptado)
   └─ Probar conexión ✓

3. Admin mapea campos
   ├─ Campo "nombre" → RENIEC.nombres
   ├─ Campo "apellido" → RENIEC.apellido_paterno + apellido_materno
   └─ Guardar mapping

4. ✓ Configuración lista
```

### Escenario 2: Usuario se Registra

```
1. Usuario abre formulario de registro
   ├─ Ve campos configurados (en orden)
   └─ Algunos tienen 🔗 (icono de API)

2. Usuario ingresa documento: "12345678"

3. Sistema detecta integración RENIEC
   ├─ Envía query: GET /dni/12345678
   ├─ Backend consulta RENIEC
   ├─ RENIEC responde con datos
   └─ Auto-llenan campos "nombre", "apellido", "fecha_nacimiento"

4. Usuario confirma/corrige datos
   └─ Marca "validado externamente"

5. Usuario completa campos faltantes
   ├─ Foto (facial)
   └─ Teléfono

6. ✓ Registro exitoso
   ├─ Datos guardados
   ├─ Registro de validación externo creado
   └─ Historial actualizado
```

---

## 💻 Código Ejemplo: Backend

### Modelo de Datos (SQLAlchemy)

```python
# backend/app/models/configuracion.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

class TipoDatoEnum(str, enum.Enum):
    STRING = "string"
    NUMBER = "number"
    DATE = "date"
    ENUM = "enum"
    BOOLEAN = "boolean"
    EMAIL = "email"
    PHONE = "phone"
    URL = "url"

class TipoAPIEnum(str, enum.Enum):
    RENIEC = "reniec"
    FACTURIZA = "facturiza"
    SUNAT = "sunat"
    CUSTOM = "custom"

class AuthTypeEnum(str, enum.Enum):
    BEARER = "bearer"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    BASIC = "basic"

class ConfiguracionCampo(Base):
    __tablename__ = "configuracion_campos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_campo = Column(String(100), unique=True, nullable=False)
    etiqueta = Column(String(255), nullable=False)
    tipo_dato = Column(Enum(TipoDatoEnum), nullable=False)
    es_obligatorio = Column(Boolean, default=False)
    posicion = Column(Integer, default=0)  # Orden en formulario
    expresion_regex = Column(String(500), nullable=True)
    valores_enum = Column(JSON, nullable=True)  # ["opción1", "opción2"]
    
    # Integración externa
    api_integracion_id = Column(Integer, ForeignKey("integraciones_api.id"), nullable=True)
    campo_mapa_api = Column(String(100), nullable=True)  # Campo en API remota
    
    # Visibilidad
    mostrar_en_registro = Column(Boolean, default=True)
    mostrar_en_perfil = Column(Boolean, default=True)
    mostrar_en_reportes = Column(Boolean, default=True)
    
    # Auditoría
    creado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    api_integracion = relationship("IntegracionAPI", back_populates="campos_configurados")
    campos_usuario = relationship("CampoUsuario", back_populates="configuracion")

class IntegracionAPI(Base):
    __tablename__ = "integraciones_api"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(Enum(TipoAPIEnum), nullable=False)
    endpoint_url = Column(String(500), nullable=False)
    auth_type = Column(Enum(AuthTypeEnum), nullable=False)
    auth_token = Column(String(500), nullable=False)  # Encriptado
    descripcion = Column(String(500), nullable=True)
    activa = Column(Boolean, default=True)
    timeout_segundos = Column(Integer, default=30)
    max_reintentos = Column(Integer, default=3)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    campos_configurados = relationship("ConfiguracionCampo", back_populates="api_integracion")
    consultas = relationship("ConsultaExterna", back_populates="integracion")

class ConsultaExterna(Base):
    __tablename__ = "consultas_externas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    integracion_api_id = Column(Integer, ForeignKey("integraciones_api.id"), nullable=False)
    tipo_consulta = Column(String(50))  # "documento", "empresa", "domicilio"
    parametro_busqueda = Column(String(255), nullable=False)
    respuesta_json = Column(JSON, nullable=True)
    campos_mapeados = Column(JSON, nullable=True)  # {"nombre": "Juan", "apellido": "Pérez"}
    estado = Column(String(50), default="pendiente")  # exitosa, fallida
    mensaje_error = Column(String(500), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_origen = Column(String(45), nullable=True)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="consultas_externas")
    integracion = relationship("IntegracionAPI", back_populates="consultas")

class CampoUsuario(Base):
    __tablename__ = "campos_usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    configuracion_campo_id = Column(Integer, ForeignKey("configuracion_campos.id"), nullable=False)
    valor = Column(String(1000), nullable=True)  # Valor del campo
    fue_validado_externamente = Column(Boolean, default=False)
    consulta_externa_id = Column(Integer, ForeignKey("consultas_externas.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="campos_customizados")
    configuracion = relationship("ConfiguracionCampo", back_populates="campos_usuario")
    consulta_externa = relationship("ConsultaExterna")
```

### Servicio de Integración API

```python
# backend/app/services/integracion_api_service.py
import requests
import json
from typing import Dict, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class IntegracionAPIService:
    """
    Servicio para consultar APIs externas (RENIEC, Facturiza, etc.)
    y mapear respuestas a campos del sistema.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def consultar_reniec(self, dni: str, integracion: IntegracionAPI) -> Dict:
        """
        Consulta RENIEC por DNI.
        
        Args:
            dni: Número de documento (8 dígitos)
            integracion: Objeto IntegracionAPI con configuración
        
        Returns:
            {
                "exitosa": bool,
                "datos": {...},
                "error": str (si falló)
            }
        """
        try:
            if not integracion.activa:
                return {"exitosa": False, "error": "Integración RENIEC desactivada"}
            
            url = f"{integracion.endpoint_url}{dni}"
            headers = {"Authorization": f"Bearer {integracion.auth_token}"}
            
            response = requests.get(
                url,
                headers=headers,
                timeout=integracion.timeout_segundos
            )
            response.raise_for_status()
            
            datos = response.json()
            
            # Mapear respuesta RENIEC
            datos_mapeados = {
                "nombre": datos.get("nombres"),
                "apellido_paterno": datos.get("apellido_paterno"),
                "apellido_materno": datos.get("apellido_materno"),
                "genero": datos.get("genero"),
                "fecha_nacimiento": datos.get("fecha_nacimiento"),
                "estado_civil": datos.get("estado_civil")
            }
            
            return {
                "exitosa": True,
                "datos": datos_mapeados,
                "respuesta_original": datos
            }
        
        except requests.exceptions.Timeout:
            return {"exitosa": False, "error": f"Timeout ({integracion.timeout_segundos}s)"}
        except requests.exceptions.HTTPError as e:
            return {"exitosa": False, "error": f"HTTP {e.response.status_code}"}
        except Exception as e:
            logger.error(f"Error consultando RENIEC: {str(e)}")
            return {"exitosa": False, "error": str(e)}
    
    def consultar_facturiza(self, ruc: str, integracion: IntegracionAPI) -> Dict:
        """Consulta Facturiza por RUC"""
        try:
            url = integracion.endpoint_url
            headers = {"X-API-Key": integracion.auth_token}
            payload = {"ruc": ruc}
            
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=integracion.timeout_segundos
            )
            response.raise_for_status()
            
            datos = response.json()
            
            datos_mapeados = {
                "razon_social": datos.get("razon_social"),
                "direccion": datos.get("direccion"),
                "representante_legal": datos.get("representante_legal"),
                "actividad_economica": datos.get("actividad_economica"),
                "estado_contribuyente": datos.get("estado_contribuyente")
            }
            
            return {
                "exitosa": True,
                "datos": datos_mapeados,
                "respuesta_original": datos
            }
        except Exception as e:
            return {"exitosa": False, "error": str(e)}
    
    def consultar_api_custom(self, parametro: str, integracion: IntegracionAPI) -> Dict:
        """Consulta API personalizada (configurable)"""
        try:
            # Implementación genérica para APIs custom
            url = integracion.endpoint_url
            
            # Determinar método y headers
            headers = {}
            if integracion.auth_type.value == "bearer":
                headers["Authorization"] = f"Bearer {integracion.auth_token}"
            elif integracion.auth_type.value == "api_key":
                headers["X-API-Key"] = integracion.auth_token
            
            response = requests.get(
                url,
                params={"q": parametro},
                headers=headers,
                timeout=integracion.timeout_segundos
            )
            response.raise_for_status()
            
            return {
                "exitosa": True,
                "datos": response.json(),
                "respuesta_original": response.json()
            }
        except Exception as e:
            return {"exitosa": False, "error": str(e)}
    
    def registrar_consulta(
        self,
        usuario_id: int,
        integracion_id: int,
        tipo_consulta: str,
        parametro: str,
        respuesta: Dict,
        estado: str,
        ip_origen: str
    ):
        """Registra consulta realizada a API externa para auditoría"""
        from app.models.configuracion import ConsultaExterna
        
        consulta = ConsultaExterna(
            usuario_id=usuario_id,
            integracion_api_id=integracion_id,
            tipo_consulta=tipo_consulta,
            parametro_busqueda=parametro,
            respuesta_json=respuesta if estado == "exitosa" else None,
            estado=estado,
            mensaje_error=respuesta.get("error") if estado == "fallida" else None,
            ip_origen=ip_origen
        )
        self.db.add(consulta)
        self.db.commit()
        return consulta
```

### Endpoint para Auto-llenar Formulario

```python
# backend/app/routes/validaciones.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.services.integracion_api_service import IntegracionAPIService
from app.models.configuracion import ConfiguracionCampo, IntegracionAPI
from app.db.database import get_db

router = APIRouter(prefix="/api/validaciones", tags=["validaciones"])

@router.post("/consultar-dni")
async def consultar_dni(
    dni: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Consulta RENIEC por DNI y retorna datos para auto-llenar formulario.
    
    Endpoint: POST /api/validaciones/consultar-dni
    Body: { "dni": "12345678" }
    Response: {
        "exitosa": true,
        "datos": {
            "nombre": "Juan",
            "apellido_paterno": "Pérez",
            ...
        }
    }
    """
    
    # Validar formato DNI
    if not dni.isdigit() or len(dni) != 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="DNI debe ser 8 dígitos"
        )
    
    # Obtener configuración de RENIEC
    config_dni = db.query(ConfiguracionCampo).filter_by(
        nombre_campo="documento_identidad"
    ).first()
    
    if not config_dni or not config_dni.api_integracion_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="RENIEC no está configurado"
        )
    
    integracion = db.query(IntegracionAPI).filter_by(
        id=config_dni.api_integracion_id
    ).first()
    
    if not integracion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integración RENIEC no encontrada"
        )
    
    # Consultar RENIEC
    service = IntegracionAPIService(db)
    resultado = service.consultar_reniec(dni, integracion)
    
    # Registrar consulta para auditoría
    ip_origen = request.client.host
    service.registrar_consulta(
        usuario_id=None,  # Aún no se registra
        integracion_id=integracion.id,
        tipo_consulta="documento",
        parametro=dni,
        respuesta=resultado,
        estado="exitosa" if resultado["exitosa"] else "fallida",
        ip_origen=ip_origen
    )
    
    if not resultado["exitosa"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error consultando RENIEC: {resultado.get('error')}"
        )
    
    return {
        "exitosa": True,
        "datos": resultado["datos"],
        "validado_externamente": True
    }

@router.post("/consultar-ruc")
async def consultar_ruc(
    ruc: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Consulta Facturiza por RUC"""
    
    if not ruc.isdigit() or len(ruc) != 11:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="RUC debe ser 11 dígitos"
        )
    
    integracion = db.query(IntegracionAPI).filter_by(
        tipo="facturiza",
        activa=True
    ).first()
    
    if not integracion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Facturiza no está configurado"
        )
    
    service = IntegracionAPIService(db)
    resultado = service.consultar_facturiza(ruc, integracion)
    
    ip_origen = request.client.host
    service.registrar_consulta(
        usuario_id=None,
        integracion_id=integracion.id,
        tipo_consulta="empresa",
        parametro=ruc,
        respuesta=resultado,
        estado="exitosa" if resultado["exitosa"] else "fallida",
        ip_origen=ip_origen
    )
    
    if not resultado["exitosa"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado.get("error")
        )
    
    return {
        "exitosa": True,
        "datos": resultado["datos"],
        "validado_externamente": True
    }
```

---

## 🎨 Componentes Vue.js 3

### ConfiguradorCampos.vue

```vue
<!-- frontend/src/components/admin/ConfiguradorCampos.vue -->
<template>
  <div class="configurador-campos">
    <h2>Configurar Campos de Registro</h2>
    
    <button @click="mostrarNuevoCampo = true" class="btn-primary">
      ➕ Nuevo Campo
    </button>
    
    <!-- Lista de campos existentes -->
    <div class="campos-list">
      <div v-for="campo in campos" :key="campo.id" class="campo-item">
        <div class="drag-handle">≡</div>
        <div class="campo-info">
          <p><strong>{{ campo.etiqueta }}</strong></p>
          <small>{{ campo.nombre_campo }} ({{ campo.tipo_dato }})</small>
          <small v-if="campo.es_obligatorio" class="badge-obligatorio">Obligatorio</small>
          <small v-if="campo.api_integracion_id" class="badge-api">🔗 API</small>
        </div>
        <div class="campo-actions">
          <button @click="editarCampo(campo)">✏️ Editar</button>
          <button @click="eliminarCampo(campo.id)">🗑️ Eliminar</button>
        </div>
      </div>
    </div>
    
    <!-- Modal: Nuevo/Editar Campo -->
    <div v-if="mostrarNuevoCampo" class="modal">
      <div class="modal-content">
        <h3>{{ editandoCampo ? 'Editar' : 'Nuevo' }} Campo</h3>
        
        <div class="form-group">
          <label>Nombre del Campo *</label>
          <input v-model="formulario.nombre_campo" type="text" 
                 placeholder="documento_identidad" />
        </div>
        
        <div class="form-group">
          <label>Etiqueta (lo que ve el usuario) *</label>
          <input v-model="formulario.etiqueta" type="text" 
                 placeholder="Documento de Identidad" />
        </div>
        
        <div class="form-group">
          <label>Tipo de Dato *</label>
          <select v-model="formulario.tipo_dato">
            <option value="string">Texto</option>
            <option value="number">Número</option>
            <option value="date">Fecha</option>
            <option value="email">Email</option>
            <option value="phone">Teléfono</option>
            <option value="enum">Lista de Opciones</option>
            <option value="boolean">Sí/No</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>
            <input v-model="formulario.es_obligatorio" type="checkbox" />
            Campo Obligatorio
          </label>
        </div>
        
        <div class="form-group">
          <label>Expresión Regular (validación)</label>
          <input v-model="formulario.expresion_regex" type="text" 
                 placeholder="^[0-9]{8}$" />
        </div>
        
        <!-- Si es enum -->
        <div v-if="formulario.tipo_dato === 'enum'" class="form-group">
          <label>Valores (separados por coma)</label>
          <textarea v-model="formulario.valores_enum_texto"></textarea>
          <small>Ej: Opción 1, Opción 2, Opción 3</small>
        </div>
        
        <!-- Integración con API -->
        <div class="form-group">
          <label>Conectar con API Externa</label>
          <select v-model="formulario.api_integracion_id">
            <option :value="null">-- Sin API --</option>
            <option v-for="api in apis" :key="api.id" :value="api.id">
              {{ api.nombre }}
            </option>
          </select>
        </div>
        
        <div v-if="formulario.api_integracion_id" class="form-group">
          <label>Campo en la API que mapea a este</label>
          <input v-model="formulario.campo_mapa_api" type="text" 
                 placeholder="nombres, apellido_paterno, etc." />
        </div>
        
        <!-- Visibilidad -->
        <div class="form-group">
          <h4>Visibilidad</h4>
          <label>
            <input v-model="formulario.mostrar_en_registro" type="checkbox" />
            Mostrar en formulario de registro
          </label>
          <label>
            <input v-model="formulario.mostrar_en_perfil" type="checkbox" />
            Mostrar en perfil del usuario
          </label>
          <label>
            <input v-model="formulario.mostrar_en_reportes" type="checkbox" />
            Incluir en reportes
          </label>
        </div>
        
        <div class="modal-actions">
          <button @click="guardarCampo" class="btn-success">💾 Guardar</button>
          <button @click="cancelar" class="btn-secondary">Cancelar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '@/services/api'

interface Campo {
  id: number
  nombre_campo: string
  etiqueta: string
  tipo_dato: string
  es_obligatorio: boolean
  expresion_regex?: string
  api_integracion_id?: number
  campo_mapa_api?: string
  mostrar_en_registro: boolean
  mostrar_en_perfil: boolean
  mostrar_en_reportes: boolean
}

const campos = ref<Campo[]>([])
const apis = ref<any[]>([])
const mostrarNuevoCampo = ref(false)
const editandoCampo = ref(false)

const formulario = ref({
  nombre_campo: '',
  etiqueta: '',
  tipo_dato: 'string',
  es_obligatorio: false,
  expresion_regex: '',
  valores_enum_texto: '',
  api_integracion_id: null,
  campo_mapa_api: '',
  mostrar_en_registro: true,
  mostrar_en_perfil: true,
  mostrar_en_reportes: true
})

onMounted(async () => {
  await cargarCampos()
  await cargarAPIs()
})

const cargarCampos = async () => {
  try {
    const res = await api.get('/admin/configuracion/campos')
    campos.value = res.data.campos
  } catch (error) {
    console.error('Error cargando campos:', error)
  }
}

const cargarAPIs = async () => {
  try {
    const res = await api.get('/admin/integraciones-api')
    apis.value = res.data.apis
  } catch (error) {
    console.error('Error cargando APIs:', error)
  }
}

const editarCampo = (campo: Campo) => {
  formulario.value = { ...campo, valores_enum_texto: '' }
  editandoCampo.value = true
  mostrarNuevoCampo.value = true
}

const guardarCampo = async () => {
  try {
    const datos = { ...formulario.value }
    if (formulario.value.tipo_dato === 'enum') {
      datos.valores_enum = formulario.value.valores_enum_texto.split(',').map(v => v.trim())
    }
    
    await api.post('/admin/configuracion/campos', datos)
    await cargarCampos()
    cancelar()
  } catch (error) {
    console.error('Error guardando campo:', error)
  }
}

const eliminarCampo = async (id: number) => {
  if (confirm('¿Eliminar este campo?')) {
    try {
      await api.delete(`/admin/configuracion/campos/${id}`)
      await cargarCampos()
    } catch (error) {
      console.error('Error eliminando campo:', error)
    }
  }
}

const cancelar = () => {
  mostrarNuevoCampo.value = false
  editandoCampo.value = false
  formulario.value = {
    nombre_campo: '',
    etiqueta: '',
    tipo_dato: 'string',
    es_obligatorio: false,
    expresion_regex: '',
    valores_enum_texto: '',
    api_integracion_id: null,
    campo_mapa_api: '',
    mostrar_en_registro: true,
    mostrar_en_perfil: true,
    mostrar_en_reportes: true
  }
}
</script>

<style scoped>
.configurador-campos {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.campos-list {
  margin-top: 20px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.campo-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #e5e7eb;
  gap: 15px;
}

.campo-item:last-child {
  border-bottom: none;
}

.drag-handle {
  cursor: grab;
  color: #9ca3af;
  font-size: 18px;
}

.campo-info {
  flex: 1;
}

.campo-info p {
  margin: 0;
  font-weight: 600;
}

.campo-info small {
  display: inline-block;
  margin-right: 10px;
  color: #6b7280;
  font-size: 12px;
}

.badge-obligatorio,
.badge-api {
  background: #dbeafe;
  color: #1e40af;
  padding: 2px 6px;
  border-radius: 3px;
}

.badge-api {
  background: #dcfce7;
  color: #166534;
}

.campo-actions {
  display: flex;
  gap: 10px;
}

.campo-actions button {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #374151;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-family: inherit;
}

.modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.btn-success,
.btn-secondary {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.btn-success {
  background: #10b981;
  color: white;
}

.btn-secondary {
  background: #e5e7eb;
  color: #374151;
}
</style>
```

---

## 🔐 Seguridad

- **Encriptación de tokens:** Usar `cryptography.Fernet` para encriptar auth tokens antes de guardar en BD
- **Rate limiting:** Máximo 10 consultas por usuario por hora a APIs externas
- **Validación:** Validar respuestas de APIs antes de mapear datos
- **Auditoría:** Registrar todas las consultas externas con IP, timestamp, usuario
- **Retry logic:** Reintentar 3 veces en caso de timeout o error 5xx
- **CORS:** Solo permitir llamadas desde dominio autorizado

---

## 📋 Próximas Secciones

Este documento continúa con:
- Configurador de APIs (ConfiguradorAPIs.vue)
- Formulario dinámico que ajusta campos según configuración
- Historial de validaciones y auditoría
- Ejemplos de integración RENIEC, Facturiza, SUNAT

¿Necesitas que continúe con estas secciones?

