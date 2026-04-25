# Modelos de Datos en Python (SQLAlchemy)

## Estructura Base

```python
# backend/app/models/__init__.py
from .usuario import Usuario, Familia
from .foto import FotoUsuario
from .aportacion import Aportacion, PeriodoAporte
from .reunion import Reunion, Asistencia
from .eleccion import Eleccion, Candidato, Voto

__all__ = [
    'Usuario', 'Familia', 'FotoUsuario', 
    'Aportacion', 'PeriodoAporte',
    'Reunion', 'Asistencia',
    'Eleccion', 'Candidato', 'Voto'
]
```

---

## 1. USUARIO Y FAMILIA

```python
# backend/app/models/usuario.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class RolEnum(str, enum.Enum):
    VECINO = "vecino"
    ADMINISTRADOR = "administrador"
    TESORERO = "tesorero"
    JUNTA_DIRECTIVA = "junta_directiva"

class EstadoEnum(str, enum.Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    SUSPENDIDO = "suspendido"

class Familia(Base):
    __tablename__ = "familias"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_grupo = Column(String(255), nullable=False)
    jefe_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    direccion = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    usuarios = relationship("Usuario", back_populates="familia")
    jefe = relationship("Usuario", foreign_keys=[jefe_id], viewonly=True)

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos básicos
    email = Column(String(255), unique=True, nullable=False, index=True)
    nombre = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    
    # Rol y estado
    rol = Column(Enum(RolEnum), default=RolEnum.VECINO, nullable=False)
    estado = Column(Enum(EstadoEnum), default=EstadoEnum.ACTIVO, nullable=False)
    
    # Familia
    familia_id = Column(Integer, ForeignKey("familias.id"), nullable=True)
    es_jefe_familia = Column(Boolean, default=False)
    
    # Dirección (heredada de familia o propia)
    direccion = Column(String(500), nullable=True)
    
    # ════════════════════════════════════════════════════════════════
    # ⚠️ CAMPOS ABIERTOS - COMPLETAR EN TABLA ABAJO
    # ════════════════════════════════════════════════════════════════
    # Ejemplos que puedes descomentar:
    # numero_casa = Column(String(50), nullable=True)
    # fecha_ingreso = Column(DateTime, nullable=True)
    # documento_identidad = Column(String(50), nullable=True)
    # profesion = Column(String(255), nullable=True)
    # campos_customizados = Column(JSON, nullable=True)  # Para flexibilidad
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    familia = relationship("Familia", back_populates="usuarios", foreign_keys=[familia_id])
    fotos = relationship("FotoUsuario", back_populates="usuario", cascade="all, delete-orphan")
    aportaciones = relationship("Aportacion", back_populates="usuario", cascade="all, delete-orphan")
    asistencias = relationship("Asistencia", back_populates="usuario", cascade="all, delete-orphan")
    votos = relationship("Voto", back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre={self.nombre}, email={self.email})>"
```

---

## 2. FOTOS Y EMBEDDINGS

```python
# backend/app/models/foto.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime

class FotoUsuario(Base):
    __tablename__ = "fotos_usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    
    # Tipo de foto (frontal, lateral izquierdo, lateral derecho)
    tipo = Column(
        String(50), 
        nullable=False,
        # Valores válidos: "frontal", "lateral_izquierdo", "lateral_derecho"
    )
    
    # Embedding como vector (128 valores float)
    # Almacenar como JSON para portabilidad
    embedding = Column(JSON, nullable=False)  # List[float] de 128 elementos
    
    # URL de la imagen en cloud storage (S3, Azure Blob, etc.)
    url_archivo = Column(String(500), nullable=True)
    
    # Metadatos
    fecha_captura = Column(DateTime, default=datetime.utcnow)
    score_calidad = Column(Float, nullable=True)  # 0-100 (opcional, para QA)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación
    usuario = relationship("Usuario", back_populates="fotos")
    
    def __repr__(self):
        return f"<FotoUsuario(usuario_id={self.usuario_id}, tipo={self.tipo})>"
```

---

## 3. APORTACIONES Y PERÍODOS

```python
# backend/app/models/aportacion.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

class TipoAporteEnum(str, enum.Enum):
    ORDINARIA = "ordinaria"
    EXTRAORDINARIA = "extraordinaria"
    DONACION = "donacion"

class FormaPagoEnum(str, enum.Enum):
    EFECTIVO = "efectivo"
    TRANSFERENCIA = "transferencia"
    CHEQUE = "cheque"
    TARJETA = "tarjeta"

class FrecuenciaEnum(str, enum.Enum):
    MENSUAL = "mensual"
    BIMESTRAL = "bimestral"
    TRIMESTRAL = "trimestral"
    SEMESTRAL = "semestral"
    ANUAL = "anual"

class PeriodoAporte(Base):
    __tablename__ = "periodos_aporte"
    
    id = Column(Integer, primary_key=True, index=True)
    frecuencia = Column(Enum(FrecuenciaEnum), nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    estado = Column(String(50), default="activo")  # activo, cerrado
    descripcion = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación
    aportaciones = relationship("Aportacion", back_populates="periodo")

class Aportacion(Base):
    __tablename__ = "aportaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    periodo_id = Column(Integer, ForeignKey("periodos_aporte.id"), nullable=True)
    
    tipo = Column(Enum(TipoAporteEnum), nullable=False)
    monto = Column(Float, nullable=False)
    fecha = Column(DateTime, nullable=False)
    forma_pago = Column(Enum(FormaPagoEnum), nullable=True)
    
    # Comprobante: URL a archivo en cloud storage
    comprobante_url = Column(String(500), nullable=True)
    
    # Observaciones
    observaciones = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="aportaciones")
    periodo = relationship("PeriodoAporte", back_populates="aportaciones")
    
    def __repr__(self):
        return f"<Aportacion(usuario_id={self.usuario_id}, monto={self.monto}, fecha={self.fecha})>"
```

---

## 4. REUNIONES Y ASISTENCIA

```python
# backend/app/models/reunion.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime

class EstadoReunionEnum(str, enum.Enum):
    PROGRAMADA = "programada"
    EN_CURSO = "en_curso"
    FINALIZADA = "finalizada"
    CANCELADA = "cancelada"

class Reunion(Base):
    __tablename__ = "reuniones"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha = Column(DateTime, nullable=False)
    hora = Column(String(5), nullable=False)  # HH:MM
    lugar = Column(String(500), nullable=False)
    
    orden_dia = Column(Text, nullable=True)  # Puntos a tratar
    quorum_requerido = Column(Integer, default=50)  # Porcentaje (%)
    estado = Column(Enum(EstadoReunionEnum), default=EstadoReunionEnum.PROGRAMADA)
    
    # Validación facial
    requiere_validacion_facial = Column(Boolean, default=True)
    umbral_facial = Column(Float, default=60.0)  # Score mínimo (0-100)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación
    asistencias = relationship("Asistencia", back_populates="reunion", cascade="all, delete-orphan")

class Asistencia(Base):
    __tablename__ = "asistencias"
    
    id = Column(Integer, primary_key=True, index=True)
    reunion_id = Column(Integer, ForeignKey("reuniones.id"), nullable=False, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    
    presente = Column(Boolean, default=False)
    hora_llegada = Column(DateTime, nullable=True)
    
    # Validación facial
    score_facial = Column(Float, nullable=True)  # 0-100
    validacion_exitosa = Column(Boolean, default=False)
    validated_at = Column(DateTime, nullable=True)
    
    # Intentos de validación
    intentos = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    reunion = relationship("Reunion", back_populates="asistencias")
    usuario = relationship("Usuario", back_populates="asistencias")
```

---

## 5. ELECCIONES Y VOTOS

```python
# backend/app/models/eleccion.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class EstadoEleccionEnum(str, enum.Enum):
    ABIERTA = "abierta"
    CERRADA = "cerrada"
    CANCELADA = "cancelada"
    RESULTADOS = "resultados"

class Eleccion(Base):
    __tablename__ = "elecciones"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    estado = Column(Enum(EstadoEleccionEnum), default=EstadoEleccionEnum.ABIERTA)
    
    # Padrón habilitado (CSV de emails o IDs de usuarios)
    padron_usuario_ids = Column(JSON, nullable=True)  # List[int]
    
    # Validación facial
    umbral_facial = Column(Float, default=65.0)  # Score mínimo
    requerir_validacion_facial = Column(Boolean, default=True)
    
    # Tipo de voto
    tipo_voto = Column(String(50), default="secreto")  # secreto, nominal, etc.
    
    # Auditoría
    permitir_auditoría = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    candidatos = relationship("Candidato", back_populates="eleccion", cascade="all, delete-orphan")
    votos = relationship("Voto", back_populates="eleccion", cascade="all, delete-orphan")

class Candidato(Base):
    __tablename__ = "candidatos"
    
    id = Column(Integer, primary_key=True, index=True)
    eleccion_id = Column(Integer, ForeignKey("elecciones.id"), nullable=False, index=True)
    
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    numero_orden = Column(Integer, nullable=False)
    
    votos_recibidos = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación
    eleccion = relationship("Eleccion", back_populates="candidatos")
    votos = relationship("Voto", back_populates="candidato")

class Voto(Base):
    __tablename__ = "votos"
    
    id = Column(Integer, primary_key=True, index=True)
    eleccion_id = Column(Integer, ForeignKey("elecciones.id"), nullable=False, index=True)
    candidato_id = Column(Integer, ForeignKey("candidatos.id"), nullable=False, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)  # Nullable para anonimato
    
    # Token anónimo para voto secreto
    # (desvincula usuario_id del voto después de validación)
    token_anonimo = Column(String(255), unique=True, nullable=False, index=True)
    
    # Validación facial
    score_facial = Column(Float, nullable=False)
    validated_at = Column(DateTime, nullable=False)
    
    # Auditoría: fingerprint para rastrear fraude
    # (sin revelar quién votó qué)
    fingerprint = Column(String(255), nullable=False)  # hash(ip + user_agent + timestamp)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    eleccion = relationship("Eleccion", back_populates="votos")
    candidato = relationship("Candidato", back_populates="votos")
    usuario = relationship("Usuario", back_populates="votos")
```

---

---

## 6. CONFIGURACIÓN DINÁMICA - CAMPOS Y APIS (NUEVO MÓDULO)

### 🎯 Descripción
Estos modelos permiten configurar **campos dinámicos para el registro** sin modificar la base de datos. Los administradores pueden:
- Crear/editar/eliminar campos de registro
- Integrar APIs externas (RENIEC para DNI, Facturiza para RUC, etc.)
- Auto-llenar datos del usuario desde APIs
- Auditar todas las consultas externas

```python
# backend/app/models/configuracion.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

# ════════════════════════════════════════════════════════════════════
# ENUMS PARA CONFIGURACIÓN
# ════════════════════════════════════════════════════════════════════

class TipoDatoEnum(str, enum.Enum):
    """Tipos de datos para campos dinámicos"""
    STRING = "string"
    NUMBER = "number"
    DATE = "date"
    ENUM = "enum"
    BOOLEAN = "boolean"
    EMAIL = "email"
    PHONE = "phone"
    URL = "url"

class TipoAPIEnum(str, enum.Enum):
    """Tipos de APIs externas soportadas"""
    RENIEC = "reniec"          # DNI en Perú
    FACTURIZA = "facturiza"    # RUC en Perú
    SUNAT = "sunat"            # Contribuyentes
    CUSTOM = "custom"          # API personalizada

class AuthTypeEnum(str, enum.Enum):
    """Tipos de autenticación para APIs"""
    BEARER = "bearer"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    BASIC = "basic"

# ════════════════════════════════════════════════════════════════════
# TABLAS PARA CONFIGURACIÓN
# ════════════════════════════════════════════════════════════════════

class IntegracionAPI(Base):
    """
    Almacena credenciales y configuración de APIs externas.
    Los tokens se encriptan con Fernet antes de guardar.
    """
    __tablename__ = "integraciones_api"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False, index=True)
    descripcion = Column(String(500), nullable=True)
    tipo = Column(Enum(TipoAPIEnum), nullable=False)
    
    # Endpoint y autenticación
    endpoint_url = Column(String(500), nullable=False)
    auth_type = Column(Enum(AuthTypeEnum), nullable=False)
    auth_token = Column(String(500), nullable=False)  # ENCRIPTADO
    
    # Configuración
    activa = Column(Boolean, default=True)
    timeout_segundos = Column(Integer, default=30)
    max_reintentos = Column(Integer, default=3)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    campos = relationship("ConfiguracionCampo", back_populates="api_integracion")
    consultas = relationship("ConsultaExterna", back_populates="api_integracion")
    
    def __repr__(self):
        return f"<IntegracionAPI(nombre={self.nombre}, tipo={self.tipo})>"

class ConfiguracionCampo(Base):
    """
    Define campos dinámicos que aparecerán en el formulario de registro.
    Permite asociar campos con APIs para auto-llenado.
    """
    __tablename__ = "configuracion_campos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_campo = Column(String(100), unique=True, nullable=False, index=True)
    etiqueta = Column(String(255), nullable=False)
    descripcion = Column(String(500), nullable=True)
    
    # Tipo de dato
    tipo_dato = Column(Enum(TipoDatoEnum), nullable=False)
    
    # Validación
    es_obligatorio = Column(Boolean, default=False)
    expresion_regex = Column(String(500), nullable=True)  # Para validación string
    valores_enum = Column(JSON, nullable=True)  # List[str] para tipo enum
    
    # Posición en el formulario
    posicion = Column(Integer, default=0)
    
    # API Integration para auto-llenado
    api_integracion_id = Column(Integer, ForeignKey("integraciones_api.id"), nullable=True)
    campo_mapa_api = Column(String(100), nullable=True)  # Qué campo consultar en la API
    
    # Visibilidad
    mostrar_en_registro = Column(Boolean, default=True)
    mostrar_en_perfil = Column(Boolean, default=True)
    mostrar_en_reportes = Column(Boolean, default=True)
    
    # Auditoría
    creado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    api_integracion = relationship("IntegracionAPI", back_populates="campos")
    campos_usuario = relationship("CampoUsuario", back_populates="configuracion")
    
    def __repr__(self):
        return f"<ConfiguracionCampo(nombre_campo={self.nombre_campo}, tipo={self.tipo_dato})>"

class CampoUsuario(Base):
    """
    Almacena los valores de campos dinámicos para cada usuario.
    Permite que usuarios tengan diferentes campos según la configuración.
    """
    __tablename__ = "campos_usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    configuracion_campo_id = Column(Integer, ForeignKey("configuracion_campos.id"), nullable=False)
    
    valor = Column(String(1000), nullable=True)
    fue_validado_externamente = Column(Boolean, default=False)
    consulta_externa_id = Column(Integer, ForeignKey("consultas_externas.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    usuario = relationship("Usuario", foreign_keys=[usuario_id])
    configuracion = relationship("ConfiguracionCampo", back_populates="campos_usuario")
    consulta_externa = relationship("ConsultaExterna")
    
    def __repr__(self):
        return f"<CampoUsuario(usuario_id={self.usuario_id}, valor={self.valor[:50] if self.valor else None})>"

class ConsultaExterna(Base):
    """
    Auditoría completa de todas las consultas a APIs externas.
    Permite rastrear qué datos se consultaron, cuándo y por quién.
    """
    __tablename__ = "consultas_externas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True, index=True)
    api_integracion_id = Column(Integer, ForeignKey("integraciones_api.id"), nullable=False, index=True)
    
    # Detalles de consulta
    tipo_consulta = Column(String(50), nullable=False)  # "DNI", "RUC", etc.
    parametro_busqueda = Column(String(255), nullable=False)
    
    # Respuesta
    respuesta_json = Column(JSON, nullable=True)
    campos_mapeados = Column(JSON, nullable=True)  # Qué campos se auto-llenaron
    
    # Estado
    estado = Column(String(50), default="pendiente")  # pendiente, exitosa, fallida
    mensaje_error = Column(String(500), nullable=True)
    
    # Auditoría
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    ip_origen = Column(String(45), nullable=True)
    
    # Relaciones
    usuario = relationship("Usuario")
    api_integracion = relationship("IntegracionAPI", back_populates="consultas")
    
    def __repr__(self):
        return f"<ConsultaExterna(tipo={self.tipo_consulta}, estado={self.estado}, timestamp={self.timestamp})>"
```

---

## ════════════════════════════════════════════════════════════════
## 📝 CAMPOS ABIERTOS – COMPLETAR CON TUS NECESIDADES
## ════════════════════════════════════════════════════════════════

Completa la tabla abajo con los campos personalizados que necesitas en el modelo `Usuario`.

El sistema permite agregar estos campos de dos formas:

**Opción 1 (Tradicional):** Descomentar en Usuario o agregar columnas directamente
**Opción 2 (Recomendado):** Usar configuración dinámica (módulo 6 arriba) - sin necesidad de migración

| Campo | Tipo | Descripción | ¿Obligatorio? | Notas |
|-------|------|-------------|----------------|-------|
| **numero_casa** | String(50) | Número de vivienda dentro de la comunidad | Sí | Se puede heredar de familia |
| **fecha_ingreso** | DateTime | Fecha en que se unió a la comunidad | No | Para reportes de antigüedad |
| **documento_identidad** | String(50) | Cédula/DNI/Pasaporte | Sí | Alternativa a email para validación |
| **profesion** | String(255) | Ocupación del usuario | No | Para estadísticas |
| **foto_perfil_url** | String(500) | Avatar del usuario | No | URL a cloud storage |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |

### Instrucciones para agregar campos:
1. Rellena la tabla arriba con tus campos
2. Copia el nombre de cada campo
3. En `backend/app/models/usuario.py`, descomenta o agrega debajo de `# ⚠️ CAMPOS ABIERTOS`:
   ```python
   numero_casa = Column(String(50), nullable=False)
   fecha_ingreso = Column(DateTime, nullable=True)
   # ... etc.
   ```
4. En `backend/app/schemas/usuario_schema.py`, agrega los campos a `UsuarioCreate` y `UsuarioResponse`
5. Ejecuta: `alembic revision --autogenerate -m "Add custom fields"`
6. Ejecuta: `alembic upgrade head`

