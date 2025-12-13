"""
Script tổ chức lại cấu trúc thư mục KG_Design
Di chuyển file vào đúng vị trí và xóa file không cần thiết
"""

from pathlib import Path
import shutil
import os

ROOT = Path(__file__).resolve().parent

# ============================================
# 1. TẠO CẤU TRÚC THƯ MỤC MỚI
# ============================================

def create_structure():
    """Tạo cấu trúc thư mục mới"""
    dirs = [
        "schema/archive",
        "docs/guides",
        "docs/queries",
        "scripts/build",
        "scripts/utils",
        "scripts/query",
        "data/grade6/csv",
        "data/grade6/ttl",
        "data/templates",
        "data/json",
        "tools",
    ]
    
    for dir_path in dirs:
        (ROOT / dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Đã tạo: {dir_path}")

# ============================================
# 2. DI CHUYỂN FILE
# ============================================

def move_files():
    """Di chuyển file vào đúng vị trí"""
    
    moves = [
        # Schema
        ("kg_schema_chuan.ttl", "schema/kg_schema_chuan.ttl"),
        ("kg_schema_grade7.ttl", "schema/archive/kg_schema_grade7.ttl"),
        
        # Docs - Chính
        ("KHUNG_KG_CHUAN.md", "docs/KHUNG_KG_CHUAN.md"),
        ("KIEM_TRA_CHUC_NANG.md", "docs/KIEM_TRA_CHUC_NANG.md"),
        ("SO_SANH_SCHEMA.md", "docs/SO_SANH_SCHEMA.md"),
        ("BAO_CAO_DU_LIEU.md", "docs/BAO_CAO_DU_LIEU.md"),
        ("README_KHUNG_KG_CHUAN.md", "docs/README_KHUNG_KG_CHUAN.md"),
        
        # Docs - Guides
        ("grade6/HUONG_DAN_BUILD_MISSING_TTL.md", "docs/guides/HUONG_DAN_BUILD_TTL.md"),
        ("grade6/HUONG_DAN_DUNG_CHUNG_SCHEMA_GRADE7.md", "docs/guides/HUONG_DAN_DUNG_CHUNG_SCHEMA.md"),
        ("grade6/EXPLAIN_CSV_FIELDS.md", "docs/guides/EXPLAIN_CSV_FIELDS.md"),
        ("HUONG_DAN_THEM_DU_LIEU_MOI.md", "docs/guides/HUONG_DAN_THEM_DU_LIEU.md"),
        ("QUICK_GUIDE_THEM_DU_LIEU.md", "docs/guides/QUICK_GUIDE.md"),
        ("HUONG_DAN_SU_DUNG_TEACHERS.md", "docs/guides/HUONG_DAN_SU_DUNG_TEACHERS.md"),
        
        # Docs - Queries
        ("grade6/sparql_queries.md", "docs/queries/sparql_queries.md"),
        ("grade6/sparql_construct_queries.md", "docs/queries/sparql_construct_queries.md"),
        ("grade6/sparql_visual_queries.md", "docs/queries/sparql_visual_queries.md"),
        
        # Scripts - Build
        ("grade6/build_missing_ttl.py", "scripts/build/build_missing_ttl.py"),
        ("grade6/build_grade6_inputs.py", "scripts/build/build_grade6_inputs.py"),
        ("grade6/build_student_mastery.py", "scripts/build/build_student_mastery.py"),
        ("grade6/export_ttl.py", "scripts/build/export_ttl.py"),
        ("grade6/generate_prereq_baseline.py", "scripts/build/generate_prereq_baseline.py"),
        
        # Scripts - Utils
        ("add_new_student.py", "scripts/utils/add_new_student.py"),
        ("add_new_class.py", "scripts/utils/add_new_class.py"),
        ("add_new_teacher.py", "scripts/utils/add_new_teacher.py"),
        ("grade6/export_teachers_assignments.py", "scripts/utils/export_teachers_assignments.py"),
        ("grade6/convert_to_grade7_namespace.py", "scripts/utils/convert_to_grade7_namespace.py"),
        ("export_teachers_to_json.py", "scripts/utils/export_teachers_to_json.py"),
        
        # Scripts - Query
        ("query_graphdb.py", "scripts/query/query_graphdb.py"),
        ("query_kg.py", "scripts/query/query_kg.py"),
        ("test_graphdb_connection.py", "scripts/query/test_graphdb_connection.py"),
        ("test_teachers.py", "scripts/query/test_teachers.py"),
        ("demo_teacher_queries.py", "scripts/query/demo_teacher_queries.py"),
        
        # Data - CSV (KHÔNG di chuyển - giữ nguyên để script dễ tìm)
        # Các script đang dùng đường dẫn tương đối từ grade6/
        
        # Data - Templates (KHÔNG di chuyển - giữ nguyên)
        
        # Data - JSON
        ("teachers_data.json", "data/json/teachers_data.json"),
        
        # Tools
        ("import_to_graphdb.py", "tools/import_to_graphdb.py"),
        ("run_dashboard_server.py", "tools/run_dashboard_server.py"),
        ("teachers_dashboard.html", "tools/teachers_dashboard.html"),
    ]
    
    for src, dst in moves:
        src_path = ROOT / src
        dst_path = ROOT / dst
        
        if src_path.exists():
            # Tạo thư mục đích nếu chưa có
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Di chuyển file/thư mục
            if src_path.is_dir():
                if dst_path.exists():
                    # Merge thư mục
                    for item in src_path.iterdir():
                        shutil.move(str(item), str(dst_path / item.name))
                    src_path.rmdir()
                else:
                    shutil.move(str(src_path), str(dst_path))
            else:
                shutil.move(str(src_path), str(dst_path))
            
            print(f"✅ Đã di chuyển: {src} → {dst}")
        else:
            print(f"⚠️  Không tìm thấy: {src}")

# ============================================
# 3. DI CHUYỂN TTL FILES
# ============================================

def move_ttl_files():
    """Di chuyển file TTL từ out_converted sang data/grade6/ttl"""
    src_dir = ROOT / "grade6/out_converted"
    dst_dir = ROOT / "data/grade6/ttl"
    
    if src_dir.exists():
        for ttl_file in src_dir.glob("*.ttl"):
            dst_file = dst_dir / ttl_file.name
            shutil.move(str(ttl_file), str(dst_file))
            print(f"✅ Đã di chuyển TTL: {ttl_file.name}")
        
        # Xóa thư mục rỗng
        try:
            src_dir.rmdir()
            print(f"✅ Đã xóa thư mục rỗng: {src_dir}")
        except:
            pass
    
    # Di chuyển file TTL mới từ build_missing_ttl.py (nếu có)
    src_dir_new = ROOT / "grade6/out"
    if src_dir_new.exists():
        # Chỉ di chuyển file TTL mới (grades, topics, lessons, etc.)
        new_ttl_files = ["grades.ttl", "topics.ttl", "lessons.ttl", "classes.ttl", 
                         "students_updated.ttl", "questions_updated.ttl", 
                         "tests.ttl", "test_results.ttl", "questions_in_tests.ttl"]
        
        for ttl_file in new_ttl_files:
            src_file = src_dir_new / ttl_file
            if src_file.exists():
                dst_file = dst_dir / ttl_file
                shutil.move(str(src_file), str(dst_file))
                print(f"✅ Đã di chuyển TTL mới: {ttl_file}")

# ============================================
# 4. XÓA FILE KHÔNG CẦN THIẾT
# ============================================

def delete_unnecessary_files():
    """Xóa các file không cần thiết"""
    
    files_to_delete = [
        # File trùng lặp
        "SCHEMA_KNOWLEDGE_GRAPH.md",
        "STEP_BY_STEP.md",
        
        # Script cũ
        "build_kg_grade7.py",
        "update_kg.py",
        
        # File không dùng
        "cypher_import_skeleton.cypher",
        
        # Thư mục namespace cũ
        "grade6/out",
        
        # File README cũ (sẽ tạo mới)
        "grade6/README.md",
    ]
    
    for file_path in files_to_delete:
        path = ROOT / file_path
        if path.exists():
            if path.is_dir():
                shutil.rmtree(str(path))
                print(f"❌ Đã xóa thư mục: {file_path}")
            else:
                path.unlink()
                print(f"❌ Đã xóa file: {file_path}")
        else:
            print(f"⚠️  Không tìm thấy: {file_path}")

# ============================================
# 5. TẠO README CHÍNH
# ============================================

def create_main_readme():
    """Tạo README.md chính"""
    readme_content = """# 📊 KNOWLEDGE GRAPH DESIGN - TIN HỌC THCS

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
"""
    
    readme_path = ROOT / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"✅ Đã tạo: README.md")

# ============================================
# MAIN
# ============================================

def main():
    """Tổ chức lại cấu trúc"""
    print("🚀 Bắt đầu tổ chức lại cấu trúc...\n")
    
    print("📁 Bước 1: Tạo cấu trúc thư mục mới...")
    create_structure()
    
    print("\n📦 Bước 2: Di chuyển file...")
    move_files()
    
    print("\n📦 Bước 3: Di chuyển file TTL...")
    move_ttl_files()
    
    print("\n🗑️  Bước 4: Xóa file không cần thiết...")
    delete_unnecessary_files()
    
    print("\n📝 Bước 5: Tạo README chính...")
    create_main_readme()
    
    print("\n✅ Hoàn thành tổ chức lại cấu trúc!")
    print("\n⚠️  LƯU Ý: Kiểm tra lại các script và cập nhật đường dẫn nếu cần!")

if __name__ == "__main__":
    # Tự động chạy (không cần xác nhận)
    print("⚠️  Script này sẽ:")
    print("  1. Tạo cấu trúc thư mục mới")
    print("  2. Di chuyển file vào đúng vị trí")
    print("  3. Xóa file không cần thiết")
    print("\n🚀 Bắt đầu tổ chức lại...\n")
    main()

