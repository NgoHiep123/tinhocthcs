# 📊 PHÂN TÍCH VÀ TỔ CHỨC LẠI CẤU TRÚC KG_DESIGN

## 🎯 MỤC ĐÍCH

Phân tích các file hiện có, xác định file không cần thiết và đề xuất cấu trúc mới rõ ràng hơn.

---

## 📋 PHÂN TÍCH FILE HIỆN TẠI

### **1. SCHEMA FILES (File Schema)**

| File | Trạng thái | Hành động |
|------|------------|-----------|
| `kg_schema_chuan.ttl` | ✅ **GIỮ** | Schema chuẩn mới (dùng chính) |
| `kg_schema_grade7.ttl` | ⚠️ **GIỮ** (tham khảo) | Schema cũ, giữ để tham khảo |
| `kg_grade7.ttl` | ❓ **KIỂM TRA** | Dữ liệu Khối 7, có thể giữ hoặc xóa |

**Đề xuất:**
- ✅ Giữ `kg_schema_chuan.ttl` (schema chính)
- ⚠️ Di chuyển `kg_schema_grade7.ttl` vào thư mục `archive/` hoặc `old/`
- ❓ Kiểm tra `kg_grade7.ttl` có còn dùng không

---

### **2. TTL OUTPUT FILES (File TTL đầu ra)**

#### **Thư mục `grade6/out/`**
- Namespace cũ: `https://example.org/kg/`
- **Trạng thái:** ⚠️ **CÓ THỂ XÓA** (đã có out_converted)

#### **Thư mục `grade6/out_converted/`**
- Namespace mới: `http://education.vn/data/`
- **Trạng thái:** ✅ **GIỮ** (dùng chung schema với grade7)

**Đề xuất:**
- ❌ Xóa `grade6/out/` (namespace cũ, không dùng nữa)
- ✅ Giữ `grade6/out_converted/` (namespace mới)
- ✅ Tạo thư mục `grade6/ttl/` cho các file TTL mới từ `build_missing_ttl.py`

---

### **3. DOCUMENTATION FILES (File tài liệu)**

#### **File chính (GIỮ):**
- ✅ `KHUNG_KG_CHUAN.md` - Tài liệu chính về khung KG
- ✅ `KIEM_TRA_CHUC_NANG.md` - Kiểm tra chức năng
- ✅ `SO_SANH_SCHEMA.md` - So sánh schema
- ✅ `BAO_CAO_DU_LIEU.md` - Báo cáo dữ liệu
- ✅ `README_KHUNG_KG_CHUAN.md` - Hướng dẫn sử dụng

#### **File cũ/trùng lặp (CÓ THỂ XÓA):**
- ❌ `SCHEMA_KNOWLEDGE_GRAPH.md` - Trùng với `KHUNG_KG_CHUAN.md`
- ❌ `STEP_BY_STEP.md` - Có thể gộp vào README
- ⚠️ `grade6/README.md` - Có thể gộp vào tài liệu chính

#### **File hướng dẫn (GIỮ):**
- ✅ `grade6/HUONG_DAN_BUILD_MISSING_TTL.md` - Hướng dẫn script mới
- ✅ `grade6/HUONG_DAN_DUNG_CHUNG_SCHEMA_GRADE7.md` - Hướng dẫn dùng chung schema
- ✅ `grade6/EXPLAIN_CSV_FIELDS.md` - Giải thích CSV
- ✅ `HUONG_DAN_THEM_DU_LIEU_MOI.md` - Hướng dẫn thêm dữ liệu
- ✅ `QUICK_GUIDE_THEM_DU_LIEU.md` - Hướng dẫn nhanh
- ✅ `HUONG_DAN_SU_DUNG_TEACHERS.md` - Hướng dẫn giáo viên

#### **File SPARQL (GIỮ):**
- ✅ `grade6/sparql_queries.md` - Query SPARQL
- ✅ `grade6/sparql_construct_queries.md` - Construct queries
- ✅ `grade6/sparql_visual_queries.md` - Visual queries

---

### **4. SCRIPT FILES (File script)**

#### **Script chính (GIỮ):**
- ✅ `grade6/build_missing_ttl.py` - **MỚI** - Tạo file TTL còn thiếu
- ✅ `grade6/export_ttl.py` - Export TTL (có thể cập nhật)
- ✅ `grade6/build_grade6_inputs.py` - Tạo CSV inputs
- ✅ `grade6/build_student_mastery.py` - Tạo mastery
- ✅ `grade6/export_teachers_assignments.py` - Export giáo viên
- ✅ `grade6/convert_to_grade7_namespace.py` - Chuyển namespace

#### **Script cũ/không dùng (CÓ THỂ XÓA):**
- ❌ `build_kg_grade7.py` - Script cũ, không dùng nữa
- ❌ `update_kg.py` - Không rõ mục đích
- ⚠️ `build_inputs_from_existing.py` - Kiểm tra có dùng không

#### **Script tiện ích (GIỮ):**
- ✅ `add_new_student.py` - Thêm học sinh
- ✅ `add_new_class.py` - Thêm lớp
- ✅ `add_new_teacher.py` - Thêm giáo viên
- ✅ `import_to_graphdb.py` - Import vào GraphDB
- ✅ `query_graphdb.py` - Query GraphDB
- ✅ `query_kg.py` - Query KG
- ✅ `test_graphdb_connection.py` - Test kết nối
- ✅ `test_teachers.py` - Test giáo viên
- ✅ `export_teachers_to_json.py` - Export JSON
- ✅ `demo_teacher_queries.py` - Demo query
- ✅ `run_dashboard_server.py` - Dashboard

---

### **5. DATA FILES (File dữ liệu)**

#### **CSV Files (GIỮ):**
- ✅ Tất cả file CSV trong `grade6/` - Dữ liệu nguồn
- ✅ `data_templates/` - Template CSV

#### **JSON Files (GIỮ):**
- ✅ `teachers_data.json` - Dữ liệu giáo viên

#### **Other Files:**
- ⚠️ `cypher_import_skeleton.cypher` - Neo4j (không dùng GraphDB)
- ⚠️ `teachers_dashboard.html` - Dashboard (có thể di chuyển)

---

## 🗂️ CẤU TRÚC MỚI ĐỀ XUẤT

```
KG_Design/
├── schema/                          # Schema và ontology
│   ├── kg_schema_chuan.ttl         # Schema chính (MỚI)
│   └── archive/                    # Schema cũ (tham khảo)
│       └── kg_schema_grade7.ttl
│
├── docs/                           # Tài liệu
│   ├── KHUNG_KG_CHUAN.md          # Tài liệu chính
│   ├── KIEM_TRA_CHUC_NANG.md      # Kiểm tra chức năng
│   ├── SO_SANH_SCHEMA.md          # So sánh schema
│   ├── BAO_CAO_DU_LIEU.md         # Báo cáo dữ liệu
│   ├── README.md                  # README chính
│   │
│   ├── guides/                     # Hướng dẫn chi tiết
│   │   ├── HUONG_DAN_BUILD_TTL.md
│   │   ├── HUONG_DAN_THEM_DU_LIEU.md
│   │   ├── HUONG_DAN_SU_DUNG_TEACHERS.md
│   │   └── QUICK_GUIDE.md
│   │
│   └── queries/                    # SPARQL queries
│       ├── sparql_queries.md
│       ├── sparql_construct_queries.md
│       └── sparql_visual_queries.md
│
├── scripts/                        # Scripts
│   ├── build/                      # Script tạo dữ liệu
│   │   ├── build_missing_ttl.py   # Tạo TTL còn thiếu (MỚI)
│   │   ├── build_grade6_inputs.py
│   │   ├── build_student_mastery.py
│   │   └── export_ttl.py
│   │
│   ├── utils/                      # Tiện ích
│   │   ├── add_new_student.py
│   │   ├── add_new_class.py
│   │   ├── add_new_teacher.py
│   │   ├── export_teachers_assignments.py
│   │   └── convert_to_grade7_namespace.py
│   │
│   └── query/                      # Query scripts
│       ├── query_graphdb.py
│       ├── query_kg.py
│       └── test_graphdb_connection.py
│
├── data/                           # Dữ liệu
│   ├── grade6/                     # Dữ liệu Khối 6
│   │   ├── csv/                    # File CSV
│   │   │   ├── skills.csv
│   │   │   ├── resources.csv
│   │   │   ├── prerequisites.csv
│   │   │   ├── question_skill.csv
│   │   │   ├── resource_skill.csv
│   │   │   ├── student_mastery.csv
│   │   │   ├── assessments.csv
│   │   │   ├── student_assessment.csv
│   │   │   └── questions_in_assessment.csv
│   │   │
│   │   └── ttl/                    # File TTL (namespace mới)
│   │       ├── grades.ttl
│   │       ├── topics.ttl
│   │       ├── lessons.ttl
│   │       ├── classes.ttl
│   │       ├── students.ttl
│   │       ├── questions.ttl
│   │       ├── tests.ttl
│   │       ├── test_results.ttl
│   │       ├── skills.ttl
│   │       ├── resources.ttl
│   │       ├── mastery.ttl
│   │       └── ...
│   │
│   ├── templates/                  # Template CSV
│   │   └── ...
│   │
│   └── json/                       # File JSON
│       └── teachers_data.json
│
└── tools/                          # Công cụ
    ├── import_to_graphdb.py
    ├── run_dashboard_server.py
    └── teachers_dashboard.html
```

---

## ❌ DANH SÁCH FILE CÓ THỂ XÓA

### **File trùng lặp/không dùng:**
1. ❌ `KG_Design/SCHEMA_KNOWLEDGE_GRAPH.md` - Trùng với `KHUNG_KG_CHUAN.md`
2. ❌ `KG_Design/STEP_BY_STEP.md` - Có thể gộp vào README
3. ❌ `KG_Design/build_kg_grade7.py` - Script cũ, không dùng
4. ❌ `KG_Design/update_kg.py` - Không rõ mục đích
5. ❌ `KG_Design/grade6/out/` - Thư mục namespace cũ (đã có out_converted)
6. ❌ `KG_Design/cypher_import_skeleton.cypher` - Neo4j, không dùng GraphDB

### **File cần kiểm tra:**
- ⚠️ `KG_Design/kg_grade7.ttl` - Kiểm tra có còn dùng không
- ⚠️ `KG_Design/build_inputs_from_existing.py` - Kiểm tra có dùng không

---

## ✅ DANH SÁCH FILE CẦN GIỮ

### **Schema:**
- ✅ `kg_schema_chuan.ttl` - Schema chính
- ⚠️ `kg_schema_grade7.ttl` - Di chuyển vào archive/

### **Scripts:**
- ✅ Tất cả script trong `grade6/`
- ✅ Scripts tiện ích (add_new_*, query_*, test_*)
- ✅ `import_to_graphdb.py`

### **Data:**
- ✅ Tất cả file CSV
- ✅ File TTL trong `out_converted/` (sẽ chuyển sang `data/grade6/ttl/`)

### **Docs:**
- ✅ Tất cả file .md (trừ các file trùng lặp đã liệt kê)

---

## 🔧 KẾ HOẠCH TỔ CHỨC LẠI

### **Bước 1: Tạo cấu trúc mới**
1. Tạo thư mục: `schema/`, `docs/`, `scripts/`, `data/`, `tools/`
2. Tạo thư mục con: `docs/guides/`, `docs/queries/`, `scripts/build/`, `scripts/utils/`, `scripts/query/`
3. Tạo thư mục: `data/grade6/csv/`, `data/grade6/ttl/`, `data/templates/`, `data/json/`
4. Tạo thư mục: `schema/archive/`

### **Bước 2: Di chuyển file**
1. Schema → `schema/`
2. Docs → `docs/` và `docs/guides/`, `docs/queries/`
3. Scripts → `scripts/build/`, `scripts/utils/`, `scripts/query/`
4. Data → `data/grade6/csv/`, `data/grade6/ttl/`
5. Tools → `tools/`

### **Bước 3: Xóa file không cần**
1. Xóa `grade6/out/` (namespace cũ)
2. Xóa các file trùng lặp
3. Xóa script cũ không dùng

### **Bước 4: Cập nhật đường dẫn**
1. Cập nhật import trong các script
2. Cập nhật đường dẫn trong tài liệu
3. Tạo README.md chính

---

## 📝 CHECKLIST

- [ ] Tạo cấu trúc thư mục mới
- [ ] Di chuyển file vào đúng vị trí
- [ ] Xóa file không cần thiết
- [ ] Cập nhật đường dẫn trong script
- [ ] Cập nhật đường dẫn trong tài liệu
- [ ] Tạo README.md chính
- [ ] Test các script sau khi di chuyển

---

**Cập nhật:** 2025-01-15

