@echo off
setlocal EnableDelayedExpansion
TITLE SchoolTrack Launcher
echo =================================================
echo   Starting SchoolTrack Environment...
echo =================================================

:: Load deployment config - skip comments and blank lines
for /f "usebackq tokens=1,2 delims== eol=#" %%a in ("deployment.env") do (
    set "%%a=%%b"
)

:: Verify config loaded correctly
if "%TAILSCALE_HOST%"=="" (
    echo ERROR: deployment.env not found or TAILSCALE_HOST not set.
    echo Please create deployment.env from deployment.env.example
    echo.
    pause
    exit /b 1
)

echo.
echo [1/3] Starting Tailscale Funnel on port %FUNNEL_PORT%...
start "" cmd /k "tailscale funnel --https=%FUNNEL_PORT% http://localhost:%CADDY_PORT%"
timeout /t 3 /nobreak >nul
echo     Done.

echo [2/3] Starting SchoolTrack Backend on port %INTERNAL_PORT%...
start "" cmd /k "cd /d "%~dp0" && call venv\Scripts\activate && uvicorn app.main:app --reload --host 127.0.0.1 --port %INTERNAL_PORT%"
timeout /t 2 /nobreak >nul
echo     Done.

echo [3/3] Checking Caddy Server...
tasklist /FI "IMAGENAME eq caddy.exe" 2>NUL | find /I /N "caddy.exe">NUL
if errorlevel 1 (
    echo     Caddy not running, starting now...
    start "" cmd /k "cd /d "%CADDY_PATH%" && caddy run --config Caddyfile"
) else (
    echo     Caddy already running, skipping...
)

echo.
echo ============================================
echo  SchoolTrack is running!
echo  URL:  https://%TAILSCALE_HOST%:%FUNNEL_PORT%
echo  Docs: https://%TAILSCALE_HOST%:%FUNNEL_PORT%/docs
echo ============================================
echo.
echo Press any key to close this window...
pause >nul
