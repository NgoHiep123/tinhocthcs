# 📊 HƯỚNG DẪN XEM KẾT QUẢ TRÊN GOOGLE SHEETS

## 🎯 TỔNG QUAN

Kết quả làm bài của học sinh được lưu vào **Google Sheets** thông qua Google Apps Script.

**Endpoint hiện tại:**
```
https://script.google.com/a/macros/asianintlschool.edu.vn/s/AKfycbytwRuA512UKakrHpIoURxfAn8-h6XB8e2Gs-cah4gxZHC7-iJOJrl-Qeg_5O-XAfrNjA/exec
```

**ID triển khai:**
```
AKfycbytwRuA512UKakrHpIoURxfAn8-h6XB8e2Gs-cah4gxZHC7-iJOJrl-Qeg_5O-XAfrNjA
```

---

## 📍 CÁCH 1: TỪ GOOGLE APPS SCRIPT

### **Bước 1: Truy cập Google Apps Script**
1. Vào: https://script.google.com
2. Đăng nhập bằng tài khoản **@asianintlschool.edu.vn**

### **Bước 2: Tìm Script**
1. Tìm script có ID: `AKfycbytwRuA512UKakrHpIoURxfAn8-h6XB8e2Gs-cah4gxZHC7-iJOJrl-Qeg_5O-XAfrNjA`
2. Hoặc tìm script có tên liên quan đến "Quiz", "Trắc nghiệm", "Save Result"

### **Bước 3: Xem Code để tìm Spreadsheet**
Trong code của script, tìm dòng có:
```javascript
SpreadsheetApp.openById('SPREADSHEET_ID')
// hoặc
SpreadsheetApp.openByUrl('https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/...')
```

### **Bước 4: Mở Google Sheet**
- Copy ID hoặc URL từ code
- Mở Google Sheet đó để xem kết quả

---

## 📍 CÁCH 2: TỪ GOOGLE DRIVE

### **Bước 1: Truy cập Google Drive**
1. Vào: https://drive.google.com
2. Đăng nhập bằng tài khoản **@asianintlschool.edu.vn**

### **Bước 2: Tìm File Google Sheet**
Tìm file có tên như:
- "Quiz Results"
- "Kết quả trắc nghiệm"
- "Student Results"
- "Tin học THCS Results"
- Hoặc tên khác liên quan

### **Bước 3: Mở File**
Click vào file để xem kết quả

---

## 📍 CÁCH 3: TỪ LỊCH SỬ GOOGLE APPS SCRIPT

### **Bước 1: Xem Execution Log**
1. Vào Google Apps Script
2. Chọn script
3. Vào **Executions** (Lịch sử thực thi)
4. Xem các lần thực thi gần đây

### **Bước 2: Kiểm tra Logs**
- Xem logs để biết script đã ghi vào file nào
- Có thể thấy tên file hoặc ID Spreadsheet trong logs

---

## 📊 CẤU TRÚC DỮ LIỆU TRONG GOOGLE SHEETS

Kết quả thường được lưu với các cột:

| Cột | Mô tả |
|-----|-------|
| **student_name** | Tên học sinh |
| **class_name** | Tên lớp |
| **quiz_id** | Mã bài (ví dụ: K6_A1) |
| **score** | Số điểm đạt được |
| **total** | Tổng số câu |
| **duration** | Thời gian làm bài (giây) |
| **timestamp** | Thời gian nộp bài |

---

## 🔍 TÌM NHANH GOOGLE SHEET

### **Nếu bạn có quyền truy cập Script:**

1. Mở Google Apps Script
2. Tìm script với ID trên
3. Xem code, tìm dòng:
   ```javascript
   var sheet = SpreadsheetApp.openById('...');
   // hoặc
   var sheet = SpreadsheetApp.openByUrl('...');
   ```
4. Copy ID/URL và mở trong Google Sheets

### **Nếu không có quyền:**

Liên hệ người quản lý Google Apps Script để:
- Xin quyền truy cập
- Hoặc xin link trực tiếp đến Google Sheet

---

## 📝 LƯU Ý

- ✅ Kết quả được lưu **tự động** sau mỗi lần học sinh hoàn thành bài
- ✅ Dữ liệu được lưu vào Google Sheets **ngay lập tức**
- ✅ Có thể **xem, sắp xếp, lọc** dữ liệu trong Google Sheets
- ✅ Có thể **xuất** dữ liệu ra Excel/CSV nếu cần

---

## 🆘 KHÔNG TÌM THẤY GOOGLE SHEET?

1. **Kiểm tra quyền truy cập:**
   - Đảm bảo đăng nhập đúng tài khoản @asianintlschool.edu.vn
   - Kiểm tra xem có quyền xem file không

2. **Liên hệ quản trị viên:**
   - Người tạo Google Apps Script
   - Người quản lý hệ thống

3. **Kiểm tra Script:**
   - Xem script có đang chạy đúng không
   - Kiểm tra logs trong Google Apps Script

---

## ✅ SAU KHI TÌM THẤY

Sau khi tìm thấy Google Sheet, bạn có thể:
- 📊 Xem tất cả kết quả
- 🔍 Lọc theo lớp, bài, học sinh
- 📈 Tạo biểu đồ thống kê
- 📥 Xuất dữ liệu ra Excel
- 📧 Chia sẻ với giáo viên khác

