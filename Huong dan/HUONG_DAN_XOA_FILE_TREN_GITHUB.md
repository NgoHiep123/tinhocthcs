# 📋 Hướng dẫn xóa tệp và thư mục trên GitHub

## 🎯 Tình trạng hiện tại
- Repository: `NgoHiep123/tinhoc321.git`
- Nhánh hiện tại: `master`
- Remote: `origin` → `https://github.com/NgoHiep123/tinhoc321.git`

---

## ⚡ CÁCH 0: Dùng file .bat (Không cần bật Execution Policy)

### Chạy file .bat:
```powershell
cd D:\A_De_tai_Tot_nghiep
.\BAT_XOA_FILE_GITHUB.bat
```

Hoặc double-click vào file `BAT_XOA_FILE_GITHUB.bat` trong Windows Explorer.

**Ưu điểm:**
- ✅ Không cần bật Execution Policy
- ✅ Dễ sử dụng, có menu lựa chọn
- ✅ An toàn, có xác nhận trước khi xóa

---

## ⚡ CÁCH 1: Xóa trực tiếp trên GitHub (Dễ nhất)

### Bước 1: Truy cập GitHub
1. Mở trình duyệt, vào: `https://github.com/NgoHiep123/tinhoc321`
2. Đăng nhập vào tài khoản GitHub của bạn

### Bước 2: Xóa file/thư mục
1. **Xóa file đơn lẻ:**
   - Click vào file cần xóa
   - Click nút **🗑️ Delete** (hoặc icon thùng rác)
   - Nhập commit message: `Xóa file [tên file]`
   - Click **Commit changes**

2. **Xóa nhiều file/thư mục:**
   - Vào thư mục chứa các file cần xóa
   - Click vào từng file → Delete
   - Hoặc dùng **GitHub Desktop** để xóa hàng loạt

---

## 💻 CÁCH 2: Copy lệnh từ file .txt (Nhanh nhất)

Mở file `LENH_XOA_FILE_GITHUB.txt` và copy các lệnh cần thiết, sau đó paste vào PowerShell.

**Ví dụ nhanh - Xóa các file đã bị xóa:**
```powershell
cd D:\A_De_tai_Tot_nghiep
git add -u
git commit -m "Xóa các file HTML cũ (đã chuyển sang thư mục Web/)"
git push origin master
```

---

## 💻 CÁCH 3: Xóa bằng Git Commands (Chuyên nghiệp)

### 📌 Lưu ý quan trọng:
- **Xóa trên GitHub = Xóa vĩnh viễn** (trừ khi có backup)
- Nên **backup** trước khi xóa
- Các lệnh dưới đây sẽ **xóa cả trên local và GitHub**

---

### 🔧 Các lệnh xóa cơ bản

#### 1. Xóa một file cụ thể:
```bash
cd D:\A_De_tai_Tot_nghiep
git rm "tên_file.html"
git commit -m "Xóa file tên_file.html"
git push origin master
```

#### 2. Xóa một thư mục (và tất cả file bên trong):
```bash
cd D:\A_De_tai_Tot_nghiep
git rm -r "tên_thư_mục"
git commit -m "Xóa thư mục tên_thư_mục"
git push origin master
```

#### 3. Xóa nhiều file cùng lúc (theo pattern):
```bash
# Xóa tất cả file .html trong thư mục gốc
git rm *.html

# Xóa tất cả file .html trong thư mục cụ thể
git rm "thư_mục/*.html"

# Commit và push
git commit -m "Xóa các file HTML"
git push origin master
```

#### 4. Xóa file nhưng giữ lại trên máy local:
```bash
# Chỉ xóa trên Git, giữ lại trên máy tính
git rm --cached "tên_file.html"
git commit -m "Xóa file khỏi Git (giữ lại local)"
git push origin master
```

---

### 📝 Ví dụ cụ thể

#### Ví dụ 1: Xóa các file HTML cũ (K6_A1.html, K6_A2.html, ...)
```bash
cd D:\A_De_tai_Tot_nghiep

# Xóa tất cả file K6_*.html trong thư mục gốc
git rm K6_*.html

# Xóa tất cả file K7_*.html
git rm K7_*.html

# Commit
git commit -m "Xóa các file HTML cũ (đã chuyển sang thư mục Web/)"

# Push lên GitHub
git push origin master
```

#### Ví dụ 2: Xóa một thư mục cụ thể
```bash
cd D:\A_De_tai_Tot_nghiep

# Xóa thư mục (ví dụ: thư mục cũ không cần thiết)
git rm -r "tên_thư_mục_cũ"

# Commit
git commit -m "Xóa thư mục tên_thư_mục_cũ"

# Push
git push origin master
```

#### Ví dụ 3: Xóa file nhưng giữ lại trên máy (thêm vào .gitignore)
```bash
cd D:\A_De_tai_Tot_nghiep

# Xóa khỏi Git nhưng giữ lại trên máy
git rm --cached "file_khong_can_upload.html"

# Thêm vào .gitignore để không upload lại
echo "file_khong_can_upload.html" >> .gitignore

# Commit
git add .gitignore
git commit -m "Xóa file khỏi Git và thêm vào .gitignore"
git push origin master
```

---

### 🗑️ Xóa tất cả file đã bị xóa (deleted) hiện tại

Nếu bạn đã xóa file trên máy local và muốn commit việc xóa này lên GitHub:

```bash
cd D:\A_De_tai_Tot_nghiep

# Xem các file đã bị xóa
git status

# Xóa tất cả file đã bị xóa (deleted)
git add -u

# Hoặc xóa cụ thể từng file
git rm K6_A1.html K6_A2.html K6_A3.html

# Commit
git commit -m "Xóa các file HTML cũ"

# Push
git push origin master
```

---

### ⚠️ Xóa file đã commit nhưng muốn giữ lại trên máy

Nếu file đã được commit lên GitHub nhưng bạn muốn:
- **Xóa trên GitHub** nhưng **giữ lại trên máy tính**

```bash
cd D:\A_De_tai_Tot_nghiep

# Xóa khỏi Git tracking nhưng giữ lại trên máy
git rm --cached "file.html"

# Thêm vào .gitignore (nếu muốn)
echo "file.html" >> .gitignore

# Commit
git add .gitignore
git commit -m "Xóa file.html khỏi repository (giữ lại local)"
git push origin master
```

---

### 🔄 Xóa và thêm lại file mới

Nếu bạn muốn thay thế file cũ bằng file mới:

```bash
cd D:\A_De_tai_Tot_nghiep

# Xóa file cũ
git rm "file_cu.html"

# Thêm file mới
git add "file_moi.html"

# Commit
git commit -m "Thay thế file_cu.html bằng file_moi.html"

# Push
git push origin master
```

---

### 📦 Xóa toàn bộ repository và tạo lại (CẨN THẬN!)

**⚠️ CẢNH BÁO: Lệnh này sẽ xóa TẤT CẢ trên GitHub!**

```bash
cd D:\A_De_tai_Tot_nghiep

# Xóa tất cả file (trừ .git)
git rm -r *

# Commit
git commit -m "Xóa tất cả file cũ"

# Push
git push origin master

# Sau đó thêm lại file mới
git add .
git commit -m "Thêm lại file mới"
git push origin master
```

---

## 🎯 Checklist trước khi xóa

- [ ] Đã backup các file quan trọng
- [ ] Đã kiểm tra file nào cần xóa
- [ ] Đã thêm file vào `.gitignore` (nếu cần)
- [ ] Đã test lệnh `git status` để xem thay đổi
- [ ] Đã commit và push thành công

---

## 🔧 Bật Execution Policy (Nếu muốn dùng file .ps1)

Nếu bạn muốn dùng file `xoa_file_tren_github.ps1`, cần bật Execution Policy:

### Cách 1: Bật tạm thời (Chỉ cho session hiện tại)
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\xoa_file_tren_github.ps1
```

### Cách 2: Bật cho user hiện tại (Khuyến nghị)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Sau đó chạy:
```powershell
.\xoa_file_tren_github.ps1
```

### Cách 3: Chạy trực tiếp không cần bật
```powershell
powershell -ExecutionPolicy Bypass -File .\xoa_file_tren_github.ps1
```

**Lưu ý:** Nếu không muốn bật Execution Policy, hãy dùng file `.bat` hoặc copy lệnh từ file `.txt`.

---

## 🆘 Khôi phục file đã xóa nhầm

Nếu xóa nhầm, có thể khôi phục:

```bash
# Xem lịch sử commit
git log --oneline

# Khôi phục file từ commit trước đó
git checkout <commit_hash> -- "tên_file.html"

# Commit lại
git add "tên_file.html"
git commit -m "Khôi phục file đã xóa nhầm"
git push origin master
```

---

## 📞 Lệnh kiểm tra nhanh

```bash
# Xem trạng thái
git status

# Xem các file đã bị xóa
git status | grep deleted

# Xem các nhánh
git branch -a

# Xem remote
git remote -v

# Xem lịch sử commit
git log --oneline -10
```

---

## 💡 Gợi ý

1. **Nên xóa từng nhóm nhỏ** thay vì xóa tất cả cùng lúc
2. **Commit message rõ ràng** để dễ theo dõi
3. **Kiểm tra `git status`** trước khi push
4. **Backup trước khi xóa** các file quan trọng

---

**Chúc bạn thành công! 🚀**


