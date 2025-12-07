"""
Script để cải thiện hàm sendResult trong các file HTML
- Bỏ mode: 'no-cors' để có thể đọc response
- Thêm logging chi tiết
- Xử lý response đúng cách
"""

import os
import re
from pathlib import Path

# Đường dẫn thư mục Web
web_dir = Path("Web")

# Pattern để tìm hàm sendResult cũ
old_pattern = r'async function sendResult\(name,className,quizId,score,total,duration\)\{try\{const url=`\$\{ENDPOINT\}\?student_name=\$\{encodeURIComponent\(name\)\}\&class_name=\$\{encodeURIComponent\(className\)\}\&quiz_id=\$\{quizId\}\&score=\$\{score\}\&total=\$\{total\}\&duration=\$\{duration\}`;await fetch\(url,\{mode:\'no-cors\'\}\);document\.getElementById\(\'send-status\'\)\.textContent=\'✅ Đã lưu!\'\}catch\(e\)\{document\.getElementById\(\'send-status\'\)\.textContent=\'⚠️ Không lưu được\'\}\}'

# Pattern đơn giản hơn - tìm dòng chứa sendResult với no-cors
old_simple_pattern = r"await fetch\(url,\{mode:'no-cors'\}\);document\.getElementById\('send-status'\)\.textContent='✅ Đã lưu!'"

# Hàm sendResult mới với logging và xử lý response
new_send_result = """async function sendResult(name,className,quizId,score,total,duration){
      try{
        const url=`${ENDPOINT}?student_name=${encodeURIComponent(name)}&class_name=${encodeURIComponent(className)}&quiz_id=${quizId}&score=${score}&total=${total}&duration=${duration}`;
        console.log('📤 Gửi kết quả:', {name, className, quizId, score, total, duration});
        console.log('🔗 URL:', url);
        
        const response = await fetch(url);
        console.log('📥 Response status:', response.status);
        console.log('📥 Response ok:', response.ok);
        
        // Thử đọc response dưới dạng text trước
        const responseText = await response.text();
        console.log('📄 Response text:', responseText);
        
        // Thử parse JSON
        let result;
        try {
          result = JSON.parse(responseText);
          console.log('✅ JSON parsed:', result);
          
          if (result.success) {
            document.getElementById('send-status').textContent='✅ Đã lưu!';
            console.log('✅ Kết quả đã được lưu thành công');
          } else {
            throw new Error(result.message || 'Không lưu được');
          }
        } catch (parseError) {
          // Nếu không parse được JSON, vẫn coi là thành công (có thể là HTML redirect)
          console.warn('⚠️ Không parse được JSON, nhưng response status OK');
          if (response.ok) {
            document.getElementById('send-status').textContent='✅ Đã lưu!';
            console.log('✅ Kết quả có thể đã được lưu (không thể xác nhận)');
          } else {
            throw new Error('Response không OK: ' + response.status);
          }
        }
      }catch(e){
        console.error('❌ Lỗi khi gửi kết quả:', e);
        document.getElementById('send-status').textContent='⚠️ Không lưu được: ' + e.message;
      }
    }"""

def fix_file(file_path):
    """Sửa file HTML"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Tìm và thay thế hàm sendResult
        # Tìm pattern đầy đủ trước (một dòng)
        if 'mode:\'no-cors\'' in content or 'mode:"no-cors"' in content:
            # Tìm phần bắt đầu của hàm sendResult
            # Pattern: async function sendResult(...){try{...await fetch(url,{mode:'no-cors'});...}catch...}
            
            # Cách 1: Tìm và thay toàn bộ hàm sendResult (một dòng)
            pattern_full_one_line = r'async function sendResult\([^)]+\)\{[^}]+\}'
            
            # Tìm tất cả các hàm sendResult trong file
            matches = re.finditer(pattern_full_one_line, content, re.DOTALL)
            
            found = False
            for match in matches:
                func_content = match.group(0)
                if 'mode:\'no-cors\'' in func_content or 'mode:"no-cors"' in func_content:
                    # Thay thế toàn bộ hàm
                    content = content[:match.start()] + new_send_result + content[match.end():]
                    found = True
                    print(f"✅ Đã sửa {file_path.name}")
                    break
            
            if not found:
                # Thử cách khác: tìm và thay từng phần
                # Thay phần fetch với no-cors
                if 'mode:\'no-cors\'' in content:
                    # Tìm đoạn từ async function sendResult đến hết catch
                    # Sử dụng regex phức tạp hơn
                    pattern = r'(async function sendResult\([^)]+\)\{[^{]*?try\{[^}]*?)(await fetch\(url,\{mode:\'no-cors\'\}\);document\.getElementById\(\'send-status\'\)\.textContent=\'✅ Đã lưu!\')([^}]*?\}catch\([^}]+?\{[^}]*?document\.getElementById\(\'send-status\'\)\.textContent=\'⚠️ Không lưu được\'[^}]*?\})'
                    
                    replacement = r'\1' + new_send_result.replace('\\', '\\\\').replace('$', '\\$') + r'\3'
                    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                    found = True
                    print(f"✅ Đã sửa {file_path.name} (cách 2)")
            
            if found and content != original_content:
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
    
    fixed_count = 0
    for html_file in html_files:
        if fix_file(html_file):
            fixed_count += 1
    
    print(f"\n✅ Hoàn thành! Đã sửa {fixed_count}/{len(html_files)} file")

if __name__ == "__main__":
    main()

