# 🚀 TIẾP TỤC UPLOAD TẦNG B - MASTER DATA

## ✅ ĐÃ HOÀN THÀNH

- ✅ Schema (Tầng A) - 319 triples
- ✅ grades.ttl - Upload thành công
- ✅ topics.ttl - Upload thành công  
- ✅ lessons.ttl - Upload thành công

---

## 📋 CÒN LẠI TRONG TẦNG B

### **Upload tiếp theo (theo thứ tự):**

```
4. classes.ttl          ← Upload tiếp theo
5. skills.ttl
6. resources.ttl
```

---

## 🔍 BƯỚC 1: UPLOAD `classes.ttl`

### **Cách upload:**
1. GraphDB Desktop → Chọn repository `tinhoc_thcs`
2. Import → RDF → Upload RDF files
3. Chọn: `KG_Design/data/grade6/ttl/classes.ttl`
4. Import
5. Đợi hoàn thành

### **Kiểm tra sau khi upload:**

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
LIMIT 20
```

**Kỳ vọng:** Thấy các lớp như 6A, 6B, 7A, 7B...

---

## 🔍 BƯỚC 2: UPLOAD `skills.ttl`

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?skill ?skillId ?name ?bloomLevel
WHERE {
  ?skill a edu:Skill ;
         edu:skillId ?skillId ;
         edu:name ?name .
  OPTIONAL { ?skill edu:bloomLevel ?bloomLevel }
}
ORDER BY ?skillId
LIMIT 20
```

**Kỳ vọng:** Thấy các kỹ năng như "Nhận biết", "Thông hiểu", "Vận dụng"...

---

## 🔍 BƯỚC 3: UPLOAD `resources.ttl`

### **Kiểm tra sau khi upload:**

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX data: <http://education.vn/data/>

SELECT ?resource ?resId ?title ?mediaType
WHERE {
  ?resource a edu:Resource ;
            edu:resId ?resId ;
            edu:title ?title .
  OPTIONAL { ?resource edu:mediaType ?mediaType }
}
ORDER BY ?resId
LIMIT 20
```

**Kỳ vọng:** Thấy các tài nguyên học tập

---

## ✅ CHECKLIST TẦNG B

```
□ grades.ttl          ✅ Đã upload
□ topics.ttl          ✅ Đã upload
□ lessons.ttl         ✅ Đã upload
□ classes.ttl         ⏳ Upload tiếp theo
□ skills.ttl          ⏳ Upload tiếp theo
□ resources.ttl       ⏳ Upload tiếp theo
```

---

## 🎯 SAU KHI HOÀN THÀNH TẦNG B

### **Bước tiếp theo: Tầng C - Entity Data**

```
7. students.ttl (hoặc students_updated.ttl)
8. questions_updated.ttl
9. tests.ttl
```

---

## 📊 QUERY KIỂM TRA TỔNG QUAN SAU TẦNG B

Sau khi upload xong tất cả Tầng B, chạy query này:

```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT 
  (COUNT(DISTINCT ?grade) as ?gradeCount)
  (COUNT(DISTINCT ?class) as ?classCount)
  (COUNT(DISTINCT ?topic) as ?topicCount)
  (COUNT(DISTINCT ?lesson) as ?lessonCount)
  (COUNT(DISTINCT ?skill) as ?skillCount)
  (COUNT(DISTINCT ?resource) as ?resourceCount)
WHERE {
  { ?grade a edu:Grade }
  UNION
  { ?class a edu:Class }
  UNION
  { ?topic a edu:Topic }
  UNION
  { ?lesson a edu:Lesson }
  UNION
  { ?skill a edu:Skill }
  UNION
  { ?resource a edu:Resource }
}
```

**Kỳ vọng:**
- gradeCount: 4 (6, 7, 8, 9)
- classCount: ~20-30 (tùy số lớp)
- topicCount: ~24 (6 topics × 4 grades)
- lessonCount: ~150 (tùy số bài học)
- skillCount: ~10-20 (tùy số kỹ năng)
- resourceCount: ~50-100 (tùy số tài nguyên)

---

## ⚠️ LƯU Ý

### **Nếu gặp lỗi RDF Parse:**
- Kiểm tra xem file có dùng dấu `/` trong URI không
- Nếu có, chạy script sửa:
  ```bash
  python KG_Design/scripts/fix_slash_in_uris.py
  ```

### **Nếu gặp lỗi "Undefined class":**
- Kiểm tra schema đã upload chưa
- Kiểm tra namespace có đúng không

---

## 🚀 BẮT ĐẦU NGAY

**Upload `classes.ttl` ngay bây giờ!**

Sau đó tiếp tục với `skills.ttl` và `resources.ttl`.

---

**Chúc bạn upload thành công! 🎉**

