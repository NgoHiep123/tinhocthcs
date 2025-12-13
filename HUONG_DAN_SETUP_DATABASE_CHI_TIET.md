# 📚 HƯỚNG DẪN SETUP DATABASE CHI TIẾT

> Hướng dẫn từng bước để setup MySQL database cho hệ thống

---

## 🎯 CÁC CÁCH SETUP

Có 3 cách để setup database:
1. **Cách 1: Dùng script tự động** (Windows) - Dễ nhất
2. **Cách 2: Dùng script tự động** (Linux/Mac)
3. **Cách 3: Setup thủ công** - Nếu MySQL không có trong PATH

---

## 📋 CÁCH 1: SETUP TỰ ĐỘNG (WINDOWS)

### Bước 1: Chạy script

```bash
cd backend_api
setup_database.bat
```

Script sẽ:
- ✅ Tự động tìm MySQL
- ✅ Yêu cầu nhập username và password
- ✅ Tạo database và các bảng
- ✅ Kiểm tra kết quả

### Bước 2: Kiểm tra

Sau khi chạy script, mở file test:
```
backend_api/test_connection.php
```

Trong trình duyệt để xem kết quả.

---

## 📋 CÁCH 2: SETUP TỰ ĐỘNG (LINUX/MAC)

### Bước 1: Cho phép chạy script

```bash
cd backend_api
chmod +x setup_database.sh
```

### Bước 2: Chạy script

```bash
./setup_database.sh
```

### Bước 3: Kiểm tra

```bash
# Test kết nối
php test_connection.php

# Hoặc mở trong browser
# http://localhost/backend_api/test_connection.php
```

---

## 📋 CÁCH 3: SETUP THỦ CÔNG

### Bước 1: Mở MySQL Console

**Windows:**
```bash
# Nếu MySQL trong PATH
mysql -u root -p

# Hoặc tìm MySQL trong:
# C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe
```

**Linux/Mac:**
```bash
mysql -u root -p
```

### Bước 2: Chạy SQL Script

**Cách 1: Import từ file**
```bash
mysql -u root -p < backend_api/create_database.sql
```

**Cách 2: Copy và paste**
1. Mở file `backend_api/create_database.sql`
2. Copy toàn bộ nội dung
3. Paste vào MySQL console
4. Nhấn Enter

**Cách 3: Dùng phpMyAdmin**
1. Đăng nhập phpMyAdmin
2. Chọn tab "SQL"
3. Copy nội dung `create_database.sql`
4. Paste vào và nhấn "Go"

### Bước 3: Kiểm tra

Trong MySQL console:
```sql
-- Kiểm tra database
SHOW DATABASES;
USE tinhoc321_quiz;

-- Kiểm tra bảng
SHOW TABLES;

-- Kiểm tra cấu trúc bảng quiz_results
DESCRIBE quiz_results;

-- Kiểm tra view
SHOW FULL TABLES WHERE Table_type = 'VIEW';
```

**Kết quả mong đợi:**
```
Database: tinhoc321_quiz
Tables:
  - quiz_results
  - students
Views:
  - v_quiz_stats
  - v_student_stats
  - v_class_stats
```

---

## 📋 BƯỚC 4: CẤU HÌNH API

### Sửa file `backend_api/api/config.php`

```php
// Cấu hình Database
define('DB_HOST', 'localhost');  // Hoặc IP MySQL server
define('DB_NAME', 'tinhoc321_quiz');
define('DB_USER', 'root');  // Hoặc user riêng nếu đã tạo
define('DB_PASS', 'your_password');  // ⚠️ Thay bằng password thực tế
```

**Lưu ý:**
- Nếu dùng user `root`: Nhập password MySQL root
- Nếu đã tạo user riêng: Nhập thông tin user đó

### Tạo User riêng (Tùy chọn - Khuyến nghị)

**Trong MySQL console:**
```sql
-- Tạo user mới
CREATE USER 'tinhoc321_user'@'localhost' IDENTIFIED BY 'your_strong_password';

-- Cấp quyền
GRANT ALL PRIVILEGES ON tinhoc321_quiz.* TO 'tinhoc321_user'@'localhost';

-- Áp dụng thay đổi
FLUSH PRIVILEGES;

-- Test user mới
mysql -u tinhoc321_user -p tinhoc321_quiz
```

Sau đó cập nhật `config.php`:
```php
define('DB_USER', 'tinhoc321_user');
define('DB_PASS', 'your_strong_password');
```

---

## 📋 BƯỚC 5: TEST KẾT NỐI

### Test 1: Mở file test trong browser

```
http://localhost/backend_api/test_connection.php
```

Hoặc nếu chưa có web server:
```bash
# Dùng PHP built-in server
cd backend_api
php -S localhost:8000

# Mở browser: http://localhost:8000/test_connection.php
```

### Test 2: Test bằng command line

```bash
mysql -u root -p tinhoc321_quiz -e "SELECT COUNT(*) FROM quiz_results;"
```

### Test 3: Test API endpoint

```bash
curl -X POST http://localhost/api/save_result.php \
  -H "Content-Type: application/json" \
  -d '{
    "student_name": "Test Student",
    "class_name": "7/1",
    "quiz_id": "TEST_QUIZ",
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
    "student": "Test Student",
    "class": "7/1",
    "quiz": "TEST_QUIZ",
    "score": "15/20",
    "percentage": "75%",
    "duration": "300s"
  }
}
```

### Test 4: Kiểm tra database

```sql
USE tinhoc321_quiz;
SELECT * FROM quiz_results ORDER BY created_at DESC LIMIT 5;
```

---

## 🔧 XỬ LÝ LỖI

### Lỗi 1: "Access denied for user 'root'@'localhost'"

**Nguyên nhân:** Password sai hoặc user không có quyền

**Giải pháp:**
1. Kiểm tra lại password trong `config.php`
2. Test kết nối:
   ```bash
   mysql -u root -p
   ```
3. Nếu quên password, reset password MySQL:
   ```sql
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
   FLUSH PRIVILEGES;
   ```

### Lỗi 2: "Unknown database 'tinhoc321_quiz'"

**Nguyên nhân:** Database chưa được tạo

**Giải pháp:**
1. Chạy lại script tạo database:
   ```bash
   mysql -u root -p < backend_api/create_database.sql
   ```
2. Hoặc tạo thủ công:
   ```sql
   CREATE DATABASE tinhoc321_quiz CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

### Lỗi 3: "Table 'quiz_results' doesn't exist"

**Nguyên nhân:** Bảng chưa được tạo

**Giải pháp:**
1. Chạy lại script `create_database.sql`
2. Hoặc tạo bảng thủ công (copy từ file SQL)

### Lỗi 4: MySQL không có trong PATH

**Nguyên nhân:** MySQL chưa được thêm vào PATH

**Giải pháp Windows:**
1. Tìm MySQL: Thường ở `C:\Program Files\MySQL\MySQL Server 8.0\bin\`
2. Thêm vào PATH:
   - Mở System Properties → Environment Variables
   - Thêm đường dẫn MySQL vào PATH
   - Hoặc dùng full path: `"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"`

**Giải pháp Linux/Mac:**
```bash
# Tìm MySQL
which mysql
# Hoặc
find /usr -name mysql 2>/dev/null

# Thêm vào PATH (nếu cần)
export PATH=$PATH:/usr/local/mysql/bin
```

---

## ✅ CHECKLIST HOÀN THÀNH

Sau khi setup, kiểm tra:

- [ ] MySQL service đã chạy
- [ ] Database `tinhoc321_quiz` đã được tạo
- [ ] Bảng `quiz_results` đã được tạo
- [ ] Bảng `students` đã được tạo (nếu có)
- [ ] Views đã được tạo (v_quiz_stats, v_student_stats, v_class_stats)
- [ ] `config.php` đã được cấu hình đúng
- [ ] Test connection thành công
- [ ] Test API endpoint thành công

---

## 📞 HỖ TRỢ

**File hỗ trợ:**
- `backend_api/test_connection.php` - Test kết nối database
- `backend_api/test_api.php` - Test API endpoint
- `backend_api/setup_database.bat` - Script tự động (Windows)
- `backend_api/setup_database.sh` - Script tự động (Linux/Mac)

**Kiểm tra MySQL:**
```bash
# Kiểm tra MySQL service
# Windows:
services.msc  # Tìm MySQL service

# Linux:
sudo systemctl status mysql
# hoặc
sudo service mysql status

# Mac:
brew services list  # Nếu dùng Homebrew
```

---

## 🎯 BƯỚC TIẾP THEO

Sau khi setup database thành công:

1. **Cấu hình API:** Sửa `backend_api/api/config.php`
2. **Test API:** Mở `backend_api/test_api.php`
3. **Test từ frontend:** Làm một bài và kiểm tra kết quả
4. **Xem Dashboard:** Mở `backend_api/dashboard/index.php`

