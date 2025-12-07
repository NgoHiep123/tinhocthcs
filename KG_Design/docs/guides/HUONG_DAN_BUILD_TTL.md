# 📘 HƯỚNG DẪN SỬ DỤNG SCRIPT TẠO TTL CÒN THIẾU

## 🎯 MỤC ĐÍCH

Script `build_missing_ttl.py` tự động tạo các file TTL còn thiếu để hoàn thiện Knowledge Graph theo schema chuẩn.

---

## 🚀 CÁCH SỬ DỤNG

### **Bước 1: Chạy script**

```bash
cd KG_Design/grade6
python build_missing_ttl.py
```

### **Bước 2: Kiểm tra kết quả**

Script sẽ tạo các file trong thư mục `out/`:
- `grades.ttl` - Khối lớp
- `topics.ttl` - Chủ đề
- `lessons.ttl` - Bài học
- `classes.ttl` - Lớp học
- `students_updated.ttl` - Học sinh (đã cập nhật)
- `questions_updated.ttl` - Câu hỏi (đã cập nhật)
- `tests.ttl` - Bài kiểm tra
- `test_results.ttl` - Kết quả
- `questions_in_tests.ttl` - Câu hỏi trong đề thi

---

## 📋 CÁC FILE ĐƯỢC TẠO

### **1. grades.ttl**
- Tạo 4 khối: 6, 7, 8, 9
- Không cần file input

### **2. topics.ttl**
- Tạo các chủ đề A, B, C, D, E, F cho từng khối
- Không cần file input (định nghĩa sẵn trong script)

### **3. lessons.ttl**
- Tạo các bài học cho Khối 6
- Không cần file input (định nghĩa sẵn trong script)

### **4. classes.ttl**
- Đọc từ `classes.csv` (nếu có)
- Hoặc tự động tạo từ `teachers_assignments.ttl`

### **5. students_updated.ttl**
- Đọc từ `student_mastery.csv`
- Bổ sung `fullName` từ `students_grade_data.json` (nếu có)
- Bổ sung `belongsToClass` từ thông tin lớp

### **6. questions_updated.ttl**
- Đọc từ `question_skill.csv`
- Bổ sung `belongsToLesson` (tự động parse từ question ID)
- Đổi `measures` thành `requiresSkill`

### **7. tests.ttl**
- Đọc từ `assessments.csv`
- Tạo các Test node

### **8. test_results.ttl**
- Đọc từ `student_assessment.csv`
- Tạo TestResult và các quan hệ:
  - Student → hasResult → TestResult
  - Student → takeTest → Test
  - TestResult → forTest → Test

### **9. questions_in_tests.ttl**
- Đọc từ `questions_in_assessment.csv`
- Tạo quan hệ Test → hasQuestion → Question

---

## ⚠️ LƯU Ý

### **1. File input cần có:**

- ✅ `student_mastery.csv` - Bắt buộc cho students_updated.ttl
- ✅ `question_skill.csv` - Bắt buộc cho questions_updated.ttl
- ✅ `assessments.csv` - Bắt buộc cho tests.ttl
- ✅ `student_assessment.csv` - Bắt buộc cho test_results.ttl
- ⚠️ `classes.csv` - Tùy chọn (nếu không có sẽ tự động tạo từ teachers_assignments.ttl)
- ⚠️ `students_grade_data.json` - Tùy chọn (để bổ sung fullName)
- ⚠️ `questions_in_assessment.csv` - Tùy chọn (cho questions_in_tests.ttl)

### **2. Namespace:**

Script sử dụng namespace chuẩn:
- `http://education.vn/ontology#` (edu:)
- `http://education.vn/data/` (data:)

### **3. Cập nhật file cũ:**

- `students_updated.ttl` thay thế `students.ttl` (có thêm fullName và belongsToClass)
- `questions_updated.ttl` thay thế `question_skill.ttl` (có thêm belongsToLesson và dùng requiresSkill)

---

## 🔄 SAU KHI CHẠY SCRIPT

### **Bước 1: Kiểm tra các file đã tạo**

```bash
ls -la KG_Design/grade6/out/*.ttl
```

### **Bước 2: Import vào GraphDB**

1. Mở GraphDB Desktop
2. Import các file TTL theo thứ tự:
   - Schema (`kg_schema_chuan.ttl`) - **PHẢI LÀM TRƯỚC**
   - `grades.ttl`
   - `topics.ttl`
   - `lessons.ttl`
   - `classes.ttl`
   - `students_updated.ttl` (thay cho students.ttl)
   - `questions_updated.ttl` (thay cho question_skill.ttl)
   - `tests.ttl`
   - `test_results.ttl`
   - `questions_in_tests.ttl`
   - Các file khác (skills, resources, ...)

### **Bước 3: Test query**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

# Kiểm tra số lượng
SELECT (COUNT(?grade) AS ?numGrades)
WHERE {
  ?grade a edu:Grade .
}

SELECT (COUNT(?topic) AS ?numTopics)
WHERE {
  ?topic a edu:Topic .
}

SELECT (COUNT(?lesson) AS ?numLessons)
WHERE {
  ?lesson a edu:Lesson .
}
```

---

## 🐛 XỬ LÝ LỖI

### **Lỗi: "File not found"**

- Kiểm tra các file CSV cần thiết có tồn tại không
- Đảm bảo đang chạy script từ đúng thư mục `KG_Design/grade6/`

### **Lỗi: "Empty file"**

- Một số file có thể trống nếu không có dữ liệu input
- Kiểm tra file CSV có dữ liệu không

### **Lỗi: "Invalid namespace"**

- Script đã sử dụng namespace chuẩn, không cần chỉnh sửa
- Nếu cần đổi namespace, sửa biến `PREFIXES` trong script

---

## ✅ CHECKLIST

- [ ] Đã chạy `build_missing_ttl.py`
- [ ] Đã kiểm tra các file TTL đã tạo
- [ ] Đã import vào GraphDB
- [ ] Đã test query
- [ ] Đã kiểm tra không có lỗi

---

**Cập nhật:** 2025-01-15

