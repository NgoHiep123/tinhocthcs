@echo off
chcp 65001 >nul
echo ========================================
echo   XÓA FILE TRÊN GITHUB
echo ========================================
echo.

cd /d D:\A_De_tai_Tot_nghiep

echo [1] Kiểm tra trạng thái Git...
git status --short

echo.
echo ========================================
echo   CHỌN HÀNH ĐỘNG
echo ========================================
echo 1. Xóa các file đã bị xóa (deleted) và commit
echo 2. Xóa tất cả file HTML cũ (K6, K7, K8, K9)
echo 3. Xem danh sách file sẽ bị xóa
echo 4. Thoát
echo.

set /p choice="Chọn (1-4): "

if "%choice%"=="1" goto delete_deleted
if "%choice%"=="2" goto delete_html
if "%choice%"=="3" goto view_deleted
if "%choice%"=="4" goto end

:delete_deleted
echo.
echo [XÓA CÁC FILE ĐÃ BỊ XÓA]
echo Đang xóa các file đã bị xóa...
git add -u
echo.
echo Các file sẽ được commit:
git status --short
echo.
set /p confirm="Bạn có chắc muốn commit và push? (y/n): "
if /i "%confirm%"=="y" (
    set /p message="Nhập commit message (hoặc Enter để dùng mặc định): "
    if "!message!"=="" set message=Xóa các file đã bị xóa
    git commit -m "!message!"
    echo.
    echo Đang push lên GitHub...
    git push origin master
    echo.
    echo ✅ Hoàn thành!
) else (
    echo Đã hủy.
)
goto end

:delete_html
echo.
echo [XÓA TẤT CẢ FILE HTML CŨ]
echo Đang xóa các file HTML cũ...
git rm K6_*.html 2>nul
git rm K7_*.html 2>nul
git rm K8_*.html 2>nul
git rm K9_*.html 2>nul
echo.
set /p confirm="Bạn có chắc muốn commit và push? (y/n): "
if /i "%confirm%"=="y" (
    set /p message="Nhập commit message (hoặc Enter để dùng mặc định): "
    if "!message!"=="" set message=Xóa các file HTML cũ (đã chuyển sang thư mục Web/)
    git commit -m "!message!"
    echo.
    echo Đang push lên GitHub...
    git push origin master
    echo.
    echo ✅ Hoàn thành!
) else (
    echo Đã hủy.
    git reset HEAD 2>nul
)
goto end

:view_deleted
echo.
echo [XEM DANH SÁCH FILE SẼ BỊ XÓA]
echo.
echo Các file đã bị xóa (deleted):
git status --short | findstr "^ D"
echo.
echo Các file chưa được track (untracked):
git status --short | findstr "^\?\?"
goto end

:end
echo.
pause

