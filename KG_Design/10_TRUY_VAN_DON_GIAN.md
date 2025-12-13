# 🔍 10 TRUY VẤN SPARQL ĐƠN GIẢN

> Các truy vấn cơ bản để bắt đầu với Knowledge Graph  
> Sử dụng trong GraphDB Desktop - Repository: `tinhocthcs`

---

## 📋 LƯU Ý TRƯỚC KHI CHẠY

1. **Prefix:** GraphDB có thể đã có prefix `edu:` và `data:` sẵn, nếu báo lỗi "Multiple prefix declarations", hãy xóa dòng `PREFIX edu:` và `PREFIX data:`
2. **Repository:** Đảm bảo đã chọn đúng repository `tinhocthcs`
3. **Dữ liệu:** Đảm bảo đã upload đầy đủ các tầng A-E

---

## 1️⃣ LIỆT KÊ TẤT CẢ HỌC SINH

**Mục đích:** Xem danh sách tất cả học sinh trong hệ thống

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?studentId ?fullName ?className
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:belongsToClass ?classIRI .
  ?classIRI edu:className ?className
}
ORDER BY ?className ?studentId
LIMIT 50
```

**Kết quả mong đợi:** Danh sách học sinh với mã, tên, và lớp

---

## 2️⃣ LIỆT KÊ TẤT CẢ LỚP HỌC

**Mục đích:** Xem danh sách tất cả lớp học

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?class ?className ?grade
WHERE {
  ?class a edu:Class ;
         edu:className ?className ;
         edu:belongsToGrade ?gradeIRI .
  ?gradeIRI edu:grade ?grade
}
ORDER BY ?grade ?className
```

**Kết quả mong đợi:** Danh sách lớp học (6_1, 6_2, 7_1, ...) và khối

---

## 3️⃣ LIỆT KÊ TẤT CẢ BÀI HỌC

**Mục đích:** Xem danh sách tất cả bài học

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?lesson ?lessonId ?label ?topicLabel
WHERE {
  ?lesson a edu:Lesson ;
          edu:lessonId ?lessonId ;
          edu:label ?label ;
          edu:belongsToTopic ?topicIRI .
  ?topicIRI edu:label ?topicLabel
}
ORDER BY ?lessonId
```

**Kết quả mong đợi:** Danh sách bài học (6_A1, 6_A2, ...) và chủ đề

---

## 4️⃣ TÌM HỌC SINH THEO LỚP

**Mục đích:** Tìm tất cả học sinh của một lớp cụ thể

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?studentId ?fullName
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:belongsToClass data:class_6_1
}
ORDER BY ?studentId
```

**Lưu ý:** Thay `data:class_6_1` bằng lớp bạn muốn tìm (ví dụ: `data:class_7_2`)

**Kết quả mong đợi:** Danh sách học sinh của lớp 6_1

---

## 5️⃣ TÌM CÂU HỎI THEO BÀI HỌC

**Mục đích:** Xem tất cả câu hỏi của một bài học cụ thể

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?question ?q_id ?questionText
WHERE {
  ?question a edu:Question ;
            edu:q_id ?q_id ;
            edu:questionText ?questionText ;
            edu:belongsToLesson data:lesson_6_A1
}
ORDER BY ?q_id
```

**Lưu ý:** Thay `data:lesson_6_A1` bằng bài học bạn muốn tìm

**Kết quả mong đợi:** Danh sách câu hỏi của bài 6_A1

---

## 6️⃣ TÌM KỸ NĂNG THEO CÂU HỎI

**Mục đích:** Xem câu hỏi yêu cầu kỹ năng gì

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?question ?q_id ?skill ?skillId ?skillName
WHERE {
  ?question a edu:Question ;
            edu:q_id ?q_id ;
            edu:requiresSkill ?skill .
  ?skill edu:skillId ?skillId ;
         edu:name ?skillName
}
ORDER BY ?q_id
LIMIT 20
```

**Kết quả mong đợi:** Mapping câu hỏi - kỹ năng

---

## 7️⃣ TÌM KẾT QUẢ KIỂM TRA CỦA HỌC SINH

**Mục đích:** Xem điểm kiểm tra của một học sinh

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?studentId ?fullName ?test ?testName ?score ?testDate
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:hasResult ?result .
  ?result edu:forTest ?test ;
          edu:score ?score ;
          edu:testDate ?testDate .
  ?test edu:testName ?testName
}
ORDER BY ?testDate DESC
LIMIT 20
```

**Kết quả mong đợi:** Danh sách kết quả kiểm tra với điểm và ngày

---

## 8️⃣ TÌM MỨC ĐỘ THÀNH THẠO CỦA HỌC SINH

**Mục đích:** Xem mức độ thành thạo kỹ năng của học sinh

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?studentId ?fullName ?skill ?skillId ?skillName ?score ?lastUpdated
WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId ;
           edu:fullName ?fullName ;
           edu:hasMastery ?mastery .
  ?mastery edu:forSkill ?skill ;
           edu:score ?score ;
           edu:lastUpdated ?lastUpdated .
  ?skill edu:skillId ?skillId ;
         edu:name ?skillName
}
ORDER BY ?studentId ?skillId
LIMIT 30
```

**Kết quả mong đợi:** Mức độ thành thạo (0.0-1.0) của học sinh với từng kỹ năng

---

## 9️⃣ TÌM GIÁO VIÊN DẠY LỚP NÀO

**Mục đích:** Xem giáo viên nào dạy lớp nào

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?teacher ?teacherId ?fullName ?class ?className
WHERE {
  ?teacher a edu:Teacher ;
           edu:teacherId ?teacherId ;
           edu:fullName ?fullName ;
           edu:teaches ?class .
  ?class edu:className ?className
}
ORDER BY ?teacherId ?className
```

**Kết quả mong đợi:** Danh sách phân công giáo viên - lớp

---

## 🔟 ĐẾM SỐ LƯỢNG THỰC THỂ

**Mục đích:** Thống kê tổng quan số lượng dữ liệu

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT 
  (COUNT(DISTINCT ?student) as ?soHocSinh)
  (COUNT(DISTINCT ?teacher) as ?soGiaoVien)
  (COUNT(DISTINCT ?class) as ?soLop)
  (COUNT(DISTINCT ?lesson) as ?soBaiHoc)
  (COUNT(DISTINCT ?question) as ?soCauHoi)
  (COUNT(DISTINCT ?skill) as ?soKyNang)
  (COUNT(DISTINCT ?test) as ?soBaiKiemTra)
  (COUNT(DISTINCT ?result) as ?soKetQua)
WHERE {
  { ?student a edu:Student }
  UNION { ?teacher a edu:Teacher }
  UNION { ?class a edu:Class }
  UNION { ?lesson a edu:Lesson }
  UNION { ?question a edu:Question }
  UNION { ?skill a edu:Skill }
  UNION { ?test a edu:Test }
  UNION { ?result a edu:TestResult }
}
```

**Kết quả mong đợi:** Bảng thống kê với 8 số liệu

---

## 📝 HƯỚNG DẪN SỬ DỤNG

### Cách chạy query trong GraphDB Desktop:

1. **Mở GraphDB Desktop**
2. **Chọn repository:** `tinhocthcs`
3. **Vào tab "SPARQL"**
4. **Copy query** vào ô editor
5. **Nhấn "Run"** hoặc `Ctrl + Enter`
6. **Xem kết quả** ở tab "Table" hoặc "Graph"

### Lưu ý:

- **Nếu báo lỗi "Multiple prefix declarations":**
  - Xóa 2 dòng `PREFIX edu:` và `PREFIX data:`
  - GraphDB có thể đã có prefix sẵn

- **Nếu không có kết quả:**
  - Kiểm tra đã upload đầy đủ dữ liệu chưa
  - Kiểm tra URI có đúng không (ví dụ: `data:class_6_1` thay vì `data:class/6_1`)

- **Để tìm URI chính xác:**
  - Chạy query 1, 2, 3 trước để xem các URI có sẵn
  - Copy URI từ kết quả để dùng trong query khác

---

## 🎯 QUERIES NÂNG CAO (Tham khảo)

Nếu muốn các query phức tạp hơn, xem file:
- `KG_Design/QUERIES_MAU_HUU_ICH.md`

---

**Cập nhật:** 2025-01-15  
**Repository:** `tinhocthcs`  
**Schema:** `KG_Design/schema/kg_schema_chuan.ttl`

