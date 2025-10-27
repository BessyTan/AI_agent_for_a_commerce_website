@echo off
REM AI Commerce Agent - Windows Quick Start Script

echo 🚀 Starting AI Commerce Agent...

REM Check if virtual environment exists
if not exist "backend\venv" (
    echo 📦 Setting up backend...
    cd backend
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    cd ..
)

REM Check if node_modules exists
if not exist "frontend\node_modules" (
    echo 📦 Setting up frontend...
    cd frontend
    call npm install
    cd ..
)

REM Start backend
echo 🖥️  Starting backend server...
start "Backend Server" cmd /k "cd backend && call venv\Scripts\activate.bat && python main.py"

REM Wait a moment
timeout /t 3 /nobreak > nul

REM Start frontend
echo 🎨 Starting frontend...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo ✅ AI Commerce Agent is running!
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.

