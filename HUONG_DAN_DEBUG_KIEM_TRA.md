# 🔍 HƯỚNG DẪN DEBUG - KIỂM TRA TẠI SAO KHÔNG LƯU

## ✅ TÌNH TRẠNG HIỆN TẠI

- ✅ Endpoint đã đúng: `AKfycbydBX3A2x7rES_Re5OnfdI3aybBCp-vBa7YNdJ2UUHzjGyo1wFK2mqvLLmdypJkHnBDzw`
- ✅ testScript() trong editor → CÓ lưu được
- ❌ Test trên web (K6_Bai_1) → KHÔNG lưu được

---

## 🔍 CÁC NGUYÊN NHÂN CÓ THỂ

### **1. Học sinh chưa đăng nhập**
Code chỉ gửi kết quả nếu học sinh đã đăng nhập:
```javascript
if(student){
  sendResult(student.name,student.className,QUIZ_ID,score,quiz.length,duration)
}else{
  document.getElementById('send-status').textContent='Chưa đăng nhập'
}
```

**Kiểm tra:**
- Khi làm bài, có thấy tên học sinh hiển thị ở góc trên không?
- Sau khi hoàn thành, có hiện "Chưa đăng nhập" hay "✅ Đã lưu!"?

### **2. Request không đến được endpoint**
Với `mode: 'no-cors'`, browser không thể xác nhận request có thành công.

**Cách kiểm tra:**
- Xem Execution Logs trong Google Apps Script
- Xem Console (F12) khi làm bài

### **3. Deployment chưa được cập nhật**
Script trong editor khác với script đã deploy.

---

## ✅ CÁCH KIỂM TRA CHI TIẾT

### **BƯỚC 1: Kiểm Tra Học Sinh Có Đăng Nhập Không**

1. **Mở trang quiz** (ví dụ: K6_B1)
2. **Xem góc trên bên phải:**
   - Có hiển thị tên học sinh không? (ví dụ: "👤 Nguyễn Văn A · Lớp 6/14")
   - Nếu không có → Học sinh chưa đăng nhập

3. **Sau khi hoàn thành bài:**
   - Xem phần "Đang gửi kết quả…"
   - Có hiện "Chưa đăng nhập" hay "✅ Đã lưu!"?

### **BƯỚC 2: Mở Console (F12) Để Xem Logs**

1. **Mở trang quiz**
2. **Nhấn F12** để mở Developer Tools
3. **Vào tab Console**
4. **Làm bài và hoàn thành**
5. **Xem Console:**
   - Có log nào không?
   - Có lỗi gì không?

### **BƯỚC 3: Kiểm Tra Execution Logs Trong Google Apps Script**

1. **Vào Google Apps Script:**
   - https://script.google.com
   - Đăng nhập bằng `@asianintlschool.edu.vn`

2. **Tìm script:**
   - ID: `AKfycbydBX3A2x7rES_Re5OnfdI3aybBCp-vBa7YNdJ2UUHzjGyo1wFK2mqvLLmdypJkHnBDzw`

3. **Vào Executions:**
   - Click menu "Executions" (Lịch sử thực thi)
   - Làm bài trên web
   - Xem có execution mới không?

4. **Xem chi tiết:**
   - Click vào execution để xem logs
   - Có lỗi gì không?

### **BƯỚC 4: Test Endpoint Trực Tiếp**

Mở URL này trong browser:
```
https://script.google.com/a/macros/asianintlschool.edu.vn/s/AKfycbydBX3A2x7rES_Re5OnfdI3aybBCp-vBa7YNdJ2UUHzjGyo1wFK2mqvLLmdypJkHnBDzw/exec?student_name=Test&class_name=6/1&quiz_id=K6_B1&score=8&total=10&duration=120
```

**Kết quả:**
- Nếu thấy JSON: `{"success":true,...}` → Endpoint hoạt động!
- Kiểm tra Google Sheet có dòng mới không?

---

## 🔧 SỬA LỖI NẾU HỌC SINH CHƯA ĐĂNG NHẬP

Nếu học sinh chưa đăng nhập, có thể sửa code để vẫn gửi kết quả (nhưng không có tên):

**Sửa trong hàm showResults():**
```javascript
// TRƯỚC:
if(student){
  sendResult(student.name,student.className,QUIZ_ID,score,quiz.length,duration)
}else{
  document.getElementById('send-status').textContent='Chưa đăng nhập'
}

// SAU (tùy chọn - nếu muốn vẫn lưu dù chưa đăng nhập):
if(student){
  sendResult(student.name,student.className,QUIZ_ID,score,quiz.length,duration)
}else{
  // Vẫn gửi nhưng không có tên
  sendResult('Chưa đăng nhập','Chưa xác định',QUIZ_ID,score,quiz.length,duration)
}
```

---

## ✅ CHECKLIST DEBUG

- [ ] Học sinh có đăng nhập không? (xem tên ở góc trên)
- [ ] Sau khi hoàn thành, có hiện "✅ Đã lưu!" hay "Chưa đăng nhập"?
- [ ] Console (F12) có log gì không? Có lỗi không?
- [ ] Execution Logs có execution mới từ web không?
- [ ] Test endpoint trực tiếp có hoạt động không?
- [ ] Google Sheet có nhận được dữ liệu từ test trực tiếp không?

---

## 🆘 NẾU VẪN KHÔNG ĐƯỢC

Gửi cho tôi:
1. **Tên học sinh có hiển thị** khi làm bài không?
2. **Thông báo sau khi hoàn thành** là gì? ("✅ Đã lưu!" hay "Chưa đăng nhập"?)
3. **Execution Logs** từ Google Apps Script (screenshot hoặc copy log)
4. **Console logs** khi làm bài (F12 → Console)
5. **Kết quả test endpoint trực tiếp** (có thấy JSON không? Google Sheet có dữ liệu không?)

