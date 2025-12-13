# ⚡ QUY TRÌNH BUILD TTL - TÓM TẮT NHANH

> Quick reference guide - Xây dựng file TTL từng tầng

---

## 🎯 QUY TRÌNH TỔNG QUAN

```bash
# BƯỚC 0: KIỂM TRA DỮ LIỆU CSV (KHUYẾN NGHỊ)
cd KG_Design/scripts/build
python check_csv_data.py                      # Kiểm tra tất cả file CSV

# BƯỚC 1: Chuẩn bị dữ liệu CSV
cd ../../..                                   # Về thư mục gốc KG_Design
python build_inputs_from_existing.py          # Tạo skills.csv, question_skill.csv

cd scripts/build
python build_student_mastery.py               # Tạo student_mastery.csv
python generate_prereq_baseline.py            # Tạo prerequisites.csv

cd ../utils
python export_teachers_assignments.py         # Tạo teachers_assignments.ttl

# BƯỚC 2: KIỂM TRA LẠI (Sau khi tạo CSV)
cd ../build
python check_csv_data.py                      # Kiểm tra lại

# BƯỚC 3: Tạo tất cả file TTL
python build_missing_ttl.py                   # Tạo 9 file TTL chính

# BƯỚC 4: Upload vào GraphDB
# Xem: HUONG_DAN_UPLOAD_GRAPHDB_PHAN_TANG.md
```

---

## 📋 BẢNG TÓM TẮT: FILE TTL → INPUT → SCRIPT

| # | Tầng | File TTL | File Input | Script Python |
|---|------|----------|------------|---------------|
| 1 | A | `schema/kg_schema_chuan.ttl` | ❌ Không cần | ❌ Không cần (đã có sẵn) |
| | | | | |
| 2 | B | `grades.ttl` | ❌ Không cần | `build_missing_ttl.py` → `export_grades()` |
| 3 | B | `topics.ttl` | ❌ Không cần | `build_missing_ttl.py` → `export_topics()` |
| 4 | B | `lessons.ttl` | ❌ Không cần | `build_missing_ttl.py` → `export_lessons()` |
| 5 | B | `classes.ttl` | `classes.csv` (tùy chọn) | `build_missing_ttl.py` → `export_classes()` |
| 6 | B | `skills.ttl` | `grade6/skills.csv` | Manual hoặc `export_ttl.py` |
| 7 | B | `resources.ttl` | `grade6/resources.csv` | Manual hoặc `export_ttl.py` |
| | | | | |
| 8 | C | `students_updated.ttl` | `grade6/student_mastery.csv`<br>`students_grade_data.json` | `build_missing_ttl.py` → `export_students_updated()` |
| 9 | C | `questions_updated.ttl` | `grade6/question_skill.csv` | `build_missing_ttl.py` → `export_questions_updated()` |
| 10 | C | `tests.ttl` | `grade6/assessments.csv` | `build_missing_ttl.py` → `export_tests()` |
| | | | | |
| 11 | D | `prerequisites.ttl` | `grade6/prerequisites.csv` | Manual hoặc `export_ttl.py` |
| 12 | D | `teachers_assignments.ttl` | `teachers_assign.csv` | `export_teachers_assignments.py` |
| 13 | D | `question_skill.ttl` | `grade6/question_skill.csv` | Manual (có thể bỏ qua) |
| 14 | D | `resource_skill.ttl` | `grade6/resource_skill.csv` | Manual hoặc `export_ttl.py` |
| 15 | D | `questions_in_tests.ttl` | `grade6/questions_in_assessment.csv` | `build_missing_ttl.py` → `export_questions_in_tests()` |
| | | | | |
| 16 | E | `mastery.ttl` | `grade6/student_mastery.csv` | Manual |
| 17 | E | `test_results.ttl` | `grade6/student_assessment.csv` | `build_missing_ttl.py` → `export_test_results()` |

---

## 🚀 LỆNH CHẠY NHANH

### 1. Tạo tất cả file CSV cần thiết:

```bash
# Từ thư mục gốc dự án
cd KG_Design
python build_inputs_from_existing.py
# → Tạo: generated/skills.csv, generated/question_skill.csv
# Copy vào: grade6/skills.csv, grade6/question_skill.csv

cd scripts/build
python build_student_mastery.py
# → Tạo: grade6/student_mastery.csv

python generate_prereq_baseline.py
# → Tạo: grade6/prerequisites.csv

cd ../utils
python export_teachers_assignments.py
# → Tạo: data/grade6/ttl/teachers_assignments.ttl
```

### 2. Tạo tất cả file TTL:

```bash
cd KG_Design/scripts/build
python build_missing_ttl.py
# → Tạo 9 file TTL trong data/grade6/ttl/
```

**Output:**
- ✅ `grades.ttl`
- ✅ `topics.ttl`
- ✅ `lessons.ttl`
- ✅ `classes.ttl`
- ✅ `students_updated.ttl`
- ✅ `questions_updated.ttl`
- ✅ `tests.ttl`
- ✅ `test_results.ttl`
- ✅ `questions_in_tests.ttl`

### 3. Tạo các file TTL còn lại (thủ công):

```bash
# Các file này cần tạo thủ công hoặc chỉnh từ CSV:
# - skills.ttl (từ skills.csv)
# - resources.ttl (từ resources.csv)
# - prerequisites.ttl (từ prerequisites.csv)
# - resource_skill.ttl (từ resource_skill.csv)
# - mastery.ttl (từ student_mastery.csv)
```

---

## 📂 CẤU TRÚC THƯ MỤC

```
KG_Design/
├── schema/
│   └── kg_schema_chuan.ttl          ← Tầng A (đã có sẵn)
│
├── grade6/                          ← Thư mục chứa CSV input
│   ├── skills.csv
│   ├── question_skill.csv
│   ├── student_mastery.csv
│   ├── assessments.csv
│   ├── student_assessment.csv
│   ├── questions_in_assessment.csv
│   ├── prerequisites.csv
│   ├── resources.csv
│   └── resource_skill.csv
│
├── data/grade6/ttl/                 ← Thư mục chứa TTL output
│   ├── grades.ttl                   ← Tầng B
│   ├── topics.ttl
│   ├── lessons.ttl
│   ├── classes.ttl
│   ├── skills.ttl
│   ├── resources.ttl
│   │
│   ├── students_updated.ttl         ← Tầng C
│   ├── questions_updated.ttl
│   ├── tests.ttl
│   │
│   ├── prerequisites.ttl            ← Tầng D
│   ├── teachers_assignments.ttl
│   ├── question_skill.ttl
│   ├── resource_skill.ttl
│   ├── questions_in_tests.ttl
│   │
│   ├── mastery.ttl                  ← Tầng E
│   └── test_results.ttl
│
└── scripts/
    ├── build/
    │   ├── build_missing_ttl.py     ← Script chính
    │   ├── build_student_mastery.py
    │   └── generate_prereq_baseline.py
    └── utils/
        └── export_teachers_assignments.py
```

---

## ✅ CHECKLIST NHANH

### Trước khi build:
- [ ] Đã chạy `check_csv_data.py` để kiểm tra dữ liệu
- [ ] Đã có file CSV trong `KG_Design/grade6/`
- [ ] Đã chạy `build_inputs_from_existing.py` (nếu cần)
- [ ] Đã chạy `build_student_mastery.py`
- [ ] Đã chạy `export_teachers_assignments.py`
- [ ] Đã chạy lại `check_csv_data.py` để xác nhận không còn lỗi

### Sau khi build:
- [ ] Đã chạy `build_missing_ttl.py`
- [ ] Kiểm tra 9 file TTL đã được tạo trong `data/grade6/ttl/`
- [ ] Tạo các file TTL còn lại (thủ công)
- [ ] Kiểm tra format TTL (namespace, IRI)

### Trước khi upload:
- [ ] Tất cả 17 file TTL đã có
- [ ] Schema đã có sẵn (`kg_schema_chuan.ttl`)
- [ ] Upload theo đúng thứ tự (A → B → C → D → E)

---

## 🔍 XEM CHI TIẾT

- **Hướng dẫn chi tiết:** `docs/QUY_TRINH_XAY_DUNG_TTL_TUNG_TANG.md`
- **Script kiểm tra CSV:** `scripts/build/check_csv_data.py`

### Chạy kiểm tra CSV:

```bash
# Windows
cd KG_Design/scripts/build
check_csv_data.bat

# Linux/Mac hoặc Python
python check_csv_data.py
```

---

**Cập nhật:** 2025-01-15

