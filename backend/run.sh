#!/bin/bash
# Backend startup script for Unix/Linux/macOS

echo ""
echo "========================================"
echo "  COMUNIDAD API - Backend Server"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "[WARN] .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "[INFO] Created .env file. Update it with your configuration."
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed"
    exit 1
fi

echo "[INFO] Installing/updating dependencies..."
pip install -r requirements.txt -q

echo "[INFO] Initializing database..."
python3 -c "from app.db.database import init_db; init_db(); print('[OK] Database initialized')"

echo ""
echo "[INFO] Starting FastAPI server on http://0.0.0.0:8000"
echo "[INFO] Swagger UI: http://localhost:8000/docs"
echo "[INFO] ReDoc: http://localhost:8000/redoc"
echo ""

# Start Uvicorn with auto-reload
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
