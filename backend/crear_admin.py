#!/usr/bin/env python
"""Crea usuario admin de prueba"""
import os
import sys
from datetime import datetime

# Agregar el directorio al path
sys.path.insert(0, os.path.dirname(__file__))

from app.db.database import SessionLocal, engine
from app.models.usuario import Usuario, Base

def main():
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Verificar si ya existe
        admin = db.query(Usuario).filter(
            Usuario.username == "admin@comunidad.test"
        ).first()

        if admin:
            print("✓ Usuario admin ya existe")
            return

        # Crear admin
        usuario = Usuario(
            username="admin@comunidad.test",
            numero_dni="99999999",
            nombres="Administrador",
            apellido_paterno="Sistema",
            email="admin@comunidad.test",
            fecha_nacimiento="1990-01-01",
            sexo="M",
            estado_civil="Soltero",
            direccion="Calle Admin 123",
            departamento="Arequipa",
            provincia="Arequipa",
            distrito="Arequipa",
            telefono="987654321",
            rol="admin",
            estado="activo",
            usar_reconocimiento_facial=False
        )

        usuario.password_hash = "password"

        db.add(usuario)
        db.commit()

        print("OK - Usuario admin creado:")
        print("   Email: admin@comunidad.test")
        print("   Contraseña: password")

    except Exception as e:
        print("ERROR: " + str(e))
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
