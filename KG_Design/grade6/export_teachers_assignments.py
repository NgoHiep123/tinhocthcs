#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script export giáo viên và phân công lớp thành file .ttl
File: KG_Design/grade6/export_teachers_assignments.py
"""

import sys
import csv
import os
from pathlib import Path
import io

# Fix encoding cho Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Thêm thư mục gốc vào path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def export_teachers_assignments_ttl(csv_file='teachers_assign.csv', output_file='teachers_assignments.ttl'):
    """
    Export giáo viên và phân công từ CSV sang TTL
    
    Args:
        csv_file: Đường dẫn đến file CSV
        output_file: File TTL output
    """
    
    print("=" * 70)
    print("📤 EXPORT GIÁO VIÊN VÀ PHÂN CÔNG LỚP SANG TTL")
    print("=" * 70)
    
    # Đường dẫn file CSV (ở thư mục gốc)
    csv_path = project_root / csv_file
    output_path = Path(__file__).parent / "out" / output_file
    
    if not csv_path.exists():
        print(f"\n❌ Không tìm thấy file: {csv_path}")
        return False
    
    print(f"\n📁 Input: {csv_path}")
    print(f"📁 Output: {output_path}")
    
    # Tạo thư mục out nếu chưa có
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Đọc CSV và tạo TTL
    teachers_set = set()
    assignments = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                teacher_id = row['Id_teacher'].strip()
                teacher_name = row['name'].strip()
                expertise = row.get('expertise', 'Tin học').strip()
                class_name = row['class'].strip()
                
                # Lưu teacher info (chỉ 1 lần)
                if teacher_id not in teachers_set:
                    teachers_set.add(teacher_id)
                    assignments.append({
                        'type': 'teacher',
                        'teacher_id': teacher_id,
                        'teacher_name': teacher_name,
                        'expertise': expertise
                    })
                
                # Lưu assignment
                assignments.append({
                    'type': 'assignment',
                    'teacher_id': teacher_id,
                    'class_name': class_name
                })
        
        print(f"\n📊 Đã đọc {len(teachers_set)} giáo viên")
        print(f"📊 Đã đọc {len([a for a in assignments if a['type'] == 'assignment'])} phân công lớp")
        
    except Exception as e:
        print(f"\n❌ Lỗi khi đọc CSV: {e}")
        return False
    
    # Tạo TTL content
    ttl_lines = []
    
    # Prefixes
    ttl_lines.append("@prefix ex:  <https://example.org/kg/> .")
    ttl_lines.append("@prefix edu: <https://example.org/edu#> .")
    ttl_lines.append("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .")
    ttl_lines.append("")
    
    # Teachers
    ttl_lines.append("# ========================================")
    ttl_lines.append("# TEACHERS")
    ttl_lines.append("# ========================================")
    ttl_lines.append("")
    
    for item in assignments:
        if item['type'] == 'teacher':
            teacher_id = item['teacher_id']
            teacher_name = item['teacher_name']
            expertise = item['expertise']
            
            ttl_lines.append(f"<https://example.org/kg/teacher/{teacher_id}> a edu:Teacher ;")
            ttl_lines.append(f'  edu:teacherId "{teacher_id}" ;')
            ttl_lines.append(f'  edu:fullName "{teacher_name}" ;')
            ttl_lines.append(f'  edu:expertise "{expertise}" .')
            ttl_lines.append("")
    
    # Assignments (Teacher teaches Class)
    ttl_lines.append("# ========================================")
    ttl_lines.append("# TEACHER ASSIGNMENTS")
    ttl_lines.append("# ========================================")
    ttl_lines.append("")
    
    for item in assignments:
        if item['type'] == 'assignment':
            teacher_id = item['teacher_id']
            class_name = item['class_name']
            class_id = class_name.replace('/', '_')
            
            ttl_lines.append(f"<https://example.org/kg/teacher/{teacher_id}> edu:teaches <https://example.org/kg/class/{class_id}> .")
    
    # Ghi file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(ttl_lines))
        
        print(f"\n✅ Đã tạo file TTL: {output_path}")
        print(f"📊 Số dòng: {len(ttl_lines)}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Lỗi khi ghi file: {e}")
        return False

def main():
    """Hàm chính"""
    success = export_teachers_assignments_ttl()
    
    if success:
        print("\n" + "=" * 70)
        print("✅ HOÀN THÀNH!")
        print("=" * 70)
        print("\n💡 Bước tiếp theo:")
        print("   1. Import file teachers_assignments.ttl vào GraphDB")
        print("   2. Hoặc chạy script import_all_kg.py")
    else:
        print("\n" + "=" * 70)
        print("❌ THẤT BẠI")
        print("=" * 70)

if __name__ == '__main__':
    main()
