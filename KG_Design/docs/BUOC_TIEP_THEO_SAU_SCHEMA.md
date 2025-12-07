# 🚀 BƯỚC TIẾP THEO SAU KHI UPLOAD SCHEMA

## ✅ BẠN ĐÃ HOÀN THÀNH

- ✅ Tạo repository: `tinhocthcs`
- ✅ Upload schema: `kg_schema_chuan.ttl`

---

## 🔍 BƯỚC 1: KIỂM TRA SCHEMA ĐÃ UPLOAD ĐÚNG

### 1.1. Kiểm tra số lượng triples

**Query:**
```sparql
SELECT (COUNT(*) as ?count) 
WHERE {
  ?s ?p ?o
}
```

**Kỳ vọng:** ~500 triples (schema có khoảng 500 dòng định nghĩa)

---

### 1.2. Kiểm tra các Classes đã được định nghĩa

**Query:**
```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?class ?label ?comment
WHERE {
  ?class a rdfs:Class ;
         rdfs:label ?label .
  OPTIONAL { ?class rdfs:comment ?comment }
  FILTER(STRSTARTS(STR(?class), "http://education.vn/ontology#"))
}
ORDER BY ?label
```

**Kỳ vọng:** Thấy 12 classes:
- Student (Học sinh)
- Teacher (Giáo viên)
- Class (Lớp học)
- Grade (Khối)
- Topic (Chủ đề)
- Lesson (Bài học)
- Question (Câu hỏi)
- Skill (Kỹ năng)
- Resource (Tài nguyên)
- Test (Bài kiểm tra)
- TestResult (Kết quả)
- Mastery (Mức độ thành thạo)

---

### 1.3. Kiểm tra các Properties đã được định nghĩa

**Query:**
```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?property ?label ?comment
WHERE {
  ?property a rdf:Property ;
            rdfs:label ?label .
  OPTIONAL { ?property rdfs:comment ?comment }
  FILTER(STRSTARTS(STR(?property), "http://education.vn/ontology#"))
}
ORDER BY ?label
```

**Kỳ vọng:** Thấy 25+ properties (belongsToClass, fullName, score, etc.)

---

### 1.4. Kiểm tra Relationships (Object Properties)

**Query:**
```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?property ?label ?domain ?range
WHERE {
  ?property a rdf:Property ;
            rdfs:label ?label ;
            rdfs:domain ?domain ;
            rdfs:range ?range .
  FILTER(STRSTARTS(STR(?property), "http://education.vn/ontology#"))
  FILTER(STRSTARTS(STR(?range), "http://education.vn/ontology#"))
}
ORDER BY ?label
```

**Kỳ vọng:** Thấy các relationships như:
- belongsToClass (Student → Class)
- belongsToGrade (Class → Grade)
- teaches (Teacher → Class)
- belongsToTopic (Lesson → Topic)
- etc.

---

## 📊 BƯỚC 2: UPLOAD DỮ LIỆU THEO PHÂN TẦNG

Sau khi kiểm tra schema OK, tiếp tục upload dữ liệu theo thứ tự:

### **TẦNG B - MASTER DATA** (Upload tiếp theo)

Upload theo thứ tự:

```
1. data/grade6/ttl/grades.ttl          ← Bắt đầu từ đây
2. data/grade6/ttl/classes.ttl
3. data/grade6/ttl/topics.ttl
4. data/grade6/ttl/skills.ttl
5. data/grade6/ttl/lessons.ttl
6. data/grade6/ttl/resources.ttl
```

**Cách upload:**
1. GraphDB Desktop → Chọn repository `tinhocthcs`
2. Import → RDF → Upload RDF files
3. Chọn file `grades.ttl`
4. Click Import
5. Đợi hoàn thành
6. Lặp lại với file tiếp theo

---

### **Sau mỗi file, kiểm tra:**

**Query kiểm tra Grades:**
```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?grade ?gradeNumber
WHERE {
  ?grade a edu:Grade ;
         edu:grade ?gradeNumber
}
ORDER BY ?gradeNumber
```

**Kỳ vọng:** Thấy Grade 6, 7, 8, 9

---

**Query kiểm tra Classes:**
```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?class ?className ?grade
WHERE {
  ?class a edu:Class ;
         edu:className ?className ;
         edu:belongsToGrade ?gradeIRI .
  ?gradeIRI edu:grade ?grade
}
ORDER BY ?grade ?className
```

**Kỳ vọng:** Thấy các lớp như 6A, 6B, 7A, 7B...

---

**Query kiểm tra Topics:**
```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?topic ?topicId ?label ?grade
WHERE {
  ?topic a edu:Topic ;
         edu:topicId ?topicId ;
         edu:label ?label ;
         edu:forGrade ?gradeIRI .
  ?gradeIRI edu:grade ?grade
}
ORDER BY ?grade ?topicId
```

**Kỳ vọng:** Thấy Topic A, B, C, D, E, F cho khối 6

---

## 🎯 BƯỚC 3: TIẾP TỤC VỚI CÁC TẦNG CÒN LẠI

Sau khi upload xong Tầng B, tiếp tục:

### **TẦNG C - ENTITY DATA**
```
7. students.ttl (hoặc students_updated.ttl)
8. questions_updated.ttl
9. tests.ttl
```

### **TẦNG D - RELATIONSHIPS**
```
10. prerequisites.ttl
11. teachers_assignments.ttl
12. question_skill.ttl
13. resource_skill.ttl
14. questions_in_tests.ttl
```

### **TẦNG E - TRANSACTIONS**
```
15. mastery.ttl
16. test_results.ttl
```

---

## 🔍 QUERIES KIỂM TRA TỔNG QUAN

### Kiểm tra tổng số triples sau mỗi tầng:

```sparql
SELECT (COUNT(*) as ?totalTriples) 
WHERE {
  ?s ?p ?o
}
```

**Kỳ vọng:**
- Sau Schema: ~500
- Sau Tầng B: ~1,000
- Sau Tầng C: ~3,000-5,000
- Sau Tầng D: ~4,000-6,000
- Sau Tầng E: ~5,000-10,000

---

### Kiểm tra số lượng instances:

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?class (COUNT(?instance) as ?count)
WHERE {
  ?instance a ?class .
  FILTER(STRSTARTS(STR(?class), "http://education.vn/ontology#"))
}
GROUP BY ?class
ORDER BY DESC(?count)
```

**Kỳ vọng sau khi upload xong:**
- Question: ~2000 instances
- Student: ~500 instances
- Lesson: ~150 instances
- Test: ~300 instances
- etc.

---

## ⚠️ LƯU Ý QUAN TRỌNG

### ❗ Nếu gặp lỗi khi upload:

1. **Lỗi "Undefined class"**
   - → Schema chưa upload đúng
   - → Kiểm tra lại schema đã có trong repository chưa

2. **Lỗi "Undefined property"**
   - → Schema chưa upload đúng
   - → Kiểm tra lại schema

3. **Lỗi "Referenced entity not found"**
   - → Upload sai thứ tự
   - → Phải upload theo đúng thứ tự A → B → C → D → E

---

## 📋 CHECKLIST BƯỚC TIẾP THEO

```
□ Bước 1: Kiểm tra schema đã upload đúng
  □ Query count triples (~500)
  □ Query list classes (12 classes)
  □ Query list properties (25+)

□ Bước 2: Upload Tầng B - Master Data
  □ grades.ttl
  □ classes.ttl
  □ topics.ttl
  □ skills.ttl
  □ lessons.ttl
  □ resources.ttl

□ Bước 3: Kiểm tra sau Tầng B
  □ Query grades
  □ Query classes
  □ Query topics
  □ Query lessons

□ Bước 4: Upload Tầng C - Entity Data
  □ students.ttl
  □ questions_updated.ttl
  □ tests.ttl

□ Bước 5: Upload Tầng D - Relationships
  □ prerequisites.ttl
  □ teachers_assignments.ttl
  □ question_skill.ttl
  □ resource_skill.ttl
  □ questions_in_tests.ttl

□ Bước 6: Upload Tầng E - Transactions
  □ mastery.ttl
  □ test_results.ttl

□ Bước 7: Kiểm tra tổng thể
  □ Query tổng triples
  □ Query số lượng instances
  □ Test một số queries phức tạp
```

---

## 🎯 QUERIES MẪU ĐỂ TEST

### Query 1: Tìm học sinh và lớp của họ

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?studentId ?fullName ?className
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:belongsToClass ?classIRI .
  ?classIRI edu:className ?className
}
LIMIT 10
```

---

### Query 2: Tìm bài học và chủ đề

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?lesson ?lessonId ?label ?topicLabel
WHERE {
  ?lesson a edu:Lesson ;
          edu:lessonId ?lessonId ;
          edu:label ?label ;
          edu:belongsToTopic ?topicIRI .
  ?topicIRI edu:label ?topicLabel
}
ORDER BY ?lessonId
LIMIT 20
```

---

### Query 3: Tìm câu hỏi và kỹ năng yêu cầu

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?question ?q_id ?questionText ?skillName
WHERE {
  ?question a edu:Question ;
            edu:q_id ?q_id ;
            edu:questionText ?questionText ;
            edu:requiresSkill ?skillIRI .
  ?skillIRI edu:name ?skillName
}
LIMIT 10
```

---

### Query 4: Tìm học sinh yếu ở chủ đề nào (sau khi chạy KNN)

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?fullName ?topicLabel
WHERE {
  ?student a edu:Student ;
           edu:fullName ?fullName ;
           edu:weakInTopic ?topicIRI .
  ?topicIRI edu:label ?topicLabel
}
LIMIT 10
```

---

### Query 5: Tìm bài học được gợi ý cho học sinh (sau khi chạy PPR)

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?fullName ?lesson ?lessonId ?label
WHERE {
  ?student a edu:Student ;
           edu:fullName ?fullName .
  ?lesson a edu:Lesson ;
          edu:lessonId ?lessonId ;
          edu:label ?label ;
          edu:recommendedFor ?student
}
LIMIT 10
```

---

## 🚀 BẮT ĐẦU NGAY

### **Hành động tiếp theo:**

1. ✅ **Kiểm tra schema** (chạy queries ở Bước 1)
2. ✅ **Upload Tầng B** (bắt đầu với `grades.ttl`)
3. ✅ **Kiểm tra sau mỗi file**
4. ✅ **Tiếp tục với các tầng còn lại**

---

## 📚 TÀI LIỆU THAM KHẢO

- **Phân tầng chi tiết:** `HUONG_DAN_UPLOAD_GRAPHDB_PHAN_TANG.md`
- **Checklist:** `CHECKLIST_UPLOAD_TTL.txt`
- **Quick guide:** `QUICK_UPLOAD_GUIDE.txt`

---

**Chúc bạn upload thành công! 🎉**

*Hãy bắt đầu với việc kiểm tra schema, sau đó upload `grades.ttl`!*

