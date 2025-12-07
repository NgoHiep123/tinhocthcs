"""
Script để cải thiện hàm sendResult trong tất cả file HTML
- Bỏ mode: 'no-cors' để có thể đọc response
- Thêm logging chi tiết để debug
- Xử lý response đúng cách
"""

import os
import re
from pathlib import Path

web_dir = Path("Web")

# Hàm sendResult mới với logging và xử lý response
new_send_result = """async function sendResult(name,className,quizId,score,total,duration){
      try{
        const url=`${ENDPOINT}?student_name=${encodeURIComponent(name)}&class_name=${encodeURIComponent(className)}&quiz_id=${quizId}&score=${score}&total=${total}&duration=${duration}`;
        console.log('📤 Đang gửi kết quả...');
        console.log('📋 Dữ liệu:', {name, className, quizId, score, total, duration});
        console.log('🔗 URL:', url);
        
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
          } else {
            throw new Error(result.message || 'Lỗi từ server: ' + JSON.stringify(result));
          }
        } catch (parseError) {
          console.error('❌ Lỗi parse JSON:', parseError);
          console.log('⚠️ Response không phải JSON, có thể là redirect hoặc HTML');
          
          // Nếu status OK nhưng không parse được JSON, vẫn coi là thành công
          if (response.ok) {
            document.getElementById('send-status').textContent='✅ Đã lưu! (đang chờ xác nhận)';
            console.log('⚠️ Không thể xác nhận nhưng status OK');
          } else {
            throw new Error('Response không OK: ' + response.status + ' - ' + responseText.substring(0, 100));
          }
        }
      }catch(e){
        console.error('❌ Lỗi khi gửi kết quả:', e);
        console.error('❌ Stack trace:', e.stack);
        document.getElementById('send-status').textContent='⚠️ Không lưu được: ' + e.message;
      }
    }"""

def fix_send_result_in_file(file_path):
    """Sửa hàm sendResult trong một file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Kiểm tra xem file có hàm sendResult với no-cors không
        if 'mode:\'no-cors\'' not in content and 'mode:"no-cors"' not in content:
            return False
        
        # Tìm và thay thế toàn bộ hàm sendResult
        # Pattern: async function sendResult(...){...}
        # Tìm từ async function sendResult đến dấu } cuối cùng của hàm
        
        # Pattern đơn giản: tìm hàm sendResult một dòng
        pattern = r'async function sendResult\([^)]+\)\{[^}]+\}'
        
        def replace_function(match):
            func_text = match.group(0)
            # Nếu có no-cors thì thay thế
            if 'mode:\'no-cors\'' in func_text or 'mode:"no-cors"' in func_text:
                return new_send_result
            return func_text
        
        content = re.sub(pattern, replace_function, content, flags=re.DOTALL)
        
        # Kiểm tra xem có thay đổi không
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Lỗi khi sửa {file_path.name}: {e}")
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
        if fix_send_result_in_file(html_file):
            fixed_count += 1
            print(f"✅ Đã sửa: {html_file.name}")
    
    print()
    print(f"✅ Hoàn thành! Đã sửa {fixed_count}/{len(html_files)} file")
    print()
    print("📝 Bước tiếp theo:")
    print("1. Commit và push lên GitHub")
    print("2. Test lại trên web")
    print("3. Mở Console (F12) để xem logs khi làm bài")

if __name__ == "__main__":
    main()

