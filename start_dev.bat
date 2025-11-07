@echo off

REM Smart Attendance System Backend - Development Startup Script (Windows)

echo 🚀 Starting Smart Attendance System Backend...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo ⚙️ Creating .env file...
    copy .env.example .env
    echo ✅ Please edit .env file with your database credentials
)

REM Run setup test
echo 🧪 Running setup validation...
python test_setup.py

echo.
echo 🎉 Setup complete! To start the server, run:
echo    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo 📚 API Documentation: http://localhost:8000/docs
echo 🔍 Health Check: http://localhost:8000/health

pause