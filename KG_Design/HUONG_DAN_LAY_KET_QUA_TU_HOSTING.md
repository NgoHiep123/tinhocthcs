# 📥 HƯỚNG DẪN LẤY KẾT QUẢ TỪ HOSTING TINHOC123.COM

> Hướng dẫn từng bước để export kết quả quiz từ MySQL trên hosting và tạo file `student_assessment.csv`

---

## 📋 TỔNG QUAN

**Mục tiêu:** Lấy dữ liệu từ bảng `quiz_results` trong MySQL trên hosting `tinhoc123.com` và chuyển đổi thành file `student_assessment.csv` để build Knowledge Graph.

**Luồng dữ liệu:**
```
Hosting tinhoc123.com (MySQL)
    ↓
Export dữ liệu (3 phương án)
    ↓
Mapping & Convert
    ↓
student_assessment.csv
    ↓
Build TTL → GraphDB
```

---

## 🔧 PHƯƠNG ÁN 1: EXPORT QUA PHPMYADMIN (Dễ nhất) ✅

### Bước 1: Đăng nhập phpMyAdmin

1. Truy cập: `http://tinhoc123.com/phpmyadmin` (hoặc URL phpMyAdmin của hosting)
2. Đăng nhập với thông tin MySQL của hosting

### Bước 2: Chọn Database

1. Chọn database: `tinhoc321_quiz` (hoặc tên database thực tế trên hosting)
2. Click vào tab **"SQL"**

### Bước 3: Chạy Query Export

**Copy và paste query sau:**

```sql
SELECT 
    qr.student_name,
    qr.class_name,
    qr.quiz_id,
    qr.score,
    qr.total,
    qr.percentage,
    DATE(qr.created_at) as date
FROM quiz_results qr
ORDER BY qr.created_at DESC;
```

**Hoặc query đầy đủ hơn:**

```sql
SELECT 
    qr.id,
    qr.student_name,
    qr.class_name,
    qr.quiz_id,
    qr.score,
    qr.total,
    ROUND(qr.score / qr.total, 2) as normalized_score,
    qr.percentage,
    qr.duration,
    qr.created_at
FROM quiz_results qr
ORDER BY qr.created_at DESC
LIMIT 10000;
```

### Bước 4: Export ra CSV

1. Sau khi query chạy xong, click nút **"Export"** (phía trên kết quả)
2. Chọn format: **"CSV"**
3. Tùy chọn:
   - ✅ **"Put columns names in the first row"** (có header)
   - ✅ **"Replace NULL with"**: để trống
4. Click **"Go"** để tải file CSV

### Bước 5: Chuyển đổi sang format đúng

File CSV từ phpMyAdmin sẽ có format:
```csv
student_name,class_name,quiz_id,score,total,percentage,date
Nguyễn Văn A,6/1,K6_A1,8,10,80.00,2024-01-15
```

**Cần chuyển đổi thành:**
```csv
studentId,assessId,score
2526_K6_0001,ASSESS_K6_A1_2024,0.8
```

**→ Dùng script Python ở Phương án 3 để chuyển đổi tự động**

---

## 🔧 PHƯƠNG ÁN 2: EXPORT QUA API (Nếu có API) ✅

### Bước 1: Kiểm tra API có sẵn

Truy cập: `http://tinhoc123.com/api/get_results.php?limit=1000`

**Kết quả mong đợi:**
```json
{
  "success": true,
  "count": 150,
  "data": [
    {
      "id": 1,
      "student_name": "Nguyễn Văn A",
      "class_name": "6/1",
      "quiz_id": "K6_A1",
      "score": 8,
      "total": 10,
      ...
    }
  ]
}
```

### Bước 2: Lưu kết quả JSON

**Cách 1: Dùng browser**
1. Mở URL trên trong browser
2. Right-click → "Save Page As" → Lưu file `results.json`

**Cách 2: Dùng curl (command line)**
```bash
curl "http://tinhoc123.com/api/get_results.php?limit=10000" > results.json
```

### Bước 3: Chuyển đổi JSON → CSV

**→ Dùng script Python ở Phương án 3**

---

## 🔧 PHƯƠNG ÁN 3: DÙNG SCRIPT PYTHON (Khuyến nghị) ✅✅✅

### Bước 1: Cài đặt thư viện

```bash
pip install mysql-connector-python pandas
```

### Bước 2: Tạo file cấu hình

Tạo file `KG_Design/scripts/utils/mysql_config.json`:

```json
{
  "host": "localhost",
  "database": "tinhoc321_quiz",
  "user": "your_username",
  "password": "your_password",
  "port": 3306
}
```

**⚠️ LƯU Ý BẢO MẬT:**
- File này chứa password, **KHÔNG commit lên GitHub**
- Thêm vào `.gitignore`: `**/mysql_config.json`

### Bước 3: Chạy script export

**Script:** `KG_Design/scripts/utils/export_student_assessment_from_mysql.py`

```bash
cd KG_Design
python scripts/utils/export_student_assessment_from_mysql.py
```

**Script sẽ:**
1. Kết nối MySQL (từ config hoặc tham số dòng lệnh)
2. Query dữ liệu từ `quiz_results`
3. Mapping `student_name` + `class_name` → `studentId` (từ `students_25_26.csv`)
4. Mapping `quiz_id` → `assessId` (format: `ASSESS_K6_A1_2024`)
5. Chuẩn hóa `score` (score/total)
6. Ghi ra `csv/student_assessment.csv`

---

## 📝 CHI TIẾT MAPPING DỮ LIỆU

### 1. Mapping `student_name` + `class_name` → `studentId`

**Nguồn:** File `KG_Design/csv/students_25_26.csv`

**Format trong MySQL:**
- `student_name`: "Nguyễn Văn A"
- `class_name`: "6/1"

**Format cần:**
- `studentId`: "2526_K6_0001"

**Cách tra cứu:**
```python
# Đọc students_25_26.csv
students = {}
with open('KG_Design/csv/students_25_26.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row['full_name'], row['class'])
        students[key] = row['id_student']  # hoặc cột tương ứng
```

**⚠️ Lưu ý:**
- Tên học sinh có thể khác nhau (có dấu/không dấu, viết hoa/thường)
- Cần normalize tên trước khi mapping
- Nếu không tìm thấy, có thể bỏ qua hoặc tạo `studentId` mới

### 2. Mapping `quiz_id` → `assessId`

**Format trong MySQL:**
- `quiz_id`: "K6_A1", "K6_A2", "K7_E1", ...

**Format cần:**
- `assessId`: "ASSESS_K6_A1_2024", "ASSESS_K6_A2_2024", ...

**Cách chuyển đổi:**
```python
def quiz_id_to_assess_id(quiz_id, year=2024):
    """Chuyển quiz_id thành assessId"""
    # K6_A1 → ASSESS_K6_A1_2024
    if quiz_id.startswith('K'):
        return f"ASSESS_{quiz_id}_{year}"
    return f"ASSESS_{quiz_id}_{year}"
```

### 3. Chuẩn hóa `score`

**Format trong MySQL:**
- `score`: 8 (số câu đúng)
- `total`: 10 (tổng số câu)

**Format cần:**
- `score`: 0.8 (chuẩn hóa 0-1) hoặc 8.0 (thang điểm 0-10)

**Cách tính:**
```python
normalized_score = score / total  # 0.8 (0-1)
# hoặc
score_10 = (score / total) * 10  # 8.0 (0-10)
```

---

## 🚀 HƯỚNG DẪN CHI TIẾT TỪNG BƯỚC

### Bước 1: Lấy thông tin MySQL từ hosting

**Cách 1: Từ Control Panel (cPanel, Plesk, ...)**
1. Đăng nhập Control Panel của hosting
2. Tìm mục **"MySQL Databases"** hoặc **"Databases"**
3. Xem thông tin:
   - **Database name:** `tinhoc321_quiz` (hoặc tên khác)
   - **Username:** `username_db`
   - **Password:** (đã lưu khi tạo)
   - **Host:** `localhost` hoặc `mysql.tinhoc123.com`

**Cách 2: Từ file `config.php` trên hosting**
1. Truy cập: `http://tinhoc123.com/backend_api/api/config.php` (nếu có)
2. Hoặc qua FTP/SSH: `backend_api/api/config.php`
3. Xem các dòng:
   ```php
   define('DB_HOST', 'localhost');
   define('DB_NAME', 'tinhoc321_quiz');
   define('DB_USER', 'username');
   define('DB_PASS', 'password');
   ```

### Bước 2: Kiểm tra kết nối MySQL

**Test từ local máy tính:**

```bash
# Cài đặt MySQL client (nếu chưa có)
# Windows: Download MySQL Workbench hoặc XAMPP
# Linux: sudo apt-get install mysql-client
# Mac: brew install mysql-client

# Test kết nối
mysql -h mysql.tinhoc123.com -u username -p tinhoc321_quiz
```

**Hoặc dùng script Python test:**

```python
import mysql.connector

try:
    conn = mysql.connector.connect(
        host='mysql.tinhoc123.com',  # hoặc IP hosting
        database='tinhoc321_quiz',
        user='username',
        password='password',
        port=3306
    )
    print("✅ Kết nối thành công!")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM quiz_results")
    count = cursor.fetchone()[0]
    print(f"📊 Số bản ghi: {count}")
    conn.close()
except Exception as e:
    print(f"❌ Lỗi: {e}")
```

### Bước 3: Export dữ liệu

**Chọn một trong 3 phương án ở trên**

### Bước 4: Chạy script chuyển đổi

```bash
cd KG_Design
python scripts/utils/export_student_assessment_from_mysql.py \
    --host mysql.tinhoc123.com \
    --user username \
    --password your_password \
    --database tinhoc321_quiz \
    --output csv/student_assessment.csv
```

**Hoặc dùng file config:**

```bash
python scripts/utils/export_student_assessment_from_mysql.py \
    --config scripts/utils/mysql_config.json
```

### Bước 5: Kiểm tra kết quả

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
2526_K6_0002,ASSESS_K6_A1_2024,0.75
```

### Bước 6: Build TTL file

```bash
cd KG_Design
python scripts/build/build_ttl.py
```

**Hoặc chỉ build `test_results.ttl`:**

```bash
python scripts/build/build_ttl.py --only test_results
```

---

## 🔒 BẢO MẬT

### ⚠️ QUAN TRỌNG:

1. **KHÔNG commit file chứa password:**
   - `mysql_config.json`
   - File `.env` nếu có
   - File `config.php` với password thật

2. **Thêm vào `.gitignore`:**
   ```
   **/mysql_config.json
   **/.env
   backend_api/api/config.php
   ```

3. **Dùng biến môi trường:**
   ```bash
   export MYSQL_HOST=mysql.tinhoc123.com
   export MYSQL_USER=username
   export MYSQL_PASSWORD=password
   ```

---

## 🐛 XỬ LÝ LỖI

### Lỗi: "Access denied for user"

**Nguyên nhân:** Username/password sai hoặc user không có quyền

**Giải pháp:**
1. Kiểm tra lại thông tin trong Control Panel
2. Đảm bảo user có quyền SELECT trên database
3. Thử kết nối từ phpMyAdmin trước

### Lỗi: "Can't connect to MySQL server"

**Nguyên nhân:** Host sai hoặc firewall chặn

**Giải pháp:**
1. Kiểm tra host: `localhost` (nếu script chạy trên hosting) hoặc IP/hostname thực tế
2. Kiểm tra port: mặc định 3306
3. Liên hệ hosting để mở port nếu cần

### Lỗi: "Unknown database"

**Nguyên nhân:** Tên database sai

**Giải pháp:**
1. Kiểm tra tên database trong Control Panel
2. Kiểm tra trong `config.php` trên hosting

### Lỗi: "Student not found in mapping"

**Nguyên nhân:** Tên học sinh trong MySQL khác với `students_25_26.csv`

**Giải pháp:**
1. Kiểm tra và normalize tên (bỏ dấu, lowercase)
2. Cập nhật `students_25_26.csv` với tên đúng
3. Hoặc bỏ qua các bản ghi không map được (ghi log)

---

## ✅ CHECKLIST

- [ ] Đã lấy thông tin MySQL từ hosting
- [ ] Đã test kết nối MySQL thành công
- [ ] Đã export dữ liệu từ `quiz_results`
- [ ] Đã chạy script chuyển đổi
- [ ] Đã kiểm tra file `student_assessment.csv` đúng format
- [ ] Đã build TTL file `test_results.ttl`
- [ ] Đã upload lên GraphDB và test query

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề:
1. Kiểm tra log file: `KG_Design/logs/export_student_assessment.log`
2. Xem báo cáo chi tiết: `KG_Design/BAO_CAO_NGUON_DU_LIEU_STUDENT_ASSESSMENT.md`
3. Kiểm tra script: `KG_Design/scripts/utils/export_student_assessment_from_mysql.py`

---

**Cập nhật:** 2025-01-15

