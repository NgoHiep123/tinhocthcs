# ✅ TIẾP TỤC SAU KHI STUDENTS OK

## ✅ ĐÃ XÁC NHẬN

- ✅ Students đã được upload thành công
- ✅ Query 1 và Query 2 chạy OK
- ✅ File `classes.ttl` đã được tạo

---

## 🚀 BƯỚC TIẾP THEO

### **BƯỚC 1: Upload file `classes.ttl` mới**

1. GraphDB Desktop → Chọn repository `tinhocthcs`
2. Import → RDF → Upload RDF files
3. Chọn: `KG_Design/data/grade6/ttl/classes.ttl`
4. Import
5. Đợi hoàn thành

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?class ?className ?grade
WHERE {
  ?class a edu:Class ;
         edu:className ?className ;
         edu:belongsToGrade ?gradeIRI .
  ?gradeIRI edu:grade ?grade
}
```

**Kỳ vọng:** Thấy `data:class_6_1` với `className = "6/1"` và `grade = 6`

---

### **BƯỚC 2: Chạy lại query ban đầu**

Sau khi upload `classes.ttl`, query ban đầu sẽ hoạt động:

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

**Kỳ vọng:** Thấy students với `className = "6/1"`

---

## 📋 TIẾP TỤC TẦNG C

Sau khi `classes.ttl` OK, tiếp tục upload:

```
8. questions_updated.ttl  ← Upload tiếp theo
9. tests.ttl
```

---

## 🔍 BƯỚC 3: UPLOAD `questions_updated.ttl`

### **Lưu ý:**
- File này có thể **LỚN** (nhiều câu hỏi)
- Upload có thể mất vài phút
- Đợi hoàn thành trước khi tiếp tục

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT (COUNT(*) as ?questionCount)
WHERE {
  ?question a edu:Question
}
```

**Kỳ vọng:** ~2000 câu hỏi (tùy dữ liệu)

---

### **Query xem câu hỏi:**

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

---

## 🔍 BƯỚC 4: UPLOAD `tests.ttl`

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

## 📊 QUERY KIỂM TRA TỔNG QUAN SAU TẦNG C

Sau khi upload xong tất cả Tầng C:

```sparql
SELECT (COUNT(*) as ?totalTriples) 
WHERE {
  ?s ?p ?o
}
```

**Kỳ vọng:** ~4,500-5,500 triples

---

## ✅ CHECKLIST TẦNG C

```
□ students_updated.ttl    ✅ Đã upload và OK
□ classes.ttl            ⏳ Upload tiếp theo (file mới)
□ questions_updated.ttl  ⏳ Upload tiếp theo
□ tests.ttl              ⏳ Upload tiếp theo
```

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

## 🚀 HÀNH ĐỘNG NGAY

1. ✅ **Upload `classes.ttl` mới**
2. ✅ **Chạy lại query ban đầu** → Sẽ có kết quả
3. ⏭️ **Tiếp tục với `questions_updated.ttl`**

---

**Chúc bạn upload thành công! 🎉**

