# 📊 BẢNG PHÂN TẦNG FILE TTL - UPLOAD VÀO GRAPHDB

## 🎯 BẢNG TÓM TẮT NHANH

| # | Tầng | File TTL | Mô Tả | Dependencies | Triples |
|---|------|----------|-------|--------------|---------|
| **1** | **A** | `schema/kg_schema_chuan.ttl` | 🏛️ Ontology - Schema | ❌ KHÔNG | ~500 |
| | | | | | |
| **2** | **B** | `data/grade6/ttl/grades.ttl` | 📚 Khối lớp | Schema | ~10 |
| **3** | **B** | `data/grade6/ttl/classes.ttl` | 📚 Lớp học | grades | ~50 |
| **4** | **B** | `data/grade6/ttl/topics.ttl` | 📚 Chủ đề | Schema | ~20 |
| **5** | **B** | `data/grade6/ttl/skills.ttl` | 📚 Kỹ năng | Schema | ~100 |
| **6** | **B** | `data/grade6/ttl/lessons.ttl` | 📚 Bài học | topics | ~150 |
| **7** | **B** | `data/grade6/ttl/resources.ttl` | 📚 Tài nguyên | Schema | ~100 |
| | | | | | |
| **8** | **C** | `data/grade6/ttl/students.ttl` | 👥 Học sinh | classes | ~500 |
| **9** | **C** | `data/grade6/ttl/questions_updated.ttl` | 👥 Câu hỏi | lessons, skills | ~2000 |
| **10** | **C** | `data/grade6/ttl/tests.ttl` | 👥 Bài kiểm tra | lessons, topics | ~300 |
| | | | | | |
| **11** | **D** | `data/grade6/ttl/prerequisites.ttl` | 🔗 Tiên quyết | lessons | ~50 |
| **12** | **D** | `data/grade6/ttl/teachers_assignments.ttl` | 🔗 Phân công GV | classes | ~100 |
| **13** | **D** | `data/grade6/ttl/question_skill.ttl` | 🔗 Câu hỏi-KN | questions, skills | ~200 |
| **14** | **D** | `data/grade6/ttl/resource_skill.ttl` | 🔗 Tài nguyên-KN | resources, skills | ~100 |
| **15** | **D** | `data/grade6/ttl/questions_in_tests.ttl` | 🔗 CH-Test | questions, tests | ~500 |
| | | | | | |
| **16** | **E** | `data/grade6/ttl/mastery.ttl` | 📊 Mastery | students, skills | ~300 |
| **17** | **E** | `data/grade6/ttl/test_results.ttl` | 📊 Kết quả | students, tests | ~500 |

**Tổng ước tính:** ~5,000 - 10,000 triples

---

## 📋 PHÂN TẦNG CHI TIẾT

### 🏛️ **TẦNG A - SCHEMA** (Upload đầu tiên)

| File | Vai Trò | Tại Sao Phải Đầu Tiên? |
|------|---------|------------------------|
| `kg_schema_chuan.ttl` | Định nghĩa Class, Property, Rules | Tất cả các file khác cần schema này để validate |

**⚠️ QUAN TRỌNG:** File này PHẢI upload đầu tiên!

---

### 📚 **TẦNG B - MASTER DATA** (Dữ liệu cơ bản)

| # | File | Entities | Tại Sao Upload Trước? |
|---|------|----------|----------------------|
| 2 | `grades.ttl` | Grade 6, 7, 8, 9 | classes cần reference |
| 3 | `classes.ttl` | 6A, 6B, 6C... | students, teachers cần reference |
| 4 | `topics.ttl` | Topic A, B, C... | lessons cần reference |
| 5 | `skills.ttl` | Kỹ năng học tập | questions, mastery cần reference |
| 6 | `lessons.ttl` | A1, A2, B1... | prerequisites, questions cần reference |
| 7 | `resources.ttl` | Tài liệu, video... | resource_skill cần reference |

**Đặc điểm:**
- Dữ liệu ổn định, ít thay đổi
- Được nhiều entity khác tham chiếu
- Phải có trước khi import entity data

---

### 👥 **TẦNG C - ENTITY DATA** (Thực thể chính)

| # | File | Entities | Dependencies |
|---|------|----------|--------------|
| 8 | `students.ttl` | Học sinh | → classes.ttl |
| 9 | `questions_updated.ttl` | Câu hỏi | → lessons.ttl, skills.ttl |
| 10 | `tests.ttl` | Bài kiểm tra | → lessons.ttl, topics.ttl |

**Lưu ý:**
- Chọn `students.ttl` **HOẶC** `students_updated.ttl` (file nào mới hơn)
- `questions_updated.ttl` thay cho `questions.ttl`

---

### 🔗 **TẦNG D - RELATIONSHIP DATA** (Quan hệ)

| # | File | Quan Hệ | Liên Kết | Dependencies |
|---|------|---------|----------|--------------|
| 11 | `prerequisites.ttl` | Lesson → Lesson | Tiên quyết | lessons.ttl |
| 12 | `teachers_assignments.ttl` | Teacher → Class | Phân công | classes.ttl |
| 13 | `question_skill.ttl` | Question → Skill | CH-KN | questions, skills |
| 14 | `resource_skill.ttl` | Resource → Skill | TL-KN | resources, skills |
| 15 | `questions_in_tests.ttl` | Test → Question | Test-CH | tests, questions |

**Đặc điểm:**
- Định nghĩa mối quan hệ giữa entities
- Cả 2 đầu của quan hệ phải đã tồn tại
- Không thể upload trước entities

---

### 📊 **TẦNG E - TRANSACTION DATA** (Dữ liệu giao dịch)

| # | File | Dữ Liệu | Dependencies | Đặc Điểm |
|---|------|---------|--------------|----------|
| 16 | `mastery.ttl` | Mastery level | students, skills, lessons | Thay đổi thường xuyên |
| 17 | `test_results.ttl` | Kết quả test | students, tests, questions | Tăng dần theo thời gian |

**Đặc điểm:**
- Dữ liệu giao dịch, thay đổi liên tục
- Phụ thuộc vào tất cả các tầng trên
- Upload cuối cùng

---

## 🎯 MA TRẬN DEPENDENCIES

```
┌─────────────────────┐
│   SCHEMA (A)        │ ← Không phụ thuộc gì
│  kg_schema_chuan    │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────────────────────────────┐
│        MASTER DATA (B)                      │
├──────────┬──────────┬──────────┬───────────┤
│ grades   │ classes  │ topics   │ skills    │
│          │          │          │           │
│ lessons  │ resources│          │           │
└──┬───────┴──────┬───┴────┬─────┴───────────┘
   │              │        │
   ↓              ↓        ↓
┌──────────────────────────────────┐
│      ENTITY DATA (C)             │
├──────────┬──────────┬────────────┤
│ students │ questions│ tests      │
└────┬─────┴─────┬────┴─────┬──────┘
     │           │          │
     ↓           ↓          ↓
┌─────────────────────────────────────────┐
│     RELATIONSHIP DATA (D)               │
├──────────┬────────────┬─────────────────┤
│prerequis │teachers_   │question_skill   │
│ites      │assignments │resource_skill   │
│          │            │questions_in_tests│
└────┬─────┴─────┬──────┴─────┬───────────┘
     │           │            │
     └───────────┴────────────┘
                 │
                 ↓
┌────────────────────────────────┐
│   TRANSACTION DATA (E)         │
├──────────┬─────────────────────┤
│ mastery  │ test_results        │
└──────────┴─────────────────────┘
```

---

## ⚠️ CÁC LỖI THƯỜNG GẶP

| Lỗi | Nguyên Nhân | Giải Pháp |
|-----|-------------|-----------|
| **Undefined property** | Chưa upload schema | Upload `kg_schema_chuan.ttl` trước |
| **Undefined class** | Chưa upload schema | Upload `kg_schema_chuan.ttl` trước |
| **Referenced entity not found** | Upload sai thứ tự | Xóa repo, upload lại từ đầu |
| **Duplicate entity** | Upload file 2 lần | Clear graph, upload lại |
| **Out of memory** | File quá lớn | Chia nhỏ file hoặc tăng heap |

---

## ✅ QUY TẮC VÀNG

1. **LUÔN** upload schema đầu tiên
2. **KHÔNG** bỏ qua bất kỳ file nào
3. **KHÔNG** đảo thứ tự upload
4. **KIỂM TRA** count sau mỗi file
5. **BACKUP** trước khi upload nhiều

---

## 📊 TIẾN TRÌNH UPLOAD

```
Start
  │
  ├─► [1] Upload Schema ──────────────► Check ✓
  │
  ├─► [2-7] Upload Master Data ──────► Check ✓
  │
  ├─► [8-10] Upload Entity Data ─────► Check ✓
  │
  ├─► [11-15] Upload Relationships ──► Check ✓
  │
  └─► [16-17] Upload Transactions ───► Check ✓
       │
       └─► HOÀN THÀNH! 🎉
```

---

## 🎯 CHECKLIST NHANH

```
□ Tầng A (1 file)   → Schema
□ Tầng B (6 files)  → Master Data  
□ Tầng C (3 files)  → Entity Data
□ Tầng D (5 files)  → Relationships
□ Tầng E (2 files)  → Transactions

Total: 17 files
```

---

**Hãy in bảng này ra và check từng file khi upload! ✅**

