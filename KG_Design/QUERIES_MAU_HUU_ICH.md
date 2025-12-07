# 📊 CÁC QUERIES MẪU HỮU ÍCH - KNOWLEDGE GRAPH

## 🎯 MỤC ĐÍCH

Tổng hợp các queries SPARQL mẫu để sử dụng Knowledge Graph hiệu quả.

---

## 📊 QUERIES THỐNG KÊ

### **1. Tổng quan hệ thống**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT 
  (COUNT(DISTINCT ?student) as ?studentCount)
  (COUNT(DISTINCT ?teacher) as ?teacherCount)
  (COUNT(DISTINCT ?class) as ?classCount)
  (COUNT(DISTINCT ?lesson) as ?lessonCount)
  (COUNT(DISTINCT ?question) as ?questionCount)
  (COUNT(DISTINCT ?test) as ?testCount)
  (COUNT(?result) as ?resultCount)
  (AVG(?score) as ?avgScore)
WHERE {
  { ?student a edu:Student }
  UNION { ?teacher a edu:Teacher }
  UNION { ?class a edu:Class }
  UNION { ?lesson a edu:Lesson }
  UNION { ?question a edu:Question }
  UNION { ?test a edu:Test }
  UNION { 
    ?result a edu:TestResult ;
            edu:score ?score
  }
}
```

---

### **2. Thống kê theo lớp**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?className 
       (COUNT(DISTINCT ?student) as ?studentCount)
       (AVG(?score) as ?avgScore)
       (COUNT(?result) as ?testCount)
WHERE {
  ?student a edu:Student ;
           edu:belongsToClass ?classIRI ;
           edu:hasResult ?result .
  ?classIRI edu:className ?className
  ?result edu:score ?score
}
GROUP BY ?className
ORDER BY ?className
```

---

### **3. Thống kê theo chủ đề**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?topicLabel 
       (COUNT(DISTINCT ?lesson) as ?lessonCount)
       (COUNT(DISTINCT ?question) as ?questionCount)
       (AVG(?score) as ?avgScore)
WHERE {
  ?topic a edu:Topic ;
         edu:label ?topicLabel .
  ?lesson edu:belongsToTopic ?topic .
  OPTIONAL {
    ?question edu:belongsToLesson ?lesson
  }
  OPTIONAL {
    ?result a edu:TestResult ;
            edu:forTest ?test ;
            edu:score ?score .
    ?test edu:hasQuestion ?question
  }
}
GROUP BY ?topicLabel
ORDER BY ?topicLabel
```

---

## 👥 QUERIES VỀ HỌC SINH

### **4. Danh sách học sinh và lớp**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?studentId ?fullName ?className ?grade
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:belongsToClass ?classIRI .
  ?classIRI edu:className ?className ;
            edu:belongsToGrade ?gradeIRI .
  ?gradeIRI edu:grade ?grade
}
ORDER BY ?grade ?className ?studentId
```

---

### **5. Top 10 học sinh điểm cao nhất**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?studentId ?fullName ?className
       (AVG(?score) as ?avgScore)
       (COUNT(?result) as ?testCount)
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:belongsToClass ?classIRI ;
           edu:hasResult ?result .
  ?classIRI edu:className ?className
  ?result edu:score ?score
}
GROUP BY ?student ?studentId ?fullName ?className
HAVING (COUNT(?result) >= 3)
ORDER BY DESC(?avgScore)
LIMIT 10
```

---

### **6. Học sinh yếu cần hỗ trợ**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?studentId ?fullName ?className
       (AVG(?score) as ?avgScore)
       (COUNT(?result) as ?testCount)
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:belongsToClass ?classIRI ;
           edu:hasResult ?result .
  ?classIRI edu:className ?className
  ?result edu:score ?score
}
GROUP BY ?student ?studentId ?fullName ?className
HAVING (AVG(?score) < 0.5 && COUNT(?result) >= 3)
ORDER BY ?avgScore
```

---

### **7. Học sinh chưa làm bài test nào**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?studentId ?fullName ?className
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:belongsToClass ?classIRI .
  ?classIRI edu:className ?className
  FILTER NOT EXISTS {
    ?student edu:hasResult ?result
  }
}
ORDER BY ?className ?studentId
```

---

## 📚 QUERIES VỀ BÀI HỌC

### **8. Danh sách bài học và số câu hỏi**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?lesson ?lessonId ?label ?topicLabel
       (COUNT(DISTINCT ?question) as ?questionCount)
WHERE {
  ?lesson a edu:Lesson ;
          edu:lessonId ?lessonId ;
          edu:label ?label ;
          edu:belongsToTopic ?topicIRI .
  ?topicIRI edu:label ?topicLabel
  OPTIONAL {
    ?question a edu:Question ;
              edu:belongsToLesson ?lesson
  }
}
GROUP BY ?lesson ?lessonId ?label ?topicLabel
ORDER BY ?topicLabel ?lessonId
```

---

### **9. Bài học khó nhất (điểm trung bình thấp)**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?lesson ?lessonId ?label 
       (AVG(?score) as ?avgScore)
       (COUNT(?result) as ?attemptCount)
WHERE {
  ?result a edu:TestResult ;
          edu:forTest ?test ;
          edu:score ?score .
  ?test edu:hasQuestion ?question .
  ?question edu:belongsToLesson ?lesson .
  ?lesson edu:lessonId ?lessonId ;
          edu:label ?label
}
GROUP BY ?lesson ?lessonId ?label
HAVING (COUNT(?result) > 5)
ORDER BY ?avgScore
LIMIT 10
```

---

### **10. Tìm bài học liên quan (prerequisites)**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?prerequisite ?prerequisiteId ?prerequisiteLabel
       ?lesson ?lessonId ?label
WHERE {
  ?prerequisite a edu:Lesson ;
                edu:lessonId ?prerequisiteId ;
                edu:label ?prerequisiteLabel ;
                edu:prerequisiteOf ?lesson .
  ?lesson edu:lessonId ?lessonId ;
          edu:label ?label
}
ORDER BY ?prerequisiteId
```

---

## 🧠 QUERIES VỀ KỸ NĂNG

### **11. Kỹ năng tiên quyết**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?prerequisiteSkill ?prerequisiteName 
       ?skill ?skillName
WHERE {
  ?prerequisiteSkill edu:prerequisiteOf ?skill ;
                     edu:name ?prerequisiteName .
  ?skill edu:name ?skillName
}
ORDER BY ?prerequisiteName
```

---

### **12. Câu hỏi yêu cầu kỹ năng nào**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?skill ?skillName ?bloomLevel
       (COUNT(?question) as ?questionCount)
WHERE {
  ?skill a edu:Skill ;
         edu:name ?skillName .
  OPTIONAL { ?skill edu:bloomLevel ?bloomLevel }
  ?question a edu:Question ;
            edu:requiresSkill ?skill
}
GROUP BY ?skill ?skillName ?bloomLevel
ORDER BY DESC(?questionCount)
```

---

## 📝 QUERIES VỀ BÀI TEST

### **13. Danh sách bài test và số câu hỏi**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?test ?testId ?testName
       (COUNT(DISTINCT ?question) as ?questionCount)
       (AVG(?score) as ?avgScore)
       (COUNT(?result) as ?attemptCount)
WHERE {
  ?test a edu:Test ;
        edu:testId ?testId .
  OPTIONAL { ?test edu:testName ?testName }
  OPTIONAL {
    ?test edu:hasQuestion ?question
  }
  OPTIONAL {
    ?result a edu:TestResult ;
            edu:forTest ?test ;
            edu:score ?score
  }
}
GROUP BY ?test ?testId ?testName
ORDER BY ?testId
```

---

### **14. Kết quả test của học sinh**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?studentId ?fullName 
       ?testId ?testName ?score ?testDate
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:hasResult ?result .
  ?result edu:forTest ?testIRI ;
          edu:score ?score .
  OPTIONAL { ?result edu:testDate ?testDate }
  ?testIRI edu:testId ?testId .
  OPTIONAL { ?testIRI edu:testName ?testName }
}
ORDER BY ?studentId ?testDate
LIMIT 50
```

---

## 👨‍🏫 QUERIES VỀ GIÁO VIÊN

### **15. Giáo viên và lớp họ dạy**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?teacher ?teacherId ?fullName ?expertise
       (COUNT(?class) as ?classCount)
       (GROUP_CONCAT(?className; separator=", ") as ?classes)
WHERE {
  ?teacher a edu:Teacher ;
           edu:teacherId ?teacherId ;
           edu:fullName ?fullName .
  OPTIONAL { ?teacher edu:expertise ?expertise }
  ?teacher edu:teaches ?classIRI .
  ?classIRI edu:className ?className
}
GROUP BY ?teacher ?teacherId ?fullName ?expertise
ORDER BY DESC(?classCount)
```

---

## 📊 QUERIES PHÂN TÍCH

### **16. Phân tích điểm theo chủ đề**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?topicLabel 
       (MIN(?score) as ?minScore)
       (MAX(?score) as ?maxScore)
       (AVG(?score) as ?avgScore)
       (COUNT(?result) as ?attemptCount)
WHERE {
  ?result a edu:TestResult ;
          edu:forTest ?test ;
          edu:score ?score .
  ?test edu:belongsToTopic ?topicIRI .
  ?topicIRI edu:label ?topicLabel
}
GROUP BY ?topicLabel
HAVING (COUNT(?result) > 10)
ORDER BY ?avgScore
```

---

### **17. Tỷ lệ học sinh đạt/không đạt**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT 
  (COUNT(DISTINCT ?student) as ?totalStudents)
  (SUM(IF(?score >= 0.5, 1, 0)) as ?passedCount)
  (SUM(IF(?score < 0.5, 1, 0)) as ?failedCount)
  ((SUM(IF(?score >= 0.5, 1, 0)) * 100.0 / COUNT(?result)) as ?passRate)
WHERE {
  ?result a edu:TestResult ;
          edu:score ?score .
  ?student edu:hasResult ?result
}
```

---

## 🔗 QUERIES LIÊN KẾT PHỨC TẠP

### **18. Học sinh → Bài học → Kỹ năng → Tài nguyên**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT DISTINCT ?student ?studentId ?fullName
       ?lesson ?lessonId ?label
       ?skill ?skillName
       ?resource ?resId ?title
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:hasResult ?result .
  ?result edu:forTest ?test .
  ?test edu:hasQuestion ?question .
  ?question edu:belongsToLesson ?lesson ;
            edu:requiresSkill ?skill .
  ?lesson edu:lessonId ?lessonId ;
          edu:label ?label .
  ?skill edu:name ?skillName .
  ?resource a edu:Resource ;
            edu:resId ?resId ;
            edu:title ?title ;
            edu:coversSkill ?skill
}
LIMIT 20
```

---

## 🎯 QUERIES CHO ML/AI

### **19. Dữ liệu cho KNN (học sinh yếu ở chủ đề)**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?studentId ?topic ?topicId 
       (AVG(?score) as ?avgScore)
       (COUNT(?result) as ?attemptCount)
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:hasResult ?result .
  ?result edu:forTest ?test ;
          edu:score ?score .
  ?test edu:belongsToTopic ?topicIRI .
  ?topicIRI edu:topicId ?topicId
}
GROUP BY ?student ?studentId ?topic ?topicId
HAVING (COUNT(?result) >= 2)
ORDER BY ?studentId ?topicId
```

---

### **20. Dữ liệu cho PPR (cấu trúc graph)**

```sparql
# Student -> Lesson -> Topic
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?lesson ?topic
WHERE {
  ?student a edu:Student ;
           edu:hasResult ?result .
  ?result edu:forTest ?test .
  ?test edu:hasQuestion ?question .
  ?question edu:belongsToLesson ?lesson .
  ?lesson edu:belongsToTopic ?topic
}
LIMIT 100
```

---

## 📋 CÁCH SỬ DỤNG

### **Trong GraphDB Desktop:**
1. Mở SPARQL editor
2. Copy query
3. Execute
4. Xem kết quả

### **Trong Python:**
```python
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://localhost:7200/repositories/tinhocthcs")
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
```

### **Trong JavaScript:**
```javascript
fetch('http://localhost:7200/repositories/tinhocthcs', {
    method: 'POST',
    headers: {'Content-Type': 'application/sparql-query'},
    body: query
})
.then(res => res.json())
.then(data => console.log(data));
```

---

**Chọn query phù hợp với nhu cầu và sử dụng! 🚀**

