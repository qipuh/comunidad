import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
from app.db.database import SessionLocal
from app.models.usuario import Usuario

load_dotenv()

db = SessionLocal()
try:
    user = db.query(Usuario).filter_by(numero_dni="12345678").first()
    if user:
        user.password_hash = "password123"
        db.commit()
        print(f"✓ Password updated for user {user.nombre_completo}")
    else:
        print("✗ User not found")
finally:
    db.close()
