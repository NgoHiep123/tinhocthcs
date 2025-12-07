# 📋 TÓM TẮT NGẮN - `kg_schema_chuan.ttl`

## 🎯 MỤC ĐÍCH

File schema định nghĩa **cấu trúc** của Knowledge Graph - giống như "bản thiết kế" cho toàn bộ dữ liệu.

---

## 📊 CẤU TRÚC TỔNG QUAN

### **12 CLASSES (Thực thể)**

| Class | Tiếng Việt | Ví dụ |
|-------|------------|-------|
| `edu:Student` | Học sinh | HS001, HS002... |
| `edu:Teacher` | Giáo viên | GV001, GV002... |
| `edu:Class` | Lớp học | 6A, 6B, 7A... |
| `edu:Grade` | Khối lớp | Khối 6, 7, 8, 9 |
| `edu:Topic` | Chủ đề | Topic A, B, C... |
| `edu:Lesson` | Bài học | A1, A2, B1... |
| `edu:Question` | Câu hỏi | Q001, Q002... |
| `edu:Skill` | Kỹ năng | Nhận biết, Thông hiểu... |
| `edu:Resource` | Tài nguyên | Video, PDF, HTML... |
| `edu:Test` | Bài kiểm tra | Test 1, Test 2... |
| `edu:TestResult` | Kết quả | Kết quả của học sinh |
| `edu:Mastery` | Mức độ thành thạo | 0.0 - 1.0 |

---

### **17 RELATIONSHIPS (Quan hệ chính)**

#### **Cấu trúc phân cấp:**
- `belongsToClass` - Học sinh → Lớp
- `belongsToGrade` - Lớp → Khối
- `belongsToTopic` - Bài học → Chủ đề
- `belongsToLesson` - Câu hỏi → Bài học
- `forGrade` - Chủ đề → Khối

#### **Giảng dạy:**
- `teaches` - Giáo viên → Lớp

#### **Nội dung học tập:**
- `requiresSkill` - Câu hỏi → Kỹ năng
- `coversSkill` - Tài nguyên → Kỹ năng
- `prerequisiteOf` - Kỹ năng → Kỹ năng (tiên quyết)

#### **Kiểm tra:**
- `takeTest` - Học sinh → Bài kiểm tra
- `hasQuestion` - Bài kiểm tra → Câu hỏi
- `hasResult` - Học sinh → Kết quả
- `forTest` - Kết quả → Bài kiểm tra

#### **Mastery:**
- `hasMastery` - Học sinh → Mức độ thành thạo
- `forSkill` - Mastery → Kỹ năng

#### **AI/ML (Tự động tạo):**
- `weakInTopic` - Học sinh → Chủ đề (KNN phát hiện)
- `recommendedFor` - Bài học → Học sinh (PPR gợi ý)
- `recommendedResourceFor` - Tài nguyên → Học sinh (PPR gợi ý)

---

### **25+ PROPERTIES (Thuộc tính)**

#### **Định danh (ID):**
- `studentId`, `teacherId`, `lessonId`, `q_id`, `skillId`, `testId`

#### **Văn bản:**
- `fullName`, `questionText`, `correctOption`, `title`, `testName`, `label`

#### **Số:**
- `score` (điểm), `coverage` (phủ sóng), `duration` (thời gian), `grade` (khối)

#### **Thời gian:**
- `testDate`, `lastUpdated`

#### **Đặc biệt:**
- `difficulty` (độ khó), `bloomLevel` (mức Bloom), `mediaType` (loại media), `url`

---

## 🔄 SƠ ĐỒ QUAN HỆ CHÍNH

```
Grade (Khối 6)
  ↑
Class (Lớp 6A) ← Student (HS001)
  ↑                    ↓
Topic (A)         Test (Kiểm tra 1)
  ↑                    ↓
Lesson (A1)      Question (CH001)
  ↑                    ↓
Skill (Nhận biết) ← Resource (Video)
```

---

## 💡 VÍ DỤ MINH HỌA

### Học sinh thuộc lớp:
```turtle
edu:student_001 edu:belongsToClass edu:class_6A .
```

### Bài học thuộc chủ đề:
```turtle
edu:lesson_A1 edu:belongsToTopic edu:topic_A .
```

### Câu hỏi yêu cầu kỹ năng:
```turtle
edu:question_001 edu:requiresSkill edu:skill_nhan_biet .
```

### Học sinh yếu ở chủ đề (KNN):
```turtle
edu:student_001 edu:weakInTopic edu:topic_C .
```

### Bài học được gợi ý (PPR):
```turtle
edu:lesson_A1 edu:recommendedFor edu:student_001 .
```

---

## 🎯 ĐIỂM QUAN TRỌNG

### ✅ **Schema phải upload đầu tiên**
- Tất cả file TTL khác phụ thuộc vào schema này
- Không có schema → Không thể validate dữ liệu

### ✅ **Hỗ trợ ML/AI**
- `weakInTopic` - KNN tự động tạo
- `recommendedFor` - PPR tự động tạo
- `recommendedResourceFor` - PPR tự động tạo

### ✅ **Cấu trúc phân cấp rõ ràng**
- Grade → Class → Student
- Grade → Topic → Lesson → Question
- Skill → Question/Resource

### ✅ **Linh hoạt mở rộng**
- Có thể thêm class mới
- Có thể thêm property mới
- Không ảnh hưởng dữ liệu cũ

---

## 📚 TÀI LIỆU THAM KHẢO

- **Chi tiết đầy đủ:** `GIAI_THICH_SCHEMA_CHUAN.md`
- **File schema:** `schema/kg_schema_chuan.ttl`

---

**Tóm lại:** Schema là "bản thiết kế" định nghĩa cấu trúc của toàn bộ Knowledge Graph! 🎯

