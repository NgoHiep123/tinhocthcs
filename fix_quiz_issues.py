#!/usr/bin/env python3
"""
Script sửa 2 lỗi trong các file HTML quiz:
1. Sửa href="index.html" thành href="/index.html" (đường dẫn tuyệt đối)
2. Sửa selector #quiz-container thành .quiz-container (vì chỉ có class, không có id)
"""

import os
from pathlib import Path

WEB_DIR = Path("Web")

def fix_file(filepath):
    """Sửa một file HTML"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Sửa 1: href="index.html" -> href="/index.html"
        content = content.replace('href="index.html"', 'href="/index.html"')
        
        # Sửa 2: #quiz-container -> .quiz-container (vì chỉ có class, không có id)
        # Nhưng cần cẩn thận, có thể có trường hợp khác
        # Kiểm tra xem có dòng nào dùng #quiz-container không
        if '#quiz-container' in content:
            # Thay thế selector trong querySelector
            content = content.replace("document.querySelector('#quiz-container>div:first-child')", 
                                    "document.querySelector('.quiz-container>div:first-child')")
            # Hoặc có thể cần thêm id vào div, nhưng tốt hơn là dùng class selector
        
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
    print("🔧 Đang sửa các lỗi...\n")
    
    fixed_count = 0
    for html_file in sorted(html_files):
        if fix_file(html_file):
            print(f"✅ Đã sửa: {html_file.name}")
            fixed_count += 1
    
    print(f"\n✨ Hoàn thành! Đã sửa {fixed_count} file.")

if __name__ == "__main__":
    main()

