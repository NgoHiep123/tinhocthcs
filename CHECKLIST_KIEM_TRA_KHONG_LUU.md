# ✅ CHECKLIST KIỂM TRA - TẠI SAO KHÔNG LƯU KẾT QUẢ

## 🎯 TÌNH TRẠNG
- ✅ Endpoint đã đúng: `AKfycbydBX3A2x7rES_Re5OnfdI3aybBCp-vBa7YNdJ2UUHzjGyo1wFK2mqvLLmdypJkHnBDzw`
- ✅ testScript() trong editor → CÓ lưu được
- ❌ Test trên web (K6_B1) → KHÔNG lưu được

---

## ✅ CHECKLIST KIỂM TRA

### **1. KIỂM TRA HỌC SINH CÓ ĐĂNG NHẬP KHÔNG**

- [ ] Mở trang quiz K6_B1
- [ ] Xem góc trên bên phải:
  - [ ] Có hiển thị tên học sinh? (ví dụ: "👤 Nguyễn Văn A · Lớp 6/14")
  - [ ] Nếu KHÔNG có → Học sinh **CHƯA ĐĂNG NHẬP**

- [ ] Sau khi hoàn thành bài:
  - [ ] Có hiện "✅ Đã lưu!" hay "Chưa đăng nhập"?

**→ Nếu hiện "Chưa đăng nhập" → Đây là nguyên nhân!**

---

### **2. TEST ENDPOINT TRỰC TIẾP**

Mở URL này trong browser:
```
https://script.google.com/a/macros/asianintlschool.edu.vn/s/AKfycbydBX3A2x7rES_Re5OnfdI3aybBCp-vBa7YNdJ2UUHzjGyo1wFK2mqvLLmdypJkHnBDzw/exec?student_name=Test&class_name=6/1&quiz_id=K6_B1&score=8&total=10&duration=120
```

- [ ] Browser có hiển thị JSON response?
  - [ ] Nếu có: `{"success":true,"message":"Đã lưu kết quả thành công",...}` → ✅ Endpoint hoạt động!
  - [ ] Nếu không: ❌ Endpoint có vấn đề

- [ ] Mở Google Sheet `result_thcs`:
  - [ ] Có dòng mới với dữ liệu "Test" không?
  - [ ] Nếu có → ✅ Script hoạt động đúng!

---

### **3. KIỂM TRA EXECUTION LOGS**

1. Vào Google Apps Script: https://script.google.com
2. Đăng nhập bằng `@asianintlschool.edu.vn`
3. Tìm script có ID: `AKfycbydBX3A2x7rES_Re5OnfdI3aybBCp-vBa7YNdJ2UUHzjGyo1wFK2mqvLLmdypJkHnBDzw`
4. Vào "Executions" (Lịch sử thực thi)
5. Làm bài K6_B1 trên web
6. Xem Executions:

- [ ] Có execution mới từ web không?
  - [ ] Nếu KHÔNG có → Request không đến được endpoint
  - [ ] Nếu có execution:
    - [ ] Status là "Success" hay "Failed"?
    - [ ] Click vào để xem logs chi tiết

---

### **4. KIỂM TRA CONSOLE (F12)**

1. Mở trang quiz K6_B1
2. Nhấn **F12** để mở Developer Tools
3. Vào tab **Console**
4. Làm bài và hoàn thành
5. Xem Console:

- [ ] Có log nào không?
- [ ] Có lỗi gì không? (màu đỏ)

---

## 🔍 PHÂN TÍCH KẾT QUẢ

### **Trường hợp 1: Học sinh CHƯA ĐĂNG NHẬP**
**Triệu chứng:**
- Không thấy tên học sinh ở góc trên
- Sau khi hoàn thành, hiện "Chưa đăng nhập"

**Giải pháp:**
- Học sinh cần đăng nhập trước khi làm bài
- Hoặc sửa code để vẫn gửi kết quả dù chưa đăng nhập

### **Trường hợp 2: Request KHÔNG đến được endpoint**
**Triệu chứng:**
- Không có execution mới trong Google Apps Script
- Console có lỗi CORS hoặc network

**Giải pháp:**
- Kiểm tra deployment
- Kiểm tra URL endpoint
- Kiểm tra network/firewall

### **Trường hợp 3: Endpoint có lỗi**
**Triệu chứng:**
- Có execution nhưng status là "Failed"
- Logs có lỗi cụ thể

**Giải pháp:**
- Xem logs để biết lỗi gì
- Sửa code Google Apps Script

---

## 🆘 GỬI THÔNG TIN ĐỂ ĐƯỢC HỖ TRỢ

Nếu vẫn không được, gửi cho tôi:

1. **Học sinh có đăng nhập không?**
   - Có thấy tên học sinh ở góc trên không?
   - Sau khi hoàn thành, hiện gì? ("✅ Đã lưu!" hay "Chưa đăng nhập"?)

2. **Kết quả test endpoint trực tiếp:**
   - Có thấy JSON response không?
   - Google Sheet có dữ liệu không?

3. **Execution Logs:**
   - Có execution mới từ web không?
   - Status là gì? (Success/Failed)
   - Logs có gì?

4. **Console logs:**
   - Có log nào không?
   - Có lỗi gì không?

