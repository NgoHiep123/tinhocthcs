# 🔗 TÍCH HỢP WEB TINHOC321.COM VỚI KNOWLEDGE GRAPH

## 📊 TÌNH TRẠNG HIỆN TẠI

### ✅ ĐÃ CÓ:

1. **Web tinhoc321.com** (github.com/NgoHiep123/tinhocthcs):
   - ✅ Các file HTML quiz (K6_*, K7_*, K8_*, K9_*)
   - ✅ Gửi kết quả đến PHP API: `https://tinhoc321.com/api/save_result.php`
   - ✅ Lưu vào MySQL database: `tinhoc321_quiz.quiz_results`

2. **Knowledge Graph (GraphDB)**:
   - ✅ Schema đã định nghĩa: `edu:TestResult`, `edu:Student`, `edu:Test`
   - ✅ Đã upload dữ liệu mẫu từ các file `.ttl`
   - ✅ Repository: `tinhocthcs`

### ❌ CHƯA CÓ:

- ❌ **Tích hợp tự động**: Kết quả từ web CHƯA tự động đồng bộ vào GraphDB
- ❌ **Script đồng bộ**: Chưa có script để chuyển dữ liệu từ MySQL → GraphDB

---

## 🎯 GIẢI PHÁP

Có **3 cách** để tích hợp:

### **Cách 1: Đồng bộ real-time (Khuyến nghị)**

Sửa `save_result.php` để **vừa lưu MySQL vừa ghi GraphDB** ngay khi học sinh nộp bài.

**Ưu điểm:**
- ✅ Real-time, không bị trễ
- ✅ Đảm bảo dữ liệu đồng bộ

**Nhược điểm:**
- ⚠️ Tăng thời gian xử lý (phải gọi GraphDB API)
- ⚠️ Nếu GraphDB down thì không lưu được

---

### **Cách 2: Đồng bộ định kỳ (Background job)**

Tạo script Python chạy định kỳ (cron job) để đồng bộ dữ liệu mới từ MySQL → GraphDB.

**Ưu điểm:**
- ✅ Tách biệt: MySQL không phụ thuộc GraphDB
- ✅ Có thể retry nếu lỗi

**Nhược điểm:**
- ⚠️ Có độ trễ (ví dụ: đồng bộ mỗi 5 phút)
- ⚠️ Cần setup cron job

---

### **Cách 3: Đồng bộ thủ công**

Chạy script Python khi cần để export dữ liệu từ MySQL và import vào GraphDB.

**Ưu điểm:**
- ✅ Đơn giản, không cần setup phức tạp
- ✅ Kiểm soát được thời điểm đồng bộ

**Nhược điểm:**
- ⚠️ Không tự động
- ⚠️ Dễ quên chạy

---

## 🚀 IMPLEMENTATION

### **CÁCH 1: Real-time Integration**

#### **Bước 1: Cài đặt GraphDB Python Client**

```bash
pip install requests rdflib
```

#### **Bước 2: Tạo module tích hợp GraphDB**

Tạo file: `backend_api/api/graphdb_sync.php`

```php
<?php
/**
 * FILE: api/graphdb_sync.php
 * Mô tả: Hàm đồng bộ kết quả vào GraphDB
 */

require_once 'config.php';

/**
 * Đồng bộ TestResult vào GraphDB
 */
function syncTestResultToGraphDB($result_data) {
    $graphdb_url = getenv('GRAPHDB_URL') ?: 'http://localhost:7200';
    $repository = getenv('GRAPHDB_REPOSITORY') ?: 'tinhocthcs';
    
    // Tạo TTL cho TestResult
    $ttl = generateTestResultTTL($result_data);
    
    // Gửi đến GraphDB REST API
    $url = "$graphdb_url/repositories/$repository/statements";
    
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $ttl);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: text/turtle',
        'Accept: application/sparql-results+json'
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($http_code >= 200 && $http_code < 300) {
        return ['success' => true];
    } else {
        error_log("GraphDB sync failed: $response");
        return ['success' => false, 'error' => $response];
    }
}

/**
 * Tạo TTL từ dữ liệu MySQL
 */
function generateTestResultTTL($data) {
    $student_id = sanitizeForURI($data['student_name']);
    $test_id = $data['quiz_id'];
    $score = $data['score'];
    $total = $data['total'];
    $percentage = ($score / $total);
    $timestamp = date('c', strtotime($data['created_at']));
    
    $result_id = "testresult_${student_id}_${test_id}_" . time();
    
    $ttl = "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n";
    $ttl .= "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n";
    $ttl .= "@prefix edu: <http://education.vn/ontology#> .\n";
    $ttl .= "@prefix data: <http://education.vn/data/> .\n\n";
    
    $ttl .= "data:${result_id} a edu:TestResult ;\n";
    $ttl .= "    edu:score \"${percentage}\"^^xsd:decimal ;\n";
    $ttl .= "    edu:forTest data:test_${test_id} ;\n";
    $ttl .= "    edu:testDate \"${timestamp}\"^^xsd:dateTime .\n\n";
    
    $ttl .= "data:student_${student_id} edu:hasResult data:${result_id} .\n";
    $ttl .= "data:student_${student_id} edu:takeTest data:test_${test_id} .\n";
    
    return $ttl;
}

function sanitizeForURI($str) {
    return preg_replace('/[^a-zA-Z0-9_]/', '_', $str);
}
?>
```

#### **Bước 3: Sửa `save_result.php`**

Thêm vào cuối file, sau khi lưu MySQL thành công:

```php
// ... (sau khi lưu MySQL thành công)

// Đồng bộ vào GraphDB (non-blocking)
try {
    require_once 'graphdb_sync.php';
    syncTestResultToGraphDB([
        'student_name' => $student_name,
        'class_name' => $class_name,
        'quiz_id' => $quiz_id,
        'score' => $score,
        'total' => $total,
        'created_at' => date('Y-m-d H:i:s')
    ]);
} catch (Exception $e) {
    // Log lỗi nhưng không fail request
    error_log('GraphDB sync error: ' . $e->getMessage());
}
```

---

### **CÁCH 2: Đồng bộ định kỳ (Background Job)**

#### **Tạo script Python: `scripts/sync_mysql_to_graphdb.py`**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script đồng bộ kết quả từ MySQL → GraphDB
Chạy định kỳ (cron job) để đồng bộ dữ liệu mới
"""

import mysql.connector
import requests
from datetime import datetime
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD

# Config
MYSQL_CONFIG = {
    'host': 'localhost',
    'database': 'tinhoc321_quiz',
    'user': 'your_username',
    'password': 'your_password'
}

GRAPHDB_URL = 'http://localhost:7200'
GRAPHDB_REPOSITORY = 'tinhocthcs'

# Namespaces
EDU = Namespace('http://education.vn/ontology#')
DATA = Namespace('http://education.vn/data/')

def get_new_results(since_timestamp=None):
    """Lấy kết quả mới từ MySQL"""
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    if since_timestamp:
        query = """
            SELECT * FROM quiz_results 
            WHERE created_at > %s 
            AND NOT EXISTS (
                SELECT 1 FROM graphdb_sync_log 
                WHERE quiz_result_id = quiz_results.id
            )
            ORDER BY created_at
        """
        cursor.execute(query, (since_timestamp,))
    else:
        # Lần đầu: lấy tất cả
        query = "SELECT * FROM quiz_results ORDER BY created_at"
        cursor.execute(query)
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def create_test_result_ttl(result):
    """Tạo TTL cho TestResult"""
    g = Graph()
    g.bind('edu', EDU)
    g.bind('data', DATA)
    g.bind('rdf', RDF)
    g.bind('xsd', XSD)
    
    student_id = result['student_name'].replace(' ', '_').replace('/', '_')
    test_id = result['quiz_id']
    result_id = f"testresult_{student_id}_{test_id}_{result['id']}"
    
    # TestResult
    result_uri = DATA[result_id]
    g.add((result_uri, RDF.type, EDU.TestResult))
    
    # Score (decimal 0.0-1.0)
    percentage = result['score'] / result['total']
    g.add((result_uri, EDU.score, Literal(percentage, datatype=XSD.decimal)))
    
    # Test
    test_uri = DATA[f"test_{test_id}"]
    g.add((result_uri, EDU.forTest, test_uri))
    
    # Date
    test_date = datetime.fromisoformat(str(result['created_at']))
    g.add((result_uri, EDU.testDate, Literal(test_date, datatype=XSD.dateTime)))
    
    # Student relationship
    student_uri = DATA[f"student_{student_id}"]
    g.add((student_uri, EDU.hasResult, result_uri))
    g.add((student_uri, EDU.takeTest, test_uri))
    
    return g.serialize(format='turtle')

def upload_to_graphdb(ttl_content):
    """Upload TTL vào GraphDB"""
    url = f"{GRAPHDB_URL}/repositories/{GRAPHDB_REPOSITORY}/statements"
    
    response = requests.post(
        url,
        data=ttl_content.encode('utf-8'),
        headers={
            'Content-Type': 'text/turtle'
        },
        timeout=30
    )
    
    response.raise_for_status()
    return response.status_code == 204

def log_sync(result_id):
    """Ghi log đã đồng bộ"""
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Tạo bảng log nếu chưa có
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS graphdb_sync_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                quiz_result_id INT NOT NULL,
                synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_result (quiz_result_id)
            )
        """)
        
        cursor.execute(
            "INSERT INTO graphdb_sync_log (quiz_result_id) VALUES (%s)",
            (result_id,)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def main():
    """Main function"""
    print("🔄 Đang đồng bộ MySQL → GraphDB...")
    
    # Lấy kết quả mới (chưa đồng bộ)
    results = get_new_results()
    
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
            upload_to_graphdb(ttl)
            
            # Ghi log
            log_sync(result['id'])
            
            success_count += 1
            print(f"✅ Đồng bộ thành công: {result['student_name']} - {result['quiz_id']}")
            
        except Exception as e:
            error_count += 1
            print(f"❌ Lỗi đồng bộ {result['id']}: {e}")
    
    print(f"\n📊 Tổng kết: {success_count} thành công, {error_count} lỗi")

if __name__ == '__main__':
    main()
```

#### **Cài đặt dependencies:**

```bash
pip install mysql-connector-python requests rdflib
```

#### **Setup cron job (Linux/Mac):**

```bash
# Chạy mỗi 5 phút
*/5 * * * * cd /path/to/project && python scripts/sync_mysql_to_graphdb.py >> logs/sync.log 2>&1
```

#### **Setup Task Scheduler (Windows):**

```powershell
# Tạo task chạy định kỳ
schtasks /create /tn "Sync MySQL to GraphDB" /tr "python D:\A_DeAnTN\scripts\sync_mysql_to_graphdb.py" /sc minute /mo 5
```

---

### **CÁCH 3: Đồng bộ thủ công**

Sử dụng script Python ở **Cách 2**, nhưng chạy thủ công khi cần:

```bash
python scripts/sync_mysql_to_graphdb.py
```

---

## 📋 KHUYẾN NGHỊ

### **Giai đoạn 1: Development/Testing**

→ Dùng **Cách 3** (đồng bộ thủ công)
- Dễ test và debug
- Không ảnh hưởng production

### **Giai đoạn 2: Production**

→ Dùng **Cách 2** (đồng bộ định kỳ)
- An toàn, không block request
- Có thể retry nếu lỗi

### **Giai đoạn 3: Real-time**

→ Dùng **Cách 1** (real-time) nếu cần dữ liệu cập nhật ngay lập tức

---

## ✅ CHECKLIST TRIỂN KHAI

- [ ] Tạo script đồng bộ (chọn 1 trong 3 cách)
- [ ] Test kết nối MySQL → GraphDB
- [ ] Test tạo TTL từ dữ liệu MySQL
- [ ] Test upload vào GraphDB
- [ ] Setup logging để track lỗi
- [ ] Setup cron job (nếu dùng Cách 2)
- [ ] Verify dữ liệu trong GraphDB sau khi đồng bộ
- [ ] Tạo monitoring để theo dõi đồng bộ

---

## 🔍 VERIFY DỮ LIỆU

Sau khi đồng bộ, kiểm tra trong GraphDB:

```sparql
SELECT ?result ?student ?testId ?score ?testDate
WHERE {
  ?result a <http://education.vn/ontology#TestResult> ;
          <http://education.vn/ontology#score> ?score ;
          <http://education.vn/ontology#forTest> ?testIRI .
  ?testIRI <http://education.vn/ontology#testId> ?testId
  OPTIONAL { ?result <http://education.vn/ontology#testDate> ?testDate }
  ?student <http://education.vn/ontology#hasResult> ?result
}
ORDER BY DESC(?testDate)
LIMIT 20
```

---

**Chọn cách phù hợp và bắt đầu triển khai! 🚀**

