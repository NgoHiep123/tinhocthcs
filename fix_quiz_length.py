#!/usr/bin/env python3
"""
Script sửa lỗi hardcode số lượng câu hỏi trong các file quiz
Thay thế hardcode "/10" bằng quiz.length để tự động tính đúng số câu
"""

import re
from pathlib import Path

WEB_DIR = Path("Web")

def fix_file(filepath):
    """Sửa một file HTML"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Sửa 1: "Câu ${currentQ+1}/10" -> "Câu ${currentQ+1}/${quiz.length}"
        content = re.sub(
            r'`Câu \$\{currentQ\+1\}/10`',
            r'`Câu ${currentQ+1}/${quiz.length}`',
            content
        )
        
        # Sửa 2: "((currentQ+1)/10*100)" -> "((currentQ+1)/quiz.length*100)"
        content = re.sub(
            r'\(\(currentQ\+1\)/10\*100\)',
            r'((currentQ+1)/quiz.length*100)',
            content
        )
        
        # Sửa 3: "${score}/10" -> "${score}/${quiz.length}"
        content = re.sub(
            r'\$\{score\}/10',
            r'${score}/${quiz.length}',
            content
        )
        
        # Sửa 4: Text "10 câu hỏi" -> "câu hỏi" (hoặc có thể giữ nguyên nếu muốn)
        # Nhưng tốt hơn là để dynamic, nên có thể bỏ qua hoặc thay bằng quiz.length
        
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
    print("🔧 Đang sửa hardcode số lượng câu hỏi...\n")
    
    fixed_count = 0
    for html_file in sorted(html_files):
        if fix_file(html_file):
            print(f"✅ Đã sửa: {html_file.name}")
            fixed_count += 1
    
    print(f"\n✨ Hoàn thành! Đã sửa {fixed_count} file.")

if __name__ == "__main__":
    main()

