"""
Script extract question_skill mapping từ Bai_tap_Tin_6/*.csv
Tạo/cập nhật file question_skill.csv với đầy đủ 372 câu hỏi
"""

import csv
import os
from pathlib import Path
from collections import OrderedDict

# Đường dẫn
ROOT = Path(__file__).resolve().parent.parent.parent.parent  # D:\A_DeAnTN
BAI_TAP_DIR = ROOT / "Bai_tap_Tin_6"
CSV_DIR = ROOT / "KG_Design" / "csv"
OUTPUT_FILE = CSV_DIR / "question_skill_full.csv"

# Danh sách file CSV trong Bai_tap_Tin_6
CSV_FILES = [
    "K6_question_A_full.csv",
    "K6_question_B_full.csv",
    "K6_question_C_full.csv",
    "K6_question_D_full.csv",
    "K6_question_E_full.csv",
    "K6_question_F_full.csv",
]

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
    """Extract q_id và topic_id từ các file CSV"""
    all_mappings = OrderedDict()  # Dùng OrderedDict để giữ thứ tự
    
    print("📖 Đang đọc các file CSV từ Bai_tap_Tin_6/...")
    
    for filename in CSV_FILES:
        file_path = BAI_TAP_DIR / filename
        
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
        
        print(f"     ✅ Đã extract {len(rows)} dòng từ {filename}")
    
    print(f"\n📊 Tổng cộng: {len(all_mappings)} mapping")
    
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
    print("🔧 EXTRACT QUESTION-SKILL MAPPING TỪ Bai_tap_Tin_6/")
    print("=" * 70)
    
    # Extract từ Bai_tap_Tin_6
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
    print(f"✅ Tổng số mapping: {len(merged_mappings)}")
    print(f"📄 File output: {OUTPUT_FILE}")
    print(f"\n💡 Bước tiếp theo:")
    print(f"   1. Kiểm tra file: {OUTPUT_FILE.name}")
    print(f"   2. Nếu OK, copy/rename thành question_skill.csv")
    print(f"   3. Hoặc sử dụng trực tiếp để build questions_updated.ttl")

if __name__ == "__main__":
    main()


