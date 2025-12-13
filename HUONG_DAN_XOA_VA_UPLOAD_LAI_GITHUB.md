# 🔄 HƯỚNG DẪN XÓA VÀ UPLOAD LẠI GITHUB REPOSITORY

> Repository: **NgoHiep123/tinhocthcs.git**

---

## ⚠️ CẢNH BÁO QUAN TRỌNG

**Script này sẽ:**
1. Xóa **TẤT CẢ** file trên GitHub repository
2. Upload lại **TẤT CẢ** file hiện tại lên GitHub

**Lưu ý:**
- ⚠️ **Dữ liệu trên GitHub sẽ bị xóa vĩnh viễn** (trừ khi có backup)
- ✅ File trên máy local sẽ **KHÔNG bị xóa**
- ✅ Lịch sử commit sẽ được giữ lại
- ✅ Nên **backup** trước khi chạy

---

## 🚀 CÁCH 1: Dùng Script Batch (Windows) - Khuyến nghị

### Bước 1: Mở file batch

**Double-click** vào file: `XOA_VA_UPLOAD_LAI_GITHUB.bat`

**Hoặc chạy từ Command Prompt:**
```cmd
cd D:\A_DeAnTN
XOA_VA_UPLOAD_LAI_GITHUB.bat
```

### Bước 2: Xác nhận

Script sẽ hỏi:
- Xác nhận: Gõ `YES` để tiếp tục
- Nhập branch: `main` hoặc `master` (mặc định: `main`)

### Bước 3: Theo dõi quá trình

Script sẽ:
1. Xóa tất cả file trên GitHub
2. Upload lại tất cả file hiện tại

---

## 🚀 CÁCH 2: Dùng Script Shell (Linux/Mac)

### Bước 1: Cấp quyền thực thi

```bash
chmod +x XOA_VA_UPLOAD_LAI_GITHUB.sh
```

### Bước 2: Chạy script

```bash
cd /path/to/A_DeAnTN
./XOA_VA_UPLOAD_LAI_GITHUB.sh
```

---

## 🚀 CÁCH 3: Dùng Git Commands Thủ Công

### Bước 1: Xóa tất cả file trên GitHub

```bash
cd D:\A_DeAnTN

# Xem file hiện tại
git ls-files

# Xóa tất cả file (trừ .git)
git rm -r --cached .

# Commit xóa
git commit -m "Xóa tất cả file cũ - Chuẩn bị upload lại"

# Push lên GitHub
git push origin main
```

### Bước 2: Upload lại tất cả file

```bash
# Thêm tất cả file
git add .

# Commit
git commit -m "Upload lại tất cả file lên GitHub"

# Push
git push origin main
```

---

## 📋 KIỂM TRA TRƯỚC KHI CHẠY

### 1. Kiểm tra remote repository

```bash
git remote -v
```

**Kết quả mong đợi:**
```
origin  https://github.com/NgoHiep123/tinhocthcs.git (fetch)
origin  https://github.com/NgoHiep123/tinhocthcs.git (push)
```

### 2. Kiểm tra branch hiện tại

```bash
git branch
```

### 3. Kiểm tra trạng thái

```bash
git status
```

---

## 🔍 KIỂM TRA SAU KHI CHẠY

### 1. Kiểm tra trên GitHub

Truy cập: https://github.com/NgoHiep123/tinhocthcs

### 2. Kiểm tra số file đã upload

```bash
git ls-files | wc -l
```

### 3. Xem commit mới nhất

```bash
git log --oneline -5
```

---

## ⚙️ TÙY CHỈNH

### Thay đổi branch

Nếu repository dùng branch `master` thay vì `main`:

**Script sẽ hỏi branch**, hoặc sửa trong script:
```bash
current_branch=master  # Thay vì main
```

### Chỉ xóa một số file/thư mục cụ thể

Thay vì xóa tất cả, có thể xóa cụ thể:

```bash
# Xóa một thư mục
git rm -r "thu_muc_can_xoa"

# Xóa nhiều file
git rm file1.html file2.html

# Commit và push
git commit -m "Xóa file cụ thể"
git push origin main
```

---

## 🐛 XỬ LÝ LỖI

### Lỗi: "fatal: not a git repository"

**Nguyên nhân:** Không phải trong thư mục Git

**Giải pháp:**
```bash
cd D:\A_DeAnTN
```

### Lỗi: "remote: Permission denied"

**Nguyên nhân:** Không có quyền push

**Giải pháp:**
1. Kiểm tra đăng nhập GitHub
2. Cấu hình credentials:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

### Lỗi: "error: failed to push some refs"

**Nguyên nhân:** Conflict hoặc branch không tồn tại

**Giải pháp:**
```bash
# Tạo branch mới nếu chưa có
git push -u origin main

# Hoặc force push (cẩn thận!)
git push -f origin main
```

---

## 📝 GHI CHÚ

- **File `.gitignore`** sẽ được giữ lại và không bị xóa
- **Lịch sử commit** sẽ được giữ lại
- **Branches khác** sẽ không bị ảnh hưởng
- Chỉ branch hiện tại (`main`/`master`) bị ảnh hưởng

---

## ✅ CHECKLIST

- [ ] Đã backup dữ liệu quan trọng
- [ ] Đã kiểm tra remote repository đúng
- [ ] Đã kiểm tra branch hiện tại
- [ ] Đã xác nhận muốn xóa và upload lại
- [ ] Đã chạy script thành công
- [ ] Đã kiểm tra trên GitHub sau khi upload

---

**Cập nhật:** 2025-01-15

