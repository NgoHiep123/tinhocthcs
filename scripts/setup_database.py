#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động setup database MySQL
File: scripts/setup_database.py
"""

import os
import sys
import subprocess
from pathlib import Path
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

def check_mysql_available():
    """Kiểm tra MySQL có sẵn không"""
    print("🔍 Kiểm tra MySQL...")
    
    try:
        result = subprocess.run(
            ['mysql', '--version'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ MySQL đã cài đặt: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠️  MySQL command không tìm thấy trong PATH")
    print("💡 Bạn có thể:")
    print("   1. Cài đặt MySQL")
    print("   2. Sử dụng XAMPP/WAMP (MySQL trong thư mục bin)")
    print("   3. Hoặc setup thủ công qua phpMyAdmin")
    
    return False

def setup_database_interactive():
    """Setup database với tương tác người dùng"""
    print_header("SETUP DATABASE MYSQL")
    
    sql_file = Path("backend_api/create_database.sql")
    
    if not sql_file.exists():
        print(f"❌ Không tìm thấy file: {sql_file}")
        return False
    
    print(f"📁 File SQL: {sql_file}")
    
    # Đọc file SQL để hiển thị
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    print(f"\n📊 Database sẽ được tạo với schema từ file SQL")
    print(f"   (Có {len(sql_content.split(';'))} statements)")
    
    if check_mysql_available():
        print("\n💡 Bạn có muốn import tự động không?")
        print("   (Cần MySQL username/password)")
        
        choice = input("\n   Import tự động? (y/n): ").strip().lower()
        
        if choice == 'y':
            username = input("   MySQL username [root]: ").strip() or "root"
            password = input("   MySQL password: ").strip()
            
            if not password:
                print("⚠️  Không có password, bỏ qua import tự động")
                return setup_manual()
            
            print("\n🔄 Đang import...")
            try:
                # Tạo command
                cmd = ['mysql', '-u', username, f'-p{password}']
                process = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = process.communicate(input=sql_content)
                
                if process.returncode == 0:
                    print("✅ Import thành công!")
                    
                    # Test kết nối
                    print("\n🔍 Kiểm tra kết nối...")
                    test_query = "SHOW DATABASES LIKE 'tinhoc321_quiz';"
                    test_process = subprocess.Popen(
                        ['mysql', '-u', username, f'-p{password}', '-e', test_query],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    test_stdout, _ = test_process.communicate()
                    
                    if 'tinhoc321_quiz' in test_stdout:
                        print("✅ Database đã được tạo thành công!")
                        return True
                    else:
                        print("⚠️  Database có thể chưa được tạo")
                        return False
                else:
                    print(f"❌ Lỗi khi import: {stderr}")
                    return False
                    
            except Exception as e:
                print(f"❌ Lỗi: {e}")
                return setup_manual()
    
    return setup_manual()

def setup_manual():
    """Hướng dẫn setup thủ công"""
    print("\n" + "=" * 70)
    print("📖 HƯỚNG DẪN SETUP THỦ CÔNG")
    print("=" * 70)
    
    print("\nCách 1: Sử dụng phpMyAdmin")
    print("  1. Mở phpMyAdmin (http://localhost/phpmyadmin)")
    print("  2. Chọn tab 'Import'")
    print("  3. Chọn file: backend_api/create_database.sql")
    print("  4. Click 'Go' để import")
    
    print("\nCách 2: Sử dụng MySQL Command Line")
    print("  mysql -u root -p < backend_api/create_database.sql")
    
    print("\nCách 3: Copy SQL và chạy trong MySQL")
    sql_file = Path("backend_api/create_database.sql")
    print(f"  File: {sql_file}")
    
    print("\n⚠️  Sau khi import, nhớ:")
    print("  1. Cập nhật backend_api/api/config.php với thông tin database")
    print("  2. Test kết nối bằng: backend_api/test_connection.php")
    
    response = input("\n   Đã setup xong chưa? (y/n): ").strip().lower()
    return response == 'y'

def update_config_file():
    """Cập nhật file config.php với thông tin database"""
    print("\n" + "=" * 70)
    print("⚙️  CẬP NHẬT FILE CONFIG")
    print("=" * 70)
    
    config_file = Path("backend_api/api/config.php")
    
    if not config_file.exists():
        print(f"❌ Không tìm thấy file: {config_file}")
        return False
    
    print(f"\n📁 File config: {config_file}")
    print("\n💡 Vui lòng cập nhật các thông tin sau trong file config.php:")
    print("   - DB_HOST: localhost (hoặc IP server)")
    print("   - DB_NAME: tinhoc321_quiz")
    print("   - DB_USER: MySQL username")
    print("   - DB_PASS: MySQL password")
    
    print("\n📝 Hoặc nhập thông tin để tự động cập nhật:")
    
    db_host = input("   DB_HOST [localhost]: ").strip() or "localhost"
    db_name = input("   DB_NAME [tinhoc321_quiz]: ").strip() or "tinhoc321_quiz"
    db_user = input("   DB_USER [root]: ").strip() or "root"
    db_pass = input("   DB_PASS: ").strip()
    
    if db_pass:
        # Đọc file config
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Cập nhật các giá trị
        import re
        content = re.sub(r"define\('DB_HOST',\s*'[^']*'\);", f"define('DB_HOST', '{db_host}');", content)
        content = re.sub(r"define\('DB_NAME',\s*'[^']*'\);", f"define('DB_NAME', '{db_name}');", content)
        content = re.sub(r"define\('DB_USER',\s*'[^']*'\);", f"define('DB_USER', '{db_user}');", content)
        content = re.sub(r"define\('DB_PASS',\s*'[^']*'\);", f"define('DB_PASS', '{db_pass}');", content)
        
        # Lưu file
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Đã cập nhật file config.php!")
        return True
    else:
        print("⚠️  Bỏ qua cập nhật tự động")
        return False

def main():
    """Hàm chính"""
    print_header("🔧 SETUP DATABASE MYSQL")
    
    # Setup database
    db_ok = setup_database_interactive()
    
    if db_ok:
        # Cập nhật config
        update_config_file()
        
        print("\n" + "=" * 70)
        print("✅ SETUP DATABASE HOÀN TẤT")
        print("=" * 70)
        print("\n💡 Bước tiếp theo:")
        print("  1. Test kết nối: backend_api/test_connection.php")
        print("  2. Test API: backend_api/test_api.php")
        print("  3. Xem dashboard: backend_api/dashboard/index.php")
    else:
        print("\n" + "=" * 70)
        print("⚠️  SETUP CHƯA HOÀN TẤT")
        print("=" * 70)
        print("\n💡 Vui lòng setup database thủ công theo hướng dẫn trên")

if __name__ == '__main__':
    main()

