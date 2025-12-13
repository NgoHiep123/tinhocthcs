#!/usr/bin/env python3
"""
Script tạo các file redirect HTML ở thư mục gốc
để chuyển hướng từ URL cũ (K6_A1.html) đến URL mới (Web/K6_A1.html)
"""

import os
from pathlib import Path

# Thư mục chứa các file HTML
WEB_DIR = Path("Web")

# Template cho file redirect HTML
REDIRECT_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url={target_url}">
  <script>
    // Fallback nếu meta refresh không hoạt động
    window.location.replace("{target_url}");
  </script>
  <title>Đang chuyển hướng...</title>
</head>
<body>
  <p>Đang chuyển hướng... Nếu không tự động chuyển, <a href="{target_url}">click vào đây</a>.</p>
</body>
</html>
"""

def create_redirect_file(filename):
    """Tạo file redirect cho một file HTML"""
    target_url = f"/Web/{filename}"  # Sử dụng đường dẫn tuyệt đối
    redirect_content = REDIRECT_TEMPLATE.format(target_url=target_url)
    
    # Ghi file redirect ở thư mục gốc
    redirect_path = Path(filename)
    redirect_path.write_text(redirect_content, encoding='utf-8')
    print(f"✅ Đã tạo: {filename} -> {target_url}")

def main():
    """Tạo tất cả các file redirect"""
    if not WEB_DIR.exists():
        print(f"❌ Không tìm thấy thư mục {WEB_DIR}")
        return
    
    # Lấy danh sách tất cả file HTML trong thư mục Web
    html_files = list(WEB_DIR.glob("*.html"))
    
    if not html_files:
        print(f"❌ Không tìm thấy file HTML nào trong {WEB_DIR}")
        return
    
    print(f"📝 Tìm thấy {len(html_files)} file HTML")
    print("🔄 Đang tạo các file redirect...\n")
    
    # Tạo redirect cho mỗi file
    for html_file in sorted(html_files):
        filename = html_file.name
        create_redirect_file(filename)
    
    print(f"\n✨ Hoàn thành! Đã tạo {len(html_files)} file redirect.")

if __name__ == "__main__":
    main()


