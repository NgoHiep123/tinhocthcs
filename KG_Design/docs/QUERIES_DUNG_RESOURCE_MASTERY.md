# ✅ QUERIES ĐÚNG CHO RESOURCE_SKILL VÀ MASTERY

## ⚠️ VẤN ĐỀ

### **1. resource_skill.ttl:**
- Dùng class `edu:Coverage` (không có trong schema hiện tại)
- Dùng properties: `edu:resource`, `edu:skill`, `edu:coverage`
- **KHÔNG** dùng `edu:coversSkill`

### **2. mastery.ttl:**
- Dùng properties: `edu:student`, `edu:skill` (không phải `edu:forSkill`)
- Student URI: `<http://education.vn/data/student/2324_0001>` (khác với `data:student_2324_0001`)

---

## ✅ QUERY ĐÚNG CHO RESOURCE_SKILL

### **Query 1: Kiểm tra Coverage có tồn tại không**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(*) as ?coverageCount)
WHERE {
  ?coverage a edu:Coverage
}
```

**Kỳ vọng:** > 0 (nếu class Coverage được định nghĩa trong schema)

**Nếu = 0:** Class `edu:Coverage` chưa được định nghĩa trong schema

---

### **Query 2: Xem Coverage (nếu có class này)**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?coverage ?resource ?skill ?coverageValue
WHERE {
  ?coverage a edu:Coverage ;
            edu:resource ?resource ;
            edu:skill ?skill ;
            edu:coverage ?coverageValue
}
LIMIT 20
```

---

### **Query 3: Kiểm tra bằng cách tìm triples trực tiếp**

```sparql
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o
  FILTER(STRSTARTS(STR(?s), "http://education.vn/data/cover/") || 
         STRSTARTS(STR(?p), "http://education.vn/ontology#resource") ||
         STRSTARTS(STR(?p), "http://education.vn/ontology#skill"))
}
LIMIT 20
```

**Mục đích:** Xem có triples nào với namespace "cover" không

---

## ✅ QUERY ĐÚNG CHO MASTERY

### **Query 1: Kiểm tra Mastery có tồn tại không**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(*) as ?masteryCount)
WHERE {
  ?mastery a edu:Mastery
}
```

**Kỳ vọng:** > 0

---

### **Query 2: Xem Mastery với format thực tế**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?mastery ?studentIRI ?skillIRI ?score ?lastUpdated
WHERE {
  ?mastery a edu:Mastery ;
           edu:student ?studentIRI ;
           edu:skill ?skillIRI ;
           edu:score ?score .
  OPTIONAL { ?mastery edu:lastUpdated ?lastUpdated }
}
LIMIT 20
```

**Kỳ vọng:** Thấy mastery với student và skill (nhưng có thể không join được với students vì URI khác)

---

### **Query 3: Join với Students (nếu URI khớp)**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?mastery ?studentIRI ?studentId ?fullName ?skillIRI ?score
WHERE {
  ?mastery a edu:Mastery ;
           edu:student ?studentIRI ;
           edu:skill ?skillIRI ;
           edu:score ?score .
  
  # Thử join với students (có thể không khớp vì URI khác)
  OPTIONAL {
    ?studentIRI edu:studentId ?studentId ;
                edu:fullName ?fullName
  }
}
LIMIT 20
```

**Lưu ý:** Có thể không join được vì URI format khác:
- mastery.ttl: `<http://education.vn/data/student/2324_0001>`
- students_updated.ttl: `data:student_2324_0001` = `<http://education.vn/data/student_2324_0001>`

---

### **Query 4: Kiểm tra Student URI trong Mastery**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT DISTINCT ?studentIRI
WHERE {
  ?mastery a edu:Mastery ;
           edu:student ?studentIRI
}
LIMIT 10
```

**Mục đích:** Xem format URI của student trong mastery

---

## 🔧 VẤN ĐỀ VỚI SCHEMA

### **Problem 1: Class `edu:Coverage` không có trong schema**

Schema hiện tại chỉ có:
- `edu:Resource` có property `edu:coversSkill`
- **KHÔNG** có class `edu:Coverage`

**Giải pháp:**
- **Option 1:** Thêm class `edu:Coverage` vào schema
- **Option 2:** Sửa file để dùng `edu:coversSkill` trực tiếp trên Resource

---

### **Problem 2: Properties trong mastery.ttl khác schema**

Schema định nghĩa:
- `edu:forSkill` (Mastery → Skill)
- `edu:hasMastery` (Student → Mastery)

File mastery.ttl dùng:
- `edu:student` (Mastery → Student) - **KHÔNG có trong schema**
- `edu:skill` (Mastery → Skill) - **KHÔNG có trong schema**

**Giải pháp:**
- **Option 1:** Cập nhật schema để có properties này
- **Option 2:** Sửa file để dùng đúng schema

---

## 🚀 QUERIES TẠM THỜI (KHÔNG CẦN SCHEMA)

### **Query xem tất cả triples của Coverage:**

```sparql
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o
  FILTER(CONTAINS(STR(?s), "/cover/") || 
         CONTAINS(STR(?s), "/Coverage"))
}
LIMIT 20
```

---

### **Query xem tất cả triples của Mastery:**

```sparql
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o
  FILTER(CONTAINS(STR(?s), "/mastery/"))
}
LIMIT 20
```

---

## ✅ HÀNH ĐỘNG TIẾP THEO

### **Nếu muốn tiếp tục:**

1. **Kiểm tra xem file đã upload chưa:**
   ```sparql
   SELECT (COUNT(*) as ?total) WHERE { ?s ?p ?o }
   ```

2. **Nếu số triples tăng → File đã upload (nhưng schema không khớp)**

3. **Có 2 lựa chọn:**
   - **A:** Cập nhật schema để phù hợp với file
   - **B:** Sửa file để phù hợp với schema

---

## 🎯 KHUYẾN NGHỊ

**Nếu chỉ để test:** Tiếp tục upload, queries trên vẫn có thể chạy được (không cần schema validation)

**Nếu cần đúng chuẩn:** Nên sửa file hoặc cập nhật schema

---

**Hãy chạy Query 1 và Query 2 của mỗi phần để xem kết quả! 🔍**

