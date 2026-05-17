"""Test usuarios route"""
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.usuario import Usuario

app = FastAPI()

@app.get("/test/usuarios")
async def listar_usuarios(limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    """Listar todos los usuarios - TEST"""
    try:
        usuarios = db.query(Usuario).order_by(Usuario.created_at.desc()).limit(limit).offset(0).all()
        total = db.query(Usuario).count()

        data = []
        for u in usuarios:
            item = {
                "id": u.id,
                "email": u.email,
                "username": u.username,
                "nombres": u.nombres,
                "apellido_paterno": u.apellido_paterno,
                "apellido_materno": u.apellido_materno,
                "nombre_completo": u.nombre_completo,
                "numero_dni": u.numero_dni,
            }
            data.append(item)

        return {
            "success": True,
            "count": len(usuarios),
            "total": total,
            "data": data
        }
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
