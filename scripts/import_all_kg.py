#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script import tất cả file Knowledge Graph vào GraphDB
File: scripts/import_all_kg.py

Chức năng:
- Import tất cả file .ttl vào GraphDB Desktop
- Hỗ trợ import nhiều file cùng lúc
- Kiểm tra và báo cáo kết quả
"""

import os
import sys
from pathlib import Path
import io

# Fix encoding cho Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Thêm thư mục KG_Design vào path
kg_design_dir = Path(__file__).parent.parent / "KG_Design"
sys.path.insert(0, str(kg_design_dir))

# Thêm thư mục gốc vào path để import dotenv
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def print_header(text):
    """In header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def find_ttl_files():
    """Tìm tất cả file .ttl trong dự án"""
    print("🔍 Đang tìm các file .ttl...")
    
    ttl_files = []
    
    # Tìm trong KG_Design
    kg_dir = Path("KG_Design")
    if kg_dir.exists():
        # File chính
        main_files = [
            kg_dir / "kg_grade7.ttl",
            kg_dir / "kg_grade7_with_knn.ttl",
            kg_dir / "kg_grade7_with_ppr.ttl"
        ]
        
        for f in main_files:
            if f.exists():
                ttl_files.append(f)
        
        # Files trong grade6/out/
        grade6_out = kg_dir / "grade6" / "out"
        if grade6_out.exists():
            for f in grade6_out.glob("*.ttl"):
                ttl_files.append(f)
    
    print(f"📁 Tìm thấy {len(ttl_files)} file .ttl:\n")
    for i, f in enumerate(ttl_files, 1):
        print(f"   {i}. {f}")
    
    return ttl_files

def check_graphdb_connection():
    """Kiểm tra kết nối GraphDB"""
    print("\n🔌 Kiểm tra kết nối GraphDB...")
    
    try:
        # Import module test_graphdb_connection từ KG_Design
        import importlib.util
        test_script = kg_design_dir / "test_graphdb_connection.py"
        
        if not test_script.exists():
            print("⚠️  Không tìm thấy script test GraphDB")
            return False
        
        spec = importlib.util.spec_from_file_location("test_kg", test_script)
        test_kg = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_kg)
        
        # Kiểm tra kết nối
        import requests
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        server = os.getenv('GRAPHDB_SERVER', 'http://localhost:7200')
        
        try:
            response = requests.get(f"{server}/rest/repositories", timeout=5)
            if response.status_code == 200:
                print("✅ Kết nối GraphDB thành công!")
                return True
            else:
                print(f"❌ Không thể kết nối GraphDB (status: {response.status_code})")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Không thể kết nối đến GraphDB server")
            print("💡 Đảm bảo GraphDB Desktop đã được khởi động")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def import_file_to_graphdb(ttl_file, clear_first=False):
    """Import một file .ttl vào GraphDB"""
    print(f"\n📤 Đang import: {ttl_file.name}")
    
    try:
        import requests
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        GRAPHDB_SERVER = os.getenv('GRAPHDB_SERVER', 'http://localhost:7200')
        GRAPHDB_REPOSITORY = os.getenv('GRAPHDB_REPOSITORY', 'tin_hoc_thcs')
        GRAPHDB_USERNAME = os.getenv('GRAPHDB_USERNAME', 'admin')
        GRAPHDB_PASSWORD = os.getenv('GRAPHDB_PASSWORD', 'root')
        
        # Xóa dữ liệu cũ nếu cần
        if clear_first:
            url = f"{GRAPHDB_SERVER}/repositories/{GRAPHDB_REPOSITORY}/statements"
            requests.delete(url, auth=(GRAPHDB_USERNAME, GRAPHDB_PASSWORD))
            print("🗑️  Đã xóa dữ liệu cũ")
        
        # Đọc file Turtle
        with open(ttl_file, 'r', encoding='utf-8') as f:
            turtle_content = f.read()
        
        # URL để import
        url = f"{GRAPHDB_SERVER}/repositories/{GRAPHDB_REPOSITORY}/statements"
        
        # Headers
        headers = {'Content-Type': 'application/x-turtle'}
        
        # Upload
        response = requests.post(
            url,
            data=turtle_content.encode('utf-8'),
            headers=headers,
            auth=(GRAPHDB_USERNAME, GRAPHDB_PASSWORD),
            timeout=30
        )
        
        if response.status_code == 204:
            print(f"✅ Import thành công: {ttl_file.name}")
            return True
        else:
            print(f"❌ Import thất bại: {ttl_file.name} (status: {response.status_code})")
            print(f"   Response: {response.text[:200]}")
            return False
        
    except Exception as e:
        print(f"❌ Lỗi khi import {ttl_file.name}: {e}")
        return False

def main():
    """Hàm chính"""
    print_header("📦 IMPORT TẤT CẢ KNOWLEDGE GRAPH VÀO GRAPHDB")
    
    # Tìm file .ttl
    ttl_files = find_ttl_files()
    
    if not ttl_files:
        print("\n❌ Không tìm thấy file .ttl nào!")
        print("💡 Hãy đảm bảo đã:")
        print("   1. Chạy build_kg_grade7.py để tạo KG")
        print("   2. Export TTL cho grade6 nếu cần")
        return
    
    # Kiểm tra GraphDB
    if not check_graphdb_connection():
        print("\n⚠️  Không thể kết nối GraphDB")
        print("💡 Hãy đảm bảo:")
        print("   1. GraphDB Desktop đã được cài và khởi động")
        print("   2. Repository đã được tạo")
        print("   3. File .env có cấu hình đúng")
        
        response = input("\n   Vẫn tiếp tục? (y/n): ").strip().lower()
        if response != 'y':
            return
    
    # Hỏi có muốn xóa dữ liệu cũ không
    print("\n⚠️  Bạn có muốn xóa dữ liệu cũ trong repository không?")
    print("   (Chỉ xóa khi import lần đầu)")
    clear_choice = input("   Xóa dữ liệu cũ? (y/n): ").strip().lower()
    clear_first = (clear_choice == 'y' and len(ttl_files) > 0)
    
    # Import từng file
    print("\n" + "=" * 70)
    print("🚀 BẮT ĐẦU IMPORT")
    print("=" * 70)
    
    results = {}
    for i, ttl_file in enumerate(ttl_files, 1):
        print(f"\n[{i}/{len(ttl_files)}] {ttl_file.name}")
        
        # Chỉ xóa dữ liệu cũ ở file đầu tiên
        clear = clear_first and (i == 1)
        
        success = import_file_to_graphdb(ttl_file, clear_first=clear)
        results[ttl_file.name] = success
        
        if not success:
            print(f"⚠️  File {ttl_file.name} import thất bại, tiếp tục file tiếp theo...")
    
    # Tổng kết
    print("\n" + "=" * 70)
    print("📊 TỔNG KẾT")
    print("=" * 70)
    
    total = len(results)
    success_count = sum(1 for v in results.values() if v)
    
    print(f"\n✅ Thành công: {success_count}/{total}")
    print(f"❌ Thất bại: {total - success_count}/{total}\n")
    
    for filename, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {filename}")
    
    if success_count == total:
        print("\n🎉 TẤT CẢ FILE ĐÃ ĐƯỢC IMPORT THÀNH CÔNG!")
        print("\n💡 Bước tiếp theo:")
        print("   1. Kiểm tra dữ liệu trong GraphDB Desktop")
        print("   2. Chạy các query test")
        print("   3. Chạy pipeline ML (KNN + PPR)")
    else:
        print("\n⚠️  MỘT SỐ FILE CHƯA ĐƯỢC IMPORT")
        print("💡 Vui lòng kiểm tra lại:")
        print("   1. GraphDB có đang chạy không?")
        print("   2. Repository đã được tạo chưa?")
        print("   3. File .env có cấu hình đúng không?")
    
    print("=" * 70 + "\n")

if __name__ == '__main__':
    main()

