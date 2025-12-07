# 📚 Hệ Thống Nội Dung Bài Học Thống Nhất

## 🎯 Mục Đích

Hệ thống này cung cấp giải pháp thống nhất để quản lý và hiển thị nội dung bài học từ nhiều định dạng khác nhau (PDF, DOCX, PPTX, MP4) trên nền tảng web, với khả năng tracking tiến độ học tập.

## ✨ Tính Năng

### 1. **Thống Nhất Định Dạng**
- ✅ PDF → Viewer nhúng trực tiếp
- ✅ DOCX → Chuyển đổi sang HTML
- ✅ PPTX → Slide viewer tương tác
- ✅ MP4 → Video player với nhiều tính năng

### 2. **Theo Dõi Tiến Độ**
- 📊 Tracking xem từng phần (Lý thuyết, Slide, Video, Quiz)
- ✅ Đánh dấu hoàn thành từng section
- ⏱️ Thống kê thời gian học
- 💾 Lưu trữ tiến độ trong localStorage

### 3. **Giao Diện Người Dùng**
- 🎨 Giao diện đẹp, hiện đại với Tailwind CSS
- 📱 Responsive - hoạt động tốt trên mọi thiết bị
- ⚡ Smooth transitions và animations
- 🎯 Navigation dễ dàng giữa các phần

### 4. **Video Player Nâng Cao**
- ⚡ Điều chỉnh tốc độ phát (0.5x - 2x)
- 📑 Chapter navigation
- 💾 Tự động lưu vị trí xem
- 🎬 Hỗ trợ nhiều chất lượng video
- ⌨️ Keyboard shortcuts

### 5. **Slide Viewer**
- 🖼️ Hiển thị slide dạng ảnh
- 📑 Thumbnails navigation
- 📝 Ghi chú cho từng slide
- ⛶ Fullscreen mode
- ⌨️ Keyboard navigation (Arrow keys)

## 📁 Cấu Trúc Thư Mục

```
Lesson_Content/
├── templates/              # Template HTML
│   ├── lesson_main.html   # Template chính
│   ├── pdf_viewer.html    # Template viewer PDF
│   ├── slides_viewer.html # Template viewer Slide
│   └── video_player.html  # Template video player
│
├── assets/
│   ├── css/
│   │   └── lesson.css     # Stylesheet chính
│   └── js/
│       └── lesson.js      # JavaScript cho tracking & navigation
│
├── scripts/                # Scripts hỗ trợ
│   ├── generate_lesson.py      # Tạo trang bài học
│   └── convert_documents.py    # Chuyển đổi tài liệu
│
├── K6/                     # Nội dung lớp 6
├── K7/                     # Nội dung lớp 7
├── K8/                     # Nội dung lớp 8
├── K9/                     # Nội dung lớp 9
│
└── README.md              # File này
```

## 🚀 Hướng Dẫn Sử Dụng

### Bước 1: Cài Đặt Dependencies

```bash
pip install pdf2image python-docx python-pptx Pillow
```

**Lưu ý:** Để convert PDF, cần cài thêm Poppler:
- Windows: [Download Poppler](https://github.com/oschwartz10612/poppler-windows/releases/)
- Linux: `sudo apt-get install poppler-utils`
- Mac: `brew install poppler`

### Bước 2: Chuyển Đổi Tài Liệu

#### Chuyển đổi PDF:
```bash
python Lesson_Content/scripts/convert_documents.py document.pdf
```

#### Chuyển đổi DOCX:
```bash
python Lesson_Content/scripts/convert_documents.py document.docx
```

#### Chuyển đổi PPTX:
```bash
python Lesson_Content/scripts/convert_documents.py presentation.pptx
```

### Bước 3: Tạo Bài Học

#### Tạo bài học mẫu:
```bash
cd Lesson_Content/scripts
python generate_lesson.py --sample
```

#### Tạo từ file config:
```bash
python generate_lesson.py --config lesson_config.json
```

### Bước 4: Config Bài Học

Tạo file `lesson_config.json`:

```json
{
  "lesson_id": "K6_A1_CONTENT",
  "lesson_code": "A1",
  "lesson_title": "Máy tính và ứng dụng",
  "lesson_icon": "💻",
  "lesson_description": "Tìm hiểu về máy tính và các ứng dụng",
  "grade": "Lớp 6",
  
  "theory": {
    "type": "pdf",
    "url": "/Lesson_Content/K6/A1/theory.pdf",
    "title": "Giáo trình lý thuyết"
  },
  
  "slides": {
    "type": "images",
    "slides": [
      "/Lesson_Content/K6/A1/slides/slide1.jpg",
      "/Lesson_Content/K6/A1/slides/slide2.jpg",
      "/Lesson_Content/K6/A1/slides/slide3.jpg"
    ],
    "notes": [
      "Giới thiệu",
      "Nội dung chính",
      "Tổng kết"
    ],
    "url": "/Lesson_Content/K6/A1/slides.pptx"
  },
  
  "video": {
    "id": "K6_A1_video",
    "url": "/Lesson_Content/K6/A1/video.mp4",
    "title": "Video bài giảng",
    "poster": "/Lesson_Content/K6/A1/poster.jpg",
    "chapters": [
      {"time": 0, "title": "Giới thiệu"},
      {"time": 120, "title": "Nội dung chính"}
    ],
    "notes": "Xem video để hiểu rõ hơn"
  },
  
  "quiz_url": "/Web/K6_A1.html"
}
```

## 📖 Cấu Trúc Bài Học

Mỗi bài học gồm 4 phần:

1. **📖 Lý thuyết** - Nội dung giáo trình (PDF/HTML)
2. **📊 Slide** - Slide bài giảng (PPTX → Images)
3. **🎥 Video** - Video giảng dạy (MP4)
4. **✅ Kiểm tra** - Bài quiz đánh giá (Link đến quiz)

## 🎨 Tùy Chỉnh Giao Diện

### CSS Variables (trong `lesson.css`)

```css
:root {
  --primary-purple: #667eea;
  --primary-indigo: #764ba2;
  --success-green: #10b981;
  --warning-yellow: #f59e0b;
  --danger-red: #ef4444;
}
```

### Thay đổi màu chủ đạo:
Sửa biến trong file `Lesson_Content/assets/css/lesson.css`

## 📊 Tracking & Analytics

### Dữ liệu được lưu trong localStorage:

```javascript
// Progress của từng bài học
{
  "lesson_progress_K6_A1": {
    "lessonId": "K6_A1",
    "viewed": ["theory", "slides", "video", "quiz"],
    "completed": ["theory", "slides"],
    "lastAccess": "2025-12-05T10:30:00.000Z",
    "timeSpent": 1200
  }
}
```

### API JavaScript:

```javascript
// Đánh dấu section đã hoàn thành
markAsCompleted('theory');

// Chuyển tab
switchTab('video');

// Lấy tiến độ
const progress = getLessonProgress();
console.log(progress.completed); // ["theory", "slides"]
```

## 🔧 Tích Hợp Vào Hệ Thống Hiện Tại

### 1. Thêm link trong `index.html`:

```html
<a href="/Lesson_Content/K6/A1_lesson_content.html" class="btn">
  💻 A1: Máy tính và ứng dụng (Đầy đủ)
</a>
```

### 2. Hoặc thay thế link hiện tại:

```html
<!-- Trước -->
<a href="/Web/K6_A1.html">💻A1</a>

<!-- Sau -->
<a href="/Lesson_Content/K6/A1_lesson_content.html">💻A1</a>
```

## 📝 Quy Trình Thêm Bài Học Mới

1. **Chuẩn bị tài liệu:**
   - PDF: Giáo trình lý thuyết
   - PPTX: Slide bài giảng
   - MP4: Video giảng dạy

2. **Chuyển đổi:**
   ```bash
   python convert_documents.py theory.pdf
   python convert_documents.py slides.pptx
   ```

3. **Tạo config:** Tạo file JSON với thông tin bài học

4. **Generate HTML:**
   ```bash
   python generate_lesson.py --config lesson_config.json
   ```

5. **Upload lên server:** Upload folder và file HTML

6. **Cập nhật navigation:** Thêm link trong `index.html`

## 🎯 Lợi Ích

### Cho Học Sinh:
- ✅ Trải nghiệm học tập nhất quán
- 📊 Theo dõi tiến độ học của mình
- 🎥 Học qua nhiều phương thức (đọc, xem, làm)
- 📱 Học mọi lúc mọi nơi (responsive)

### Cho Giáo Viên:
- 📝 Dễ dàng tổ chức nội dung
- 🔄 Cập nhật tài liệu đơn giản
- 📊 Xem được tiến độ học sinh (nếu tích hợp backend)
- 🎨 Giao diện chuyên nghiệp

### Cho Hệ Thống:
- 🗂️ Quản lý tập trung
- 🔗 Tích hợp Knowledge Graph dễ dàng
- 📈 Thu thập dữ liệu học tập
- 🚀 Dễ mở rộng

## 🤝 Support

Nếu gặp vấn đề:

1. Check console log (F12)
2. Kiểm tra đường dẫn file
3. Đảm bảo file tồn tại và có quyền truy cập
4. Kiểm tra localStorage có dữ liệu không

## 📄 License

MIT License - Sử dụng tự do cho mục đích giáo dục

---

**Tạo bởi:** Hệ thống hỗ trợ giáo viên THCS  
**Phiên bản:** 1.0.0  
**Ngày cập nhật:** 05/12/2025


