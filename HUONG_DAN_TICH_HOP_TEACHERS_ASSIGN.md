# 📋 HƯỚNG DẪN TÍCH HỢP FILE `teachers_assign.csv`

## 📊 TỔNG QUAN

File `teachers_assign.csv` chứa thông tin **phân công giáo viên dạy các lớp**. File này đã được tích hợp vào hệ thống Knowledge Graph.

### **Cấu trúc file:**
```csv
Id_teacher,name,expertise,class
tin_01,Ngô Tiến Hiệp,Tin học,6/14
tin_01,Ngô Tiến Hiệp,Tin học,6/15
...
```

### **Các trường:**
- `Id_teacher`: Mã giáo viên (ví dụ: tin_01, tin_02, ...)
- `name`: Tên giáo viên
- `expertise`: Chuyên môn (thường là "Tin học")
- `class`: Lớp được phân công (ví dụ: 6/14, 7/19, ...)

---

## ✅ CÁC THAY ĐỔI ĐÃ THỰC HIỆN

### **1. Cập nhật Schema (`kg_schema_grade7.ttl`)**

Đã thêm 2 thuộc tính mới cho Teacher:
- `edu:teacherId` - Mã giáo viên
- `edu:expertise` - Chuyên môn

### **2. Cập nhật Script Build KG (`build_kg_grade7.py`)**

Đã thêm hàm `add_teachers_to_kg()` để:
- Đọc file `teachers_assign.csv`
- Tạo Teacher nodes trong Knowledge Graph
- Tạo relationship `teaches` (Teacher → Class)
- Tự động tạo Class và Grade nodes nếu chưa có

### **3. Cập nhật Query Functions (`query_kg.py`)**

Đã thêm 2 hàm truy vấn mới:
- `query_teacher_by_class()` - Tìm giáo viên dạy một lớp
- `query_classes_by_teacher()` - Tìm các lớp mà giáo viên dạy

---

## 🚀 CÁCH SỬ DỤNG

### **Bước 1: Đảm bảo file CSV đúng vị trí**

File `teachers_assign.csv` phải nằm ở thư mục gốc của project:
```
A_De_tai_Tot_nghiep/
├── teachers_assign.csv  ← File này
├── students.json
└── KG_Design/
    └── build_kg_grade7.py
```

### **Bước 2: Chạy script build KG**

```bash
cd KG_Design
python build_kg_grade7.py
```

Script sẽ tự động:
1. ✅ Đọc `teachers_assign.csv`
2. ✅ Tạo Teacher nodes
3. ✅ Tạo relationship `teaches` với các Class
4. ✅ Tạo Class và Grade nodes nếu chưa có

### **Bước 3: Kiểm tra kết quả**

Sau khi chạy script, bạn sẽ thấy output:
```
👨‍🏫 Đang thêm dữ liệu giáo viên...
✅ Đã thêm 7 giáo viên, 54 phân công lớp
```

### **Bước 4: Truy vấn dữ liệu giáo viên**

```python
from KG_Design.query_kg import load_kg, query_teacher_by_class, query_classes_by_teacher

# Tải KG
g = load_kg('kg_grade7.ttl')

# Tìm giáo viên dạy lớp 7/19
query_teacher_by_class(g, '7/19')

# Tìm các lớp giáo viên tin_01 dạy
query_classes_by_teacher(g, 'tin_01')
```

---

## 📝 VÍ DỤ TRUY VẤN SPARQL

### **1. Tìm giáo viên dạy một lớp:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?teacher ?name ?teacherId ?expertise
WHERE {
    ?class edu:className "7/19" .
    ?teacher edu:teaches ?class .
    ?teacher rdfs:label ?name .
    OPTIONAL { ?teacher edu:teacherId ?teacherId . }
    OPTIONAL { ?teacher edu:expertise ?expertise . }
}
```

### **2. Tìm các lớp một giáo viên dạy:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?class ?className
WHERE {
    ?teacher edu:teacherId "tin_01" .
    ?teacher edu:teaches ?class .
    ?class edu:className ?className .
}
ORDER BY ?className
```

### **3. Tìm tất cả giáo viên và số lớp họ dạy:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?teacher ?name (COUNT(?class) as ?num_classes)
WHERE {
    ?teacher a edu:Teacher .
    ?teacher rdfs:label ?name .
    ?teacher edu:teaches ?class .
}
GROUP BY ?teacher ?name
ORDER BY DESC(?num_classes)
```

---

## 🔍 KIỂM TRA DỮ LIỆU

### **Kiểm tra bằng Python:**

```python
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS

EDU = Namespace("http://education.vn/ontology#")
DATA = Namespace("http://education.vn/data/")

g = Graph()
g.parse('kg_grade7.ttl', format='turtle')

# Đếm số giáo viên
teachers = list(g.subjects(RDF.type, EDU.Teacher))
print(f"Số giáo viên: {len(teachers)}")

# Đếm số relationship teaches
teaches = list(g.subject_objects(EDU.teaches))
print(f"Số phân công lớp: {len(teaches)}")

# Liệt kê tất cả giáo viên
for teacher in teachers:
    name = g.value(teacher, RDFS.label)
    teacher_id = g.value(teacher, EDU.teacherId)
    print(f"- {name} (ID: {teacher_id})")
```

---

## ⚠️ LƯU Ý

### **1. Encoding của file CSV:**
- File CSV phải dùng encoding **UTF-8** hoặc **UTF-8 with BOM**
- Script tự động xử lý BOM bằng `encoding='utf-8-sig'`

### **2. Trùng lặp dữ liệu:**
- Script tự động loại bỏ trùng lặp Teacher (dựa trên `Id_teacher`)
- Mỗi giáo viên chỉ được tạo 1 lần trong KG
- Mỗi dòng trong CSV tạo 1 relationship `teaches`

### **3. Class chưa tồn tại:**
- Nếu Class chưa có trong KG (chưa được tạo từ `students.json`), script sẽ tự động tạo
- Grade cũng sẽ được tạo tự động nếu chưa có

### **4. Cập nhật dữ liệu:**
- Nếu cập nhật `teachers_assign.csv`, cần chạy lại script `build_kg_grade7.py`
- Hoặc xóa KG cũ và build lại từ đầu

---

## 📊 CẤU TRÚC TRONG KNOWLEDGE GRAPH

Sau khi tích hợp, KG sẽ có cấu trúc:

```
Teacher (tin_01)
  ├── fullName: "Ngô Tiến Hiệp"
  ├── teacherId: "tin_01"
  ├── expertise: "Tin học"
  └── teaches → Class (6/14)
       ├── className: "6/14"
       ├── belongsToGrade → Grade (6)
       └── ← belongsToClass ← Student (nhiều học sinh)
```

---

## 🎯 ỨNG DỤNG

### **1. Dashboard giáo viên:**
- Hiển thị thông tin giáo viên phụ trách từng lớp
- Lọc kết quả theo giáo viên

### **2. Phân tích theo giáo viên:**
- So sánh kết quả học tập giữa các lớp do cùng giáo viên dạy
- Đánh giá hiệu quả giảng dạy

### **3. Gợi ý cá nhân hóa:**
- Gợi ý bài học dựa trên giáo viên và lớp
- Phân tích điểm mạnh/yếu của từng giáo viên

---

## 📚 TÀI LIỆU LIÊN QUAN

- **Schema:** `KG_Design/kg_schema_grade7.ttl`
- **Build Script:** `KG_Design/build_kg_grade7.py`
- **Query Functions:** `KG_Design/query_kg.py`
- **Schema Documentation:** `KG_Design/SCHEMA_KNOWLEDGE_GRAPH.md`

---

**Cập nhật:** $(date)

