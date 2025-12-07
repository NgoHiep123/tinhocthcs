# 📖 GIẢI THÍCH CHI TIẾT FILE `kg_schema_chuan.ttl`

## 🎯 TỔNG QUAN

File `kg_schema_chuan.ttl` là **Ontology Schema** (lược đồ tri thức) định nghĩa cấu trúc của Knowledge Graph cho hệ thống Tin học THCS. Đây là "bản thiết kế" cho toàn bộ dữ liệu sẽ được lưu trữ.

---

## 📋 PHẦN 1: PREFIXES (Dòng 1-5)

```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix edu: <http://education.vn/ontology#> .
```

### Giải thích:

| Prefix | Ý Nghĩa | Mục Đích |
|--------|---------|----------|
| **rdf:** | Resource Description Framework | Định nghĩa cơ bản về RDF (Class, Property) |
| **rdfs:** | RDF Schema | Mở rộng RDF (label, comment, domain, range) |
| **xsd:** | XML Schema Datatypes | Kiểu dữ liệu (string, integer, decimal, date) |
| **owl:** | Web Ontology Language | Ngôn ngữ ontology mạnh mẽ hơn |
| **edu:** | Education Ontology | **Namespace riêng** của dự án |

**Ví dụ sử dụng:**
- `edu:Student` = Học sinh trong hệ thống giáo dục
- `rdfs:Class` = Một lớp (class) trong RDF
- `xsd:string` = Kiểu dữ liệu chuỗi

---

## 🏗️ PHẦN 2: CLASSES (Thực thể) - Dòng 12-72

### 2.1. **Học Sinh (Student)** - Dòng 14-17

```turtle
edu:Student a rdfs:Class ;
    rdfs:label "Học sinh"@vi ;
    rdfs:comment "Thực thể đại diện cho học sinh THCS" .
```

**Giải thích:**
- `edu:Student` = Tên class (URI)
- `a rdfs:Class` = Khai báo đây là một Class
- `rdfs:label` = Nhãn hiển thị (tiếng Việt)
- `rdfs:comment` = Mô tả chi tiết

**Ví dụ instance:**
```turtle
edu:student_001 a edu:Student ;
    edu:fullName "Nguyễn Văn A" ;
    edu:studentId "HS001" .
```

---

### 2.2. **Giáo Viên (Teacher)** - Dòng 19-22

```turtle
edu:Teacher a rdfs:Class ;
    rdfs:label "Giáo viên"@vi ;
    rdfs:comment "Thực thể đại diện cho giáo viên dạy Tin học" .
```

**Đại diện cho:** Giáo viên dạy môn Tin học

---

### 2.3. **Lớp Học (Class)** - Dòng 24-27

```turtle
edu:Class a rdfs:Class ;
    rdfs:label "Lớp học"@vi ;
    rdfs:comment "Lớp học THCS (6/1, 7/1, ...)" .
```

**Ví dụ:** Lớp 6A, 6B, 7A, 7B...

---

### 2.4. **Khối Lớp (Grade)** - Dòng 29-32

```turtle
edu:Grade a rdfs:Class ;
    rdfs:label "Khối"@vi ;
    rdfs:comment "Khối lớp 6, 7, 8, 9" .
```

**Ví dụ:** Khối 6, Khối 7, Khối 8, Khối 9

---

### 2.5. **Chủ Đề (Topic)** - Dòng 34-37

```turtle
edu:Topic a rdfs:Class ;
    rdfs:label "Chủ đề"@vi ;
    rdfs:comment "Chủ đề học tập (A, B, C, D, E, F)" .
```

**Ví dụ:** 
- Topic A: Máy tính và cộng đồng
- Topic B: Mạng máy tính và Internet
- Topic C: Tổ chức lưu trữ, tìm kiếm và trao đổi thông tin

---

### 2.6. **Bài Học (Lesson)** - Dòng 39-42

```turtle
edu:Lesson a rdfs:Class ;
    rdfs:label "Bài học"@vi ;
    rdfs:comment "Bài học cụ thể (A1, A2, A4, A5, ...)" .
```

**Ví dụ:** 
- A1: Máy tính và ứng dụng
- A2: Hệ điều hành và phần mềm ứng dụng
- B1: Mạng máy tính

---

### 2.7. **Câu Hỏi (Question)** - Dòng 44-47

```turtle
edu:Question a rdfs:Class ;
    rdfs:label "Câu hỏi"@vi ;
    rdfs:comment "Câu hỏi trắc nghiệm" .
```

**Đại diện cho:** Câu hỏi trắc nghiệm trong bài học

---

### 2.8. **Kỹ Năng (Skill)** - Dòng 49-52

```turtle
edu:Skill a rdfs:Class ;
    rdfs:label "Kỹ năng"@vi ;
    rdfs:comment "Kỹ năng: nhận biết, thông hiểu, vận dụng" .
```

**Ví dụ:**
- Nhận biết: Nhận biết được các thành phần máy tính
- Thông hiểu: Giải thích được chức năng của CPU
- Vận dụng: Sử dụng được phần mềm soạn thảo văn bản

---

### 2.9. **Tài Nguyên Học Tập (Resource)** - Dòng 54-57

```turtle
edu:Resource a rdfs:Class ;
    rdfs:label "Tài nguyên học tập"@vi ;
    rdfs:comment "Tài nguyên học tập: HTML, video, PDF, bài tập" .
```

**Ví dụ:**
- Video bài giảng
- PDF giáo trình
- HTML interactive lesson
- Bài tập online

---

### 2.10. **Bài Kiểm Tra (Test)** - Dòng 59-62

```turtle
edu:Test a rdfs:Class ;
    rdfs:label "Bài kiểm tra"@vi ;
    rdfs:comment "Bài kiểm tra trắc nghiệm" .
```

**Đại diện cho:** Bài kiểm tra, bài thi

---

### 2.11. **Kết Quả Làm Bài (TestResult)** - Dòng 64-67

```turtle
edu:TestResult a rdfs:Class ;
    rdfs:label "Kết quả làm bài"@vi ;
    rdfs:comment "Kết quả làm bài của học sinh" .
```

**Đại diện cho:** Kết quả khi học sinh làm bài kiểm tra

---

### 2.12. **Mức Độ Thành Thạo (Mastery)** - Dòng 69-72

```turtle
edu:Mastery a rdfs:Class ;
    rdfs:label "Mức độ thành thạo"@vi ;
    rdfs:comment "Mức độ thành thạo của học sinh đối với kỹ năng" .
```

**Ví dụ:** Học sinh A có mức độ thành thạo 0.8 (80%) với kỹ năng "Sử dụng phần mềm soạn thảo"

---

## 🔗 PHẦN 3: RELATIONSHIPS (Quan hệ) - Dòng 74-187

### 3.1. **Quan Hệ Cơ Bản**

#### `belongsToClass` - Học sinh thuộc lớp (Dòng 76-80)

```turtle
edu:belongsToClass a rdf:Property ;
    rdfs:label "thuộc lớp"@vi ;
    rdfs:domain edu:Student ;    # Chỉ Student mới có property này
    rdfs:range edu:Class .       # Giá trị phải là Class
```

**Ví dụ:**
```turtle
edu:student_001 edu:belongsToClass edu:class_6A .
```

**Ý nghĩa:** Học sinh 001 thuộc lớp 6A

---

#### `belongsToGrade` - Lớp thuộc khối (Dòng 82-86)

```turtle
edu:belongsToGrade a rdf:Property ;
    rdfs:label "thuộc khối"@vi ;
    rdfs:domain edu:Class ;
    rdfs:range edu:Grade .
```

**Ví dụ:**
```turtle
edu:class_6A edu:belongsToGrade edu:grade_6 .
```

**Ý nghĩa:** Lớp 6A thuộc khối 6

---

#### `teaches` - Giáo viên dạy lớp (Dòng 88-92)

```turtle
edu:teaches a rdf:Property ;
    rdfs:label "giảng dạy"@vi ;
    rdfs:domain edu:Teacher ;
    rdfs:range edu:Class .
```

**Ví dụ:**
```turtle
edu:teacher_001 edu:teaches edu:class_6A .
```

**Ý nghĩa:** Giáo viên 001 dạy lớp 6A

---

### 3.2. **Quan Hệ Nội Dung Học Tập**

#### `belongsToTopic` - Bài học thuộc chủ đề (Dòng 94-98)

```turtle
edu:belongsToTopic a rdf:Property ;
    rdfs:label "thuộc chủ đề"@vi ;
    rdfs:domain edu:Lesson ;
    rdfs:range edu:Topic .
```

**Ví dụ:**
```turtle
edu:lesson_A1 edu:belongsToTopic edu:topic_A .
```

**Ý nghĩa:** Bài A1 thuộc chủ đề A

---

#### `forGrade` - Chủ đề dành cho khối (Dòng 100-104)

```turtle
edu:forGrade a rdf:Property ;
    rdfs:label "dành cho khối"@vi ;
    rdfs:domain edu:Topic ;
    rdfs:range edu:Grade .
```

**Ví dụ:**
```turtle
edu:topic_A edu:forGrade edu:grade_6 .
```

**Ý nghĩa:** Chủ đề A dành cho khối 6

---

#### `belongsToLesson` - Câu hỏi thuộc bài học (Dòng 106-110)

```turtle
edu:belongsToLesson a rdf:Property ;
    rdfs:label "thuộc bài học"@vi ;
    rdfs:domain edu:Question ;
    rdfs:range edu:Lesson .
```

**Ví dụ:**
```turtle
edu:question_001 edu:belongsToLesson edu:lesson_A1 .
```

**Ý nghĩa:** Câu hỏi 001 thuộc bài A1

---

### 3.3. **Quan Hệ Kỹ Năng**

#### `requiresSkill` - Câu hỏi yêu cầu kỹ năng (Dòng 112-116)

```turtle
edu:requiresSkill a rdf:Property ;
    rdfs:label "yêu cầu kỹ năng"@vi ;
    rdfs:domain edu:Question ;
    rdfs:range edu:Skill .
```

**Ví dụ:**
```turtle
edu:question_001 edu:requiresSkill edu:skill_nhan_biet .
```

**Ý nghĩa:** Câu hỏi 001 yêu cầu kỹ năng "nhận biết"

---

#### `coversSkill` - Tài nguyên phủ sóng kỹ năng (Dòng 118-123)

```turtle
edu:coversSkill a rdf:Property ;
    rdfs:label "phủ sóng kỹ năng"@vi ;
    rdfs:comment "Tài nguyên học tập phủ sóng kỹ năng với mức độ coverage"@vi ;
    rdfs:domain edu:Resource ;
    rdfs:range edu:Skill .
```

**Ví dụ:**
```turtle
edu:resource_video_001 edu:coversSkill edu:skill_thong_hieu ;
    edu:coverage 0.9 .
```

**Ý nghĩa:** Video 001 phủ sóng kỹ năng "thông hiểu" với mức độ 90%

---

#### `prerequisiteOf` - Kỹ năng tiên quyết (Dòng 125-130)

```turtle
edu:prerequisiteOf a rdf:Property ;
    rdfs:label "tiên quyết của"@vi ;
    rdfs:comment "Kỹ năng này là tiên quyết của kỹ năng kia"@vi ;
    rdfs:domain edu:Skill ;
    rdfs:range edu:Skill .
```

**Ví dụ:**
```turtle
edu:skill_nhan_biet edu:prerequisiteOf edu:skill_thong_hieu .
```

**Ý nghĩa:** Kỹ năng "nhận biết" là tiên quyết của "thông hiểu"

---

### 3.4. **Quan Hệ Kiểm Tra & Kết Quả**

#### `takeTest` - Học sinh làm bài kiểm tra (Dòng 132-136)

```turtle
edu:takeTest a rdf:Property ;
    rdfs:label "làm bài kiểm tra"@vi ;
    rdfs:domain edu:Student ;
    rdfs:range edu:Test .
```

**Ví dụ:**
```turtle
edu:student_001 edu:takeTest edu:test_kiemtra_1 .
```

**Ý nghĩa:** Học sinh 001 làm bài kiểm tra 1

---

#### `hasQuestion` - Bài kiểm tra có câu hỏi (Dòng 138-142)

```turtle
edu:hasQuestion a rdf:Property ;
    rdfs:label "có câu hỏi"@vi ;
    rdfs:domain edu:Test ;
    rdfs:range edu:Question .
```

**Ví dụ:**
```turtle
edu:test_kiemtra_1 edu:hasQuestion edu:question_001 .
```

**Ý nghĩa:** Bài kiểm tra 1 có câu hỏi 001

---

#### `hasResult` - Học sinh có kết quả (Dòng 144-148)

```turtle
edu:hasResult a rdf:Property ;
    rdfs:label "có kết quả"@vi ;
    rdfs:domain edu:Student ;
    rdfs:range edu:TestResult .
```

**Ví dụ:**
```turtle
edu:student_001 edu:hasResult edu:result_001 .
```

**Ý nghĩa:** Học sinh 001 có kết quả 001

---

#### `forTest` - Kết quả thuộc bài kiểm tra (Dòng 150-154)

```turtle
edu:forTest a rdf:Property ;
    rdfs:label "của bài kiểm tra"@vi ;
    rdfs:domain edu:TestResult ;
    rdfs:range edu:Test .
```

**Ví dụ:**
```turtle
edu:result_001 edu:forTest edu:test_kiemtra_1 ;
    edu:score 8.5 .
```

**Ý nghĩa:** Kết quả 001 là của bài kiểm tra 1, điểm 8.5

---

### 3.5. **Quan Hệ Mastery**

#### `hasMastery` - Học sinh có mức độ thành thạo (Dòng 156-160)

```turtle
edu:hasMastery a rdf:Property ;
    rdfs:label "có mức độ thành thạo"@vi ;
    rdfs:domain edu:Student ;
    rdfs:range edu:Mastery .
```

**Ví dụ:**
```turtle
edu:student_001 edu:hasMastery edu:mastery_001 .
```

---

#### `forSkill` - Mức độ thành thạo đối với kỹ năng (Dòng 162-166)

```turtle
edu:forSkill a rdf:Property ;
    rdfs:label "đối với kỹ năng"@vi ;
    rdfs:domain edu:Mastery ;
    rdfs:range edu:Skill .
```

**Ví dụ:**
```turtle
edu:mastery_001 edu:forSkill edu:skill_nhan_biet ;
    edu:score 0.85 .
```

**Ý nghĩa:** Mức độ thành thạo 001 đối với kỹ năng "nhận biết" là 85%

---

### 3.6. **Quan Hệ ML/AI (Machine Learning)**

#### `weakInTopic` - Học sinh yếu ở chủ đề (KNN) - Dòng 168-173

```turtle
edu:weakInTopic a rdf:Property ;
    rdfs:label "yếu ở chủ đề"@vi ;
    rdfs:comment "Được xác định bởi k-Nearest Neighbors (KNN)"@vi ;
    rdfs:domain edu:Student ;
    rdfs:range edu:Topic .
```

**Giải thích:**
- Thuật toán **KNN** phân tích điểm số của học sinh
- Xác định học sinh nào yếu ở chủ đề nào
- Tự động tạo quan hệ này

**Ví dụ:**
```turtle
edu:student_001 edu:weakInTopic edu:topic_C .
```

**Ý nghĩa:** Học sinh 001 yếu ở chủ đề C (được KNN phát hiện)

---

#### `recommendedFor` - Bài học được gợi ý (PPR) - Dòng 175-180

```turtle
edu:recommendedFor a rdf:Property ;
    rdfs:label "được gợi ý cho"@vi ;
    rdfs:comment "Được xác định bởi Personalized PageRank (PPR)"@vi ;
    rdfs:domain edu:Lesson ;
    rdfs:range edu:Student .
```

**Giải thích:**
- Thuật toán **PPR** chạy trên Knowledge Graph
- Dựa vào điểm yếu của học sinh (từ KNN)
- Gợi ý bài học phù hợp để cải thiện

**Ví dụ:**
```turtle
edu:lesson_A1 edu:recommendedFor edu:student_001 .
```

**Ý nghĩa:** Bài A1 được gợi ý cho học sinh 001

---

#### `recommendedResourceFor` - Tài nguyên được gợi ý (PPR) - Dòng 182-187

```turtle
edu:recommendedResourceFor a rdf:Property ;
    rdfs:label "tài nguyên được gợi ý cho"@vi ;
    rdfs:comment "Tài nguyên học tập được gợi ý cho học sinh (PPR)"@vi ;
    rdfs:domain edu:Resource ;
    rdfs:range edu:Student .
```

**Ví dụ:**
```turtle
edu:resource_video_001 edu:recommendedResourceFor edu:student_001 .
```

**Ý nghĩa:** Video 001 được gợi ý cho học sinh 001

---

## 📊 PHẦN 4: PROPERTIES (Thuộc tính) - Dòng 189-357

### 4.1. **Thuộc Tính Số (Numeric)**

#### `score` - Điểm số (Dòng 191-195)

```turtle
edu:score a rdf:Property ;
    rdfs:label "điểm số"@vi ;
    rdfs:domain edu:TestResult , edu:Mastery ;  # Dùng cho cả 2 class
    rdfs:range xsd:decimal .                    # Kiểu số thập phân
```

**Ví dụ:**
```turtle
edu:result_001 edu:score 8.5 .
edu:mastery_001 edu:score 0.85 .
```

---

#### `coverage` - Mức độ phủ sóng (Dòng 221-225)

```turtle
edu:coverage a rdf:Property ;
    rdfs:label "mức độ phủ sóng"@vi ;
    rdfs:comment "Mức độ phủ sóng của tài nguyên đối với kỹ năng (0.0-1.0)"@vi ;
    rdfs:range xsd:decimal .
```

**Ví dụ:**
```turtle
edu:resource_video_001 edu:coversSkill edu:skill_nhan_biet ;
    edu:coverage 0.9 .
```

**Ý nghĩa:** Video phủ sóng 90% kỹ năng "nhận biết"

---

### 4.2. **Thuộc Tính Thời Gian**

#### `duration` - Thời gian làm bài (Dòng 203-207)

```turtle
edu:duration a rdf:Property ;
    rdfs:label "thời gian"@vi ;
    rdfs:domain edu:TestResult , edu:Resource ;
    rdfs:range xsd:integer .  # Giây
```

**Ví dụ:**
```turtle
edu:result_001 edu:duration 1800 .  # 30 phút
```

---

#### `testDate` - Ngày làm bài (Dòng 209-213)

```turtle
edu:testDate a rdf:Property ;
    rdfs:label "ngày làm bài"@vi ;
    rdfs:domain edu:TestResult ;
    rdfs:range xsd:dateTime .
```

**Ví dụ:**
```turtle
edu:result_001 edu:testDate "2025-12-05T10:30:00"^^xsd:dateTime .
```

---

#### `lastUpdated` - Ngày cập nhật (Dòng 215-219)

```turtle
edu:lastUpdated a rdf:Property ;
    rdfs:label "ngày cập nhật"@vi ;
    rdfs:domain edu:Mastery ;
    rdfs:range xsd:date .
```

**Ví dụ:**
```turtle
edu:mastery_001 edu:lastUpdated "2025-12-05"^^xsd:date .
```

---

### 4.3. **Thuộc Tính Văn Bản**

#### `fullName` - Họ tên (Dòng 227-231)

```turtle
edu:fullName a rdf:Property ;
    rdfs:label "họ tên"@vi ;
    rdfs:domain edu:Student , edu:Teacher ;
    rdfs:range xsd:string .
```

**Ví dụ:**
```turtle
edu:student_001 edu:fullName "Nguyễn Văn A" .
```

---

#### `questionText` - Nội dung câu hỏi (Dòng 287-291)

```turtle
edu:questionText a rdf:Property ;
    rdfs:label "nội dung câu hỏi"@vi ;
    rdfs:domain edu:Question ;
    rdfs:range xsd:string .
```

**Ví dụ:**
```turtle
edu:question_001 edu:questionText "Máy tính là gì?" .
```

---

#### `correctOption` - Đáp án đúng (Dòng 293-297)

```turtle
edu:correctOption a rdf:Property ;
    rdfs:label "đáp án đúng"@vi ;
    rdfs:domain edu:Question ;
    rdfs:range xsd:string .
```

**Ví dụ:**
```turtle
edu:question_001 edu:correctOption "A" .
```

---

### 4.4. **Thuộc Tính Định Danh (ID)**

#### `studentId` - Mã học sinh (Dòng 233-237)

```turtle
edu:studentId a rdf:Property ;
    rdfs:label "mã học sinh"@vi ;
    rdfs:domain edu:Student ;
    rdfs:range xsd:string .
```

**Ví dụ:**
```turtle
edu:student_001 edu:studentId "HS001" .
```

---

#### `teacherId` - Mã giáo viên (Dòng 245-249)

```turtle
edu:teacherId a rdf:Property ;
    rdfs:label "mã giáo viên"@vi ;
    rdfs:domain edu:Teacher ;
    rdfs:range xsd:string .
```

---

#### `lessonId` - Mã bài học (Dòng 275-279)

```turtle
edu:lessonId a rdf:Property ;
    rdfs:label "mã bài học"@vi ;
    rdfs:domain edu:Lesson ;
    rdfs:range xsd:string .
```

**Ví dụ:**
```turtle
edu:lesson_A1 edu:lessonId "A1" .
```

---

#### `q_id` - Mã câu hỏi (Dòng 281-285)

```turtle
edu:q_id a rdf:Property ;
    rdfs:label "mã câu hỏi"@vi ;
    rdfs:domain edu:Question ;
    rdfs:range xsd:string .
```

---

#### `skillId` - Mã kỹ năng (Dòng 299-303)

```turtle
edu:skillId a rdf:Property ;
    rdfs:label "mã kỹ năng"@vi ;
    rdfs:domain edu:Skill ;
    rdfs:range xsd:string .
```

---

#### `testId` - Mã bài kiểm tra (Dòng 347-351)

```turtle
edu:testId a rdf:Property ;
    rdfs:label "mã bài kiểm tra"@vi ;
    rdfs:domain edu:Test ;
    rdfs:range xsd:string .
```

---

### 4.5. **Thuộc Tính Đặc Biệt**

#### `difficulty` - Độ khó (Dòng 197-201)

```turtle
edu:difficulty a rdf:Property ;
    rdfs:label "độ khó"@vi ;
    rdfs:domain edu:Question , edu:Resource ;
    rdfs:range xsd:string .
```

**Ví dụ:**
```turtle
edu:question_001 edu:difficulty "Dễ" .
edu:question_002 edu:difficulty "Trung bình" .
edu:question_003 edu:difficulty "Khó" .
```

---

#### `bloomLevel` - Mức độ Bloom (Dòng 311-315)

```turtle
edu:bloomLevel a rdf:Property ;
    rdfs:label "mức độ Bloom"@vi ;
    rdfs:domain edu:Skill ;
    rdfs:range xsd:string .
```

**Ví dụ:**
```turtle
edu:skill_nhan_biet edu:bloomLevel "Nhận biết" .
edu:skill_thong_hieu edu:bloomLevel "Thông hiểu" .
edu:skill_van_dung edu:bloomLevel "Vận dụng" .
```

**Giải thích:** Thang đo Bloom phân loại mức độ nhận thức:
- **Nhận biết:** Biết được khái niệm
- **Thông hiểu:** Hiểu được ý nghĩa
- **Vận dụng:** Áp dụng được vào thực tế
- **Phân tích:** Phân tích được các thành phần
- **Đánh giá:** Đánh giá được chất lượng
- **Sáng tạo:** Tạo ra cái mới

---

#### `mediaType` - Loại media (Dòng 335-339)

```turtle
edu:mediaType a rdf:Property ;
    rdfs:label "loại media"@vi ;
    rdfs:domain edu:Resource ;
    rdfs:range xsd:string .
```

**Ví dụ:**
```turtle
edu:resource_001 edu:mediaType "video" .
edu:resource_002 edu:mediaType "PDF" .
edu:resource_003 edu:mediaType "HTML" .
```

---

#### `url` - URL (Dòng 341-345)

```turtle
edu:url a rdf:Property ;
    rdfs:label "URL"@vi ;
    rdfs:domain edu:Resource ;
    rdfs:range xsd:string .
```

**Ví dụ:**
```turtle
edu:resource_video_001 edu:url "https://example.com/video1.mp4" .
```

---

## 🎯 TỔNG KẾT CẤU TRÚC

### **12 Classes (Thực thể):**
1. Student (Học sinh)
2. Teacher (Giáo viên)
3. Class (Lớp học)
4. Grade (Khối lớp)
5. Topic (Chủ đề)
6. Lesson (Bài học)
7. Question (Câu hỏi)
8. Skill (Kỹ năng)
9. Resource (Tài nguyên)
10. Test (Bài kiểm tra)
11. TestResult (Kết quả)
12. Mastery (Mức độ thành thạo)

### **17 Relationships (Quan hệ):**
- Cấu trúc: belongsToClass, belongsToGrade, belongsToTopic, belongsToLesson
- Giảng dạy: teaches
- Nội dung: forGrade, requiresSkill, coversSkill, prerequisiteOf
- Kiểm tra: takeTest, hasQuestion, hasResult, forTest
- Mastery: hasMastery, forSkill
- AI/ML: weakInTopic, recommendedFor, recommendedResourceFor

### **25+ Properties (Thuộc tính):**
- Định danh: studentId, teacherId, lessonId, q_id, skillId, testId
- Văn bản: fullName, questionText, correctOption, title, testName
- Số: score, coverage, duration, grade
- Thời gian: testDate, lastUpdated
- Đặc biệt: difficulty, bloomLevel, mediaType, url

---

## 🔄 LUỒNG DỮ LIỆU

```
Grade (Khối 6)
  ↓ belongsToGrade
Class (Lớp 6A)
  ↑ belongsToClass
Student (HS001)
  ↓ takeTest
Test (Kiểm tra 1)
  ↓ hasQuestion
Question (CH001)
  ↓ belongsToLesson
Lesson (A1)
  ↓ belongsToTopic
Topic (A)
  ↓ forGrade
Grade (Khối 6)
```

---

## 💡 VÍ DỤ HOÀN CHỈNH

```turtle
# Học sinh
edu:student_001 a edu:Student ;
    edu:studentId "HS001" ;
    edu:fullName "Nguyễn Văn A" ;
    edu:belongsToClass edu:class_6A ;
    edu:takeTest edu:test_1 ;
    edu:hasResult edu:result_001 ;
    edu:hasMastery edu:mastery_001 ;
    edu:weakInTopic edu:topic_C .

# Lớp học
edu:class_6A a edu:Class ;
    edu:className "6A" ;
    edu:belongsToGrade edu:grade_6 .

# Khối
edu:grade_6 a edu:Grade ;
    edu:grade 6 .

# Bài học
edu:lesson_A1 a edu:Lesson ;
    edu:lessonId "A1" ;
    edu:label "Máy tính và ứng dụng" ;
    edu:belongsToTopic edu:topic_A ;
    edu:recommendedFor edu:student_001 .

# Chủ đề
edu:topic_A a edu:Topic ;
    edu:topicId "A" ;
    edu:label "Máy tính và cộng đồng" ;
    edu:forGrade edu:grade_6 .

# Câu hỏi
edu:question_001 a edu:Question ;
    edu:q_id "Q001" ;
    edu:questionText "Máy tính là gì?" ;
    edu:correctOption "A" ;
    edu:belongsToLesson edu:lesson_A1 ;
    edu:requiresSkill edu:skill_nhan_biet ;
    edu:difficulty "Dễ" .

# Kỹ năng
edu:skill_nhan_biet a edu:Skill ;
    edu:skillId "SK001" ;
    edu:name "Nhận biết" ;
    edu:bloomLevel "Nhận biết" ;
    edu:domain "Tin học" .

# Kết quả
edu:result_001 a edu:TestResult ;
    edu:forTest edu:test_1 ;
    edu:score 8.5 ;
    edu:testDate "2025-12-05T10:30:00"^^xsd:dateTime ;
    edu:duration 1800 .

# Mastery
edu:mastery_001 a edu:Mastery ;
    edu:forSkill edu:skill_nhan_biet ;
    edu:score 0.85 ;
    edu:lastUpdated "2025-12-05"^^xsd:date .
```

---

## 🎓 KẾT LUẬN

File `kg_schema_chuan.ttl` là **"bản thiết kế"** của toàn bộ Knowledge Graph:

✅ **Định nghĩa** các thực thể (Classes)  
✅ **Định nghĩa** các quan hệ (Relationships)  
✅ **Định nghĩa** các thuộc tính (Properties)  
✅ **Hỗ trợ** thuật toán ML (KNN, PPR)  
✅ **Chuẩn hóa** cấu trúc dữ liệu  

**Tất cả file TTL khác phải tuân theo schema này!**

---

**Hy vọng giải thích này giúp bạn hiểu rõ schema! 🎉**

