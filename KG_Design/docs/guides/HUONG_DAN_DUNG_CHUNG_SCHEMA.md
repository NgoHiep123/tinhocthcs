# 📘 HƯỚNG DẪN DÙNG CHUNG SCHEMA KHỐI 7 CHO KHỐI 6

## 🎯 MỤC ĐÍCH

Chuyển đổi namespace của các file TTL Khối 6 để có thể dùng chung schema `kg_schema_grade7.ttl` với Khối 7.

---

## 📋 SO SÁNH NAMESPACE

| Khối | Ontology Namespace | Data Namespace |
|------|-------------------|----------------|
| **Khối 6 (hiện tại)** | `https://example.org/edu#` | `https://example.org/kg/` |
| **Khối 7** | `http://education.vn/ontology#` | `http://education.vn/data/` |

**→ Cần chuyển đổi Khối 6 sang namespace của Khối 7**

---

## 🚀 CÁC BƯỚC THỰC HIỆN

### **Bước 1: Chuyển đổi namespace các file TTL Khối 6**

Chạy script chuyển đổi:

```bash
cd KG_Design/grade6
python convert_to_grade7_namespace.py
```

**Kết quả:**
- Script sẽ tạo thư mục `out_converted/`
- Tất cả file TTL đã chuyển đổi namespace sẽ nằm trong thư mục này

**Các file được chuyển đổi:**
- ✅ `skills.ttl`
- ✅ `resources.ttl`
- ✅ `resource_skill.ttl`
- ✅ `prerequisites.ttl`
- ✅ `question_skill.ttl`
- ✅ `students.ttl`
- ✅ `mastery.ttl`
- ✅ `teachers_assignments.ttl`

---

### **Bước 2: Upload vào GraphDB Desktop**

#### **2.1. Tạo Repository mới (nếu chưa có)**

1. Mở GraphDB Desktop
2. Click **"New Repository"**
3. Đặt tên: `THCS_All_Grades` (hoặc tên khác)
4. Chọn **OWL-Horst** hoặc **OWL2-RL** (khuyến nghị)
5. Click **"Create"**

#### **2.2. Upload Schema (BẮT BUỘC - PHẢI LÀM TRƯỚC)**

1. Vào tab **"Import"**
2. Click **"Add file"**
3. Chọn file: `KG_Design/kg_schema_grade7.ttl`
4. Click **"Import"**
5. ✅ Đợi import xong (quan trọng!)

**Lưu ý:** Schema phải được import **TRƯỚC** các file dữ liệu!

#### **2.3. Upload dữ liệu Khối 6 (đã chuyển đổi)**

1. Vào tab **"Import"**
2. Click **"Add file"** (hoặc **"Add folder"**)
3. Chọn thư mục: `KG_Design/grade6/out_converted/`
4. Hoặc chọn từng file một theo thứ tự:
   - `skills.ttl`
   - `resources.ttl`
   - `students.ttl`
   - `teachers_assignments.ttl`
   - `prerequisites.ttl`
   - `question_skill.ttl`
   - `resource_skill.ttl`
   - `mastery.ttl`
5. Click **"Import"**

#### **2.4. Upload dữ liệu Khối 7 (tùy chọn)**

1. Vào tab **"Import"**
2. Click **"Add file"**
3. Chọn file: `KG_Design/kg_grade7.ttl`
4. Click **"Import"**

---

## ✅ KIỂM TRA SAU KHI UPLOAD

### **Test 1: Kiểm tra Schema**

Chạy query sau để xem các class đã được định nghĩa:

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?class ?label
WHERE {
  ?class a rdfs:Class .
  ?class rdfs:label ?label .
}
ORDER BY ?label
```

**Kết quả mong đợi:** Thấy các class như `Student`, `Teacher`, `Skill`, `Resource`, ...

### **Test 2: Kiểm tra dữ liệu Khối 6**

```sparql
PREFIX data: <http://education.vn/data/>
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(?student) AS ?count)
WHERE {
  ?student a edu:Student .
  ?student edu:studentId ?id .
  FILTER(STRSTARTS(STR(?id), "2324"))
}
```

**Kết quả mong đợi:** Số lượng học sinh Khối 6

### **Test 3: Kiểm tra dữ liệu Khối 7**

```sparql
PREFIX data: <http://education.vn/data/>
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(?student) AS ?count)
WHERE {
  ?student a edu:Student .
  ?student edu:fullName ?name .
  FILTER(CONTAINS(STR(?student), "student_7_"))
}
```

**Kết quả mong đợi:** Số lượng học sinh Khối 7

### **Test 4: Kiểm tra giáo viên (có thể trùng)**

```sparql
PREFIX data: <http://education.vn/data/>
PREFIX edu: <http://education.vn/ontology#>

SELECT ?teacher ?name ?id
WHERE {
  ?teacher a edu:Teacher .
  ?teacher edu:teacherId "tin_01" .
  OPTIONAL { ?teacher edu:fullName ?name }
  OPTIONAL { ?teacher edu:teacherId ?id }
}
```

**Lưu ý:** Có thể có 2 bản ghi cho cùng một giáo viên (một từ Khối 6, một từ Khối 7)

---

## ⚠️ LƯU Ý QUAN TRỌNG

### **1. Thứ tự import**

**BẮT BUỘC:**
1. Schema trước (`kg_schema_grade7.ttl`)
2. Dữ liệu sau (các file TTL)

### **2. Namespace đã được chuyển đổi**

Sau khi chạy script, tất cả file trong `out_converted/` đã dùng namespace của Khối 7:
- ✅ `http://education.vn/ontology#` (cho properties)
- ✅ `http://education.vn/data/` (cho instances)

### **3. Có thể có trùng dữ liệu**

- **Giáo viên:** Cùng một giáo viên có thể có 2 IRI khác nhau (một từ Khối 6, một từ Khối 7)
- **Học sinh:** Học sinh Khối 6 và Khối 7 có cách định danh khác nhau nên không trùng

**Giải pháp:** Có thể dùng `owl:sameAs` để liên kết các thực thể giống nhau (nếu cần)

### **4. Query cần dùng đúng namespace**

Khi query, phải dùng namespace của Khối 7:

```sparql
PREFIX data: <http://education.vn/data/>
PREFIX edu: <http://education.vn/ontology#>
```

**KHÔNG dùng:**
```sparql
PREFIX ex: <https://example.org/kg/>  ❌
PREFIX edu: <https://example.org/edu#>  ❌
```

---

## 🔄 QUAY LẠI NAMESPACE CŨ (NẾU CẦN)

Nếu muốn quay lại dùng namespace riêng cho Khối 6:
- Các file gốc vẫn nằm trong `out/` (chưa bị thay đổi)
- Chỉ cần không dùng các file trong `out_converted/`

---

## 📊 TÓM TẮT

| Bước | Hành động | Kết quả |
|------|-----------|---------|
| 1 | Chạy script chuyển đổi | Tạo thư mục `out_converted/` |
| 2 | Upload `kg_schema_grade7.ttl` | Schema được định nghĩa |
| 3 | Upload file trong `out_converted/` | Dữ liệu Khối 6 với namespace Khối 7 |
| 4 | Upload `kg_grade7.ttl` (tùy chọn) | Dữ liệu Khối 7 |
| 5 | Test query | Kiểm tra dữ liệu đã đúng |

---

## 🆘 XỬ LÝ LỖI

### **Lỗi: "Unknown property"**

**Nguyên nhân:** Chưa upload schema hoặc upload sai thứ tự

**Giải pháp:**
1. Xóa repository
2. Tạo lại repository
3. Upload schema trước
4. Upload dữ liệu sau

### **Lỗi: "Invalid namespace"**

**Nguyên nhân:** File chưa được chuyển đổi namespace

**Giải pháp:**
1. Kiểm tra file trong `out_converted/` đã đúng namespace chưa
2. Chạy lại script `convert_to_grade7_namespace.py`

### **Lỗi: "Duplicate data"**

**Nguyên nhân:** Upload cùng một file 2 lần

**Giải pháp:**
1. Xóa dữ liệu cũ
2. Upload lại một lần

---

**Cập nhật:** $(date)

