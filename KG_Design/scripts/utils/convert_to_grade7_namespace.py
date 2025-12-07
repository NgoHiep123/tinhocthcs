#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script chuyển đổi namespace của Khối 6 sang namespace của Khối 7
Để có thể dùng chung schema kg_schema_grade7.ttl

Chuyển đổi:
- https://example.org/edu# → http://education.vn/ontology#
- https://example.org/kg/ → http://education.vn/data/
"""

import sys
from pathlib import Path
import io

# Fix encoding cho Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Đường dẫn
SCRIPT_DIR = Path(__file__).parent
OUT_DIR = SCRIPT_DIR / "out"
OUT_CONVERTED_DIR = SCRIPT_DIR / "out_converted"

# Namespace mapping
NAMESPACE_MAP = {
    'https://example.org/edu#': 'http://education.vn/ontology#',
    'https://example.org/kg/': 'http://education.vn/data/',
}

def convert_namespace(content: str) -> str:
    """Chuyển đổi namespace trong nội dung TTL"""
    result = content
    
    # Chuyển đổi prefix declarations
    result = result.replace('@prefix edu: <https://example.org/edu#>', 
                           '@prefix edu: <http://education.vn/ontology#>')
    result = result.replace('@prefix ex:  <https://example.org/kg/>', 
                           '@prefix data: <http://education.vn/data/>')
    
    # Chuyển đổi full URIs
    result = result.replace('https://example.org/edu#', 
                           'http://education.vn/ontology#')
    result = result.replace('https://example.org/kg/', 
                           'http://education.vn/data/')
    
    # Chuyển đổi prefix usage (ex: → data:)
    # Chỉ thay thế khi đứng trước dấu : hoặc /
    import re
    # Thay thế <https://example.org/kg/...> thành <http://education.vn/data/...>
    result = re.sub(r'<https://example\.org/kg/([^>]+)>', 
                   r'<http://education.vn/data/\1>', result)
    
    # Thay thế ex: thành data: trong các triple
    result = re.sub(r'\bex:([a-zA-Z_][a-zA-Z0-9_]*)', r'data:\1', result)
    
    return result

def convert_file(input_file: Path, output_file: Path):
    """Chuyển đổi một file TTL"""
    print(f"📄 Đang chuyển đổi: {input_file.name}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        converted_content = convert_namespace(content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(converted_content)
        
        print(f"   ✅ Đã tạo: {output_file.name}")
        return True
        
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
        return False

def main():
    """Hàm chính"""
    print("=" * 70)
    print("🔄 CHUYỂN ĐỔI NAMESPACE KHỐI 6 SANG NAMESPACE KHỐI 7")
    print("=" * 70)
    print("\n📋 Mapping:")
    print(f"   {NAMESPACE_MAP['https://example.org/edu#']}")
    print(f"   {NAMESPACE_MAP['https://example.org/kg/']}")
    print()
    
    # Tạo thư mục output
    OUT_CONVERTED_DIR.mkdir(parents=True, exist_ok=True)
    
    # Danh sách file cần chuyển đổi
    ttl_files = [
        'skills.ttl',
        'resources.ttl',
        'resource_skill.ttl',
        'prerequisites.ttl',
        'question_skill.ttl',
        'students.ttl',
        'mastery.ttl',
        'teachers_assignments.ttl',
    ]
    
    success_count = 0
    failed_count = 0
    
    for filename in ttl_files:
        input_file = OUT_DIR / filename
        output_file = OUT_CONVERTED_DIR / filename
        
        if not input_file.exists():
            print(f"⚠️  Bỏ qua: {filename} (không tồn tại)")
            continue
        
        if convert_file(input_file, output_file):
            success_count += 1
        else:
            failed_count += 1
    
    print("\n" + "=" * 70)
    print("📊 KẾT QUẢ")
    print("=" * 70)
    print(f"✅ Thành công: {success_count} file")
    if failed_count > 0:
        print(f"❌ Thất bại: {failed_count} file")
    
    print(f"\n📁 File đã chuyển đổi nằm ở: {OUT_CONVERTED_DIR}")
    print("\n💡 Bước tiếp theo:")
    print("   1. Upload kg_schema_grade7.ttl vào GraphDB (nếu chưa có)")
    print("   2. Upload các file trong thư mục out_converted/")
    print("   3. Upload kg_grade7.ttl (nếu muốn có dữ liệu Khối 7)")

if __name__ == '__main__':
    main()

