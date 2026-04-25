# Backend Setup & Startup Guide

## 🚀 Quick Start

### Windows
```bash
cd backend
run.bat
```

### macOS/Linux
```bash
cd backend
bash run.sh
```

### Or manually:
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📋 Prerequisites

- Python 3.10+
- pip (Python package manager)

## 🔧 Setup Steps

### 1. Environment Configuration
```bash
cd backend
cp .env.example .env
```
Edit `.env` with your configuration:
- `DATABASE_URL`: PostgreSQL or SQLite (default: SQLite)
- `SECRET_KEY`: Change this in production
- `ENCRYPTION_KEY`: For API credential encryption
- External API tokens (RENIEC, Facturiza, SUNAT)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Initialization
The database is created automatically on first run. SQLAlchemy creates tables based on models in `app/models/`.

**Tables created:**
- `usuarios` - User profiles
- `configuracion_campos` - Dynamic field definitions
- `integraciones_api` - External API integrations
- `consultas_externas` - API query audit trail
- `campos_usuario` - User field values

### 4. Start Backend Server
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Expected output:
```
INFO:     Started server process [PID]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 📚 API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Health Check
```bash
curl http://localhost:8000/api/health
```

---

## 📁 Backend Structure

```
backend/
├── main.py                    # FastAPI app entry point
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables (local)
├── .env.example             # Environment template
├── app/
│   ├── __init__.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py       # SQLAlchemy config & session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── usuario.py        # User model
│   │   └── configuracion.py  # Dynamic config models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin_configuracion.py  # Admin endpoints
│   │   └── validaciones.py        # Validation endpoints
│   └── services/
│       ├── __init__.py
│       └── integracion_api_service.py  # External API service
└── migrations/              # Alembic migration scripts (optional)
```

---

## 🔌 Key Endpoints

### Admin Routes (require authentication)
```
GET    /api/admin/configuracion/campos           - List fields
POST   /api/admin/configuracion/campos           - Create field
PUT    /api/admin/configuracion/campos/{id}      - Update field
DELETE /api/admin/configuracion/campos/{id}      - Delete field

GET    /api/admin/integraciones-api              - List APIs
POST   /api/admin/integraciones-api              - Create API
PUT    /api/admin/integraciones-api/{id}         - Update API
DELETE /api/admin/integraciones-api/{id}         - Delete API
POST   /api/admin/integraciones-api/{id}/probar  - Test API
```

### Validation Routes (public)
```
POST   /api/validaciones/consultar-dni          - Validate DNI
POST   /api/validaciones/consultar-ruc          - Validate RUC
GET    /api/validaciones/probar-reniec          - Test RENIEC
GET    /api/validaciones/probar-facturiza       - Test Facturiza
GET    /api/validaciones/historial/{id}         - User query history
```

---

## 🧪 Testing

### Using cURL
```bash
# Health check
curl http://localhost:8000/api/health

# List fields (requires admin auth)
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8000/api/admin/configuracion/campos

# Query DNI
curl -X POST http://localhost:8000/api/validaciones/consultar-dni \
     -H "Content-Type: application/json" \
     -d '{"dni": "12345678"}'
```

### Using Python Script
```bash
python test_api.py
```
(See `test_api.py` for complete test suite)

### Using Docker
```bash
docker-compose -f docker-compose.testing.yml up
```

---

## 🔐 Security Notes

1. **NEVER commit secrets** - Keep `.env` out of version control
2. **Change SECRET_KEY** in production
3. **Use PostgreSQL** for production (SQLite for dev only)
4. **Enable HTTPS** in production
5. **Implement proper authentication** before deploying

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'app'"
- Ensure you're running commands from the `backend/` directory
- Check Python path: `export PYTHONPATH=/path/to/backend:$PYTHONPATH`

### "Port 8000 already in use"
- Change port: `--port 8001`
- Kill process: `lsof -ti:8000 | xargs kill -9` (Linux/macOS)

### Database errors
- Delete `.db` file and restart (dev only)
- Check DATABASE_URL in `.env`
- Verify SQLAlchemy is installed: `pip install sqlalchemy`

### CORS errors
- Check frontend URL matches CORS config in `main.py`
- Default allows: `http://localhost:5173` (Vue dev server)

---

## 📦 Dependencies

Key packages installed:
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **sqlalchemy** - ORM
- **pydantic** - Data validation
- **cryptography** - Encryption
- **requests** - HTTP client

See `requirements.txt` for complete list.

---

## 🚀 Next Steps

1. ✅ Backend running on `http://localhost:8000`
2. ⏭️ Frontend setup: `cd ../frontend && npm install && npm run dev`
3. 🧪 Test integration between backend & frontend
4. 🔐 Implement authentication (JWT)
5. 📊 Add database persistence & migrations

---

## 📞 Support

- **API Docs:** http://localhost:8000/docs
- **Full Spec:** See `ENDPOINTS_EJEMPLOS.md`
- **Models:** See `MODELOS_DATOS.md`
- **Architecture:** See `ARQUITECTURA.md`
