# 📊 Hướng Dẫn: So Sánh GraphDB vs KNN

> **Mục đích:** So sánh 2 phương pháp phát hiện học sinh yếu và khuyến nghị

---

## 🎯 TỔNG QUAN

Hệ thống hỗ trợ 2 phương pháp:

1. **GraphDB (SPARQL)** - Dựa trên truy vấn Knowledge Graph
2. **KNN (Machine Learning)** - Dựa trên thuật toán học máy

### So sánh nhanh:

| Tiêu chí | GraphDB | KNN |
|----------|---------|-----|
| **Cơ sở** | Truy vấn SPARQL trên KG | Machine Learning |
| **Cần training** | ❌ Không | ✅ Có |
| **Explainable** | ✅ Có | ❌ Khó |
| **Tận dụng KG** | ✅ Tốt | ⚠️ Hạn chế |
| **Xử lý patterns** | ⚠️ Logic cố định | ✅ Tự động |

---

## 📋 CÁC BƯỚC THỰC HIỆN

### Bước 1: Tạo file .ttl cho giáo viên và phân công

```bash
cd KG_Design/grade6
python export_teachers_assignments.py
```

**Output:** `KG_Design/grade6/out/teachers_assignments.ttl`

**File này chứa:**
- Thông tin giáo viên (Teacher nodes)
- Phân công lớp (Teacher → teaches → Class)

---

### Bước 2: Import vào GraphDB

```bash
# Chạy script import
python scripts/import_all_kg.py

# Hoặc import thủ công trong GraphDB Desktop
```

---

### Bước 3: Chạy GraphDB Detection

```bash
cd ML_Algorithms
python graphdb_detection_recommendation.py
```

**Output:** `ML_Algorithms/graphdb_results.json`

**Kết quả:**
- Danh sách học sinh yếu được phát hiện
- Khuyến nghị tài nguyên học tập

---

### Bước 4: Chạy KNN Analysis

```bash
cd ML_Algorithms
python knn_student_analysis.py
```

**Output:** `ML_Algorithms/knn_results.json` (hoặc trong KG_Design)

**Kết quả:**
- Danh sách học sinh yếu từ KNN
- Phân tích dựa trên vector đặc trưng

---

### Bước 5: So sánh kết quả

```bash
cd ML_Algorithms
python compare_graphdb_vs_knn.py
```

**Output:** `ML_Algorithms/comparison_report.json`

**Báo cáo bao gồm:**
- So sánh số lượng học sinh yếu phát hiện được
- Jaccard Similarity
- Precision, Recall, F1 Score
- So sánh khuyến nghị

---

## 📊 PHƯƠNG PHÁP 1: GRAPHDB (SPARQL)

### Cách hoạt động:

1. **Phát hiện học sinh yếu:**
   - Truy vấn tất cả học sinh và điểm mastery
   - Tính điểm trung bình cho mỗi skill
   - Filter những học sinh có điểm < ngưỡng (5.0)

2. **Khuyến nghị:**
   - Với mỗi học sinh yếu ở skill X
   - Tìm resource liên quan đến skill X
   - Sắp xếp theo coverage

### Ưu điểm:
- ✅ Tận dụng cấu trúc liên kết của KG
- ✅ Không cần training data
- ✅ Giải thích được (explainable)
- ✅ Truy vấn trực tiếp trên dữ liệu

### Nhược điểm:
- ❌ Phụ thuộc vào chất lượng KG
- ❌ Logic truy vấn có thể phức tạp
- ❌ Khó tối ưu với dữ liệu lớn

---

## 🤖 PHƯƠNG PHÁP 2: KNN (MACHINE LEARNING)

### Cách hoạt động:

1. **Xây dựng vector đặc trưng:**
   - Điểm trung bình các bài kiểm tra
   - Số bài đã làm
   - Tỷ lệ hoàn thành
   - Thời gian làm bài

2. **Training:**
   - Gán nhãn học sinh yếu/không yếu
   - Training KNN model

3. **Prediction:**
   - Với mỗi học sinh mới, tìm k hàng xóm gần nhất
   - Dự đoán dựa trên nhãn của k hàng xóm

### Ưu điểm:
- ✅ Học từ dữ liệu lịch sử
- ✅ Phát hiện patterns phức tạp
- ✅ Tự động điều chỉnh theo dữ liệu mới
- ✅ Có thể xử lý nhiều features

### Nhược điểm:
- ❌ Cần dữ liệu training đủ lớn
- ❌ Black box (khó giải thích)
- ❌ Phụ thuộc vào quality của features
- ❌ Cần tuning hyperparameters

---

## 📈 METRICS SO SÁNH

### Jaccard Similarity

Đo độ tương đồng giữa 2 tập hợp:

```
J(A, B) = |A ∩ B| / |A ∪ B|
```

- **0.0 - 0.3:** Khác biệt nhiều
- **0.3 - 0.7:** Tương đồng vừa phải
- **0.7 - 1.0:** Tương đồng cao

### Precision, Recall, F1

- **Precision:** Độ chính xác (trong số phát hiện, bao nhiêu đúng)
- **Recall:** Độ bao phủ (trong số thực tế, phát hiện được bao nhiêu)
- **F1 Score:** Trung bình điều hòa của Precision và Recall

---

## 💡 KẾT LUẬN VÀ KHUYẾN NGHỊ

### Khi nào dùng GraphDB:
- ✅ Cần giải thích được kết quả
- ✅ Dữ liệu đã có trong KG
- ✅ Cần tận dụng cấu trúc liên kết
- ✅ Logic truy vấn rõ ràng

### Khi nào dùng KNN:
- ✅ Có nhiều dữ liệu lịch sử
- ✅ Cần phát hiện patterns phức tạp
- ✅ Cần tự động hóa cao
- ✅ Chấp nhận black box

### Kết hợp cả 2:
- ✅ GraphDB để validate kết quả KNN
- ✅ KNN để bổ sung cho GraphDB
- ✅ Ensemble: Lấy kết quả cả 2 và vote

---

## 📁 FILE OUTPUT

Sau khi chạy, bạn sẽ có:

```
ML_Algorithms/
├── graphdb_results.json          ← Kết quả GraphDB
├── knn_results.json              ← Kết quả KNN
└── comparison_report.json        ← Báo cáo so sánh
```

---

## 🔍 XEM KẾT QUẢ

### Xem kết quả GraphDB:
```bash
cat ML_Algorithms/graphdb_results.json | python -m json.tool
```

### Xem kết quả KNN:
```bash
cat ML_Algorithms/knn_results.json | python -m json.tool
```

### Xem báo cáo so sánh:
```bash
cat ML_Algorithms/comparison_report.json | python -m json.tool
```

---

## 🎯 VÍ DỤ KẾT QUẢ

### GraphDB Results:
```json
{
  "method": "GraphDB SPARQL",
  "weak_students": [
    {
      "student_id": "2324_0001",
      "skill_id": "A1_Thong_tin_va_xu_li",
      "avg_score": 4.2,
      "method": "GraphDB"
    }
  ],
  "recommendations": [
    {
      "student_id": "2324_0001",
      "resource_id": "K6_A1.html",
      "coverage": 0.9
    }
  ]
}
```

### Comparison Report:
```json
{
  "comparison": {
    "weak_students": {
      "graphdb_total": 25,
      "knn_total": 28,
      "common": 20,
      "jaccard_similarity": 0.61,
      "graphdb_metrics": {
        "precision": 0.80,
        "recall": 0.71,
        "f1_score": 0.75
      }
    }
  }
}
```

---

## ❓ FAQ

### Q: Phương pháp nào tốt hơn?
**A:** Tùy vào mục đích:
- GraphDB tốt cho explainability
- KNN tốt cho accuracy cao

### Q: Có thể kết hợp cả 2 không?
**A:** Có! Có thể:
- Dùng GraphDB để validate KNN
- Dùng KNN để bổ sung cho GraphDB
- Ensemble voting

### Q: Cần dữ liệu bao nhiêu?
**A:** 
- GraphDB: Chỉ cần dữ liệu trong KG
- KNN: Cần ít nhất 100+ học sinh để training tốt

---

**Chúc bạn thành công! 🚀**

