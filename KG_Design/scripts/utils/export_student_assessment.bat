@echo off
REM Script batch để export student_assessment từ MySQL
REM Usage: export_student_assessment.bat

echo ========================================
echo EXPORT STUDENT ASSESSMENT TU MYSQL
echo ========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Khong tim thay Python!
    echo 💡 Hay cai dat Python truoc
    pause
    exit /b 1
)

REM Kiểm tra thư viện
echo 📦 Dang kiem tra thu vien...
python -c "import mysql.connector" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Chua cai dat mysql-connector-python
    echo 💡 Dang cai dat...
    pip install mysql-connector-python
    if errorlevel 1 (
        echo ❌ Loi khi cai dat!
        pause
        exit /b 1
    )
)

echo ✅ Da co day du thu vien
echo.

REM Nhập thông tin MySQL
echo ════════════════════════════════════════
echo NHAP THONG TIN MYSQL
echo ════════════════════════════════════════
echo.

set /p MYSQL_HOST="Host (mac dinh: localhost): "
if "%MYSQL_HOST%"=="" set MYSQL_HOST=localhost

set /p MYSQL_USER="Username: "
if "%MYSQL_USER%"=="" (
    echo ❌ Username khong duoc de trong!
    pause
    exit /b 1
)

set /p MYSQL_PASSWORD="Password: "
if "%MYSQL_PASSWORD%"=="" (
    echo ❌ Password khong duoc de trong!
    pause
    exit /b 1
)

set /p MYSQL_DATABASE="Database (mac dinh: tinhoc321_quiz): "
if "%MYSQL_DATABASE%"=="" set MYSQL_DATABASE=tinhoc321_quiz

set /p MYSQL_YEAR="Nam (mac dinh: 2024): "
if "%MYSQL_YEAR%"=="" set MYSQL_YEAR=2024

echo.
echo ════════════════════════════════════════
echo DANG XU LY...
echo ════════════════════════════════════════
echo.

REM Chạy script Python
cd /d "%~dp0"
python export_student_assessment_from_mysql.py ^
    --host "%MYSQL_HOST%" ^
    --user "%MYSQL_USER%" ^
    --password "%MYSQL_PASSWORD%" ^
    --database "%MYSQL_DATABASE%" ^
    --year %MYSQL_YEAR% ^
    --output ../../csv/student_assessment.csv

if errorlevel 1 (
    echo.
    echo ❌ Co loi xay ra!
    pause
    exit /b 1
)

echo.
echo ✅ Hoan thanh!
echo 📁 File da duoc luu: KG_Design\csv\student_assessment.csv
echo.
pause

