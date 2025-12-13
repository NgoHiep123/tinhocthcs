# 🚀 Hướng Dẫn Sử Dụng Script Tự Động Hóa

> **Mục đích:** Tự động hóa các bước còn lại để hoàn thiện dự án

---

## 📋 TỔNG QUAN

Đã tạo **5 script chính** để tự động hóa các bước setup:

1. **`00_setup_all.py`** - Script tổng hợp (chạy tất cả)
2. **`setup_database.py`** - Setup MySQL database
3. **`import_all_kg.py`** - Import KG vào GraphDB
4. **`run_ml_pipeline.py`** - Chạy pipeline ML
5. **`test_complete_system.py`** - Test hệ thống

---

## 🎯 CÁCH SỬ DỤNG NHANH NHẤT

### Cách 1: Chạy tất cả (Khuyến nghị)

**Windows:**
```batch
run_all_automation.bat
```

**Mac/Linux:**
```bash
python scripts/00_setup_all.py
```

Script này sẽ tự động:
1. ✅ Kiểm tra môi trường
2. ✅ Setup database
3. ✅ Cập nhật endpoint
4. ✅ Import KG
5. ✅ Chạy ML pipeline
6. ✅ Test hệ thống

---

## 📝 CHI TIẾT TỪNG SCRIPT

### 1. Script Tổng Hợp (`00_setup_all.py`)

**Chức năng:** Chạy tất cả các bước setup tự động

**Cách chạy:**
```bash
python scripts/00_setup_all.py
```

**Các bước:**
- Bước 0: Kiểm tra dependencies (Python packages)
- Bước 1: Setup database MySQL (có hướng dẫn thủ công)
- Bước 2: Cập nhật endpoint trong HTML
- Bước 3: Import KG vào GraphDB
- Bước 4: Chạy pipeline ML (KNN + PPR)
- Bước 5: Test hệ thống

**Output:**
- Báo cáo tổng hợp trên console
- File `SETUP_REPORT.json` (nếu có)

---

### 2. Setup Database (`setup_database.py`)

**Chức năng:** Tự động setup MySQL database

**Cách chạy:**
```bash
python scripts/setup_database.py
```

**Tính năng:**
- ✅ Kiểm tra MySQL có sẵn không
- ✅ Import SQL file tự động (nếu có MySQL command line)
- ✅ Hướng dẫn setup thủ công qua phpMyAdmin
- ✅ Cập nhật file `config.php` với thông tin database

**Yêu cầu:**
- MySQL đã được cài đặt (hoặc XAMPP/WAMP)
- File `backend_api/create_database.sql` có sẵn

**Sau khi chạy:**
1. Database được tạo
2. File `backend_api/api/config.php` được cập nhật
3. Có thể test kết nối bằng `backend_api/test_connection.php`

---

### 3. Import Knowledge Graph (`import_all_kg.py`)

**Chức năng:** Import tất cả file KG vào GraphDB

**Cách chạy:**
```bash
python scripts/import_all_kg.py
```

**Tính năng:**
- ✅ Tự động tìm tất cả file `.ttl` trong dự án
- ✅ Kiểm tra kết nối GraphDB
- ✅ Import nhiều file cùng lúc
- ✅ Báo cáo kết quả chi tiết

**Yêu cầu:**
- GraphDB Desktop đã cài và đang chạy
- Repository đã được tạo trong GraphDB
- File `.env` có cấu hình đúng:
  ```env
  GRAPHDB_SERVER=http://localhost:7200
  GRAPHDB_REPOSITORY=tin_hoc_thcs
  GRAPHDB_USERNAME=admin
  GRAPHDB_PASSWORD=root
  ```

**Các file sẽ được import:**
- `KG_Design/kg_grade7.ttl`
- `KG_Design/kg_grade7_with_knn.ttl`
- `KG_Design/kg_grade7_with_ppr.ttl`
- `KG_Design/grade6/out/*.ttl` (tất cả file trong thư mục)

---

### 4. Run ML Pipeline (`run_ml_pipeline.py`)

**Chức năng:** Chạy pipeline Machine Learning hoàn chỉnh

**Cách chạy:**
```bash
python scripts/run_ml_pipeline.py
```

**Các bước:**
1. ✅ Kiểm tra điều kiện tiên quyết
2. ✅ Chạy KNN (phát hiện học sinh yếu)
3. ✅ Chạy PPR (gợi ý bài học)
4. ✅ Tạo báo cáo kết quả

**Yêu cầu:**
- Đã cài đặt: `pip install -r requirements.txt`
- File KG đã có: `KG_Design/kg_grade7.ttl`
- Dữ liệu học sinh và kết quả

**Output:**
- `KG_Design/kg_grade7_with_knn.ttl` - KG với thông tin học sinh yếu
- `KG_Design/kg_grade7_with_ppr.ttl` - KG với gợi ý bài học
- `ML_PIPELINE_REPORT.json` - Báo cáo chi tiết

---

### 5. Test Hệ Thống (`test_complete_system.py`)

**Chức năng:** Kiểm tra toàn bộ hệ thống

**Cách chạy:**
```bash
python scripts/test_complete_system.py
```

**Kiểm tra:**
- ✅ Database connection (file config)
- ✅ API files (save_result.php, get_results.php)
- ✅ GraphDB setup (file .env, import script)
- ✅ ML outputs (file KNN, PPR)
- ✅ HTML files (thư mục Web)

**Output:**
- `TEST_REPORT.json` - Báo cáo chi tiết

---

## 🔧 CẤU HÌNH

### 1. File `.env` (cho GraphDB)

Tạo file `.env` trong thư mục gốc:

```env
GRAPHDB_SERVER=http://localhost:7200
GRAPHDB_REPOSITORY=tin_hoc_thcs
GRAPHDB_USERNAME=admin
GRAPHDB_PASSWORD=root
```

### 2. File `backend_api/api/config.php`

Cập nhật thông tin database:

```php
define('DB_HOST', 'localhost');
define('DB_NAME', 'tinhoc321_quiz');
define('DB_USER', 'root');
define('DB_PASS', 'your_password');
```

### 3. File `scripts/update_endpoint_to_php_api.py`

Cập nhật endpoint PHP API:

```python
NEW_API_ENDPOINT = "https://your-domain.com/api/save_result.php"
```

---

## 📋 CHECKLIST TRƯỚC KHI CHẠY

### Trước khi chạy bất kỳ script nào:

- [ ] Đã cài đặt Python 3.8+
- [ ] Đã cài dependencies: `pip install -r requirements.txt`
- [ ] Đã có file `.env` (nếu dùng GraphDB)
- [ ] Đã có file `backend_api/create_database.sql`

### Trước khi chạy `setup_database.py`:

- [ ] MySQL đã được cài đặt (hoặc XAMPP/WAMP)
- [ ] Có quyền tạo database
- [ ] Biết username/password MySQL

### Trước khi chạy `import_all_kg.py`:

- [ ] GraphDB Desktop đã cài và đang chạy
- [ ] Đã tạo repository trong GraphDB
- [ ] File `.env` có cấu hình đúng
- [ ] Đã có file `.ttl` (chạy build_kg trước nếu chưa có)

### Trước khi chạy `run_ml_pipeline.py`:

- [ ] Đã cài đặt tất cả dependencies
- [ ] Đã có file KG: `KG_Design/kg_grade7.ttl`
- [ ] Có dữ liệu học sinh và kết quả

### Trước khi chạy `update_endpoint_to_php_api.py`:

- [ ] Đã có domain/hosting cho PHP API
- [ ] Backend API đã được deploy
- [ ] Database đã được setup

---

## 🚨 XỬ LÝ LỖI

### Lỗi: "Module not found"

```bash
pip install -r requirements.txt
```

### Lỗi: "GraphDB connection failed"

- Kiểm tra GraphDB Desktop đã chạy chưa
- Kiểm tra file `.env` có đúng không
- Kiểm tra repository đã tạo chưa
- Kiểm tra port 7200 có bị chặn không

### Lỗi: "MySQL connection failed"

- Kiểm tra MySQL đã chạy chưa
- Kiểm tra username/password trong `config.php`
- Kiểm tra database đã được tạo chưa

### Lỗi: "File not found"

- Đảm bảo đang chạy script từ thư mục gốc dự án
- Kiểm tra các file cần thiết đã có chưa
- Kiểm tra đường dẫn file

---

## 📊 BÁO CÁO

Các script sẽ tạo các file báo cáo JSON:

1. **`SETUP_REPORT.json`** - Báo cáo setup tổng thể
2. **`ML_PIPELINE_REPORT.json`** - Báo cáo ML pipeline
3. **`TEST_REPORT.json`** - Báo cáo test hệ thống

Đọc file JSON để xem chi tiết kết quả.

---

## 💡 TIPS

1. **Chạy từng bước một:** Nếu gặp lỗi, chạy từng script riêng để dễ debug

2. **Kiểm tra log:** Các script sẽ in ra console, đọc kỹ để biết lỗi

3. **Backup trước:** Nếu có dữ liệu quan trọng, backup trước khi chạy

4. **Test thử:** Chạy test sau mỗi bước để đảm bảo thành công

5. **Đọc báo cáo:** Sau khi chạy, đọc file JSON để xem chi tiết

---

## 🎯 THỨ TỰ KHUYẾN NGHỊ

### Tuần 1: Setup Cơ Bản
1. ✅ Chạy `setup_database.py`
2. ✅ Chạy `update_endpoint_to_php_api.py`
3. ✅ Test API endpoints

### Tuần 2: Knowledge Graph
1. ✅ Setup GraphDB Desktop
2. ✅ Chạy `import_all_kg.py`
3. ✅ Test queries trong GraphDB

### Tuần 3: Machine Learning
1. ✅ Chuẩn bị dữ liệu
2. ✅ Chạy `run_ml_pipeline.py`
3. ✅ Kiểm tra kết quả

### Tuần 4: Hoàn Thiện
1. ✅ Chạy `test_complete_system.py`
2. ✅ Sửa các lỗi còn lại
3. ✅ Viết luận văn

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề:

1. **Đọc file báo cáo:** Xem file JSON để biết lỗi chi tiết
2. **Kiểm tra log:** Đọc console output
3. **Xem tài liệu:** Đọc `scripts/README_AUTOMATION.md`
4. **Chạy từng bước:** Chạy script riêng để dễ debug

---

## ✅ KẾT LUẬN

Với các script tự động hóa này, bạn có thể:

- ✅ Setup toàn bộ hệ thống nhanh chóng
- ✅ Giảm thiểu lỗi thủ công
- ✅ Có báo cáo chi tiết về tiến độ
- ✅ Dễ dàng kiểm tra và debug

**Chúc bạn thành công! 🚀**

---

**Tài liệu được tạo:** Hôm nay  
**Phiên bản:** 1.0

