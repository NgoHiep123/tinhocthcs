# ⚡ TÓM TẮT NHANH - GraphDB vs KNN

> So sánh 2 phương pháp phát hiện học sinh yếu và khuyến nghị

---

## 🚀 CHẠY NHANH

```bash
# Chạy tất cả các bước
python scripts/run_complete_comparison.py

# Hoặc chạy từng bước:
cd KG_Design/grade6 && python export_teachers_assignments.py
cd ML_Algorithms && python graphdb_detection_recommendation.py
cd ML_Algorithms && python knn_student_analysis.py
cd ML_Algorithms && python compare_graphdb_vs_knn.py
```

---

## 📋 CÁC FILE ĐÃ TẠO

1. **`KG_Design/grade6/export_teachers_assignments.py`**
   - Export giáo viên và phân công → `.ttl`

2. **`ML_Algorithms/graphdb_detection_recommendation.py`**
   - Phát hiện học sinh yếu bằng GraphDB SPARQL
   - Khuyến nghị tài nguyên

3. **`ML_Algorithms/compare_graphdb_vs_knn.py`**
   - So sánh kết quả 2 phương pháp

4. **`scripts/run_complete_comparison.py`**
   - Script tổng hợp chạy tất cả

---

## 📊 KẾT QUẢ

Sau khi chạy, sẽ có:
- `graphdb_results.json` - Kết quả GraphDB
- `knn_results.json` - Kết quả KNN
- `comparison_report.json` - Báo cáo so sánh

---

## 💡 SO SÁNH

| | GraphDB | KNN |
|---|---|---|
| **Explainable** | ✅ Có | ❌ Khó |
| **Cần training** | ❌ Không | ✅ Có |
| **Tận dụng KG** | ✅ Tốt | ⚠️ Hạn chế |
| **Accuracy** | ⚠️ Logic cố định | ✅ Tự động học |

---

**Xem chi tiết:** `HUONG_DAN_GRAPHDB_VS_KNN.md`

