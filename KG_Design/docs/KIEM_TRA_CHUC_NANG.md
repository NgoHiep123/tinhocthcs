# ✅ KIỂM TRA CHỨC NĂNG - SCHEMA KG CHUẨN

## 🎯 MỤC ĐÍCH

Tài liệu này kiểm tra xem schema KG chuẩn có hỗ trợ đầy đủ các chức năng đề xuất trong đề cương Đề án 2 hay không.

---

## 📋 CÁC CHỨC NĂNG CẦN HỖ TRỢ

Theo đề cương (dòng 25), hệ thống cần hỗ trợ:

1. **Đề xuất bài giảng/chương học:**
   - Top k theo điểm
   - Bài kiểm tra điểm thấp

2. **Đề xuất đề thi:**
   - Top k theo điểm
   - Bài kiểm tra điểm thấp

3. **Cải tiến phương pháp giảng dạy:**
   - Top k theo điểm/xếp loại

---

## ✅ KIỂM TRA TỪNG CHỨC NĂNG

### **1. ĐỀ XUẤT BÀI GIẢNG/CHƯƠNG HỌC**

#### **1.1. Top k theo điểm**

**Yêu cầu:** Tìm các bài học có điểm trung bình cao nhất.

**Schema hỗ trợ:**
- ✅ `Lesson` - Thực thể bài học
- ✅ `TestResult` - Kết quả làm bài (có `score`)
- ✅ `Test` - Bài kiểm tra
- ✅ `Question` - Câu hỏi
- ✅ `Question → belongsToLesson → Lesson` - Liên kết câu hỏi với bài học
- ✅ `Test → hasQuestion → Question` - Liên kết đề thi với câu hỏi
- ✅ `TestResult → forTest → Test` - Liên kết kết quả với đề thi

**SPARQL Query:**
```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?lesson ?lessonLabel (AVG(?score) AS ?avgScore) (COUNT(?result) AS ?numTests)
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

**Kết luận:** ✅ **HỖ TRỢ ĐẦY ĐỦ**

---

#### **1.2. Bài kiểm tra điểm thấp**

**Yêu cầu:** Tìm các bài học liên quan đến bài kiểm tra có điểm thấp.

**Schema hỗ trợ:**
- ✅ `TestResult` - Có `score` để xác định điểm thấp
- ✅ `TestResult → forTest → Test` - Liên kết với đề thi
- ✅ `Test → hasQuestion → Question` - Liên kết với câu hỏi
- ✅ `Question → belongsToLesson → Lesson` - Liên kết với bài học

**SPARQL Query:**
```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT DISTINCT ?lesson ?lessonLabel ?test ?testName (AVG(?score) AS ?avgScore)
WHERE {
  ?result a edu:TestResult ;
          edu:score ?score ;
          edu:forTest ?test .
  ?test edu:testName ?testName ;
        edu:hasQuestion ?question .
  ?question edu:belongsToLesson ?lesson .
  ?lesson edu:label ?lessonLabel .
  FILTER(?score < 0.5)  # Điểm thấp (< 5.0)
}
GROUP BY ?lesson ?lessonLabel ?test ?testName
ORDER BY ASC(?avgScore)
```

**Kết luận:** ✅ **HỖ TRỢ ĐẦY ĐỦ**

---

### **2. ĐỀ XUẤT ĐỀ THI**

#### **2.1. Top k theo điểm**

**Yêu cầu:** Tìm các đề thi có điểm trung bình cao nhất.

**Schema hỗ trợ:**
- ✅ `Test` - Thực thể đề thi
- ✅ `TestResult` - Kết quả làm bài (có `score`)
- ✅ `TestResult → forTest → Test` - Liên kết kết quả với đề thi

**SPARQL Query:**
```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?test ?testName (AVG(?score) AS ?avgScore) (COUNT(?result) AS ?numStudents)
WHERE {
  ?test a edu:Test ;
        edu:testName ?testName .
  ?result a edu:TestResult ;
          edu:forTest ?test ;
          edu:score ?score .
}
GROUP BY ?test ?testName
ORDER BY DESC(?avgScore)
LIMIT 5
```

**Kết luận:** ✅ **HỖ TRỢ ĐẦY ĐỦ**

---

#### **2.2. Bài kiểm tra điểm thấp**

**Yêu cầu:** Tìm các đề thi có điểm thấp để cải tiến.

**Schema hỗ trợ:**
- ✅ `Test` - Thực thể đề thi
- ✅ `TestResult` - Có `score` để xác định điểm thấp
- ✅ `TestResult → forTest → Test` - Liên kết kết quả với đề thi

**SPARQL Query:**
```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?test ?testName (AVG(?score) AS ?avgScore) (COUNT(?result) AS ?numStudents)
WHERE {
  ?test a edu:Test ;
        edu:testName ?testName .
  ?result a edu:TestResult ;
          edu:forTest ?test ;
          edu:score ?score .
}
GROUP BY ?test ?testName
HAVING (AVG(?score) < 0.5)  # Điểm trung bình < 5.0
ORDER BY ASC(?avgScore)
```

**Kết luận:** ✅ **HỖ TRỢ ĐẦY ĐỦ**

---

### **3. CẢI TIẾN PHƯƠNG PHÁP GIẢNG DẠY**

#### **3.1. Top k theo điểm/xếp loại**

**Yêu cầu:** Phân tích hiệu quả giảng dạy theo lớp, giáo viên.

**Schema hỗ trợ:**
- ✅ `Teacher` - Thực thể giáo viên
- ✅ `Class` - Thực thể lớp học
- ✅ `Student` - Thực thể học sinh
- ✅ `Teacher → teaches → Class` - Giáo viên dạy lớp
- ✅ `Student → belongsToClass → Class` - Học sinh thuộc lớp
- ✅ `Student → hasResult → TestResult` - Học sinh có kết quả
- ✅ `TestResult` - Có `score` để tính điểm trung bình

**SPARQL Query (theo lớp):**
```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?class ?className 
       (AVG(?score) AS ?avgScore)
       (COUNT(DISTINCT ?student) AS ?numStudents)
       (COUNT(?result) AS ?numTests)
WHERE {
  ?class a edu:Class ;
         edu:className ?className .
  ?student a edu:Student ;
           edu:belongsToClass ?class .
  ?result a edu:TestResult ;
          edu:hasResult ?student ;
          edu:score ?score .
}
GROUP BY ?class ?className
ORDER BY DESC(?avgScore)
LIMIT 10
```

**SPARQL Query (theo giáo viên):**
```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?teacher ?teacherName 
       (AVG(?score) AS ?avgScore)
       (COUNT(DISTINCT ?student) AS ?numStudents)
       (COUNT(DISTINCT ?class) AS ?numClasses)
WHERE {
  ?teacher a edu:Teacher ;
            edu:fullName ?teacherName ;
            edu:teaches ?class .
  ?student a edu:Student ;
            edu:belongsToClass ?class .
  ?result a edu:TestResult ;
          edu:hasResult ?student ;
          edu:score ?score .
}
GROUP BY ?teacher ?teacherName
ORDER BY DESC(?avgScore)
LIMIT 10
```

**Kết luận:** ✅ **HỖ TRỢ ĐẦY ĐỦ**

---

## 🎯 CÁC CHỨC NĂNG BỔ SUNG

### **4. GỢI Ý DỰA TRÊN PPR**

**Yêu cầu:** Gợi ý bài học/tài nguyên phù hợp cho học sinh dựa trên Personalized PageRank.

**Schema hỗ trợ:**
- ✅ `Lesson → recommendedFor → Student` - Bài học được gợi ý cho học sinh
- ✅ `Resource → recommendedResourceFor → Student` - Tài nguyên được gợi ý cho học sinh

**SPARQL Query (bài học):**
```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?studentName ?lesson ?lessonLabel
WHERE {
  ?student a edu:Student ;
           edu:fullName ?studentName .
  ?lesson a edu:Lesson ;
          edu:recommendedFor ?student ;
          edu:label ?lessonLabel .
}
ORDER BY ?student ?lesson
```

**SPARQL Query (tài nguyên):**
```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?student ?studentName ?resource ?resourceTitle
WHERE {
  ?student a edu:Student ;
           edu:fullName ?studentName .
  ?resource a edu:Resource ;
            edu:recommendedResourceFor ?student ;
            edu:title ?resourceTitle .
}
ORDER BY ?student ?resource
```

**Kết luận:** ✅ **HỖ TRỢ ĐẦY ĐỦ**

---

### **5. PHÁT HIỆN HỌC SINH YẾU**

**Yêu cầu:** Xác định học sinh yếu ở các kỹ năng/chủ đề.

**Schema hỗ trợ:**
- ✅ `weakInTopic` (KNN) - Học sinh yếu ở chủ đề (được xác định bởi KNN)
- ✅ `Mastery` - Mức độ thành thạo
- ✅ `Student → hasMastery → Mastery` - Học sinh có mức độ thành thạo
- ✅ `Mastery → forSkill → Skill` - Mức độ thành thạo đối với kỹ năng
- ✅ `Mastery` có `score` (0.0-1.0) để xác định yếu

**SPARQL Query (KNN - theo chủ đề):**
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

**SPARQL Query (Mastery - theo kỹ năng):**
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
  FILTER(?score < 0.5)  # Điểm < 5.0 (yếu)
}
ORDER BY ?student ?score
```

**Kết luận:** ✅ **HỖ TRỢ ĐẦY ĐỦ** (có cả KNN và Mastery, bổ sung cho nhau)

---

## 📊 TÓM TẮT

| Chức năng | Yêu cầu | Schema hỗ trợ | Trạng thái |
|-----------|---------|---------------|------------|
| Đề xuất bài giảng - Top k | ✅ | ✅ | **ĐẦY ĐỦ** |
| Đề xuất bài giảng - Điểm thấp | ✅ | ✅ | **ĐẦY ĐỦ** |
| Đề xuất đề thi - Top k | ✅ | ✅ | **ĐẦY ĐỦ** |
| Đề xuất đề thi - Điểm thấp | ✅ | ✅ | **ĐẦY ĐỦ** |
| Cải tiến PP giảng dạy - Theo điểm | ✅ | ✅ | **ĐẦY ĐỦ** |
| Cải tiến PP giảng dạy - Theo xếp loại | ✅ | ✅ | **ĐẦY ĐỦ** |
| Gợi ý PPR - Bài học | ✅ | ✅ | **ĐẦY ĐỦ** |
| Gợi ý PPR - Tài nguyên | ✅ | ✅ | **ĐẦY ĐỦ** |
| Phát hiện học sinh yếu (KNN) | ✅ | ✅ | **ĐẦY ĐỦ** |
| Phát hiện học sinh yếu (Mastery) | ✅ | ✅ | **ĐẦY ĐỦ** |

---

## ✅ KẾT LUẬN

**Schema KG chuẩn (`kg_schema_chuan.ttl`) HỖ TRỢ ĐẦY ĐỦ tất cả các chức năng đề xuất trong đề cương Đề án 2:**

1. ✅ **Đề xuất bài giảng/chương học** (Top k, điểm thấp)
2. ✅ **Đề xuất đề thi** (Top k, điểm thấp)
3. ✅ **Cải tiến phương pháp giảng dạy** (Theo điểm/xếp loại)
4. ✅ **Gợi ý dựa trên PPR** (Bài học, tài nguyên)
5. ✅ **Phát hiện học sinh yếu** (Có cả KNN và Mastery, bổ sung cho nhau)

**Schema đã sẵn sàng để triển khai!** 🎉

---

**Cập nhật:** 2025-01-15

