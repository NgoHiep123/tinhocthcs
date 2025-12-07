# 📊 HƯỚNG DẪN UPLOAD TTL VÀO GRAPHDB - PHÂN TẦNG

## 🎯 Nguyên Tắc Phân Tầng

Upload theo thứ tự từ **TẦNG CƠ BẢN → TẦNG CAO CẤP** để tránh lỗi thiếu reference.

---

## 📋 PHÂN TẦNG CHI TIẾT

### 🏛️ **TẦNG A - SCHEMA (Ontology)**
**Mục đích:** Định nghĩa các class, property, structure của Knowledge Graph

#### Upload đầu tiên:
```
1. KG_Design/schema/kg_schema_chuan.ttl
```

**Lý do:** File này chứa:
- Định nghĩa các Class (Student, Teacher, Lesson, Topic, Skill, Question, Test...)
- Định nghĩa các Property (hasName, belongsToClass, hasScore...)
- Constraints và rules
- Phải có trước khi import data

**Cách upload:**
1. Mở GraphDB Desktop
2. Chọn repository
3. Import → `kg_schema_chuan.ttl`
4. Chờ hoàn thành

---

### 📚 **TẦNG B - MASTER DATA (Dữ liệu tham chiếu cơ bản)**
**Mục đích:** Dữ liệu được các entity khác tham chiếu đến

#### Upload theo thứ tự:

```
2. KG_Design/data/grade6/ttl/grades.ttl          # Lớp học (Grade 6, 7, 8, 9)
3. KG_Design/data/grade6/ttl/classes.ttl         # Các lớp (6A, 6B, 6C...)
4. KG_Design/data/grade6/ttl/topics.ttl          # Chủ đề (Topic A, B, C...)
5. KG_Design/data/grade6/ttl/skills.ttl          # Kỹ năng
6. KG_Design/data/grade6/ttl/lessons.ttl         # Bài học (A1, A2, B1...)
7. KG_Design/data/grade6/ttl/resources.ttl       # Tài nguyên học tập
```

**Lý do:**
- `grades` → Được `classes` tham chiếu
- `classes` → Được `students`, `teachers` tham chiếu
- `topics` → Được `lessons` tham chiếu
- `skills` → Được `lessons`, `questions` tham chiếu
- `lessons` → Được `prerequisites`, `questions` tham chiếu
- `resources` → Được `resource_skill` tham chiếu

---

### 👥 **TẦNG C - ENTITY DATA (Dữ liệu thực thể)**
**Mục đích:** Dữ liệu người dùng và câu hỏi

#### Upload theo thứ tự:

```
8. KG_Design/data/grade6/ttl/students.ttl        # Học sinh (hoặc students_updated.ttl)
9. KG_Design/data/grade6/ttl/questions_updated.ttl  # Câu hỏi
10. KG_Design/data/grade6/ttl/tests.ttl          # Bài kiểm tra
```

**Lưu ý:**
- Chọn **students.ttl** HOẶC **students_updated.ttl** (không cần cả 2)
- Nếu có file `_updated`, ưu tiên dùng file đó

**Lý do:**
- `students` → Tham chiếu đến `classes`
- `questions` → Tham chiếu đến `lessons`, `skills`
- `tests` → Tham chiếu đến `lessons`, `topics`

---

### 🔗 **TẦNG D - RELATIONSHIP DATA (Quan hệ)**
**Mục đích:** Quan hệ giữa các entities

#### Upload theo thứ tự:

```
11. KG_Design/data/grade6/ttl/prerequisites.ttl      # Quan hệ tiên quyết giữa các lesson
12. KG_Design/data/grade6/ttl/teachers_assignments.ttl  # Phân công giáo viên
13. KG_Design/data/grade6/ttl/question_skill.ttl     # Quan hệ câu hỏi - kỹ năng
14. KG_Design/data/grade6/ttl/resource_skill.ttl     # Quan hệ tài nguyên - kỹ năng
15. KG_Design/data/grade6/ttl/questions_in_tests.ttl # Câu hỏi trong bài test
```

**Lý do:**
- Các file này định nghĩa mối quan hệ giữa entities đã tồn tại
- Phải import entities trước

---

### 📊 **TẦNG E - TRANSACTION DATA (Dữ liệu giao dịch)**
**Mục đích:** Kết quả, điểm số, mastery

#### Upload cuối cùng:

```
16. KG_Design/data/grade6/ttl/mastery.ttl        # Mức độ thành thạo
17. KG_Design/data/grade6/ttl/test_results.ttl   # Kết quả bài test
```

**Lý do:**
- Dữ liệu này phụ thuộc vào tất cả các tầng trên
- `mastery` → Tham chiếu `students`, `skills`, `lessons`
- `test_results` → Tham chiếu `students`, `tests`, `questions`

---

## 📝 TÓM TẮT THỨ TỰ UPLOAD

### ✅ Checklist Upload:

```
TẦNG A - SCHEMA
□ 1. kg_schema_chuan.ttl

TẦNG B - MASTER DATA
□ 2. grades.ttl
□ 3. classes.ttl
□ 4. topics.ttl
□ 5. skills.ttl
□ 6. lessons.ttl
□ 7. resources.ttl

TẦNG C - ENTITY DATA
□ 8. students.ttl (hoặc students_updated.ttl)
□ 9. questions_updated.ttl
□ 10. tests.ttl

TẦNG D - RELATIONSHIP DATA
□ 11. prerequisites.ttl
□ 12. teachers_assignments.ttl
□ 13. question_skill.ttl
□ 14. resource_skill.ttl
□ 15. questions_in_tests.ttl

TẦNG E - TRANSACTION DATA
□ 16. mastery.ttl
□ 17. test_results.ttl
```

---

## 🚀 HƯỚNG DẪN UPLOAD TRONG GRAPHDB DESKTOP

### Bước 1: Tạo Repository
```
1. Mở GraphDB Desktop
2. Setup → Repositories
3. Create new repository
4. Repository ID: "tin_hoc_thcs"
5. Ruleset: "RDFS-Plus" hoặc "OWL-Horst"
6. Create
```

### Bước 2: Upload Schema (Tầng A)
```
1. Chọn repository "tin_hoc_thcs"
2. Import → RDF
3. Upload RDF files
4. Chọn: KG_Design/schema/kg_schema_chuan.ttl
5. Import
6. Đợi hoàn thành
```

### Bước 3: Upload Master Data (Tầng B)
```
Lặp lại với từng file theo thứ tự:
- grades.ttl
- classes.ttl
- topics.ttl
- skills.ttl
- lessons.ttl
- resources.ttl

Mỗi file:
1. Import → RDF
2. Upload file
3. Import
4. Đợi hoàn thành
```

### Bước 4: Upload Entity Data (Tầng C)
```
Tiếp tục với:
- students.ttl (hoặc students_updated.ttl)
- questions_updated.ttl
- tests.ttl
```

### Bước 5: Upload Relationship Data (Tầng D)
```
Tiếp tục với:
- prerequisites.ttl
- teachers_assignments.ttl
- question_skill.ttl
- resource_skill.ttl
- questions_in_tests.ttl
```

### Bước 6: Upload Transaction Data (Tầng E)
```
Cuối cùng:
- mastery.ttl
- test_results.ttl
```

---

## ✅ KIỂM TRA SAU KHI UPLOAD

### 1. Kiểm tra số lượng triples:
```sparql
SELECT (COUNT(*) as ?count) 
WHERE {
  ?s ?p ?o
}
```

### 2. Kiểm tra các Class:
```sparql
SELECT DISTINCT ?class (COUNT(?instance) as ?count)
WHERE {
  ?instance a ?class
}
GROUP BY ?class
ORDER BY DESC(?count)
```

### 3. Kiểm tra Students:
```sparql
PREFIX ex: <http://example.org/tin_hoc#>
SELECT ?student ?name ?class
WHERE {
  ?student a ex:Student ;
           ex:hasName ?name ;
           ex:belongsToClass ?classIRI .
  ?classIRI ex:hasName ?class .
}
LIMIT 10
```

### 4. Kiểm tra Lessons:
```sparql
PREFIX ex: <http://example.org/tin_hoc#>
SELECT ?lesson ?name ?topic
WHERE {
  ?lesson a ex:Lesson ;
          ex:hasName ?name ;
          ex:belongsToTopic ?topicIRI .
  ?topicIRI ex:hasName ?topic .
}
LIMIT 10
```

### 5. Kiểm tra Questions:
```sparql
PREFIX ex: <http://example.org/tin_hoc#>
SELECT ?question ?text ?lesson
WHERE {
  ?question a ex:Question ;
            ex:hasQuestionText ?text ;
            ex:belongsToLesson ?lessonIRI .
  ?lessonIRI ex:hasName ?lesson .
}
LIMIT 10
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

### ❗ Nếu gặp lỗi:

#### 1. **Lỗi "Undefined property"**
→ Chưa upload schema (`kg_schema_chuan.ttl`)
→ **Giải pháp:** Upload schema trước

#### 2. **Lỗi "Undefined class"**
→ Chưa upload schema
→ **Giải pháp:** Upload schema trước

#### 3. **Lỗi "Referenced entity not found"**
→ Upload sai thứ tự
→ **Giải pháp:** 
   - Xóa repository
   - Tạo lại
   - Upload lại từ đầu theo đúng thứ tự

#### 4. **File quá lớn**
→ GraphDB Desktop có giới hạn
→ **Giải pháp:**
   - Chia nhỏ file
   - Hoặc dùng GraphDB Server (không giới hạn)

#### 5. **Encoding error**
→ File không phải UTF-8
→ **Giải pháp:**
   - Convert file sang UTF-8
   - Hoặc chỉnh Base IRI khi import

---

## 🔄 UPLOAD LẠI (Re-import)

### Nếu cần update dữ liệu:

#### Option 1: Clear và Upload lại
```
1. Repository → Clear repository
2. Upload lại tất cả file theo thứ tự
```

#### Option 2: Update từng file
```
1. Xóa triples cũ của file đó
2. Upload file mới
```

#### SPARQL để xóa triples của một graph:
```sparql
CLEAR GRAPH <http://example.org/graph_name>
```

---

## 📊 KẾT QUẢ MONG ĐỢI

Sau khi upload xong tất cả:

```
✅ Schema: 1 file (kg_schema_chuan.ttl)
✅ Master Data: 6 files
✅ Entity Data: 3 files
✅ Relationship Data: 5 files
✅ Transaction Data: 2 files

Tổng: 17 files TTL
```

### Số lượng triples ước tính:
- Schema: ~500 triples
- Grades: ~10 triples
- Classes: ~50 triples
- Topics: ~20 triples
- Skills: ~100 triples
- Lessons: ~150 triples
- Resources: ~100 triples
- Students: ~500 triples (tùy số học sinh)
- Questions: ~2000 triples
- Tests: ~300 triples
- Relationships: ~1000 triples
- Results: ~500 triples

**Tổng ước tính: ~5,000 - 10,000 triples**

---

## 🎯 TIPS & TRICKS

1. **Upload từng file một** - Dễ debug nếu có lỗi
2. **Check count sau mỗi file** - Đảm bảo import thành công
3. **Backup repository** - Trước khi upload lớn
4. **Use named graphs** - Để dễ quản lý và xóa
5. **Monitor memory** - GraphDB Desktop có giới hạn RAM

---

## 📞 TROUBLESHOOTING

### Nếu GraphDB Desktop chậm:
- Giảm heap size
- Upload ít file hơn mỗi lần
- Restart GraphDB sau mỗi vài file

### Nếu cần upload nhiều repository:
- Tạo repository riêng cho mỗi khối (K6, K7, K8, K9)
- Hoặc dùng named graphs

---

**Chúc bạn upload thành công! 🎉**

*Last updated: 2025-12-05*

