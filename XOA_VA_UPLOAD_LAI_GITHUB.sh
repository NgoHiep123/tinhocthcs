#!/bin/bash
# Script xóa và upload lại GitHub repository
# Repository: NgoHiep123/tinhocthcs.git

echo "========================================"
echo "  XOA VA UPLOAD LAI GITHUB REPOSITORY"
echo "  Repository: NgoHiep123/tinhocthcs.git"
echo "========================================"
echo ""

# Chuyển đến thư mục dự án
cd "$(dirname "$0")" || exit 1

echo "⚠️  CẢNH BÁO: Script này sẽ xóa TẤT CẢ file trên GitHub!"
echo ""
echo "Repository: tinhocthcs"
echo "Remote: origin"
echo ""

# Kiểm tra Git
if ! command -v git &> /dev/null; then
    echo "❌ Không tìm thấy Git!"
    echo "💡 Hãy cài đặt Git trước"
    exit 1
fi

# Kiểm tra remote
echo "[1] Kiểm tra remote repository..."
git remote -v
echo ""

# Kiểm tra branch hiện tại
echo "[2] Kiểm tra branch hiện tại..."
git branch
echo ""
read -p "Nhập tên branch (mặc định: main): " current_branch
current_branch=${current_branch:-main}

echo ""
echo "========================================"
echo "  XÁC NHẬN"
echo "========================================"
echo "⚠️  Bạn có chắc chắn muốn:"
echo "   1. Xóa TẤT CẢ file trên GitHub repository tinhocthcs"
echo "   2. Upload lại TẤT CẢ file hiện tại lên GitHub"
echo ""
read -p "Bạn có CHẮC CHẮN muốn tiếp tục? (gõ 'YES' để xác nhận): " confirm

if [ "$confirm" != "YES" ]; then
    echo ""
    echo "❌ Đã hủy!"
    exit 0
fi

echo ""
echo "========================================"
echo "  BƯỚC 1: XÓA TẤT CẢ FILE TRÊN GITHUB"
echo "========================================"
echo ""

# Xem file hiện có
echo "Danh sách file hiện tại:"
git ls-files | head -n 20
echo "..."

read -p "Tiếp tục xóa TẤT CẢ file trên GitHub? (y/n): " confirm_step1
if [ "$confirm_step1" != "y" ] && [ "$confirm_step1" != "Y" ]; then
    echo "❌ Đã hủy!"
    exit 0
fi

echo ""
echo "Đang xóa tất cả file..."
# Xóa tất cả file (trừ .git)
git rm -r --cached . 2>/dev/null
git add .gitignore 2>/dev/null

# Kiểm tra xem có file nào để xóa không
if git status --short | grep -q "^D"; then
    echo "Các file sẽ bị xóa:"
    git status --short | grep "^D" | head -n 10
    echo "..."
    echo ""
    
    echo "Đang commit xóa file..."
    git commit -m "Xóa tất cả file cũ - Chuẩn bị upload lại"
    
    if [ $? -eq 0 ]; then
        echo "Đang push lên GitHub..."
        git push origin "$current_branch"
        
        if [ $? -eq 0 ]; then
            echo "✅ Đã xóa file trên GitHub!"
        else
            echo "❌ Lỗi khi push! Kiểm tra lại kết nối."
            exit 1
        fi
    fi
else
    echo "ℹ️  Không có file nào để xóa (có thể đã xóa hết rồi)"
fi

echo ""
echo "========================================"
echo "  BƯỚC 2: UPLOAD LẠI TẤT CẢ FILE"
echo "========================================"
echo ""

# Kiểm tra file hiện tại
echo "Danh sách file hiện tại trong thư mục:"
ls -la | grep -v "^d.*\.git" | head -n 20
echo "..."

read -p "Tiếp tục upload TẤT CẢ file hiện tại lên GitHub? (y/n): " confirm_step2
if [ "$confirm_step2" != "y" ] && [ "$confirm_step2" != "Y" ]; then
    echo "❌ Đã hủy!"
    exit 0
fi

echo ""
echo "Đang thêm tất cả file..."
git add .

# Kiểm tra xem có file nào để commit không
if git status --short | grep -q .; then
    echo "Các file sẽ được thêm/upload:"
    git status --short | head -n 20
    echo "..."
    echo ""
    
    read -p "Nhập commit message (hoặc Enter để dùng mặc định): " commit_message
    commit_message=${commit_message:-"Upload lại tất cả file lên GitHub"}
    
    echo "Đang commit..."
    git commit -m "$commit_message"
    
    if [ $? -eq 0 ]; then
        echo "Đang push lên GitHub..."
        git push origin "$current_branch"
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Hoàn thành!"
            echo ""
            echo "📊 Thống kê:"
            git ls-files | wc -l
            echo "file đã được upload lên GitHub"
        else
            echo "❌ Lỗi khi push!"
            echo "💡 Thử chạy: git push -u origin $current_branch"
            exit 1
        fi
    else
        echo "❌ Lỗi khi commit!"
        exit 1
    fi
else
    echo "⚠️  Không có file nào để thêm"
fi

echo ""
echo "========================================"
echo "  KẾT THÚC"
echo "========================================"
echo ""
echo "✅ Đã hoàn thành xóa và upload lại repository!"
echo ""
echo "Kiểm tra tại: https://github.com/NgoHiep123/tinhocthcs"
echo ""

