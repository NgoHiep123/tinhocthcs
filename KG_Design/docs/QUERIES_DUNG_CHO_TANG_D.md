# ✅ QUERIES ĐÚNG CHO TẦNG D

## ⚠️ VẤN ĐỀ

Queries ban đầu không đúng vì:
1. **prerequisites.ttl**: Dùng `prerequisiteOf` giữa **Skills**, không phải Lessons
2. **teachers_assignments.ttl**: Dùng full URI, không dùng prefix `data:`

---

## ✅ QUERY ĐÚNG CHO PREREQUISITES

### **Query 1: Prerequisites giữa Skills**

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

**Kỳ vọng:** Thấy quan hệ tiên quyết giữa các kỹ năng

---

### **Query 2: Xem tất cả prerequisites (đơn giản)**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?prerequisite ?skill
WHERE {
  ?prerequisite edu:prerequisiteOf ?skill
}
LIMIT 20
```

**Kỳ vọng:** Thấy các cặp skill tiên quyết

---

## ✅ QUERY ĐÚNG CHO TEACHERS ASSIGNMENTS

### **Query 1: Teachers và Classes (dùng full URI)**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?teacher ?teacherId ?fullName ?classIRI
WHERE {
  ?teacher a edu:Teacher ;
           edu:teacherId ?teacherId ;
           edu:fullName ?fullName ;
           edu:teaches ?classIRI
}
LIMIT 20
```

**Kỳ vọng:** Thấy giáo viên và lớp họ dạy (classIRI sẽ là full URI)

---

### **Query 2: Teachers và Classes với className (nếu có)**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?teacher ?teacherId ?fullName ?classIRI ?className
WHERE {
  ?teacher a edu:Teacher ;
           edu:teacherId ?teacherId ;
           edu:fullName ?fullName ;
           edu:teaches ?classIRI .
  OPTIONAL {
    ?classIRI edu:className ?className
  }
}
LIMIT 20
```

**Lưu ý:** Có thể không có className vì class URI format khác

---

### **Query 3: Đếm số lớp mỗi giáo viên dạy**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?teacher ?teacherId ?fullName (COUNT(?class) as ?classCount)
WHERE {
  ?teacher a edu:Teacher ;
           edu:teacherId ?teacherId ;
           edu:fullName ?fullName ;
           edu:teaches ?class
}
GROUP BY ?teacher ?teacherId ?fullName
ORDER BY DESC(?classCount)
```

**Kỳ vọng:** Thấy mỗi giáo viên dạy bao nhiêu lớp

---

## 🔍 QUERIES KIỂM TRA TỔNG QUAN

### **Query 1: Kiểm tra Prerequisites có tồn tại không**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(*) as ?prerequisiteCount)
WHERE {
  ?s edu:prerequisiteOf ?o
}
```

**Kỳ vọng:** > 0 (có prerequisites)

---

### **Query 2: Kiểm tra Teachers có tồn tại không**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(*) as ?teacherCount)
WHERE {
  ?teacher a edu:Teacher
}
```

**Kỳ vọng:** > 0 (có teachers)

---

### **Query 3: Kiểm tra teaches relationships**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(*) as ?teachesCount)
WHERE {
  ?teacher edu:teaches ?class
}
```

**Kỳ vọng:** > 0 (có quan hệ teaches)

---

## 📊 QUERY XEM TẤT CẢ PREREQUISITES

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?prerequisite ?prerequisiteName ?skill ?skillName
WHERE {
  ?prerequisite edu:prerequisiteOf ?skill .
  OPTIONAL { ?prerequisite edu:name ?prerequisiteName }
  OPTIONAL { ?skill edu:name ?skillName }
}
LIMIT 30
```

---

## 📊 QUERY XEM TẤT CẢ TEACHERS

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?teacher ?teacherId ?fullName ?expertise
WHERE {
  ?teacher a edu:Teacher ;
           edu:teacherId ?teacherId ;
           edu:fullName ?fullName .
  OPTIONAL { ?teacher edu:expertise ?expertise }
}
ORDER BY ?teacherId
```

---

## 🎯 LƯU Ý

### **Về Prerequisites:**
- Quan hệ giữa **Skills**, không phải Lessons
- Dùng full URI: `<http://education.vn/data/skill/...>`
- Property: `edu:prerequisiteOf`

### **Về Teachers:**
- Dùng full URI: `<http://education.vn/data/teacher/...>`
- Class URI: `<http://education.vn/data/class/6_14>` (format khác với `data:class_6_1`)
- Có thể không join được với classes.ttl vì format khác

---

## 🚀 HÀNH ĐỘNG NGAY

**Chạy các queries trên để kiểm tra!**

1. Query đếm prerequisites
2. Query đếm teachers
3. Query xem prerequisites
4. Query xem teachers

---

**Các queries này sẽ hoạt động! ✅**

