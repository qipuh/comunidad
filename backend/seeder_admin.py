"""
Seeder para crear usuario admin de prueba
"""
import sys
from datetime import datetime
from app.db.database import SessionLocal, engine
from app.models.usuario import Usuario
from app.models.configuracion import Base

def crear_usuario_admin():
    """Crea un usuario admin de prueba"""

    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Verificar si el usuario admin ya existe
        usuario_existente = db.query(Usuario).filter(
            Usuario.username == "admin@comunidad.test"
        ).first()

        if usuario_existente:
            print("✓ Usuario admin ya existe")
            return

        # Crear usuario admin
        usuario_admin = Usuario(
            username="admin@comunidad.test",
            numero_dni="12345678",
            nombres="Administrador",
            apellido_paterno="Sistema",
            email="admin@comunidad.test",
            fecha_nacimiento="1990-01-01",
            sexo="M",
            estado_civil="Soltero",
            direccion="Calle Principal 123",
            departamento="Arequipa",
            provincia="Arequipa",
            distrito="Arequipa",
            telefono="987654321",
            rol="admin",
            estado="activo",
            usar_reconocimiento_facial=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Establecer contraseña (se hashea automáticamente)
        usuario_admin.set_password("password")

        # Guardar en BD
        db.add(usuario_admin)
        db.commit()

        print("✅ Usuario admin creado exitosamente")
        print(f"   Email: admin@comunidad.test")
        print(f"   Contraseña: password")
        print(f"   Rol: admin")

    except Exception as e:
        print(f"❌ Error creando usuario admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    crear_usuario_admin()
