# 🚀 HƯỚNG DẪN TRIỂN KHAI HOÀN CHỈNH

> Hướng dẫn từng bước để triển khai hệ thống lưu kết quả bằng PHP API

---

## ✅ TRẠNG THÁI HIỆN TẠI

**Đã hoàn thành:**
- ✅ **120 file HTML** đã được cập nhật sang PHP API endpoint
- ✅ Backend API đã có sẵn (`backend_api/api/`)
- ✅ Dashboard giáo viên đã có sẵn
- ✅ Database schema đã có sẵn
- ✅ CORS đã được cấu hình

**Cần làm:**
- ⚠️ Setup MySQL database
- ⚠️ Cấu hình backend API (domain, database credentials)
- ⚠️ Upload backend lên hosting
- ⚠️ Test hệ thống

---

## 📋 BƯỚC 1: CẬP NHẬT ENDPOINT (Nếu cần)

**Nếu domain của bạn khác `https://tinhoc321.com`, cần cập nhật:**

1. Mở file `scripts/update_endpoint_to_php_api.py`
2. Sửa dòng:
   ```python
   NEW_API_ENDPOINT = "https://your-domain.com/api/save_result.php"
   ```
3. Chạy lại script:
   ```bash
   python scripts/update_endpoint_to_php_api.py
   ```

**Hoặc cập nhật thủ công trong một file HTML để test:**
- Mở file HTML bất kỳ
- Tìm: `const ENDPOINT="https://tinhoc321.com/api/save_result.php";`
- Sửa thành domain của bạn

---

## 📋 BƯỚC 2: SETUP DATABASE MYSQL

### 2.1. Tạo Database

```bash
# Đăng nhập MySQL
mysql -u root -p

# Chạy script tạo database
source backend_api/create_database.sql

# Hoặc import trực tiếp
mysql -u root -p < backend_api/create_database.sql
```

### 2.2. Tạo User (Tùy chọn)

```sql
CREATE USER 'tinhoc321_user'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON tinhoc321_quiz.* TO 'tinhoc321_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2.3. Kiểm tra

```sql
SHOW DATABASES;
USE tinhoc321_quiz;
SHOW TABLES;
DESCRIBE quiz_results;
```

---

## 📋 BƯỚC 3: CẤU HÌNH BACKEND API

### 3.1. Cấu hình Database

Chỉnh sửa `backend_api/api/config.php`:

```php
// Cấu hình Database
define('DB_HOST', 'localhost');  // Hoặc IP MySQL server
define('DB_NAME', 'tinhoc321_quiz');
define('DB_USER', 'root');  // Hoặc 'tinhoc321_user'
define('DB_PASS', 'your_password');  // Mật khẩu MySQL
```

### 3.2. Cấu hình CORS

Trong `backend_api/api/config.php`, đảm bảo domain frontend của bạn có trong `ALLOWED_ORIGINS`:

```php
define('ALLOWED_ORIGINS', [
    'https://your-domain.com',
    'https://www.your-domain.com',
    'https://ngohiep123.github.io',  // GitHub Pages
    'http://localhost',  // Test local
]);
```

**Lưu ý:** Hiện tại đã có `'*'` để cho phép tất cả (để test). Nên thu hẹp lại sau.

### 3.3. Cấu hình Bảo mật

Sửa `API_SECRET` trong `config.php`:

```php
define('API_SECRET', 'your_random_secret_key_here');
```

Tạo secret key:
```bash
openssl rand -base64 32
```

---

## 📋 BƯỚC 4: UPLOAD LÊN HOSTING

### 4.1. Upload Backend API

1. Upload thư mục `backend_api/` lên hosting
2. Đảm bảo cấu trúc thư mục:
   ```
   your-domain.com/
   ├── api/
   │   ├── config.php
   │   ├── save_result.php
   │   └── get_results.php
   ├── dashboard/
   │   └── index.php
   └── create_database.sql
   ```

3. Đảm bảo PHP 7.4+ đã được cài đặt trên hosting

### 4.2. Quyền truy cập

- Thư mục `api/` phải có quyền 755
- File PHP phải có quyền 644
- File `.htaccess` (nếu có) phải có quyền 644

### 4.3. Cấu hình .htaccess (Nếu cần)

Tạo file `backend_api/api/.htaccess`:

```apache
# Security
Options -Indexes
<Files "config.php">
    Order allow,deny
    Deny from all
</Files>

# CORS (nếu server không hỗ trợ PHP header)
<IfModule mod_headers.c>
    Header set Access-Control-Allow-Origin "*"
    Header set Access-Control-Allow-Methods "GET, POST, OPTIONS"
    Header set Access-Control-Allow-Headers "Content-Type, Authorization"
</IfModule>
```

---

## 📋 BƯỚC 5: TEST HỆ THỐNG

### 5.1. Test API Endpoint

**Test lưu kết quả:**
```bash
curl -X POST https://your-domain.com/api/save_result.php \
  -H "Content-Type: application/json" \
  -d '{
    "student_name": "Nguyen Van A",
    "class_name": "7/1",
    "quiz_id": "K7_E1",
    "score": 15,
    "total": 20,
    "duration": 300
  }'
```

**Kết quả mong đợi:**
```json
{
  "success": true,
  "message": "Đã lưu kết quả thành công",
  "data": {
    "id": 1,
    "student": "Nguyen Van A",
    "class": "7/1",
    "quiz": "K7_E1",
    "score": "15/20",
    "percentage": "75%",
    "duration": "300s"
  }
}
```

**Test lấy kết quả:**
```bash
curl https://your-domain.com/api/get_results.php
```

### 5.2. Test từ Frontend

1. Mở `index.html` trong trình duyệt
2. Đăng nhập với `login.html`
3. Chọn một bài học bất kỳ (ví dụ: `K7_E1.html`)
4. Làm bài và submit
5. Kiểm tra console (F12) xem có lỗi không
6. Kiểm tra status: `✅ Đã lưu!` hoặc `⚠️ Không lưu được`

### 5.3. Kiểm tra Database

```sql
USE tinhoc321_quiz;
SELECT * FROM quiz_results ORDER BY created_at DESC LIMIT 10;
```

### 5.4. Kiểm tra Dashboard

Mở: `https://your-domain.com/backend_api/dashboard/index.php`

Xem thống kê và danh sách kết quả.

---

## 🔧 XỬ LÝ LỖI

### Lỗi: "Failed to fetch" hoặc CORS error

**Nguyên nhân:** CORS chưa được cấu hình đúng

**Giải pháp:**
1. Kiểm tra `ALLOWED_ORIGINS` trong `config.php`
2. Đảm bảo domain frontend có trong danh sách
3. Kiểm tra response headers trong Network tab (F12)

### Lỗi: "NetworkError" hoặc không có response

**Nguyên nhân:** 
- API endpoint không đúng
- Server chưa được cấu hình
- PHP error

**Giải pháp:**
1. Kiểm tra URL API có đúng không
2. Test API bằng curl hoặc Postman
3. Kiểm tra PHP error logs
4. Kiểm tra file `save_result.php` có tồn tại không

### Lỗi: "Database connection failed"

**Nguyên nhân:** Thông tin database sai

**Giải pháp:**
1. Kiểm tra `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS` trong `config.php`
2. Test kết nối MySQL:
   ```bash
   mysql -u your_user -p -h your_host your_database
   ```
3. Kiểm tra MySQL service có chạy không

### Lỗi: "Table 'quiz_results' doesn't exist"

**Nguyên nhân:** Database chưa được tạo đầy đủ

**Giải pháp:**
1. Chạy lại script tạo database:
   ```bash
   mysql -u root -p < backend_api/create_database.sql
   ```

---

## ✅ CHECKLIST HOÀN THIỆN

- [ ] Database MySQL đã được tạo
- [ ] User MySQL đã được tạo (nếu cần)
- [ ] `config.php` đã được cấu hình đúng
- [ ] Backend API đã được upload lên hosting
- [ ] Test API bằng curl thành công
- [ ] Test từ frontend thành công
- [ ] Dashboard hiển thị dữ liệu
- [ ] Database có dữ liệu mới sau khi làm bài

---

## 📞 HỖ TRỢ

**File hướng dẫn chi tiết:**
- `HUONG_DAN_SETUP_DATABASE.md` - Setup MySQL database
- `backend_api/README.md` - Hướng dẫn backend API
- `CHECKLIST_DEMO.md` - Checklist demo

**Test kết nối:**
```bash
# Test MySQL
mysql -u root -p -e "SELECT 1;"

# Test PHP API
curl https://your-domain.com/api/get_results.php

# Test từ browser
# Mở: https://your-domain.com/api/get_results.php
```

---

## 🎯 KẾT LUẬN

Sau khi hoàn thành các bước trên, hệ thống sẽ:
- ✅ Lưu kết quả vào MySQL database
- ✅ Hiển thị thống kê trên Dashboard
- ✅ Không còn phụ thuộc vào Google Sheets

**Thời gian ước tính:** 30-60 phút

