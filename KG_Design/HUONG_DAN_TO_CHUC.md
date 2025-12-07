# 📁 HƯỚNG DẪN TỔ CHỨC LẠI CẤU TRÚC

## 🎯 MỤC ĐÍCH

Tổ chức lại cấu trúc thư mục `KG_Design` cho rõ ràng, dễ quản lý và sử dụng.

---

## 📊 PHÂN TÍCH FILE

### **File có thể XÓA:**

1. ❌ `SCHEMA_KNOWLEDGE_GRAPH.md` - Trùng với `KHUNG_KG_CHUAN.md`
2. ❌ `STEP_BY_STEP.md` - Có thể gộp vào README
3. ❌ `build_kg_grade7.py` - Script cũ, không dùng nữa
4. ❌ `update_kg.py` - Phụ thuộc vào `build_kg_grade7.py` (đã xóa)
5. ❌ `cypher_import_skeleton.cypher` - Neo4j, không dùng GraphDB
6. ❌ `grade6/out/` - Thư mục namespace cũ (đã có `out_converted/`)

### **File cần KIỂM TRA:**

- ⚠️ `kg_grade7.ttl` - Kiểm tra có còn dùng không
- ⚠️ `build_inputs_from_existing.py` - Kiểm tra có dùng không

### **File GIỮ LẠI:**

- ✅ Tất cả file schema, docs, scripts, data còn lại

---

## 🗂️ CẤU TRÚC MỚI

```
KG_Design/
├── schema/                    # Schema và ontology
│   ├── kg_schema_chuan.ttl   # Schema chính
│   └── archive/              # Schema cũ (tham khảo)
│       └── kg_schema_grade7.ttl
│
├── docs/                     # Tài liệu
│   ├── KHUNG_KG_CHUAN.md
│   ├── KIEM_TRA_CHUC_NANG.md
│   ├── SO_SANH_SCHEMA.md
│   ├── BAO_CAO_DU_LIEU.md
│   ├── README.md             # README chính
│   ├── guides/               # Hướng dẫn chi tiết
│   └── queries/              # SPARQL queries
│
├── scripts/                  # Scripts Python
│   ├── build/                # Script tạo dữ liệu
│   ├── utils/                # Tiện ích
│   └── query/                # Query scripts
│
├── data/                     # Dữ liệu
│   ├── grade6/
│   │   ├── csv/              # File CSV
│   │   └── ttl/              # File TTL (namespace mới)
│   ├── templates/            # Template CSV
│   └── json/                 # File JSON
│
└── tools/                    # Công cụ
    ├── import_to_graphdb.py
    └── ...
```

---

## 🚀 CÁCH SỬ DỤNG SCRIPT TỔ CHỨC

### **Bước 1: Xem báo cáo phân tích**

```bash
# Đọc file phân tích
cat KG_Design/PHAN_TICH_VA_TO_CHUC.md
```

### **Bước 2: Chạy script tổ chức lại**

```bash
cd KG_Design
python reorganize_structure.py
```

Script sẽ:
1. ✅ Tạo cấu trúc thư mục mới
2. ✅ Di chuyển file vào đúng vị trí
3. ✅ Xóa file không cần thiết
4. ✅ Tạo README.md chính

### **Bước 3: Kiểm tra và cập nhật**

Sau khi tổ chức lại, cần:
1. Kiểm tra các script có hoạt động không
2. Cập nhật đường dẫn trong script nếu cần
3. Cập nhật đường dẫn trong tài liệu

---

## ⚠️ LƯU Ý QUAN TRỌNG

### **1. Backup trước khi chạy**

Script sẽ:
- Di chuyển file (không copy)
- Xóa file không cần thiết

**Khuyến nghị:** Backup thư mục `KG_Design` trước khi chạy!

### **2. Cập nhật đường dẫn**

Sau khi tổ chức lại, một số script có thể cần cập nhật đường dẫn:
- `build_missing_ttl.py` - Cập nhật đường dẫn CSV
- `export_ttl.py` - Cập nhật đường dẫn
- Các script query - Cập nhật đường dẫn file TTL

### **3. Test sau khi tổ chức**

```bash
# Test script build
cd scripts/build
python build_missing_ttl.py

# Test import
cd ../../tools
python import_to_graphdb.py
```

---

## ✅ CHECKLIST

- [ ] Đã đọc `PHAN_TICH_VA_TO_CHUC.md`
- [ ] Đã backup thư mục `KG_Design`
- [ ] Đã chạy `reorganize_structure.py`
- [ ] Đã kiểm tra cấu trúc mới
- [ ] Đã test các script
- [ ] Đã cập nhật đường dẫn (nếu cần)

---

## 📝 SAU KHI TỔ CHỨC LẠI

### **Cấu trúc mới:**
- ✅ Rõ ràng, dễ tìm file
- ✅ Phân loại theo chức năng
- ✅ Dễ mở rộng cho các khối khác

### **File quan trọng:**
- Schema: `schema/kg_schema_chuan.ttl`
- Script chính: `scripts/build/build_missing_ttl.py`
- Tài liệu: `docs/README.md`
- Dữ liệu: `data/grade6/`

---

**Cập nhật:** 2025-01-15

