@echo off
chcp 65001 >nul
echo ========================================
echo   XOA VA UPLOAD LAI GITHUB REPOSITORY
echo   Repository: NgoHiep123/tinhocthcs.git
echo ========================================
echo.

REM Kiểm tra đang ở đúng thư mục
cd /d D:\A_DeAnTN

echo ⚠️  CANH BAO: Script nay se xoa TAT CA file tren GitHub!
echo.
echo Repository: tinhocthcs
echo Remote: origin
echo Branch: main (hoac master)
echo.

REM Kiểm tra Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Khong tim thay Git!
    echo 💡 Hay cai dat Git truoc
    pause
    exit /b 1
)

REM Kiểm tra remote
echo [1] Kiem tra remote repository...
git remote -v
echo.

REM Kiểm tra branch hiện tại
echo [2] Kiem tra branch hien tai...
git branch
echo.
set /p current_branch="Nhap ten branch (mac dinh: main): "
if "%current_branch%"=="" set current_branch=main

echo.
echo ========================================
echo   XAC NHAN
echo ========================================
echo ⚠️  Ban co chac chan muon:
echo    1. Xoa TAT CA file tren GitHub repository tinhocthcs
echo    2. Upload lai TAT CA file hien tai len GitHub
echo.
set /p confirm="Ban co CHAC CHAN muon tiep tuc? (go 'YES' de xac nhan): "

if /i not "%confirm%"=="YES" (
    echo.
    echo ❌ Da huy!
    pause
    exit /b 0
)

echo.
echo ========================================
echo   BUOC 1: XOA TAT CA FILE TREN GITHUB
echo ========================================
echo.

REM Xem file hiện có
echo Danh sach file hien tai:
git ls-files | head -n 20
echo ...
echo.

set /p confirm_step1="Tiep tuc xoa TAT CA file tren GitHub? (y/n): "
if /i not "%confirm_step1%"=="y" (
    echo ❌ Da huy!
    pause
    exit /b 0
)

echo.
echo Dang xoa tat ca file...
REM Xóa tất cả file (trừ .git và .gitignore)
git rm -r --cached . 2>nul
git add .gitignore 2>nul

REM Kiểm tra xem có file nào để xóa không
git status --short | findstr "^D" >nul
if errorlevel 1 (
    echo ℹ️  Khong co file nao de xoa (co the da xoa het roi)
) else (
    echo Cac file se bi xoa:
    git status --short | findstr "^D" | head -n 10
    echo ...
    echo.
    
    echo Dang commit xoa file...
    git commit -m "Xoa tat ca file cu - Chuan bi upload lai"
    
    if errorlevel 1 (
        echo ⚠️  Khong co gi de commit (co the da xoa het roi)
    ) else (
        echo Dang push len GitHub...
        git push origin %current_branch%
        
        if errorlevel 1 (
            echo ❌ Loi khi push! Kiem tra lai ket noi.
            pause
            exit /b 1
        )
        
        echo ✅ Da xoa file tren GitHub!
    )
)

echo.
echo ========================================
echo   BUOC 2: UPLOAD LAI TAT CA FILE
echo ========================================
echo.

REM Kiểm tra file hiện tại
echo Danh sach file hien tai trong thu muc:
dir /b | findstr /v ".git" | head -n 20
echo ...

set /p confirm_step2="Tiep tuc upload TAT CA file hien tai len GitHub? (y/n): "
if /i not "%confirm_step2%"=="y" (
    echo ❌ Da huy!
    pause
    exit /b 0
)

echo.
echo Dang them tat ca file...
git add .

REM Kiểm tra xem có file nào để commit không
git status --short >nul
if errorlevel 1 (
    echo ⚠️  Khong co file nao de them
) else (
    echo Cac file se duoc them/upload:
    git status --short | head -n 20
    echo ...
    echo.
    
    set /p commit_message="Nhap commit message (hoac Enter de dung mac dinh): "
    if "!commit_message!"=="" set commit_message=Upload lai tat ca file len GitHub
    
    echo Dang commit...
    git commit -m "%commit_message%"
    
    if errorlevel 1 (
        echo ❌ Loi khi commit!
        pause
        exit /b 1
    )
    
    echo Dang push len GitHub...
    git push origin %current_branch%
    
    if errorlevel 1 (
        echo ❌ Loi khi push!
        echo 💡 Thu chay: git push -u origin %current_branch%
        pause
        exit /b 1
    )
    
    echo.
    echo ✅ Hoan thanh!
    echo.
    echo 📊 Thong ke:
    git ls-files | find /c /v ""
    echo file da duoc upload len GitHub
)

echo.
echo ========================================
echo   KET THUC
echo ========================================
echo.
echo ✅ Da hoan thanh xoa va upload lai repository!
echo.
echo Kiem tra tai: https://github.com/NgoHiep123/tinhocthcs
echo.
pause

