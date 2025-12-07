# 🎉 UPLOAD FILE CUỐI CÙNG - test_results.ttl

## ✅ ĐÃ HOÀN THÀNH

- ✅ **Tầng A - Schema:** 319 triples
- ✅ **Tầng B - Master Data:** ~800 triples
- ✅ **Tầng C - Entity Data:** ~150 triples
- ✅ **Tầng D - Relationships:**
  - ✅ prerequisites.ttl
  - ✅ teachers_assignments.ttl
  - ✅ question_skill.ttl
  - ✅ resource_skill.ttl (đã upload, có dữ liệu)
  - ✅ questions_in_tests.ttl
- ✅ **Tầng E - Transactions:**
  - ✅ mastery.ttl (đã upload, có dữ liệu)

---

## 🎯 FILE CUỐI CÙNG: `test_results.ttl`

### **Upload ngay:**

```
1. GraphDB Desktop → Import → RDF
2. Chọn: KG_Design/data/grade6/ttl/test_results.ttl
3. Import
4. Đợi hoàn thành
```

---

## 🔍 QUERY KIỂM TRA SAU KHI UPLOAD

### **Query 1: Kiểm tra test_results.ttl đã upload chưa**

```sparql
SELECT (COUNT(*) as ?count)
WHERE {
  ?s ?p ?o
  FILTER(CONTAINS(STR(?s), "/testresult/") || 
         CONTAINS(STR(?s), "/result/"))
}
```

**Kỳ vọng:** > 0

---

### **Query 2: Xem một số triples của test_results**

```sparql
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o
  FILTER(CONTAINS(STR(?s), "/testresult/") || 
         CONTAINS(STR(?s), "/result/"))
}
LIMIT 10
```

---

### **Query 3: Kiểm tra tổng số triples CUỐI CÙNG**

```sparql
SELECT (COUNT(*) as ?totalTriples) 
WHERE {
  ?s ?p ?o
}
```

**Kỳ vọng:** ~2,500-4,000 triples (tùy dữ liệu)

---

## 📊 QUERY TỔNG HỢP CUỐI CÙNG

### **Đếm tất cả instances:**

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
}
```

---

## ✅ CHECKLIST CUỐI CÙNG

```
✅ Tầng A - Schema
✅ Tầng B - Master Data (6 files)
✅ Tầng C - Entity Data (3 files)
✅ Tầng D - Relationships (5 files)
✅ Tầng E - Transactions (1 file: mastery.ttl)
⏳ test_results.ttl (FILE CUỐI CÙNG!)
```

---

## 🎉 SAU KHI HOÀN THÀNH

### **Knowledge Graph đã sẵn sàng!**

Bạn có thể:
- ✅ Chạy các queries phức tạp
- ✅ Test các thuật toán KNN và PPR
- ✅ Sử dụng hệ thống gợi ý
- ✅ Phân tích dữ liệu học tập

---

## 📊 QUERIES DEMO SAU KHI HOÀN THÀNH

### **Query 1: Tìm học sinh và lớp**

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

### **Query 2: Tìm bài học và chủ đề**

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
LIMIT 20
```

---

### **Query 3: Tìm câu hỏi và kỹ năng**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?question ?q_id ?skillName
WHERE {
  ?question a edu:Question ;
            edu:q_id ?q_id ;
            edu:requiresSkill ?skillIRI .
  ?skillIRI edu:name ?skillName
}
LIMIT 20
```

---

## 🚀 BẮT ĐẦU NGAY

**Upload `test_results.ttl` ngay bây giờ!**

Sau đó chạy query tổng quan để xem kết quả cuối cùng.

---

**Sắp hoàn thành rồi! 🎉**

