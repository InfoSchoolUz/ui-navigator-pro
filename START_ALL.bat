@echo off
setlocal
title UI Navigator PRO - START ALL

set ROOT=C:\ui-navigator-pro
set CLOUD=%ROOT%\cloud_agent
set DESK=%ROOT%\desktop_client

echo ================================
echo UI Navigator PRO - START ALL
echo ================================
echo ROOT  = %ROOT%
echo CLOUD = %CLOUD%
echo DESK  = %DESK%
echo.

REM --- sanity checks ---
if not exist "%CLOUD%\app\main.py" (
  echo [ERROR] cloud_agent not found: %CLOUD%\app\main.py
  pause
  exit /b 1
)
if not exist "%DESK%\app\main.py" (
  echo [ERROR] desktop_client not found: %DESK%\app\main.py
  pause
  exit /b 1
)

if not exist "%CLOUD%\.venv\Scripts\python.exe" (
  echo [ERROR] Cloud venv missing: %CLOUD%\.venv\Scripts\python.exe
  echo Create it:
  echo   cd /d "%CLOUD%"
  echo   python -m venv .venv
  echo   .venv\Scripts\python -m pip install -r requirements.txt
  pause
  exit /b 1
)

if not exist "%DESK%\.venv\Scripts\python.exe" (
  echo [ERROR] Desktop venv missing: %DESK%\.venv\Scripts\python.exe
  echo Create it:
  echo   cd /d "%DESK%"
  echo   python -m venv .venv
  echo   .venv\Scripts\python -m pip install -r requirements.txt
  pause
  exit /b 1
)

REM --- set your key here ---
set GEMINI_API_KEY=AIzaSyCZUH0nOaIeGymzokx2uHU69fo0iD9a25s
set PLANNER_MODEL_ID=gemini-2.5-flash

echo Starting Cloud Agent...
start "Cloud Agent" cmd /k ^
"cd /d "%CLOUD%" ^&^& ^
set GEMINI_API_KEY=%GEMINI_API_KEY% ^&^& ^
set PLANNER_MODEL_ID=%PLANNER_MODEL_ID% ^&^& ^
.venv\Scripts\python -m uvicorn app.main:app --reload --port 8080"

echo Waiting 3 seconds...
timeout /t 3 > nul

echo Starting Desktop UI...
start "Desktop UI" cmd /k ^
"cd /d "%DESK%" ^&^& ^
set AGENT_URL=http://127.0.0.1:8080 ^&^& ^
.venv\Scripts\python -m app.main"

echo.
echo If UI still doesn't open, look at the "Desktop UI" window output.
echo ================================
pause