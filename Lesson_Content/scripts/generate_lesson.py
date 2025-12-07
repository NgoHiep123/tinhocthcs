#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo trang bài học từ template
Hỗ trợ chuyển đổi PDF, DOCX, PPTX sang HTML
"""

import os
import sys
import json
import argparse
from pathlib import Path
import re

# Thêm đường dẫn để import các module cần thiết
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class LessonGenerator:
    """Tạo trang bài học từ các nguồn tài liệu"""
    
    def __init__(self, template_dir='../templates', output_dir='../'):
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        
        # Load templates
        self.main_template = self._load_template('lesson_main.html')
        self.pdf_template = self._load_template('pdf_viewer.html')
        self.slides_template = self._load_template('slides_viewer.html')
        self.video_template = self._load_template('video_player.html')
    
    def _load_template(self, filename):
        """Load template file"""
        template_path = self.template_dir / filename
        if not template_path.exists():
            raise FileNotFoundError(f"Template không tồn tại: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def generate_lesson(self, lesson_config):
        """
        Tạo trang bài học từ config
        
        lesson_config = {
            'lesson_id': 'K6_A1',
            'lesson_code': 'A1',
            'lesson_title': 'Máy tính và ứng dụng',
            'lesson_icon': '💻',
            'lesson_description': 'Tìm hiểu về máy tính và các ứng dụng',
            'grade': 'Lớp 6',
            'theory': {
                'type': 'pdf',  # 'pdf', 'docx', 'html'
                'url': '/content/K6/A1/theory.pdf',
                'title': 'Giáo trình lý thuyết'
            },
            'slides': {
                'type': 'images',  # 'images', 'google', 'ppt'
                'slides': ['slide1.jpg', 'slide2.jpg', ...],
                'notes': ['Note 1', 'Note 2', ...],
                'url': '/content/K6/A1/slides.pptx'
            },
            'video': {
                'url': '/content/K6/A1/video.mp4',
                'title': 'Video bài giảng',
                'poster': '/content/K6/A1/poster.jpg',
                'chapters': [
                    {'time': 0, 'title': 'Giới thiệu'},
                    {'time': 120, 'title': 'Nội dung chính'},
                ],
                'notes': 'Xem video để hiểu rõ hơn'
            },
            'quiz_url': '/Web/K6_A1.html'
        }
        """
        
        # Tạo nội dung cho từng phần
        theory_content = self._generate_theory_content(lesson_config.get('theory', {}))
        slides_content = self._generate_slides_content(lesson_config.get('slides', {}))
        video_content = self._generate_video_content(lesson_config.get('video', {}))
        
        # Thay thế placeholders trong main template
        html_content = self.main_template
        
        replacements = {
            '{{LESSON_ID}}': lesson_config['lesson_id'],
            '{{LESSON_CODE}}': lesson_config['lesson_code'],
            '{{LESSON_TITLE}}': lesson_config['lesson_title'],
            '{{LESSON_ICON}}': lesson_config.get('lesson_icon', '📚'),
            '{{LESSON_DESCRIPTION}}': lesson_config.get('lesson_description', ''),
            '{{GRADE}}': lesson_config.get('grade', 'Lớp 6'),
            '{{THEORY_CONTENT}}': theory_content,
            '{{SLIDES_CONTENT}}': slides_content,
            '{{VIDEO_CONTENT}}': video_content,
            '{{QUIZ_URL}}': lesson_config.get('quiz_url', '#'),
        }
        
        for placeholder, value in replacements.items():
            html_content = html_content.replace(placeholder, str(value))
        
        return html_content
    
    def _generate_theory_content(self, theory_config):
        """Tạo nội dung lý thuyết"""
        if not theory_config:
            return '<p class="text-gray-500">Nội dung lý thuyết đang được cập nhật...</p>'
        
        theory_type = theory_config.get('type', 'pdf')
        
        if theory_type == 'pdf':
            content = self.pdf_template.replace('{{PDF_URL}}', theory_config.get('url', ''))
            content = content.replace('{{PDF_TITLE}}', theory_config.get('title', 'Tài liệu PDF'))
            return content
        
        elif theory_type == 'html':
            # Nội dung HTML trực tiếp
            return theory_config.get('content', '')
        
        elif theory_type == 'docx':
            # TODO: Chuyển đổi DOCX sang HTML
            return f'<p>📄 <a href="{theory_config.get("url")}" class="text-purple-600 font-bold">Tải tài liệu DOCX</a></p>'
        
        return '<p class="text-gray-500">Định dạng không được hỗ trợ</p>'
    
    def _generate_slides_content(self, slides_config):
        """Tạo nội dung slide"""
        if not slides_config:
            return '<p class="text-gray-500">Slide đang được cập nhật...</p>'
        
        slides_type = slides_config.get('type', 'images')
        
        content = self.slides_template
        
        # Thay thế placeholders
        replacements = {
            '{{SLIDES_TYPE}}': slides_type,
            '{{TOTAL_SLIDES}}': str(len(slides_config.get('slides', []))),
            '{{SLIDE_IMAGE_URL}}': slides_config.get('slides', [''])[0] if slides_config.get('slides') else '',
            '{{SLIDES_DATA}}': json.dumps(slides_config.get('slides', [])),
            '{{SLIDES_NOTES}}': json.dumps(slides_config.get('notes', [])),
            '{{SLIDES_URL}}': slides_config.get('url', '#'),
            '{{GOOGLE_SLIDES_URL}}': slides_config.get('google_url', ''),
            '{{SLIDES_EMBED_URL}}': slides_config.get('embed_url', ''),
            '{{CURRENT_SLIDE}}': '1'
        }
        
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, str(value))
        
        return content
    
    def _generate_video_content(self, video_config):
        """Tạo nội dung video"""
        if not video_config:
            return '<p class="text-gray-500">Video đang được cập nhật...</p>'
        
        content = self.video_template
        
        # Thay thế placeholders
        replacements = {
            '{{VIDEO_ID}}': video_config.get('id', 'video_' + str(hash(video_config.get('url', '')))),
            '{{VIDEO_URL}}': video_config.get('url', ''),
            '{{VIDEO_URL_WEBM}}': video_config.get('url_webm', ''),
            '{{VIDEO_TITLE}}': video_config.get('title', 'Video bài giảng'),
            '{{VIDEO_POSTER}}': video_config.get('poster', ''),
            '{{VIDEO_CHAPTERS}}': json.dumps(video_config.get('chapters', [])),
            '{{VIDEO_NOTES}}': video_config.get('notes', 'Xem video để hiểu rõ hơn về bài học'),
            '{{VIDEO_QUALITIES}}': json.dumps(video_config.get('qualities', {})),
            '{{YOUTUBE_EMBED_URL}}': video_config.get('youtube_url', '')
        }
        
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, str(value))
        
        return content
    
    def save_lesson(self, html_content, output_filename):
        """Lưu file HTML"""
        output_path = self.output_dir / output_filename
        
        # Tạo thư mục nếu chưa tồn tại
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Đã tạo file: {output_path}")
        return output_path


def create_sample_lesson():
    """Tạo bài học mẫu để demo"""
    generator = LessonGenerator()
    
    # Config mẫu cho bài K6_A1
    lesson_config = {
        'lesson_id': 'K6_A1_CONTENT',
        'lesson_code': 'A1',
        'lesson_title': 'Máy tính và ứng dụng',
        'lesson_icon': '💻',
        'lesson_description': 'Tìm hiểu về máy tính, các loại máy tính và ứng dụng của máy tính trong cuộc sống',
        'grade': 'Lớp 6',
        
        'theory': {
            'type': 'pdf',
            'url': '/Lesson_Content/K6/A1/theory.pdf',
            'title': 'Giáo trình: Máy tính và ứng dụng'
        },
        
        'slides': {
            'type': 'images',
            'slides': [
                '/Lesson_Content/K6/A1/slides/slide1.jpg',
                '/Lesson_Content/K6/A1/slides/slide2.jpg',
                '/Lesson_Content/K6/A1/slides/slide3.jpg',
                '/Lesson_Content/K6/A1/slides/slide4.jpg',
                '/Lesson_Content/K6/A1/slides/slide5.jpg',
            ],
            'notes': [
                'Giới thiệu về máy tính',
                'Các loại máy tính',
                'Ứng dụng của máy tính',
                'Lịch sử phát triển',
                'Tổng kết'
            ],
            'url': '/Lesson_Content/K6/A1/slides.pptx'
        },
        
        'video': {
            'id': 'K6_A1_video',
            'url': '/Lesson_Content/K6/A1/video.mp4',
            'title': 'Video bài giảng: Máy tính và ứng dụng',
            'poster': '/Lesson_Content/K6/A1/video_poster.jpg',
            'chapters': [
                {'time': 0, 'title': 'Giới thiệu'},
                {'time': 120, 'title': 'Các loại máy tính'},
                {'time': 300, 'title': 'Ứng dụng của máy tính'},
                {'time': 500, 'title': 'Tổng kết'}
            ],
            'notes': 'Xem video để hiểu rõ hơn về máy tính và các ứng dụng của nó trong cuộc sống hàng ngày',
            'qualities': {
                '720p': '/Lesson_Content/K6/A1/video_720p.mp4',
                '480p': '/Lesson_Content/K6/A1/video_480p.mp4',
                '360p': '/Lesson_Content/K6/A1/video_360p.mp4'
            }
        },
        
        'quiz_url': '/Web/K6_A1.html'
    }
    
    # Tạo HTML
    html_content = generator.generate_lesson(lesson_config)
    
    # Lưu file
    generator.save_lesson(html_content, 'K6/A1_lesson_content.html')
    
    print("\n✅ Đã tạo bài học mẫu thành công!")
    print("📁 File: Lesson_Content/K6/A1_lesson_content.html")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Tạo trang bài học từ config')
    parser.add_argument('--config', '-c', help='File config JSON')
    parser.add_argument('--sample', '-s', action='store_true', help='Tạo bài học mẫu')
    
    args = parser.parse_args()
    
    if args.sample:
        create_sample_lesson()
    elif args.config:
        # Load config từ file JSON
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        generator = LessonGenerator()
        html_content = generator.generate_lesson(config)
        
        output_file = f"{config['grade']}/{config['lesson_code']}_lesson_content.html"
        generator.save_lesson(html_content, output_file)
    else:
        parser.print_help()
        print("\nVí dụ:")
        print("  python generate_lesson.py --sample")
        print("  python generate_lesson.py --config lesson_config.json")


if __name__ == '__main__':
    main()


