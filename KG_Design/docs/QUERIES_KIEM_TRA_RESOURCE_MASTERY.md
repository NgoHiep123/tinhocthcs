# 🔍 QUERIES KIỂM TRA RESOURCE_SKILL VÀ MASTERY

## ⚠️ VẤN ĐỀ

File không khớp với schema:
- `resource_skill.ttl`: Dùng class `edu:Coverage` (không có trong schema)
- `mastery.ttl`: Dùng `edu:student`, `edu:skill` (không đúng schema)

---

## ✅ QUERIES ĐƠN GIẢN - KIỂM TRA DỮ LIỆU

### **Query 1: Kiểm tra resource_skill.ttl đã upload chưa**

```sparql
SELECT (COUNT(*) as ?count)
WHERE {
  ?s ?p ?o
  FILTER(CONTAINS(STR(?s), "/cover/") || 
         CONTAINS(STR(?s), "/Coverage"))
}
```

**Kỳ vọng:** > 0 nếu file đã upload

---

### **Query 2: Xem triples của Coverage**

```sparql
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o
  FILTER(CONTAINS(STR(?s), "/cover/"))
}
LIMIT 10
```

**Kỳ vọng:** Thấy các triples với namespace "cover"

---

### **Query 3: Kiểm tra mastery.ttl đã upload chưa**

```sparql
SELECT (COUNT(*) as ?count)
WHERE {
  ?s ?p ?o
  FILTER(CONTAINS(STR(?s), "/mastery/"))
}
```

**Kỳ vọng:** > 0 nếu file đã upload

---

### **Query 4: Xem triples của Mastery**

```sparql
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o
  FILTER(CONTAINS(STR(?s), "/mastery/"))
}
LIMIT 10
```

**Kỳ vọng:** Thấy các triples với namespace "mastery"

---

### **Query 5: Kiểm tra Mastery có property edu:student không**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?mastery ?studentIRI ?skillIRI ?score
WHERE {
  ?mastery ?p1 ?studentIRI ;
           ?p2 ?skillIRI ;
           edu:score ?score .
  FILTER(?p1 = edu:student && ?p2 = edu:skill)
}
LIMIT 10
```

**Hoặc đơn giản hơn:**

```sparql
SELECT ?s ?p ?o
WHERE {
  ?s <http://education.vn/ontology#student> ?o
}
LIMIT 10
```

---

### **Query 6: Kiểm tra Coverage có property edu:resource không**

```sparql
SELECT ?s ?p ?o
WHERE {
  ?s <http://education.vn/ontology#resource> ?o
}
LIMIT 10
```

---

## 📊 QUERY TỔNG QUAN

### **Kiểm tra tổng số triples:**

```sparql
SELECT (COUNT(*) as ?totalTriples) 
WHERE {
  ?s ?p ?o
}
```

**Sau resource_skill.ttl:** Tăng thêm ~30-50 triples
**Sau mastery.ttl:** Tăng thêm ~400-500 triples

---

## 🔍 QUERY XEM TẤT CẢ CLASSES TRONG REPOSITORY

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?class
WHERE {
  ?instance a ?class
}
ORDER BY ?class
```

**Xem có class `edu:Coverage` không**

---

## ✅ NẾU DỮ LIỆU ĐÃ ĐƯỢC UPLOAD

Có thể queries không hoạt động vì:
1. Schema không khớp với file
2. Properties không đúng như định nghĩa trong schema

**Nhưng dữ liệu vẫn có trong repository!**

---

## 🚀 HÀNH ĐỘNG NGAY

**Chạy các queries đơn giản trên để kiểm tra:**
1. Query 1: Đếm triples có "/cover/"
2. Query 3: Đếm triples có "/mastery/"
3. Query tổng quan: Xem tổng số triples có tăng không

**Nếu có triples → File đã upload thành công!**

---

**Hãy chạy các queries đơn giản trên và cho tôi biết kết quả! 🔍**

