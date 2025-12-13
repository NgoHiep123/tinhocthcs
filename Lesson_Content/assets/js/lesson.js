/**
 * Lesson Content Management System
 * Handles lesson navigation, progress tracking, and content display
 */

// Global state
const LessonManager = {
  currentLesson: null,
  student: null,
  progress: {},
  
  init() {
    this.loadStudent();
    this.loadProgress();
    this.setupEventListeners();
    console.log('📚 Lesson Manager initialized');
  },
  
  // Load student info from localStorage
  loadStudent() {
    try {
      this.student = JSON.parse(localStorage.getItem('student') || 'null');
      console.log('👤 Student loaded:', this.student);
    } catch (e) {
      console.error('Error loading student:', e);
      this.student = null;
    }
  },
  
  // Load progress from localStorage
  loadProgress() {
    try {
      const progressData = localStorage.getItem('lessons_progress');
      this.progress = progressData ? JSON.parse(progressData) : {};
      console.log('📊 Progress loaded:', this.progress);
    } catch (e) {
      console.error('Error loading progress:', e);
      this.progress = {};
    }
  },
  
  // Save progress to localStorage
  saveProgress() {
    try {
      localStorage.setItem('lessons_progress', JSON.stringify(this.progress));
      console.log('💾 Progress saved');
    } catch (e) {
      console.error('Error saving progress:', e);
    }
  },
  
  // Get progress for a specific lesson
  getLessonProgress(lessonId) {
    if (!this.progress[lessonId]) {
      this.progress[lessonId] = {
        lessonId: lessonId,
        viewed: [],
        completed: [],
        lastAccess: null,
        timeSpent: 0
      };
    }
    return this.progress[lessonId];
  },
  
  // Mark section as viewed
  markSectionViewed(lessonId, section) {
    const progress = this.getLessonProgress(lessonId);
    if (!progress.viewed.includes(section)) {
      progress.viewed.push(section);
      progress.lastAccess = new Date().toISOString();
      this.saveProgress();
      console.log(`✓ Section "${section}" marked as viewed`);
    }
  },
  
  // Mark section as completed
  markSectionCompleted(lessonId, section) {
    const progress = this.getLessonProgress(lessonId);
    if (!progress.completed.includes(section)) {
      progress.completed.push(section);
      progress.lastAccess = new Date().toISOString();
      this.saveProgress();
      console.log(`✅ Section "${section}" marked as completed`);
      
      // Show notification
      this.showNotification(`✅ Đã hoàn thành: ${this.getSectionName(section)}`, 'success');
      
      // Check if entire lesson is completed
      if (progress.completed.length >= 4) {
        this.markLessonCompleted(lessonId);
      }
    }
  },
  
  // Mark entire lesson as completed
  markLessonCompleted(lessonId) {
    const progress = this.getLessonProgress(lessonId);
    progress.fullyCompleted = true;
    progress.completedAt = new Date().toISOString();
    this.saveProgress();
    
    console.log('🎉 Lesson completed!');
    this.showNotification('🎉 Chúc mừng! Bạn đã hoàn thành toàn bộ bài học!', 'success');
    
    // Trigger confetti
    if (typeof confetti === 'function') {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });
    }
  },
  
  // Get section display name
  getSectionName(section) {
    const names = {
      'theory': 'Lý thuyết',
      'slides': 'Slide bài giảng',
      'video': 'Video',
      'quiz': 'Kiểm tra'
    };
    return names[section] || section;
  },
  
  // Show notification
  showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} fixed top-20 right-4 z-50 px-6 py-4 rounded-xl shadow-2xl transform translate-x-0 transition-all duration-300`;
    notification.style.cssText = `
      background: ${type === 'success' ? 'linear-gradient(135deg, #10b981, #059669)' : 
                    type === 'error' ? 'linear-gradient(135deg, #ef4444, #dc2626)' :
                    'linear-gradient(135deg, #3b82f6, #2563eb)'};
      color: white;
      font-weight: bold;
      max-width: 400px;
      animation: slideInRight 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
      notification.style.transform = 'translateX(500px)';
      notification.style.opacity = '0';
      setTimeout(() => {
        notification.remove();
      }, 300);
    }, 3000);
  },
  
  // Setup event listeners
  setupEventListeners() {
    // Track time spent on page
    let startTime = Date.now();
    
    window.addEventListener('beforeunload', () => {
      const timeSpent = Math.floor((Date.now() - startTime) / 1000);
      if (this.currentLesson) {
        const progress = this.getLessonProgress(this.currentLesson);
        progress.timeSpent = (progress.timeSpent || 0) + timeSpent;
        this.saveProgress();
      }
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      // Ctrl/Cmd + H: Go home
      if ((e.ctrlKey || e.metaKey) && e.key === 'h') {
        e.preventDefault();
        window.location.href = '/index.html';
      }
    });
  },
  
  // Get completion percentage
  getCompletionPercentage(lessonId) {
    const progress = this.getLessonProgress(lessonId);
    const total = 4; // theory, slides, video, quiz
    const completed = progress.completed.length;
    return Math.round((completed / total) * 100);
  },
  
  // Get all completed lessons
  getCompletedLessons() {
    return Object.keys(this.progress).filter(lessonId => {
      return this.progress[lessonId].fullyCompleted === true;
    });
  },
  
  // Get total time spent on all lessons
  getTotalTimeSpent() {
    return Object.values(this.progress).reduce((total, lesson) => {
      return total + (lesson.timeSpent || 0);
    }, 0);
  },
  
  // Export progress data
  exportProgress() {
    const data = {
      student: this.student,
      progress: this.progress,
      exportedAt: new Date().toISOString(),
      totalLessons: Object.keys(this.progress).length,
      completedLessons: this.getCompletedLessons().length,
      totalTimeSpent: this.getTotalTimeSpent()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `progress_${this.student?.name || 'user'}_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    this.showNotification('📥 Đã tải xuống dữ liệu tiến độ', 'success');
  },
  
  // Import progress data
  importProgress(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result);
        if (data.progress) {
          this.progress = data.progress;
          this.saveProgress();
          this.showNotification('📤 Đã nhập dữ liệu tiến độ thành công', 'success');
          location.reload();
        }
      } catch (error) {
        console.error('Import error:', error);
        this.showNotification('❌ Lỗi khi nhập dữ liệu', 'error');
      }
    };
    reader.readAsText(file);
  },
  
  // Reset progress for a lesson
  resetLessonProgress(lessonId) {
    if (confirm(`Bạn có chắc muốn xóa tiến độ của bài học này?`)) {
      delete this.progress[lessonId];
      this.saveProgress();
      this.showNotification('🔄 Đã đặt lại tiến độ', 'info');
      location.reload();
    }
  },
  
  // Reset all progress
  resetAllProgress() {
    if (confirm('⚠️ Bạn có chắc muốn xóa TẤT CẢ tiến độ học tập? Hành động này không thể hoàn tác!')) {
      this.progress = {};
      this.saveProgress();
      this.showNotification('🔄 Đã đặt lại tất cả tiến độ', 'info');
      location.reload();
    }
  }
};

// Utility functions
const Utils = {
  // Format time from seconds to readable format
  formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    }
    if (minutes > 0) {
      return `${minutes}m ${secs}s`;
    }
    return `${secs}s`;
  },
  
  // Format date
  formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  },
  
  // Debounce function
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },
  
  // Throttle function
  throttle(func, limit) {
    let inThrottle;
    return function(...args) {
      if (!inThrottle) {
        func.apply(this, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  },
  
  // Check if user is on mobile
  isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  },
  
  // Copy text to clipboard
  copyToClipboard(text) {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(() => {
        LessonManager.showNotification('📋 Đã sao chép vào clipboard', 'success');
      });
    } else {
      // Fallback for older browsers
      const textarea = document.createElement('textarea');
      textarea.value = text;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      LessonManager.showNotification('📋 Đã sao chép vào clipboard', 'success');
    }
  }
};

// Initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    LessonManager.init();
  });
} else {
  LessonManager.init();
}

// Export to global scope
window.LessonManager = LessonManager;
window.Utils = Utils;

console.log('✅ Lesson.js loaded successfully');


