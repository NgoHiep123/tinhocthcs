# 🔍 DEBUG: TẦNG C CÓ SỐ LƯỢNG THẤP

## ⚠️ VẤN ĐỀ

- Questions: **39** (kỳ vọng ~2000)
- Tests: **23** (kỳ vọng ~300)
- Tổng triples: **1270** (kỳ vọng ~4,500-5,500)

**→ Có thể file chưa upload đầy đủ hoặc có lỗi**

---

## 🔍 KIỂM TRA NGAY

### **Query 1: Kiểm tra Questions có tồn tại không**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(*) as ?questionCount)
WHERE {
  ?question a edu:Question
}
```

**Kết quả:** 39 (thấp hơn kỳ vọng)

---

### **Query 2: Xem một số Questions**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?question ?q_id ?questionText
WHERE {
  ?question a edu:Question ;
            edu:q_id ?q_id ;
            edu:questionText ?questionText
}
LIMIT 10
```

**Mục đích:** Xem questions có được upload đúng không

---

### **Query 3: Kiểm tra Tests**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?test ?testId ?testName
WHERE {
  ?test a edu:Test ;
        edu:testId ?testId .
  OPTIONAL { ?test edu:testName ?testName }
}
LIMIT 10
```

---

## 🔧 NGUYÊN NHÂN CÓ THỂ

### **1. File có lỗi syntax**
- Một số dòng bị lỗi → GraphDB bỏ qua
- Encoding không đúng UTF-8
- Thiếu dấu `.` ở cuối statement

### **2. File quá lớn**
- GraphDB Desktop có giới hạn
- Upload bị cắt

### **3. Namespace không đúng**
- URI không khớp với schema

---

## ✅ GIẢI PHÁP

### **BƯỚC 1: Kiểm tra file có lỗi không**

Mở file `questions_updated.ttl` và kiểm tra:
- Có đầy đủ prefix không?
- Mỗi statement có dấu `.` ở cuối không?
- Encoding là UTF-8 không?

---

### **BƯỚC 2: Kiểm tra số dòng file**

```bash
# Đếm số dòng trong file
wc -l KG_Design/data/grade6/ttl/questions_updated.ttl
```

**Nếu file có hàng nghìn dòng nhưng chỉ upload được 39 → Có lỗi**

---

### **BƯỚC 3: Thử upload lại**

1. **Xóa data cũ (nếu cần):**
   ```sparql
   # Xóa tất cả questions
   PREFIX edu: <http://education.vn/ontology#>
   DELETE WHERE {
     ?question a edu:Question ;
               ?p ?o
   }
   ```

2. **Upload lại file**

---

## 📊 QUERY KIỂM TRA CHI TIẾT

### **Xem tất cả Questions với lesson:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?question ?q_id ?lessonId
WHERE {
  ?question a edu:Question ;
            edu:q_id ?q_id ;
            edu:belongsToLesson ?lessonIRI .
  ?lessonIRI edu:lessonId ?lessonId
}
ORDER BY ?lessonId ?q_id
LIMIT 50
```

**Mục đích:** Xem questions có được link với lessons không

---

### **Đếm Questions theo lesson:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?lessonId (COUNT(?question) as ?questionCount)
WHERE {
  ?question a edu:Question ;
            edu:belongsToLesson ?lessonIRI .
  ?lessonIRI edu:lessonId ?lessonId
}
GROUP BY ?lessonId
ORDER BY ?lessonId
```

**Kỳ vọng:** Mỗi lesson có nhiều questions

---

## 🎯 QUYẾT ĐỊNH

### **Option 1: Tiếp tục với số lượng hiện tại**

Nếu 39 questions và 23 tests đủ cho mục đích test → Tiếp tục với Tầng D

### **Option 2: Sửa và upload lại**

Nếu cần đầy đủ dữ liệu → Kiểm tra và sửa file, upload lại

---

## 🚀 BƯỚC TIẾP THEO

### **Nếu quyết định tiếp tục:**

**Tầng D - Relationship Data:**
```
10. prerequisites.ttl
11. teachers_assignments.ttl
12. question_skill.ttl
13. resource_skill.ttl
14. questions_in_tests.ttl
```

---

## 📋 CHECKLIST

```
□ Query 1: COUNT questions → 39 (thấp)
□ Query 2: Xem một số questions → Có dữ liệu không?
□ Query 3: Xem tests → Có dữ liệu không?
□ Quyết định: Tiếp tục hay sửa lại?
```

---

**Hãy chạy Query 2 và Query 3 để xem dữ liệu có đúng không! 🔍**

