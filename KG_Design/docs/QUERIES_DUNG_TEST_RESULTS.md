# ✅ QUERIES ĐÚNG CHO TEST_RESULTS

## ⚠️ VẤN ĐỀ

File `test_results.ttl` dùng format:
- `data:testresult_result_...` (dùng prefix `data:`)
- **KHÔNG** dùng full URI với `/testresult/`

---

## ✅ QUERIES ĐÚNG

### **Query 1: Kiểm tra test_results.ttl đã upload chưa**

```sparql
SELECT (COUNT(*) as ?count)
WHERE {
  ?s ?p ?o
  FILTER(CONTAINS(STR(?s), "testresult_") || 
         CONTAINS(STR(?s), "testresult"))
}
```

**Kỳ vọng:** > 0 nếu file đã upload

---

### **Query 2: Xem triples của test_results**

```sparql
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o
  FILTER(CONTAINS(STR(?s), "testresult_"))
}
LIMIT 10
```

**Kỳ vọng:** Thấy các triples với testresult

---

### **Query 3: Kiểm tra TestResult instances**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(*) as ?testResultCount)
WHERE {
  ?result a edu:TestResult
}
```

**Kỳ vọng:** > 0

---

### **Query 4: Xem TestResults chi tiết**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?result ?score ?testDate ?testId
WHERE {
  ?result a edu:TestResult ;
          edu:score ?score ;
          edu:forTest ?testIRI .
  OPTIONAL { ?result edu:testDate ?testDate }
  OPTIONAL { ?testIRI edu:testId ?testId }
}
LIMIT 20
```

**Kỳ vọng:** Thấy các kết quả test với điểm số và ngày

---

### **Query 5: TestResults với Students**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?result ?student ?studentId ?fullName ?score ?testId
WHERE {
  ?result a edu:TestResult ;
          edu:score ?score ;
          edu:forTest ?testIRI .
  ?testIRI edu:testId ?testId
  ?student edu:hasResult ?result ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName
}
LIMIT 20
```

**Kỳ vọng:** Thấy kết quả test của học sinh

---

## 📊 QUERY TỔNG QUAN CUỐI CÙNG

### **Tổng số triples:**

```sparql
SELECT (COUNT(*) as ?totalTriples) 
WHERE {
  ?s ?p ?o
}
```

---

### **Tổng hợp tất cả instances:**

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
  (COUNT(DISTINCT ?test) as ?testCount)
  (COUNT(DISTINCT ?result) as ?resultCount)
WHERE {
  { ?student a edu:Student }
  UNION { ?teacher a edu:Teacher }
  UNION { ?class a edu:Class }
  UNION { ?grade a edu:Grade }
  UNION { ?topic a edu:Topic }
  UNION { ?lesson a edu:Lesson }
  UNION { ?question a edu:Question }
  UNION { ?skill a edu:Skill }
  UNION { ?test a edu:Test }
  UNION { ?result a edu:TestResult }
}
```

---

## 🚀 HÀNH ĐỘNG NGAY

**Chạy Query 1 và Query 3 để kiểm tra!**

Nếu có kết quả → File đã upload thành công! ✅

---

## 🎉 SAU KHI HOÀN THÀNH

Knowledge Graph đã sẵn sàng để sử dụng!

---

**Hãy chạy các queries trên! 🔍**

