@echo off
echo ========================================
echo Second Brain, First Person - Quick Start
echo ========================================
echo.

REM Check if GEMINI_API_KEY is set
if "%GEMINI_API_KEY%"=="" (
    echo ERROR: GEMINI_API_KEY environment variable is not set!
    echo.
    echo Please set it first:
    echo   set GEMINI_API_KEY=your_api_key_here
    echo.
    echo Get your API key from: https://aistudio.google.com/app/apikey
    echo.
    pause
    exit /b 1
)

echo Starting backend server...
cd backend
start cmd /k "python main.py"

timeout /t 3 /nobreak > nul

echo Starting frontend...
cd ..\frontend
start cmd /k "npm run dev"

echo.
echo ========================================
echo Both servers are starting!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo ========================================
echo.
echo Press any key to exit this window...
pause > nul
