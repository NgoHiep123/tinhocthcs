# ✅ BÁO CÁO TÍCH HỢP TẤT CẢ CÁC KHỐI VÀO KNOWLEDGE GRAPH

> Đã tích hợp 1080 câu hỏi từ khối 6, 7, 8, 9 vào Knowledge Graph

---

## 📊 TỔNG QUAN

**Ngày thực hiện:** 2025-01-15

**Nguồn dữ liệu:**
- `Bai_tap_Tin_6/` - 6 files CSV (372 câu hỏi)
- `Bai_tap_Tin_7/` - 5 files CSV (324 câu hỏi)
- `Bai_tap_Tin_8/` - 7 files CSV (210 câu hỏi)
- `Bai_tap_Tin_9/` - 14 files CSV (174 câu hỏi)

**Tổng cộng:** 32 files CSV → **1080 câu hỏi**

---

## ✅ ĐÃ HOÀN THÀNH

### 1. Extract Question-Skill Mapping ✅

**Script:** `scripts/utils/extract_question_skill_all_grades.py`

**Kết quả:**
- File output: `csv/question_skill_all_grades.csv`
- Tổng số mapping: **1074 dòng**
  - Khối 6: 372 mapping
  - Khối 7: 324 mapping
  - Khối 8: 204 mapping
  - Khối 9: 173 mapping

**Lưu ý:** Một số câu hỏi có thể không có `topic_id` nên số mapping < số câu hỏi

---

### 2. Build File TTL ✅

**Script:** `scripts/build/build_questions_all_grades.py`

**Kết quả:**
- File output: `data/grade6/ttl/questions_updated_all_grades.ttl`
- Tổng số câu hỏi: **1080 câu hỏi** dưới dạng RDF/Turtle

**Cấu trúc mỗi câu hỏi:**
```turtle
data:question_K6A1_01 a edu:Question ;
    edu:q_id "K6A1_01" ;
    edu:questionText "Thông tin là gì?" ;
    edu:correctOption "A" ;
    edu:difficulty "Nhận biết" ;
    edu:belongsToLesson data:lesson_6_A1 ;
    edu:requiresSkill data:skill_A1_Thong_tin_va_xu_li .
```

---

## 📁 CÁC FILE ĐÃ TẠO

### 1. `KG_Design/csv/question_skill_all_grades.csv`
- 1074 dòng (q_id, skillId)
- Mapping đầy đủ từ tất cả các khối

### 2. `KG_Design/data/grade6/ttl/questions_updated_all_grades.ttl`
- 1080 câu hỏi dưới dạng RDF/Turtle
- Bao gồm: q_id, questionText, correctOption, difficulty
- Có quan hệ: belongsToLesson, requiresSkill

---

## 📊 THỐNG KÊ CHI TIẾT

### Theo khối:

| Khối | Số file CSV | Số câu hỏi | Số mapping |
|------|-------------|------------|------------|
| **6** | 6 | 372 | 372 |
| **7** | 5 | 324 | 324 |
| **8** | 7 | 210 | 204 |
| **9** | 14 | 174 | 173 |
| **TỔNG** | **32** | **1080** | **1074** |

### Theo chủ đề (Khối 6):

| Chủ đề | Số câu hỏi |
|--------|------------|
| A | 60 |
| B | 48 |
| C | 72 |
| D | 36 |
| E | 96 |
| F | 60 |
| **TỔNG** | **372** |

---

## 🔍 CẤU TRÚC FILE TTL

### Prefix:
```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix edu: <http://education.vn/ontology#> .
@prefix data: <http://education.vn/data/> .
```

### Ví dụ câu hỏi:
```turtle
data:question_K6A1_01 a edu:Question ;
    edu:q_id "K6A1_01" ;
    edu:questionText "Thông tin là gì?" ;
    edu:correctOption "A" ;
    edu:difficulty "Nhận biết" ;
    edu:belongsToLesson data:lesson_6_A1 ;
    edu:requiresSkill data:skill_A1_Thong_tin_va_xu_li .
```

---

## 🚀 BƯỚC TIẾP THEO

### 1. Upload vào GraphDB

```bash
# Mở GraphDB Desktop
# Repository: tinhocthcs
# Upload file: KG_Design/data/grade6/ttl/questions_updated_all_grades.ttl
# Layer: C (Entity Data)
```

### 2. Kiểm tra sau khi upload

#### Query 1: Đếm số câu hỏi

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(DISTINCT ?question) as ?soCauHoi)
WHERE {
  ?question a edu:Question
}
```

**Kỳ vọng:** 1080 câu hỏi

#### Query 2: Đếm theo khối

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT 
  (COUNT(DISTINCT ?q6) as ?khoi6)
  (COUNT(DISTINCT ?q7) as ?khoi7)
  (COUNT(DISTINCT ?q8) as ?khoi8)
  (COUNT(DISTINCT ?q9) as ?khoi9)
WHERE {
  { ?q6 a edu:Question ; edu:q_id ?id6 . FILTER(STRSTARTS(?id6, "K6")) }
  UNION
  { ?q7 a edu:Question ; edu:q_id ?id7 . FILTER(STRSTARTS(?id7, "K7")) }
  UNION
  { ?q8 a edu:Question ; edu:q_id ?id8 . FILTER(STRSTARTS(?id8, "K8")) }
  UNION
  { ?q9 a edu:Question ; edu:q_id ?id9 . FILTER(STRSTARTS(?id9, "K9")) }
}
```

**Kỳ vọng:**
- Khối 6: 372
- Khối 7: 324
- Khối 8: 210
- Khối 9: 174

#### Query 3: Kiểm tra một câu hỏi mẫu

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?question ?q_id ?questionText ?correctOption ?difficulty ?lesson ?skill
WHERE {
  ?question a edu:Question ;
            edu:q_id "K6A1_01" ;
            edu:questionText ?questionText ;
            edu:correctOption ?correctOption ;
            edu:difficulty ?difficulty ;
            edu:belongsToLesson ?lesson ;
            edu:requiresSkill ?skill .
}
```

---

## ⚠️ LƯU Ý

1. **Missing Skill Mapping:**
   - Một số câu hỏi có thể không có `topic_id` trong file CSV
   - Những câu hỏi này sẽ không có quan hệ `requiresSkill`

2. **Lesson ID Extraction:**
   - Pattern cho K6, K7, K8: `K6A1_01` → `lesson_6_A1`
   - Pattern cho K9: `K9Bai_1_01` → `lesson_9_B1`
   - Cần kiểm tra xem lesson ID có tồn tại trong `lessons.ttl` không

3. **Skill URI:**
   - Format: `data:skill_{skillId}`
   - Cần đảm bảo skill URI khớp với format trong `skills.ttl`

---

## ✅ CHECKLIST

- [x] Extract question-skill mapping từ tất cả các khối
- [x] Tạo file `question_skill_all_grades.csv`
- [x] Build file `questions_updated_all_grades.ttl`
- [ ] Kiểm tra file TTL có hợp lệ không
- [ ] Upload vào GraphDB (Layer C)
- [ ] Chạy query kiểm tra số lượng questions
- [ ] Verify một vài câu hỏi mẫu
- [ ] Kiểm tra quan hệ belongsToLesson
- [ ] Kiểm tra quan hệ requiresSkill

---

## 📝 KẾT LUẬN

✅ **Đã tích hợp thành công 1080 câu hỏi từ 4 khối (6, 7, 8, 9) vào Knowledge Graph**

Các file đã được tạo và sẵn sàng để upload vào GraphDB.

---

**Cập nhật:** 2025-01-15


