#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động sửa lỗi dấu "/" trong URI của các file TTL
Thay thế: data:entity/name → data:entity_name
"""

import os
import re
from pathlib import Path

def fix_slash_in_uri(content):
    """
    Sửa tất cả URI có dấu / thành _
    Ví dụ: data:grade/6 → data:grade_6
    """
    # Pattern: data:entity/name hoặc data:entity/name/subname
    # Thay thế tất cả / thành _
    pattern = r'data:([a-z_]+)/([^;\s\.\)]+)'
    
    def replace_func(match):
        entity = match.group(1)
        name = match.group(2)
        # Thay tất cả / trong name thành _
        name_fixed = name.replace('/', '_')
        return f'data:{entity}_{name_fixed}'
    
    # Thay thế tất cả occurrences
    fixed_content = re.sub(pattern, replace_func, content)
    
    return fixed_content

def process_file(file_path):
    """Xử lý một file TTL"""
    print(f"📄 Đang xử lý: {file_path}")
    
    try:
        # Đọc file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sửa lỗi
        fixed_content = fix_slash_in_uri(content)
        
        # Kiểm tra xem có thay đổi không
        if content != fixed_content:
            # Backup file gốc
            backup_path = str(file_path) + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  💾 Đã backup: {backup_path}")
            
            # Ghi file đã sửa
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"  ✅ Đã sửa: {file_path}")
            return True
        else:
            print(f"  ⏭️  Không có thay đổi: {file_path}")
            return False
            
    except Exception as e:
        print(f"  ❌ Lỗi: {e}")
        return False

def main():
    """Hàm chính"""
    print("=" * 60)
    print("🔧 SỬA LỖI DẤU '/' TRONG URI CỦA FILE TTL")
    print("=" * 60)
    
    # Đường dẫn thư mục TTL
    script_file = Path(__file__).resolve()
    script_dir = script_file.parent
    base_dir = script_dir.parent  # KG_Design
    ttl_dir = base_dir / 'data' / 'grade6' / 'ttl'
    
    print(f"🔍 Script file: {script_file}")
    print(f"🔍 Base dir: {base_dir}")
    print(f"🔍 TTL dir: {ttl_dir}")
    print(f"🔍 TTL dir exists: {ttl_dir.exists()}")
    
    if not ttl_dir.exists():
        print(f"❌ Không tìm thấy thư mục: {ttl_dir}")
        return
    
    # Tìm tất cả file .ttl
    ttl_files = list(ttl_dir.glob('*.ttl'))
    
    if not ttl_files:
        print(f"❌ Không tìm thấy file .ttl trong: {ttl_dir}")
        return
    
    print(f"\n📁 Tìm thấy {len(ttl_files)} file TTL")
    print("-" * 60)
    
    # Xử lý từng file
    fixed_count = 0
    for ttl_file in sorted(ttl_files):
        if process_file(ttl_file):
            fixed_count += 1
        print()
    
    print("=" * 60)
    print(f"✅ HOÀN THÀNH!")
    print(f"   - Tổng file: {len(ttl_files)}")
    print(f"   - Đã sửa: {fixed_count}")
    print(f"   - Không thay đổi: {len(ttl_files) - fixed_count}")
    print("=" * 60)
    
    if fixed_count > 0:
        print("\n💡 Lưu ý:")
        print("   - File backup có đuôi .backup")
        print("   - Có thể xóa file backup sau khi kiểm tra OK")
        print("   - Upload lại các file đã sửa vào GraphDB")

if __name__ == '__main__':
    main()

