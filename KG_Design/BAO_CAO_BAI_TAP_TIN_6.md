# 📊 BÁO CÁO VỀ CÁC FILE CSV TRONG `Bai_tap_Tin_6/`

> Phân tích các file CSV chứa ngân hàng câu hỏi Khối 6

---

## 📋 TỔNG QUAN

**Thư mục:** `Bai_tap_Tin_6/`

**Số lượng file:** 6 files CSV

**Mục đích:** Ngân hàng câu hỏi trắc nghiệm cho từng chủ đề (A, B, C, D, E, F) của khối 6

---

## 📁 DANH SÁCH FILE

| File | Chủ đề | Mô tả |
|------|--------|-------|
| `K6_question_A_full.csv` | Chủ đề A | Máy tính và cộng đồng |
| `K6_question_B_full.csv` | Chủ đề B | Mạng máy tính và Internet |
| `K6_question_C_full.csv` | Chủ đề C | Tổ chức lưu trữ, tìm kiếm và trao đổi thông tin |
| `K6_question_D_full.csv` | Chủ đề D | Đạo đức, pháp luật và văn hóa trong môi trường số |
| `K6_question_E_full.csv` | Chủ đề E | Ứng dụng tin học |
| `K6_question_F_full.csv` | Chủ đề F | Giải quyết vấn đề với sự trợ giúp của máy tính |

---

## 📊 CẤU TRÚC FILE CSV

### Header (Các cột):

```csv
q_id,topic_id,question_text,option_A,option_B,option_C,option_D,correct_option,difficulty,source
```

### Giải thích các cột:

| Cột | Kiểu dữ liệu | Mô tả | Ví dụ |
|-----|--------------|-------|-------|
| `q_id` | String | Mã câu hỏi duy nhất | `K6A1_01`, `K6B1_05` |
| `topic_id` | String | Mã chủ đề/kỹ năng | `A1_Thong_tin_va_xu_li`, `k6_b1_khai_niem_loi_ich` |
| `question_text` | String | Nội dung câu hỏi | "Thông tin là gì?" |
| `option_A` | String | Lựa chọn A | "Những gì đem lại hiểu biết cho con người" |
| `option_B` | String | Lựa chọn B | "Vật mang tin" |
| `option_C` | String | Lựa chọn C | "Dữ liệu hình ảnh" |
| `option_D` | String | Lựa chọn D | "Thiết bị số" |
| `correct_option` | String (A/B/C/D) | Đáp án đúng | `A`, `B`, `C`, hoặc `D` |
| `difficulty` | String | Độ khó (theo Bloom) | `Nhận biết`, `Thông hiểu`, `Vận dụng` |
| `source` | String | Nguồn tài liệu | "Tin 6 – Cánh Diều · Chủ đề A – Bài 1..." |

---

## 🎯 CÁC CHỨC NĂNG HỖ TRỢ

### 1. **Tạo file HTML Quiz** ✅

**Script sử dụng:**
- `scripts/generate_all_k6_html.py`
- `scripts/generate_k6_quiz_new.py`
- `scripts/generate_k6_html_files.py`

**Chức năng:**
- Đọc các file CSV này
- Tạo các file HTML quiz tương ứng (ví dụ: `K6_A1.html`, `K6_A2.html`)
- Mỗi file HTML chứa 10 câu hỏi ngẫu nhiên từ chủ đề tương ứng

**Output:**
- Các file HTML trong thư mục `Web/` hoặc thư mục gốc
- Ví dụ: `K6_A1.html`, `K6_A2.html`, `K6_B1.html`, ...

---

### 2. **Tạo bài kiểm tra** ✅

**Script sử dụng:**
- `scripts/generate_k6_tests_hk1.py` - Tạo 4 bài kiểm tra học kỳ 1
- `scripts/generate_k6_tests_hk2.py` - Tạo bài kiểm tra học kỳ 2

**Chức năng:**
- Tạo các bài kiểm tra tổng hợp từ nhiều chủ đề
- Mỗi bài kiểm tra có 20-40 câu hỏi
- Phân bổ câu hỏi theo mức độ (Nhận biết, Thông hiểu, Vận dụng)

**Output:**
- `K6_KIEM_TRA_1.html` - Kiểm tra 1 (Chủ đề A)
- `K6_KIEM_TRA_2.html` - Kiểm tra 2 (Chủ đề A & B)
- `K6_KIEM_TRA_3.html` - Kiểm tra 3 (Chủ đề C)
- `K6_KIEM_TRA_4.html` - Kiểm tra 4 (Chủ đề A, B, C)
- Và các bài kiểm tra học kỳ 2

---

### 3. **Tích hợp với Knowledge Graph** 🔄

**Khả năng:**
- Dữ liệu trong các file CSV này có thể được import vào Knowledge Graph
- Cột `q_id` có thể mapping với `questions_updated.ttl`
- Cột `topic_id` có thể mapping với `question_skill.csv` → `skillId`
- Cột `difficulty` có thể được lưu vào property `edu:difficulty`

**Ví dụ mapping:**
```csv
# K6_question_A_full.csv
q_id: K6A1_01
topic_id: A1_Thong_tin_va_xu_li

# question_skill.csv (trong KG_Design/csv/)
q_id: K6A1_01
skillId: A1_Thong_tin_va_xu_li
```

---

### 4. **Xuất dữ liệu sang các format khác** 🔄

**Khả năng:**
- Export sang JSON để sử dụng trong web app
- Export sang format phù hợp với MySQL database
- Tạo mapping với các file CSV trong `KG_Design/csv/`

---

## 📈 THỐNG KÊ

### Số lượng câu hỏi:

| Chủ đề | File | Số câu hỏi |
|--------|------|------------|
| A | `K6_question_A_full.csv` | 60 câu |
| B | `K6_question_B_full.csv` | 48 câu |
| C | `K6_question_C_full.csv` | 72 câu |
| D | `K6_question_D_full.csv` | 36 câu |
| E | `K6_question_E_full.csv` | 96 câu |
| F | `K6_question_F_full.csv` | 60 câu |

**Tổng cộng:** 372 câu hỏi

---

## 🔗 MỐI LIÊN HỆ VỚI HỆ THỐNG

### Với `KG_Design/csv/`:

| File trong `Bai_tap_Tin_6/` | Liên hệ với file trong `KG_Design/csv/` |
|------------------------------|------------------------------------------|
| `K6_question_*.csv` | `question_skill.csv` (cột `q_id`, `topic_id` → `skillId`) |
| `K6_question_*.csv` | Có thể tạo `questions.csv` (nếu cần) |

### Với Knowledge Graph:

```
Bai_tap_Tin_6/K6_question_A_full.csv
    ↓ (q_id, topic_id)
question_skill.csv
    ↓ (q_id, skillId)
questions_updated.ttl
    ↓ (RDF)
GraphDB
```

---

## 💡 GỢI Ý SỬ DỤNG

### 1. **Để tạo HTML quiz:**
```bash
cd scripts
python generate_all_k6_html.py
```

### 2. **Để tạo bài kiểm tra:**
```bash
cd scripts
python generate_k6_tests_hk1.py
python generate_k6_tests_hk2.py
```

### 3. **Để tích hợp với KG:**
- Đảm bảo `q_id` trong `Bai_tap_Tin_6/*.csv` khớp với `q_id` trong `KG_Design/csv/question_skill.csv`
- Đảm bảo `topic_id` khớp với `skillId` trong `KG_Design/csv/skills.csv`

---

## ⚠️ LƯU Ý

1. **Encoding:** File CSV sử dụng UTF-8 (có thể có BOM ở đầu file)

2. **Format câu hỏi:** 
   - Mỗi câu có 4 lựa chọn (A, B, C, D)
   - Chỉ có 1 đáp án đúng
   - Độ khó được phân loại theo Bloom (Nhận biết, Thông hiểu, Vận dụng)

3. **topic_id không nhất quán:**
   - Một số dùng format: `A1_Thong_tin_va_xu_li` (có underscore)
   - Một số dùng format: `k6_b1_khai_niem_loi_ich` (có chữ thường và underscore)
   - Cần chuẩn hóa khi tích hợp với KG

4. **Mapping với KG:**
   - Cần kiểm tra xem `topic_id` có khớp với `skillId` trong `KG_Design/csv/skills.csv` không
   - Nếu không khớp, cần tạo mapping table hoặc script chuyển đổi

---

## 📝 KẾT LUẬN

Các file CSV trong `Bai_tap_Tin_6/` là **nguồn dữ liệu chính** cho:
- ✅ Tạo các file HTML quiz cho web
- ✅ Tạo các bài kiểm tra
- 🔄 Tích hợp với Knowledge Graph (cần mapping)

Đây là **ngân hàng câu hỏi đầy đủ** với **372 câu hỏi**, được phân loại theo chủ đề và mức độ khó.

---

**Cập nhật:** 2025-01-15

