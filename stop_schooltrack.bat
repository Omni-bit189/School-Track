@echo off
setlocal
TITLE SchoolTrack Stopper
echo =================================================
echo   Stopping SchoolTrack Environment... 🛑
echo =================================================

:: 1. Stop Tailscale Funnel for SchoolTrack (port 8443)
echo [1/3] 📡 Stopping Tailscale Funnel on port 8443...
tailscale funnel --https=8443 off
timeout /t 2 /nobreak >nul
echo     Done.

:: 2. Stop Uvicorn on port 8001 (SchoolTrack only)
echo [2/3] 🐍 Stopping SchoolTrack Backend on port 8001...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8001" ^| findstr "LISTENING"') do (
    echo     Found process on port 8001 with PID %%a
    taskkill /PID %%a /F /T
)

:: Fallback — kill by process name if port method missed it
wmic process where "commandline like '%%port 8001%%'" delete >nul 2>&1
wmic process where "commandline like '%%--port=8001%%'" delete >nul 2>&1
echo     Done.

:: 3. Stop Caddy only if MedAce is also not running
echo [3/3] 🚦 Checking if Caddy is still needed...
netstat -ano | findstr ":8000" | findstr "LISTENING" >nul
if "%ERRORLEVEL%"=="1" (
    echo     MedAce is not running, stopping Caddy...
    taskkill /IM caddy.exe /F
    echo     Caddy stopped.
) else (
    echo     MedAce is still running, leaving Caddy alive...
)

echo.
echo ✅ SchoolTrack fully stopped.
echo    - Uvicorn on port 8001: stopped
echo    - Tailscale Funnel: off
echo.
echo Press any key to close this window...
pause >nul
