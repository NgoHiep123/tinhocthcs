#!/usr/bin/env python3
"""
Script cải thiện hàm sendResult trong các file HTML quiz
Thêm logging và error handling tốt hơn
"""

from pathlib import Path
import re

WEB_DIR = Path("Web")

# Hàm sendResult cũ (pattern để tìm)
OLD_FUNCTION_PATTERN = r'async function sendResult\([^)]+\)\{[^}]*mode:\'no-cors\'[^}]*\}'

# Hàm sendResult mới với logging tốt hơn
NEW_FUNCTION = '''async function sendResult(name,className,quizId,score,total,duration){
  try{
    const url=`${ENDPOINT}?student_name=${encodeURIComponent(name)}&class_name=${encodeURIComponent(className)}&quiz_id=${quizId}&score=${score}&total=${total}&duration=${duration}`;
    
    console.log('📤 Đang gửi kết quả...');
    console.log('📍 URL:', url);
    console.log('📋 Dữ liệu:', {name, className, quizId, score, total, duration});
    
    const response = await fetch(url, {
      method: 'GET',
      mode: 'no-cors',
      cache: 'no-cache'
    });
    
    console.log('✅ Request đã được gửi (no-cors mode)');
    
    // Đợi một chút để đảm bảo request được xử lý
    await new Promise(resolve => setTimeout(resolve, 500));
    
    document.getElementById('send-status').textContent='✅ Đã lưu!';
    
    console.log('💾 Trạng thái: Đã lưu (kiểm tra Google Sheet để xác nhận)');
    
  }catch(e){
    console.error('❌ Lỗi khi lưu:', e);
    document.getElementById('send-status').textContent='⚠️ Không lưu được: ' + e.message;
  }
}'''

def improve_file(filepath):
    """Cải thiện hàm sendResult trong một file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Tìm và thay thế hàm sendResult
        # Pattern linh hoạt để match các biến thể
        pattern = r'async function sendResult\([^)]+\)\{[^}]*mode:\'no-cors\'[^}]*\}'
        
        if re.search(pattern, content, re.DOTALL):
            # Tìm từ "async function sendResult" đến hết function
            lines = content.split('\n')
            new_lines = []
            in_function = False
            brace_count = 0
            function_start = -1
            
            for i, line in enumerate(lines):
                if 'async function sendResult' in line:
                    in_function = True
                    function_start = i
                    new_lines.append(NEW_FUNCTION)
                    continue
                
                if in_function:
                    # Đếm braces để tìm kết thúc function
                    brace_count += line.count('{')
                    brace_count -= line.count('}')
                    
                    if brace_count <= 0 and '{' in line:
                        # Có thể là kết thúc function
                        if line.strip() == '}' or (line.strip().startswith('}') and not line.strip().startswith('})')):
                            in_function = False
                            brace_count = 0
                            continue
                    continue
                
                new_lines.append(line)
            
            if in_function:
                # Nếu vẫn trong function, có thể là format khác - dùng regex
                content = re.sub(pattern, NEW_FUNCTION, content, flags=re.DOTALL)
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
    """Cải thiện tất cả các file HTML trong thư mục Web"""
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
        if improve_file(html_file):
            print(f"✅ Đã cải thiện: {html_file.name}")
            fixed_count += 1
    
    print(f"\n✨ Hoàn thành! Đã cải thiện {fixed_count} file.")

if __name__ == "__main__":
    main()

