#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script export dữ liệu từ MySQL → student_assessment.csv

Usage:
    python export_student_assessment_from_mysql.py [options]

Options:
    --host HOST          MySQL host (default: localhost)
    --port PORT          MySQL port (default: 3306)
    --user USER          MySQL username
    --password PASS      MySQL password
    --database DB        Database name (default: tinhoc321_quiz)
    --config FILE        JSON config file (thay cho các option trên)
    --output FILE        Output CSV file (default: ../../csv/student_assessment.csv)
    --year YEAR          Year for assessId (default: 2024)
    --limit LIMIT        Limit số bản ghi (default: 10000)
    --students-file FILE File CSV mapping students (default: ../../csv/students_25_26.csv)
    --normalize-score    Chuẩn hóa score về 0-1 (default: True)
    --help               Hiển thị help
"""

import sys
import os
import argparse
import json
import csv
from pathlib import Path
from datetime import datetime
import unicodedata
import re

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    print("❌ Cần cài đặt: pip install mysql-connector-python")
    sys.exit(1)

# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'tinhoc321_quiz',
    'user': 'root',
    'password': '',
}

# ============================================================
# FUNCTIONS
# ============================================================

def normalize_text(text):
    """Chuẩn hóa text: lowercase, bỏ dấu, trim"""
    if not text:
        return ''
    # Chuyển về lowercase
    text = text.lower().strip()
    # Bỏ dấu tiếng Việt
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text

def load_students_mapping(students_file):
    """Load mapping từ students_25_26.csv"""
    mapping = {}
    if not os.path.exists(students_file):
        print(f"⚠️  File không tồn tại: {students_file}")
        return mapping
    
    try:
        with open(students_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Thử các cột có thể có
                student_id = row.get('id_student') or row.get('studentId') or row.get('student_id')
                full_name = row.get('full_name') or row.get('fullName') or row.get('name')
                class_name = row.get('class') or row.get('className') or row.get('class_name')
                
                if student_id and full_name and class_name:
                    # Tạo key normalized
                    key = (normalize_text(full_name), normalize_text(class_name))
                    mapping[key] = student_id
                    # Cũng lưu với key gốc (có dấu)
                    key_original = (full_name.strip(), class_name.strip())
                    mapping[key_original] = student_id
        
        print(f"✅ Đã load {len(mapping)} mapping từ {students_file}")
    except Exception as e:
        print(f"⚠️  Lỗi khi đọc file students: {e}")
    
    return mapping

def find_student_id(student_name, class_name, mapping):
    """Tìm studentId từ student_name và class_name"""
    # Thử key gốc trước
    key_original = (student_name.strip(), class_name.strip())
    if key_original in mapping:
        return mapping[key_original]
    
    # Thử key normalized
    key_normalized = (normalize_text(student_name), normalize_text(class_name))
    if key_normalized in mapping:
        return mapping[key_normalized]
    
    # Không tìm thấy
    return None

def quiz_id_to_assess_id(quiz_id, year=2024):
    """Chuyển quiz_id thành assessId"""
    # K6_A1 → ASSESS_K6_A1_2024
    # K7_E1 → ASSESS_K7_E1_2024
    if quiz_id.startswith('K'):
        return f"ASSESS_{quiz_id}_{year}"
    return f"ASSESS_{quiz_id}_{year}"

def get_db_connection(config):
    """Kết nối MySQL"""
    try:
        conn = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password'],
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        return conn
    except Error as e:
        print(f"❌ Lỗi kết nối MySQL: {e}")
        return None

def export_data(conn, students_mapping, output_file, year=2024, limit=10000, normalize_score=True):
    """Export dữ liệu từ MySQL"""
    cursor = conn.cursor(dictionary=True)
    
    # Query dữ liệu
    query = """
        SELECT 
            student_name,
            class_name,
            quiz_id,
            score,
            total,
            percentage,
            created_at
        FROM quiz_results
        ORDER BY created_at DESC
        LIMIT %s
    """
    
    print(f"📊 Đang query dữ liệu (limit: {limit})...")
    cursor.execute(query, (limit,))
    results = cursor.fetchall()
    
    print(f"✅ Đã lấy {len(results)} bản ghi")
    
    # Thống kê
    stats = {
        'total': len(results),
        'mapped': 0,
        'unmapped': 0,
        'skipped': 0
    }
    
    # Ghi ra CSV
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['studentId', 'assessId', 'score'])
        
        for row in results:
            student_name = row['student_name']
            class_name = row['class_name']
            quiz_id = row['quiz_id']
            score = row['score']
            total = row['total']
            
            # Tìm studentId
            student_id = find_student_id(student_name, class_name, students_mapping)
            
            if not student_id:
                stats['unmapped'] += 1
                print(f"⚠️  Không tìm thấy mapping: {student_name} - {class_name}")
                # Có thể bỏ qua hoặc tạo studentId mới
                # Ở đây ta bỏ qua
                continue
            
            # Chuyển quiz_id → assessId
            assess_id = quiz_id_to_assess_id(quiz_id, year)
            
            # Chuẩn hóa score
            if normalize_score:
                # Chuẩn hóa về 0-1
                normalized_score = round(score / total, 2) if total > 0 else 0.0
            else:
                # Giữ nguyên score (0-10)
                normalized_score = round((score / total) * 10, 1) if total > 0 else 0.0
            
            # Ghi ra CSV
            writer.writerow([student_id, assess_id, normalized_score])
            stats['mapped'] += 1
    
    cursor.close()
    
    # Báo cáo
    print("\n📊 THỐNG KÊ:")
    print(f"  ✅ Tổng số bản ghi: {stats['total']}")
    print(f"  ✅ Đã map thành công: {stats['mapped']}")
    print(f"  ⚠️  Không tìm thấy mapping: {stats['unmapped']}")
    print(f"  📁 File output: {output_path.absolute()}")
    
    return stats

# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='Export dữ liệu từ MySQL → student_assessment.csv',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  # Dùng tham số dòng lệnh
  python export_student_assessment_from_mysql.py \\
      --host mysql.tinhoc123.com \\
      --user username \\
      --password password \\
      --database tinhoc321_quiz \\
      --output csv/student_assessment.csv

  # Dùng file config
  python export_student_assessment_from_mysql.py \\
      --config mysql_config.json \\
      --output csv/student_assessment.csv
        """
    )
    
    parser.add_argument('--host', help='MySQL host', default=None)
    parser.add_argument('--port', type=int, help='MySQL port', default=3306)
    parser.add_argument('--user', help='MySQL username', default=None)
    parser.add_argument('--password', help='MySQL password', default=None)
    parser.add_argument('--database', help='Database name', default='tinhoc321_quiz')
    parser.add_argument('--config', help='JSON config file', default=None)
    parser.add_argument('--output', help='Output CSV file', 
                       default='../../csv/student_assessment.csv')
    parser.add_argument('--year', type=int, help='Year for assessId', default=2024)
    parser.add_argument('--limit', type=int, help='Limit số bản ghi', default=10000)
    parser.add_argument('--students-file', help='File CSV mapping students',
                       default='../../csv/students_25_26.csv')
    parser.add_argument('--normalize-score', action='store_true', default=True,
                       help='Chuẩn hóa score về 0-1')
    parser.add_argument('--no-normalize-score', dest='normalize_score', action='store_false',
                       help='Không chuẩn hóa score (giữ nguyên 0-10)')
    
    args = parser.parse_args()
    
    # Load config
    config = DEFAULT_CONFIG.copy()
    
    if args.config:
        # Load từ file config
        if not os.path.exists(args.config):
            print(f"❌ File config không tồn tại: {args.config}")
            sys.exit(1)
        
        with open(args.config, 'r', encoding='utf-8') as f:
            file_config = json.load(f)
            config.update(file_config)
    
    # Override với tham số dòng lệnh
    if args.host:
        config['host'] = args.host
    if args.port:
        config['port'] = args.port
    if args.user:
        config['user'] = args.user
    if args.password:
        config['password'] = args.password
    if args.database:
        config['database'] = args.database
    
    # Kiểm tra thông tin bắt buộc
    if not config.get('user') or not config.get('password'):
        print("❌ Thiếu username hoặc password!")
        print("💡 Dùng --user và --password hoặc --config")
        sys.exit(1)
    
    # Resolve paths
    script_dir = Path(__file__).parent
    students_file = (script_dir / args.students_file).resolve()
    output_file = (script_dir / args.output).resolve()
    
    print("=" * 60)
    print("📥 EXPORT STUDENT ASSESSMENT TỪ MYSQL")
    print("=" * 60)
    print(f"Host: {config['host']}")
    print(f"Database: {config['database']}")
    print(f"User: {config['user']}")
    print(f"Students file: {students_file}")
    print(f"Output file: {output_file}")
    print("=" * 60)
    
    # Load students mapping
    print("\n📚 Đang load mapping students...")
    students_mapping = load_students_mapping(str(students_file))
    
    if not students_mapping:
        print("⚠️  Không có mapping students! Tiếp tục với mapping rỗng...")
        response = input("Bạn có muốn tiếp tục? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Kết nối MySQL
    print("\n🔌 Đang kết nối MySQL...")
    conn = get_db_connection(config)
    if not conn:
        sys.exit(1)
    
    print("✅ Kết nối thành công!")
    
    try:
        # Export dữ liệu
        print("\n📊 Đang export dữ liệu...")
        stats = export_data(
            conn,
            students_mapping,
            str(output_file),
            year=args.year,
            limit=args.limit,
            normalize_score=args.normalize_score
        )
        
        print("\n✅ Hoàn thành!")
        print(f"📁 File đã được lưu: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        conn.close()

if __name__ == '__main__':
    main()

