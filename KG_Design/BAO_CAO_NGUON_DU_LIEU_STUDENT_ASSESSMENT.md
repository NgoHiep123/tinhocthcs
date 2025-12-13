# 📊 BÁO CÁO NGUỒN DỮ LIỆU FILE `student_assessment.csv`

> Phân tích nguồn gốc và cách tạo file `student_assessment.csv`

---

## 📋 TỔNG QUAN

**File:** `KG_Design/csv/student_assessment.csv`

**Mục đích:** Lưu kết quả đánh giá (điểm số) của học sinh trong các bài kiểm tra để tạo `test_results.ttl` trong Knowledge Graph.

**Format hiện tại:**
```csv
studentId,assessId,score
2526_K6_0001,ASSESS_K6_A1_2024,8.5
2526_K6_0001,ASSESS_K6_A2_2024,9.0
2526_K6_0002,ASSESS_K6_A1_2024,7.5
2526_K6_0002,ASSESS_K6_A2_2024,8.0
2526_K6_0003,ASSESS_K6_A1_2024,9.5
2526_K6_0003,ASSESS_K6_A2_2024,9.0
```

---

## 🔍 NGUỒN DỮ LIỆU

### 1. **Dữ liệu hiện tại: DỮ LIỆU MẪU (Sample Data)** ⚠️

File hiện tại chứa **dữ liệu mẫu** để test, không phải dữ liệu thực tế:
- 3 học sinh: `2526_K6_0001`, `2526_K6_0002`, `2526_K6_0003`
- 2 bài kiểm tra: `ASSESS_K6_A1_2024`, `ASSESS_K6_A2_2024`
- Điểm số mẫu: 7.5 - 9.5

---

### 2. **Nguồn dữ liệu THỰC TẾ (Production Data)** ✅

Dữ liệu thực tế sẽ đến từ:

#### A. **Web Application (Nguồn chính)**

**Luồng dữ liệu:**
```
Học sinh làm quiz trên web (tinhoc321.com)
    ↓
Submit kết quả qua API
    ↓
backend_api/api/save_result.php
    ↓
MySQL Database: bảng quiz_results
    ↓
Export hoặc Sync → student_assessment.csv
```

**Chi tiết:**
1. **Frontend:** File HTML quiz (ví dụ: `K6_A1.html`)
   - Học sinh làm bài và submit
   - Gửi kết quả qua API endpoint

2. **Backend API:** `backend_api/api/save_result.php`
   - Nhận dữ liệu: `student_name`, `class_name`, `quiz_id`, `score`, `total`, `duration`
   - Lưu vào MySQL bảng `quiz_results`

3. **MySQL Database:**
   - **Database:** `tinhoc321_quiz`
   - **Table:** `quiz_results`
   - **Cấu trúc:**
     ```sql
     CREATE TABLE quiz_results (
       id INT AUTO_INCREMENT PRIMARY KEY,
       student_name VARCHAR(100) NOT NULL,
       class_name VARCHAR(20) NOT NULL,
       quiz_id VARCHAR(50) NOT NULL,
       score INT NOT NULL,
       total INT NOT NULL,
       percentage DECIMAL(5,2) NOT NULL,
       duration INT NOT NULL,
       ip_address VARCHAR(45),
       user_agent TEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     )
     ```

#### B. **Export từ MySQL**

Để tạo file `student_assessment.csv` từ MySQL, cần:

1. **Query MySQL:**
   ```sql
   SELECT 
     CONCAT(year, '_', grade, '_', LPAD(student_num, 4, '0')) AS studentId,
     quiz_id AS assessId,
     (score / total) AS score
   FROM quiz_results
   WHERE ... -- Điều kiện lọc
   ORDER BY studentId, assessId;
   ```

2. **Mapping:**
   - `student_name` + `class_name` → `studentId` (cần mapping với `students_25_26.csv`)
   - `quiz_id` → `assessId` (cần đảm bảo format đúng, ví dụ: `ASSESS_K6_A1_2024`)
   - `score` / `total` → `score` (chuẩn hóa về thang điểm 0-1 hoặc 0-10)

---

### 3. **Script đồng bộ tự động**

**File:** `scripts/sync_mysql_to_graphdb.py`

**Chức năng:**
- Đồng bộ dữ liệu từ MySQL → GraphDB trực tiếp (không qua CSV)
- Đọc từ bảng `quiz_results` trong MySQL
- Tạo RDF triples và upload lên GraphDB

**Cách dùng:**
```bash
# Đồng bộ tất cả kết quả chưa sync
python scripts/sync_mysql_to_graphdb.py --all

# Đồng bộ từ một thời điểm cụ thể
python scripts/sync_mysql_to_graphdb.py --since "2024-01-01 00:00:00"
```

---

## 🔄 CÁCH TẠO FILE `student_assessment.csv`

### Phương án 1: Export từ MySQL (Khuyến nghị) ✅

**Bước 1:** Kết nối MySQL và query dữ liệu

```sql
USE tinhoc321_quiz;

SELECT 
    -- Cần mapping student_name + class_name → studentId
    -- Ví dụ: sử dụng bảng mapping hoặc function
    qr.quiz_id AS assessId,
    qr.score / qr.total AS score,
    DATE(qr.created_at) AS date
FROM quiz_results qr
ORDER BY qr.created_at DESC;
```

**Bước 2:** Export kết quả ra CSV

```bash
# Sử dụng MySQL command line
mysql -u root -p -e "
SELECT student_name, class_name, quiz_id, score/total as score
FROM tinhoc321_quiz.quiz_results
" | sed 's/\t/,/g' > student_assessment_raw.csv
```

**Bước 3:** Chuyển đổi format

- Mapping `student_name` + `class_name` → `studentId` (từ `students_25_26.csv`)
- Mapping `quiz_id` → `assessId` (đảm bảo format đúng)
- Chuẩn hóa `score` (nếu cần)

---

### Phương án 2: Tạo script Python để export ✅

**Tạo script:** `KG_Design/scripts/utils/export_student_assessment_from_mysql.py`

```python
import mysql.connector
import csv
from pathlib import Path

# Kết nối MySQL
conn = mysql.connector.connect(
    host='localhost',
    database='tinhoc321_quiz',
    user='your_user',
    password='your_password'
)

cursor = conn.cursor()

# Query
query = """
SELECT 
    student_name,
    class_name,
    quiz_id,
    score,
    total,
    created_at
FROM quiz_results
ORDER BY created_at DESC
"""

cursor.execute(query)
results = cursor.fetchall()

# Mapping student_name + class_name → studentId
# (Cần đọc students_25_26.csv để mapping)

# Ghi ra CSV
output_file = Path("KG_Design/csv/student_assessment.csv")
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['studentId', 'assessId', 'score'])
    
    for row in results:
        student_name, class_name, quiz_id, score, total, created_at = row
        # TODO: Mapping studentId
        # TODO: Mapping assessId
        normalized_score = score / total  # hoặc score / 10.0
        writer.writerow([studentId, assessId, normalized_score])

cursor.close()
conn.close()
```

---

### Phương án 3: Nhập thủ công (Cho dữ liệu nhỏ) ⚠️

Nếu chỉ có vài kết quả, có thể nhập thủ công vào file CSV.

---

## 📊 MAPPING DỮ LIỆU

### Mapping `student_name` + `class_name` → `studentId`

**Nguồn:** File `KG_Design/csv/students_25_26.csv`

**Ví dụ:**
```
student_name: "Nguyễn Văn A"
class_name: "6/1"
    ↓
studentId: "2526_K6_0001"
```

**Cách tra cứu:**
```python
import csv

# Đọc students_25_26.csv
students = {}
with open('KG_Design/csv/students_25_26.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row['fullName'], row['className'])
        students[key] = row['studentId']

# Tra cứu
student_id = students.get(('Nguyễn Văn A', '6/1'))
```

### Mapping `quiz_id` → `assessId`

**Format trong MySQL:** `quiz_id` (ví dụ: `K6_A1`, `K6_A2`)

**Format cần:** `assessId` (ví dụ: `ASSESS_K6_A1_2024`, `ASSESS_K6_A2_2024`)

**Cách chuyển đổi:**
```python
def quiz_id_to_assess_id(quiz_id, year=2024):
    """Chuyển quiz_id thành assessId"""
    # Ví dụ: K6_A1 → ASSESS_K6_A1_2024
    if quiz_id.startswith('K'):
        return f"ASSESS_{quiz_id}_{year}"
    return f"ASSESS_{quiz_id}_{year}"
```

---

## ✅ KHUYẾN NGHỊ

### Cho Production:

1. **Sử dụng script đồng bộ trực tiếp:**
   - Dùng `scripts/sync_mysql_to_graphdb.py` để đồng bộ từ MySQL → GraphDB
   - Không cần file CSV trung gian

2. **Nếu cần file CSV:**
   - Tạo script Python để export từ MySQL
   - Chạy định kỳ (cron job) để cập nhật

3. **Format chuẩn:**
   ```csv
   studentId,assessId,score
   2526_K6_0001,ASSESS_K6_A1_2024,0.85
   2526_K6_0001,ASSESS_K6_A2_2024,0.90
   ```
   - `score`: Nên chuẩn hóa về 0-1 (0.85 = 8.5/10) hoặc 0-10 (8.5)

---

## 📝 TÓM TẮT

| Nguồn dữ liệu | Trạng thái | Cách tạo |
|---------------|------------|----------|
| **File hiện tại** | ⚠️ Dữ liệu mẫu | Tạo thủ công để test |
| **MySQL Database** | ✅ Nguồn chính | Từ web application qua API |
| **Export từ MySQL** | ✅ Khuyến nghị | Script Python hoặc SQL export |
| **Sync trực tiếp** | ✅ Tốt nhất | `sync_mysql_to_graphdb.py` |

---

**Cập nhật:** 2025-01-15


