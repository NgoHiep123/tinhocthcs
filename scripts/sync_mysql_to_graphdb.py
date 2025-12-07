#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script đồng bộ kết quả từ MySQL → GraphDB
Chạy định kỳ (cron job) để đồng bộ dữ liệu mới từ web tinhoc321.com

Usage:
    python scripts/sync_mysql_to_graphdb.py [--since TIMESTAMP] [--all]
"""

import sys
import os
import argparse
from datetime import datetime, timedelta
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    print("❌ Cần cài đặt: pip install mysql-connector-python")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("❌ Cần cài đặt: pip install requests")
    sys.exit(1)

try:
    from rdflib import Graph, URIRef, Literal, Namespace
    from rdflib.namespace import RDF, XSD
except ImportError:
    print("❌ Cần cài đặt: pip install rdflib")
    sys.exit(1)

# ============================================================
# CONFIGURATION
# ============================================================

# MySQL Config (đọc từ file config hoặc environment)
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'database': os.getenv('MYSQL_DATABASE', 'tinhoc321_quiz'),
    'user': os.getenv('MYSQL_USER', 'tinhoc321_user'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
}

# GraphDB Config
GRAPHDB_URL = os.getenv('GRAPHDB_URL', 'http://localhost:7200')
GRAPHDB_REPOSITORY = os.getenv('GRAPHDB_REPOSITORY', 'tinhocthcs')
GRAPHDB_USER = os.getenv('GRAPHDB_USER', 'admin')
GRAPHDB_PASSWORD = os.getenv('GRAPHDB_PASSWORD', 'root')

# Namespaces
EDU = Namespace('http://education.vn/ontology#')
DATA = Namespace('http://education.vn/data/')

# ============================================================
# FUNCTIONS
# ============================================================

def get_db_connection():
    """Kết nối MySQL"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        return conn
    except Error as e:
        print(f"❌ Lỗi kết nối MySQL: {e}")
        return None

def create_sync_log_table(cursor):
    """Tạo bảng log đồng bộ nếu chưa có"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS graphdb_sync_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            quiz_result_id INT NOT NULL,
            synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            error_message TEXT,
            INDEX idx_result (quiz_result_id),
            INDEX idx_synced (synced_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

def get_new_results(cursor, since_timestamp=None, all_records=False):
    """Lấy kết quả mới từ MySQL chưa đồng bộ"""
    if all_records:
        query = """
            SELECT qr.* FROM quiz_results qr
            LEFT JOIN graphdb_sync_log gsl ON qr.id = gsl.quiz_result_id
            WHERE gsl.id IS NULL
            ORDER BY qr.created_at
        """
        cursor.execute(query)
    elif since_timestamp:
        query = """
            SELECT qr.* FROM quiz_results qr
            LEFT JOIN graphdb_sync_log gsl ON qr.id = gsl.quiz_result_id
            WHERE qr.created_at > %s AND gsl.id IS NULL
            ORDER BY qr.created_at
        """
        cursor.execute(query, (since_timestamp,))
    else:
        # Mặc định: lấy kết quả trong 24h qua
        yesterday = datetime.now() - timedelta(days=1)
        query = """
            SELECT qr.* FROM quiz_results qr
            LEFT JOIN graphdb_sync_log gsl ON qr.id = gsl.quiz_result_id
            WHERE qr.created_at > %s AND gsl.id IS NULL
            ORDER BY qr.created_at
        """
        cursor.execute(query, (yesterday,))
    
    return cursor.fetchall()

def sanitize_for_uri(text):
    """Sanitize string để dùng trong URI"""
    import re
    # Thay thế ký tự đặc biệt bằng underscore
    text = re.sub(r'[^a-zA-Z0-9_]', '_', text)
    # Loại bỏ underscore liên tiếp
    text = re.sub(r'_+', '_', text)
    # Loại bỏ underscore ở đầu/cuối
    text = text.strip('_')
    return text

def create_test_result_ttl(result):
    """Tạo TTL cho TestResult từ dữ liệu MySQL"""
    g = Graph()
    g.bind('edu', EDU)
    g.bind('data', DATA)
    g.bind('rdf', RDF)
    g.bind('xsd', XSD)
    
    # Tạo URIs
    student_id = sanitize_for_uri(result['student_name'])
    test_id = sanitize_for_uri(result['quiz_id'])
    result_id = f"testresult_{student_id}_{test_id}_{result['id']}"
    
    result_uri = DATA[result_id]
    student_uri = DATA[f"student_{student_id}"]
    test_uri = DATA[f"test_{test_id}"]
    
    # TestResult instance
    g.add((result_uri, RDF.type, EDU.TestResult))
    
    # Score (decimal 0.0-1.0)
    percentage = float(result['score']) / float(result['total'])
    g.add((result_uri, EDU.score, Literal(percentage, datatype=XSD.decimal)))
    
    # ForTest
    g.add((result_uri, EDU.forTest, test_uri))
    
    # TestDate
    if isinstance(result['created_at'], datetime):
        test_date = result['created_at']
    else:
        test_date = datetime.fromisoformat(str(result['created_at']).replace(' ', 'T'))
    g.add((result_uri, EDU.testDate, Literal(test_date, datatype=XSD.dateTime)))
    
    # Duration (nếu có)
    if result.get('duration'):
        g.add((result_uri, EDU.duration, Literal(result['duration'], datatype=XSD.integer)))
    
    # Student relationships
    g.add((student_uri, EDU.hasResult, result_uri))
    g.add((student_uri, EDU.takeTest, test_uri))
    
    return g.serialize(format='turtle', encoding='utf-8').decode('utf-8')

def upload_to_graphdb(ttl_content):
    """Upload TTL vào GraphDB qua REST API"""
    url = f"{GRAPHDB_URL}/repositories/{GRAPHDB_REPOSITORY}/statements"
    
    auth = None
    if GRAPHDB_USER and GRAPHDB_PASSWORD:
        from requests.auth import HTTPBasicAuth
        auth = HTTPBasicAuth(GRAPHDB_USER, GRAPHDB_PASSWORD)
    
    try:
        response = requests.post(
            url,
            data=ttl_content.encode('utf-8'),
            headers={
                'Content-Type': 'text/turtle',
                'Accept': 'application/sparql-results+json'
            },
            auth=auth,
            timeout=30
        )
        response.raise_for_status()
        return True, None
    except requests.exceptions.RequestException as e:
        return False, str(e)

def log_sync(cursor, result_id, success=True, error_message=None):
    """Ghi log đồng bộ"""
    if success:
        cursor.execute(
            "INSERT INTO graphdb_sync_log (quiz_result_id) VALUES (%s)",
            (result_id,)
        )
    else:
        cursor.execute(
            "INSERT INTO graphdb_sync_log (quiz_result_id, error_message) VALUES (%s, %s)",
            (result_id, error_message)
        )

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Đồng bộ MySQL → GraphDB')
    parser.add_argument('--since', help='Đồng bộ từ thời điểm (YYYY-MM-DD HH:MM:SS)')
    parser.add_argument('--all', action='store_true', help='Đồng bộ tất cả (chưa đồng bộ)')
    parser.add_argument('--config', help='File config JSON')
    
    args = parser.parse_args()
    
    # Load config từ file nếu có
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
            MYSQL_CONFIG.update(config.get('mysql', {}))
            globals().update({
                'GRAPHDB_URL': config.get('graphdb', {}).get('url', GRAPHDB_URL),
                'GRAPHDB_REPOSITORY': config.get('graphdb', {}).get('repository', GRAPHDB_REPOSITORY),
            })
    
    print("🔄 Đang đồng bộ MySQL → GraphDB...")
    print(f"   MySQL: {MYSQL_CONFIG['database']}")
    print(f"   GraphDB: {GRAPHDB_URL}/{GRAPHDB_REPOSITORY}")
    
    # Kết nối MySQL
    conn = get_db_connection()
    if not conn:
        sys.exit(1)
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Tạo bảng log
        create_sync_log_table(cursor)
        
        # Parse since_timestamp
        since_timestamp = None
        if args.since:
            try:
                since_timestamp = datetime.strptime(args.since, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                print(f"❌ Format timestamp không đúng. Dùng: YYYY-MM-DD HH:MM:SS")
                sys.exit(1)
        
        # Lấy kết quả mới
        results = get_new_results(cursor, since_timestamp, args.all)
        
        if not results:
            print("✅ Không có dữ liệu mới cần đồng bộ")
            return
        
        print(f"📊 Tìm thấy {len(results)} kết quả mới")
        
        success_count = 0
        error_count = 0
        
        for result in results:
            try:
                # Tạo TTL
                ttl = create_test_result_ttl(result)
                
                # Upload vào GraphDB
                success, error = upload_to_graphdb(ttl)
                
                if success:
                    log_sync(cursor, result['id'], success=True)
                    conn.commit()
                    success_count += 1
                    print(f"✅ [{success_count}] {result['student_name']} - {result['quiz_id']} ({result['score']}/{result['total']})")
                else:
                    log_sync(cursor, result['id'], success=False, error_message=error)
                    conn.commit()
                    error_count += 1
                    print(f"❌ [{error_count}] Lỗi: {result['id']} - {error}")
                    
            except Exception as e:
                error_count += 1
                error_msg = str(e)
                log_sync(cursor, result['id'], success=False, error_message=error_msg)
                conn.commit()
                print(f"❌ [{error_count}] Exception: {result['id']} - {error_msg}")
        
        print(f"\n📊 Tổng kết:")
        print(f"   ✅ Thành công: {success_count}")
        print(f"   ❌ Lỗi: {error_count}")
        print(f"   📝 Tổng cộng: {len(results)}")
        
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    main()

