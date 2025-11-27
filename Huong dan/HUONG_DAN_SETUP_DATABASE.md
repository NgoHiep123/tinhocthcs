# 📚 HƯỚNG DẪN SETUP DATABASE MYSQL

> Hướng dẫn chi tiết để setup database MySQL cho hệ thống lưu kết quả

---

## 🎯 YÊU CẦU

- MySQL Server 5.7+ hoặc MariaDB 10.2+
- Quyền tạo database và user

---

## 📋 BƯỚC 1: TẠO DATABASE

### Cách 1: Dùng MySQL Command Line

```bash
# Đăng nhập MySQL
mysql -u root -p

# Chạy script tạo database
source backend_api/create_database.sql

# Hoặc copy nội dung và paste vào MySQL console
```

### Cách 2: Dùng phpMyAdmin

1. Đăng nhập phpMyAdmin
2. Chọn tab "SQL"
3. Copy nội dung file `backend_api/create_database.sql`
4. Paste vào và nhấn "Go"

### Cách 3: Import file trực tiếp

```bash
mysql -u root -p < backend_api/create_database.sql
```

**Kiểm tra:**
```sql
SHOW DATABASES;
USE tinhoc321_quiz;
SHOW TABLES;
DESCRIBE quiz_results;
```

---

## 📋 BƯỚC 2: TẠO USER MYSQL (Tùy chọn)

**Nếu muốn dùng user riêng thay vì root:**

```sql
-- Tạo user mới
CREATE USER 'tinhoc321_user'@'localhost' IDENTIFIED BY 'your_strong_password';

-- Cấp quyền
GRANT ALL PRIVILEGES ON tinhoc321_quiz.* TO 'tinhoc321_user'@'localhost';

-- Áp dụng thay đổi
FLUSH PRIVILEGES;
```

**Lưu ý:** Thay `your_strong_password` bằng mật khẩu mạnh.

---

## 📋 BƯỚC 3: CẤU HÌNH API

Chỉnh sửa file `backend_api/api/config.php`:

```php
// Cấu hình Database
define('DB_HOST', 'localhost');  // Hoặc IP MySQL server
define('DB_NAME', 'tinhoc321_quiz');
define('DB_USER', 'root');  // Hoặc 'tinhoc321_user' nếu đã tạo user riêng
define('DB_PASS', 'your_password');  // Mật khẩu MySQL
```

---

## 📋 BƯỚC 4: TEST KẾT NỐI

### Test bằng PHP script:

Tạo file `backend_api/test_connection.php`:

```php
<?php
require_once 'api/config.php';

try {
    $pdo = getDBConnection();
    echo "✅ Kết nối database thành công!\n";
    
    // Test query
    $stmt = $pdo->query("SELECT COUNT(*) as count FROM quiz_results");
    $result = $stmt->fetch();
    echo "📊 Số bản ghi hiện có: " . $result['count'] . "\n";
    
} catch (Exception $e) {
    echo "❌ Lỗi: " . $e->getMessage() . "\n";
}
?>
```

Chạy:
```bash
php backend_api/test_connection.php
```

### Test bằng command line:

```bash
mysql -u root -p tinhoc321_quiz -e "SELECT COUNT(*) FROM quiz_results;"
```

---

## 📋 BƯỚC 5: TEST API ENDPOINT

### Test API lưu kết quả:

```bash
curl -X POST http://localhost/api/save_result.php \
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

### Test API lấy kết quả:

```bash
curl http://localhost/api/get_results.php
```

---

## ✅ KIỂM TRA

1. **Kiểm tra database có dữ liệu:**
   ```sql
   USE tinhoc321_quiz;
   SELECT * FROM quiz_results ORDER BY created_at DESC LIMIT 10;
   ```

2. **Kiểm tra dashboard:**
   - Mở: `http://localhost/backend_api/dashboard/index.php`
   - Xem thống kê và danh sách kết quả

3. **Test từ frontend:**
   - Mở `index.html`
   - Đăng nhập
   - Làm một bài bất kỳ
   - Kiểm tra kết quả có lưu vào database không

---

## 🔧 XỬ LÝ LỖI

### Lỗi: "Access denied for user"

**Nguyên nhân:** Username/password sai hoặc user chưa có quyền

**Giải pháp:**
1. Kiểm tra lại `DB_USER` và `DB_PASS` trong `config.php`
2. Đảm bảo user có quyền truy cập database:
   ```sql
   GRANT ALL PRIVILEGES ON tinhoc321_quiz.* TO 'your_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Lỗi: "Unknown database 'tinhoc321_quiz'"

**Nguyên nhân:** Database chưa được tạo

**Giải pháp:**
1. Chạy lại script tạo database:
   ```bash
   mysql -u root -p < backend_api/create_database.sql
   ```

### Lỗi: "Table 'quiz_results' doesn't exist"

**Nguyên nhân:** Bảng chưa được tạo

**Giải pháp:**
1. Kiểm tra lại script `create_database.sql` đã chạy đầy đủ chưa
2. Tạo bảng thủ công nếu cần:
   ```sql
   USE tinhoc321_quiz;
   -- Copy nội dung CREATE TABLE từ create_database.sql
   ```

### Lỗi CORS khi gọi API từ frontend

**Nguyên nhân:** CORS chưa được cấu hình đúng

**Giải pháp:**
1. Kiểm tra `ALLOWED_ORIGINS` trong `config.php`
2. Đảm bảo domain frontend có trong danh sách
3. Tạm thời có thể dùng `'*'` để test (không nên dùng trong production)

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề, kiểm tra:
1. **MySQL logs:** `/var/log/mysql/error.log` (Linux) hoặc MySQL log (Windows)
2. **PHP error log:** Kiểm tra file log của PHP
3. **Browser console:** Xem lỗi JavaScript/CORS

