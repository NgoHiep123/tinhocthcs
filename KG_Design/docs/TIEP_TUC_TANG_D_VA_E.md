# 🚀 TIẾP TỤC TẦNG D VÀ TẦNG E

## ✅ ĐÃ HOÀN THÀNH

- ✅ **Tầng A - Schema:** 319 triples
- ✅ **Tầng B - Master Data:** ~800 triples
- ✅ **Tầng C - Entity Data:** ~150 triples
- ✅ **Tầng D - Relationships (một phần):**
  - ✅ prerequisites.ttl
  - ✅ teachers_assignments.ttl
- **Tổng hiện tại:** 1575 triples

---

## 🎯 TIẾP TỤC TẦNG D - CÒN 3 FILE

### **Upload theo thứ tự:**

```
12. question_skill.ttl      ← Upload tiếp theo
13. resource_skill.ttl
14. questions_in_tests.ttl
```

---

## 📋 BƯỚC 1: UPLOAD `question_skill.ttl`

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(*) as ?questionSkillCount)
WHERE {
  ?question edu:requiresSkill ?skill
}
```

**Kỳ vọng:** > 0 (có quan hệ question-skill)

---

### **Query xem chi tiết:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?question ?q_id ?skill ?skillName
WHERE {
  ?question a edu:Question ;
            edu:q_id ?q_id ;
            edu:requiresSkill ?skill .
  OPTIONAL { ?skill edu:name ?skillName }
}
LIMIT 20
```

**Kỳ vọng:** Thấy câu hỏi và kỹ năng yêu cầu

---

## 📋 BƯỚC 2: UPLOAD `resource_skill.ttl`

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(*) as ?resourceSkillCount)
WHERE {
  ?resource edu:coversSkill ?skill
}
```

**Kỳ vọng:** > 0 (có quan hệ resource-skill)

---

### **Query xem chi tiết:**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?resource ?resId ?title ?skill ?skillName ?coverage
WHERE {
  ?resource a edu:Resource ;
            edu:resId ?resId ;
            edu:title ?title ;
            edu:coversSkill ?skill .
  OPTIONAL { ?skill edu:name ?skillName }
  OPTIONAL { ?resource edu:coverage ?coverage }
}
LIMIT 20
```

**Kỳ vọng:** Thấy tài nguyên và kỹ năng phủ sóng

---

## 📋 BƯỚC 3: UPLOAD `questions_in_tests.ttl`

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(*) as ?questionInTestCount)
WHERE {
  ?test edu:hasQuestion ?question
}
```

**Kỳ vọng:** > 0 (có câu hỏi trong test)

---

### **Query xem chi tiết:**

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

**Kỳ vọng:** ~1,800-2,200 triples

---

## ✅ CHECKLIST TẦNG D

```
□ prerequisites.ttl          ✅ Đã upload và OK
□ teachers_assignments.ttl    ✅ Đã upload và OK
□ question_skill.ttl          ⏳ Upload tiếp theo
□ resource_skill.ttl          ⏳ Upload tiếp theo
□ questions_in_tests.ttl      ⏳ Upload tiếp theo
```

---

## 🎯 SAU KHI HOÀN THÀNH TẦNG D

### **Bước tiếp theo: Tầng E - Transaction Data (CUỐI CÙNG)**

```
15. mastery.ttl              ← Upload cuối cùng
16. test_results.ttl
```

---

## 📋 BƯỚC 4: UPLOAD `mastery.ttl`

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(*) as ?masteryCount)
WHERE {
  ?mastery a edu:Mastery
}
```

**Kỳ vọng:** > 0 (có mastery records)

---

### **Query xem chi tiết:**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?mastery ?student ?studentId ?fullName ?skill ?skillName ?score
WHERE {
  ?mastery a edu:Mastery ;
           edu:forSkill ?skill ;
           edu:score ?score .
  ?student edu:hasMastery ?mastery ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName .
  OPTIONAL { ?skill edu:name ?skillName }
}
ORDER BY ?studentId ?skillName
LIMIT 20
```

**Kỳ vọng:** Thấy mastery của học sinh với kỹ năng

---

## 📋 BƯỚC 5: UPLOAD `test_results.ttl` (FILE CUỐI CÙNG!)

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(*) as ?testResultCount)
WHERE {
  ?result a edu:TestResult
}
```

**Kỳ vọng:** > 0 (có kết quả test)

---

### **Query xem chi tiết:**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?result ?student ?studentId ?fullName ?test ?testId ?score ?testDate
WHERE {
  ?result a edu:TestResult ;
          edu:forTest ?test ;
          edu:score ?score .
  OPTIONAL { ?result edu:testDate ?testDate }
  ?student edu:hasResult ?result ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName .
  ?test edu:testId ?testId
}
ORDER BY ?studentId ?testDate
LIMIT 20
```

**Kỳ vọng:** Thấy kết quả test của học sinh

---

## 📊 QUERY KIỂM TRA TỔNG QUAN CUỐI CÙNG

Sau khi upload xong TẤT CẢ các tầng:

```sparql
SELECT (COUNT(*) as ?totalTriples) 
WHERE {
  ?s ?p ?o
}
```

**Kỳ vọng:** ~2,500-4,000 triples (tùy dữ liệu)

---

## 📊 QUERY TỔNG HỢP TẤT CẢ INSTANCES

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT 
  (COUNT(DISTINCT ?student) as ?studentCount)
  (COUNT(DISTINCT ?teacher) as ?teacherCount)
  (COUNT(DISTINCT ?class) as ?classCount)
  (COUNT(DISTINCT ?grade) as ?gradeCount)
  (COUNT(DISTINCT ?topic) as ?topicCount)
  (COUNT(DISTINCT ?lesson) as ?lessonCount)
  (COUNT(DISTINCT ?question) as ?questionCount)
  (COUNT(DISTINCT ?skill) as ?skillCount)
  (COUNT(DISTINCT ?resource) as ?resourceCount)
  (COUNT(DISTINCT ?test) as ?testCount)
  (COUNT(DISTINCT ?result) as ?resultCount)
  (COUNT(DISTINCT ?mastery) as ?masteryCount)
WHERE {
  { ?student a edu:Student }
  UNION { ?teacher a edu:Teacher }
  UNION { ?class a edu:Class }
  UNION { ?grade a edu:Grade }
  UNION { ?topic a edu:Topic }
  UNION { ?lesson a edu:Lesson }
  UNION { ?question a edu:Question }
  UNION { ?skill a edu:Skill }
  UNION { ?resource a edu:Resource }
  UNION { ?test a edu:Test }
  UNION { ?result a edu:TestResult }
  UNION { ?mastery a edu:Mastery }
}
```

**Kỳ vọng:** Thấy số lượng của từng loại entity

---

## ✅ CHECKLIST TẦNG E

```
□ mastery.ttl              ⏳ Upload cuối cùng
□ test_results.ttl         ⏳ File cuối cùng!
```

---

## 🎉 SAU KHI HOÀN THÀNH TẤT CẢ

### **Knowledge Graph đã sẵn sàng!**

Bạn có thể:
- ✅ Chạy các queries phức tạp
- ✅ Test các thuật toán KNN và PPR
- ✅ Sử dụng hệ thống gợi ý
- ✅ Phân tích dữ liệu học tập

---

## 🚀 HÀNH ĐỘNG NGAY

**Upload 3 file còn lại trong Tầng D:**
1. `question_skill.ttl`
2. `resource_skill.ttl`
3. `questions_in_tests.ttl`

**Sau đó upload Tầng E:**
4. `mastery.ttl`
5. `test_results.ttl` ← File cuối cùng!

---

**Chúc bạn upload thành công và hoàn thành Knowledge Graph! 🎉**


