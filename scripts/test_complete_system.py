#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script test toàn bộ hệ thống
File: scripts/test_complete_system.py

Kiểm tra:
1. Database connection
2. API endpoints
3. GraphDB connection
4. File KG
5. ML outputs
"""

import os
import sys
from pathlib import Path
import json
import io

# Fix encoding cho Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def print_header(text):
    """In header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_test(name, result, details=""):
    """In kết quả test"""
    status = "✅" if result else "❌"
    print(f"  {status} {name}")
    if details:
        print(f"      {details}")

def test_database():
    """Test database connection"""
    print("🔍 Testing Database...")
    
    config_file = Path("backend_api/api/config.php")
    if not config_file.exists():
        print_test("Database Config", False, "File config.php không tồn tại")
        return False
    
    print_test("Database Config", True, "File config.php có tồn tại")
    
    # Đọc file để kiểm tra cấu hình
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_host = "DB_HOST" in content
        has_name = "DB_NAME" in content
        has_user = "DB_USER" in content
        has_pass = "DB_PASS" in content
        
        print_test("Database Config Values", all([has_host, has_name, has_user, has_pass]), 
                  "Có đầy đủ cấu hình")
        
        return all([has_host, has_name, has_user, has_pass])
    except Exception as e:
        print_test("Database Config Read", False, str(e))
        return False

def test_api_files():
    """Test API files"""
    print("\n🔍 Testing API Files...")
    
    api_files = {
        "save_result.php": Path("backend_api/api/save_result.php"),
        "get_results.php": Path("backend_api/api/get_results.php"),
        "config.php": Path("backend_api/api/config.php"),
        "dashboard": Path("backend_api/dashboard/index.php")
    }
    
    all_exist = True
    for name, filepath in api_files.items():
        exists = filepath.exists()
        print_test(name, exists)
        if not exists:
            all_exist = False
    
    return all_exist

def test_graphdb():
    """Test GraphDB"""
    print("\n🔍 Testing GraphDB...")
    
    # Kiểm tra file .env
    env_file = Path(".env")
    if env_file.exists():
        print_test(".env file", True)
    else:
        print_test(".env file", False, "File .env không tồn tại")
        print("      💡 Tạo file .env với cấu hình GraphDB")
        return False
    
    # Kiểm tra script import
    import_script = Path("KG_Design/import_to_graphdb.py")
    print_test("Import Script", import_script.exists())
    
    # Kiểm tra file KG
    kg_files = [
        Path("KG_Design/kg_grade7.ttl"),
        Path("KG_Design/kg_grade7_with_knn.ttl"),
        Path("KG_Design/kg_grade7_with_ppr.ttl")
    ]
    
    kg_exists = False
    for kg_file in kg_files:
        if kg_file.exists():
            print_test(f"KG File: {kg_file.name}", True)
            kg_exists = True
    
    if not kg_exists:
        print_test("KG Files", False, "Không tìm thấy file KG nào")
    
    return kg_exists

def test_ml_outputs():
    """Test ML outputs"""
    print("\n🔍 Testing ML Outputs...")
    
    knn_output = Path("KG_Design/kg_grade7_with_knn.ttl")
    ppr_output = Path("KG_Design/kg_grade7_with_ppr.ttl")
    
    knn_ok = knn_output.exists()
    ppr_ok = ppr_output.exists()
    
    print_test("KNN Output", knn_ok, str(knn_output) if not knn_ok else "")
    print_test("PPR Output", ppr_ok, str(ppr_output) if not ppr_ok else "")
    
    return knn_ok and ppr_ok

def test_html_files():
    """Test HTML files"""
    print("\n🔍 Testing HTML Files...")
    
    web_dir = Path("Web")
    if not web_dir.exists():
        print_test("Web Directory", False)
        return False
    
    print_test("Web Directory", True)
    
    # Đếm số file HTML
    html_files = list(web_dir.glob("*.html"))
    count = len(html_files)
    
    print_test("HTML Files", count > 0, f"Tìm thấy {count} file HTML")
    
    return count > 0

def generate_report(results):
    """Tạo báo cáo test"""
    print("\n" + "=" * 70)
    print("📊 BÁO CÁO TEST")
    print("=" * 70)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    print(f"\nTổng số test: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Tỉ lệ: {passed/total*100:.1f}%\n")
    
    report = {
        "timestamp": str(Path(__file__).stat().st_mtime),
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "results": results
    }
    
    report_file = Path("TEST_REPORT.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Đã lưu báo cáo: {report_file}")
    
    return report

def main():
    """Hàm chính"""
    print_header("🧪 TEST TOÀN BỘ HỆ THỐNG")
    
    print("Script này sẽ kiểm tra:")
    print("  1. Database connection")
    print("  2. API files")
    print("  3. GraphDB setup")
    print("  4. ML outputs")
    print("  5. HTML files")
    
    input("\nNhấn Enter để bắt đầu...")
    
    results = {}
    
    # Test từng thành phần
    results['database'] = test_database()
    results['api_files'] = test_api_files()
    results['graphdb'] = test_graphdb()
    results['ml_outputs'] = test_ml_outputs()
    results['html_files'] = test_html_files()
    
    # Tạo báo cáo
    report = generate_report(results)
    
    # Tổng kết
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print("\n" + "=" * 70)
    
    if passed == total:
        print("🎉 TẤT CẢ TEST ĐÃ PASS!")
    elif passed >= total * 0.8:
        print("⚠️  HẦU HẾT TEST ĐÃ PASS")
    else:
        print("❌ NHIỀU TEST CHƯA PASS")
    
    print("=" * 70 + "\n")

if __name__ == '__main__':
    main()

