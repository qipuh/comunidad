"""
Seeder - Datos iniciales del sistema
Ejecutar: python seeder.py
"""
from app.db.database import SessionLocal, init_db, engine
from sqlalchemy import text

def migrate():
    """Agregar columnas faltantes si no existen"""
    with engine.connect() as conn:
        # Cambiar ENUM a VARCHAR para rol y estado
        try:
            conn.execute(text("ALTER TABLE usuarios MODIFY COLUMN rol VARCHAR(50) DEFAULT 'user'"))
            print("  rol: VARCHAR OK")
        except Exception:
            pass

        try:
            conn.execute(text("ALTER TABLE usuarios MODIFY COLUMN estado VARCHAR(50) DEFAULT 'activo'"))
            print("  estado: VARCHAR OK")
        except Exception:
            pass

        columnas = [
            ("numero_dni",                "VARCHAR(20) NULL"),
            ("telefono",                  "VARCHAR(20) NULL"),
            ("fecha_nacimiento",          "VARCHAR(10) NULL"),
            ("sexo",                      "VARCHAR(50) NULL"),
            ("estado_civil",              "VARCHAR(50) NULL"),
            ("direccion",                 "VARCHAR(500) NULL"),
            ("departamento",              "VARCHAR(100) NULL"),
            ("provincia",                 "VARCHAR(100) NULL"),
            ("distrito",                  "VARCHAR(100) NULL"),
            ("foto_frontal",              "VARCHAR(500) NULL"),
            ("foto_lateral_izq",          "VARCHAR(500) NULL"),
            ("foto_lateral_der",          "VARCHAR(500) NULL"),
            ("usar_reconocimiento_facial","BOOLEAN DEFAULT FALSE"),
        ]

        for col, definition in columnas:
            try:
                conn.execute(text(f"ALTER TABLE usuarios ADD COLUMN {col} {definition}"))
                print(f"  +{col}")
            except Exception:
                print(f"  {col}: ya existe")

        conn.commit()


def seed():
    """Insertar datos iniciales"""
    db = SessionLocal()
    try:
        from app.models.usuario import Usuario

        usuarios = [
            {
                "email":          "admin@comunidad.local",
                "username":       "admin",
                "password_hash":  "password",
                "numero_dni":     "00000000",
                "nombres":        "Administrador",
                "apellido_paterno":"Sistema",
                "telefono":       "000000000",
                "rol":            "admin",
                "estado":         "activo",
                "usar_reconocimiento_facial": False,
            },
        ]

        for datos in usuarios:
            existe = db.query(Usuario).filter(Usuario.username == datos["username"]).first()
            if existe:
                print(f"  Usuario '{datos['username']}' ya existe — omitido")
                continue

            usuario = Usuario(**datos)
            db.add(usuario)
            db.commit()
            print(f"  Usuario '{datos['username']}' creado (rol: {datos['rol']})")

    finally:
        db.close()


if __name__ == "__main__":
    print("=== Migrando estructura ===")
    migrate()

    print("\n=== Creando tablas nuevas ===")
    init_db()

    print("\n=== Insertando usuarios ===")
    seed()

    print("\n=== Seeder completado ===")
