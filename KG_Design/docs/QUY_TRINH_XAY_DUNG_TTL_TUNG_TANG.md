# 🏗️ QUY TRÌNH XÂY DỰNG TTL TỪNG TẦNG A-E

> Hướng dẫn chi tiết: Tạo file TTL nào, từ dữ liệu nào, chạy script Python nào

---

## 📋 TỔNG QUAN

Quy trình xây dựng Knowledge Graph được chia thành 5 tầng:

| Tầng | Mô Tả | Số File | Đặc Điểm |
|------|-------|---------|----------|
| **A** | Schema (Ontology) | 1 | Định nghĩa cấu trúc, không cần build |
| **B** | Master Data | 6 | Dữ liệu tham chiếu cơ bản |
| **C** | Entity Data | 3 | Thực thể chính (học sinh, câu hỏi, bài kiểm tra) |
| **D** | Relationships | 5 | Quan hệ giữa các thực thể |
| **E** | Transactions | 2 | Dữ liệu giao dịch (kết quả, mastery) |

**Tổng cộng:** 17 file TTL

---

## 🏛️ TẦNG A - SCHEMA (Ontology)

### File: `schema/kg_schema_chuan.ttl`

**Đặc điểm:**
- ✅ **KHÔNG CẦN BUILD** - File đã có sẵn
- ✅ Chỉ cần upload vào GraphDB
- ✅ Phải upload đầu tiên

**Nội dung:**
- Định nghĩa 12 Classes (Student, Teacher, Lesson, Topic, Skill, Question, Test...)
- Định nghĩa 17 Relationships (belongsToClass, teaches, requiresSkill...)
- Định nghĩa 25+ Properties (studentId, fullName, score...)

**Cách sử dụng:**
```bash
# Chỉ cần upload vào GraphDB Desktop
# File: KG_Design/schema/kg_schema_chuan.ttl
```

**Không cần script Python!**

---

## 📚 TẦNG B - MASTER DATA

### 1. `grades.ttl` - Khối lớp

**Input:** ❌ Không cần file input (định nghĩa sẵn trong code)

**Script Python:**
```bash
cd KG_Design/scripts/build
python build_missing_ttl.py
```

**Hoặc chạy hàm riêng:**
```python
# Trong build_missing_ttl.py
def export_grades():
    """Tạo file grades.ttl với 4 khối: 6, 7, 8, 9"""
    # Tạo 4 grade: grade_6, grade_7, grade_8, grade_9
```

**Output:** `KG_Design/data/grade6/ttl/grades.ttl`

**Nội dung:**
- 4 khối lớp: 6, 7, 8, 9
- ~10 triples

---

### 2. `topics.ttl` - Chủ đề

**Input:** ❌ Không cần file input (định nghĩa sẵn trong code)

**Script Python:**
```bash
cd KG_Design/scripts/build
python build_missing_ttl.py
```

**Hoặc chạy hàm riêng:**
```python
# Trong build_missing_ttl.py
def export_topics():
    """Tạo file topics.ttl với các chủ đề cho từng khối"""
    # Topics config cho từng khối (A, B, C, D, E, F)
```

**Output:** `KG_Design/data/grade6/ttl/topics.ttl`

**Nội dung:**
- 24 chủ đề (6 chủ đề × 4 khối)
- ~20 triples

**Cấu trúc dữ liệu:**
```python
topics_config = {
    6: {
        "A": "Chủ đề A: Máy tính và cộng đồng",
        "B": "Chủ đề B: Mạng máy tính và Internet",
        # ...
    },
    # Khối 7, 8, 9 tương tự
}
```

---

### 3. `lessons.ttl` - Bài học

**Input:** ❌ Không cần file input (định nghĩa sẵn trong code)

**Script Python:**
```bash
cd KG_Design/scripts/build
python build_missing_ttl.py
```

**Hoặc chạy hàm riêng:**
```python
# Trong build_missing_ttl.py
def export_lessons():
    """Tạo file lessons.ttl với các bài học cho từng chủ đề"""
    # Lessons cho khối 6: A1-A5, B1-B4, C1-C6, D1-D3, E1-E8, F1-F5
```

**Output:** `KG_Design/data/grade6/ttl/lessons.ttl`

**Nội dung:**
- ~31 bài học cho khối 6
- ~150 triples

---

### 4. `classes.ttl` - Lớp học

**Input:** 
- ✅ `KG_Design/grade6/classes.csv` (tùy chọn)
- ✅ Hoặc tự động từ `teachers_assignments.ttl` (nếu có)

**Script Python:**
```bash
cd KG_Design/scripts/build
python build_missing_ttl.py
```

**Hoặc chạy hàm riêng:**
```python
# Trong build_missing_ttl.py
def export_classes():
    """Tạo file classes.ttl từ teachers_assignments hoặc classes.csv"""
    # Đọc từ CSV hoặc parse từ teachers_assignments.ttl
```

**Output:** `KG_Design/data/grade6/ttl/classes.ttl`

**Nội dung:**
- Các lớp học: 6/1, 6/2, 7/1, ...
- ~50 triples

**Format CSV (nếu có):**
```csv
classId,name,grade
6_1,6/1,6
6_2,6/2,6
```

---

### 5. `skills.ttl` - Kỹ năng

**Input:** 
- ✅ `KG_Design/grade6/skills.csv`

**Cách tạo CSV:**
```bash
# Option 1: Tự động từ câu hỏi
cd KG_Design
python build_inputs_from_existing.py
# Output: KG_Design/generated/skills.csv
# Copy vào: KG_Design/grade6/skills.csv

# Option 2: Tạo thủ công theo format:
# skillId,name,domain,bloomLevel,grade,description
```

**Script Python để tạo TTL:**
```bash
# Hiện tại chưa có script riêng cho skills.ttl
# Có thể dùng export_ttl.py (nhưng cần chỉnh namespace)

# Hoặc tạo thủ công dựa trên skills.csv
```

**Output:** `KG_Design/data/grade6/ttl/skills.ttl`

**Format CSV:**
```csv
skillId,name,domain,bloomLevel,grade,description
K6_A1,Kỹ năng A1,Tin học,Remember,6,...
```

---

### 6. `resources.ttl` - Tài nguyên

**Input:**
- ✅ `KG_Design/grade6/resources.csv`

**Script Python:**
```bash
cd KG_Design/scripts/build
# Có thể dùng export_ttl.py (cần chỉnh namespace)
```

**Output:** `KG_Design/data/grade6/ttl/resources.ttl`

**Format CSV:**
```csv
resId,title,mediaType,url,grade
R001,Tài liệu bài A1,PDF,http://...,6
```

---

## 👥 TẦNG C - ENTITY DATA

### 7. `students_updated.ttl` - Học sinh (Cập nhật)

**Input:**
- ✅ `KG_Design/grade6/student_mastery.csv` (bắt buộc)
- ✅ `students_grade_data.json` (tùy chọn, để bổ sung fullName)

**Cách tạo `student_mastery.csv`:**
```bash
cd KG_Design/scripts/build
python build_student_mastery.py
# Output: KG_Design/grade6/student_mastery.csv
```

**Script Python để tạo TTL:**
```bash
cd KG_Design/scripts/build
python build_missing_ttl.py
```

**Hoặc chạy hàm riêng:**
```python
# Trong build_missing_ttl.py
def export_students_updated():
    """Cập nhật students.ttl với fullName và belongsToClass"""
    # Đọc từ student_mastery.csv
    # Bổ sung fullName từ students_grade_data.json
```

**Output:** `KG_Design/data/grade6/ttl/students_updated.ttl`

**Format CSV (student_mastery.csv):**
```csv
studentId,skillId,score,lastUpdated
HS001,K6_A1,0.75,2024-01-15
```

**Format JSON (students_grade_data.json):**
```json
[
  {
    "student_id": "HS001",
    "name": "Nguyễn Văn A",
    "class": "6/1",
    "year": "2023-2024"
  }
]
```

**Nội dung TTL:**
- ~500 học sinh
- Bao gồm: studentId, fullName, belongsToClass

---

### 8. `questions_updated.ttl` - Câu hỏi (Cập nhật)

**Input:**
- ✅ `KG_Design/grade6/question_skill.csv`

**Cách tạo `question_skill.csv`:**
```bash
# Option 1: Tự động từ câu hỏi
cd KG_Design
python build_inputs_from_existing.py
# Output: KG_Design/generated/question_skill.csv
# Copy vào: KG_Design/grade6/question_skill.csv

# Option 2: Tạo từ Bai_tap_Tin_6/*.csv
# Scan các file CSV trong Bai_tap_Tin_6/
# Extract q_id và topic_id (skill)
```

**Script Python để tạo TTL:**
```bash
cd KG_Design/scripts/build
python build_missing_ttl.py
```

**Hoặc chạy hàm riêng:**
```python
# Trong build_missing_ttl.py
def export_questions_updated():
    """Cập nhật questions.ttl với đầy đủ thuộc tính"""
    # Đọc question_skill.csv
    # Parse lesson ID từ question ID (K6A1_01 -> A1)
    # Tạo requiresSkill và belongsToLesson
```

**Output:** `KG_Design/data/grade6/ttl/questions_updated.ttl`

**Format CSV (question_skill.csv):**
```csv
q_id,skillId
K6A1_01,K6_A1
K6A1_02,K6_A1
```

**Nội dung TTL:**
- ~2000 câu hỏi
- Bao gồm: q_id, requiresSkill, belongsToLesson

---

### 9. `tests.ttl` - Bài kiểm tra

**Input:**
- ✅ `KG_Design/grade6/assessments.csv`

**Script Python để tạo TTL:**
```bash
cd KG_Design/scripts/build
python build_missing_ttl.py
```

**Hoặc chạy hàm riêng:**
```python
# Trong build_missing_ttl.py
def export_tests():
    """Tạo file tests.ttl từ assessments.csv"""
    # Đọc assessments.csv
    # Tạo Test node cho mỗi assessment
```

**Output:** `KG_Design/data/grade6/ttl/tests.ttl`

**Format CSV (assessments.csv):**
```csv
assessId,name,description
K6_KIEM_TRA_1,Kiểm tra 1 HK1,...
```

**Nội dung TTL:**
- ~32 bài kiểm tra (4 HK1 + 4 HK2 cho mỗi khối)
- ~300 triples

---

## 🔗 TẦNG D - RELATIONSHIPS

### 10. `prerequisites.ttl` - Tiên quyết

**Input:**
- ✅ `KG_Design/grade6/prerequisites.csv`

**Cách tạo `prerequisites.csv`:**
```bash
cd KG_Design/scripts/build
python generate_prereq_baseline.py
# Output: KG_Design/grade6/prerequisites.csv
# Tạo quan hệ tiên quyết cơ bản (A1 -> A2 -> A3...)
```

**Script Python để tạo TTL:**
```bash
cd KG_Design/scripts/build
# Có thể dùng export_ttl.py (cần chỉnh namespace)
# Hoặc tạo thủ công từ prerequisites.csv
```

**Output:** `KG_Design/data/grade6/ttl/prerequisites.ttl`

**Format CSV (prerequisites.csv):**
```csv
fromSkillId,toSkillId,relationType,note
K6_A1,K6_A2,PREREQUISITE_OF,baseline auto
```

**Nội dung TTL:**
- Quan hệ Skill → prerequisiteOf → Skill
- ~50 triples

---

### 11. `teachers_assignments.ttl` - Phân công giáo viên

**Input:**
- ✅ `teachers_assign.csv` (ở thư mục gốc dự án)

**Script Python:**
```bash
cd KG_Design/scripts/utils
python export_teachers_assignments.py
```

**Output:** 
- `KG_Design/data/grade6/ttl/teachers_assignments.ttl`

**Format CSV (teachers_assign.csv):**
```csv
Id_teacher,name,expertise,class
T001,Nguyễn Thị A,Tin học,6/1
T001,Nguyễn Thị A,Tin học,6/2
```

**Nội dung TTL:**
- Teacher nodes
- Teacher → teaches → Class
- ~100 triples

---

### 12. `question_skill.ttl` - Câu hỏi - Kỹ năng

**Input:**
- ✅ `KG_Design/grade6/question_skill.csv`

**Script Python:**
```bash
cd KG_Design/scripts/build
# Có thể dùng export_ttl.py (cần chỉnh namespace)
```

**Output:** `KG_Design/data/grade6/ttl/question_skill.ttl`

**Format CSV:**
```csv
q_id,skillId
K6A1_01,K6_A1
```

**Lưu ý:** Quan hệ này có thể đã được tích hợp vào `questions_updated.ttl` qua `requiresSkill`.

---

### 13. `resource_skill.ttl` - Tài nguyên - Kỹ năng

**Input:**
- ✅ `KG_Design/grade6/resource_skill.csv`

**Script Python:**
```bash
cd KG_Design/scripts/build
# Có thể dùng export_ttl.py
```

**Output:** `KG_Design/data/grade6/ttl/resource_skill.ttl`

**Format CSV:**
```csv
resId,skillId,coverage
R001,K6_A1,1.0
```

**Nội dung TTL:**
- Resource → coversSkill → Skill (qua Coverage node)
- ~100 triples

---

### 14. `questions_in_tests.ttl` - Câu hỏi trong đề thi

**Input:**
- ✅ `KG_Design/grade6/questions_in_assessment.csv`

**Script Python:**
```bash
cd KG_Design/scripts/build
python build_missing_ttl.py
```

**Hoặc chạy hàm riêng:**
```python
# Trong build_missing_ttl.py
def export_questions_in_tests():
    """Tạo quan hệ Test -> hasQuestion -> Question"""
    # Đọc questions_in_assessment.csv
    # Tạo Test → hasQuestion → Question
```

**Output:** `KG_Design/data/grade6/ttl/questions_in_tests.ttl`

**Format CSV (questions_in_assessment.csv):**
```csv
assessId,q_id,order
K6_KIEM_TRA_1,K6A1_01,1
K6_KIEM_TRA_1,K6A1_02,2
```

**Nội dung TTL:**
- Test → hasQuestion → Question
- ~500 triples

---

## 📊 TẦNG E - TRANSACTIONS

### 15. `mastery.ttl` - Mức độ thành thạo

**Input:**
- ✅ `KG_Design/grade6/student_mastery.csv`

**Script Python:**
```bash
cd KG_Design/scripts/build
# Có thể tạo trực tiếp từ student_mastery.csv
# Hoặc dùng script riêng (nếu có)
```

**Output:** `KG_Design/data/grade6/ttl/mastery.ttl`

**Format CSV (student_mastery.csv):**
```csv
studentId,skillId,score,lastUpdated
HS001,K6_A1,0.75,2024-01-15
```

**Nội dung TTL:**
- Student → hasMastery → Mastery
- Mastery → forSkill → Skill
- Mastery → score (decimal)
- ~300 triples

---

### 16. `test_results.ttl` - Kết quả kiểm tra

**Input:**
- ✅ `KG_Design/grade6/student_assessment.csv`

**Script Python:**
```bash
cd KG_Design/scripts/build
python build_missing_ttl.py
```

**Hoặc chạy hàm riêng:**
```python
# Trong build_missing_ttl.py
def export_test_results():
    """Tạo file test_results.ttl từ student_assessment.csv"""
    # Đọc student_assessment.csv
    # Tạo TestResult node
    # Student → hasResult → TestResult
    # Student → takeTest → Test
    # TestResult → forTest → Test
```

**Output:** `KG_Design/data/grade6/ttl/test_results.ttl`

**Format CSV (student_assessment.csv):**
```csv
studentId,assessId,score,date
HS001,K6_KIEM_TRA_1,8.5,2024-01-15
```

**Nội dung TTL:**
- ~500 kết quả kiểm tra
- Bao gồm: TestResult, score, testDate, quan hệ với Student và Test

---

## 🚀 QUY TRÌNH TỔNG THỂ

### Bước 1: Chuẩn bị dữ liệu CSV

```bash
# 1. Tạo skills.csv và question_skill.csv
cd KG_Design
python build_inputs_from_existing.py

# 2. Tạo student_mastery.csv
cd scripts/build
python build_student_mastery.py

# 3. Tạo prerequisites.csv (baseline)
python generate_prereq_baseline.py

# 4. Export teachers_assignments.ttl
cd utils
python export_teachers_assignments.py
```

### Bước 2: Tạo tất cả file TTL

```bash
# Chạy script chính
cd KG_Design/scripts/build
python build_missing_ttl.py
```

**Script này sẽ tạo:**
- ✅ `grades.ttl`
- ✅ `topics.ttl`
- ✅ `lessons.ttl`
- ✅ `classes.ttl`
- ✅ `students_updated.ttl`
- ✅ `questions_updated.ttl`
- ✅ `tests.ttl`
- ✅ `test_results.ttl`
- ✅ `questions_in_tests.ttl`

### Bước 3: Tạo các file còn lại (thủ công hoặc script)

```bash
# skills.ttl - Cần chỉnh từ skills.csv
# resources.ttl - Cần chỉnh từ resources.csv
# prerequisites.ttl - Cần chỉnh từ prerequisites.csv
# question_skill.ttl - Có thể bỏ qua (đã có trong questions_updated.ttl)
# resource_skill.ttl - Cần chỉnh từ resource_skill.csv
# mastery.ttl - Cần chỉnh từ student_mastery.csv
```

### Bước 4: Upload vào GraphDB

Xem file: `HUONG_DAN_UPLOAD_GRAPHDB_PHAN_TANG.md`

---

## 📋 CHECKLIST

### Chuẩn bị dữ liệu:
- [ ] `KG_Design/grade6/skills.csv`
- [ ] `KG_Design/grade6/question_skill.csv`
- [ ] `KG_Design/grade6/student_mastery.csv`
- [ ] `KG_Design/grade6/assessments.csv`
- [ ] `KG_Design/grade6/student_assessment.csv`
- [ ] `KG_Design/grade6/questions_in_assessment.csv`
- [ ] `KG_Design/grade6/prerequisites.csv`
- [ ] `KG_Design/grade6/resources.csv` (nếu có)
- [ ] `KG_Design/grade6/resource_skill.csv` (nếu có)
- [ ] `teachers_assign.csv` (ở thư mục gốc)
- [ ] `students_grade_data.json` (tùy chọn, ở thư mục gốc)

### Tạo file TTL:
- [ ] `schema/kg_schema_chuan.ttl` (đã có sẵn)
- [ ] `grades.ttl`
- [ ] `topics.ttl`
- [ ] `lessons.ttl`
- [ ] `classes.ttl`
- [ ] `skills.ttl`
- [ ] `resources.ttl`
- [ ] `students_updated.ttl`
- [ ] `questions_updated.ttl`
- [ ] `tests.ttl`
- [ ] `prerequisites.ttl`
- [ ] `teachers_assignments.ttl`
- [ ] `question_skill.ttl` (hoặc bỏ qua)
- [ ] `resource_skill.ttl`
- [ ] `questions_in_tests.ttl`
- [ ] `mastery.ttl`
- [ ] `test_results.ttl`

---

## 🐛 XỬ LÝ LỖI

### Lỗi: "File not found"
- Kiểm tra đường dẫn file CSV
- Đảm bảo đã chạy script tạo CSV trước

### Lỗi: "Empty file"
- Kiểm tra file CSV có dữ liệu không
- Kiểm tra format CSV có đúng không

### Lỗi: "Invalid namespace"
- Script `build_missing_ttl.py` dùng namespace chuẩn
- Các script khác có thể dùng namespace khác, cần chỉnh lại

---

## 📚 TÀI LIỆU LIÊN QUAN

- `HUONG_DAN_BUILD_TTL.md` - Hướng dẫn sử dụng script
- `HUONG_DAN_UPLOAD_GRAPHDB_PHAN_TANG.md` - Hướng dẫn upload
- `BANG_PHAN_TANG_TTL.md` - Bảng phân tầng

---

**Cập nhật:** 2025-01-15

