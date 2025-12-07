# 🎉 BƯỚC TIẾP THEO SAU KHI HOÀN THÀNH KNOWLEDGE GRAPH

## ✅ ĐÃ HOÀN THÀNH

- ✅ **Tầng A - Schema:** 319 triples
- ✅ **Tầng B - Master Data:** 6 files
- ✅ **Tầng C - Entity Data:** 3 files
- ✅ **Tầng D - Relationships:** 5 files
- ✅ **Tầng E - Transactions:** 2 files
- ✅ **Tổng:** ~2,500-4,000 triples

**Knowledge Graph đã sẵn sàng! 🎉**

---

## 🎯 CÁC BƯỚC TIẾP THEO

### **1. KIỂM TRA TỔNG QUAN**

#### **Query tổng hợp tất cả:**

**Nếu gặp lỗi "Multiple prefix declarations", hãy xóa dòng PREFIX nếu đã có sẵn trong GraphDB:**

```sparql
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
WHERE {
  { ?student a <http://education.vn/ontology#Student> }
  UNION { ?teacher a <http://education.vn/ontology#Teacher> }
  UNION { ?class a <http://education.vn/ontology#Class> }
  UNION { ?grade a <http://education.vn/ontology#Grade> }
  UNION { ?topic a <http://education.vn/ontology#Topic> }
  UNION { ?lesson a <http://education.vn/ontology#Lesson> }
  UNION { ?question a <http://education.vn/ontology#Question> }
  UNION { ?skill a <http://education.vn/ontology#Skill> }
  UNION { ?resource a <http://education.vn/ontology#Resource> }
  UNION { ?test a <http://education.vn/ontology#Test> }
  UNION { ?result a <http://education.vn/ontology#TestResult> }
}
```

**Hoặc nếu repository đã có prefix `edu:` và `data:` được định nghĩa sẵn, dùng query này:**

```sparql
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
}
```

---

### **2. TEST CÁC QUERIES PHỨC TẠP**

#### **Query 1: Tìm học sinh và kết quả test của họ**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?studentId ?fullName ?className ?testId ?score ?testDate
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:belongsToClass ?classIRI ;
           edu:hasResult ?result .
  ?classIRI edu:className ?className
  ?result a edu:TestResult ;
          edu:forTest ?testIRI ;
          edu:score ?score .
  OPTIONAL { ?result edu:testDate ?testDate }
  ?testIRI edu:testId ?testId
}
ORDER BY ?studentId ?testDate
LIMIT 20
```

---

#### **Query 2: Tìm bài học và câu hỏi liên quan**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?lesson ?lessonId ?label ?topicLabel 
       (COUNT(?question) as ?questionCount)
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
ORDER BY ?lessonId
LIMIT 20
```

---

#### **Query 3: Tìm kỹ năng tiên quyết**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?prerequisiteSkill ?prerequisiteName ?skill ?skillName
WHERE {
  ?prerequisiteSkill edu:prerequisiteOf ?skill ;
                     edu:name ?prerequisiteName .
  ?skill edu:name ?skillName
}
LIMIT 20
```

---

#### **Query 4: Tìm giáo viên và số lớp họ dạy**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?teacher ?teacherId ?fullName 
       (COUNT(?class) as ?classCount)
WHERE {
  ?teacher a edu:Teacher ;
           edu:teacherId ?teacherId ;
           edu:fullName ?fullName ;
           edu:teaches ?class
}
GROUP BY ?teacher ?teacherId ?fullName
ORDER BY DESC(?classCount)
```

---

#### **Query 5: Tìm câu hỏi trong bài test**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?test ?testId ?testName 
       (COUNT(?question) as ?questionCount)
WHERE {
  ?test a edu:Test ;
        edu:testId ?testId .
  OPTIONAL { ?test edu:testName ?testName }
  OPTIONAL {
    ?test edu:hasQuestion ?question
  }
}
GROUP BY ?test ?testId ?testName
ORDER BY ?testId
LIMIT 20
```

---

### **3. SỬ DỤNG KNOWLEDGE GRAPH CHO CÁC MỤC ĐÍCH**

#### **A. Phân tích dữ liệu học tập**

##### **Tìm học sinh yếu ở chủ đề nào:**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?studentId ?fullName ?topicLabel 
       (AVG(?score) as ?avgScore)
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:hasResult ?result .
  ?result edu:forTest ?test ;
          edu:score ?score .
  ?test edu:belongsToTopic ?topicIRI .
  ?topicIRI edu:label ?topicLabel
}
GROUP BY ?student ?studentId ?fullName ?topicLabel
HAVING (AVG(?score) < 0.5)
ORDER BY ?studentId ?avgScore
```

---

##### **Tìm bài học khó nhất (điểm trung bình thấp nhất):**

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

#### **B. Gợi ý bài học (có thể dùng PPR sau)**

##### **Tìm bài học liên quan đến chủ đề:**

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
ORDER BY ?topicLabel ?lessonId
```

---

##### **Tìm tài nguyên học tập cho kỹ năng:**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?resource ?resId ?title ?skillName ?coverage
WHERE {
  ?resource a edu:Resource ;
            edu:resId ?resId ;
            edu:title ?title ;
            edu:coversSkill ?skillIRI .
  ?skillIRI edu:name ?skillName
  OPTIONAL { ?resource edu:coverage ?coverage }
}
ORDER BY ?skillName
LIMIT 20
```

---

#### **C. Phân tích giáo viên**

##### **Xem giáo viên nào dạy nhiều lớp nhất:**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?teacher ?teacherId ?fullName 
       (COUNT(?class) as ?classCount)
       (GROUP_CONCAT(?className; separator=", ") as ?classes)
WHERE {
  ?teacher a edu:Teacher ;
           edu:teacherId ?teacherId ;
           edu:fullName ?fullName ;
           edu:teaches ?classIRI .
  ?classIRI edu:className ?className
}
GROUP BY ?teacher ?teacherId ?fullName
ORDER BY DESC(?classCount)
```

---

### **4. TÍCH HỢP VỚI BACKEND/API**

#### **Kết nối GraphDB với Python:**

```python
from SPARQLWrapper import SPARQLWrapper, JSON

# Cấu hình GraphDB
GRAPHDB_URL = "http://localhost:7200"
REPOSITORY = "tinhocthcs"
SPARQL_ENDPOINT = f"{GRAPHDB_URL}/repositories/{REPOSITORY}"

def query_graphdb(query):
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings']

# Ví dụ query
query = """
PREFIX edu: <http://education.vn/ontology#>
SELECT ?student ?studentId ?fullName
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName
}
LIMIT 10
"""

results = query_graphdb(query)
for result in results:
    print(result['studentId']['value'], result['fullName']['value'])
```

---

#### **Kết nối GraphDB với JavaScript:**

```javascript
// Sử dụng fetch API
async function queryGraphDB(query) {
    const response = await fetch('http://localhost:7200/repositories/tinhocthcs', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/sparql-query',
            'Accept': 'application/sparql-results+json'
        },
        body: query
    });
    return await response.json();
}

// Ví dụ query
const query = `
PREFIX edu: <http://education.vn/ontology#>
SELECT ?student ?studentId ?fullName
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName
}
LIMIT 10
`;

queryGraphDB(query).then(results => {
    console.log(results);
});
```

---

### **5. SỬ DỤNG CHO THUẬT TOÁN ML**

#### **A. Chuẩn bị dữ liệu cho KNN:**

```sparql
# Lấy điểm số của học sinh theo chủ đề
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?studentId ?topic ?topicId 
       (AVG(?score) as ?avgScore)
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
ORDER BY ?studentId ?topicId
```

---

#### **B. Chuẩn bị dữ liệu cho PPR:**

```sparql
# Lấy cấu trúc graph: Student -> Lesson -> Topic
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

### **6. TẠO DASHBOARD/REPORTS**

#### **Thống kê tổng quan:**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT 
  (COUNT(DISTINCT ?student) as ?totalStudents)
  (COUNT(DISTINCT ?teacher) as ?totalTeachers)
  (COUNT(DISTINCT ?lesson) as ?totalLessons)
  (COUNT(DISTINCT ?question) as ?totalQuestions)
  (COUNT(DISTINCT ?test) as ?totalTests)
  (COUNT(?result) as ?totalResults)
  (AVG(?score) as ?avgScore)
WHERE {
  { ?student a edu:Student }
  UNION { ?teacher a edu:Teacher }
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

#### **Top 10 học sinh điểm cao nhất:**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?studentId ?fullName 
       (AVG(?score) as ?avgScore)
       (COUNT(?result) as ?testCount)
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:hasResult ?result .
  ?result edu:score ?score
}
GROUP BY ?student ?studentId ?fullName
HAVING (COUNT(?result) > 3)
ORDER BY DESC(?avgScore)
LIMIT 10
```

---

### **7. BACKUP VÀ BẢO TRÌ**

#### **Export dữ liệu:**

```sparql
# Export tất cả dữ liệu
CONSTRUCT {
  ?s ?p ?o
}
WHERE {
  ?s ?p ?o
}
```

---

#### **Kiểm tra dữ liệu:**

```sparql
# Kiểm tra dữ liệu bị thiếu
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?studentId
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId
  FILTER NOT EXISTS {
    ?student edu:belongsToClass ?class
  }
}
```

---

## 📊 QUERIES MẪU HỮU ÍCH

### **1. Tìm học sinh chưa làm bài test nào:**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?studentId ?fullName
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName
  FILTER NOT EXISTS {
    ?student edu:hasResult ?result
  }
}
```

---

### **2. Tìm bài học có nhiều câu hỏi nhất:**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?lesson ?lessonId ?label 
       (COUNT(?question) as ?questionCount)
WHERE {
  ?lesson a edu:Lesson ;
          edu:lessonId ?lessonId ;
          edu:label ?label .
  ?question a edu:Question ;
            edu:belongsToLesson ?lesson
}
GROUP BY ?lesson ?lessonId ?label
ORDER BY DESC(?questionCount)
LIMIT 10
```

---

### **3. Tìm chủ đề khó nhất:**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?topic ?topicId ?label 
       (AVG(?score) as ?avgScore)
       (COUNT(?result) as ?attemptCount)
WHERE {
  ?result a edu:TestResult ;
          edu:forTest ?test ;
          edu:score ?score .
  ?test edu:belongsToTopic ?topicIRI .
  ?topicIRI edu:topicId ?topicId ;
            edu:label ?label
}
GROUP BY ?topic ?topicId ?label
HAVING (COUNT(?result) > 10)
ORDER BY ?avgScore
LIMIT 10
```

---

## 🎯 NEXT STEPS

### **1. Test các queries trên**
- Chạy từng query
- Kiểm tra kết quả
- Điều chỉnh nếu cần

### **2. Tích hợp với backend**
- Kết nối GraphDB với Python/Node.js
- Tạo API endpoints
- Build frontend để hiển thị

### **3. Triển khai ML algorithms**
- KNN để phát hiện học sinh yếu
- PPR để gợi ý bài học
- Lưu kết quả vào KG

### **4. Tạo reports và analytics**
- Dashboard cho giáo viên
- Reports cho học sinh
- Analytics cho nhà trường

---

## 📚 TÀI LIỆU THAM KHẢO

- **SPARQL Tutorial:** https://www.w3.org/TR/sparql11-query/
- **GraphDB Documentation:** https://graphdb.ontotext.com/documentation/
- **RDF Best Practices:** https://www.w3.org/TR/rdf11-primer/

---

**Chúc bạn sử dụng Knowledge Graph hiệu quả! 🚀**

