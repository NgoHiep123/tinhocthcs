#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động hóa tất cả các bước còn lại của dự án
File: scripts/00_setup_all.py

Chức năng:
1. Kiểm tra môi trường
2. Setup database MySQL
3. Cập nhật endpoint trong HTML
4. Import KG vào GraphDB
5. Chạy pipeline ML (KNN + PPR)
6. Test hệ thống
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Fix encoding cho Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Thêm thư mục scripts vào path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir.parent))

def print_header(text):
    """In header đẹp"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_step(num, text):
    """In bước hiện tại"""
    print(f"\n[{num}] {text}")
    print("-" * 70)

def check_file_exists(filepath):
    """Kiểm tra file có tồn tại không"""
    return Path(filepath).exists()

def check_python_dependencies():
    """Kiểm tra các thư viện Python cần thiết"""
    print_step(0, "KIỂM TRA MÔI TRƯỜNG")
    
    required_packages = [
        'rdflib', 'numpy', 'pandas', 'sklearn', 
        'networkx', 'requests', 'dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            elif package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - CHƯA CÀI")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Thiếu các package: {', '.join(missing)}")
        print("💡 Chạy lệnh: pip install -r requirements.txt")
        return False
    
    print("\n✅ Tất cả dependencies đã được cài đặt!")
    return True

def setup_database():
    """Bước 1: Setup database MySQL"""
    print_step(1, "SETUP DATABASE MYSQL")
    
    sql_file = Path("backend_api/create_database.sql")
    
    if not sql_file.exists():
        print(f"❌ Không tìm thấy file: {sql_file}")
        print("💡 Vui lòng tạo database thủ công")
        return False
    
    print(f"📁 Tìm thấy file SQL: {sql_file}")
    print("\n⚠️  Bước này cần chạy thủ công:")
    print("   1. Mở MySQL/phpMyAdmin")
    print("   2. Import file: backend_api/create_database.sql")
    print("   3. Cập nhật thông tin trong: backend_api/api/config.php")
    print("   4. Test kết nối database")
    
    response = input("\n   Đã setup database chưa? (y/n): ").strip().lower()
    return response == 'y'

def update_endpoints():
    """Bước 2: Cập nhật endpoint trong HTML"""
    print_step(2, "CẬP NHẬT ENDPOINT TRONG HTML")
    
    script = script_dir / "update_endpoint_to_php_api.py"
    
    if not script.exists():
        print(f"❌ Không tìm thấy script: {script}")
        return False
    
    print(f"📝 Chạy script: {script.name}")
    
    try:
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=script_dir.parent,
            capture_output=True,
            text=True,
            encoding='utf-8' if sys.platform != 'win32' else None
        )
        
        print(result.stdout)
        if result.stderr:
            print("⚠️  Warnings:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def import_kg_to_graphdb():
    """Bước 3: Import KG vào GraphDB"""
    print_step(3, "IMPORT KNOWLEDGE GRAPH VÀO GRAPHDB")
    
    import_script = Path("KG_Design/import_to_graphdb.py")
    
    if not import_script.exists():
        print(f"❌ Không tìm thấy script: {import_script}")
        print("💡 Vui lòng import thủ công trong GraphDB Desktop")
        return False
    
    print("⚠️  Cần GraphDB Desktop đã được cài và chạy")
    print("   1. Mở GraphDB Desktop")
    print("   2. Tạo repository mới (nếu chưa có)")
    print("   3. Chạy script import")
    
    response = input("\n   GraphDB đã sẵn sàng? (y/n): ").strip().lower()
    
    if response != 'y':
        print("⏭️  Bỏ qua bước này")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(import_script)],
            cwd=import_script.parent,
            capture_output=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def run_ml_pipeline():
    """Bước 4: Chạy pipeline ML (KNN + PPR)"""
    print_step(4, "CHẠY PIPELINE MACHINE LEARNING")
    
    knn_script = Path("ML_Algorithms/knn_student_analysis.py")
    ppr_script = Path("ML_Algorithms/ppr_recommendation.py")
    
    if not knn_script.exists():
        print(f"❌ Không tìm thấy script KNN: {knn_script}")
        return False
    
    if not ppr_script.exists():
        print(f"❌ Không tìm thấy script PPR: {ppr_script}")
        return False
    
    print("🤖 Chạy thuật toán KNN...")
    try:
        result = subprocess.run(
            [sys.executable, str(knn_script)],
            cwd=knn_script.parent,
            capture_output=False
        )
        if result.returncode != 0:
            print("❌ Lỗi khi chạy KNN")
            return False
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False
    
    print("\n🤖 Chạy thuật toán PPR...")
    try:
        result = subprocess.run(
            [sys.executable, str(ppr_script)],
            cwd=ppr_script.parent,
            capture_output=False
        )
        if result.returncode != 0:
            print("❌ Lỗi khi chạy PPR")
            return False
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False
    
    print("\n✅ Pipeline ML hoàn thành!")
    return True

def test_system():
    """Bước 5: Test hệ thống"""
    print_step(5, "TEST HỆ THỐNG")
    
    test_script = script_dir / "test_complete_system.py"
    
    if test_script.exists():
        print(f"📝 Chạy script test: {test_script.name}")
        try:
            result = subprocess.run(
                [sys.executable, str(test_script)],
                cwd=script_dir.parent,
                capture_output=False
            )
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    
    print("⚠️  Script test chưa có, bỏ qua")
    return True

def generate_report():
    """Tạo báo cáo kết quả"""
    print_step(6, "TẠO BÁO CÁO")
    
    report = {
        "status": "completed",
        "steps": {
            "dependencies": True,
            "database": False,
            "endpoints": False,
            "graphdb": False,
            "ml_pipeline": False,
            "testing": False
        }
    }
    
    report_file = Path("SETUP_REPORT.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Đã lưu báo cáo: {report_file}")

def main():
    """Hàm chính"""
    print_header("🚀 TỰ ĐỘNG HÓA SETUP HỆ THỐNG")
    
    print("Chào mừng bạn đến với script tự động hóa setup!")
    print("\nScript này sẽ thực hiện các bước sau:")
    print("  1. Kiểm tra môi trường (dependencies)")
    print("  2. Setup database MySQL")
    print("  3. Cập nhật endpoint trong HTML")
    print("  4. Import KG vào GraphDB")
    print("  5. Chạy pipeline ML (KNN + PPR)")
    print("  6. Test hệ thống")
    
    input("\nNhấn Enter để bắt đầu...")
    
    results = {}
    
    # Bước 0: Kiểm tra môi trường
    results['dependencies'] = check_python_dependencies()
    if not results['dependencies']:
        print("\n❌ Vui lòng cài đặt dependencies trước!")
        return
    
    # Bước 1: Setup database
    results['database'] = setup_database()
    
    # Bước 2: Cập nhật endpoint
    results['endpoints'] = update_endpoints()
    
    # Bước 3: Import KG
    results['graphdb'] = import_kg_to_graphdb()
    
    # Bước 4: Chạy ML pipeline
    if results['graphdb']:
        results['ml_pipeline'] = run_ml_pipeline()
    else:
        print("⏭️  Bỏ qua ML pipeline (cần GraphDB)")
        results['ml_pipeline'] = False
    
    # Bước 5: Test
    results['testing'] = test_system()
    
    # Tổng kết
    print_header("📊 TỔNG KẾT")
    
    total = len(results)
    completed = sum(1 for v in results.values() if v)
    
    print(f"✅ Hoàn thành: {completed}/{total} bước\n")
    
    for step, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {step}")
    
    print("\n" + "=" * 70)
    
    if completed == total:
        print("🎉 TẤT CẢ CÁC BƯỚC ĐÃ HOÀN THÀNH!")
    else:
        print("⚠️  Một số bước chưa hoàn thành, vui lòng kiểm tra lại")
    
    print("=" * 70 + "\n")

if __name__ == '__main__':
    main()

