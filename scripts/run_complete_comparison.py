#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script chạy đầy đủ: Export teachers, GraphDB detection, KNN, và so sánh
File: scripts/run_complete_comparison.py
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

def print_step(num, text):
    """In bước"""
    print(f"\n[{num}] {text}")
    print("-" * 70)

def run_script(script_path, description):
    """Chạy một script Python"""
    print(f"🔄 {description}...")
    print(f"   Script: {script_path.name}")
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=script_path.parent,
            capture_output=False
        )
        
        if result.returncode == 0:
            print(f"✅ {description} thành công!")
            return True
        else:
            print(f"❌ {description} thất bại (exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def main():
    """Hàm chính"""
    print_header("🚀 CHẠY SO SÁNH GRAPHDB vs KNN")
    
    project_root = Path(__file__).parent.parent
    
    print("Script này sẽ thực hiện các bước sau:")
    print("  1. Export giáo viên và phân công → .ttl")
    print("  2. Phát hiện học sinh yếu bằng GraphDB")
    print("  3. Phát hiện học sinh yếu bằng KNN")
    print("  4. So sánh kết quả")
    
    input("\nNhấn Enter để bắt đầu...")
    
    results = {}
    
    # Bước 1: Export teachers
    print_step(1, "EXPORT GIÁO VIÊN VÀ PHÂN CÔNG")
    export_script = project_root / "KG_Design" / "grade6" / "export_teachers_assignments.py"
    results['export_teachers'] = run_script(export_script, "Export teachers và assignments")
    
    # Bước 2: GraphDB Detection
    print_step(2, "PHÁT HIỆN HỌC SINH YẾU - GRAPHDB")
    graphdb_script = project_root / "ML_Algorithms" / "graphdb_detection_recommendation.py"
    results['graphdb_detection'] = run_script(graphdb_script, "GraphDB detection và recommendation")
    
    # Bước 3: KNN Analysis
    print_step(3, "PHÁT HIỆN HỌC SINH YẾU - KNN")
    knn_script = project_root / "ML_Algorithms" / "knn_student_analysis.py"
    results['knn_analysis'] = run_script(knn_script, "KNN student analysis")
    
    # Bước 4: Compare
    print_step(4, "SO SÁNH KẾT QUẢ")
    compare_script = project_root / "ML_Algorithms" / "compare_graphdb_vs_knn.py"
    results['comparison'] = run_script(compare_script, "So sánh GraphDB vs KNN")
    
    # Tổng kết
    print_header("📊 TỔNG KẾT")
    
    total = len(results)
    completed = sum(1 for v in results.values() if v)
    
    print(f"✅ Hoàn thành: {completed}/{total} bước\n")
    
    for step, success in results.items():
        status = "✅" if success else "❌"
        step_name = step.replace('_', ' ').title()
        print(f"  {status} {step_name}")
    
    print("\n" + "=" * 70)
    
    if completed == total:
        print("🎉 TẤT CẢ CÁC BƯỚC ĐÃ HOÀN THÀNH!")
        print("\n💡 Xem kết quả:")
        print("   - graphdb_results.json")
        print("   - knn_results.json")
        print("   - comparison_report.json")
    else:
        print("⚠️  MỘT SỐ BƯỚC CHƯA HOÀN THÀNH")
        print("💡 Vui lòng kiểm tra lại các bước thất bại")
    
    print("=" * 70 + "\n")

if __name__ == '__main__':
    main()

