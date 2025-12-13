# ✅ BÁO CÁO KIỂM TRA VÀ SỬA LỖI FILE TTL TRONG THƯ MỤC SCHEMA

> Đã kiểm tra và sửa các script tạo file TTL để đảm bảo format URI đúng

---

## 📊 TỔNG QUAN

**Ngày kiểm tra:** 2025-01-15

**Mục tiêu:** Kiểm tra các file TTL trong thư mục `schema/` và sửa các script nếu có vấn đề về format URI

---

## ✅ KẾT QUẢ KIỂM TRA

### 1. Kiểm tra các file TTL trong `schema/` ✅

**Tổng số file:** 18 file TTL (không bao gồm `.backup`)

**Các file chính:**
- ✅ `kg_schema.ttl` - Schema định nghĩa
- ✅ `grades.ttl` - Khối lớp (6, 7, 8, 9)
- ✅ `topics.ttl` - Chủ đề
- ✅ `lessons.ttl` - Bài học
- ✅ `classes.ttl` - Lớp học
- ✅ `students_updated.ttl` - Học sinh
- ✅ `questions_updated.ttl` - Câu hỏi
- ✅ `tests.ttl` - Bài kiểm tra
- ✅ `test_results.ttl` - Kết quả
- ✅ ... và các file khác

**Kết quả:** ✅ Tất cả các file chính đều có format URI đúng (dùng `_` thay vì `/`)

**Ví dụ format đúng:**
```turtle
data:grade_6
data:topic_6_A
data:lesson_6_A1
data:class_6_1
data:question_K6A1_01
```

---

### 2. Phát hiện vấn đề trong script `build_ttl.py` ⚠️ → ✅ ĐÃ SỬA

**Vấn đề:** Hàm `iri()` đang tạo URI với format sai:
```python
# SAI (có dấu /)
return f"data:{kind}/{ident}"  # → data:class/6_1
```

**Hậu quả:** Nếu script này được chạy, sẽ tạo ra file TTL có URI sai format, gây lỗi `RDF Parse Error` khi upload vào GraphDB.

**Đã sửa thành:**
```python
# ĐÚNG (dùng _ thay vì /)
return f"data:{kind}_{ident}"  # → data:class_6_1
```

**Vị trí sửa:** `KG_Design/scripts/build/build_ttl.py` - Dòng 32

---

### 3. Kiểm tra các file `.backup` ⚠️

**Phát hiện:** Các file `.backup` có format URI sai (dùng `/`):
- `students_updated.ttl.backup`
- `questions_updated.ttl.backup`
- `tests.ttl.backup`
- `test_results.ttl.backup`
- `questions_in_tests.ttl.backup`

**Giải pháp:** Các file `.backup` không ảnh hưởng vì:
- Đây chỉ là file backup
- Các file chính (không có `.backup`) đã đúng format
- Có thể xóa hoặc giữ lại tùy ý

---

## 🔧 CÁC THAY ĐỔI ĐÃ THỰC HIỆN

### Sửa script `build_ttl.py`

**File:** `KG_Design/scripts/build/build_ttl.py`

**Thay đổi:**
```python
# TRƯỚC (SAI):
def iri(kind: str, ident: str) -> str:
    ident = str(ident).strip().replace(" ", "_").replace("/", "_")
    if ident.startswith(kind + "_"):
        ident = ident[len(kind) + 1:]
    return f"data:{kind}/{ident}"  # ❌ Dùng /

# SAU (ĐÚNG):
def iri(kind: str, ident: str) -> str:
    ident = str(ident).strip().replace(" ", "_").replace("/", "_")
    if ident.startswith(kind + "_"):
        ident = ident[len(kind) + 1:]
    return f"data:{kind}_{ident}"  # ✅ Dùng _
```

**Lý do:** 
- Dấu `/` trong Turtle URI có thể gây lỗi `RDF Parse Error` trong GraphDB
- Format chuẩn: `data:class_6_1` thay vì `data:class/6_1`

---

## 📝 LƯU Ý VỀ ĐƯỜNG DẪN OUTPUT

### Script `build_ttl.py` hiện tại:

**Đường dẫn output:** `KG_Design/data/grade6/ttl/`

**Các file được tạo:**
- `grades.ttl`
- `topics.ttl`
- `lessons.ttl`
- `classes.ttl`
- `students_updated.ttl`
- `questions_updated.ttl`
- `tests.ttl`
- `test_results.ttl`
- `questions_in_tests.ttl`

**Lưu ý:**
- Các file trong thư mục `schema/` có thể được tạo từ script khác hoặc copy thủ công
- Nếu muốn script ghi vào thư mục `schema/`, cần sửa biến `OUT` trong script:
  ```python
  # Thay đổi từ:
  OUT = ROOT / "data/grade6/ttl"
  
  # Thành:
  OUT = ROOT / "schema"
  ```

---

## ✅ KẾT LUẬN

1. ✅ **Các file TTL trong thư mục `schema/` đã đúng format**
   - Tất cả URI đều dùng `_` thay vì `/`
   - Không có vấn đề `RDF Parse Error`

2. ✅ **Script `build_ttl.py` đã được sửa**
   - Hàm `iri()` giờ tạo URI đúng format
   - Các file TTL được tạo từ script này sẽ không còn lỗi format

3. ⚠️ **Các file `.backup` có format sai nhưng không ảnh hưởng**
   - Đây chỉ là file backup
   - Có thể xóa hoặc giữ lại

---

## 🚀 BƯỚC TIẾP THEO

1. **Nếu muốn tạo lại các file TTL từ script:**
   ```bash
   cd KG_Design
   python scripts/build/build_ttl.py
   ```
   Kết quả sẽ được ghi vào `data/grade6/ttl/` với format URI đúng.

2. **Nếu muốn script ghi vào thư mục `schema/`:**
   - Sửa dòng 14 trong `build_ttl.py`: `OUT = ROOT / "schema"`

3. **Xóa các file `.backup` nếu không cần:**
   ```bash
   Remove-Item KG_Design/schema/*.backup
   ```

---

**Cập nhật:** 2025-01-15

