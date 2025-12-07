# 🔍 DEBUG: Query Students Không Có Kết Quả

## ⚠️ VẤN ĐỀ

Query không trả về kết quả sau khi upload `students_updated.ttl`

---

## 🔍 NGUYÊN NHÂN CÓ THỂ

### **1. Class reference không khớp**

File `students_updated.ttl` dùng: `data:class_6_1`
File `classes.ttl` có thể dùng: `data:class_6A` hoặc format khác

---

## ✅ GIẢI PHÁP

### **BƯỚC 1: Kiểm tra xem có Students trong repository không**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(*) as ?studentCount)
WHERE {
  ?student a edu:Student
}
```

**Nếu count > 0:** Students đã được upload, vấn đề là ở query
**Nếu count = 0:** Students chưa được upload hoặc có lỗi

---

### **BƯỚC 2: Kiểm tra Students không cần join với Class**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?studentId ?fullName
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName
}
LIMIT 20
```

**Nếu có kết quả:** Vấn đề là ở `belongsToClass`
**Nếu không có kết quả:** Students chưa được upload

---

### **BƯỚC 3: Kiểm tra Classes có tồn tại không**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?class ?className
WHERE {
  ?class a edu:Class ;
         edu:className ?className
}
ORDER BY ?className
LIMIT 20
```

**Xem format của className:** `6_1`, `6A`, `6/1`, etc.

---

### **BƯỚC 4: Kiểm tra belongsToClass trực tiếp**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?classIRI
WHERE {
  ?student a edu:Student ;
           edu:belongsToClass ?classIRI
}
LIMIT 20
```

**Xem classIRI có format gì:** `data:class_6_1`, `data:class_6A`, etc.

---

### **BƯỚC 5: Query đơn giản nhất - Tất cả Students**

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student
WHERE {
  ?student a edu:Student
}
LIMIT 10
```

**Nếu không có kết quả:** Students chưa được upload thành công

---

## 🔧 NẾU STUDENTS CHƯA ĐƯỢC UPLOAD

### **Kiểm tra lỗi:**

1. **Xem logs trong GraphDB Desktop**
   - Có lỗi import không?
   - File có được parse đúng không?

2. **Kiểm tra file có lỗi syntax không**
   - Mở file `students_updated.ttl`
   - Kiểm tra encoding UTF-8
   - Kiểm tra có dấu `.` ở cuối mỗi statement

3. **Thử upload lại**
   - Clear repository (nếu cần)
   - Upload lại file

---

## 🔧 NẾU CLASS REFERENCE KHÔNG KHỚP

### **Vấn đề:**
- `students_updated.ttl` dùng: `data:class_6_1`
- `classes.ttl` có thể dùng: `data:class_6A`

### **Giải pháp:**

**Option 1: Sửa file `students_updated.ttl`**
- Thay `data:class_6_1` → `data:class_6A` (hoặc format đúng)

**Option 2: Sửa file `classes.ttl`**
- Đảm bảo có class với ID `data:class_6_1`

**Option 3: Query không join với Class**

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

---

## 📋 CHECKLIST DEBUG

```
□ Query 1: COUNT students → Có > 0 không?
□ Query 2: Students không join Class → Có kết quả không?
□ Query 3: List Classes → Format className là gì?
□ Query 4: belongsToClass trực tiếp → classIRI là gì?
□ Query 5: Tất cả Students → Có kết quả không?
```

---

## 🚀 HÀNH ĐỘNG NGAY

**Chạy Query 1 và Query 2 trước:**

```sparql
# Query 1: Đếm Students
PREFIX edu: <http://education.vn/ontology#>
SELECT (COUNT(*) as ?studentCount)
WHERE {
  ?student a edu:Student
}

# Query 2: Students không join
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?studentId ?fullName
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName
}
LIMIT 20
```

**Gửi kết quả cho tôi để phân tích tiếp!**

