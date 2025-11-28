@echo off
chcp 65001 >nul
echo ========================================
echo   TỰ ĐỘNG HÓA SETUP DỰ ÁN
echo ========================================
echo.
echo Script này sẽ chạy tất cả các bước setup tự động
echo.
pause

cd /d %~dp0

python scripts/00_setup_all.py

pause

