#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
So sánh kết quả giữa GraphDB (SPARQL) và KNN
File: ML_Algorithms/compare_graphdb_vs_knn.py

Chức năng:
1. Chạy cả 2 phương pháp
2. So sánh kết quả phát hiện học sinh yếu
3. So sánh khuyến nghị
4. Tạo báo cáo so sánh chi tiết
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple
from datetime import datetime
import io

# Fix encoding cho Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Thêm path
ml_dir = Path(__file__).parent
sys.path.insert(0, str(ml_dir))

def print_header(text):
    """In header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def load_graphdb_results() -> Dict[str, Any]:
    """Load kết quả từ GraphDB"""
    result_file = ml_dir / "graphdb_results.json"
    
    if not result_file.exists():
        print(f"⚠️  Không tìm thấy file: {result_file}")
        print("💡 Chạy graphdb_detection_recommendation.py trước")
        return None
    
    with open(result_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_knn_results() -> Dict[str, Any]:
    """Load kết quả từ KNN"""
    # Tìm file KNN results (có thể là từ knn_student_analysis.py)
    result_file = ml_dir / "knn_results.json"
    
    if not result_file.exists():
        # Thử tìm file trong KG_Design
        kg_result_file = ml_dir.parent / "KG_Design" / "knn_results.json"
        if kg_result_file.exists():
            result_file = kg_result_file
        else:
            print(f"⚠️  Không tìm thấy file KNN results")
            print("💡 Chạy knn_student_analysis.py trước")
            return None
    
    with open(result_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_weak_student_key(weak_student: Dict) -> str:
    """Tạo key chuẩn hóa để so sánh"""
    student_id = weak_student.get('student_id', '')
    skill_id = weak_student.get('skill_id', '')
    return f"{student_id}::{skill_id}"

def compare_weak_students(graphdb_results: Dict, knn_results: Dict) -> Dict[str, Any]:
    """So sánh kết quả phát hiện học sinh yếu"""
    
    graphdb_weak = graphdb_results.get('weak_students', [])
    knn_weak = knn_results.get('weak_students', [])
    
    # Tạo sets để so sánh
    graphdb_set = {normalize_weak_student_key(ws) for ws in graphdb_weak}
    knn_set = {normalize_weak_student_key(ws) for ws in knn_weak}
    
    # Tính các metrics
    total_graphdb = len(graphdb_set)
    total_knn = len(knn_set)
    
    # Giao nhau (cả 2 phương pháp đều phát hiện)
    intersection = graphdb_set & knn_set
    common_count = len(intersection)
    
    # Chỉ GraphDB phát hiện
    only_graphdb = graphdb_set - knn_set
    only_graphdb_count = len(only_graphdb)
    
    # Chỉ KNN phát hiện
    only_knn = knn_set - graphdb_set
    only_knn_count = len(only_knn)
    
    # Hợp (tất cả phát hiện)
    union = graphdb_set | knn_set
    union_count = len(union)
    
    # Jaccard Similarity
    jaccard = common_count / union_count if union_count > 0 else 0
    
    # Precision, Recall cho từng phương pháp
    precision_graphdb = common_count / total_graphdb if total_graphdb > 0 else 0
    recall_graphdb = common_count / total_knn if total_knn > 0 else 0
    
    precision_knn = common_count / total_knn if total_knn > 0 else 0
    recall_knn = common_count / total_graphdb if total_graphdb > 0 else 0
    
    # F1 Score
    f1_graphdb = 2 * (precision_graphdb * recall_graphdb) / (precision_graphdb + recall_graphdb) if (precision_graphdb + recall_graphdb) > 0 else 0
    f1_knn = 2 * (precision_knn * recall_knn) / (precision_knn + recall_knn) if (precision_knn + recall_knn) > 0 else 0
    
    comparison = {
        'graphdb_total': total_graphdb,
        'knn_total': total_knn,
        'common': common_count,
        'only_graphdb': only_graphdb_count,
        'only_knn': only_knn_count,
        'union': union_count,
        'jaccard_similarity': jaccard,
        'graphdb_metrics': {
            'precision': precision_graphdb,
            'recall': recall_graphdb,
            'f1_score': f1_graphdb
        },
        'knn_metrics': {
            'precision': precision_knn,
            'recall': recall_knn,
            'f1_score': f1_knn
        },
        'common_items': list(intersection)[:10],  # Top 10
        'only_graphdb_items': list(only_graphdb)[:10],
        'only_knn_items': list(only_knn)[:10]
    }
    
    return comparison

def compare_recommendations(graphdb_results: Dict, knn_results: Dict) -> Dict[str, Any]:
    """So sánh khuyến nghị"""
    
    graphdb_recs = graphdb_results.get('recommendations', [])
    knn_recs = knn_results.get('recommendations', [])
    
    # Nhóm theo học sinh
    graphdb_by_student = {}
    knn_by_student = {}
    
    for rec in graphdb_recs:
        student_id = rec.get('student_id', '')
        if student_id not in graphdb_by_student:
            graphdb_by_student[student_id] = []
        graphdb_by_student[student_id].append(rec)
    
    for rec in knn_recs:
        student_id = rec.get('student_id', '')
        if student_id not in knn_by_student:
            knn_by_student[student_id] = []
        knn_by_student[student_id].append(rec)
    
    # So sánh số lượng khuyến nghị
    total_graphdb = len(graphdb_recs)
    total_knn = len(knn_recs)
    
    # Số học sinh có khuyến nghị
    students_graphdb = len(graphdb_by_student)
    students_knn = len(knn_by_student)
    
    # Học sinh có khuyến nghị ở cả 2 phương pháp
    common_students = set(graphdb_by_student.keys()) & set(knn_by_student.keys())
    
    comparison = {
        'graphdb_total': total_graphdb,
        'knn_total': total_knn,
        'students_with_recs_graphdb': students_graphdb,
        'students_with_recs_knn': students_knn,
        'common_students': len(common_students),
        'avg_recs_per_student_graphdb': total_graphdb / students_graphdb if students_graphdb > 0 else 0,
        'avg_recs_per_student_knn': total_knn / students_knn if students_knn > 0 else 0
    }
    
    return comparison

def analyze_score_distribution(graphdb_results: Dict, knn_results: Dict) -> Dict[str, Any]:
    """Phân tích phân bố điểm số"""
    
    graphdb_scores = [ws.get('avg_score', 0) for ws in graphdb_results.get('weak_students', [])]
    knn_scores = [ws.get('avg_score', 0) for ws in knn_results.get('weak_students', [])]
    
    if not graphdb_scores and not knn_scores:
        return {}
    
    def calc_stats(scores):
        if not scores:
            return {}
        return {
            'min': min(scores),
            'max': max(scores),
            'mean': sum(scores) / len(scores),
            'count': len(scores)
        }
    
    return {
        'graphdb': calc_stats(graphdb_scores),
        'knn': calc_stats(knn_scores)
    }

def generate_comparison_report(graphdb_results: Dict, knn_results: Dict) -> Dict[str, Any]:
    """Tạo báo cáo so sánh tổng hợp"""
    
    print_header("📊 SO SÁNH KẾT QUẢ")
    
    # So sánh phát hiện học sinh yếu
    weak_comparison = compare_weak_students(graphdb_results, knn_results)
    
    # So sánh khuyến nghị
    rec_comparison = compare_recommendations(graphdb_results, knn_results)
    
    # Phân tích phân bố điểm
    score_dist = analyze_score_distribution(graphdb_results, knn_results)
    
    # Tạo report
    report = {
        'timestamp': datetime.now().isoformat(),
        'comparison': {
            'weak_students': weak_comparison,
            'recommendations': rec_comparison,
            'score_distribution': score_dist
        },
        'methods': {
            'graphdb': {
                'method': 'GraphDB SPARQL',
                'description': 'Sử dụng truy vấn SPARQL trên Knowledge Graph',
                'advantages': [
                    'Tận dụng cấu trúc liên kết của KG',
                    'Không cần training data',
                    'Giải thích được (explainable)',
                    'Truy vấn trực tiếp trên dữ liệu'
                ],
                'disadvantages': [
                    'Phụ thuộc vào chất lượng KG',
                    'Logic truy vấn có thể phức tạp',
                    'Khó tối ưu hiệu năng với dữ liệu lớn'
                ]
            },
            'knn': {
                'method': 'K-Nearest Neighbors',
                'description': 'Machine Learning dựa trên tương đồng học sinh',
                'advantages': [
                    'Học từ dữ liệu lịch sử',
                    'Phát hiện patterns phức tạp',
                    'Tự động điều chỉnh theo dữ liệu mới',
                    'Có thể xử lý nhiều features'
                ],
                'disadvantages': [
                    'Cần dữ liệu training đủ lớn',
                    'Black box (khó giải thích)',
                    'Phụ thuộc vào quality của features',
                    'Cần tuning hyperparameters'
                ]
            }
        }
    }
    
    return report

def print_comparison_summary(report: Dict):
    """In tóm tắt so sánh"""
    
    comp = report['comparison']
    weak = comp['weak_students']
    recs = comp['recommendations']
    
    print_header("📋 TÓM TẮT SO SÁNH")
    
    print("🔍 PHÁT HIỆN HỌC SINH YẾU:")
    print("-" * 70)
    print(f"  GraphDB phát hiện:     {weak['graphdb_total']:4d} học sinh")
    print(f"  KNN phát hiện:         {weak['knn_total']:4d} học sinh")
    print(f"  Cả 2 phát hiện:        {weak['common']:4d} học sinh")
    print(f"  Chỉ GraphDB:           {weak['only_graphdb']:4d} học sinh")
    print(f"  Chỉ KNN:               {weak['only_knn']:4d} học sinh")
    print(f"  Jaccard Similarity:    {weak['jaccard_similarity']:.2%}")
    
    print("\n📊 METRICS:")
    print("-" * 70)
    print("  GraphDB:")
    print(f"    Precision:  {weak['graphdb_metrics']['precision']:.2%}")
    print(f"    Recall:     {weak['graphdb_metrics']['recall']:.2%}")
    print(f"    F1 Score:   {weak['graphdb_metrics']['f1_score']:.2%}")
    print("  KNN:")
    print(f"    Precision:  {weak['knn_metrics']['precision']:.2%}")
    print(f"    Recall:     {weak['knn_metrics']['recall']:.2%}")
    print(f"    F1 Score:   {weak['knn_metrics']['f1_score']:.2%}")
    
    print("\n💡 KHUYẾN NGHỊ:")
    print("-" * 70)
    print(f"  GraphDB:               {recs['graphdb_total']:4d} khuyến nghị")
    print(f"  KNN:                   {recs['knn_total']:4d} khuyến nghị")
    print(f"  Học sinh có khuyến nghị (GraphDB): {recs['students_with_recs_graphdb']:4d}")
    print(f"  Học sinh có khuyến nghị (KNN):     {recs['students_with_recs_knn']:4d}")
    print(f"  TB khuyến nghị/học sinh (GraphDB): {recs['avg_recs_per_student_graphdb']:.1f}")
    print(f"  TB khuyến nghị/học sinh (KNN):     {recs['avg_recs_per_student_knn']:.1f}")

def save_report(report: Dict, output_file: str = "comparison_report.json"):
    """Lưu báo cáo"""
    output_path = ml_dir / output_file
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Đã lưu báo cáo: {output_path}")
    
    return output_path

def main():
    """Hàm chính"""
    print_header("📊 SO SÁNH GRAPHDB vs KNN")
    
    print("Bước 1: Load kết quả GraphDB...")
    graphdb_results = load_graphdb_results()
    
    if not graphdb_results:
        print("\n❌ Không thể load kết quả GraphDB")
        print("💡 Chạy: python graphdb_detection_recommendation.py")
        return
    
    print("✅ Đã load kết quả GraphDB")
    print(f"   - Học sinh yếu: {len(graphdb_results.get('weak_students', []))}")
    print(f"   - Khuyến nghị: {len(graphdb_results.get('recommendations', []))}")
    
    print("\nBước 2: Load kết quả KNN...")
    knn_results = load_knn_results()
    
    if not knn_results:
        print("\n❌ Không thể load kết quả KNN")
        print("💡 Chạy: python knn_student_analysis.py")
        return
    
    print("✅ Đã load kết quả KNN")
    print(f"   - Học sinh yếu: {len(knn_results.get('weak_students', []))}")
    print(f"   - Khuyến nghị: {len(knn_results.get('recommendations', []))}")
    
    print("\nBước 3: So sánh kết quả...")
    report = generate_comparison_report(graphdb_results, knn_results)
    
    print("\nBước 4: Hiển thị tóm tắt...")
    print_comparison_summary(report)
    
    print("\nBước 5: Lưu báo cáo...")
    save_report(report)
    
    print("\n" + "=" * 70)
    print("✅ HOÀN THÀNH SO SÁNH!")
    print("=" * 70)
    print("\n💡 Xem chi tiết trong file: comparison_report.json")

if __name__ == '__main__':
    main()

