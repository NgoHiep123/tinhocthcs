# 🔗 HƯỚNG DẪN TÍCH HỢP `Bai_tap_Tin_6/` VÀO KNOWLEDGE GRAPH

> Cách import 372 câu hỏi từ các file CSV vào Knowledge Graph

---

## 📋 TỔNG QUAN

**Nguồn dữ liệu:** 6 file CSV trong `Bai_tap_Tin_6/`
- `K6_question_A_full.csv` (60 câu)
- `K6_question_B_full.csv` (48 câu)
- `K6_question_C_full.csv` (72 câu)
- `K6_question_D_full.csv` (36 câu)
- `K6_question_E_full.csv` (96 câu)
- `K6_question_F_full.csv` (60 câu)

**Tổng:** 372 câu hỏi

**Đích:** Knowledge Graph trong GraphDB

---

## 🎯 QUY TRÌNH TÍCH HỢP

### Bước 1: Kiểm tra mapping `topic_id` → `skillId`

**Vấn đề:** Cột `topic_id` trong `Bai_tap_Tin_6/*.csv` có thể không khớp với `skillId` trong `KG_Design/csv/question_skill.csv`

**Cách kiểm tra:**
```bash
# Xem topic_id trong Bai_tap_Tin_6
cd Bai_tap_Tin_6
head -1 K6_question_A_full.csv | cut -d',' -f2  # Cột topic_id

# Xem skillId trong question_skill.csv
cd ../KG_Design/csv
head -5 question_skill.csv
```

**Mapping hiện tại:**
- `Bai_tap_Tin_6/*.csv`: `topic_id` = `A1_Thong_tin_va_xu_li`, `k6_b1_khai_niem_loi_ich`
- `KG_Design/csv/question_skill.csv`: `skillId` = `A1_Thong_tin_va_xu_li`, `k6_b1_khai_niem_loi_ich`

**Kết luận:** ✅ Mapping đã có sẵn trong `question_skill.csv` (cột `skillId`)

---

### Bước 2: Tạo/cập nhật `question_skill.csv`

**File hiện tại:** `KG_Design/csv/question_skill.csv` (chỉ có ~41 dòng)

**Cần:** Tạo đầy đủ mapping cho 372 câu hỏi

**Cách làm:**

#### 2.1. Tự động extract từ `Bai_tap_Tin_6/*.csv`

Sử dụng script: `KG_Design/scripts/utils/extract_question_skill_from_bai_tap.py` (sẽ tạo)

Script sẽ:
1. Đọc tất cả file CSV trong `Bai_tap_Tin_6/`
2. Extract cột `q_id` và `topic_id`
3. Tạo file `question_skill.csv` mới với format: `q_id,skillId`

#### 2.2. Merge với file hiện tại

```bash
# Kiểm tra xem có trùng lặp không
python scripts/utils/merge_question_skill.py
```

---

### Bước 3: Tạo file TTL cho Questions

#### 3.1. Cấu trúc TTL cần tạo

```turtle
@prefix edu: <http://education.vn/ontology#> .
@prefix data: <http://education.vn/data/> .

data:question_K6A1_01 a edu:Question ;
    edu:q_id "K6A1_01" ;
    edu:questionText "Thông tin là gì?" ;
    edu:correctOption "A" ;
    edu:difficulty "Nhận biết" ;
    edu:belongsToLesson data:lesson_6_A1 ;
    edu:requiresSkill data:skill_A1_Thong_tin_va_xu_li .
```

#### 3.2. Dữ liệu cần có

Từ `Bai_tap_Tin_6/*.csv`:
- `q_id` → `edu:q_id`
- `question_text` → `edu:questionText`
- `correct_option` → `edu:correctOption`
- `difficulty` → `edu:difficulty`
- `topic_id` → mapping với `edu:requiresSkill` (qua `question_skill.csv`)

**Thiếu:** `lesson_id` để map với `edu:belongsToLesson`

**Giải pháp:** 
- Từ `q_id` (ví dụ: `K6A1_01`) → extract `lesson_id` = `6_A1`
- Hoặc sử dụng mapping từ `KG_Design/csv/lessons.csv`

---

### Bước 4: Build file TTL

Sử dụng script: `KG_Design/scripts/build/build_questions_from_bai_tap.py` (sẽ tạo)

Script sẽ:
1. Đọc tất cả file CSV trong `Bai_tap_Tin_6/`
2. Đọc `question_skill.csv` để map `q_id` → `skillId`
3. Đọc `lessons.csv` để map `q_id` → `lesson_id`
4. Tạo file `questions_updated.ttl` với đầy đủ thông tin

---

### Bước 5: Upload vào GraphDB

```bash
# Upload file questions_updated.ttl vào GraphDB Desktop
# Repository: tinhocthcs
# Layer: C (Entity Data)
```

---

## 🔧 SCRIPTS CẦN TẠO

### Script 1: `extract_question_skill_from_bai_tap.py`

**Mục đích:** Extract `q_id` và `topic_id` từ `Bai_tap_Tin_6/*.csv` để tạo `question_skill.csv`

**Input:**
- Tất cả file CSV trong `Bai_tap_Tin_6/`

**Output:**
- `KG_Design/csv/question_skill_full.csv` (hoặc merge vào file hiện tại)

---

### Script 2: `build_questions_from_bai_tap.py`

**Mục đích:** Tạo file `questions_updated.ttl` từ `Bai_tap_Tin_6/*.csv`

**Input:**
- `Bai_tap_Tin_6/K6_question_*.csv` (6 files)
- `KG_Design/csv/question_skill.csv` (mapping q_id → skillId)
- `KG_Design/csv/lessons.csv` (mapping để tìm lesson_id)

**Output:**
- `KG_Design/data/grade6/ttl/questions_updated.ttl`

---

## 📊 SƠ ĐỒ QUY TRÌNH

```
Bai_tap_Tin_6/K6_question_*.csv
    ↓ (extract q_id, topic_id)
question_skill.csv (cập nhật)
    ↓
questions_updated.ttl (build)
    ↓
GraphDB (Layer C)
```

---

## ✅ CHECKLIST

### Trước khi tích hợp:
- [ ] Kiểm tra `topic_id` trong `Bai_tap_Tin_6/*.csv` có khớp với `skillId` không
- [ ] Kiểm tra `q_id` có format đúng không (ví dụ: `K6A1_01`)
- [ ] Xác nhận có mapping `q_id` → `lesson_id` (từ `q_id` hoặc `lessons.csv`)

### Quá trình tích hợp:
- [ ] Chạy script extract `question_skill.csv`
- [ ] Merge/cập nhật `question_skill.csv`
- [ ] Chạy script build `questions_updated.ttl`
- [ ] Kiểm tra file TTL có hợp lệ không
- [ ] Upload vào GraphDB (Layer C)

### Sau khi tích hợp:
- [ ] Chạy query kiểm tra số lượng questions trong GraphDB
- [ ] Kiểm tra một vài câu hỏi mẫu
- [ ] Kiểm tra quan hệ `requiresSkill` có đúng không

---

## 🔍 QUERY KIỂM TRA

### Query 1: Đếm số câu hỏi

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(DISTINCT ?question) as ?soCauHoi)
WHERE {
  ?question a edu:Question
}
```

**Kỳ vọng:** 372 câu hỏi

---

### Query 2: Kiểm tra một câu hỏi mẫu

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?question ?q_id ?questionText ?correctOption ?difficulty ?skill
WHERE {
  ?question a edu:Question ;
            edu:q_id "K6A1_01" ;
            edu:questionText ?questionText ;
            edu:correctOption ?correctOption ;
            edu:difficulty ?difficulty ;
            edu:requiresSkill ?skill .
}
```

---

### Query 3: Kiểm tra quan hệ với skill

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?skill ?skillId (COUNT(?question) as ?soCauHoi)
WHERE {
  ?question a edu:Question ;
            edu:requiresSkill ?skill .
  ?skill edu:skillId ?skillId
}
GROUP BY ?skill ?skillId
ORDER BY DESC(?soCauHoi)
LIMIT 10
```

---

## ⚠️ LƯU Ý

1. **Mapping topic_id → skillId:**
   - Một số `topic_id` có format khác nhau (ví dụ: `A1_Thong_tin_va_xu_li` vs `k6_b1_khai_niem_loi_ich`)
   - Cần chuẩn hóa hoặc tạo mapping table

2. **Mapping q_id → lesson_id:**
   - Từ `q_id` = `K6A1_01` → `lesson_id` = `6_A1`
   - Cần extract từ pattern hoặc sử dụng mapping table

3. **Encoding:**
   - File CSV có thể có BOM (Byte Order Mark)
   - Cần xử lý khi đọc file

4. **Thuộc tính bổ sung:**
   - Có thể lưu thêm: `option_A`, `option_B`, `option_C`, `option_D`, `source`
   - Nhưng schema hiện tại không có các properties này
   - Có thể cần mở rộng schema hoặc lưu vào property khác

---

## 📝 VÍ DỤ MAPPING

### Ví dụ 1: Câu hỏi K6A1_01

**Input từ `Bai_tap_Tin_6/K6_question_A_full.csv`:**
```csv
K6A1_01,A1_Thong_tin_va_xu_li,"Thông tin là gì?",...,A,Nhận biết,...
```

**Mapping:**
- `q_id` = `K6A1_01`
- `topic_id` = `A1_Thong_tin_va_xu_li` → `skillId` (qua `question_skill.csv`)
- `lesson_id` = `6_A1` (extract từ `q_id`)

**Output TTL:**
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

1. **Tạo script extract `question_skill.csv`**
2. **Tạo script build `questions_updated.ttl`**
3. **Test với một vài câu hỏi mẫu**
4. **Build toàn bộ và upload vào GraphDB**
5. **Kiểm tra và verify**

---

**Cập nhật:** 2025-01-15


