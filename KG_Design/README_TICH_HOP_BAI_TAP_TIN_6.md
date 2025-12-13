# 📚 TÍCH HỢP Bai_tap_Tin_6/ VÀO KNOWLEDGE GRAPH

> Hướng dẫn nhanh để import 372 câu hỏi từ `Bai_tap_Tin_6/` vào Knowledge Graph

---

## 🎯 TÓM TẮT

**Nguồn:** 6 file CSV trong `Bai_tap_Tin_6/` (372 câu hỏi)
**Đích:** Knowledge Graph trong GraphDB
**Output:** File `questions_updated.ttl` (Layer C)

---

## ⚡ QUY TRÌNH NHANH

### Bước 1: Extract question-skill mapping

```bash
cd KG_Design
python scripts/utils/extract_question_skill_from_bai_tap.py
```

**Kết quả:** Tạo file `csv/question_skill_full.csv` với 372 mapping

**Nếu cần:** Copy/rename thành `csv/question_skill.csv` (thay thế file cũ)

---

### Bước 2: Build file TTL

```bash
cd KG_Design
python scripts/build/build_questions_from_bai_tap.py
```

**Kết quả:** Tạo file `data/grade6/ttl/questions_updated.ttl`

---

### Bước 3: Upload vào GraphDB

1. Mở GraphDB Desktop
2. Chọn repository: `tinhocthcs`
3. Upload file: `KG_Design/data/grade6/ttl/questions_updated.ttl`
4. Layer: **C (Entity Data)**

---

### Bước 4: Kiểm tra

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(DISTINCT ?question) as ?soCauHoi)
WHERE {
  ?question a edu:Question
}
```

**Kỳ vọng:** 372 câu hỏi

---

## 📊 KẾT QUẢ

### File tạo ra:

1. **`KG_Design/csv/question_skill_full.csv`**
   - 372 dòng (q_id, skillId)
   - Mapping đầy đủ từ Bai_tap_Tin_6

2. **`KG_Design/data/grade6/ttl/questions_updated.ttl`**
   - 372 câu hỏi dưới dạng RDF/Turtle
   - Bao gồm: q_id, questionText, correctOption, difficulty
   - Có quan hệ: belongsToLesson, requiresSkill

---

## 🔍 CHI TIẾT

Xem file đầy đủ: `HUONG_DAN_TICH_HOP_BAI_TAP_TIN_6.md`

---

## ✅ CHECKLIST

- [ ] Chạy script extract question_skill
- [ ] Kiểm tra file question_skill_full.csv
- [ ] (Tùy chọn) Copy/rename thành question_skill.csv
- [ ] Chạy script build questions_updated.ttl
- [ ] Kiểm tra file TTL có hợp lệ không
- [ ] Upload vào GraphDB (Layer C)
- [ ] Chạy query kiểm tra số lượng questions
- [ ] Verify một vài câu hỏi mẫu

---

**Cập nhật:** 2025-01-15


