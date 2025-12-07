/**
 * GOOGLE APPS SCRIPT - ĐÃ SỬA LỖI
 * 
 * ⚠️ QUAN TRỌNG: Trước khi sử dụng, cần sửa:
 * 1. Tên sheet (dòng có sheetName)
 * 2. Nếu script standalone, thêm Spreadsheet ID
 */

function doGet(e) {
  try {
    // Kiểm tra e có tồn tại không (tránh lỗi khi test trực tiếp)
    if (!e || !e.parameter) {
      return ContentService.createTextOutput(
        JSON.stringify({
          success: false,
          message: 'Không có dữ liệu. Hàm này chỉ chạy khi được gọi từ URL.'
        })
      ).setMimeType(ContentService.MimeType.JSON);
    }
    
    // Lấy tham số từ URL
    const studentName = e.parameter.student_name || '';
    const className = e.parameter.class_name || '';
    const quizId = e.parameter.quiz_id || '';
    const score = parseInt(e.parameter.score) || 0;
    const total = parseInt(e.parameter.total) || 0;
    const duration = parseInt(e.parameter.duration) || 0;
    
    // Thông tin bổ sung (nếu có)
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
    
    // Tính toán các giá trị
    const timestamp = new Date();
    const percentage = total > 0 ? ((score / total) * 100).toFixed(2) : '0.00';
    const passFail = parseFloat(percentage) >= 50 ? 'Pass' : 'Fail';
    const grade = className.split('/')[0] || '';
    
    // ============================================================================
    // ⚠️ QUAN TRỌNG: SỬA TÊN SHEET Ở ĐÂY
    // ============================================================================
    // Nếu script BOUND với Google Sheet (script được tạo từ trong Sheet):
    const sheetName = 'results'; // ← SỬA TÊN NÀY thành tên sheet thực tế
    
    // Nếu script STANDALONE (script được tạo từ script.google.com):
    // Bỏ comment và điền Spreadsheet ID:
    // const SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID_HERE';
    // const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    // const sheet = spreadsheet.getSheetByName(sheetName);
    
    // Script BOUND (mặc định):
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
    
    if (!sheet) {
      // Log tất cả tên sheet có sẵn để debug
      const allSheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();
      const sheetNames = allSheets.map(s => s.getName()).join(', ');
      Logger.log('Không tìm thấy sheet "' + sheetName + '"');
      Logger.log('Các sheet có sẵn: ' + sheetNames);
      
      throw new Error('Không tìm thấy sheet "' + sheetName + '". Các sheet có sẵn: ' + sheetNames);
    }
    
    // Tạo dòng dữ liệu mới
    const newRow = [
      timestamp,           // Timestamp (cột A)
      quizId,              // QuizID (cột B)
      grade,               // Grade (cột C)
      className,           // Class (cột D)
      studentName,         // StudentName (cột E)
      studentId || '',     // StudentID (cột F)
      score,               // Score (cột G)
      total,               // Total (cột H)
      percentage + '%',    // Percent (cột I)
      answerJSON,          // AnswerJSON (cột J)
      yccdList,            // YCCD_List (cột K)
      conceptList,         // Concept_List (cột L)
      passFail,            // Pass/Fail (cột M)
      device,              // Device (cột N)
      version              // Version (cột O)
    ];
    
    // Thêm dòng mới vào sheet
    sheet.appendRow(newRow);
    
    // Format các cột
    const lastRow = sheet.getLastRow();
    sheet.getRange(lastRow, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss');
    
    // Log để debug
    Logger.log('✅ Đã lưu kết quả thành công:');
    Logger.log('   - Học sinh: ' + studentName);
    Logger.log('   - Lớp: ' + className);
    Logger.log('   - Bài: ' + quizId);
    Logger.log('   - Điểm: ' + score + '/' + total + ' (' + percentage + '%)');
    Logger.log('   - Dòng: ' + lastRow);
    
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
    // Log lỗi chi tiết
    Logger.log('❌ Lỗi: ' + error.toString());
    Logger.log('Stack: ' + error.stack);
    
    return ContentService.createTextOutput(
      JSON.stringify({
        success: false,
        message: 'Lỗi: ' + error.toString()
      })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

// =============================================================================
// HÀM TEST (chạy để kiểm tra script)
// =============================================================================

function testScript() {
  const testParams = {
    parameter: {
      student_name: 'Nguyễn Văn A',
      class_name: '6/14',
      quiz_id: 'K6_A1',
      score: '8',
      total: '10',
      duration: '450',
      student_id: '2324_0001'
    }
  };
  
  Logger.log('🧪 Bắt đầu test script...');
  
  const result = doGet(testParams);
  const resultText = result.getContent();
  
  Logger.log('📝 Kết quả:');
  Logger.log(resultText);
  
  // Kiểm tra trong Google Sheets
  const sheetName = 'results'; // ← Đảm bảo tên giống với hàm doGet()
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  
  if (sheet) {
    const lastRow = sheet.getLastRow();
    Logger.log('📊 Dòng mới nhất trong sheet: ' + lastRow);
    
    if (lastRow > 1) {
      // Lấy dữ liệu dòng cuối cùng
      const lastRowData = sheet.getRange(lastRow, 1, 1, 15).getValues()[0];
      Logger.log('📋 Dữ liệu dòng cuối: ' + JSON.stringify(lastRowData));
    }
  } else {
    Logger.log('⚠️ Không tìm thấy sheet "' + sheetName + '"');
  }
}

// =============================================================================
// HÀM XEM TẤT CẢ TÊN SHEET (để debug)
// =============================================================================

function listAllSheets() {
  const sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();
  Logger.log('📋 Danh sách tất cả sheet:');
  sheets.forEach(function(sheet, index) {
    Logger.log('   ' + (index + 1) + '. "' + sheet.getName() + '"');
  });
  return sheets.map(s => s.getName());
}

// =============================================================================
// HÀM XÓA DỮ LIỆU TEST (tùy chọn - cẩn thận!)
// =============================================================================

function clearTestData() {
  const sheetName = 'results'; // ← Sửa tên sheet
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  
  if (sheet) {
    const lastRow = sheet.getLastRow();
    if (lastRow > 1) {
      const confirm = Browser.msgBox(
        'Xác nhận',
        'Bạn có chắc muốn xóa tất cả dữ liệu? (Giữ lại header)',
        Browser.Buttons.YES_NO
      );
      if (confirm === 'yes') {
        sheet.deleteRows(2, lastRow - 1);
        Logger.log('✅ Đã xóa dữ liệu test');
      }
    } else {
      Logger.log('ℹ️ Không có dữ liệu để xóa');
    }
  } else {
    Logger.log('❌ Không tìm thấy sheet "' + sheetName + '"');
  }
}

