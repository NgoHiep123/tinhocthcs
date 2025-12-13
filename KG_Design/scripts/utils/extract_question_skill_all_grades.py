"""
Script extract question_skill mapping từ tất cả Bai_tap_Tin_*/ (Khối 6, 7, 8, 9)
Tạo/cập nhật file question_skill.csv với đầy đủ tất cả câu hỏi
"""

import csv
import os
from pathlib import Path
from collections import OrderedDict

# Đường dẫn
ROOT = Path(__file__).resolve().parent.parent.parent.parent  # D:\A_DeAnTN
CSV_DIR = ROOT / "KG_Design" / "csv"
OUTPUT_FILE = CSV_DIR / "question_skill_all_grades.csv"

# Định nghĩa các thư mục và file CSV
GRADE_CONFIGS = {
    6: {
        "dir": ROOT / "Bai_tap_Tin_6",
        "files": [
            "K6_question_A_full.csv",
            "K6_question_B_full.csv",
            "K6_question_C_full.csv",
            "K6_question_D_full.csv",
            "K6_question_E_full.csv",
            "K6_question_F_full.csv",
        ]
    },
    7: {
        "dir": ROOT / "Bai_tap_Tin_7",
        "files": [
            "K7_question_A_full.csv",
            "K7_question_B_full.csv",
            "K7_question_D_full.csv",
            "K7_question_E_full.csv",
            "K7_question_F_full.csv",
        ]
    },
    8: {
        "dir": ROOT / "Bai_tap_Tin_8",
        "files": [
            "K8_question_A_full.csv",
            "K8_question_C_full.csv",
            "K8_question_D_full.csv",
            "K8_question_E1_full.csv",
            "K8_question_E2_full.csv",
            "K8_question_F_full.csv",
            "K8_question_G_full.csv",
        ]
    },
    9: {
        "dir": ROOT / "Bai_tap_Tin_9",
        "files": [
            "K9_question_Bai_1_full.csv",
            "K9_question_Bai_2_full.csv",
            "K9_question_Bai_3_full.csv",
            "K9_question_Bai_4_full.csv",
            "K9_question_Bai_5_full.csv",
            "K9_question_Bai_6A_full.csv",
            "K9_question_Bai_7A_full.csv",
            "K9_question_Bai_8A_full.csv",
            "K9_question_Bai_9A_full.csv",
            "K9_question_Bai_10A_full.csv",
            "K9_question_Bai_11_full.csv",
            "K9_question_Bai_12_full.csv",
            "K9_question_Bai_13_full.csv",
            "K9_question_Bai_14_full.csv",
        ]
    }
}

def read_csv_file(file_path: Path) -> list:
    """Đọc file CSV và trả về danh sách rows"""
    rows = []
    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:  # utf-8-sig để xử lý BOM
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except Exception as e:
        print(f"  ❌ Lỗi đọc file {file_path.name}: {e}")
    return rows

def extract_question_skill_mapping():
    """Extract q_id và topic_id từ tất cả các file CSV"""
    all_mappings = OrderedDict()  # Dùng OrderedDict để giữ thứ tự
    
    print("📖 Đang đọc các file CSV từ tất cả các khối...\n")
    
    total_count = 0
    
    for grade, config in GRADE_CONFIGS.items():
        grade_dir = config["dir"]
        files = config["files"]
        
        print(f"📚 KHỐI {grade}:")
        grade_count = 0
        
        for filename in files:
            file_path = grade_dir / filename
            
            if not file_path.exists():
                print(f"  ⚠️  Không tìm thấy: {filename}")
                continue
            
            print(f"  📄 Đang đọc: {filename}")
            rows = read_csv_file(file_path)
            
            for row in rows:
                q_id = row.get("q_id", "").strip()
                topic_id = row.get("topic_id", "").strip()
                
                if q_id and topic_id:
                    # topic_id = skillId
                    all_mappings[q_id] = topic_id
                    grade_count += 1
            
            print(f"     ✅ Đã extract {len(rows)} dòng từ {filename}")
        
        print(f"  📊 Khối {grade}: {grade_count} mapping\n")
        total_count += grade_count
    
    print(f"📊 Tổng cộng: {total_count} mapping từ tất cả các khối")
    
    return all_mappings

def merge_with_existing():
    """Merge với file question_skill.csv hiện tại (nếu có)"""
    existing_file = CSV_DIR / "question_skill.csv"
    existing_mappings = {}
    
    if existing_file.exists():
        print(f"\n📄 Đang đọc file hiện tại: question_skill.csv")
        rows = read_csv_file(existing_file)
        
        for row in rows:
            q_id = row.get("q_id", "").strip()
            skill_id = row.get("skillId", "").strip()
            if q_id and skill_id:
                existing_mappings[q_id] = skill_id
        
        print(f"     ✅ Đã có {len(existing_mappings)} mapping trong file hiện tại")
    
    return existing_mappings

def write_output(mappings: dict, output_file: Path):
    """Ghi ra file CSV"""
    print(f"\n💾 Đang ghi file: {output_file.name}")
    
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["q_id", "skillId"])
        
        # Sắp xếp theo q_id
        sorted_items = sorted(mappings.items(), key=lambda x: x[0])
        
        for q_id, skill_id in sorted_items:
            writer.writerow([q_id, skill_id])
    
    print(f"     ✅ Đã ghi {len(mappings)} dòng")

def main():
    """Hàm chính"""
    print("=" * 70)
    print("🔧 EXTRACT QUESTION-SKILL MAPPING TỪ TẤT CẢ CÁC KHỐI (6, 7, 8, 9)")
    print("=" * 70)
    
    # Extract từ tất cả các khối
    new_mappings = extract_question_skill_mapping()
    
    # Merge với file hiện tại
    existing_mappings = merge_with_existing()
    
    # Merge (ưu tiên file hiện tại nếu có conflict)
    merged_mappings = {**new_mappings, **existing_mappings}
    
    if existing_mappings:
        conflicts = set(new_mappings.keys()) & set(existing_mappings.keys())
        if conflicts:
            different = [q for q in conflicts if new_mappings[q] != existing_mappings[q]]
            if different:
                print(f"\n⚠️  Có {len(different)} q_id có mapping khác nhau:")
                for q_id in different[:5]:
                    print(f"     {q_id}: '{new_mappings[q_id]}' (mới) vs '{existing_mappings[q_id]}' (cũ)")
                print(f"     → Giữ lại mapping từ file cũ")
    
    # Ghi ra file
    write_output(merged_mappings, OUTPUT_FILE)
    
    # Thống kê
    print("\n" + "=" * 70)
    print("📊 TÓM TẮT")
    print("=" * 70)
    
    # Đếm theo khối
    by_grade = {"6": 0, "7": 0, "8": 0, "9": 0}
    for q_id in merged_mappings.keys():
        if q_id.startswith("K6"):
            by_grade["6"] += 1
        elif q_id.startswith("K7"):
            by_grade["7"] += 1
        elif q_id.startswith("K8"):
            by_grade["8"] += 1
        elif q_id.startswith("K9"):
            by_grade["9"] += 1
    
    print(f"✅ Tổng số mapping: {len(merged_mappings)}")
    print(f"   - Khối 6: {by_grade['6']} câu hỏi")
    print(f"   - Khối 7: {by_grade['7']} câu hỏi")
    print(f"   - Khối 8: {by_grade['8']} câu hỏi")
    print(f"   - Khối 9: {by_grade['9']} câu hỏi")
    print(f"\n📄 File output: {OUTPUT_FILE}")
    print(f"\n💡 Bước tiếp theo:")
    print(f"   1. Kiểm tra file: {OUTPUT_FILE.name}")
    print(f"   2. Nếu OK, copy/rename thành question_skill.csv")
    print(f"   3. Hoặc sử dụng trực tiếp để build questions_updated.ttl")

if __name__ == "__main__":
    main()


