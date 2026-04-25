#!/bin/bash
# Frontend startup script for Unix/Linux/macOS

echo ""
echo "========================================"
echo "  COMUNIDAD - Frontend Server"
echo "========================================"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "[INFO] Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "[ERROR] npm install failed"
        exit 1
    fi
fi

echo "[INFO] Starting Vue dev server on http://localhost:5173"
echo "[INFO] Backend API: http://localhost:8000"
echo ""

# Start Vite dev server
npm run dev
