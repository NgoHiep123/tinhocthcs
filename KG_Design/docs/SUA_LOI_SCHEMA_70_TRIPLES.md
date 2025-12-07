# 🔧 SỬA LỖI: SCHEMA CHỈ CÓ 70 TRIPLES

## ⚠️ VẤN ĐỀ

- Query 1: Chỉ có **70 triples** (kỳ vọng ~500)
- Query 2, 3: **No data available**

## 🔍 NGUYÊN NHÂN CÓ THỂ

### 1. **Schema chưa upload đầy đủ**
- File bị cắt khi upload
- Chỉ upload được một phần
- Lỗi encoding

### 2. **File schema có vấn đề**
- File bị lỗi format
- Thiếu dòng
- Encoding không đúng UTF-8

### 3. **GraphDB import có vấn đề**
- Import bị dừng giữa chừng
- Lỗi parsing
- Base URI không đúng

---

## ✅ GIẢI PHÁP

### **BƯỚC 1: Kiểm tra file schema**

Mở file `KG_Design/schema/kg_schema_chuan.ttl` và kiểm tra:

1. **File có đầy đủ 359 dòng không?**
   - Mở file → Xem số dòng cuối cùng
   - Phải là dòng 359

2. **Encoding là UTF-8?**
   - File → Save As → Encoding: UTF-8

3. **Có lỗi syntax không?**
   - Kiểm tra các dòng có dấu `.` ở cuối
   - Kiểm tra các prefix có đúng không

---

### **BƯỚC 2: Xóa và upload lại schema**

#### **Option A: Clear repository và upload lại**

```
1. GraphDB Desktop
2. Chọn repository "tinhocthcs"
3. Setup → Repositories → Edit
4. Clear repository (hoặc Delete và tạo lại)
5. Import → RDF → Upload RDF files
6. Chọn file: KG_Design/schema/kg_schema_chuan.ttl
7. Base URI: Để trống hoặc: http://education.vn/ontology#
8. Import
9. Đợi hoàn thành
```

#### **Option B: Upload vào named graph riêng**

```
1. Import → RDF
2. Upload file
3. Named graph: http://education.vn/ontology/schema
4. Import
```

---

### **BƯỚC 3: Kiểm tra sau khi upload lại**

#### **Query 1: Đếm lại triples**

```sparql
SELECT (COUNT(*) as ?count) 
WHERE {
  ?s ?p ?o
}
```

**Kỳ vọng:** ~500 triples

#### **Query 2: Kiểm tra namespace**

```sparql
SELECT DISTINCT ?namespace
WHERE {
  ?s ?p ?o
  BIND(REPLACE(STR(?s), "/[^/]*$", "") AS ?namespace)
}
ORDER BY ?namespace
```

**Kỳ vọng:** Thấy `http://education.vn/ontology#`

#### **Query 3: Kiểm tra classes (không filter)**

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?class ?label
WHERE {
  ?class a rdfs:Class .
  OPTIONAL { ?class rdfs:label ?label }
}
ORDER BY ?class
```

**Kỳ vọng:** Thấy 12 classes với namespace `http://education.vn/ontology#`

---

## 🔍 QUERIES DEBUG (Chạy ngay)

### **Query A: Xem tất cả triples (50 đầu tiên)**

```sparql
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o
}
LIMIT 50
```

**Mục đích:** Xem thực tế có gì trong repository

---

### **Query B: Tìm namespace "education"**

```sparql
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o
  FILTER(CONTAINS(STR(?s), "education") || 
         CONTAINS(STR(?p), "education") ||
         CONTAINS(STR(?o), "education"))
}
LIMIT 50
```

**Mục đích:** Xem có triples nào với namespace edu: không

---

### **Query C: Đếm theo loại**

```sparql
SELECT 
  (COUNT(*) as ?total) 
  (COUNT(DISTINCT ?s) as ?subjects)
  (COUNT(DISTINCT ?p) as ?predicates)
  (COUNT(DISTINCT ?o) as ?objects)
WHERE {
  ?s ?p ?o
}
```

**Mục đích:** Xem tổng quan về dữ liệu

---

## 🎯 HƯỚNG DẪN UPLOAD LẠI CHI TIẾT

### **Cách 1: Clear và upload lại (Khuyên dùng)**

```
1. Mở GraphDB Desktop
2. Chọn repository "tinhocthcs"
3. Setup → Repositories
4. Chọn "tinhocthcs" → Edit
5. Scroll xuống → "Clear repository"
6. Confirm
7. Quay lại repository
8. Import → RDF
9. Upload RDF files
10. Chọn: KG_Design/schema/kg_schema_chuan.ttl
11. Base URI: (Để trống hoặc: http://education.vn/ontology#)
12. Click Import
13. Đợi hoàn thành (có thể mất vài giây)
14. Kiểm tra lại với Query 1
```

---

### **Cách 2: Tạo repository mới**

```
1. Setup → Repositories → Create new repository
2. Repository ID: tinhoc_thcs_new
3. Ruleset: RDFS-Plus (hoặc OWL-Horst)
4. Create
5. Import → RDF → Upload file schema
6. Test
7. Nếu OK → Xóa repository cũ, đổi tên repository mới
```

---

## ⚠️ LƯU Ý KHI UPLOAD

### **1. Base URI**
- **Để trống** (GraphDB sẽ tự nhận)
- HOẶC: `http://education.vn/ontology#`
- **KHÔNG** thêm `/` ở cuối

### **2. File encoding**
- Phải là **UTF-8**
- Không phải UTF-8 BOM

### **3. File format**
- Phải là `.ttl` (Turtle format)
- Không phải `.txt` hoặc format khác

### **4. Import settings**
- **Context/Named graph:** Để trống (default graph)
- **Inference:** Bật (nếu dùng RDFS-Plus)

---

## ✅ CHECKLIST SAU KHI UPLOAD LẠI

```
□ Query 1: Count triples ~500
□ Query 2: Thấy namespace "http://education.vn/ontology#"
□ Query 3: Thấy 12 classes
□ Query 4: Thấy 25+ properties
□ Query 5: Thấy 17 relationships
```

---

## 🐛 NẾU VẪN LỖI

### **Kiểm tra file schema:**

1. **Mở file** `KG_Design/schema/kg_schema_chuan.ttl`
2. **Kiểm tra:**
   - Dòng cuối cùng là dòng 359
   - Có đầy đủ prefix declarations
   - Không có lỗi syntax
   - Encoding UTF-8

3. **Test file:**
   - Copy một phần nhỏ (10-20 dòng đầu)
   - Tạo file test.ttl
   - Upload test.ttl
   - Xem có lỗi gì không

### **Kiểm tra GraphDB:**

1. **Version GraphDB Desktop:**
   - Phải là version mới nhất
   - Update nếu cần

2. **Memory settings:**
   - Setup → Settings
   - Tăng heap size nếu cần

3. **Logs:**
   - Xem logs trong GraphDB
   - Tìm lỗi import

---

## 📞 BÁO CÁO LỖI

Nếu vẫn không được, gửi cho tôi:

1. **Kết quả Query A, B, C** (từ queries debug)
2. **Số dòng file schema** (mở file, xem dòng cuối)
3. **Version GraphDB Desktop**
4. **Lỗi trong logs** (nếu có)

---

## 🎯 KẾT QUẢ MONG ĐỢI SAU KHI SỬA

```
✅ Query 1: ~500 triples
✅ Query 2: Thấy 12 classes với namespace edu:
✅ Query 3: Thấy 25+ properties
✅ Query 4: Thấy 17 relationships
✅ Tất cả queries trong queries_kiem_tra_schema.txt chạy OK
```

---

**Hãy thử upload lại schema và chạy các queries debug! 🔧**

