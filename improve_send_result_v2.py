"""
Script để cải thiện hàm sendResult trong tất cả file HTML
Thay thế hàm sendResult cũ bằng hàm mới có logging chi tiết
"""

import os
import re
from pathlib import Path

web_dir = Path("Web")

# Hàm sendResult mới
new_function = """async function sendResult(name,className,quizId,score,total,duration){
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

def fix_file(file_path):
    """Sửa một file HTML"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Kiểm tra xem có dùng no-cors không
        if 'mode:\'no-cors\'' not in content and 'mode:"no-cors"' not in content:
            return False
        
        # Tìm toàn bộ hàm sendResult - có thể là một dòng hoặc nhiều dòng
        # Pattern: async function sendResult(...) { ... }
        # Tìm từ "async function sendResult" đến dấu } cuối cùng của hàm
        
        # Thử cách 1: Tìm hàm một dòng
        pattern_one_line = r'async function sendResult\([^)]+\)\{[^}]+\}'
        
        # Thử cách 2: Tìm hàm nhiều dòng (từ async đến } cuối cùng)
        # Sử dụng non-greedy để tìm } đầu tiên sau khi match được cặp {}
        pattern_multi_line = r'async function sendResult\([^)]+\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        
        # Cách đơn giản nhất: Tìm từ "async function sendResult" đến khi gặp "}" sau "catch"
        # Nhưng với regex, khó match chính xác nested {}
        # Tốt nhất là tìm và thay thế đoạn có chứa "mode:'no-cors'"
        
        # Tìm đoạn: async function sendResult( ... ){ ... mode:'no-cors' ... }
        # Thay toàn bộ hàm
        
        # Cách tốt nhất: Tìm vị trí bắt đầu và kết thúc hàm sendResult
        start_pattern = r'async function sendResult\([^)]+\)\s*\{'
        end_positions = []
        
        # Tìm vị trí bắt đầu
        start_match = re.search(start_pattern, content)
        if not start_match:
            return False
        
        start_pos = start_match.start()
        
        # Tìm vị trí kết thúc - tìm dấu } cuối cùng của hàm
        # Đếm số { và } từ vị trí start
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
        
        # Lấy nội dung hàm cũ
        old_function = content[start_pos:end_pos]
        
        # Kiểm tra xem có no-cors không
        if 'mode:\'no-cors\'' in old_function or 'mode:"no-cors"' in old_function:
            # Thay thế
            content = content[:start_pos] + new_function + content[end_pos:]
            
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

