# 📊 KHUNG KNOWLEDGE GRAPH CHUẨN - TIN HỌC THCS

## 🎯 TỔNG QUAN

Tài liệu này mô tả khung Knowledge Graph chuẩn cho hệ thống hỗ trợ giáo viên THCS nâng cao chất lượng giảng dạy Tin học, dựa trên **Đề cương Đề án 2**.

---

## 📋 MỤC TIÊU

Khung KG này được thiết kế để:

1. **Mô hình hóa dữ liệu học tập** thành đồ thị tri thức
2. **Phân tích, thống kê và trích xuất thông tin** có giá trị từ KG phục vụ giảng dạy
3. **Đề xuất các giải pháp cải tiến** bài giảng, đề kiểm tra và phương pháp giảng dạy dựa trên dữ liệu
4. **Hỗ trợ Personalized PageRank (PPR)** để gợi ý bài học/tài nguyên phù hợp

---

## 📦 CÁC THỰC THỂ (ENTITIES/CLASSES)

### 1. **Student** (Học sinh)
- **Thuộc tính:**
  - `studentId` (string) - Mã học sinh (unique)
  - `fullName` (string) - Họ và tên
- **Quan hệ:**
  - `belongsToClass` → Class
  - `takeTest` → Test
  - `hasResult` → TestResult
  - `hasMastery` → Mastery
  - `weakInTopic` → Topic (KNN)
  - `recommendedFor` ← Lesson (PPR)
  - `recommendedResourceFor` ← Resource (PPR)

### 2. **Teacher** (Giáo viên)
- **Thuộc tính:**
  - `teacherId` (string) - Mã giáo viên (unique)
  - `fullName` (string) - Họ và tên
  - `expertise` (string) - Chuyên môn
- **Quan hệ:**
  - `teaches` → Class

### 3. **Class** (Lớp học)
- **Thuộc tính:**
  - `className` (string) - Tên lớp (ví dụ: "6/14", "7/19")
- **Quan hệ:**
  - `belongsToGrade` → Grade
  - `belongsToClass` ← Student
  - `teaches` ← Teacher

### 4. **Grade** (Khối lớp)
- **Thuộc tính:**
  - `grade` (integer) - Số khối (6, 7, 8, 9)
- **Quan hệ:**
  - `belongsToGrade` ← Class
  - `forGrade` ← Topic

### 5. **Topic** (Chủ đề)
- **Thuộc tính:**
  - `topicId` (string) - Mã chủ đề (A, B, C, D, E, F)
  - `label` (string) - Tên chủ đề (ví dụ: "Chủ đề A: Máy tính và cộng đồng")
  - `grade` (integer) - Khối lớp
- **Quan hệ:**
  - `forGrade` → Grade
  - `belongsToTopic` ← Lesson
  - `weakInTopic` ← Student (KNN)

### 6. **Lesson** (Bài học)
- **Thuộc tính:**
  - `lessonId` (string) - Mã bài học (A1, A2, B1, ...)
  - `label` (string) - Tên bài học (ví dụ: "Bài A1: Thông tin và xử lí")
- **Quan hệ:**
  - `belongsToTopic` → Topic
  - `belongsToLesson` ← Question
  - `recommendedFor` → Student (PPR)

### 7. **Question** (Câu hỏi)
- **Thuộc tính:**
  - `q_id` (string) - Mã câu hỏi (ví dụ: "K6A1_01")
  - `questionText` (string) - Nội dung câu hỏi
  - `difficulty` (string) - Độ khó: "Nhận biết", "Thông hiểu", "Vận dụng"
  - `correctOption` (string) - Đáp án đúng (A, B, C, D)
- **Quan hệ:**
  - `belongsToLesson` → Lesson
  - `requiresSkill` → Skill
  - `hasQuestion` ← Test

### 8. **Skill** (Kỹ năng)
- **Thuộc tính:**
  - `skillId` (string) - Mã kỹ năng (unique)
  - `name` (string) - Tên kỹ năng
  - `bloomLevel` (string) - Mức độ Bloom: "Nhận biết", "Thông hiểu", "Vận dụng"
  - `domain` (string) - Lĩnh vực
  - `grade` (integer) - Khối lớp
- **Quan hệ:**
  - `prerequisiteOf` → Skill (Skill này là tiên quyết của Skill kia)
  - `requiresSkill` ← Question
  - `coversSkill` ← Resource
  - `forSkill` ← Mastery

### 9. **Resource** (Tài nguyên học tập)
- **Thuộc tính:**
  - `resId` (string) - Mã tài nguyên (unique)
  - `title` (string) - Tiêu đề
  - `mediaType` (string) - Loại: "html", "video", "pdf", "quiz", "exercise"
  - `url` (string) - Đường dẫn (ví dụ: "Web/K6_A1.html")
  - `difficulty` (string) - Độ khó
  - `duration` (integer) - Thời lượng (phút)
  - `grade` (integer) - Khối lớp
- **Quan hệ:**
  - `coversSkill` → Skill (với coverage 0.0-1.0)
  - `recommendedResourceFor` → Student (PPR)

### 10. **Test** (Bài kiểm tra)
- **Thuộc tính:**
  - `testId` (string) - Mã bài kiểm tra
  - `testName` (string) - Tên bài kiểm tra
- **Quan hệ:**
  - `hasQuestion` → Question
  - `takeTest` ← Student
  - `forTest` ← TestResult

### 11. **TestResult** (Kết quả làm bài)
- **Thuộc tính:**
  - `score` (decimal) - Điểm số (0.0-1.0, đã chuẩn hóa)
  - `duration` (integer) - Thời gian làm bài (giây)
  - `testDate` (dateTime) - Ngày làm bài
- **Quan hệ:**
  - `forTest` → Test
  - `hasResult` ← Student

### 12. **Mastery** (Mức độ thành thạo)
- **Thuộc tính:**
  - `score` (decimal) - Điểm thành thạo (0.0-1.0)
  - `lastUpdated` (date) - Ngày cập nhật cuối
- **Quan hệ:**
  - `forSkill` → Skill
  - `hasMastery` ← Student

---

## 🔗 QUAN HỆ CHÍNH (RELATIONSHIPS)

### **Quan hệ phân cấp tổ chức:**
```
Grade
  ├─ Class (belongsToGrade)
  │   ├─ Student (belongsToClass)
  │   └─ Teacher (teaches)
  │
  └─ Topic (forGrade)
      └─ Lesson (belongsToTopic)
          └─ Question (belongsToLesson)
```

### **Quan hệ kỹ năng và tri thức:**
```
Skill ← prerequisiteOf → Skill (quan hệ tiên quyết)
Resource → coversSkill → Skill (với coverage)
Question → requiresSkill → Skill
Student → hasMastery → Mastery → forSkill → Skill
```

### **Quan hệ đánh giá:**
```
Student → takeTest → Test
Test → hasQuestion → Question
Student → hasResult → TestResult → forTest → Test
```

### **Quan hệ ML (Machine Learning):**
```
Student → weakInTopic → Topic  (KNN phát hiện)
Lesson → recommendedFor → Student  (PPR gợi ý bài học)
Resource → recommendedResourceFor → Student  (PPR gợi ý tài nguyên)
```

---

## 📊 SƠ ĐỒ QUAN HỆ TỔNG QUAN

```
                    ┌─────────┐
                    │  Grade  │
                    └────┬────┘
                         │
            ┌────────────┼────────────┐
            │                        │
      ┌─────▼─────┐          ┌───────▼──────┐
      │   Class  │          │    Topic     │
      └─────┬────┘          └───────┬──────┘
            │                        │
      ┌─────▼─────┐          ┌───────▼──────┐
      │  Student  │          │    Lesson    │
      └─────┬────┘          └───────┬──────┘
            │                        │
            │                ┌───────▼──────┐
            │                │   Question   │
            │                └───────┬──────┘
            │                        │
            │                ┌───────▼──────┐
            │                │    Skill      │
            │                └───────┬──────┘
            │                        │
            │                ┌───────▼──────┐
            │                │   Resource   │
            │                └──────────────┘
            │
      ┌─────▼────────┐
      │   Mastery    │
      └──────────────┘

         ┌─────────┐       ┌──────────┐
         │   Test  │──────►│ Question │
         └────┬────┘       └──────────┘
              │
         ┌────▼────────┐
         │  TestResult │
         └────────────┘
```

---

## 🎯 CÁC CHỨC NĂNG HỖ TRỢ

### **1. Đề xuất bài giảng/chương học**
- **Top k theo điểm:** Tìm các bài học có điểm trung bình cao nhất
- **Bài kiểm tra điểm thấp:** Tìm các bài học liên quan đến bài kiểm tra có điểm thấp

**SPARQL ví dụ:**
```sparql
# Tìm top 5 bài học có điểm trung bình cao nhất
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?lesson ?label (AVG(?score) AS ?avgScore)
WHERE {
  ?lesson a edu:Lesson ;
          edu:label ?label .
  ?result edu:forTest ?test .
  ?test edu:hasQuestion ?question .
  ?question edu:belongsToLesson ?lesson .
  ?result edu:score ?score .
}
GROUP BY ?lesson ?label
ORDER BY DESC(?avgScore)
LIMIT 5
```

### **2. Đề xuất đề thi**
- **Top k theo điểm:** Tìm các đề thi có điểm trung bình cao nhất
- **Bài kiểm tra điểm thấp:** Tìm các đề thi có điểm thấp để cải tiến

**SPARQL ví dụ:**
```sparql
# Tìm các đề thi có điểm trung bình thấp (< 5.0)
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?test ?testName (AVG(?score) AS ?avgScore) (COUNT(?result) AS ?numStudents)
WHERE {
  ?test a edu:Test ;
        edu:testName ?testName .
  ?result edu:forTest ?test ;
          edu:score ?score .
  FILTER(?score < 0.5)  # < 5.0 điểm (chuẩn hóa)
}
GROUP BY ?test ?testName
HAVING (AVG(?score) < 0.5)
ORDER BY ASC(?avgScore)
```

### **3. Cải tiến phương pháp giảng dạy**
- **Top k theo điểm/xếp loại:** Phân tích hiệu quả giảng dạy theo lớp, giáo viên

**SPARQL ví dụ:**
```sparql
# Phân tích hiệu quả giảng dạy theo lớp
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?class ?className 
       (AVG(?score) AS ?avgScore)
       (COUNT(DISTINCT ?student) AS ?numStudents)
WHERE {
  ?class a edu:Class ;
         edu:className ?className .
  ?student edu:belongsToClass ?class .
  ?result edu:hasResult ?student ;
          edu:score ?score .
}
GROUP BY ?class ?className
ORDER BY DESC(?avgScore)
```

### **4. Gợi ý dựa trên PPR (Personalized PageRank)**
- **Gợi ý bài học:** Dựa trên mức độ thành thạo kỹ năng của học sinh
- **Gợi ý tài nguyên:** Dựa trên kỹ năng cần cải thiện

**SPARQL ví dụ:**
```sparql
# Tìm các bài học được gợi ý cho học sinh (đã được PPR tính toán)
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?studentName ?lesson ?lessonLabel
WHERE {
  ?student a edu:Student ;
           edu:fullName ?studentName .
  ?lesson edu:recommendedFor ?student ;
          edu:label ?lessonLabel .
}
ORDER BY ?student ?lesson
```

---

## 📝 LƯU Ý QUAN TRỌNG

### **1. Sử dụng KNN**
- ✅ Sử dụng quan hệ `weakInTopic` để xác định học sinh yếu ở chủ đề
- Quan hệ này được tạo bởi thuật toán KNN (k-Nearest Neighbors)
- Có thể kết hợp với `Mastery` để có cái nhìn toàn diện hơn:
  ```sparql
  # Tìm học sinh yếu ở chủ đề (KNN)
  SELECT ?student ?topic ?topicLabel
  WHERE {
    ?student edu:weakInTopic ?topic .
    ?topic edu:label ?topicLabel .
  }
  ```

### **2. Sử dụng PPR**
- Quan hệ `recommendedFor` và `recommendedResourceFor` được tính toán bởi PPR
- PPR hoạt động trên cấu trúc đồ thị để tìm các nút quan trọng nhất từ điểm khởi đầu

### **3. Chuẩn hóa điểm số**
- Tất cả điểm số trong KG được **chuẩn hóa về [0, 1]**
  - 0.0 = 0 điểm
  - 1.0 = điểm tối đa
  - 0.5 = 5.0 điểm (nếu thang 10)

### **4. Namespace**
- **Ontology:** `http://education.vn/ontology#`
- **Data:** `http://education.vn/data/`

---

## ✅ KIỂM TRA SCHEMA

### **Các thực thể cần có:**
- [x] Student (Học sinh)
- [x] Teacher (Giáo viên)
- [x] Class (Lớp)
- [x] Grade (Khối)
- [x] Topic (Chủ đề)
- [x] Lesson (Bài học)
- [x] Question (Câu hỏi)
- [x] Skill (Kỹ năng)
- [x] Resource (Tài nguyên)
- [x] Test (Bài kiểm tra)
- [x] TestResult (Kết quả)
- [x] Mastery (Mức độ thành thạo)

### **Các quan hệ cần có:**
- [x] Student → belongsToClass → Class
- [x] Class → belongsToGrade → Grade
- [x] Teacher → teaches → Class
- [x] Lesson → belongsToTopic → Topic
- [x] Topic → forGrade → Grade
- [x] Question → belongsToLesson → Lesson
- [x] Question → requiresSkill → Skill
- [x] Resource → coversSkill → Skill
- [x] Skill → prerequisiteOf → Skill
- [x] Student → takeTest → Test
- [x] Test → hasQuestion → Question
- [x] Student → hasResult → TestResult
- [x] TestResult → forTest → Test
- [x] Student → hasMastery → Mastery
- [x] Mastery → forSkill → Skill
- [x] Student → weakInTopic → Topic (KNN)
- [x] Lesson → recommendedFor → Student (PPR)
- [x] Resource → recommendedResourceFor → Student (PPR)

---

## 🎯 FILE THAM KHẢO

- **Schema chính:** `KG_Design/kg_schema_chuan.ttl`
- **Tài liệu này:** `KG_Design/KHUNG_KG_CHUAN.md`
- **Schema cũ (có KNN):** `KG_Design/kg_schema_grade7.ttl`

---

**Cập nhật:** 2025-01-15

