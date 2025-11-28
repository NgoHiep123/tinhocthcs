#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script chạy pipeline Machine Learning hoàn chỉnh
File: scripts/run_ml_pipeline.py

Chức năng:
1. Chạy KNN để phát hiện học sinh yếu
2. Chạy PPR để gợi ý bài học
3. Cập nhật KG với kết quả
4. Tạo báo cáo kết quả
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import io
from datetime import datetime

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
    """In bước hiện tại"""
    print(f"\n[{num}] {text}")
    print("-" * 70)

def check_prerequisites():
    """Kiểm tra điều kiện tiên quyết"""
    print_step(0, "KIỂM TRA ĐIỀU KIỆN TIÊN QUYẾT")
    
    checks = {}
    
    # 1. Kiểm tra file KG
    kg_file = Path("KG_Design/kg_grade7.ttl")
    checks['kg_file'] = kg_file.exists()
    print(f"{'✅' if checks['kg_file'] else '❌'} File KG: {kg_file}")
    
    # 2. Kiểm tra script KNN
    knn_script = Path("ML_Algorithms/knn_student_analysis.py")
    checks['knn_script'] = knn_script.exists()
    print(f"{'✅' if checks['knn_script'] else '❌'} Script KNN: {knn_script}")
    
    # 3. Kiểm tra script PPR
    ppr_script = Path("ML_Algorithms/ppr_recommendation.py")
    checks['ppr_script'] = ppr_script.exists()
    print(f"{'✅' if checks['ppr_script'] else '❌'} Script PPR: {ppr_script}")
    
    # 4. Kiểm tra dependencies
    try:
        import sklearn
        import networkx
        import rdflib
        checks['dependencies'] = True
        print("✅ Dependencies (sklearn, networkx, rdflib)")
    except ImportError as e:
        checks['dependencies'] = False
        print(f"❌ Thiếu dependency: {e}")
    
    all_ok = all(checks.values())
    
    if not all_ok:
        print("\n⚠️  Một số điều kiện chưa đủ!")
        print("💡 Vui lòng:")
        if not checks['kg_file']:
            print("   - Chạy build_kg_grade7.py để tạo KG")
        if not checks['dependencies']:
            print("   - Cài đặt: pip install -r requirements.txt")
    
    return all_ok

def run_knn():
    """Chạy thuật toán KNN"""
    print_step(1, "CHẠY THUẬT TOÁN KNN")
    
    knn_script = Path("ML_Algorithms/knn_student_analysis.py")
    
    print(f"🤖 Đang chạy KNN: {knn_script.name}")
    print("   (Phát hiện học sinh yếu ở các chủ đề)")
    
    try:
        result = subprocess.run(
            [sys.executable, str(knn_script)],
            cwd=knn_script.parent,
            capture_output=False  # Hiển thị output trực tiếp
        )
        
        if result.returncode == 0:
            print("\n✅ KNN hoàn thành!")
            
            # Kiểm tra file output
            output_file = Path("KG_Design/kg_grade7_with_knn.ttl")
            if output_file.exists():
                print(f"✅ File output: {output_file}")
            else:
                print(f"⚠️  Không tìm thấy file output: {output_file}")
            
            return True
        else:
            print(f"\n❌ KNN thất bại (exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"\n❌ Lỗi khi chạy KNN: {e}")
        return False

def run_ppr():
    """Chạy thuật toán PPR"""
    print_step(2, "CHẠY THUẬT TOÁN PPR")
    
    ppr_script = Path("ML_Algorithms/ppr_recommendation.py")
    
    # Kiểm tra file input
    input_file = Path("KG_Design/kg_grade7_with_knn.ttl")
    if not input_file.exists():
        print(f"⚠️  Không tìm thấy file input: {input_file}")
        print("💡 Đảm bảo đã chạy KNN trước")
        input_file = Path("KG_Design/kg_grade7.ttl")
        if not input_file.exists():
            print(f"❌ Không tìm thấy file KG nào!")
            return False
    
    print(f"🤖 Đang chạy PPR: {ppr_script.name}")
    print(f"   Input: {input_file.name}")
    print("   (Gợi ý bài học cho học sinh yếu)")
    
    try:
        result = subprocess.run(
            [sys.executable, str(ppr_script)],
            cwd=ppr_script.parent,
            capture_output=False
        )
        
        if result.returncode == 0:
            print("\n✅ PPR hoàn thành!")
            
            # Kiểm tra file output
            output_file = Path("KG_Design/kg_grade7_with_ppr.ttl")
            if output_file.exists():
                print(f"✅ File output: {output_file}")
            else:
                print(f"⚠️  Không tìm thấy file output: {output_file}")
            
            return True
        else:
            print(f"\n❌ PPR thất bại (exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"\n❌ Lỗi khi chạy PPR: {e}")
        return False

def generate_report(results):
    """Tạo báo cáo kết quả"""
    print_step(3, "TẠO BÁO CÁO")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "pipeline": "ML Pipeline (KNN + PPR)",
        "results": {
            "knn": {
                "status": "success" if results['knn'] else "failed",
                "output_file": "KG_Design/kg_grade7_with_knn.ttl" if Path("KG_Design/kg_grade7_with_knn.ttl").exists() else None
            },
            "ppr": {
                "status": "success" if results['ppr'] else "failed",
                "output_file": "KG_Design/kg_grade7_with_ppr.ttl" if Path("KG_Design/kg_grade7_with_ppr.ttl").exists() else None
            }
        },
        "summary": {
            "total_steps": 2,
            "successful_steps": sum(1 for v in [results['knn'], results['ppr']] if v),
            "failed_steps": sum(1 for v in [results['knn'], results['ppr']] if not v)
        }
    }
    
    report_file = Path("ML_PIPELINE_REPORT.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Đã lưu báo cáo: {report_file}")
    
    return report

def main():
    """Hàm chính"""
    print_header("🤖 CHẠY PIPELINE MACHINE LEARNING")
    
    print("Pipeline này sẽ thực hiện:")
    print("  1. KNN - Phát hiện học sinh yếu")
    print("  2. PPR - Gợi ý bài học")
    print("  3. Tạo báo cáo kết quả")
    
    input("\nNhấn Enter để bắt đầu...")
    
    # Kiểm tra điều kiện
    if not check_prerequisites():
        print("\n❌ Điều kiện tiên quyết chưa đủ, dừng pipeline")
        return
    
    results = {}
    
    # Chạy KNN
    results['knn'] = run_knn()
    
    # Chạy PPR (chỉ khi KNN thành công)
    if results['knn']:
        results['ppr'] = run_ppr()
    else:
        print("\n⏭️  Bỏ qua PPR (KNN chưa thành công)")
        results['ppr'] = False
    
    # Tạo báo cáo
    report = generate_report(results)
    
    # Tổng kết
    print_header("📊 TỔNG KẾT")
    
    total = 2
    completed = sum(1 for k in ['knn', 'ppr'] if results.get(k, False))
    
    print(f"✅ Hoàn thành: {completed}/{total} bước\n")
    
    for step, success in results.items():
        status = "✅" if success else "❌"
        step_name = "KNN" if step == 'knn' else "PPR"
        print(f"  {status} {step_name}")
    
    print("\n" + "=" * 70)
    
    if completed == total:
        print("🎉 PIPELINE HOÀN THÀNH!")
        print("\n💡 Bước tiếp theo:")
        print("   1. Import file KG mới vào GraphDB (nếu chưa)")
        print("   2. Kiểm tra kết quả trong GraphDB")
        print("   3. Cập nhật Dashboard để hiển thị gợi ý")
    else:
        print("⚠️  PIPELINE CHƯA HOÀN THÀNH HOÀN TOÀN")
        print("💡 Vui lòng kiểm tra lại các bước thất bại")
    
    print("=" * 70 + "\n")

if __name__ == '__main__':
    main()

