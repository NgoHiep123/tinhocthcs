# 🤖 Scripts Tự Động Hóa Dự Án

Tài liệu hướng dẫn sử dụng các script tự động hóa để hoàn thiện dự án.

---

## 📋 Danh sách Scripts

### 1. `00_setup_all.py` - Script Tổng Hợp
**Chức năng:** Chạy tất cả các bước setup tự động

```bash
python scripts/00_setup_all.py
```

**Các bước thực hiện:**
1. ✅ Kiểm tra môi trường (dependencies)
2. ✅ Setup database MySQL
3. ✅ Cập nhật endpoint trong HTML
4. ✅ Import KG vào GraphDB
5. ✅ Chạy pipeline ML (KNN + PPR)
6. ✅ Test hệ thống

---

### 2. `setup_database.py` - Setup Database
**Chức năng:** Tự động setup MySQL database

```bash
python scripts/setup_database.py
```

**Tính năng:**
- ✅ Kiểm tra MySQL có sẵn không
- ✅ Import SQL file tự động
- ✅ Hướng dẫn setup thủ công
- ✅ Cập nhật file config.php

---

### 3. `import_all_kg.py` - Import Knowledge Graph
**Chức năng:** Import tất cả file KG vào GraphDB

```bash
python scripts/import_all_kg.py
```

**Tính năng:**
- ✅ Tự động tìm tất cả file .ttl
- ✅ Kiểm tra kết nối GraphDB
- ✅ Import nhiều file cùng lúc
- ✅ Báo cáo kết quả chi tiết

**Yêu cầu:**
- GraphDB Desktop đã cài và chạy
- Repository đã được tạo
- File .env có cấu hình đúng

---

### 4. `run_ml_pipeline.py` - Chạy ML Pipeline
**Chức năng:** Chạy pipeline Machine Learning hoàn chỉnh

```bash
python scripts/run_ml_pipeline.py
```

**Các bước:**
1. ✅ Kiểm tra điều kiện tiên quyết
2. ✅ Chạy KNN (phát hiện học sinh yếu)
3. ✅ Chạy PPR (gợi ý bài học)
4. ✅ Tạo báo cáo kết quả

**Output:**
- `KG_Design/kg_grade7_with_knn.ttl`
- `KG_Design/kg_grade7_with_ppr.ttl`
- `ML_PIPELINE_REPORT.json`

---

### 5. `test_complete_system.py` - Test Hệ Thống
**Chức năng:** Kiểm tra toàn bộ hệ thống

```bash
python scripts/test_complete_system.py
```

**Kiểm tra:**
- ✅ Database connection
- ✅ API files
- ✅ GraphDB setup
- ✅ ML outputs
- ✅ HTML files

**Output:**
- `TEST_REPORT.json`

---

### 6. `update_endpoint_to_php_api.py` - Cập Nhật Endpoint
**Chức năng:** Cập nhật endpoint từ Google Sheets sang PHP API

```bash
python scripts/update_endpoint_to_php_api.py
```

**Tính năng:**
- ✅ Tìm tất cả file HTML
- ✅ Thay thế endpoint
- ✅ Cập nhật function sendResult()

---

## 🚀 Sử Dụng Nhanh

### Cách 1: Chạy tất cả (Khuyến nghị)
```bash
python scripts/00_setup_all.py
```

### Cách 2: Chạy từng bước
```bash
# Bước 1: Setup database
python scripts/setup_database.py

# Bước 2: Cập nhật endpoint
python scripts/update_endpoint_to_php_api.py

# Bước 3: Import KG
python scripts/import_all_kg.py

# Bước 4: Chạy ML pipeline
python scripts/run_ml_pipeline.py

# Bước 5: Test hệ thống
python scripts/test_complete_system.py
```

---

## 📋 Checklist Trước Khi Chạy

### Trước khi chạy `setup_database.py`:
- [ ] MySQL đã được cài đặt (hoặc XAMPP/WAMP)
- [ ] Có quyền tạo database
- [ ] Biết username/password MySQL

### Trước khi chạy `import_all_kg.py`:
- [ ] GraphDB Desktop đã cài và chạy
- [ ] Đã tạo repository trong GraphDB
- [ ] File `.env` có cấu hình đúng
- [ ] Đã có file `.ttl` (chạy build_kg trước)

### Trước khi chạy `run_ml_pipeline.py`:
- [ ] Đã cài đặt dependencies: `pip install -r requirements.txt`
- [ ] Đã có file KG: `KG_Design/kg_grade7.ttl`
- [ ] Có dữ liệu học sinh và kết quả

### Trước khi chạy `update_endpoint_to_php_api.py`:
- [ ] Đã có domain/hosting cho PHP API
- [ ] Backend API đã được deploy
- [ ] Database đã được setup

---

## ⚙️ Cấu Hình

### File `.env` (cho GraphDB)
```env
GRAPHDB_SERVER=http://localhost:7200
GRAPHDB_REPOSITORY=tin_hoc_thcs
GRAPHDB_USERNAME=admin
GRAPHDB_PASSWORD=root
```

### File `backend_api/api/config.php`
```php
define('DB_HOST', 'localhost');
define('DB_NAME', 'tinhoc321_quiz');
define('DB_USER', 'root');
define('DB_PASS', 'your_password');
```

### File `scripts/update_endpoint_to_php_api.py`
```python
NEW_API_ENDPOINT = "https://your-domain.com/api/save_result.php"
```

---

## 🐛 Xử Lý Lỗi

### Lỗi: "Module not found"
```bash
pip install -r requirements.txt
```

### Lỗi: "GraphDB connection failed"
- Kiểm tra GraphDB Desktop đã chạy chưa
- Kiểm tra file `.env` có đúng không
- Kiểm tra repository đã tạo chưa

### Lỗi: "MySQL connection failed"
- Kiểm tra MySQL đã chạy chưa
- Kiểm tra username/password
- Kiểm tra file `config.php`

### Lỗi: "File not found"
- Đảm bảo đang chạy script từ thư mục gốc dự án
- Kiểm tra các file cần thiết đã có chưa

---

## 📊 Báo Cáo

Các script sẽ tạo các file báo cáo:

1. **`SETUP_REPORT.json`** - Báo cáo setup tổng thể
2. **`ML_PIPELINE_REPORT.json`** - Báo cáo ML pipeline
3. **`TEST_REPORT.json`** - Báo cáo test hệ thống

---

## 💡 Tips

1. **Chạy từng bước một:** Nếu gặp lỗi, chạy từng script riêng để dễ debug

2. **Kiểm tra log:** Các script sẽ in ra console, đọc kỹ để biết lỗi

3. **Backup trước:** Nếu có dữ liệu quan trọng, backup trước khi chạy

4. **Test thử:** Chạy test sau mỗi bước để đảm bảo thành công

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Đọc file báo cáo (JSON) để xem chi tiết
2. Kiểm tra các file log/error
3. Xem lại tài liệu trong từng script

---

**Chúc bạn thành công! 🚀**

