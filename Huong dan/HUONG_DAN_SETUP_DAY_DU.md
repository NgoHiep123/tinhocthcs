# 🚀 HƯỚNG DẪN SETUP DATABASE ĐẦY ĐỦ

> Hướng dẫn chi tiết từng bước để setup MySQL database

---

## ✅ CÁC FILE ĐÃ ĐƯỢC TẠO

### Scripts tự động:
- ✅ `backend_api/setup_database.bat` - Script tự động cho Windows
- ✅ `backend_api/setup_database.sh` - Script tự động cho Linux/Mac
- ✅ `backend_api/create_database.sql` - Script SQL tạo database

### File test:
- ✅ `backend_api/test_connection.php` - Test kết nối database
- ✅ `backend_api/test_api.php` - Test API endpoint

### Tài liệu:
- ✅ `HUONG_DAN_SETUP_DATABASE.md` - Hướng dẫn cơ bản
- ✅ `HUONG_DAN_SETUP_DATABASE_CHI_TIET.md` - Hướng dẫn chi tiết
- ✅ `SETUP_NHANH.md` - Hướng dẫn nhanh

---

## 🎯 CÁCH 1: SETUP TỰ ĐỘNG (KHUYẾN NGHỊ)

### Windows:

**Bước 1:** Mở Command Prompt hoặc PowerShell trong thư mục `backend_api`

**Bước 2:** Chạy script:
```bash
cd backend_api
setup_database.bat
```

**Bước 3:** Nhập thông tin khi được hỏi:
- Username: `root` (hoặc user MySQL của bạn)
- Host: `localhost` (hoặc IP MySQL server)
- Password: Nhập password MySQL khi được yêu cầu

**Bước 4:** Kiểm tra kết quả:
- Script sẽ tự động tạo database
- Kiểm tra xem có thông báo thành công không

### Linux/Mac:

**Bước 1:** Mở terminal trong thư mục `backend_api`

**Bước 2:** Cho phép chạy script:
```bash
chmod +x setup_database.sh
```

**Bước 3:** Chạy script:
```bash
./setup_database.sh
```

**Bước 4:** Nhập thông tin tương tự như Windows

---

## 🎯 CÁCH 2: SETUP THỦ CÔNG

### Bước 1: Mở MySQL Console

**Windows:**
```bash
# Nếu MySQL trong PATH
mysql -u root -p

# Hoặc tìm MySQL tại:
# C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe
```

**Linux/Mac:**
```bash
mysql -u root -p
```

### Bước 2: Tạo Database

**Cách 1: Import từ file (Nhanh nhất)**
```bash
mysql -u root -p < backend_api/create_database.sql
```

**Cách 2: Copy và paste SQL**
1. Mở file `backend_api/create_database.sql`
2. Copy toàn bộ nội dung
3. Paste vào MySQL console
4. Nhấn Enter

**Cách 3: Dùng phpMyAdmin**
1. Đăng nhập phpMyAdmin
2. Chọn tab "SQL"
3. Copy nội dung `create_database.sql`
4. Paste và nhấn "Go"

### Bước 3: Kiểm tra

Trong MySQL console:
```sql
-- Kiểm tra database
SHOW DATABASES;

-- Sử dụng database
USE tinhoc321_quiz;

-- Kiểm tra bảng
SHOW TABLES;

-- Kiểm tra cấu trúc bảng quiz_results
DESCRIBE quiz_results;
```

**Kết quả mong đợi:**
```
Tables:
- quiz_results
- students

Views:
- v_quiz_stats
- v_student_stats
- v_class_stats
```

---

## 📋 BƯỚC 3: CẤU HÌNH API

### Sửa file `backend_api/api/config.php`

```php
// Cấu hình Database
define('DB_HOST', 'localhost');  // Hoặc IP MySQL server
define('DB_NAME', 'tinhoc321_quiz');
define('DB_USER', 'root');  // Hoặc user riêng nếu đã tạo
define('DB_PASS', 'your_password');  // ⚠️ THAY BẰNG PASSWORD THỰC TẾ
```

**⚠️ QUAN TRỌNG:** Nhớ thay `your_password` bằng password MySQL thực tế của bạn!

---

## 📋 BƯỚC 4: TEST KẾT NỐI

### Test 1: Mở file test trong browser

1. Đảm bảo bạn có web server (Apache/Nginx/XAMPP/WAMP)
2. Hoặc dùng PHP built-in server:
   ```bash
   cd backend_api
   php -S localhost:8000
   ```
3. Mở browser: `http://localhost:8000/test_connection.php`

**Kết quả mong đợi:**
- ✅ "Kết nối database thành công!"
- ✅ Danh sách các bảng
- ✅ Test INSERT thành công

### Test 2: Test bằng command line

```bash
mysql -u root -p tinhoc321_quiz -e "SELECT COUNT(*) as count FROM quiz_results;"
```

**Kết quả:** Hiển thị số bản ghi (có thể là 0 nếu chưa có dữ liệu)

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

**Hoặc dùng browser:** Mở `http://localhost/backend_api/test_api.php`

---

## ✅ CHECKLIST HOÀN THÀNH

Sau khi setup, kiểm tra:

- [ ] MySQL service đã chạy
- [ ] Database `tinhoc321_quiz` đã được tạo
- [ ] Bảng `quiz_results` đã được tạo
- [ ] Bảng `students` đã được tạo
- [ ] Views đã được tạo (3 views)
- [ ] File `config.php` đã được cấu hình với password đúng
- [ ] Test connection thành công
- [ ] Test API endpoint thành công

---

## 🔧 XỬ LÝ LỖI THƯỜNG GẶP

### ❌ Lỗi: "Access denied for user 'root'@'localhost'"

**Nguyên nhân:** Password sai

**Giải pháp:**
1. Kiểm tra lại password trong `config.php`
2. Test password:
   ```bash
   mysql -u root -p
   ```
   Nếu không vào được → Password sai
3. Nếu quên password, reset:
   ```sql
   -- Trong MySQL console (với quyền admin)
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
   FLUSH PRIVILEGES;
   ```

### ❌ Lỗi: "Unknown database 'tinhoc321_quiz'"

**Nguyên nhân:** Database chưa được tạo

**Giải pháp:**
```bash
# Chạy lại script tạo database
mysql -u root -p < backend_api/create_database.sql
```

### ❌ Lỗi: "Table 'quiz_results' doesn't exist"

**Nguyên nhân:** Bảng chưa được tạo

**Giải pháp:**
1. Kiểm tra đã chạy đầy đủ script SQL chưa
2. Kiểm tra database có đúng tên không:
   ```sql
   USE tinhoc321_quiz;
   SHOW TABLES;
   ```

### ❌ Lỗi: MySQL không có trong PATH

**Nguyên nhân:** MySQL chưa được thêm vào PATH

**Giải pháp Windows:**
1. Tìm MySQL: `C:\Program Files\MySQL\MySQL Server 8.0\bin\`
2. Dùng full path:
   ```bash
   "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < backend_api/create_database.sql
   ```

**Giải pháp Linux/Mac:**
```bash
# Tìm MySQL
which mysql
# Hoặc
find /usr -name mysql 2>/dev/null

# Dùng full path nếu cần
/usr/local/mysql/bin/mysql -u root -p < backend_api/create_database.sql
```

---

## 📞 HỖ TRỢ

**Nếu gặp vấn đề, kiểm tra:**

1. **MySQL có chạy không?**
   - Windows: Mở `services.msc` → Tìm MySQL service
   - Linux: `sudo systemctl status mysql`
   - Mac: `brew services list` (nếu dùng Homebrew)

2. **Test kết nối MySQL:**
   ```bash
   mysql -u root -p
   ```
   Nếu vào được → MySQL OK

3. **Kiểm tra file config:**
   - Mở `backend_api/api/config.php`
   - Kiểm tra DB_HOST, DB_NAME, DB_USER, DB_PASS

4. **Test PHP kết nối:**
   - Mở `backend_api/test_connection.php` trong browser

---

## 🎯 SAU KHI SETUP XONG

1. ✅ Database đã được tạo
2. ✅ API đã được cấu hình
3. ⏭️ **Bước tiếp theo:** Test từ frontend
   - Mở `index.html`
   - Đăng nhập
   - Làm một bài bất kỳ
   - Kiểm tra kết quả có lưu vào database không

---

## 📝 TÓM TẮT CÁC LỆNH

```bash
# 1. Tạo database
mysql -u root -p < backend_api/create_database.sql

# 2. Kiểm tra
mysql -u root -p -e "USE tinhoc321_quiz; SHOW TABLES;"

# 3. Test connection
# Mở: backend_api/test_connection.php

# 4. Test API
# Mở: backend_api/test_api.php
```

---

**Chúc bạn setup thành công!** 🎉

