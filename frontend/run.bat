@echo off
REM Frontend startup script for Windows

echo.
echo ========================================
echo   COMUNIDAD - Frontend Server
echo ========================================
echo.

REM Check if node_modules exists
if not exist node_modules (
    echo [INFO] Installing dependencies...
    npm install
    if %errorlevel% neq 0 (
        echo [ERROR] npm install failed
        exit /b 1
    )
)

echo [INFO] Starting Vue dev server on http://localhost:5173
echo [INFO] Backend API: http://localhost:8000
echo.

REM Start Vite dev server
npm run dev

pause
