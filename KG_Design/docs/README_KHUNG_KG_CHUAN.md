# 📘 HƯỚNG DẪN SỬ DỤNG KHUNG KG CHUẨN

## 🎯 TỔNG QUAN

Khung Knowledge Graph chuẩn được xây dựng dựa trên **Đề cương Đề án 2**, bỏ qua phần KNN và tập trung vào các chức năng đề xuất dựa trên dữ liệu và PPR.

---

## 📁 CÁC FILE QUAN TRỌNG

| File | Mô tả |
|------|-------|
| `kg_schema_chuan.ttl` | **Schema chính** - Định nghĩa tất cả thực thể và quan hệ |
| `KHUNG_KG_CHUAN.md` | **Tài liệu chi tiết** - Mô tả đầy đủ khung KG |
| `SO_SANH_SCHEMA.md` | **So sánh** - So sánh schema cũ và schema mới |
| `KIEM_TRA_CHUC_NANG.md` | **Kiểm tra** - Xác nhận schema hỗ trợ đầy đủ chức năng |

---

## 🚀 BẮT ĐẦU NHANH

### **Bước 1: Đọc tài liệu**

1. Đọc `KHUNG_KG_CHUAN.md` để hiểu cấu trúc KG
2. Đọc `SO_SANH_SCHEMA.md` để biết thay đổi so với schema cũ
3. Đọc `KIEM_TRA_CHUC_NANG.md` để xem các chức năng được hỗ trợ

### **Bước 2: Import Schema**

1. Mở GraphDB Desktop
2. Tạo repository mới (hoặc dùng repository hiện có)
3. Import file `kg_schema_chuan.ttl` vào repository

### **Bước 3: Import Dữ liệu**

Import các file TTL theo thứ tự:
1. Schema (`kg_schema_chuan.ttl`) - **PHẢI LÀM TRƯỚC**
2. Skills (`skills.ttl`)
3. Resources (`resources.ttl`)
4. Resource-Skill (`resource_skill.ttl`)
5. Prerequisites (`prerequisites.ttl`)
6. Questions (`question_skill.ttl`)
7. Students (`students.ttl`)
8. Mastery (`mastery.ttl`)
9. Tests và TestResults (nếu có)

---

## 📊 CẤU TRÚC KG

### **Các thực thể chính:**

```
Grade (Khối)
  ├─ Class (Lớp)
  │   ├─ Student (Học sinh)
  │   └─ Teacher (Giáo viên)
  │
  └─ Topic (Chủ đề)
      └─ Lesson (Bài học)
          └─ Question (Câu hỏi)
              └─ Skill (Kỹ năng)
                  └─ Resource (Tài nguyên)
```

### **Quan hệ đánh giá:**

```
Student → takeTest → Test
Test → hasQuestion → Question
Student → hasResult → TestResult → forTest → Test
Student → hasMastery → Mastery → forSkill → Skill
```

### **Quan hệ gợi ý (PPR):**

```
Lesson → recommendedFor → Student
Resource → recommendedResourceFor → Student
```

---

## 🔍 CÁC CHỨC NĂNG HỖ TRỢ

### **1. Đề xuất bài giảng/chương học**

- ✅ Top k theo điểm
- ✅ Bài kiểm tra điểm thấp

**Xem ví dụ query:** `KIEM_TRA_CHUC_NANG.md` - Mục 1

### **2. Đề xuất đề thi**

- ✅ Top k theo điểm
- ✅ Bài kiểm tra điểm thấp

**Xem ví dụ query:** `KIEM_TRA_CHUC_NANG.md` - Mục 2

### **3. Cải tiến phương pháp giảng dạy**

- ✅ Top k theo điểm/xếp loại
- ✅ Phân tích theo lớp
- ✅ Phân tích theo giáo viên

**Xem ví dụ query:** `KIEM_TRA_CHUC_NANG.md` - Mục 3

### **4. Gợi ý dựa trên PPR**

- ✅ Gợi ý bài học
- ✅ Gợi ý tài nguyên

**Xem ví dụ query:** `KIEM_TRA_CHUC_NANG.md` - Mục 4

### **5. Phát hiện học sinh yếu**

- ✅ Dựa trên Mastery (thay thế KNN)

**Xem ví dụ query:** `KIEM_TRA_CHUC_NANG.md` - Mục 5

---

## ⚠️ LƯU Ý QUAN TRỌNG

### **1. Sử dụng KNN**

- ✅ **CÓ** quan hệ `weakInTopic` để xác định học sinh yếu ở chủ đề (KNN)
- ✅ Có thể kết hợp với `Mastery` để xác định học sinh yếu ở kỹ năng

### **2. Chuẩn hóa điểm số**

- Tất cả điểm số được chuẩn hóa về **[0, 1]**
  - 0.0 = 0 điểm
  - 1.0 = điểm tối đa
  - 0.5 = 5.0 điểm (nếu thang 10)

### **3. Namespace**

- **Ontology:** `http://education.vn/ontology#`
- **Data:** `http://education.vn/data/`

### **4. Thứ tự import**

- **BẮT BUỘC:** Import schema trước, dữ liệu sau

---

## 📝 VÍ DỤ QUERY

### **Tìm học sinh yếu ở chủ đề (KNN):**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?studentName ?topic ?topicLabel
WHERE {
  ?student a edu:Student ;
           edu:fullName ?studentName .
  ?student edu:weakInTopic ?topic .
  ?topic edu:label ?topicLabel .
}
ORDER BY ?student ?topic
```

### **Tìm học sinh yếu ở kỹ năng (Mastery):**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?studentName ?skill ?skillName ?score
WHERE {
  ?student a edu:Student ;
           edu:fullName ?studentName .
  ?mastery a edu:Mastery ;
           edu:hasMastery ?student ;
           edu:forSkill ?skill ;
           edu:score ?score .
  ?skill edu:name ?skillName .
  FILTER(?score < 0.5)  # Điểm < 5.0
}
ORDER BY ?student ?score
```

### **Tìm top 5 bài học có điểm cao nhất:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?lesson ?lessonLabel (AVG(?score) AS ?avgScore)
WHERE {
  ?lesson a edu:Lesson ;
          edu:label ?lessonLabel .
  ?result a edu:TestResult ;
          edu:score ?score ;
          edu:forTest ?test .
  ?test edu:hasQuestion ?question .
  ?question edu:belongsToLesson ?lesson .
}
GROUP BY ?lesson ?lessonLabel
ORDER BY DESC(?avgScore)
LIMIT 5
```

---

## 🔄 CHUYỂN ĐỔI TỪ SCHEMA CŨ

Nếu bạn đang dùng schema cũ (`kg_schema_grade7.ttl`), xem hướng dẫn trong `SO_SANH_SCHEMA.md`.

**Các bước chính:**
1. Import schema mới
2. Thêm dữ liệu Mastery
3. Thêm dữ liệu Resource
4. Xóa dữ liệu `weakInTopic` (nếu có)
5. Cập nhật các query SPARQL

---

## ✅ CHECKLIST

- [ ] Đã đọc `KHUNG_KG_CHUAN.md`
- [ ] Đã đọc `SO_SANH_SCHEMA.md` (nếu chuyển từ schema cũ)
- [ ] Đã import schema (`kg_schema_chuan.ttl`)
- [ ] Đã import dữ liệu
- [ ] Đã test các query cơ bản
- [ ] Đã cập nhật code (nếu cần)

---

## 🆘 HỖ TRỢ

Nếu gặp vấn đề:

1. Kiểm tra lại thứ tự import (schema trước, dữ liệu sau)
2. Kiểm tra namespace (phải đúng `http://education.vn/ontology#`)
3. Xem lại các file tài liệu trong thư mục `KG_Design/`

---

## 📚 TÀI LIỆU THAM KHẢO

- **Schema chính:** `kg_schema_chuan.ttl`
- **Tài liệu chi tiết:** `KHUNG_KG_CHUAN.md`
- **So sánh:** `SO_SANH_SCHEMA.md`
- **Kiểm tra chức năng:** `KIEM_TRA_CHUC_NANG.md`

---

**Cập nhật:** 2025-01-15

