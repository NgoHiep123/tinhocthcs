# 📊 KNOWLEDGE GRAPH DESIGN - TIN HỌC THCS

## 🎯 TỔNG QUAN

Thư mục này chứa schema, scripts và dữ liệu để xây dựng Knowledge Graph cho hệ thống hỗ trợ giáo viên THCS nâng cao chất lượng giảng dạy Tin học.

---

## 📁 CẤU TRÚC THƯ MỤC

```
KG_Design/
├── schema/              # Schema và ontology
├── docs/                # Tài liệu
├── scripts/             # Scripts Python
├── data/                # Dữ liệu CSV, TTL, JSON
└── tools/               # Công cụ tiện ích
```

---

## 🚀 BẮT ĐẦU NHANH

### **1. Đọc tài liệu chính:**
- [KHUNG KG CHUẨN](docs/KHUNG_KG_CHUAN.md) - Tài liệu chi tiết về khung KG
- [HƯỚNG DẪN SỬ DỤNG](docs/README_KHUNG_KG_CHUAN.md) - Hướng dẫn sử dụng nhanh

### **2. Tạo file TTL còn thiếu:**
```bash
cd scripts/build
python build_missing_ttl.py
```
**Lưu ý:** File TTL sẽ được tạo trong `data/grade6/ttl/`

### **3. Import vào GraphDB:**
```bash
cd tools
python import_to_graphdb.py
```

---

## 📚 TÀI LIỆU

### **Tài liệu chính:**
- [Khung KG Chuẩn](docs/KHUNG_KG_CHUAN.md)
- [Kiểm tra Chức năng](docs/KIEM_TRA_CHUC_NANG.md)
- [So sánh Schema](docs/SO_SANH_SCHEMA.md)
- [Báo cáo Dữ liệu](docs/BAO_CAO_DU_LIEU.md)

### **Hướng dẫn:**
- [Hướng dẫn Build TTL](docs/guides/HUONG_DAN_BUILD_TTL.md)
- [Hướng dẫn Thêm Dữ liệu](docs/guides/HUONG_DAN_THEM_DU_LIEU.md)
- [Hướng dẫn Sử dụng Teachers](docs/guides/HUONG_DAN_SU_DUNG_TEACHERS.md)
- [Quick Guide](docs/guides/QUICK_GUIDE.md)

### **SPARQL Queries:**
- [SPARQL Queries](docs/queries/sparql_queries.md)
- [SPARQL Construct](docs/queries/sparql_construct_queries.md)
- [SPARQL Visual](docs/queries/sparql_visual_queries.md)

---

## 🔧 SCRIPTS

### **Build Scripts:**
- `build_missing_ttl.py` - Tạo file TTL còn thiếu
- `build_grade6_inputs.py` - Tạo CSV inputs
- `build_student_mastery.py` - Tạo mastery
- `export_ttl.py` - Export TTL

### **Utils Scripts:**
- `add_new_student.py` - Thêm học sinh
- `add_new_class.py` - Thêm lớp
- `add_new_teacher.py` - Thêm giáo viên
- `export_teachers_assignments.py` - Export giáo viên

### **Query Scripts:**
- `query_graphdb.py` - Query GraphDB
- `query_kg.py` - Query KG
- `test_graphdb_connection.py` - Test kết nối

---

## 📊 DỮ LIỆU

### **CSV Files:**
- `data/grade6/csv/` - File CSV Khối 6
- `data/templates/` - Template CSV

### **TTL Files:**
- `data/grade6/ttl/` - File TTL (namespace chuẩn)

### **JSON Files:**
- `data/json/` - File JSON

---

## 🎯 SCHEMA

- **Schema chính:** `schema/kg_schema_chuan.ttl`
- **Schema cũ (tham khảo):** `schema/archive/kg_schema_grade7.ttl`

---

## ⚠️ LƯU Ý

- Tất cả file TTL sử dụng namespace: `http://education.vn/ontology#` và `http://education.vn/data/`
- Import schema trước, dữ liệu sau khi import vào GraphDB
- Xem [Báo cáo Dữ liệu](docs/BAO_CAO_DU_LIEU.md) để biết file nào còn thiếu

---

**Cập nhật:** 2025-01-15
