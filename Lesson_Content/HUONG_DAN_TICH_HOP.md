# 🔗 Hướng Dẫn Tích Hợp Hệ Thống Nội Dung Bài Học

## 📋 Tổng Quan

Hướng dẫn này giúp bạn tích hợp hệ thống nội dung bài học mới vào hệ thống hiện tại.

## ✅ Đã Hoàn Thành

1. ✅ Cấu trúc thư mục
2. ✅ Template HTML (lesson_main.html, pdf_viewer.html, slides_viewer.html, video_player.html)
3. ✅ CSS & JavaScript (lesson.css, lesson.js)
4. ✅ Scripts chuyển đổi (convert_documents.py, generate_lesson.py)
5. ✅ Bài học mẫu (K6/A1_lesson_content.html)

## 🚀 Các Bước Tích Hợp

### Bước 1: Cập nhật index.html

Thêm link đến bài học có nội dung đầy đủ trong `index.html`:

#### Option 1: Thêm nút mới "Xem đầy đủ"

```html
<!-- Tìm section bài học K6_A1 hiện tại -->
<a class="btn small primary" href="Web/K6_A1.html" onclick="return ensureAuth('Web/K6_A1.html')">
  💻A1
</a>

<!-- Thêm nút mới ngay bên cạnh -->
<a class="btn small success" href="Lesson_Content/K6/A1_lesson_content.html" onclick="return ensureAuth('Lesson_Content/K6/A1_lesson_content.html')">
  📚 A1 (Đầy đủ)
</a>
```

#### Option 2: Thay thế link hiện tại

```html
<!-- Trước: Chỉ có quiz -->
<a href="Web/K6_A1.html">💻A1</a>

<!-- Sau: Link đến trang nội dung đầy đủ -->
<a href="Lesson_Content/K6/A1_lesson_content.html">💻A1</a>
```

#### Option 3: Dropdown menu

```html
<div class="lesson-dropdown">
  <button class="btn">💻 A1: Máy tính ▼</button>
  <div class="dropdown-menu">
    <a href="Lesson_Content/K6/A1_lesson_content.html">📚 Học bài</a>
    <a href="Web/K6_A1.html">✅ Kiểm tra</a>
  </div>
</div>
```

### Bước 2: Tạo Trang Tổng Quan (Dashboard)

Tạo file `Lesson_Content/dashboard.html`:

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <title>📚 Tổng Quan Bài Học</title>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-purple-100 to-indigo-100 min-h-screen">
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-4xl font-bold text-center mb-8">📚 Bài Học Của Tôi</h1>
    
    <!-- Thống kê -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-white rounded-xl p-6 shadow-lg">
        <div class="text-3xl mb-2">📖</div>
        <div class="text-2xl font-bold" id="totalLessons">0</div>
        <div class="text-gray-600">Tổng bài học</div>
      </div>
      <div class="bg-white rounded-xl p-6 shadow-lg">
        <div class="text-3xl mb-2">✅</div>
        <div class="text-2xl font-bold text-green-600" id="completedLessons">0</div>
        <div class="text-gray-600">Đã hoàn thành</div>
      </div>
      <div class="bg-white rounded-xl p-6 shadow-lg">
        <div class="text-3xl mb-2">⏱️</div>
        <div class="text-2xl font-bold text-blue-600" id="totalTime">0h</div>
        <div class="text-gray-600">Thời gian học</div>
      </div>
      <div class="bg-white rounded-xl p-6 shadow-lg">
        <div class="text-3xl mb-2">🎯</div>
        <div class="text-2xl font-bold text-purple-600" id="avgProgress">0%</div>
        <div class="text-gray-600">Tiến độ TB</div>
      </div>
    </div>
    
    <!-- Danh sách bài học -->
    <div id="lessonsList" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Lessons will be populated by JavaScript -->
    </div>
  </div>
  
  <script src="assets/js/lesson.js"></script>
  <script>
    // Danh sách bài học
    const lessons = [
      {
        id: 'K6_A1_CONTENT',
        title: 'A1: Máy tính và ứng dụng',
        icon: '💻',
        grade: 'Lớp 6',
        url: 'K6/A1_lesson_content.html'
      },
      // Thêm các bài học khác...
    ];
    
    // Hiển thị thống kê
    function updateStats() {
      const progress = LessonManager.progress;
      const totalLessons = lessons.length;
      const completedLessons = LessonManager.getCompletedLessons().length;
      const totalTime = LessonManager.getTotalTimeSpent();
      
      document.getElementById('totalLessons').textContent = totalLessons;
      document.getElementById('completedLessons').textContent = completedLessons;
      document.getElementById('totalTime').textContent = Utils.formatTime(totalTime);
      
      const avgProgress = totalLessons > 0 
        ? Math.round((completedLessons / totalLessons) * 100) 
        : 0;
      document.getElementById('avgProgress').textContent = avgProgress + '%';
    }
    
    // Hiển thị danh sách bài học
    function renderLessons() {
      const container = document.getElementById('lessonsList');
      container.innerHTML = '';
      
      lessons.forEach(lesson => {
        const progress = LessonManager.getLessonProgress(lesson.id);
        const percentage = LessonManager.getCompletionPercentage(lesson.id);
        
        const card = document.createElement('div');
        card.className = 'bg-white rounded-xl shadow-lg p-6 hover:shadow-2xl transition cursor-pointer';
        card.onclick = () => window.location.href = lesson.url;
        
        card.innerHTML = `
          <div class="text-5xl mb-3">${lesson.icon}</div>
          <h3 class="text-xl font-bold mb-2">${lesson.title}</h3>
          <div class="text-sm text-gray-600 mb-3">${lesson.grade}</div>
          
          <div class="mb-2">
            <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
              <div class="h-full bg-gradient-to-r from-purple-600 to-indigo-600" 
                   style="width: ${percentage}%"></div>
            </div>
          </div>
          
          <div class="flex justify-between items-center">
            <span class="text-sm font-bold text-purple-600">${percentage}%</span>
            ${progress.fullyCompleted ? 
              '<span class="text-green-600 font-bold">✅ Hoàn thành</span>' :
              '<span class="text-gray-500">Đang học...</span>'
            }
          </div>
        `;
        
        container.appendChild(card);
      });
    }
    
    // Init
    updateStats();
    renderLessons();
  </script>
</body>
</html>
```

### Bước 3: Thêm Menu Navigation

Cập nhật header trong `index.html`:

```html
<nav class="navigation-menu">
  <a href="index.html">🏠 Trang chủ</a>
  <a href="Lesson_Content/dashboard.html">📚 Bài học của tôi</a>
  <a href="#grades">📖 Các lớp</a>
  <a href="login.html">👤 Đăng nhập</a>
</nav>
```

### Bước 4: Tạo Nội Dung Cho Các Bài Học

#### 4.1. Chuẩn bị tài liệu

Tổ chức tài liệu theo cấu trúc:

```
Lesson_Content/
└── K6/
    └── A1/
        ├── theory.pdf          # Giáo trình lý thuyết
        ├── slides.pptx         # Slide bài giảng
        ├── slides/             # Slide đã convert thành ảnh
        │   ├── slide1.jpg
        │   ├── slide2.jpg
        │   └── ...
        ├── video.mp4           # Video bài giảng
        └── video_poster.jpg    # Ảnh thumbnail video
```

#### 4.2. Chuyển đổi tài liệu

```bash
# Chuyển PPTX thành ảnh
cd Lesson_Content/scripts
python convert_documents.py ../../path/to/slides.pptx -o ../K6/A1/slides

# Chuyển DOCX thành HTML
python convert_documents.py ../../path/to/theory.docx -o ../K6/A1
```

#### 4.3. Tạo config file

Tạo `K6_A1_config.json`:

```json
{
  "lesson_id": "K6_A1_CONTENT",
  "lesson_code": "A1",
  "lesson_title": "Máy tính và ứng dụng",
  "lesson_icon": "💻",
  "lesson_description": "Tìm hiểu về máy tính và các ứng dụng của máy tính",
  "grade": "Lớp 6",
  
  "theory": {
    "type": "pdf",
    "url": "/Lesson_Content/K6/A1/theory.pdf",
    "title": "Giáo trình: Máy tính và ứng dụng"
  },
  
  "slides": {
    "type": "images",
    "slides": [
      "/Lesson_Content/K6/A1/slides/slide1.jpg",
      "/Lesson_Content/K6/A1/slides/slide2.jpg",
      "/Lesson_Content/K6/A1/slides/slide3.jpg"
    ],
    "notes": ["Giới thiệu", "Nội dung", "Tổng kết"],
    "url": "/Lesson_Content/K6/A1/slides.pptx"
  },
  
  "video": {
    "id": "K6_A1_video",
    "url": "/Lesson_Content/K6/A1/video.mp4",
    "title": "Video bài giảng",
    "poster": "/Lesson_Content/K6/A1/video_poster.jpg",
    "chapters": [
      {"time": 0, "title": "Giới thiệu"},
      {"time": 120, "title": "Nội dung chính"}
    ],
    "notes": "Xem video để hiểu rõ hơn"
  },
  
  "quiz_url": "/Web/K6_A1.html"
}
```

#### 4.4. Generate HTML

```bash
python generate_lesson.py --config K6_A1_config.json
```

### Bước 5: Test

1. Mở `Lesson_Content/K6/A1_lesson_content.html` trong browser
2. Kiểm tra:
   - ✅ Navigation giữa các tab
   - ✅ PDF hiển thị đúng
   - ✅ Slide navigation hoạt động
   - ✅ Video play được
   - ✅ Progress tracking
   - ✅ Link đến quiz

### Bước 6: Deploy

#### Development (Local):
```bash
# Chỉ cần mở file HTML trong browser
# hoặc dùng live server
python -m http.server 8000
```

#### Production (GitHub Pages):
```bash
git add Lesson_Content/
git commit -m "Add unified lesson content system"
git push origin main
```

## 📊 Monitoring & Analytics

### Xem tiến độ học sinh

Thêm vào console:

```javascript
// Xem tất cả tiến độ
console.log(LessonManager.progress);

// Xem bài đã hoàn thành
console.log(LessonManager.getCompletedLessons());

// Tổng thời gian học
console.log(Utils.formatTime(LessonManager.getTotalTimeSpent()));
```

### Export dữ liệu

```javascript
// Export progress của học sinh
LessonManager.exportProgress();
```

## 🔄 Quy Trình Làm Việc Hàng Ngày

### Thêm bài học mới:

1. Chuẩn bị tài liệu (PDF, PPTX, MP4)
2. Chạy `convert_documents.py` để chuyển đổi
3. Tạo file config JSON
4. Chạy `generate_lesson.py` để tạo HTML
5. Cập nhật link trong `index.html`
6. Test và deploy

### Cập nhật bài học hiện có:

1. Cập nhật file tài liệu
2. Chạy lại `convert_documents.py` nếu cần
3. Chạy lại `generate_lesson.py`
4. Clear browser cache để test

## ⚙️ Cấu Hình Nâng Cao

### Thay đổi theme colors

Sửa trong `Lesson_Content/assets/css/lesson.css`:

```css
:root {
  --primary-purple: #667eea;  /* Màu chính */
  --primary-indigo: #764ba2;  /* Màu phụ */
}
```

### Thêm tính năng mới

Sửa trong `Lesson_Content/assets/js/lesson.js`:

```javascript
// Thêm function mới vào LessonManager
LessonManager.customFeature = function() {
  // Code của bạn
};
```

## 🐛 Troubleshooting

### Vấn đề thường gặp:

1. **PDF không hiển thị:**
   - Kiểm tra đường dẫn file
   - Kiểm tra CORS (nếu chạy local, dùng http-server)

2. **Video không play:**
   - Kiểm tra codec (dùng H.264)
   - Kiểm tra file size
   - Thử format khác (MP4, WebM)

3. **Slide không hiển thị:**
   - Kiểm tra array slides trong config
   - Kiểm tra đường dẫn ảnh

4. **Progress không lưu:**
   - Kiểm tra localStorage có enabled không
   - Clear cache và thử lại

## 📞 Support

Nếu gặp vấn đề, kiểm tra:
1. Console log (F12)
2. Network tab (xem request nào fail)
3. localStorage (Application tab)

---

**Chúc bạn tích hợp thành công! 🎉**


