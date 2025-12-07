# 🔗 UPLOAD TẦNG D - RELATIONSHIP DATA

## ✅ ĐÃ HOÀN THÀNH

- ✅ **Tầng A - Schema:** 319 triples
- ✅ **Tầng B - Master Data:** ~800 triples
- ✅ **Tầng C - Entity Data:** ~150 triples
  - ✅ students_updated.ttl
  - ✅ classes.ttl
  - ✅ questions_updated.ttl (39 questions - đúng với file)
  - ✅ tests.ttl (23 tests)
- **Tổng hiện tại:** 1270 triples

---

## 🎯 BƯỚC TIẾP THEO: TẦNG D - RELATIONSHIP DATA

### **Upload theo thứ tự:**

```
10. prerequisites.ttl          ← Bắt đầu từ đây
11. teachers_assignments.ttl
12. question_skill.ttl
13. resource_skill.ttl
14. questions_in_tests.ttl
```

---

## 📋 BƯỚC 1: UPLOAD `prerequisites.ttl`

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?prerequisite ?prerequisiteId ?lesson ?lessonId
WHERE {
  ?prerequisite a edu:Lesson ;
                edu:lessonId ?prerequisiteId ;
                edu:prerequisiteOf ?lesson .
  ?lesson edu:lessonId ?lessonId
}
LIMIT 20
```

**Kỳ vọng:** Thấy quan hệ tiên quyết giữa các bài học

---

## 📋 BƯỚC 2: UPLOAD `teachers_assignments.ttl`

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?teacher ?teacherId ?fullName ?className
WHERE {
  ?teacher a edu:Teacher ;
           edu:teacherId ?teacherId ;
           edu:fullName ?fullName ;
           edu:teaches ?classIRI .
  ?classIRI edu:className ?className
}
LIMIT 20
```

**Kỳ vọng:** Thấy giáo viên và lớp họ dạy

---

## 📋 BƯỚC 3: UPLOAD `question_skill.ttl`

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?question ?q_id ?skill ?skillName
WHERE {
  ?question a edu:Question ;
            edu:q_id ?q_id ;
            edu:requiresSkill ?skill .
  ?skill edu:name ?skillName
}
LIMIT 20
```

**Kỳ vọng:** Thấy câu hỏi và kỹ năng yêu cầu

---

## 📋 BƯỚC 4: UPLOAD `resource_skill.ttl`

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?resource ?resId ?title ?skill ?skillName
WHERE {
  ?resource a edu:Resource ;
            edu:resId ?resId ;
            edu:title ?title ;
            edu:coversSkill ?skill .
  ?skill edu:name ?skillName
}
LIMIT 20
```

**Kỳ vọng:** Thấy tài nguyên và kỹ năng phủ sóng

---

## 📋 BƯỚC 5: UPLOAD `questions_in_tests.ttl`

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?test ?testId ?question ?q_id
WHERE {
  ?test a edu:Test ;
        edu:testId ?testId ;
        edu:hasQuestion ?question .
  ?question edu:q_id ?q_id
}
ORDER BY ?testId ?q_id
LIMIT 20
```

**Kỳ vọng:** Thấy bài test và các câu hỏi trong test

---

## 📊 QUERY KIỂM TRA TỔNG QUAN SAU TẦNG D

Sau khi upload xong tất cả Tầng D:

```sparql
SELECT (COUNT(*) as ?totalTriples) 
WHERE {
  ?s ?p ?o
}
```

**Kỳ vọng:** ~1,500-2,000 triples (tùy dữ liệu)

---

## ✅ CHECKLIST TẦNG D

```
□ prerequisites.ttl          ⏳ Upload tiếp theo
□ teachers_assignments.ttl    ⏳ Upload tiếp theo
□ question_skill.ttl          ⏳ Upload tiếp theo
□ resource_skill.ttl          ⏳ Upload tiếp theo
□ questions_in_tests.ttl      ⏳ Upload tiếp theo
```

---

## 🎯 SAU KHI HOÀN THÀNH TẦNG D

### **Bước tiếp theo: Tầng E - Transaction Data**

```
15. mastery.ttl
16. test_results.ttl
```

---

## 🚀 BẮT ĐẦU NGAY

**Upload `prerequisites.ttl` ngay bây giờ!**

Sau đó tiếp tục với các file còn lại trong Tầng D.

---

**Chúc bạn upload thành công! 🎉**

