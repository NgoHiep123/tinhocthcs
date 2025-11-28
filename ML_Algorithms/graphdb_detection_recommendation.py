#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phát hiện học sinh yếu và khuyến nghị sử dụng GraphDB (SPARQL)
File: ML_Algorithms/graphdb_detection_recommendation.py

Phương pháp:
- Sử dụng SPARQL queries để phân tích dữ liệu trong GraphDB
- Không cần Machine Learning, dựa trên logic truy vấn
- So sánh với phương pháp KNN
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
from datetime import datetime
import io

# Fix encoding cho Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Thêm thư mục KG_Design vào path
kg_design_dir = Path(__file__).parent.parent / "KG_Design"
sys.path.insert(0, str(kg_design_dir))

try:
    from query_graphdb import GraphDBClient
    USE_GRAPHD_B = True
except ImportError:
    print("⚠️  Không tìm thấy GraphDBClient, sẽ dùng file TTL local")
    USE_GRAPHD_B = False

# Ngưỡng để xác định học sinh yếu
WEAK_THRESHOLD = 5.0  # Điểm dưới 5.0 là yếu

def print_header(text):
    """In header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def detect_weak_students_graphdb(client: GraphDBClient = None, use_file: bool = False) -> List[Dict[str, Any]]:
    """
    Phát hiện học sinh yếu sử dụng GraphDB SPARQL
    
    Phương pháp:
    1. Truy vấn tất cả học sinh và điểm mastery của họ
    2. Tính điểm trung bình cho mỗi skill/chủ đề
    3. Xác định học sinh yếu (điểm < threshold)
    
    Returns:
        List of dict: [{'student_id': '...', 'skill_id': '...', 'avg_score': 4.5, ...}]
    """
    print("🔍 Phát hiện học sinh yếu bằng GraphDB SPARQL...")
    
    weak_students = []
    
    if use_file or not USE_GRAPHD_B or client is None:
        # Sử dụng file TTL local
        return detect_weak_students_from_file()
    
    # SPARQL query để tìm học sinh yếu
    query = """
    PREFIX ex: <https://example.org/kg/>
    PREFIX edu: <https://example.org/edu#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    SELECT ?student ?studentId ?skill ?skillId ?skillName ?avgScore (COUNT(?mastery) as ?attemptCount)
    WHERE {
        ?mastery a edu:Mastery .
        ?mastery edu:student ?student .
        ?mastery edu:skill ?skill .
        ?mastery edu:score ?score .
        
        ?student edu:studentId ?studentId .
        ?skill edu:skillId ?skillId .
        OPTIONAL { ?skill edu:name ?skillName . }
        
        # Tính điểm trung bình cho mỗi học sinh ở mỗi skill
        {
            SELECT ?student ?skill (AVG(?score) as ?avgScore)
            WHERE {
                ?mastery a edu:Mastery .
                ?mastery edu:student ?student .
                ?mastery edu:skill ?skill .
                ?mastery edu:score ?score .
            }
            GROUP BY ?student ?skill
        }
        
        # Chỉ lấy những học sinh có điểm trung bình < 5.0
        FILTER(?avgScore < 5.0)
    }
    GROUP BY ?student ?studentId ?skill ?skillId ?skillName ?avgScore
    ORDER BY ?avgScore ?studentId
    """
    
    try:
        results = client.query(query)
        
        print(f"📊 Tìm thấy {len(results)} kết quả học sinh yếu")
        
        for row in results:
            student_id = row.get('studentId', {}).get('value', '')
            skill_id = row.get('skillId', {}).get('value', '')
            skill_name = row.get('skillName', {}).get('value', '')
            avg_score = float(row.get('avgScore', {}).get('value', 0))
            attempt_count = int(row.get('attemptCount', {}).get('value', 0))
            
            weak_students.append({
                'student_id': student_id,
                'skill_id': skill_id,
                'skill_name': skill_name,
                'avg_score': avg_score,
                'attempt_count': attempt_count,
                'method': 'GraphDB'
            })
        
        print(f"✅ Phát hiện {len(weak_students)} học sinh yếu")
        
    except Exception as e:
        print(f"❌ Lỗi khi truy vấn GraphDB: {e}")
        print("💡 Chuyển sang dùng file TTL local...")
        return detect_weak_students_from_file()
    
    return weak_students

def detect_weak_students_from_file() -> List[Dict[str, Any]]:
    """Phát hiện học sinh yếu từ file TTL local"""
    print("📖 Đang đọc từ file TTL local...")
    
    from rdflib import Graph, Namespace
    from rdflib.namespace import RDF
    
    EX = Namespace("https://example.org/kg/")
    EDU = Namespace("https://example.org/edu#")
    
    # Tìm file TTL
    mastery_file = kg_design_dir / "grade6" / "out" / "mastery.ttl"
    
    if not mastery_file.exists():
        print(f"❌ Không tìm thấy file: {mastery_file}")
        return []
    
    # Đọc KG
    g = Graph()
    g.parse(str(mastery_file), format='turtle')
    
    # Tính điểm trung bình cho mỗi học sinh ở mỗi skill
    student_skill_scores = {}
    
    for s, p, o in g.triples((None, None, None)):
        if p == RDF.type and o == EDU.Mastery:
            mastery_node = s
            
            # Lấy student, skill, score
            student = None
            skill = None
            score = None
            
            for s2, p2, o2 in g.triples((mastery_node, None, None)):
                if p2 == EDU.student:
                    student = str(o2).split('/')[-1]  # Lấy ID từ URI
                elif p2 == EDU.skill:
                    skill = str(o2).split('/')[-1]
                elif p2 == EDU.score:
                    score = float(o2)
            
            if student and skill and score is not None:
                key = (student, skill)
                if key not in student_skill_scores:
                    student_skill_scores[key] = []
                student_skill_scores[key].append(score)
    
    # Tính trung bình và tìm học sinh yếu
    weak_students = []
    
    for (student_id, skill_id), scores in student_skill_scores.items():
        avg_score = sum(scores) / len(scores)
        
        if avg_score < WEAK_THRESHOLD:
            weak_students.append({
                'student_id': student_id,
                'skill_id': skill_id,
                'skill_name': skill_id.replace('_', ' '),
                'avg_score': avg_score,
                'attempt_count': len(scores),
                'method': 'GraphDB (File)'
            })
    
    print(f"✅ Phát hiện {len(weak_students)} học sinh yếu từ file")
    
    return weak_students

def recommend_resources_graphdb(weak_students: List[Dict], client: GraphDBClient = None, use_file: bool = False) -> List[Dict[str, Any]]:
    """
    Khuyến nghị tài nguyên học tập sử dụng GraphDB SPARQL
    
    Phương pháp:
    1. Với mỗi học sinh yếu ở skill X
    2. Tìm các resource liên quan đến skill X
    3. Tìm các skill tiên quyết nếu cần
    4. Trả về danh sách resource được khuyến nghị
    
    Returns:
        List of recommendations
    """
    print("\n💡 Đang tạo khuyến nghị bằng GraphDB SPARQL...")
    
    recommendations = []
    
    if use_file or not USE_GRAPHD_B or client is None:
        return recommend_resources_from_file(weak_students)
    
    for weak_student in weak_students[:10]:  # Giới hạn 10 học sinh để test
        student_id = weak_student['student_id']
        skill_id = weak_student['skill_id']
        
        # SPARQL query để tìm resource cho skill
        query = f"""
        PREFIX ex: <https://example.org/kg/>
        PREFIX edu: <https://example.org/edu#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        
        SELECT ?resource ?resourceId ?title ?url ?coverage
        WHERE {{
            # Tìm resource cho skill này
            ?resource edu:COVERS ?skill .
            ?resource edu:resId ?resourceId .
            ?resource edu:title ?title .
            OPTIONAL {{ ?resource edu:url ?url . }}
            OPTIONAL {{ ?resource edu:coverage ?coverage . }}
            
            ?skill edu:skillId "{skill_id}" .
        }}
        ORDER BY DESC(?coverage)
        LIMIT 5
        """
        
        try:
            results = client.query(query)
            
            for row in results:
                resource_id = row.get('resourceId', {}).get('value', '')
                title = row.get('title', {}).get('value', '')
                url = row.get('url', {}).get('value', '')
                coverage = float(row.get('coverage', {}).get('value', 0.5))
                
                recommendations.append({
                    'student_id': student_id,
                    'skill_id': skill_id,
                    'resource_id': resource_id,
                    'resource_title': title,
                    'resource_url': url,
                    'coverage': coverage,
                    'method': 'GraphDB'
                })
                
        except Exception as e:
            print(f"⚠️  Lỗi khi tìm resource cho {student_id}: {e}")
            continue
    
    print(f"✅ Đã tạo {len(recommendations)} khuyến nghị")
    
    return recommendations

def recommend_resources_from_file(weak_students: List[Dict]) -> List[Dict[str, Any]]:
    """Khuyến nghị từ file TTL local"""
    print("📖 Đang đọc từ file TTL local...")
    
    from rdflib import Graph, Namespace
    from rdflib.namespace import RDF
    
    EX = Namespace("https://example.org/kg/")
    EDU = Namespace("https://example.org/edu#")
    
    # Đọc file resource_skill.ttl
    resource_skill_file = kg_design_dir / "grade6" / "out" / "resource_skill.ttl"
    resources_file = kg_design_dir / "grade6" / "out" / "resources.ttl"
    
    if not resource_skill_file.exists() or not resources_file.exists():
        print(f"❌ Không tìm thấy file resource")
        return []
    
    # Đọc KG
    g = Graph()
    g.parse(str(resource_skill_file), format='turtle')
    g.parse(str(resources_file), format='turtle')
    
    recommendations = []
    
    # Với mỗi học sinh yếu, tìm resource cho skill đó
    for weak_student in weak_students[:10]:  # Giới hạn
        skill_id = weak_student['skill_id']
        student_id = weak_student['student_id']
        
        # Tìm resource cho skill
        skill_uri = EX[f"skill/{skill_id}"]
        
        for s, p, o in g.triples((None, EDU.COVERS, skill_uri)):
            resource_uri = s
            
            # Lấy thông tin resource
            resource_id = None
            title = None
            url = None
            coverage = 0.5
            
            for s2, p2, o2 in g.triples((resource_uri, None, None)):
                if p2 == EDU.resId:
                    resource_id = str(o2)
                elif p2 == EDU.title:
                    title = str(o2)
                elif p2 == EDU.url:
                    url = str(o2)
                elif p2 == EDU.coverage:
                    coverage = float(o2)
            
            if resource_id:
                recommendations.append({
                    'student_id': student_id,
                    'skill_id': skill_id,
                    'resource_id': resource_id,
                    'resource_title': title or resource_id,
                    'resource_url': url or '',
                    'coverage': coverage,
                    'method': 'GraphDB (File)'
                })
    
    print(f"✅ Đã tạo {len(recommendations)} khuyến nghị từ file")
    
    return recommendations

def save_results(weak_students: List[Dict], recommendations: List[Dict], output_file: str = "graphdb_results.json"):
    """Lưu kết quả ra file JSON"""
    output_path = Path(__file__).parent / output_file
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'GraphDB SPARQL',
        'weak_threshold': WEAK_THRESHOLD,
        'statistics': {
            'total_weak_students': len(weak_students),
            'total_recommendations': len(recommendations),
            'unique_students': len(set(s['student_id'] for s in weak_students)),
            'unique_skills': len(set(s['skill_id'] for s in weak_students))
        },
        'weak_students': weak_students,
        'recommendations': recommendations
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Đã lưu kết quả: {output_path}")
    
    return output_path

def main():
    """Hàm chính"""
    print_header("🔍 PHÁT HIỆN HỌC SINH YẾU VÀ KHUYẾN NGHỊ - GRAPHDB")
    
    # Khởi tạo GraphDB client
    client = None
    use_file = False
    
    if USE_GRAPHD_B:
        try:
            client = GraphDBClient()
            if client.test_connection():
                print("✅ Kết nối GraphDB thành công!")
            else:
                print("⚠️  Không thể kết nối GraphDB, dùng file TTL local")
                use_file = True
        except Exception as e:
            print(f"⚠️  Lỗi kết nối GraphDB: {e}")
            print("💡 Chuyển sang dùng file TTL local...")
            use_file = True
    else:
        use_file = True
    
    # Phát hiện học sinh yếu
    weak_students = detect_weak_students_graphdb(client, use_file)
    
    if not weak_students:
        print("\n⚠️  Không tìm thấy học sinh yếu nào!")
        return
    
    # Hiển thị top 10 học sinh yếu
    print("\n📋 TOP 10 HỌC SINH YẾU:")
    print("-" * 70)
    for i, ws in enumerate(sorted(weak_students, key=lambda x: x['avg_score'])[:10], 1):
        print(f"{i:2d}. Học sinh: {ws['student_id']:15s} | "
              f"Skill: {ws['skill_id']:30s} | "
              f"Điểm TB: {ws['avg_score']:.2f}")
    
    # Tạo khuyến nghị
    recommendations = recommend_resources_graphdb(weak_students, client, use_file)
    
    # Lưu kết quả
    save_results(weak_students, recommendations)
    
    print("\n" + "=" * 70)
    print("✅ HOÀN THÀNH!")
    print("=" * 70)
    print("\n💡 Bước tiếp theo:")
    print("   1. So sánh với kết quả KNN: python compare_methods.py")
    print("   2. Xem chi tiết: graphdb_results.json")

if __name__ == '__main__':
    main()

