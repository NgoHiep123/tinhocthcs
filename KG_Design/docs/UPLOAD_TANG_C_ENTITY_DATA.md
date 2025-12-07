# 📊 UPLOAD TẦNG C - ENTITY DATA

## ✅ ĐÃ HOÀN THÀNH

- ✅ **Tầng A - Schema:** 319 triples
- ✅ **Tầng B - Master Data:** ~800 triples (tổng: 1120)
  - ✅ grades.ttl
  - ✅ classes.ttl
  - ✅ topics.ttl
  - ✅ skills.ttl
  - ✅ lessons.ttl
  - ✅ resources.ttl

---

## 🎯 BƯỚC TIẾP THEO: TẦNG C - ENTITY DATA

### **Upload theo thứ tự:**

```
7. students.ttl (hoặc students_updated.ttl)  ← Bắt đầu từ đây
8. questions_updated.ttl
9. tests.ttl
```

---

## 📋 BƯỚC 1: UPLOAD `students.ttl` HOẶC `students_updated.ttl`

### **Lưu ý quan trọng:**
- Chọn **MỘT trong hai** file:
  - `students.ttl` (file gốc)
  - `students_updated.ttl` (file cập nhật - **ƯU TIÊN**)

### **Cách upload:**
1. GraphDB Desktop → Chọn repository `tinhoc_thcs`
2. Import → RDF → Upload RDF files
3. Chọn: `KG_Design/data/grade6/ttl/students_updated.ttl` (hoặc `students.ttl`)
4. Import
5. Đợi hoàn thành

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?studentId ?fullName ?className
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:belongsToClass ?classIRI .
  ?classIRI edu:className ?className
}
ORDER BY ?className ?studentId
LIMIT 20
```

**Kỳ vọng:** Thấy danh sách học sinh với mã, tên, và lớp

---

## 📋 BƯỚC 2: UPLOAD `questions_updated.ttl`

### **Lưu ý:**
- File này có thể **LỚN** (nhiều câu hỏi)
- Upload có thể mất vài phút
- Đợi hoàn thành trước khi tiếp tục

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?question ?q_id ?questionText ?lessonId
WHERE {
  ?question a edu:Question ;
            edu:q_id ?q_id ;
            edu:questionText ?questionText ;
            edu:belongsToLesson ?lessonIRI .
  ?lessonIRI edu:lessonId ?lessonId
}
ORDER BY ?lessonId ?q_id
LIMIT 20
```

**Kỳ vọng:** Thấy các câu hỏi với nội dung và bài học tương ứng

---

## 📋 BƯỚC 3: UPLOAD `tests.ttl`

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?test ?testId ?testName
WHERE {
  ?test a edu:Test ;
        edu:testId ?testId ;
        edu:testName ?testName
}
ORDER BY ?testId
LIMIT 20
```

**Kỳ vọng:** Thấy các bài kiểm tra

---

## ✅ CHECKLIST TẦNG C

```
□ students_updated.ttl    ⏳ Upload tiếp theo
□ questions_updated.ttl  ⏳ Upload tiếp theo
□ tests.ttl              ⏳ Upload tiếp theo
```

---

## 📊 QUERY KIỂM TRA TỔNG QUAN SAU TẦNG C

Sau khi upload xong tất cả Tầng C:

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT 
  (COUNT(DISTINCT ?student) as ?studentCount)
  (COUNT(DISTINCT ?question) as ?questionCount)
  (COUNT(DISTINCT ?test) as ?testCount)
WHERE {
  { ?student a edu:Student }
  UNION
  { ?question a edu:Question }
  UNION
  { ?test a edu:Test }
}
```

**Kỳ vọng:**
- studentCount: ~500 (tùy số học sinh)
- questionCount: ~2000 (tùy số câu hỏi)
- testCount: ~300 (tùy số bài test)

---

## 📊 QUERY ĐẾM TỔNG TRIPLES

Sau mỗi file, kiểm tra:

```sparql
SELECT (COUNT(*) as ?totalTriples) 
WHERE {
  ?s ?p ?o
}
```

**Kỳ vọng sau Tầng C:**
- Sau students: ~1,500-2,000 triples
- Sau questions: ~4,000-5,000 triples
- Sau tests: ~4,500-5,500 triples

---

## ⚠️ LƯU Ý

### **Nếu file quá lớn:**
- GraphDB Desktop có thể chậm
- Đợi hoàn thành (có thể mất vài phút)
- Kiểm tra progress bar

### **Nếu gặp lỗi:**
- Kiểm tra file có dấu `/` trong URI không
- Chạy script sửa: `python KG_Design/scripts/fix_slash_in_uris.py`
- Kiểm tra namespace có đúng không

---

## 🎯 SAU KHI HOÀN THÀNH TẦNG C

### **Bước tiếp theo: Tầng D - Relationship Data**

```
10. prerequisites.ttl
11. teachers_assignments.ttl
12. question_skill.ttl
13. resource_skill.ttl
14. questions_in_tests.ttl
```

---

## 🚀 BẮT ĐẦU NGAY

**Upload `students_updated.ttl` ngay bây giờ!**

Sau đó tiếp tục với `questions_updated.ttl` và `tests.ttl`.

---

**Chúc bạn upload thành công! 🎉**

