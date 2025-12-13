# ✅ CHECKLIST SẴN SÀNG DEMO

> Kiểm tra toàn bộ hệ thống trước khi demo

---

## 📊 1. FILE .TTL CHO GRAPHDB

### ✅ Đã có:
- [x] `KG_Design/kg_grade7.ttl` - Knowledge Graph cho khối 7
- [x] `KG_Design/kg_schema_grade7.ttl` - Schema định nghĩa
- [x] `KG_Design/grade6/out/*.ttl` - Các file TTL cho khối 6
  - [x] `students.ttl`
  - [x] `skills.ttl`
  - [x] `resources.ttl`
  - [x] `resource_skill.ttl`
  - [x] `question_skill.ttl`
  - [x] `prerequisites.ttl`
  - [x] `mastery.ttl`

### 📝 Scripts hỗ trợ:
- [x] `KG_Design/build_kg_grade7.py` - Tạo KG cho khối 7
- [x] `KG_Design/import_to_graphdb.py` - Upload lên GraphDB
- [x] `KG_Design/grade6/export_ttl.py` - Export TTL cho khối 6
- [x] `KG_Design/query_graphdb.py` - Query GraphDB
- [x] `KG_Design/test_graphdb_connection.py` - Test kết nối

### ⚠️ Cần kiểm tra:
- [ ] **Chạy lại script để tạo/update .ttl nếu có dữ liệu mới:**
  ```bash
  cd KG_Design
  python build_kg_grade7.py
  ```
- [ ] **Upload lên GraphDB:**
  ```bash
  python import_to_graphdb.py
  ```
  Hoặc import thủ công trong GraphDB Desktop:
  - Mở GraphDB Desktop
  - Tạo repository mới (OWL-Horst)
  - Import file `kg_grade7.ttl`

---

## 💾 2. HỆ THỐNG LƯU KẾT QUẢ HỌC SINH

### ✅ Backend API đã có:
- [x] `backend_api/api/save_result.php` - Lưu kết quả
- [x] `backend_api/api/get_results.php` - Lấy kết quả
- [x] `backend_api/api/config.php` - Cấu hình database
- [x] `backend_api/dashboard/index.php` - Dashboard giáo viên
- [x] `backend_api/create_database.sql` - Script tạo database

### ⚠️ VẤN ĐỀ HIỆN TẠI:
- [ ] **Các file HTML đang dùng Google Sheets API** thay vì PHP API
  - Hiện tại: `ENDPOINT="https://script.google.com/macros/s/.../exec"`
  - Nên chuyển sang: `ENDPOINT="http://your-domain.com/api/save_result.php"`

### 📝 Cách chuyển đổi:
1. **Cập nhật tất cả file HTML** để dùng PHP API:
   ```bash
   python scripts/update_endpoint_to_php_api.py
   ```

2. **Hoặc cập nhật thủ công** trong mỗi file HTML:
   ```javascript
   // Thay đổi từ:
   const ENDPOINT="https://script.google.com/macros/s/.../exec";
   
   // Sang:
   const ENDPOINT="http://your-domain.com/api/save_result.php";
   
   // Và cập nhật function sendResult():
   async function sendResult(name,className,quizId,score,total,duration){
     try{
       const response = await fetch(ENDPOINT, {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',
         },
         body: JSON.stringify({
           student_name: name,
           class_name: className,
           quiz_id: quizId,
           score: score,
           total: total,
           duration: duration
         })
       });
       const result = await response.json();
       if (result.success) {
         document.getElementById('send-status').textContent='✅ Đã lưu!'
       } else {
         document.getElementById('send-status').textContent='⚠️ Không lưu được'
       }
     }catch(e){
       document.getElementById('send-status').textContent='⚠️ Không lưu được'
     }
   }
   ```

3. **Setup database MySQL:**
   ```bash
   mysql -u root -p < backend_api/create_database.sql
   ```

4. **Cấu hình `backend_api/api/config.php`:**
   ```php
   define('DB_HOST', 'localhost');
   define('DB_NAME', 'tinhoc321_quiz');
   define('DB_USER', 'your_username');
   define('DB_PASS', 'your_password');
   ```

---

## 🎯 3. TRẠNG THÁI SẴN SÀNG DEMO

### ✅ Frontend - Đã hoàn thành:
- [x] **Khối 6:** 31 bài học + 8 bài kiểm tra (4 HK1 + 4 HK2)
- [x] **Khối 7:** 27 bài học + 8 bài kiểm tra (4 HK1 + 4 HK2)
- [x] **Khối 8:** 11+ bài học + 8 bài kiểm tra (4 HK1 + 4 HK2)
- [x] **Khối 9:** 14 bài học + 8 bài kiểm tra (4 HK1 + 4 HK2)
- [x] `index.html` - Trang chủ với đầy đủ các khối
- [x] `login.html` - Đăng nhập học sinh
- [x] Tất cả file HTML đã có giao diện đẹp, responsive

### ✅ Backend - Đã có:
- [x] PHP API để lưu/lấy kết quả
- [x] Dashboard giáo viên
- [x] Database schema

### ✅ Knowledge Graph - Đã có:
- [x] File .ttl cho khối 6 và 7
- [x] Scripts để build và import
- [x] Scripts để query

### ⚠️ CẦN HOÀN THIỆN TRƯỚC KHI DEMO:

#### A. Chuyển endpoint sang PHP API:
- [ ] Chạy script cập nhật endpoint:
  ```bash
  python scripts/update_endpoint_to_php_api.py
  ```
- [ ] Hoặc cập nhật thủ công tất cả file HTML

#### B. Setup Backend:
- [ ] Cài đặt MySQL server
- [ ] Tạo database:
  ```bash
  mysql -u root -p < backend_api/create_database.sql
  ```
- [ ] Cấu hình `backend_api/api/config.php`
- [ ] Test API: `http://your-domain.com/api/save_result.php`

#### C. Setup GraphDB:
- [ ] Cài đặt GraphDB Desktop
- [ ] Tạo repository mới (OWL-Horst)
- [ ] Import file `KG_Design/kg_grade7.ttl`
- [ ] Test query trong GraphDB

#### D. Kiểm tra tổng thể:
- [ ] Test đăng nhập: `login.html`
- [ ] Test làm bài: Chọn một bài bất kỳ
- [ ] Kiểm tra kết quả có lưu vào database không
- [ ] Kiểm tra dashboard giáo viên: `backend_api/dashboard/index.php`
- [ ] Kiểm tra GraphDB có dữ liệu không

---

## 📋 4. CHECKLIST TRƯỚC KHI DEMO

### Hệ thống Frontend:
- [ ] Tất cả file HTML hoạt động tốt
- [ ] Đăng nhập thành công
- [ ] Làm bài và submit kết quả thành công
- [ ] Kết quả hiển thị đúng

### Hệ thống Backend:
- [ ] MySQL database đã setup
- [ ] PHP API hoạt động (lưu/lấy kết quả)
- [ ] Dashboard giáo viên hiển thị dữ liệu
- [ ] CORS đã được cấu hình đúng

### Knowledge Graph:
- [ ] GraphDB đã cài đặt và chạy
- [ ] Repository đã được tạo
- [ ] File .ttl đã được import
- [ ] Có thể query được dữ liệu trong GraphDB

### Demo Script:
- [ ] Đã chuẩn bị kịch bản demo
- [ ] Đã test tất cả chức năng
- [ ] Đã chuẩn bị dữ liệu mẫu (nếu cần)

---

## 🚀 5. HƯỚNG DẪN DEMO NHANH

### Bước 1: Khởi động hệ thống
```bash
# 1. Khởi động MySQL
# 2. Khởi động web server (Apache/Nginx)
# 3. Khởi động GraphDB Desktop
```

### Bước 2: Kiểm tra
1. Mở `index.html` trong trình duyệt
2. Đăng nhập với `login.html`
3. Chọn một bài học bất kỳ
4. Làm bài và submit
5. Kiểm tra kết quả trong `backend_api/dashboard/index.php`

### Bước 3: Demo Knowledge Graph
1. Mở GraphDB Desktop
2. Vào repository đã import
3. Chạy một số SPARQL query mẫu:
   ```sparql
   # Xem tất cả học sinh
   SELECT ?student ?name WHERE {
     ?student a edu:Student .
     ?student edu:name ?name .
   }
   ```

---

## 📞 6. LIÊN HỆ & HỖ TRỢ

Nếu gặp vấn đề, kiểm tra:
1. **File hướng dẫn:**
   - `HUONG_DAN_TRIEN_KHAI_PHP_API.md`
   - `KG_Design/STEP_BY_STEP.md`
   - `backend_api/README.md`

2. **Logs:**
   - PHP error log
   - MySQL error log
   - GraphDB logs

3. **Test kết nối:**
   - Test PHP API: `curl http://your-domain.com/api/get_results.php`
   - Test GraphDB: `python KG_Design/test_graphdb_connection.py`

---

## ✅ KẾT LUẬN

**Tình trạng hiện tại:**
- ✅ Frontend: **Hoàn thành 100%**
- ⚠️ Backend: **Cần setup và cập nhật endpoint**
- ✅ Knowledge Graph: **Có file .ttl, cần import vào GraphDB**

**Cần làm trước khi demo:**
1. Chuyển endpoint từ Google Sheets sang PHP API
2. Setup MySQL database
3. Import .ttl vào GraphDB
4. Test toàn bộ hệ thống

**Ước tính thời gian:** 30-60 phút để hoàn thiện

