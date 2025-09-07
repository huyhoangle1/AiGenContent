@echo off
setlocal ENABLEDELAYEDEXPANSION

echo === AI Content Generator - Start ===
cd /d "%~dp0"

REM Ensure virtual environment exists
if not exist "venv\Scripts\python.exe" (
  echo [Setup] Creating virtual environment...
  py -3 -m venv venv || (
    echo [Error] Failed to create virtual environment.
    goto :end
  )
)

REM Activate venv
call "venv\Scripts\activate.bat" || (
  echo [Error] Failed to activate virtual environment.
  goto :end
)

REM Install dependencies if FastAPI is missing
python -c "import fastapi" 1>nul 2>nul
if errorlevel 1 (
  echo [Setup] Installing dependencies from requirements.txt ...
  python -m pip install --upgrade pip
  pip install -r requirements.txt || (
    echo [Error] Failed to install dependencies.
    goto :end
  )
)

REM Environment variables (override if needed)
set "API_HOST=127.0.0.1"
set "API_PORT=8000"
set "MODEL_PATH=.\models\fine_tuned_gpt2"

echo [Run] Starting API at http://%API_HOST%:%API_PORT% ...
python src\api.py

:end
echo.
echo === Process finished. Press any key to close. ===
pause >nul
endlocal


