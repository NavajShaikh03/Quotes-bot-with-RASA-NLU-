@echo off
setlocal enabledelayedexpansion
echo ============================================
echo Quotes Bot with RASA NLU
echo ============================================
echo.

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found.
    echo Please create one:
    echo   python -m venv venv
    echo   venv\Scripts\activate.bat
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo Ports cleared successfully.
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo ============================================
echo Step 1: Training RASA model...
echo ============================================
rasa train

echo.
echo ============================================
echo Step 2: Starting RASA Action Server...
echo ============================================
start "RASA Action Server" cmd /k "rasa run actions --port 5055"

echo Waiting for action server to initialize (3 seconds)...
timeout /t 3 /nobreak > nul

echo.
echo ============================================
echo Step 3: Starting RASA API server...
echo ============================================
start "RASA API Server" cmd /k "rasa run --enable-api --cors * --port 5005"

echo Waiting for Rasa server to initialize (5 seconds)...
timeout /t 5 /nobreak > nul

echo.
echo ============================================
echo Step 4: Starting Web UI server...
echo ============================================
start "Web UI Server" cmd /k "python web_integration\chat_ui.py"

echo Waiting for web server to initialize (3 seconds)...
timeout /t 3 /nobreak > nul

echo.
echo ============================================
echo Step 5: Opening chatbot UI in browser...
echo ============================================
start "" "http://localhost:5500"

echo.
echo ============================================
echo Bot is ready! All servers started.
echo ============================================
echo Training: Complete
echo Action Server: http://localhost:5055
echo API Server: http://localhost:5005
echo Web UI: http://localhost:5500
echo.
