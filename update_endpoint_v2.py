#!/usr/bin/env python3
"""
Script cập nhật endpoint Google Apps Script mới vào tất cả các file quiz
"""

from pathlib import Path

WEB_DIR = Path("Web")

# Endpoint cũ
OLD_ENDPOINT = "https://script.google.com/a/macros/asianintlschool.edu.vn/s/AKfycbytwRuA512UKakrHpIoURxfAn8-h6XB8e2Gs-cah4gxZHC7-iJOJrl-Qeg_5O-XAfrNjA/exec"

# Endpoint mới
NEW_ENDPOINT = "https://script.google.com/a/macros/asianintlschool.edu.vn/s/AKfycbxoj7jkOooCg_2ciiNIgbBjsLc2MIcGUgnIm_I43eYjPGiUOKwnloqUBCXWZOlOspWxLA/exec"

def update_file(filepath):
    """Cập nhật endpoint trong một file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if OLD_ENDPOINT in content:
            content = content.replace(OLD_ENDPOINT, NEW_ENDPOINT)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"❌ Lỗi khi xử lý {filepath}: {e}")
        return False

def main():
    """Cập nhật tất cả các file HTML trong thư mục Web"""
    if not WEB_DIR.exists():
        print(f"❌ Không tìm thấy thư mục {WEB_DIR}")
        return
    
    html_files = list(WEB_DIR.glob("*.html"))
    
    if not html_files:
        print(f"❌ Không tìm thấy file HTML nào trong {WEB_DIR}")
        return
    
    print(f"📝 Tìm thấy {len(html_files)} file HTML")
    print("🔄 Đang cập nhật endpoint mới...\n")
    print(f"   Cũ: {OLD_ENDPOINT[:60]}...")
    print(f"   Mới: {NEW_ENDPOINT[:60]}...\n")
    
    updated_count = 0
    for html_file in sorted(html_files):
        if update_file(html_file):
            print(f"✅ Đã cập nhật: {html_file.name}")
            updated_count += 1
    
    print(f"\n✨ Hoàn thành! Đã cập nhật {updated_count} file.")

if __name__ == "__main__":
    main()

