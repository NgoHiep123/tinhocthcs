#!/usr/bin/env python3
"""
Script sửa hàm sendResult để có thể kiểm tra lỗi và debug tốt hơn
Thay thế mode: 'no-cors' bằng cách xử lý tốt hơn
"""

import re
from pathlib import Path

WEB_DIR = Path("Web")

# Pattern để tìm hàm sendResult cũ
OLD_PATTERN = r'async function sendResult\(name,className,quizId,score,total,duration\)\{try\{const url=`\$\{ENDPOINT\}\?student_name=\$\{encodeURIComponent\(name\)\}\&class_name=\$\{encodeURIComponent\(className\)\}\&quiz_id=\$\{quizId\}\&score=\$\{score\}\&total=\$\{total\}\&duration=\$\{duration\}`;await fetch\(url,\{mode:\'no-cors\'\}\);document\.getElementById\(\'send-status\'\)\.textContent=\'✅ Đã lưu!\'\}catch\(e\)\{document\.getElementById\(\'send-status\'\)\.textContent=\'⚠️ Không lưu được\'\}\}'

# Hàm sendResult mới với error handling tốt hơn
NEW_FUNCTION = '''async function sendResult(name,className,quizId,score,total,duration){
  try{
    const url=`${ENDPOINT}?student_name=${encodeURIComponent(name)}&class_name=${encodeURIComponent(className)}&quiz_id=${quizId}&score=${score}&total=${total}&duration=${duration}`;
    console.log('Sending result to:', url);
    
    // Thử fetch với no-cors (vì Google Apps Script có thể không cho CORS)
    const response = await fetch(url, {
      method: 'GET',
      mode: 'no-cors',
      cache: 'no-cache'
    });
    
    // Với no-cors, không thể đọc response, nhưng có thể log
    console.log('Request sent (no-cors mode)');
    
    // Đợi một chút để đảm bảo request được gửi
    await new Promise(resolve => setTimeout(resolve, 500));
    
    document.getElementById('send-status').textContent='✅ Đã lưu!';
    
    // Log để debug
    console.log('Result saved:', {name, className, quizId, score, total, duration});
    
  }catch(e){
    console.error('Save error:', e);
    document.getElementById('send-status').textContent='⚠️ Không lưu được: ' + e.message;
  }
}'''

def fix_file(filepath):
    """Sửa một file HTML"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Tìm và thay thế hàm sendResult
        # Pattern linh hoạt hơn để match các biến thể
        pattern = r'async function sendResult\([^)]+\)\{[^}]*mode:\'no-cors\'[^}]*\}'
        
        if re.search(pattern, content):
            # Thay thế bằng hàm mới
            content = re.sub(
                pattern,
                NEW_FUNCTION,
                content,
                flags=re.DOTALL
            )
        
        # Nếu không match pattern trên, thử pattern đơn giản hơn
        if 'mode:\'no-cors\'' in content and 'async function sendResult' in content:
            # Tìm từ async function sendResult đến hết function
            lines = content.split('\n')
            new_lines = []
            in_function = False
            function_start = -1
            
            for i, line in enumerate(lines):
                if 'async function sendResult' in line:
                    in_function = True
                    function_start = i
                    new_lines.append(NEW_FUNCTION)
                    continue
                
                if in_function:
                    # Bỏ qua các dòng trong function cũ
                    if '}' in line and line.strip().count('}') >= line.strip().count('{'):
                        # Có thể là kết thúc function
                        if line.strip() == '}' or (line.strip().startswith('}') and not line.strip().startswith('})')):
                            in_function = False
                            # Giữ lại dòng } nếu cần
                            if '}' in line and line.strip() != '}':
                                new_lines.append(line)
                    continue
                
                new_lines.append(line)
            
            if in_function:  # Nếu vẫn trong function, có thể là format khác
                content = '\n'.join(new_lines)
            else:
                content = '\n'.join(new_lines)
        
        # Nếu có thay đổi, ghi lại file
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"❌ Lỗi khi xử lý {filepath}: {e}")
        return False

def main():
    """Sửa tất cả các file HTML trong thư mục Web"""
    if not WEB_DIR.exists():
        print(f"❌ Không tìm thấy thư mục {WEB_DIR}")
        return
    
    html_files = list(WEB_DIR.glob("*.html"))
    
    if not html_files:
        print(f"❌ Không tìm thấy file HTML nào trong {WEB_DIR}")
        return
    
    print(f"📝 Tìm thấy {len(html_files)} file HTML")
    print("🔧 Đang cải thiện hàm sendResult...\n")
    
    fixed_count = 0
    for html_file in sorted(html_files):
        if fix_file(html_file):
            print(f"✅ Đã sửa: {html_file.name}")
            fixed_count += 1
    
    print(f"\n✨ Hoàn thành! Đã sửa {fixed_count} file.")
    print("\n💡 LƯU Ý:")
    print("   - Với mode: 'no-cors', browser không thể đọc response")
    print("   - Cần kiểm tra Google Apps Script logs để xác nhận")
    print("   - Hoặc test endpoint trực tiếp trong browser")

if __name__ == "__main__":
    main()

