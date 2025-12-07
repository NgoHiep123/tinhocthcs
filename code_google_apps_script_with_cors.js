/**
 * GOOGLE APPS SCRIPT - VỚI CORS HEADERS
 * 
 * ⚠️ QUAN TRỌNG: 
 * 1. Sửa tên sheet (dòng có sheetName)
 * 2. Deploy với "Who has access: Anyone" để tránh CORS issues
 */

function doGet(e) {
  try {
    // Kiểm tra e có tồn tại không
    if (!e || !e.parameter) {
      return createJSONResponse({
        success: false,
        message: 'Không có dữ liệu. Hàm này chỉ chạy khi được gọi từ URL.'
      });
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
      return createJSONResponse({
        success: false,
        message: 'Thiếu thông tin bắt buộc: student_name, class_name, quiz_id'
      });
    }
    
    // Tính toán các giá trị
    const timestamp = new Date();
    const percentage = total > 0 ? ((score / total) * 100).toFixed(2) : '0.00';
    const passFail = parseFloat(percentage) >= 50 ? 'Pass' : 'Fail';
    const grade = className.split('/')[0] || '';
    
    // ============================================================================
    // ⚠️ QUAN TRỌNG: SỬA TÊN SHEET Ở ĐÂY
    // ============================================================================
    const sheetName = 'results'; // ← SỬA TÊN NÀY thành tên sheet thực tế
    
    // Script BOUND (mặc định):
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
    
    if (!sheet) {
      // Log tất cả tên sheet có sẵn để debug
      const allSheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();
      const sheetNames = allSheets.map(s => s.getName()).join(', ');
      Logger.log('Không tìm thấy sheet "' + sheetName + '"');
      Logger.log('Các sheet có sẵn: ' + sheetNames);
      
      return createJSONResponse({
        success: false,
        message: 'Không tìm thấy sheet "' + sheetName + '". Các sheet có sẵn: ' + sheetNames
      });
    }
    
    // Tạo dòng dữ liệu mới
    const newRow = [
      timestamp,              // Timestamp
      studentName,            // StudentName
      className,              // Class
      quizId,                 // QuizID
      score,                  // Score
      total,                  // Total
      percentage + '%',       // Percentage
      passFail,               // PassFail
      duration + 's',         // Duration
      grade,                  // Grade
      studentId,              // StudentID (nếu có)
      answerJSON,             // AnswerJSON (nếu có)
      yccdList,               // YCCDList (nếu có)
      conceptList,            // ConceptList (nếu có)
      device,                 // Device
      version                 // Version
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
    
    // Trả về kết quả thành công với CORS headers
    return createJSONResponse({
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
    });
    
  } catch (error) {
    // Log lỗi chi tiết
    Logger.log('❌ Lỗi: ' + error.toString());
    Logger.log('Stack: ' + error.stack);
    
    return createJSONResponse({
      success: false,
      message: 'Lỗi: ' + error.toString()
    });
  }
}

/**
 * Tạo JSON response với CORS headers
 */
function createJSONResponse(data) {
  const output = ContentService.createTextOutput(JSON.stringify(data));
  output.setMimeType(ContentService.MimeType.JSON);
  
  // Google Apps Script tự động xử lý CORS khi deploy với "Who has access: Anyone"
  // Không cần set headers thủ công
  
  return output;
}

// =============================================================================
// HÀM TEST (chạy để kiểm tra script)
// =============================================================================

function testScript() {
  const testParams = {
    parameter: {
      student_name: 'Test Student',
      class_name: '6/1',
      quiz_id: 'K6_B1',
      score: '8',
      total: '10',
      duration: '120'
    }
  };
  
  Logger.log('🧪 Bắt đầu test...');
  const result = doGet(testParams);
  Logger.log('📄 Kết quả: ' + result.getContent());
  Logger.log('✅ Test hoàn thành!');
}

/**
 * Liệt kê tất cả các sheet trong spreadsheet
 */
function listAllSheets() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheets = spreadsheet.getSheets();
  Logger.log('📋 Danh sách các sheet:');
  sheets.forEach(function(sheet, index) {
    Logger.log('  ' + (index + 1) + '. ' + sheet.getName());
  });
}

/**
 * Xóa dòng test (dòng cuối cùng có tên "Test Student")
 */
function clearTestData() {
  const sheetName = 'results'; // ← SỬA TÊN NÀY
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  
  if (!sheet) {
    Logger.log('❌ Không tìm thấy sheet: ' + sheetName);
    return;
  }
  
  const lastRow = sheet.getLastRow();
  if (lastRow <= 1) {
    Logger.log('⚠️ Sheet trống hoặc chỉ có header');
    return;
  }
  
  const studentName = sheet.getRange(lastRow, 2).getValue();
  if (studentName === 'Test Student') {
    sheet.deleteRow(lastRow);
    Logger.log('✅ Đã xóa dòng test');
  } else {
    Logger.log('⚠️ Dòng cuối không phải "Test Student"');
  }
}

