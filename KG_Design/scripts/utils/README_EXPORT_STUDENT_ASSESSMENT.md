# 📥 HƯỚNG DẪN NHANH: EXPORT STUDENT ASSESSMENT

## 🚀 Cách 1: Dùng Script Batch (Windows) - Dễ nhất

1. **Chạy file batch:**
   ```bash
   cd KG_Design/scripts/utils
   export_student_assessment.bat
   ```

2. **Nhập thông tin MySQL khi được hỏi:**
   - Host: `localhost` hoặc `mysql.tinhoc123.com`
   - Username: Tên user MySQL
   - Password: Mật khẩu MySQL
   - Database: `tinhoc321_quiz`
   - Year: `2024`

3. **Kết quả:** File `KG_Design/csv/student_assessment.csv`

---

## 🚀 Cách 2: Dùng File Config

1. **Tạo file config:**
   ```bash
   cd KG_Design/scripts/utils
   copy mysql_config.json.example mysql_config.json
   ```

2. **Sửa file `mysql_config.json`:**
   ```json
   {
     "host": "mysql.tinhoc123.com",
     "port": 3306,
     "database": "tinhoc321_quiz",
     "user": "your_username",
     "password": "your_password"
   }
   ```

3. **Chạy script:**
   ```bash
   python export_student_assessment_from_mysql.py --config mysql_config.json
   ```

---

## 🚀 Cách 3: Dùng Tham Số Dòng Lệnh

```bash
cd KG_Design/scripts/utils
python export_student_assessment_from_mysql.py \
    --host mysql.tinhoc123.com \
    --user username \
    --password password \
    --database tinhoc321_quiz \
    --year 2024 \
    --output ../../csv/student_assessment.csv
```

---

## 📋 Yêu Cầu

- Python 3.6+
- Thư viện: `mysql-connector-python`
  ```bash
  pip install mysql-connector-python
  ```

---

## 🔍 Lấy Thông Tin MySQL Từ Hosting

### Từ Control Panel (cPanel, Plesk):
1. Đăng nhập Control Panel
2. Tìm mục **"MySQL Databases"**
3. Xem thông tin:
   - Database name
   - Username
   - Password
   - Host (thường là `localhost`)

### Từ File config.php trên hosting:
1. Truy cập qua FTP/SSH: `backend_api/api/config.php`
2. Xem các dòng:
   ```php
   define('DB_HOST', 'localhost');
   define('DB_NAME', 'tinhoc321_quiz');
   define('DB_USER', 'username');
   define('DB_PASS', 'password');
   ```

---

## ✅ Kiểm Tra Kết Quả

```bash
# Xem 10 dòng đầu
head -n 10 KG_Design/csv/student_assessment.csv

# Đếm số dòng
wc -l KG_Design/csv/student_assessment.csv
```

**Format đúng:**
```csv
studentId,assessId,score
2526_K6_0001,ASSESS_K6_A1_2024,0.85
2526_K6_0001,ASSESS_K6_A2_2024,0.90
```

---

## 🐛 Xử Lý Lỗi

### Lỗi: "Access denied"
- Kiểm tra lại username/password
- Đảm bảo user có quyền SELECT

### Lỗi: "Can't connect"
- Kiểm tra host đúng chưa
- Kiểm tra port (mặc định 3306)
- Kiểm tra firewall

### Lỗi: "Student not found"
- Kiểm tra file `students_25_26.csv` có đúng không
- Tên học sinh có thể khác nhau (có dấu/không dấu)

---

## 📚 Tài Liệu Chi Tiết

Xem: `KG_Design/HUONG_DAN_LAY_KET_QUA_TU_HOSTING.md`

