# 🔧 HƯỚNG DẪN SỬA LỖI: TEST TRONG EDITOR OK NHƯNG WEB KHÔNG LƯU

## ✅ TÌNH TRẠNG HIỆN TẠI

- ✅ Chạy `testScript()` trong Google Apps Script Editor → **CÓ lưu được vào Google Sheet**
- ❌ Test trên web (từ browser/quiz HTML) → **KHÔNG lưu được**

→ Vấn đề nằm ở **deployment** hoặc **endpoint URL**.

---

## 🔍 CÁC NGUYÊN NHÂN CÓ THỂ

### **1. Script chưa được deploy sau khi sửa code**
- Code trong editor là bản mới nhất
- Nhưng deployment vẫn dùng code cũ

### **2. Endpoint URL trong HTML không đúng**
- URL trong HTML có thể không khớp với deployment mới
- Hoặc deployment cũ đã bị xóa

### **3. Deployment chưa được cập nhật**
- Cần deploy lại sau khi sửa code

---

## ✅ CÁCH SỬA

### **BƯỚC 1: Deploy Lại Google Apps Script**

1. **Trong Google Apps Script Editor:**
   - Đảm bảo code đã được **Save** (💾)

2. **Deploy script:**
   - Click **Deploy → Manage deployments**
   - Nếu chưa có deployment:
     - Click **Create deployment** (hoặc **New deployment**)
     - Chọn type: **Web app**
     - Execute as: **Me** (tài khoản của bạn)
     - Who has access: **Anyone** (hoặc **Anyone with Google account**)
     - Click **Deploy**
   - Nếu đã có deployment:
     - Click icon **Edit** (✏️) bên cạnh deployment
     - Chọn **New version** (hoặc để "Head")
     - Click **Deploy**

3. **Copy URL mới:**
   - Copy **Web App URL** (sẽ có format: `https://script.google.com/a/macros/.../exec`)

---

### **BƯỚC 2: Kiểm Tra Endpoint URL Trong HTML**

1. **Mở file HTML quiz** (ví dụ: `Web/K6_A1.html`)
2. **Tìm dòng có ENDPOINT:**
   ```javascript
   const ENDPOINT="https://script.google.com/a/macros/asianintlschool.edu.vn/s/.../exec";
   ```

3. **So sánh với URL từ deployment:**
   - URL trong HTML: `AKfycbxoj7jkOooCg_2ciiNIgbBjsLc2MIcGUgnIm_I43eYjPGiUOKwnloqUBCXWZOlOspWxLA`
   - URL từ deployment: `???`
   - **Nếu khác nhau → CẦN CẬP NHẬT**

---

### **BƯỚC 3: Cập Nhật Endpoint URL Trong HTML (Nếu Cần)**

Nếu URL deployment mới khác với URL trong HTML:

1. **Copy URL deployment mới**
2. **Cập nhật trong tất cả file HTML:**
   - Chạy script `update_endpoint_v2.py` với URL mới
   - Hoặc sửa thủ công trong mỗi file

---

### **BƯỚC 4: Test Endpoint Trực Tiếp**

1. **Mở file `test_endpoint_direct.html`** (đã tạo sẵn)
2. **Click nút "Test với no-cors"**
3. **Kiểm tra:**
   - Xem có lỗi gì không
   - Mở Google Sheet để xem có dòng mới không

Hoặc **test trực tiếp bằng URL:**
```
https://script.google.com/a/macros/asianintlschool.edu.vn/s/AKfycbxoj7jkOooCg_2ciiNIgbBjsLc2MIcGUgnIm_I43eYjPGiUOKwnloqUBCXWZOlOspWxLA/exec?student_name=Test&class_name=6/1&quiz_id=K6_A1&score=8&total=10&duration=120
```

**Kết quả mong đợi:**
- Browser hiển thị JSON response: `{"success":true,"message":"Đã lưu kết quả thành công",...}`
- Google Sheet có dòng mới

---

### **BƯỚC 5: Kiểm Tra Execution Logs**

1. **Trong Google Apps Script:**
   - Vào **Executions** (Lịch sử thực thi)
   - Xem các execution gần đây từ web
   - Kiểm tra:
     - ✅ **Success** (màu xanh) = Request đến được và chạy thành công
     - ❌ **Failed** (màu đỏ) = Có lỗi

2. **Xem logs chi tiết:**
   - Click vào execution
   - Xem logs để biết:
     - Request có đến được không?
     - Có lỗi gì không?
     - Dữ liệu có đúng không?

---

## 🔧 CẢI THIỆN HÀM sendResult

Để debug tốt hơn, có thể cải thiện hàm `sendResult` trong HTML:

```javascript
async function sendResult(name, className, quizId, score, total, duration) {
  try {
    const url = `${ENDPOINT}?student_name=${encodeURIComponent(name)}&class_name=${encodeURIComponent(className)}&quiz_id=${quizId}&score=${score}&total=${total}&duration=${duration}`;
    
    console.log('Sending result to:', url);
    console.log('Data:', {name, className, quizId, score, total, duration});
    
    // Thử với no-cors (như hiện tại)
    const response = await fetch(url, {
      method: 'GET',
      mode: 'no-cors',
      cache: 'no-cache'
    });
    
    console.log('Request sent (no-cors mode)');
    
    // Đợi một chút để đảm bảo request được gửi
    await new Promise(resolve => setTimeout(resolve, 500));
    
    document.getElementById('send-status').textContent = '✅ Đã lưu!';
    
  } catch (e) {
    console.error('Save error:', e);
    document.getElementById('send-status').textContent = '⚠️ Không lưu được: ' + e.message;
  }
}
```

---

## ✅ CHECKLIST

- [ ] Đã save code trong Google Apps Script Editor
- [ ] Đã deploy lại script (tạo deployment mới hoặc update)
- [ ] Đã copy URL deployment mới
- [ ] Đã kiểm tra URL trong HTML có đúng không
- [ ] Đã cập nhật URL trong HTML nếu cần
- [ ] Đã test endpoint trực tiếp bằng browser
- [ ] Đã kiểm tra Execution Logs trong Google Apps Script
- [ ] Đã test làm bài trên web và kiểm tra Google Sheet

---

## 🆘 NẾU VẪN KHÔNG ĐƯỢC

1. **Xem Execution Logs:**
   - Có execution từ web không?
   - Có lỗi gì không?

2. **Test URL trực tiếp:**
   - Mở URL endpoint trong browser
   - Xem có response JSON không
   - Kiểm tra Google Sheet có dữ liệu không

3. **Kiểm tra Quyền:**
   - Deployment có quyền "Anyone" không?
   - Script có quyền Editor trên Google Sheet không?

4. **Gửi thông tin:**
   - URL endpoint đang dùng
   - Logs từ Execution
   - Kết quả test URL trực tiếp

