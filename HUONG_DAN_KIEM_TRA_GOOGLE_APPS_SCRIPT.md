# 🔍 HƯỚNG DẪN KIỂM TRA GOOGLE APPS SCRIPT

## 🎯 VẤN ĐỀ

Kết quả không được lưu vào Google Sheet `result_thcs` mặc dù hiển thị "✅ Đã lưu!".

**Nguyên nhân có thể:**
1. Google Apps Script không nhận được request
2. Script có lỗi khi xử lý dữ liệu
3. Script không có quyền ghi vào Google Sheet
4. Tên file Google Sheet không đúng
5. Endpoint không hoạt động

---

## 📍 CÁCH 1: KIỂM TRA GOOGLE APPS SCRIPT LOGS

### **Bước 1: Truy cập Google Apps Script**
1. Vào: https://script.google.com
2. Đăng nhập bằng tài khoản **@asianintlschool.edu.vn**

### **Bước 2: Tìm Script**
- Tìm script có ID: `AKfycbytwRuA512UKakrHpIoURxfAn8-h6XB8e2Gs-cah4gxZHC7-iJOJrl-Qeg_5O-XAfrNjA`
- Hoặc tìm script liên quan đến "Quiz", "Save Result"

### **Bước 3: Xem Execution Logs**
1. Mở script
2. Click vào **"Executions"** (Lịch sử thực thi) ở menu bên trái
3. Xem các lần thực thi gần đây:
   - ✅ **Success** (màu xanh) = Script chạy thành công
   - ❌ **Failed** (màu đỏ) = Script có lỗi
   - ⏱️ **Timed out** = Script chạy quá lâu

### **Bước 4: Xem Chi Tiết Logs**
1. Click vào một execution để xem chi tiết
2. Xem **"Logs"** để biết:
   - Script có nhận được request không?
   - Dữ liệu có đúng không?
   - Có lỗi gì không?

---

## 📍 CÁCH 2: KIỂM TRA CODE GOOGLE APPS SCRIPT

### **Bước 1: Mở Script**
1. Vào Google Apps Script
2. Mở script có ID trên

### **Bước 2: Kiểm tra Code**
Tìm các phần quan trọng:

#### **1. Hàm doGet (nhận request GET)**
```javascript
function doGet(e) {
  // Kiểm tra xem có nhận được parameters không
  Logger.log('Received parameters:', e.parameter);
  
  // Lấy dữ liệu
  var student_name = e.parameter.student_name;
  var class_name = e.parameter.class_name;
  var quiz_id = e.parameter.quiz_id;
  var score = e.parameter.score;
  var total = e.parameter.total;
  var duration = e.parameter.duration;
  
  // ... code xử lý ...
}
```

#### **2. Phần mở Google Sheet**
```javascript
// Kiểm tra tên file có đúng không
var sheet = SpreadsheetApp.openById('SPREADSHEET_ID');
// hoặc
var sheet = SpreadsheetApp.openByName('result_thcs'); // Tên file
```

#### **3. Phần ghi dữ liệu**
```javascript
// Kiểm tra có ghi được không
sheet.appendRow([student_name, class_name, quiz_id, score, total, duration]);
```

### **Bước 3: Test Script**
1. Click **"Run"** (▶️) để test script
2. Xem logs để biết có lỗi gì không

---

## 📍 CÁCH 3: TEST ENDPOINT TRỰC TIẾP

### **Test trong Browser:**
1. Mở file `test_endpoint.html` (đã tạo sẵn)
2. Click nút "Test Endpoint"
3. Xem kết quả

### **Test bằng URL trực tiếp:**
Mở URL này trong browser (thay thế dữ liệu test):
```
https://script.google.com/a/macros/asianintlschool.edu.vn/s/AKfycbytwRuA512UKakrHpIoURxfAn8-h6XB8e2Gs-cah4gxZHC7-iJOJrl-Qeg_5O-XAfrNjA/exec?student_name=Test&class_name=6/1&quiz_id=K6_A1&score=8&total=10&duration=120
```

**Kết quả mong đợi:**
- Nếu thành công: Có thể thấy response hoặc redirect
- Nếu lỗi: Sẽ hiển thị lỗi

---

## 📍 CÁCH 4: KIỂM TRA GOOGLE SHEET

### **Bước 1: Mở Google Sheet**
1. Vào Google Drive
2. Tìm file `result_thcs`
3. Mở file

### **Bước 2: Kiểm tra**
1. **Xem có header không?**
   - Cần có các cột: student_name, class_name, quiz_id, score, total, duration, timestamp
   
2. **Xem có dữ liệu cũ không?**
   - Nếu có dữ liệu cũ nhưng không có dữ liệu mới = Script có vấn đề
   - Nếu hoàn toàn trống = Có thể chưa có header hoặc script chưa chạy

3. **Kiểm tra quyền:**
   - Đảm bảo Google Apps Script có quyền **Editor** trên file
   - Vào **File > Share** và kiểm tra

---

## 🔧 CÁC LỖI THƯỜNG GẶP

### **1. Script không nhận được request**
**Nguyên nhân:**
- Endpoint không đúng
- Script chưa được deploy
- Script bị xóa hoặc vô hiệu hóa

**Giải pháp:**
- Kiểm tra lại endpoint
- Deploy lại script
- Kiểm tra script có tồn tại không

### **2. Script nhận được nhưng không ghi được**
**Nguyên nhân:**
- Tên file Google Sheet không đúng
- Script không có quyền ghi
- Code có lỗi

**Giải pháp:**
- Kiểm tra tên file trong code
- Cấp quyền Editor cho script
- Xem logs để tìm lỗi

### **3. Dữ liệu bị thiếu hoặc sai**
**Nguyên nhân:**
- Parameters không đúng tên
- Code xử lý sai

**Giải pháp:**
- Kiểm tra tên parameters trong code
- So sánh với dữ liệu gửi đi

---

## ✅ CHECKLIST KIỂM TRA

- [ ] Google Apps Script có tồn tại và đang hoạt động
- [ ] Script đã được deploy với đúng ID
- [ ] Endpoint URL đúng
- [ ] Script có quyền Editor trên Google Sheet
- [ ] Tên file Google Sheet trong code đúng (`result_thcs`)
- [ ] Google Sheet có header đúng
- [ ] Script logs không có lỗi
- [ ] Test endpoint trực tiếp thành công

---

## 🆘 NẾU VẪN KHÔNG ĐƯỢC

1. **Xem logs chi tiết trong Google Apps Script**
2. **Test endpoint trực tiếp trong browser**
3. **Kiểm tra code Google Apps Script có đúng không**
4. **Liên hệ người tạo script để kiểm tra**

---

## 💡 GỢI Ý

Nếu Google Apps Script có vấn đề, có thể chuyển sang dùng **PHP API + MySQL** (Cách 2) để:
- ✅ Kiểm soát tốt hơn
- ✅ Debug dễ hơn
- ✅ Có dashboard xem kết quả
- ✅ Không phụ thuộc vào Google

