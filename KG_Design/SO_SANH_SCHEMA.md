# 📊 SO SÁNH SCHEMA CŨ VÀ SCHEMA CHUẨN

## 🎯 TỔNG QUAN

Tài liệu này so sánh schema cũ (`kg_schema_grade7.ttl`) và schema chuẩn mới (`kg_schema_chuan.ttl`) dựa trên đề cương Đề án 2.

---

## 🔄 THAY ĐỔI CHÍNH

### **1. GIỮ LẠI KNN**

| Schema cũ | Schema chuẩn |
|-----------|--------------|
| ✅ Có `weakInTopic` (KNN) | ✅ **GIỮ** `weakInTopic` |
| `Student → weakInTopic → Topic` | `Student → weakInTopic → Topic` |

**Lý do:** Quan hệ `weakInTopic` được giữ lại để hỗ trợ phát hiện học sinh yếu ở chủ đề thông qua thuật toán KNN.

**Sử dụng kết hợp:** Có thể sử dụng cả `weakInTopic` (KNN) và `Mastery` để có cái nhìn toàn diện:
```sparql
# Tìm học sinh yếu ở chủ đề (KNN)
SELECT ?student ?topic ?topicLabel
WHERE {
  ?student edu:weakInTopic ?topic .
  ?topic edu:label ?topicLabel .
}

# Tìm học sinh yếu ở kỹ năng (Mastery)
SELECT ?student ?skill ?score
WHERE {
  ?mastery edu:hasMastery ?student ;
           edu:forSkill ?skill ;
           edu:score ?score .
  FILTER(?score < 0.5)  # < 5.0 điểm
}
```

---

### **2. THÊM MASTERY (Mức độ thành thạo)**

| Schema cũ | Schema chuẩn |
|-----------|--------------|
| ❌ Không có class `Mastery` | ✅ **THÊM** class `Mastery` |
| Chỉ có `TestResult` | Có cả `TestResult` và `Mastery` |

**Lý do:** Cần theo dõi mức độ thành thạo của học sinh đối với từng kỹ năng một cách chi tiết hơn.

**Cấu trúc:**
```
Student → hasMastery → Mastery → forSkill → Skill
Mastery có: score (0.0-1.0), lastUpdated
```

---

### **3. BỔ SUNG RESOURCE**

| Schema cũ | Schema chuẩn |
|-----------|--------------|
| ❌ Không có class `Resource` | ✅ **THÊM** class `Resource` |
| Không có quan hệ với Resource | Có `coversSkill` và `recommendedResourceFor` |

**Lý do:** Cần mô hình hóa tài nguyên học tập (HTML, video, PDF) để hỗ trợ gợi ý.

**Cấu trúc:**
```
Resource → coversSkill → Skill (với coverage)
Resource → recommendedResourceFor → Student (PPR)
```

---

### **4. BỔ SUNG THUỘC TÍNH**

| Thuộc tính | Schema cũ | Schema chuẩn |
|------------|-----------|--------------|
| `studentId` | ❌ | ✅ |
| `teacherId` | ✅ | ✅ |
| `topicId` | ❌ | ✅ |
| `lessonId` | ❌ | ✅ |
| `q_id` | ❌ | ✅ |
| `skillId` | ❌ | ✅ |
| `resId` | ❌ | ✅ |
| `testId` | ❌ | ✅ |
| `coverage` | ❌ | ✅ (cho quan hệ Resource-Skill) |
| `lastUpdated` | ❌ | ✅ (cho Mastery) |

---

### **5. QUAN HỆ MỚI**

| Quan hệ | Schema cũ | Schema chuẩn |
|---------|-----------|--------------|
| `coversSkill` | ❌ | ✅ Resource → Skill |
| `prerequisiteOf` | ❌ | ✅ Skill → Skill |
| `hasMastery` | ❌ | ✅ Student → Mastery |
| `forSkill` | ❌ | ✅ Mastery → Skill |
| `recommendedResourceFor` | ❌ | ✅ Resource → Student (PPR) |
| `weakInTopic` | ✅ | ✅ **GIỮ** |

---

## 📋 BẢNG SO SÁNH ĐẦY ĐỦ

### **THỰC THỂ (Classes)**

| Class | Schema cũ | Schema chuẩn | Ghi chú |
|-------|-----------|--------------|---------|
| Student | ✅ | ✅ | Giữ nguyên |
| Teacher | ✅ | ✅ | Giữ nguyên |
| Class | ✅ | ✅ | Giữ nguyên |
| Grade | ✅ | ✅ | Giữ nguyên |
| Topic | ✅ | ✅ | Giữ nguyên |
| Lesson | ✅ | ✅ | Giữ nguyên |
| Question | ✅ | ✅ | Giữ nguyên |
| Skill | ✅ | ✅ | Giữ nguyên |
| Resource | ❌ | ✅ | **THÊM MỚI** |
| Test | ✅ | ✅ | Giữ nguyên |
| TestResult | ✅ | ✅ | Giữ nguyên |
| Mastery | ❌ | ✅ | **THÊM MỚI** |

### **QUAN HỆ (Properties)**

| Quan hệ | Schema cũ | Schema chuẩn | Ghi chú |
|---------|-----------|--------------|---------|
| belongsToClass | ✅ | ✅ | Giữ nguyên |
| belongsToGrade | ✅ | ✅ | Giữ nguyên |
| teaches | ✅ | ✅ | Giữ nguyên |
| belongsToTopic | ✅ | ✅ | Giữ nguyên |
| forGrade | ✅ | ✅ | Giữ nguyên |
| belongsToLesson | ✅ | ✅ | Giữ nguyên |
| requiresSkill | ✅ | ✅ | Giữ nguyên |
| coversSkill | ❌ | ✅ | **THÊM MỚI** |
| prerequisiteOf | ❌ | ✅ | **THÊM MỚI** |
| takeTest | ✅ | ✅ | Giữ nguyên |
| hasQuestion | ✅ | ✅ | Giữ nguyên |
| hasResult | ✅ | ✅ | Giữ nguyên |
| forTest | ✅ | ✅ | Giữ nguyên |
| hasMastery | ❌ | ✅ | **THÊM MỚI** |
| forSkill | ❌ | ✅ | **THÊM MỚI** |
| recommendedFor | ✅ | ✅ | Giữ nguyên (PPR) |
| recommendedResourceFor | ❌ | ✅ | **THÊM MỚI** (PPR) |
| weakInTopic | ✅ | ✅ | **GIỮ NGUYÊN** (KNN) |

---

## 🔄 HƯỚNG DẪN CHUYỂN ĐỔI

### **Bước 1: Cập nhật Schema**

1. Import schema mới vào GraphDB:
   ```bash
   # Upload file: KG_Design/kg_schema_chuan.ttl
   ```

2. **LƯU Ý:** Schema mới **CÓ** `weakInTopic`, nên các query cũ dùng quan hệ này vẫn hoạt động bình thường.

### **Bước 2: Cập nhật Dữ liệu**

1. **Thêm Mastery:**
   - Tạo file `mastery.ttl` từ `student_mastery.csv`
   - Import vào GraphDB

2. **Thêm Resource:**
   - Tạo file `resources.ttl` từ `resources.csv`
   - Tạo file `resource_skill.ttl` từ `resource_skill.csv`
   - Import vào GraphDB

3. **Giữ dữ liệu cũ:**
   - Giữ các triple có `weakInTopic` (nếu đã có)

### **Bước 3: Cập nhật Query**

**Query dùng weakInTopic (KNN):**
```sparql
# ✅ HOẠT ĐỘNG trong schema mới
SELECT ?student ?topic ?topicLabel
WHERE {
  ?student edu:weakInTopic ?topic .
  ?topic edu:label ?topicLabel .
}
```

**Query dùng Mastery (bổ sung):**
```sparql
# ✅ HOẠT ĐỘNG trong schema mới
SELECT ?student ?skill ?score
WHERE {
  ?mastery edu:hasMastery ?student ;
           edu:forSkill ?skill ;
           edu:score ?score .
  FILTER(?score < 0.5)  # Học sinh yếu
}
```

**Lưu ý:** Có thể sử dụng cả hai phương pháp để có cái nhìn toàn diện hơn.

---

## ✅ CHECKLIST CHUYỂN ĐỔI

- [ ] Import schema mới (`kg_schema_chuan.ttl`)
- [ ] Xóa schema cũ (nếu cần)
- [ ] Thêm dữ liệu Mastery
- [ ] Thêm dữ liệu Resource
- [ ] Thêm quan hệ Resource-Skill
- [ ] Giữ dữ liệu `weakInTopic` (nếu đã có)
- [ ] Cập nhật các query SPARQL
- [ ] Test các query mới
- [ ] Cập nhật documentation

---

## 🎯 KẾT LUẬN

Schema chuẩn mới:
- ✅ **Giữ KNN** (`weakInTopic`) để phát hiện học sinh yếu ở chủ đề
- ✅ **Thêm Mastery** để theo dõi thành thạo kỹ năng (bổ sung cho KNN)
- ✅ **Thêm Resource** để hỗ trợ gợi ý tài nguyên
- ✅ **Giữ PPR** để gợi ý bài học/tài nguyên
- ✅ **Đầy đủ thuộc tính** cho tất cả thực thể

Schema mới phù hợp với đề cương Đề án 2 và hỗ trợ đầy đủ các chức năng cần thiết, bao gồm cả KNN và PPR.

---

**Cập nhật:** 2025-01-15

