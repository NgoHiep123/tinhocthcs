# ✅ KIỂM TRA FILE HÌNH `Knowledge_graph.png`

## 📋 HƯỚNG DẪN KIỂM TRA

Mở file `Knowledge_graph.png` và đối chiếu với checklist dưới đây.

---

## ✅ CHECKLIST: CÁC THỰC THỂ (ENTITIES/CLASSES) CẦN CÓ

### **Thực thể bắt buộc:**
- [ ] **Student** (Học sinh) - Có trong hình
- [ ] **Class** (Lớp học) - Có trong hình
- [ ] **Grade** (Khối lớp) - Có trong hình
- [ ] **Topic** (Chủ đề) - Có trong hình
- [ ] **Lesson** (Bài học) - Có trong hình
- [ ] **Question** (Câu hỏi) - Có trong hình
- [ ] **Skill** (Kỹ năng) - Có trong hình

### **Thực thể quan trọng:**
- [ ] **Resource** (Tài nguyên) - Có trong hình
- [ ] **Test** hoặc **Assessment** (Bài kiểm tra) - Có trong hình
- [ ] **TestResult** (Kết quả) - Có trong hình

### **Thực thể tùy chọn:**
- [ ] **Teacher** (Giáo viên) - Có trong hình (không bắt buộc)
- [ ] **Mastery** (Độ thành thạo) - Có trong hình (tùy chọn)

---

## ✅ CHECKLIST: CÁC QUAN HỆ (RELATIONSHIPS) CẦN CÓ

### **Quan hệ phân cấp:**
- [ ] **Student** → `belongsToClass` → **Class**
- [ ] **Class** → `belongsToGrade` → **Grade**
- [ ] **Lesson** → `belongsToTopic` → **Topic**
- [ ] **Topic** → `forGrade` → **Grade**
- [ ] **Question** → `belongsToLesson` → **Lesson** (hoặc `belongsToSkill` → **Skill**)

### **Quan hệ kỹ năng:**
- [ ] **Question** → `requiresSkill` hoặc `measures` → **Skill**
- [ ] **Resource** → `COVERS` hoặc `covers` → **Skill** (với `coverage` 0.0-1.0)
- [ ] **Skill** → `prerequisiteOf` hoặc `PREREQUISITE_OF` → **Skill**

### **Quan hệ đánh giá:**
- [ ] **Student** → `takeTest` hoặc `takes` → **Test**
- [ ] **Test** → `hasQuestion` hoặc `contains` → **Question**
- [ ] **Student** → `hasResult` → **TestResult**
- [ ] **TestResult** → `forTest` → **Test**

### **Quan hệ ML (Machine Learning):**
- [ ] **Student** → `weakInTopic` → **Topic** (được xác định bởi KNN)
- [ ] **Lesson** → `recommendedFor` → **Student** (được xác định bởi PPR)

### **Quan hệ tùy chọn:**
- [ ] **Student** → `MASTERY` hoặc `mastery` → **Skill** (với `score` 0.0-1.0)
- [ ] **Teacher** → `teaches` → **Class** (tùy chọn)

---

## ✅ CHECKLIST: CẤU TRÚC PHÂN CẤP

Kiểm tra cấu trúc phân cấp trong hình có đúng không:

### **Phân cấp lớp học:**
```
Grade (Khối)
  └─ Class (Lớp)
      └─ Student (Học sinh)
```

### **Phân cấp bài học:**
```
Grade (Khối)
  └─ Topic (Chủ đề: A, B, C, D, E, F)
      └─ Lesson (Bài học: A1, A2, B1, ...)
          └─ Question (Câu hỏi)
```

### **Quan hệ kỹ năng:**
```
Skill (Kỹ năng)
  ├─ PREREQUISITE_OF → Skill (Kỹ năng khác)
  ├─ Question → requiresSkill → Skill
  └─ Resource → COVERS → Skill
```

---

## ✅ KIỂM TRA NỘI DUNG CHƯƠNG TRÌNH

### **Khối 6 - 6 chủ đề:**
- [ ] **Chủ đề A**: Máy tính và cộng đồng
- [ ] **Chủ đề B**: Mạng máy tính và Internet
- [ ] **Chủ đề C**: Tổ chức lưu trữ, tìm kiếm thông tin
- [ ] **Chủ đề D**: Đạo đức và pháp luật
- [ ] **Chủ đề E**: Ứng dụng tin học
- [ ] **Chủ đề F**: Giải quyết vấn đề với sự trợ giúp của máy tính

### **Khối 7 - 6 chủ đề:**
- [ ] **Chủ đề A**: Máy tính và hệ điều hành
- [ ] **Chủ đề B**: Soạn thảo văn bản
- [ ] **Chủ đề C**: Mạng máy tính và Internet
- [ ] **Chủ đề D**: Trình chiếu
- [ ] **Chủ đề E**: Thuật toán và lập trình
- [ ] **Chủ đề F**: Dự án

---

## 📊 CÁC VẤN ĐỀ THƯỜNG GẶP

### **1. Thiếu thực thể:**
- ❌ **Thiếu Resource** - Cần có để lưu tài nguyên học tập (HTML, video, PDF)
- ❌ **Thiếu Skill** - Cần có để mô hình hóa kỹ năng và quan hệ tiên quyết
- ❌ **Thiếu Mastery** - Cần có để lưu độ thành thạo của học sinh

### **2. Thiếu quan hệ:**
- ❌ **Thiếu PREREQUISITE_OF** - Cần có để mô hình hóa quan hệ tiên quyết giữa các kỹ năng
- ❌ **Thiếu COVERS** - Cần có để ánh xạ tài nguyên đến kỹ năng
- ❌ **Thiếu weakInTopic** và **recommendedFor** - Cần có cho ML algorithms

### **3. Tên quan hệ sai:**
- ❌ **belongsTo** thay vì **belongsToClass**, **belongsToTopic**, **belongsToLesson**
- ❌ **has** thay vì **hasQuestion**, **hasResult**
- ❌ **requires** thay vì **requiresSkill**

---

## ✅ KẾT QUẢ KIỂM TRA

### **Điểm số:**
- **Thực thể bắt buộc (7):** ___/7
- **Thực thể quan trọng (3):** ___/3
- **Quan hệ phân cấp (5):** ___/5
- **Quan hệ kỹ năng (3):** ___/3
- **Quan hệ đánh giá (4):** ___/4
- **Quan hệ ML (2):** ___/2

### **Tổng điểm:** ___/24

### **Đánh giá:**
- ✅ **22-24 điểm**: Hình mô tả đúng và đầy đủ với chương trình
- ⚠️ **18-21 điểm**: Hình mô tả gần đúng, thiếu một số chi tiết
- ❌ **<18 điểm**: Hình mô tả chưa đúng, cần cập nhật

---

## 📝 GHI CHÚ

**Các điểm cần lưu ý:**

1. **Namespace:** Hình có thể dùng namespace khác (ví dụ: `ex:`, `edu:`) nhưng phải nhất quán

2. **Tên quan hệ:** Tên quan hệ có thể khác một chút nhưng phải đúng ý nghĩa:
   - `belongsToClass` = `belongsTo` (nếu chỉ có 1 loại belongsTo)
   - `requiresSkill` = `measures` = `relatesToSkill`

3. **Cấu trúc:** Không nhất thiết phải có tất cả thực thể trong 1 hình, có thể chia thành nhiều hình

4. **ML Relations:** Quan hệ `weakInTopic` và `recommendedFor` là kết quả từ ML, có thể không có trong hình schema ban đầu

---

## 🔧 CẦN SỬA NẾU THIẾU

Nếu hình thiếu các thành phần sau, cần cập nhật:

### **Thiếu Resource:**
- Thêm node **Resource**
- Thêm quan hệ **Resource** → `COVERS` → **Skill**

### **Thiếu quan hệ tiên quyết:**
- Thêm quan hệ **Skill** → `PREREQUISITE_OF` → **Skill**

### **Thiếu Mastery:**
- Thêm node **Mastery** hoặc quan hệ trực tiếp **Student** → `MASTERY` → **Skill**

### **Thiếu ML relations:**
- Thêm **Student** → `weakInTopic` → **Topic** (KNN)
- Thêm **Lesson** → `recommendedFor` → **Student** (PPR)

---

**File này được tạo để hỗ trợ kiểm tra `Knowledge_graph.png`**  
**Ngày:** $(date)

