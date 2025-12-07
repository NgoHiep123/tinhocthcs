# 🔧 ĐÃ SỬA LỖI: RDF Parse Error - Dấu "/" trong URI

## ⚠️ VẤN ĐỀ

**Lỗi:** `RDF Parse Error: Expected an RDF value here, found '/' [line 7]`

**Nguyên nhân:** Dấu `/` trong URI như `data:grade/6` không hợp lệ trong Turtle syntax.

---

## ✅ ĐÃ SỬA

### **File đã sửa:**

1. ✅ `grades.ttl`
   - `data:grade/6` → `data:grade_6`
   - `data:grade/7` → `data:grade_7`
   - `data:grade/8` → `data:grade_8`
   - `data:grade/9` → `data:grade_9`

2. ✅ `topics.ttl`
   - `data:topic/6_A` → `data:topic_6_A`
   - `data:grade/6` → `data:grade_6`
   - (Tất cả các topic đã được sửa)

3. ✅ `lessons.ttl`
   - `data:lesson/6_A1` → `data:lesson_6_A1`
   - `data:topic/6_A` → `data:topic_6_A`
   - (Tất cả các lesson đã được sửa)

---

## 🚀 BÂY GIỜ CÓ THỂ UPLOAD

### **Thứ tự upload:**

1. ✅ **grades.ttl** (đã sửa)
2. ✅ **topics.ttl** (đã sửa)
3. ✅ **lessons.ttl** (đã sửa)

---

## 📋 KIỂM TRA SAU KHI UPLOAD

### **Query kiểm tra Grades:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?grade ?gradeNumber
WHERE {
  ?grade a edu:Grade ;
         edu:grade ?gradeNumber
}
ORDER BY ?gradeNumber
```

**Kỳ vọng:** Thấy Grade 6, 7, 8, 9

---

### **Query kiểm tra Topics:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?topic ?topicId ?label ?grade
WHERE {
  ?topic a edu:Topic ;
         edu:topicId ?topicId ;
         edu:label ?label ;
         edu:grade ?grade
}
ORDER BY ?grade ?topicId
LIMIT 20
```

**Kỳ vọng:** Thấy các topics như 6_A, 6_B, 7_A...

---

### **Query kiểm tra Lessons:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?lesson ?lessonId ?label ?topic
WHERE {
  ?lesson a edu:Lesson ;
          edu:lessonId ?lessonId ;
          edu:label ?label ;
          edu:belongsToTopic ?topicIRI .
  ?topicIRI edu:topicId ?topic
}
ORDER BY ?lessonId
LIMIT 20
```

**Kỳ vọng:** Thấy các lessons như A1, A2, B1...

---

## ⚠️ LƯU Ý CHO CÁC FILE KHÁC

### **Nếu gặp lỗi tương tự với file khác:**

**Nguyên tắc:** 
- ❌ **KHÔNG dùng:** `data:entity/name`
- ✅ **DÙNG:** `data:entity_name` (dấu `_` thay vì `/`)

**Ví dụ:**
- ❌ `data:student/001` 
- ✅ `data:student_001`

- ❌ `data:class/6A`
- ✅ `data:class_6A`

---

## 🔍 KIỂM TRA FILE KHÁC CÓ LỖI TƯƠNG TỰ

Các file có thể cần kiểm tra:
- `classes.ttl` - Có thể dùng `data:class/6A`
- `students.ttl` - Có thể dùng `data:student/001`
- `questions_updated.ttl` - Có thể dùng `data:question/001`
- `tests.ttl` - Có thể dùng `data:test/001`
- Các file khác trong Tầng C, D, E

**Nếu gặp lỗi tương tự → Sửa theo cách trên!**

---

## ✅ CHECKLIST UPLOAD TẦNG B

```
□ grades.ttl - Đã sửa, upload OK
□ topics.ttl - Đã sửa, upload OK
□ lessons.ttl - Đã sửa, upload OK
□ classes.ttl - Kiểm tra nếu có lỗi
□ skills.ttl - Kiểm tra nếu có lỗi
□ resources.ttl - Kiểm tra nếu có lỗi
```

---

## 🎯 BƯỚC TIẾP THEO

1. ✅ Upload lại `grades.ttl` (đã sửa)
2. ✅ Upload lại `topics.ttl` (đã sửa)
3. ✅ Upload lại `lessons.ttl` (đã sửa)
4. ⏭️ Tiếp tục với `classes.ttl`, `skills.ttl`, `resources.ttl`

---

**Các file đã được sửa! Hãy upload lại và kiểm tra! 🚀**

