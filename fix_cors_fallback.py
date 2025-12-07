"""
Script để sửa hàm sendResult với fallback khi gặp lỗi CORS
- Thử fetch với CORS trước
- Nếu thất bại, fallback về no-cors mode
"""

import os
import re
from pathlib import Path

web_dir = Path("Web")

# Hàm sendResult mới với CORS fallback
new_send_result = """async function sendResult(name,className,quizId,score,total,duration){
      try{
        const url=`${ENDPOINT}?student_name=${encodeURIComponent(name)}&class_name=${encodeURIComponent(className)}&quiz_id=${quizId}&score=${score}&total=${total}&duration=${duration}`;
        console.log('📤 Đang gửi kết quả...');
        console.log('📋 Dữ liệu:', {name, className, quizId, score, total, duration});
        console.log('🔗 URL:', url);
        
        // Thử fetch với CORS trước
        try {
          const response = await fetch(url);
          console.log('📥 Response status:', response.status);
          console.log('📥 Response ok:', response.ok);
          
          const responseText = await response.text();
          console.log('📄 Response text:', responseText);
          
          try {
            const result = JSON.parse(responseText);
            console.log('✅ JSON response:', result);
            
            if (result.success) {
              document.getElementById('send-status').textContent='✅ Đã lưu!';
              console.log('✅ Kết quả đã được lưu thành công vào Google Sheet');
              return;
            } else {
              throw new Error(result.message || 'Lỗi từ server: ' + JSON.stringify(result));
            }
          } catch (parseError) {
            console.error('❌ Lỗi parse JSON:', parseError);
            console.log('⚠️ Response không phải JSON');
            
            if (response.ok) {
              document.getElementById('send-status').textContent='✅ Đã lưu! (đang chờ xác nhận)';
              console.log('⚠️ Không thể xác nhận nhưng status OK');
              return;
            } else {
              throw new Error('Response không OK: ' + response.status);
            }
          }
        } catch (corsError) {
          // Nếu gặp lỗi CORS, thử lại với no-cors mode
          console.warn('⚠️ Lỗi CORS, thử lại với no-cors mode:', corsError.message);
          
          try {
            await fetch(url, {mode: 'no-cors'});
            document.getElementById('send-status').textContent='✅ Đã gửi (kiểm tra Google Sheet)';
            console.log('📤 Đã gửi request với no-cors mode. Kiểm tra Google Sheet để xác nhận.');
            
            // Mở một tab ẩn để kiểm tra URL
            const checkUrl = url + '&_check=1';
            setTimeout(() => {
              const hiddenFrame = document.createElement('iframe');
              hiddenFrame.style.display = 'none';
              hiddenFrame.src = checkUrl;
              document.body.appendChild(hiddenFrame);
              setTimeout(() => document.body.removeChild(hiddenFrame), 2000);
            }, 500);
          } catch (noCorsError) {
            throw new Error('Lỗi khi gửi request: ' + noCorsError.message);
          }
        }
      }catch(e){
        console.error('❌ Lỗi khi gửi kết quả:', e);
        console.error('❌ Stack trace:', e.stack);
        document.getElementById('send-status').textContent='⚠️ Không lưu được: ' + e.message;
      }
    }"""

def fix_file(file_path):
    """Sửa một file HTML"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Kiểm tra xem có hàm sendResult không
        if 'async function sendResult' not in content:
            return False
        
        # Tìm vị trí bắt đầu và kết thúc hàm sendResult
        start_pattern = r'async function sendResult\([^)]+\)\s*\{'
        start_match = re.search(start_pattern, content)
        
        if not start_match:
            return False
        
        start_pos = start_match.start()
        
        # Tìm vị trí kết thúc hàm (dấu } cuối cùng)
        brace_count = 0
        in_function = False
        end_pos = start_pos
        
        for i in range(start_pos, len(content)):
            if content[i] == '{':
                brace_count += 1
                in_function = True
            elif content[i] == '}':
                brace_count -= 1
                if in_function and brace_count == 0:
                    end_pos = i + 1
                    break
        
        if end_pos <= start_pos:
            return False
        
        # Thay thế hàm
        content = content[:start_pos] + new_send_result + content[end_pos:]
        
        # Lưu file
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Lỗi khi sửa {file_path.name}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Chạy script"""
    if not web_dir.exists():
        print(f"❌ Không tìm thấy thư mục {web_dir}")
        return
    
    html_files = list(web_dir.glob("*.html"))
    print(f"📁 Tìm thấy {len(html_files)} file HTML")
    print()
    
    fixed_count = 0
    for html_file in html_files:
        if fix_file(html_file):
            fixed_count += 1
            print(f"✅ Đã sửa: {html_file.name}")
    
    print()
    print(f"✅ Hoàn thành! Đã sửa {fixed_count}/{len(html_files)} file")

if __name__ == "__main__":
    main()

