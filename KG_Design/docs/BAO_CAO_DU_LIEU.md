# 📊 BÁO CÁO KIỂM TRA DỮ LIỆU - KHUNG KG CHUẨN

## 🎯 TỔNG QUAN

Báo cáo này kiểm tra dữ liệu hiện có và xác định các phần còn thiếu để xây dựng Knowledge Graph chuẩn theo schema `kg_schema_chuan.ttl`.

---

## ✅ DỮ LIỆU ĐÃ CÓ

### **1. Thực thể (Entities)**

| Thực thể | File TTL | Trạng thái | Ghi chú |
|----------|----------|------------|---------|
| **Student** | `students.ttl` | ⚠️ **THIẾU** | Có `studentId`, thiếu `fullName`, thiếu `belongsToClass` |
| **Teacher** | `teachers_assignments.ttl` | ✅ **ĐỦ** | Có đầy đủ thuộc tính và quan hệ `teaches` |
| **Class** | `teachers_assignments.ttl` | ⚠️ **THIẾU** | Có IRI nhưng thiếu thuộc tính `className`, thiếu `belongsToGrade` |
| **Skill** | `skills.ttl` | ✅ **ĐỦ** | Có đầy đủ thuộc tính |
| **Resource** | `resources.ttl` | ✅ **ĐỦ** | Có đầy đủ thuộc tính |
| **Mastery** | `mastery.ttl` | ✅ **ĐỦ** | Có đầy đủ thuộc tính và quan hệ |

### **2. Quan hệ (Relationships)**

| Quan hệ | File TTL | Trạng thái | Ghi chú |
|---------|----------|------------|---------|
| `teaches` | `teachers_assignments.ttl` | ✅ **ĐỦ** | Teacher → Class |
| `coversSkill` | `resource_skill.ttl` | ✅ **ĐỦ** | Resource → Skill |
| `prerequisiteOf` | `prerequisites.ttl` | ✅ **ĐỦ** | Skill → Skill |
| `requiresSkill` | `question_skill.ttl` | ⚠️ **SAI** | Dùng `measures` thay vì `requiresSkill` |
| `hasMastery` | `mastery.ttl` | ✅ **ĐỦ** | Student → Mastery |
| `forSkill` | `mastery.ttl` | ✅ **ĐỦ** | Mastery → Skill |

---

## ❌ DỮ LIỆU CÒN THIẾU

### **1. Thực thể (Entities)**

| Thực thể | Trạng thái | Cần bổ sung |
|----------|------------|-------------|
| **Grade** | ❌ **THIẾU HOÀN TOÀN** | Tạo file `grades.ttl` với các khối 6, 7, 8, 9 |
| **Topic** | ❌ **THIẾU HOÀN TOÀN** | Tạo file `topics.ttl` với các chủ đề A, B, C, D, E, F cho từng khối |
| **Lesson** | ❌ **THIẾU HOÀN TOÀN** | Tạo file `lessons.ttl` với các bài học (A1, A2, B1, ...) |
| **Question** | ⚠️ **THIẾU THUỘC TÍNH** | Có IRI nhưng thiếu `questionText`, `difficulty`, `correctOption`, `belongsToLesson` |
| **Test** | ❌ **THIẾU HOÀN TOÀN** | Tạo file `tests.ttl` từ `assessments.csv` |
| **TestResult** | ❌ **THIẾU HOÀN TOÀN** | Tạo file `test_results.ttl` từ `student_assessment.csv` |

### **2. Quan hệ (Relationships)**

| Quan hệ | Trạng thái | Cần bổ sung |
|---------|------------|-------------|
| `belongsToClass` | ❌ **THIẾU** | Student → Class |
| `belongsToGrade` | ❌ **THIẾU** | Class → Grade |
| `forGrade` | ❌ **THIẾU** | Topic → Grade |
| `belongsToTopic` | ❌ **THIẾU** | Lesson → Topic |
| `belongsToLesson` | ❌ **THIẾU** | Question → Lesson |
| `hasQuestion` | ❌ **THIẾU** | Test → Question |
| `takeTest` | ❌ **THIẾU** | Student → Test |
| `hasResult` | ❌ **THIẾU** | Student → TestResult |
| `forTest` | ❌ **THIẾU** | TestResult → Test |
| `weakInTopic` | ❌ **THIẾU** | Student → Topic (KNN) |
| `recommendedFor` | ❌ **THIẾU** | Lesson → Student (PPR) |
| `recommendedResourceFor` | ❌ **THIẾU** | Resource → Student (PPR) |

### **3. Thuộc tính còn thiếu**

| Thực thể | Thuộc tính thiếu |
|----------|-----------------|
| **Student** | `fullName`, liên kết `belongsToClass` |
| **Class** | `className`, liên kết `belongsToGrade` |
| **Question** | `questionText`, `difficulty`, `correctOption`, `belongsToLesson` |

---

## 📋 DANH SÁCH CẦN BỔ SUNG

### **A. DỮ LIỆU CƠ BẢN (BẮT BUỘC)**

#### **1. Grades (Khối lớp)**
- **File:** `grades.ttl`
- **Nội dung:** Tạo 4 khối: 6, 7, 8, 9
- **Ví dụ:**
  ```turtle
  data:grade_6 a edu:Grade ; edu:grade 6 .
  data:grade_7 a edu:Grade ; edu:grade 7 .
  data:grade_8 a edu:Grade ; edu:grade 8 .
  data:grade_9 a edu:Grade ; edu:grade 9 .
  ```

#### **2. Topics (Chủ đề)**
- **File:** `topics.ttl`
- **Nội dung:** Tạo các chủ đề cho từng khối
- **Khối 6:** A, B, C, D, E, F
- **Khối 7:** A, B, C, D, E, F
- **Ví dụ:**
  ```turtle
  data:topic_6_A a edu:Topic ;
    edu:topicId "A" ;
    edu:label "Chủ đề A: Máy tính và cộng đồng" ;
    edu:grade 6 ;
    edu:forGrade data:grade_6 .
  ```

#### **3. Lessons (Bài học)**
- **File:** `lessons.ttl`
- **Nội dung:** Tạo các bài học cho từng chủ đề
- **Khối 6:** A1-A5, B1-B4, C1-C6, D1-D3, E1-E8, F1-F5
- **Ví dụ:**
  ```turtle
  data:lesson_6_A1 a edu:Lesson ;
    edu:lessonId "A1" ;
    edu:label "Bài A1: Thông tin và xử lí" ;
    edu:belongsToTopic data:topic_6_A .
  ```

#### **4. Questions (Câu hỏi) - Bổ sung thuộc tính**
- **File:** `questions.ttl` (hoặc cập nhật `question_skill.ttl`)
- **Cần bổ sung:**
  - `questionText` - Nội dung câu hỏi
  - `difficulty` - Độ khó
  - `correctOption` - Đáp án đúng
  - `belongsToLesson` - Liên kết với bài học
  - Đổi `measures` thành `requiresSkill`

#### **5. Classes (Lớp học) - Bổ sung thuộc tính**
- **File:** `classes.ttl` (hoặc cập nhật `teachers_assignments.ttl`)
- **Cần bổ sung:**
  - `className` - Tên lớp (6/1, 6/2, ...)
  - `belongsToGrade` - Liên kết với khối

#### **6. Students - Bổ sung thuộc tính**
- **File:** Cập nhật `students.ttl`
- **Cần bổ sung:**
  - `fullName` - Họ và tên
  - `belongsToClass` - Liên kết với lớp

#### **7. Tests (Bài kiểm tra)**
- **File:** `tests.ttl`
- **Nguồn:** `assessments.csv`
- **Nội dung:** Chuyển đổi từ CSV sang TTL
- **Ví dụ:**
  ```turtle
  data:test_ASSESS_K6_A1_2024 a edu:Test ;
    edu:testId "ASSESS_K6_A1_2024" ;
    edu:testName "Kiểm tra Chủ đề A1" .
  ```

#### **8. TestResults (Kết quả)**
- **File:** `test_results.ttl`
- **Nguồn:** `student_assessment.csv`
- **Nội dung:** Chuyển đổi từ CSV sang TTL
- **Ví dụ:**
  ```turtle
  data:result_2324_0001_ASSESS_K6_A1_2024 a edu:TestResult ;
    edu:score "0.7"^^xsd:decimal ;
    edu:testDate "2024-09-15T00:00:00"^^xsd:dateTime ;
    edu:forTest data:test_ASSESS_K6_A1_2024 .
  
  data:student_2324_0001 edu:hasResult data:result_2324_0001_ASSESS_K6_A1_2024 .
  data:student_2324_0001 edu:takeTest data:test_ASSESS_K6_A1_2024 .
  ```

---

### **B. DỮ LIỆU ML (TÙY CHỌN - TẠO SAU)**

#### **9. weakInTopic (KNN)**
- **File:** `weak_in_topic.ttl`
- **Nội dung:** Quan hệ Student → Topic (được tạo bởi thuật toán KNN)
- **Ví dụ:**
  ```turtle
  data:student_2324_0001 edu:weakInTopic data:topic_6_A .
  ```

#### **10. recommendedFor (PPR)**
- **File:** `recommended_lessons.ttl`
- **Nội dung:** Quan hệ Lesson → Student (được tạo bởi thuật toán PPR)
- **Ví dụ:**
  ```turtle
  data:lesson_6_A1 edu:recommendedFor data:student_2324_0001 .
  ```

#### **11. recommendedResourceFor (PPR)**
- **File:** `recommended_resources.ttl`
- **Nội dung:** Quan hệ Resource → Student (được tạo bởi thuật toán PPR)
- **Ví dụ:**
  ```turtle
  data:resource_R_K6_A1_HTML edu:recommendedResourceFor data:student_2324_0001 .
  ```

---

## 🔧 CÁC SCRIPT CẦN TẠO/CẬP NHẬT

### **1. Script tạo Grades**
- **File:** `KG_Design/grade6/build_grades.py`
- **Chức năng:** Tạo file `grades.ttl` với 4 khối

### **2. Script tạo Topics**
- **File:** `KG_Design/grade6/build_topics.py`
- **Chức năng:** Tạo file `topics.ttl` từ danh sách chủ đề

### **3. Script tạo Lessons**
- **File:** `KG_Design/grade6/build_lessons.py`
- **Chức năng:** Tạo file `lessons.ttl` từ danh sách bài học

### **4. Script cập nhật Questions**
- **File:** `KG_Design/grade6/update_questions.py`
- **Chức năng:** 
  - Đọc từ file câu hỏi gốc
  - Bổ sung thuộc tính: `questionText`, `difficulty`, `correctOption`
  - Thêm quan hệ `belongsToLesson`
  - Đổi `measures` thành `requiresSkill`

### **5. Script tạo Classes**
- **File:** `KG_Design/grade6/build_classes.py`
- **Chức năng:** 
  - Tạo file `classes.ttl`
  - Bổ sung `className` và `belongsToGrade`

### **6. Script cập nhật Students**
- **File:** `KG_Design/grade6/update_students.py`
- **Chức năng:**
  - Đọc từ `students_grade_data.json`
  - Bổ sung `fullName` và `belongsToClass`

### **7. Script tạo Tests**
- **File:** `KG_Design/grade6/build_tests.py`
- **Chức năng:** Chuyển đổi `assessments.csv` → `tests.ttl`

### **8. Script tạo TestResults**
- **File:** `KG_Design/grade6/build_test_results.py`
- **Chức năng:** Chuyển đổi `student_assessment.csv` → `test_results.ttl`

---

## 📊 TÓM TẮT THEO ĐỘ ƯU TIÊN

### **🔴 ƯU TIÊN CAO (Bắt buộc để KG hoạt động)**

1. ✅ **Grades** - Khối lớp
2. ✅ **Topics** - Chủ đề
3. ✅ **Lessons** - Bài học
4. ✅ **Questions** - Bổ sung thuộc tính và quan hệ
5. ✅ **Classes** - Bổ sung thuộc tính và quan hệ
6. ✅ **Students** - Bổ sung thuộc tính và quan hệ
7. ✅ **Tests** - Bài kiểm tra
8. ✅ **TestResults** - Kết quả

### **🟡 ƯU TIÊN TRUNG BÌNH (Cần cho chức năng đầy đủ)**

9. ⚠️ **weakInTopic** - KNN (có thể tạo sau khi có đủ dữ liệu)
10. ⚠️ **recommendedFor** - PPR (có thể tạo sau khi có đủ dữ liệu)
11. ⚠️ **recommendedResourceFor** - PPR (có thể tạo sau khi có đủ dữ liệu)

---

## ✅ CHECKLIST

### **Dữ liệu cơ bản:**
- [ ] Tạo `grades.ttl`
- [ ] Tạo `topics.ttl`
- [ ] Tạo `lessons.ttl`
- [ ] Cập nhật `questions.ttl` (bổ sung thuộc tính)
- [ ] Tạo/cập nhật `classes.ttl` (bổ sung thuộc tính)
- [ ] Cập nhật `students.ttl` (bổ sung thuộc tính)
- [ ] Tạo `tests.ttl`
- [ ] Tạo `test_results.ttl`

### **Dữ liệu ML (tùy chọn):**
- [ ] Tạo `weak_in_topic.ttl` (KNN)
- [ ] Tạo `recommended_lessons.ttl` (PPR)
- [ ] Tạo `recommended_resources.ttl` (PPR)

---

## 🎯 KẾT LUẬN

**Dữ liệu hiện tại:**
- ✅ Có: Skills, Resources, Resource-Skill, Prerequisites, Mastery, Teachers
- ⚠️ Thiếu một phần: Students, Classes, Questions
- ❌ Thiếu hoàn toàn: Grades, Topics, Lessons, Tests, TestResults

**Cần bổ sung ngay:**
1. 8 file TTL cơ bản (ưu tiên cao)
2. 3 file TTL ML (ưu tiên trung bình, có thể tạo sau)

**Tổng cộng cần tạo/cập nhật: 11 file TTL**

---

**Cập nhật:** 2025-01-15

