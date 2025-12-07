# 🔧 SỬA LỖI GOOGLE APPS SCRIPT

## ❌ VẤN ĐỀ TÌM THẤY

### **1. Tên Sheet Không Nhất Quán**
```javascript
// Trong hàm doGet():
const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('results'); // ❌ chữ thường

// Trong hàm testScript():
const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Results'); // ❌ chữ hoa
```

**→ Cần sửa thành TÊN SHEET ĐÚNG trong Google Sheet của bạn!**

### **2. Script Phải Được Bound Với Google Sheet**
Code đang dùng:
```javascript
SpreadsheetApp.getActiveSpreadsheet()
```
→ Có nghĩa là script **PHẢI** được đính kèm (bound) vào Google Sheet, không phải standalone script.

---

## ✅ CÁCH SỬA

### **BƯỚC 1: Kiểm Tra Tên Sheet Trong Google Sheet**

1. Mở file Google Sheet `result_thcs`
2. Xem tên của sheet ở tab dưới cùng (ví dụ: "Sheet1", "results", "Results", "Data")
3. **Ghi nhớ TÊN CHÍNH XÁC** (phân biệt chữ hoa/thường)

### **BƯỚC 2: Sửa Code Google Apps Script**

#### **Nếu Script ĐANG Bound Với Google Sheet:**

Sửa dòng này trong hàm `doGet()`:
```javascript
// THAY ĐỔI 'results' thành TÊN SHEET ĐÚNG của bạn
const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('results');
```

Ví dụ nếu tên sheet là "Sheet1":
```javascript
const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
```

#### **Nếu Script LÀ Standalone (không bound):**

Cần sửa thành dùng Spreadsheet ID hoặc URL:

**Cách 1: Dùng Spreadsheet ID**
```javascript
// Lấy Spreadsheet ID từ URL:
// https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
const SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID_HERE';
const sheet = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName('results');
```

**Cách 2: Dùng Spreadsheet Name**
```javascript
const SPREADSHEET_NAME = 'result_thcs';
const sheet = SpreadsheetApp.openByName(SPREADSHEET_NAME).getSheetByName('results');
```

### **BƯỚC 3: Đảm Bảo Sheet Có Header**

Kiểm tra Google Sheet có các cột header như sau (dòng 1):
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

---

## 📝 CODE ĐÃ SỬA (THAM KHẢO)

### **Code Hoàn Chỉnh (Bound Script):**

```javascript
function doGet(e) {
  try {
    // Lấy tham số từ URL
    const studentName = e.parameter.student_name || '';
    const className = e.parameter.class_name || '';
    const quizId = e.parameter.quiz_id || '';
    const score = parseInt(e.parameter.score) || 0;
    const total = parseInt(e.parameter.total) || 0;
    const duration = parseInt(e.parameter.duration) || 0;
    
    // Thông tin bổ sung
    const studentId = e.parameter.student_id || '';
    const answerJSON = e.parameter.answer_json || '';
    const yccdList = e.parameter.yccd_list || '';
    const conceptList = e.parameter.concept_list || '';
    const device = e.parameter.device || 'Web';
    const version = e.parameter.version || '1.0';
    
    // Kiểm tra dữ liệu bắt buộc
    if (!studentName || !className || !quizId) {
      return ContentService.createTextOutput(
        JSON.stringify({
          success: false,
          message: 'Thiếu thông tin bắt buộc: student_name, class_name, quiz_id'
        })
      ).setMimeType(ContentService.MimeType.JSON);
    }
    
    // Tính toán
    const timestamp = new Date();
    const percentage = total > 0 ? ((score / total) * 100).toFixed(2) : '0.00';
    const passFail = parseFloat(percentage) >= 50 ? 'Pass' : 'Fail';
    const grade = className.split('/')[0] || '';
    
    // ⚠️ QUAN TRỌNG: Thay 'results' bằng TÊN SHEET ĐÚNG
    const sheetName = 'results'; // ← SỬA TÊN NÀY
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
    
    if (!sheet) {
      // Log để debug
      Logger.log('Available sheets: ' + SpreadsheetApp.getActiveSpreadsheet().getSheets().map(s => s.getName()).join(', '));
      
      throw new Error('Không tìm thấy sheet "' + sheetName + '". Các sheet có sẵn: ' + 
        SpreadsheetApp.getActiveSpreadsheet().getSheets().map(s => s.getName()).join(', '));
    }
    
    // Tạo dòng dữ liệu mới
    const newRow = [
      timestamp,
      quizId,
      grade,
      className,
      studentName,
      studentId || '',
      score,
      total,
      percentage + '%',
      answerJSON,
      yccdList,
      conceptList,
      passFail,
      device,
      version
    ];
    
    // Thêm dòng mới
    sheet.appendRow(newRow);
    
    // Format timestamp
    const lastRow = sheet.getLastRow();
    sheet.getRange(lastRow, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss');
    
    // Log để debug
    Logger.log('Đã lưu kết quả: ' + studentName + ' - ' + quizId + ' - ' + score + '/' + total);
    
    // Trả về kết quả thành công
    return ContentService.createTextOutput(
      JSON.stringify({
        success: true,
        message: 'Đã lưu kết quả thành công',
        data: {
          timestamp: timestamp.toISOString(),
          student: studentName,
          class: className,
          quiz: quizId,
          score: score + '/' + total,
          percentage: percentage + '%',
          passFail: passFail
        }
      })
    ).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    Logger.log('Error: ' + error.toString());
    Logger.log('Stack: ' + error.stack);
    
    return ContentService.createTextOutput(
      JSON.stringify({
        success: false,
        message: 'Lỗi: ' + error.toString()
      })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}
```

### **Code Cho Standalone Script:**

```javascript
function doGet(e) {
  try {
    // ... (giữ nguyên phần lấy parameters) ...
    
    // ⚠️ THAY ĐỔI: Dùng Spreadsheet ID hoặc Name
    const SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID_HERE'; // ← ĐIỀN ID VÀO ĐÂY
    const sheetName = 'results'; // ← TÊN SHEET
    
    const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    const sheet = spreadsheet.getSheetByName(sheetName);
    
    if (!sheet) {
      throw new Error('Không tìm thấy sheet "' + sheetName + '"');
    }
    
    // ... (phần còn lại giữ nguyên) ...
  } catch (error) {
    // ...
  }
}
```

---

## 🔍 CÁCH TÌM SPREADSHEET ID

1. Mở Google Sheet `result_thcs`
2. Xem URL:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit
   ```
3. Copy phần `SPREADSHEET_ID_HERE`

---

## ✅ CHECKLIST SỬA LỖI

- [ ] Đã kiểm tra tên sheet trong Google Sheet
- [ ] Đã sửa tên sheet trong code cho đúng (phân biệt chữ hoa/thường)
- [ ] Đã sửa cả hàm `doGet()` và `testScript()` cho nhất quán
- [ ] Đã kiểm tra script có bound với Google Sheet không
- [ ] Nếu standalone, đã thêm Spreadsheet ID/Name
- [ ] Đã tạo header trong Google Sheet (nếu chưa có)
- [ ] Đã test bằng hàm `testScript()`
- [ ] Đã xem logs trong Google Apps Script
- [ ] Đã test endpoint từ browser

---

## 🧪 TEST SCRIPT

1. Mở Google Apps Script Editor
2. Chạy hàm `testScript()`:
   - Click vào dropdown "Select function" → chọn `testScript`
   - Click "Run" (▶️)
3. Xem logs:
   - View → Logs
   - Xem có lỗi gì không
4. Kiểm tra Google Sheet:
   - Mở file `result_thcs`
   - Xem có dòng mới được thêm vào không

---

## 🆘 VẪN KHÔNG ĐƯỢC?

1. **Kiểm tra Execution Logs:**
   - Vào "Executions" trong Google Apps Script
   - Xem có lỗi gì không

2. **Kiểm tra Quyền:**
   - Script cần quyền "Editor" trên Google Sheet
   - Vào File → Share → Kiểm tra

3. **Test Thủ Công:**
   - Chạy hàm `testScript()` trong editor
   - Xem logs để biết lỗi cụ thể

4. **Kiểm Tra Tên Sheet:**
   - Log tất cả tên sheet có sẵn để so sánh
   - Đảm bảo tên chính xác 100%

