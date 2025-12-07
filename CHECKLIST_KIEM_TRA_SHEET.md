# ✅ CHECKLIST KIỂM TRA - TÊN SHEET

## 🎯 MỤC TIÊU

Xác định tên sheet chính xác trong Google Sheet `result_thcs` và sửa code cho đúng.

---

## 📋 CÁC BƯỚC KIỂM TRA

### **BƯỚC 1: Kiểm Tra Tên Sheet Trong Google Sheet**

1. Mở file Google Sheet `result_thcs` trên Google Drive
2. Xem **tab ở dưới cùng** (ví dụ: "Sheet1", "results", "Results")
3. **Ghi lại tên sheet:** ________________

---

### **BƯỚC 2: Chạy Hàm listAllSheets()**

1. Mở Google Apps Script Editor
2. Dropdown → chọn `listAllSheets`
3. Click **Run** (▶️)
4. Xem logs: **View → Logs**

**Kết quả:**
```
📋 Danh sách tất cả sheet:
   1. "_____________"
   2. "_____________"
   ...
```

**Ghi lại tên sheet chính xác:** ________________

---

### **BƯỚC 3: So Sánh**

- [ ] Tên sheet trong Google Sheet (Bước 1): ________________
- [ ] Tên sheet trong logs (Bước 2): ________________
- [ ] Tên sheet trong code hiện tại: `'results'`

**Nếu khác nhau → CẦN SỬA CODE**

---

### **BƯỚC 4: Sửa Code**

Trong file `code_google_apps_script_fixed.js`, tìm và sửa **3 chỗ:**

#### **Chỗ 1: Dòng 57 (hàm doGet)**
```javascript
// TRƯỚC:
const sheetName = 'results';

// SAU (sửa thành tên sheet thực tế):
const sheetName = 'TÊN_SHEET_THỰC_TẾ'; // ← ĐIỀN VÀO ĐÂY
```

#### **Chỗ 2: Dòng 169 (hàm testScript)**
```javascript
// TRƯỚC:
const sheetName = 'results';

// SAU (sửa thành TÊN GIỐNG với chỗ 1):
const sheetName = 'TÊN_SHEET_THỰC_TẾ'; // ← ĐIỀN VÀO ĐÂY
```

#### **Chỗ 3: Dòng 204 (hàm clearTestData)**
```javascript
// TRƯỚC:
const sheetName = 'results';

// SAU (sửa thành TÊN GIỐNG):
const sheetName = 'TÊN_SHEET_THỰC_TẾ'; // ← ĐIỀN VÀO ĐÂY
```

---

### **BƯỚC 5: Copy Code Đã Sửa Vào Google Apps Script**

1. Copy toàn bộ code từ file `code_google_apps_script_fixed.js` (đã sửa tên sheet)
2. Paste vào Google Apps Script Editor
3. Click **Save** (💾)

---

### **BƯỚC 6: Test**

1. Chạy hàm `testScript()`:
   - Dropdown → chọn `testScript`
   - Click **Run** (▶️)

2. Xem logs (View → Logs):
   - [ ] Có thông báo "✅ Đã lưu kết quả thành công"?
   - [ ] Không có lỗi?

3. Kiểm tra Google Sheet:
   - [ ] Có dòng dữ liệu mới được thêm vào?

---

## ✅ HOÀN THÀNH

- [ ] Đã xác định tên sheet chính xác
- [ ] Đã sửa code ở 3 chỗ
- [ ] Đã copy code vào Google Apps Script
- [ ] Đã test và thấy dữ liệu trong Google Sheet

---

## 🆘 NẾU VẪN KHÔNG ĐƯỢC

1. Copy toàn bộ log từ Google Apps Script
2. Gửi kèm tên sheet bạn đã xác định
3. Mô tả các bước bạn đã làm

