@echo off
REM ============================================================
REM SCRIPT CHẠY BACKEND API SERVER
REM ============================================================
REM Hướng dẫn: Double-click file này để chạy PHP API server
REM ============================================================

echo.
echo ============================================================
echo    CHAY BACKEND API SERVER
echo ============================================================
echo.

REM Kiểm tra PHP
php --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PHP chua duoc cai dat!
    echo Vui long cai dat XAMPP hoac PHP standalone
    echo Hoac mo XAMPP Control Panel va start Apache
    pause
    exit /b 1
)

REM Di chuyển đến thư mục backend_api
cd /d "%~dp0backend_api"

echo [INFO] Dang khoi dong PHP server...
echo.
echo [INFO] API server se chay tren: http://localhost:8080
echo [INFO] Endpoint: http://localhost:8080/api/save_result.php
echo [INFO] Nhan Ctrl+C de dung server
echo.
echo ============================================================
echo.

REM Chạy PHP built-in server
php -S localhost:8080

pause

