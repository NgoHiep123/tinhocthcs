# 🔍 HƯỚNG DẪN KIỂM TRA CUỐI CÙNG

## ❌ VẤN ĐỀ HIỆN TẠI

File CSV `result_thcs - results.csv` chỉ có header, **KHÔNG có dữ liệu**.
→ Kết quả không được lưu vào Google Sheet.

---

## ✅ CÁC BƯỚC KIỂM TRA VÀ SỬA LỖI

### **BƯỚC 1: Kiểm Tra Tên Sheet Trong Google Sheet**

1. Mở file Google Sheet `result_thcs` trên Google Drive
2. Xem tên sheet ở **tab dưới cùng** (ví dụ: "Sheet1", "results", "Results")
3. **Ghi nhớ TÊN CHÍNH XÁC** (phân biệt chữ hoa/thường)

**Ví dụ:**
- Nếu tab hiển thị: `results` → Tên sheet là `'results'`
- Nếu tab hiển thị: `Sheet1` → Tên sheet là `'Sheet1'`
- Nếu tab hiển thị: `Results` → Tên sheet là `'Results'`

---

### **BƯỚC 2: Chạy Hàm listAllSheets() Trong Google Apps Script**

1. Mở Google Apps Script Editor
2. Dropdown "Select function" → chọn **`listAllSheets`**
3. Click **Run** (▶️)
4. Xem logs: **View → Logs**

**Kết quả mong đợi:**
```
📋 Danh sách tất cả sheet:
   1. "Sheet1"
   2. "results"
   3. ...
```

→ **Ghi nhớ tên sheet chính xác từ logs**

---

### **BƯỚC 3: Sửa Tên Sheet Trong Code**

Trong file `code_google_apps_script_fixed.js`, tìm và sửa:

**Dòng 57:**
```javascript
const sheetName = 'results'; // ← SỬA TÊN NÀY
```

**Sửa thành tên sheet thực tế** (ví dụ nếu sheet tên là "Sheet1"):
```javascript
const sheetName = 'Sheet1'; // ← TÊN SHEET THỰC TẾ
```

**Dòng 169 (trong hàm testScript):**
```javascript
const sheetName = 'results'; // ← ĐẢM BẢO TÊN GIỐNG VỚI DÒNG 57
```

**Sửa thành tên giống nhau:**
```javascript
const sheetName = 'Sheet1'; // ← CÙNG TÊN VỚI DÒNG 57
```

**Dòng 204 (trong hàm clearTestData):**
```javascript
const sheetName = 'results'; // ← SỬA TÊN NÀY (nếu cần)
```

---

### **BƯỚC 4: Kiểm Tra Header Trong Google Sheet**

1. Mở file Google Sheet `result_thcs`
2. Kiểm tra **dòng 1** có header không:

**Header cần có:**
```
A: Timestamp
B: QuizID
C: Grade
D: Class
E: StudentName
F: StudentID
G: Score
H: Total
I: Percent
J: AnswerJSON
K: YCCD_List
L: Concept_List
M: Pass/Fail
N: Device
O: Version
```

**Nếu chưa có header:**
- Thêm header vào dòng 1
- Hoặc để trống (code sẽ tự động append)

---

### **BƯỚC 5: Copy Code Đã Sửa Vào Google Apps Script**

1. Copy toàn bộ code từ file `code_google_apps_script_fixed.js`
2. Paste vào Google Apps Script Editor (thay thế code cũ)
3. **Đảm bảo đã sửa tên sheet** ở 3 chỗ:
   - Dòng 57 (hàm `doGet`)
   - Dòng 169 (hàm `testScript`)
   - Dòng 204 (hàm `clearTestData`)

---

### **BƯỚC 6: Lưu Và Deploy Script**

1. **Lưu code:**
   - Click **Save** (💾) hoặc `Ctrl+S`

2. **Deploy script:**
   - Click **Deploy → New deployment**
   - Hoặc **Deploy → Manage deployments → Edit**
   - Chọn type: **Web app**
   - Execute as: **Me** (hoặc tài khoản của bạn)
   - Who has access: **Anyone** (hoặc tùy chọn)
   - Click **Deploy**

3. **Copy URL mới:**
   - Copy **Web App URL** (để cập nhật vào HTML nếu cần)

---

### **BƯỚC 7: Test Script**

1. **Chạy hàm `testScript()`:**
   - Dropdown → chọn `testScript`
   - Click **Run** (▶️)

2. **Xem logs:**
   - **View → Logs**
   - Kiểm tra có thông báo:
     ```
     ✅ Đã lưu kết quả thành công:
        - Học sinh: Nguyễn Văn A
        - Lớp: 6/14
        - Bài: K6_A1
        - Điểm: 8/10 (80.00%)
        - Dòng: 2
     ```

3. **Kiểm tra Google Sheet:**
   - Mở file `result_thcs`
   - Xem có dòng mới được thêm vào không

---

### **BƯỚC 8: Test Từ Browser (Nếu Cần)**

1. **Lấy Web App URL:**
   - Trong Google Apps Script
   - **Deploy → Manage deployments**
   - Copy URL

2. **Test URL trong browser:**
   ```
   [YOUR_WEB_APP_URL]?student_name=Test&class_name=6/1&quiz_id=K6_A1&score=8&total=10&duration=120
   ```

3. **Xem kết quả:**
   - Browser sẽ hiển thị JSON response
   - Kiểm tra Google Sheet có dòng mới không

---

## 🔧 CÁC VẤN ĐỀ THƯỜNG GẶP

### **1. Lỗi: "Không tìm thấy sheet"**

**Nguyên nhân:**
- Tên sheet trong code không đúng
- Sheet không tồn tại

**Giải pháp:**
- Chạy `listAllSheets()` để xem tên sheet
- Sửa tên sheet trong code cho đúng

### **2. Lỗi: "getActiveSpreadsheet() is null"**

**Nguyên nhân:**
- Script không bound với Google Sheet
- Script là standalone

**Giải pháp:**
- Script phải được tạo từ **trong Google Sheet** (Extensions → Apps Script)
- Hoặc sửa code thành dùng Spreadsheet ID

### **3. Không có dữ liệu sau khi test**

**Nguyên nhân:**
- Script có lỗi nhưng không hiển thị
- Quyền không đủ

**Giải pháp:**
- Xem logs trong Google Apps Script
- Kiểm tra quyền Editor trên Google Sheet
- Test lại bằng `testScript()`

---

## ✅ CHECKLIST CUỐI CÙNG

- [ ] Đã chạy `listAllSheets()` và biết tên sheet chính xác
- [ ] Đã sửa tên sheet ở 3 chỗ trong code (dòng 57, 169, 204)
- [ ] Đã copy code đã sửa vào Google Apps Script Editor
- [ ] Đã lưu code trong Google Apps Script
- [ ] Đã deploy script (nếu cần)
- [ ] Đã chạy `testScript()` và thấy log "✅ Đã lưu kết quả thành công"
- [ ] Đã mở Google Sheet và thấy dòng dữ liệu mới
- [ ] Đã test từ browser (nếu cần)

---

## 🆘 NẾU VẪN KHÔNG ĐƯỢC

1. **Xem Execution Logs:**
   - Vào "Executions" trong Google Apps Script
   - Xem có lỗi gì không

2. **Kiểm tra Quyền:**
   - Script cần quyền "Editor" trên Google Sheet
   - Vào File → Share → Kiểm tra

3. **Test Thủ Công:**
   - Chạy `testScript()` và xem logs chi tiết
   - Copy log và gửi để được hỗ trợ

---

## 💡 LƯU Ý QUAN TRỌNG

**Tên sheet phải chính xác 100%:**
- Phân biệt chữ hoa/thường
- `'results'` ≠ `'Results'` ≠ `'RESULTS'`
- Không có khoảng trắng thừa

**Script phải BOUND với Google Sheet:**
- Script được tạo từ trong Google Sheet (Extensions → Apps Script)
- Nếu là standalone, phải dùng Spreadsheet ID

