# 📊 HƯỚNG DẪN XEM KẾT QUẢ HỌC SINH

## 🎯 TỔNG QUAN

Kết quả làm bài của học sinh được lưu tại **3 nơi** và có thể xem qua **3 cách**:

1. **Dashboard PHP (MySQL)** - Kết quả thực tế từ database
2. **Dashboard HTML** - Giao diện mẫu với dữ liệu demo
3. **API get_results.php** - Lấy dữ liệu qua API

---

## 📍 CÁCH 1: DASHBOARD PHP (KHUYẾN NGHỊ)

### **Đường dẫn:**
```
backend_api/dashboard/index.php
```

### **Truy cập:**
1. **Local (sau khi deploy Backend API):**
   ```
   http://localhost/backend_api/dashboard/index.php
   ```
   
2. **Online (sau khi upload lên hosting):**
   ```
   https://yourdomain.com/backend_api/dashboard/index.php
   ```

### **Tính năng:**
- ✅ **Thống kê tổng quan:** Tổng học sinh, Lượt làm bài, Điểm TB, Số quiz, Số lớp
- ✅ **Kết quả gần đây:** 20 kết quả mới nhất với thông tin đầy đủ
- ✅ **Thống kê theo lớp:** Điểm trung bình, số học sinh, lượt làm bài của mỗi lớp
- ✅ **Thống kê theo bài quiz:** Điểm TB, cao nhất, thấp nhất của từng bài
- ✅ **Dữ liệu thời gian thực:** Tự động lấy từ MySQL database

### **Hướng dẫn sử dụng:**

#### **Bước 1: Đảm bảo Backend API đã được triển khai**
- Database MySQL đã được tạo (chạy `create_database.sql`)
- File `config.php` đã cấu hình kết nối database
- Backend API đã được upload lên hosting (nếu xem online)

#### **Bước 2: Truy cập Dashboard**
- Mở trình duyệt và vào URL dashboard
- Nếu có lỗi, kiểm tra:
  - Database có kết nối được không
  - File `config.php` có đúng cấu hình không
  - Database có dữ liệu chưa (nếu chưa có, dashboard sẽ hiển thị 0)

#### **Bước 3: Xem kết quả**
- **Thẻ thống kê:** Xem tổng quan ở trên cùng
- **Bảng "Kết quả gần đây":** Xem chi tiết từng lần làm bài
- **Bảng "Thống kê theo lớp":** So sánh giữa các lớp
- **Bảng "Thống kê theo bài quiz":** Xem bài nào khó/dễ nhất

### **Screenshot mô tả:**
```
┌─────────────────────────────────────────────────────┐
│  📊 Dashboard Kết Quả Trắc Nghiệm                   │
├─────────────────────────────────────────────────────┤
│  [Tổng HS]  [Lượt làm]  [ĐTB]  [Số quiz]  [Số lớp] │
├─────────────────────────────────────────────────────┤
│  Kết quả gần đây        │  Thống kê theo lớp        │
│  [Bảng chi tiết]        │  [Bảng theo lớp]          │
├─────────────────────────────────────────────────────┤
│  Thống kê theo bài quiz                             │
│  [Bảng chi tiết theo quiz]                          │
└─────────────────────────────────────────────────────┘
```

---

## 📍 CÁCH 2: DASHBOARD HTML (DEMO)

### **Đường dẫn:**
```
Web_Teacher/dashboard.html
```

### **Truy cập:**
1. **Local:**
   - Mở trực tiếp file `Web_Teacher/dashboard.html` bằng trình duyệt
   - Hoặc: `file:///D:/A_De_tai_Tot_nghiep/Web_Teacher/dashboard.html`

2. **GitHub Pages:**
   ```
   https://ngohiep123.github.io/tinhoc321/Web_Teacher/dashboard.html
   ```

### **Tính năng:**
- ✅ Giao diện đẹp với TailwindCSS
- ✅ Biểu đồ trực quan với Chart.js
- ✅ Hiển thị học sinh cần can thiệp (mẫu)
- ✅ Gợi ý bài học từ PPR (mẫu)
- ⚠️ **Dữ liệu là mẫu (demo)**, không phải kết quả thực

### **Lưu ý:**
- Dashboard HTML này chỉ dùng để **xem giao diện** và **demo**
- Dữ liệu hiển thị là **hardcoded** (cố định)
- Để xem kết quả thực, cần dùng **Dashboard PHP**

---

## 📍 CÁCH 3: API get_results.php

### **Đường dẫn:**
```
backend_api/api/get_results.php
```

### **Truy cập:**
1. **Local:**
   ```
   http://localhost/backend_api/api/get_results.php
   ```

2. **Online:**
   ```
   https://yourdomain.com/backend_api/api/get_results.php
   ```

### **Tính năng:**
- ✅ **API REST** để lấy kết quả dưới dạng JSON
- ✅ **Lọc theo:** quiz_id, class_name, student_name, limit
- ✅ **Phù hợp cho:** Tích hợp vào ứng dụng khác, tạo dashboard tùy chỉnh

### **Hướng dẫn sử dụng:**

#### **1. Lấy tất cả kết quả (mặc định 100 bản ghi mới nhất):**
```bash
GET http://localhost/backend_api/api/get_results.php
```

#### **2. Lọc theo quiz:**
```bash
GET http://localhost/backend_api/api/get_results.php?quiz_id=K6_A1
```

#### **3. Lọc theo lớp:**
```bash
GET http://localhost/backend_api/api/get_results.php?class_name=6/14
```

#### **4. Lọc theo học sinh:**
```bash
GET http://localhost/backend_api/api/get_results.php?student_name=Nguyễn Văn A
```

#### **5. Giới hạn số lượng:**
```bash
GET http://localhost/backend_api/api/get_results.php?limit=50
```

#### **6. Kết hợp nhiều filter:**
```bash
GET http://localhost/backend_api/api/get_results.php?quiz_id=K6_A1&class_name=6/14&limit=20
```

### **Ví dụ Response:**
```json
{
  "success": true,
  "count": 25,
  "data": [
    {
      "id": 1,
      "student_name": "Nguyễn Văn A",
      "class_name": "6/14",
      "quiz_id": "K6_A1",
      "score": 8,
      "total": 10,
      "percentage": 80.0,
      "duration": 450,
      "created_at": "2024-12-15 10:30:00"
    },
    ...
  ]
}
```

### **Sử dụng trong JavaScript:**
```javascript
async function loadResults() {
  try {
    const response = await fetch('http://localhost/backend_api/api/get_results.php?quiz_id=K6_A1');
    const data = await response.json();
    
    if (data.success) {
      console.log('Tổng số kết quả:', data.count);
      console.log('Dữ liệu:', data.data);
    }
  } catch (error) {
    console.error('Lỗi:', error);
  }
}
```

---

## 📊 SO SÁNH 3 CÁCH XEM KẾT QUẢ

| Tính năng | Dashboard PHP | Dashboard HTML | API |
|-----------|--------------|----------------|-----|
| **Dữ liệu thực** | ✅ Có | ❌ Mẫu | ✅ Có |
| **Giao diện** | ✅ Đẹp | ✅ Đẹp | ❌ JSON |
| **Thống kê** | ✅ Đầy đủ | ✅ Mẫu | ⚠️ Cần xử lý |
| **Tích hợp** | ⚠️ Khó | ❌ Không | ✅ Dễ |
| **Tùy chỉnh** | ⚠️ Khó | ✅ Dễ | ✅ Dễ |
| **Khuyến nghị** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

---

## 🎯 KHUYẾN NGHỊ

### **Nếu bạn là giáo viên:**
👉 Dùng **Dashboard PHP** để xem kết quả thực tế

### **Nếu bạn muốn xem giao diện:**
👉 Dùng **Dashboard HTML** để xem demo

### **Nếu bạn muốn tích hợp vào hệ thống khác:**
👉 Dùng **API get_results.php** để lấy dữ liệu JSON

---

## 🔧 CÁCH TRIỂN KHAI DASHBOARD PHP

### **Bước 1: Tạo Database**
```sql
-- Chạy file create_database.sql
mysql -u root -p < backend_api/create_database.sql
```

### **Bước 2: Cấu hình Database**
```php
// Sửa file backend_api/api/config.php
define('DB_HOST', 'localhost');
define('DB_NAME', 'tin_hoc_thcs');
define('DB_USER', 'your_username');
define('DB_PASS', 'your_password');
```

### **Bước 3: Upload lên hosting**
- Upload thư mục `backend_api/` lên hosting
- Đảm bảo hosting hỗ trợ PHP và MySQL
- Kiểm tra quyền truy cập database

### **Bước 4: Truy cập Dashboard**
```
https://yourdomain.com/backend_api/dashboard/index.php
```

---

## 📝 LƯU Ý

### **Nếu Dashboard PHP hiển thị lỗi:**

1. **Lỗi kết nối database:**
   - Kiểm tra `config.php` có đúng không
   - Kiểm tra database có tồn tại không
   - Kiểm tra user/password có đúng không

2. **Không có dữ liệu:**
   - Kiểm tra bảng `quiz_results` có dữ liệu chưa
   - Kiểm tra học sinh đã làm bài và lưu kết quả chưa
   - Kiểm tra endpoint lưu kết quả (`save_result.php`) có hoạt động không

3. **Lỗi 404:**
   - Kiểm tra đường dẫn file có đúng không
   - Kiểm tra file có tồn tại không
   - Kiểm tra cấu hình server (Apache/Nginx)

---

## 📚 TÀI LIỆU THAM KHẢO

- **Hướng dẫn triển khai Backend API:** `HUONG_DAN_TRIEN_KHAI_PHP_API.md`
- **So sánh giải pháp:** `SO_SANH_GIAI_PHAP_LUU_KET_QUA.md`
- **Backend API README:** `backend_api/README.md`

---

**Cập nhật:** $(date)

