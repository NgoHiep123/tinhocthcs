# Script xóa file trên GitHub
# Sử dụng: .\xoa_file_tren_github.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  XÓA FILE TRÊN GITHUB" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Chuyển đến thư mục dự án
Set-Location "D:\A_De_tai_Tot_nghiep"

# Kiểm tra trạng thái Git
Write-Host "[1] Kiểm tra trạng thái Git..." -ForegroundColor Yellow
git status --short

Write-Host ""
Write-Host "Bạn muốn làm gì?" -ForegroundColor Green
Write-Host "1. Xóa các file đã bị xóa (deleted) và commit" -ForegroundColor White
Write-Host "2. Xóa file cụ thể" -ForegroundColor White
Write-Host "3. Xóa thư mục cụ thể" -ForegroundColor White
Write-Host "4. Xóa tất cả file HTML cũ (K6_*.html, K7_*.html)" -ForegroundColor White
Write-Host "5. Xem danh sách file sẽ bị xóa (không thực hiện)" -ForegroundColor White
Write-Host "6. Thoát" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Chọn (1-6)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "[XÓA CÁC FILE ĐÃ BỊ XÓA]" -ForegroundColor Yellow
        Write-Host "Đang xóa các file đã bị xóa (deleted)..." -ForegroundColor Yellow
        
        # Xóa tất cả file đã bị xóa
        git add -u
        
        Write-Host ""
        Write-Host "Các file sẽ được commit:" -ForegroundColor Cyan
        git status --short
        
        $confirm = Read-Host "`nBạn có chắc muốn commit và push? (y/n)"
        if ($confirm -eq "y" -or $confirm -eq "Y") {
            $message = Read-Host "Nhập commit message (hoặc Enter để dùng mặc định)"
            if ([string]::IsNullOrWhiteSpace($message)) {
                $message = "Xóa các file đã bị xóa"
            }
            
            git commit -m $message
            Write-Host ""
            Write-Host "Đang push lên GitHub..." -ForegroundColor Yellow
            git push origin master
            Write-Host ""
            Write-Host "✅ Hoàn thành!" -ForegroundColor Green
        } else {
            Write-Host "Đã hủy." -ForegroundColor Red
        }
    }
    
    "2" {
        Write-Host ""
        Write-Host "[XÓA FILE CỤ THỂ]" -ForegroundColor Yellow
        $fileName = Read-Host "Nhập tên file cần xóa (ví dụ: K6_A1.html)"
        
        if (Test-Path $fileName) {
            Write-Host "File tồn tại. Đang xóa..." -ForegroundColor Yellow
            git rm $fileName
            
            $confirm = Read-Host "`nBạn có chắc muốn commit và push? (y/n)"
            if ($confirm -eq "y" -or $confirm -eq "Y") {
                $message = Read-Host "Nhập commit message (hoặc Enter để dùng mặc định)"
                if ([string]::IsNullOrWhiteSpace($message)) {
                    $message = "Xóa file $fileName"
                }
                
                git commit -m $message
                git push origin master
                Write-Host "✅ Hoàn thành!" -ForegroundColor Green
            } else {
                Write-Host "Đã hủy." -ForegroundColor Red
            }
        } else {
            Write-Host "❌ File không tồn tại!" -ForegroundColor Red
        }
    }
    
    "3" {
        Write-Host ""
        Write-Host "[XÓA THƯ MỤC CỤ THỂ]" -ForegroundColor Yellow
        $folderName = Read-Host "Nhập tên thư mục cần xóa (ví dụ: thư_mục_cũ)"
        
        if (Test-Path $folderName) {
            Write-Host "Thư mục tồn tại. Đang xóa..." -ForegroundColor Yellow
            git rm -r $folderName
            
            $confirm = Read-Host "`nBạn có chắc muốn commit và push? (y/n)"
            if ($confirm -eq "y" -or $confirm -eq "Y") {
                $message = Read-Host "Nhập commit message (hoặc Enter để dùng mặc định)"
                if ([string]::IsNullOrWhiteSpace($message)) {
                    $message = "Xóa thư mục $folderName"
                }
                
                git commit -m $message
                git push origin master
                Write-Host "✅ Hoàn thành!" -ForegroundColor Green
            } else {
                Write-Host "Đã hủy." -ForegroundColor Red
            }
        } else {
            Write-Host "❌ Thư mục không tồn tại!" -ForegroundColor Red
        }
    }
    
    "4" {
        Write-Host ""
        Write-Host "[XÓA TẤT CẢ FILE HTML CŨ]" -ForegroundColor Yellow
        Write-Host "Đang tìm các file HTML cũ..." -ForegroundColor Yellow
        
        # Tìm các file HTML cũ
        $htmlFiles = Get-ChildItem -Filter "K*_*.html" -File | Where-Object { $_.Name -match "^K[6-9]_" }
        
        if ($htmlFiles.Count -gt 0) {
            Write-Host "Tìm thấy $($htmlFiles.Count) file HTML:" -ForegroundColor Cyan
            $htmlFiles | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor White }
            
            $confirm = Read-Host "`nBạn có chắc muốn xóa tất cả các file này? (y/n)"
            if ($confirm -eq "y" -or $confirm -eq "Y") {
                foreach ($file in $htmlFiles) {
                    git rm $file.Name
                }
                
                $message = Read-Host "Nhập commit message (hoặc Enter để dùng mặc định)"
                if ([string]::IsNullOrWhiteSpace($message)) {
                    $message = "Xóa các file HTML cũ (đã chuyển sang thư mục Web/)"
                }
                
                git commit -m $message
                git push origin master
                Write-Host "✅ Hoàn thành!" -ForegroundColor Green
            } else {
                Write-Host "Đã hủy." -ForegroundColor Red
            }
        } else {
            Write-Host "Không tìm thấy file HTML cũ." -ForegroundColor Yellow
        }
    }
    
    "5" {
        Write-Host ""
        Write-Host "[XEM DANH SÁCH FILE SẼ BỊ XÓA]" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Các file đã bị xóa (deleted):" -ForegroundColor Cyan
        git status --short | Where-Object { $_ -match "^ D" } | ForEach-Object {
            Write-Host "  $_" -ForegroundColor White
        }
        Write-Host ""
        Write-Host "Các file chưa được track (untracked):" -ForegroundColor Cyan
        git status --short | Where-Object { $_ -match "^\?\?" } | ForEach-Object {
            Write-Host "  $_" -ForegroundColor White
        }
    }
    
    "6" {
        Write-Host "Thoát." -ForegroundColor Yellow
        exit
    }
    
    default {
        Write-Host "Lựa chọn không hợp lệ!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Nhấn phím bất kỳ để thoát..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


