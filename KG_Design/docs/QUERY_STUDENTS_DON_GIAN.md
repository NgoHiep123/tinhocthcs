# 🔍 QUERY STUDENTS ĐƠN GIẢN (KHÔNG CẦN JOIN CLASS)

## ⚠️ VẤN ĐỀ

Query join với Class không có kết quả vì file `classes.ttl` trống.

---

## ✅ GIẢI PHÁP TẠM THỜI

### **Query Students không cần join với Class:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?studentId ?fullName ?classIRI
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:belongsToClass ?classIRI
}
ORDER BY ?studentId
LIMIT 20
```

**Query này sẽ trả về:**
- student: URI của học sinh
- studentId: Mã học sinh
- fullName: Tên học sinh
- classIRI: URI của lớp (data:class_6_1)

---

## 🔧 ĐÃ TẠO FILE `classes.ttl`

Tôi đã tạo file `classes.ttl` với class `data:class_6_1`.

### **Bước tiếp theo:**

1. **Upload file `classes.ttl` mới:**
   ```
   GraphDB Desktop → Import → RDF
   Chọn: KG_Design/data/grade6/ttl/classes.ttl
   Import
   ```

2. **Sau đó query ban đầu sẽ hoạt động:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?studentId ?fullName ?className
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:belongsToClass ?classIRI .
  ?classIRI edu:className ?className
}
ORDER BY ?className ?studentId
LIMIT 20
```

---

## 🔍 KIỂM TRA TRƯỚC KHI UPLOAD CLASSES

### **Query 1: Kiểm tra Students có tồn tại không**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(*) as ?studentCount)
WHERE {
  ?student a edu:Student
}
```

**Kỳ vọng:** > 0 (có students)

---

### **Query 2: Xem Students và classIRI**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?studentId ?fullName ?classIRI
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:belongsToClass ?classIRI
}
LIMIT 10
```

**Kỳ vọng:** Thấy students với `classIRI = data:class_6_1`

---

## ✅ SAU KHI UPLOAD CLASSES.TTL

### **Query kiểm tra Class:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?class ?className ?grade
WHERE {
  ?class a edu:Class ;
         edu:className ?className ;
         edu:belongsToGrade ?gradeIRI .
  ?gradeIRI edu:grade ?grade
}
```

**Kỳ vọng:** Thấy `data:class_6_1` với `className = "6/1"` và `grade = 6`

---

## 🚀 HÀNH ĐỘNG NGAY

1. **Chạy Query 1 và Query 2** để xác nhận students đã được upload
2. **Upload file `classes.ttl` mới** (đã được tạo)
3. **Chạy lại query ban đầu** → Sẽ có kết quả!

---

**Hãy thử các queries trên và cho tôi biết kết quả! 🔍**

