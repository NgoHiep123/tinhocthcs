# ✅ KIỂM TRA SCHEMA VỚI 319 TRIPLES

## 📊 TÌNH TRẠNG HIỆN TẠI

- ✅ Query 1: **319 triples** (tốt hơn 70, nhưng chưa đạt ~500)
- ⏳ Cần kiểm tra xem đã đủ classes và properties chưa

---

## 🔍 BƯỚC 1: KIỂM TRA CLASSES

### **Query kiểm tra Classes:**

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?class ?label
WHERE {
  ?class a rdfs:Class .
  OPTIONAL { ?class rdfs:label ?label }
}
ORDER BY ?class
```

**Kỳ vọng:** Thấy 12 classes:
- Student (Học sinh)
- Teacher (Giáo viên)
- Class (Lớp học)
- Grade (Khối)
- Topic (Chủ đề)
- Lesson (Bài học)
- Question (Câu hỏi)
- Skill (Kỹ năng)
- Resource (Tài nguyên)
- Test (Bài kiểm tra)
- TestResult (Kết quả)
- Mastery (Mức độ thành thạo)

**Nếu thấy đủ 12 classes → Schema OK! ✅**

---

## 🔍 BƯỚC 2: KIỂM TRA PROPERTIES

### **Query kiểm tra Properties:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?property ?label
WHERE {
  ?property a rdf:Property .
  OPTIONAL { ?property rdfs:label ?label }
}
ORDER BY ?property
```

**Kỳ vọng:** Thấy 25+ properties

**Nếu thấy đủ properties → Schema OK! ✅**

---

## 🔍 BƯỚC 3: KIỂM TRA NAMESPACE

### **Query kiểm tra namespace:**

```sparql
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o
  FILTER(CONTAINS(STR(?s), "education") || 
         CONTAINS(STR(?p), "education") ||
         CONTAINS(STR(?o), "education"))
}
LIMIT 20
```

**Kỳ vọng:** Thấy các triples với namespace `http://education.vn/ontology#`

---

## 💡 GIẢI THÍCH VỀ 319 TRIPLES

### **Tại sao không phải ~500?**

Có thể:
1. **File schema thực tế có ít triples hơn** (do cách đếm)
2. **Một số triples bị trùng** (GraphDB tự động merge)
3. **Chỉ đếm triples chính** (không đếm metadata)

### **Quan trọng:**
- **Số lượng triples không quan trọng bằng việc có đủ classes và properties**
- **Nếu có đủ 12 classes và 25+ properties → Schema OK!**

---

## ✅ CHECKLIST KIỂM TRA

```
□ Query Classes: Thấy 12 classes
□ Query Properties: Thấy 25+ properties  
□ Query Namespace: Thấy namespace "education"
□ Tất cả classes có label tiếng Việt
□ Tất cả properties có label tiếng Việt
```

---

## 🎯 NẾU ĐỦ CLASSES VÀ PROPERTIES

### **→ Schema đã sẵn sàng!**

**Bước tiếp theo:**
1. ✅ Schema OK
2. ⏭️ Upload **Tầng B - Master Data**
   - Bắt đầu với: `grades.ttl`

---

## 📋 QUERIES KIỂM TRA NHANH

### **Query tổng hợp:**

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT 
  (COUNT(DISTINCT ?class) as ?classCount)
  (COUNT(DISTINCT ?property) as ?propertyCount)
WHERE {
  { ?class a rdfs:Class }
  UNION
  { ?property a rdf:Property }
}
```

**Kỳ vọng:**
- classCount: 12
- propertyCount: 25+

---

## 🚀 HÀNH ĐỘNG TIẾP THEO

### **Nếu đủ 12 classes và 25+ properties:**

1. ✅ **Schema đã OK!**
2. ⏭️ **Bắt đầu upload Tầng B:**
   ```
   - grades.ttl
   - classes.ttl
   - topics.ttl
   - skills.ttl
   - lessons.ttl
   - resources.ttl
   ```

### **Nếu thiếu classes/properties:**

1. ⚠️ **Kiểm tra lại file schema**
2. ⚠️ **Upload lại schema**
3. ⚠️ **Kiểm tra logs trong GraphDB**

---

**Hãy chạy các queries kiểm tra trên và cho tôi biết kết quả! 🔍**

