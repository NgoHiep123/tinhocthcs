# 🧪 HƯỚNG DẪN TEST GOOGLE APPS SCRIPT

## ❌ LỖI ĐÃ GẶP

```
❌ Lỗi: TypeError: Cannot read properties of undefined (reading 'parameter')
```

**Nguyên nhân:** Đang chạy hàm `doGet()` trực tiếp trong editor mà không có tham số.

---

## ✅ CÁCH TEST ĐÚNG

### **CÁCH 1: Dùng Hàm testScript() (KHUYẾN NGHỊ)**

1. **Trong Google Apps Script Editor:**
   - Click dropdown "Select function" → chọn `testScript`
   - Click nút **Run** (▶️)
   - Xem logs: **View → Logs** hoặc **View → Executions**

2. **Kiểm tra kết quả:**
   - Xem logs có thông báo "✅ Đã lưu kết quả thành công" không
   - Mở Google Sheet để xem có dòng mới không

### **CÁCH 2: Test Qua URL (Giống như thực tế)**

1. **Lấy URL Web App:**
   - Trong Google Apps Script Editor
   - Vào **Deploy → Manage deployments**
   - Click icon **Copy URL** (📋) để copy Web App URL
   - Hoặc tạo deployment mới: **Deploy → New deployment**

2. **Test URL trong Browser:**
   ```
   [YOUR_WEB_APP_URL]?student_name=Nguyễn Văn A&class_name=6/14&quiz_id=K6_A1&score=8&total=10&duration=120
   ```

3. **Xem kết quả:**
   - Browser sẽ hiển thị JSON response
   - Kiểm tra Google Sheet có dòng mới không

### **CÁCH 3: Xem Tất Cả Sheet Trước**

Chạy hàm `listAllSheets()` để xem tên sheet:
1. Dropdown → chọn `listAllSheets`
2. Click **Run** (▶️)
3. Xem logs để biết tên sheet chính xác
4. Sửa tên sheet trong code cho đúng

---

## 📝 CÁC BƯỚC TEST CHI TIẾT

### **BƯỚC 1: Kiểm Tra Tên Sheet**

```javascript
// Chạy hàm này:
listAllSheets()

// Xem logs, ví dụ:
// 📋 Danh sách tất cả sheet:
//    1. "Sheet1"
//    2. "results"
//    3. "Data"
```

→ Ghi nhớ tên sheet chính xác

### **BƯỚC 2: Sửa Tên Sheet Trong Code**

Tìm dòng này trong `doGet()`:
```javascript
const sheetName = 'results'; // ← SỬA TÊN NÀY
```

Sửa thành tên sheet thực tế (ví dụ: `'Sheet1'`)

### **BƯỚC 3: Test Bằng testScript()**

1. Chọn function: `testScript`
2. Click **Run**
3. Xem logs:
   ```
   🧪 Bắt đầu test script...
   ✅ Đã lưu kết quả thành công:
      - Học sinh: Nguyễn Văn A
      - Lớp: 6/14
      - Bài: K6_A1
      - Điểm: 8/10 (80.00%)
      - Dòng: 2
   ```

### **BƯỚC 4: Kiểm Tra Google Sheet**

1. Mở file Google Sheet `result_thcs`
2. Xem có dòng mới với dữ liệu:
   - Timestamp
   - QuizID: K6_A1
   - Grade: 6
   - Class: 6/14
   - StudentName: Nguyễn Văn A
   - Score: 8
   - Total: 10
   - Percent: 80.00%

---

## ⚠️ LƯU Ý QUAN TRỌNG

### **1. KHÔNG chạy doGet() trực tiếp**
- ❌ **SAI:** Dropdown → `doGet` → Run
- ✅ **ĐÚNG:** Dropdown → `testScript` → Run

### **2. Script phải BOUND với Google Sheet**
- Script phải được tạo từ **trong Google Sheet** (Extensions → Apps Script)
- Hoặc nếu standalone, phải có Spreadsheet ID

### **3. Tên Sheet phải chính xác**
- Phân biệt chữ hoa/thường
- `'results'` ≠ `'Results'` ≠ `'RESULTS'`

### **4. Cần có Header trong Sheet**
- Dòng 1 phải có các cột header
- Nếu chưa có, thêm header trước khi test

---

## 🔧 CODE ĐÃ SỬA

Code mới đã được cập nhật để:
- ✅ Kiểm tra `e` có tồn tại không
- ✅ Log chi tiết để debug
- ✅ Báo lỗi rõ ràng nếu thiếu thông tin

---

## 📋 CHECKLIST TEST

- [ ] Đã chạy `listAllSheets()` để xem tên sheet
- [ ] Đã sửa tên sheet trong code cho đúng
- [ ] Đã kiểm tra sheet có header chưa
- [ ] Đã chạy `testScript()` (KHÔNG chạy `doGet()`)
- [ ] Đã xem logs để kiểm tra kết quả
- [ ] Đã mở Google Sheet để xem dữ liệu mới
- [ ] Nếu có lỗi, đã đọc thông báo lỗi trong logs

---

## 🆘 NẾU VẪN LỖI

### **Lỗi: "Không tìm thấy sheet"**
→ Sửa tên sheet trong code cho đúng

### **Lỗi: "getActiveSpreadsheet() is null"**
→ Script không bound với Google Sheet, cần dùng Spreadsheet ID

### **Lỗi: "Cannot append row"**
→ Kiểm tra quyền, script cần quyền Editor

### **Không có dữ liệu trong Sheet**
→ Kiểm tra logs xem có lỗi gì, hoặc sheet có đúng không

