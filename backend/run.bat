@echo off
REM Backend startup script for Windows

echo.
echo ========================================
echo   COMUNIDAD API - Backend Server
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo [WARN] .env file not found. Creating from .env.example...
    copy .env.example .env
    echo [INFO] Created .env file. Update it with your configuration.
)

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    exit /b 1
)

echo [INFO] Installing/updating dependencies...
pip install -r requirements.txt -q

echo [INFO] Initializing database...
python -c "from app.db.database import init_db; init_db(); print('[OK] Database initialized')"

echo.
echo [INFO] Starting FastAPI server on http://0.0.0.0:8000
echo [INFO] Swagger UI: http://localhost:8000/docs
echo [INFO] ReDoc: http://localhost:8000/redoc
echo.

REM Start Uvicorn with auto-reload
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
