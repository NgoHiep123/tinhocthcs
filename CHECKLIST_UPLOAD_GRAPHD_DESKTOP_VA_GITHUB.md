# 📋 CHECKLIST: NỘI DUNG UPLOAD GRAPHDB DESKTOP VÀ GITHUB

> Hướng dẫn chi tiết về nội dung nào cần upload vào GraphDB Desktop và nội dung nào upload lên GitHub

---

## ⚡ TÓM TẮT NHANH

### GraphDB Desktop → Upload file `.ttl` (Turtle/RDF)
- ✅ **Khối 6**: 7 file trong `KG_Design/grade6/out/*.ttl`
- ✅ **Khối 7**: `kg_schema_grade7.ttl` + `kg_grade7.ttl` (bao gồm cả giáo viên & phân công)
- ⚠️ **Khối 8**: Chưa có (cần tạo sau)
- ⚠️ **Khối 9**: Chưa có (cần tạo sau)
- 📝 **Cách**: Import thủ công trong GraphDB Desktop hoặc dùng script `import_to_graphdb.py`

### GitHub → Upload source code, dữ liệu, tài liệu
- ✅ **Source code**: Python scripts, PHP, HTML
- ✅ **Dữ liệu**: CSV, JSON, Excel nhỏ (< 1MB)
- ✅ **Tài liệu**: Markdown, README
- ✅ **Web**: HTML files, images
- ❌ **KHÔNG upload**: `.ttl` files (có thể tái tạo), file lớn, credentials

**Xem chi tiết bên dưới ↓**

---

## 🎯 TỔNG QUAN

### GraphDB Desktop
- **Mục đích**: Lưu trữ và truy vấn Knowledge Graph (dữ liệu RDF/Turtle)
- **Nội dung**: Các file `.ttl` (Turtle format) đã được build/generate từ dữ liệu CSV
- **Cách upload**: Import trực tiếp trong GraphDB Desktop hoặc dùng script `import_to_graphdb.py`

### GitHub
- **Mục đích**: Lưu trữ source code, tài liệu, dữ liệu nguồn (CSV, JSON)
- **Nội dung**: Tất cả file source code, scripts, HTML, CSV, JSON, documentation
- **Cách upload**: Dùng Git commands hoặc script `upload_to_github.sh`

---

## 📤 NỘI DUNG UPLOAD VÀO GRAPHDB DESKTOP

### ✅ File TTL (Turtle/RDF) - BẮT BUỘC

#### Khối 6:
```
KG_Design/grade6/out/
├── skills.ttl                    ✅ Upload
├── resources.ttl                ✅ Upload
├── resource_skill.ttl            ✅ Upload
├── prerequisites.ttl             ✅ Upload
├── question_skill.ttl            ✅ Upload
├── students.ttl                  ✅ Upload
└── mastery.ttl                   ✅ Upload
```

#### Khối 7:
```
KG_Design/
├── kg_schema_grade7.ttl          ✅ Upload (Schema định nghĩa - BẮT BUỘC)
├── kg_grade7.ttl                 ✅ Upload (KG đã build - BẮT BUỘC)
│   └── ⚠️ File này BAO GỒM:
│       - Dữ liệu học sinh (students)
│       - Dữ liệu giáo viên và phân công lớp (teachers & assignments)
│       - Dữ liệu kỹ năng, tài nguyên, quan hệ tiên quyết
├── kg_grade7_with_knn.ttl       ✅ Upload (nếu có - KG + KNN results)
└── kg_grade7_with_ppr.ttl       ✅ Upload (nếu có - KG + PPR results)
```

**Lưu ý quan trọng:**
- **Schema** (`kg_schema_grade7.ttl`) phải import **TRƯỚC** các file dữ liệu
- **Thứ tự import** trong GraphDB Desktop:
  1. Schema trước
  2. Dữ liệu sau (theo thứ tự: skills → resources → prerequisites → students → teachers → mastery)
- **Giáo viên & phân công**: Được bao gồm trong `kg_grade7.ttl` (KHÔNG có file TTL riêng)
  - Dữ liệu nguồn: `teachers_assign.csv` (ở root)
  - Script build: `KG_Design/build_kg_grade7.py` (hàm `add_teachers_to_kg()`)

#### Khối 8 & 9:
```
⚠️ CHƯA CÓ - Cần tạo sau:
├── KG_Design/grade8/             ⚠️ Chưa có
│   └── export_ttl.py             ⚠️ Cần tạo tương tự grade6
└── KG_Design/grade9/             ⚠️ Chưa có
    └── export_ttl.py             ⚠️ Cần tạo tương tự grade6
```

**Lưu ý:**
- Hiện tại chỉ có **Khối 6** và **Khối 7**
- **Khối 8** và **Khối 9** chưa có script build TTL
- Cần tạo thư mục và script tương tự `grade6/export_ttl.py` cho khối 8 và 9

**Hướng dẫn tạo TTL cho Khối 8 & 9 (tương lai):**
1. Tạo thư mục: `KG_Design/grade8/` và `KG_Design/grade9/`
2. Copy script từ `grade6/export_ttl.py` và chỉnh sửa:
   - Đổi đường dẫn CSV từ `Bai_tap_Tin_6/` sang `Bai_tap_Tin_8/` hoặc `Bai_tap_Tin_9/`
   - Đổi namespace/prefix nếu cần (ví dụ: `grade8`, `grade9`)
3. Chuẩn bị dữ liệu CSV tương tự grade6:
   - `skills.csv`, `question_skill.csv`, `prerequisites.csv`
   - `resources.csv`, `resource_skill.csv`
   - `student_mastery.csv`, `students.ttl`
4. Chạy script: `python KG_Design/grade8/export_ttl.py`
5. Kết quả: File TTL trong `KG_Design/grade8/out/` và `KG_Design/grade9/out/`

### ✅ File Cypher (nếu dùng Neo4j thay vì GraphDB)
```
KG_Design/
└── cypher_import_skeleton.cypher  ⚠️ Chỉ dùng nếu migrate sang Neo4j
```

### 📝 CÁCH UPLOAD VÀO GRAPHDB DESKTOP

#### Phương pháp 1: Import thủ công (Khuyến nghị)
1. Mở GraphDB Desktop
2. Tạo repository mới:
   - Click "New repository"
   - Tên: `tin_hoc_thcs` (hoặc tên khác)
   - Ruleset: **OWL-Horst** (khuyến nghị) hoặc **RDFS**
   - Click "Create"
3. Import file TTL:
   - Chọn repository vừa tạo
   - Vào tab **"Import"**
   - Click **"Import RDF"** → Chọn file `.ttl`
   - Lặp lại cho tất cả file TTL cần import
   - **Lưu ý**: Import theo thứ tự:
     1. Schema trước (`kg_schema_grade7.ttl` hoặc `skills.ttl`)
     2. Dữ liệu sau (các file còn lại)

#### Phương pháp 2: Dùng script Python (Tự động)
```bash
cd KG_Design
python import_to_graphdb.py
```
- Script sẽ tự động upload file `.ttl` vào GraphDB qua REST API
- Cần cấu hình file `.env` trước:
  ```
  GRAPHDB_SERVER=http://localhost:7200
  GRAPHDB_REPOSITORY=tin_hoc_thcs
  GRAPHDB_USERNAME=admin
  GRAPHDB_PASSWORD=root
  ```

### ✅ KIỂM TRA SAU KHI UPLOAD

1. Vào tab **"SPARQL"** trong GraphDB Desktop
2. Chạy query đếm triples:
   ```sparql
   SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }
   ```
3. Kiểm tra dữ liệu:
   ```sparql
   PREFIX edu: <http://education.vn/ontology#>
   SELECT ?student ?name WHERE {
     ?student edu:fullName ?name .
   } LIMIT 10
   ```

---

## 📤 NỘI DUNG UPLOAD LÊN GITHUB

### ✅ Source Code & Scripts

#### Python Scripts:
```
KG_Design/
├── build_kg_grade7.py            ✅ Upload
├── query_kg.py                   ✅ Upload
├── import_to_graphdb.py          ✅ Upload
├── add_new_student.py            ✅ Upload
├── add_new_teacher.py            ✅ Upload
├── add_new_class.py              ✅ Upload
├── update_kg.py                  ✅ Upload
├── test_graphdb_connection.py   ✅ Upload
├── demo_teacher_queries.py       ✅ Upload
└── grade6/
    ├── build_grade6_inputs.py    ✅ Upload
    ├── export_ttl.py             ✅ Upload
    ├── build_student_mastery.py   ✅ Upload
    └── generate_prereq_baseline.py ✅ Upload

ML_Algorithms/
├── knn_student_analysis.py       ✅ Upload
└── ppr_recommendation.py         ✅ Upload

scripts/
├── convert_excel_to_students_json.py ✅ Upload
├── generate_all_k6_html.py       ✅ Upload
├── generate_k7_full_html.py      ✅ Upload
├── update_endpoint_to_php_api.py ✅ Upload
└── ... (tất cả file .py)         ✅ Upload
```

#### Backend API:
```
backend_api/
├── api/
│   ├── config.php                ✅ Upload
│   ├── get_results.php           ✅ Upload
│   └── save_result.php           ✅ Upload
├── dashboard/
│   └── index.php                 ✅ Upload
├── create_database.sql           ✅ Upload
├── setup_database_manual.sql     ✅ Upload
└── test_api.php                  ✅ Upload
```

### ✅ Dữ liệu nguồn (CSV, JSON)

#### CSV Files:
```
Bai_tap_Tin_6/
├── K6_question_A_full.csv        ✅ Upload
├── K6_question_B_full.csv        ✅ Upload
├── K6_question_C_full.csv        ✅ Upload
├── K6_question_D_full.csv        ✅ Upload
├── K6_question_E_full.csv        ✅ Upload
└── K6_question_F_full.csv         ✅ Upload

Bai_tap_Tin_7/
├── K7_question_A_full.csv         ✅ Upload
├── K7_question_B_full.csv         ✅ Upload
├── K7_question_D_full.csv         ✅ Upload
├── K7_question_E_full.csv         ✅ Upload
└── K7_question_F_full.csv         ✅ Upload

Bai_tap_Tin_8/
└── ... (tất cả file CSV)          ✅ Upload

Bai_tap_Tin_9/
└── ... (tất cả file CSV)          ✅ Upload

KG_Design/grade6/
├── skills.csv                     ✅ Upload
├── question_skill.csv             ✅ Upload
├── prerequisites.csv               ✅ Upload
├── resources.csv                  ✅ Upload
├── resource_skill.csv             ✅ Upload
├── student_assessment.csv         ✅ Upload
├── questions_in_assessment.csv   ✅ Upload
└── student_mastery.csv            ✅ Upload

KG_Design/data_templates/
└── ... (tất cả file CSV templates) ✅ Upload

Root/
├── teachers_assign.csv            ✅ Upload
└── students.json                  ✅ Upload
└── students_grade_data.json       ✅ Upload
```

### ✅ Web Interface

#### HTML Files:
```
Root/
├── index.html                     ✅ Upload
├── login.html                     ✅ Upload
├── login_offline.html             ✅ Upload
├── quiz_template_with_images.html ✅ Upload
├── K6_*.html (tất cả)             ✅ Upload
├── K7_*.html (tất cả)             ✅ Upload
├── K8_*.html (tất cả)             ✅ Upload
└── K9_*.html (tất cả)             ✅ Upload

Web_Teacher/
└── dashboard.html                 ✅ Upload

KG_Design/
└── teachers_dashboard.html        ✅ Upload
```

### ✅ Documentation

#### Markdown Files:
```
Root/
├── README.md                      ✅ Upload
├── README_THIET_KE.md             ✅ Upload
├── _README_FIRST.txt             ✅ Upload
├── DE_CUONG_DE_AN_2.txt          ✅ Upload
├── TOM_TAT_DE_XUAT.md            ✅ Upload
├── TOM_TAT_UPLOAD_GITHUB.md      ✅ Upload
├── TOM_TAT_SETUP_NHANH.md        ✅ Upload
├── TOM_TAT_BAO_CAO_TIEN_DO.md    ✅ Upload
├── TOMTAT_HOAN_THIEN.md          ✅ Upload
├── TONG_KET_DA_CHUAN_BI.md       ✅ Upload
├── HUONG_DAN_UPLOAD_GITHUB_BANG_GIT_BASH.md ✅ Upload
├── CHECKLIST_TRUOC_KHI_UPLOAD.md ✅ Upload
├── CHECKLIST_DEMO.md             ✅ Upload
├── CHECKLIST_UPLOAD_GRAPHD_DESKTOP_VA_GITHUB.md ✅ Upload (file này)
├── HUONG_DAN_SETUP_*.md          ✅ Upload (tất cả)
├── HUONG_DAN_TRIEN_KHAI_*.md     ✅ Upload (tất cả)
├── HUONG_DAN_TICH_HOP_*.md       ✅ Upload (tất cả)
├── HUONG_DAN_XEM_*.md            ✅ Upload (tất cả)
├── BAO_CAO_*.md                   ✅ Upload (tất cả)
├── KE_HOACH_THUC_HIEN_DU_AN.md   ✅ Upload
├── QUYET_DINH_NGAY_BAY_GIO.md    ✅ Upload
├── CHON_GIAI_PHAP_NÀO.md         ✅ Upload
├── GIAI_PHAP_FIREBASE.md         ✅ Upload
├── SO_SANH_GIAI_PHAP_LUU_KET_QUA.md ✅ Upload
├── KIEM_TRA_KNOWLEDGE_GRAPH.png.md ✅ Upload (file kiểm tra schema)
└── ... (tất cả file .md)         ✅ Upload

KG_Design/
├── README.md                      ✅ Upload
├── SCHEMA_KNOWLEDGE_GRAPH.md     ✅ Upload
├── STEP_BY_STEP.md               ✅ Upload
├── HUONG_DAN_*.md                 ✅ Upload (tất cả)
└── grade6/
    ├── README.md                  ✅ Upload
    ├── EXPLAIN_CSV_FIELDS.md     ✅ Upload
    ├── sparql_queries.md          ✅ Upload
    └── sparql_visual_queries.md  ✅ Upload
```

### ✅ Configuration Files

```
Root/
├── requirements.txt               ✅ Upload
├── .gitignore                     ✅ Upload
├── CNAME                          ✅ Upload (GitHub Pages custom domain)
├── run_pipeline.bat               ✅ Upload
├── run_pipeline.sh                ✅ Upload
└── upload_to_github.sh            ✅ Upload

backend_api/
├── setup_database.bat             ✅ Upload
└── setup_database.sh              ✅ Upload
```

### ✅ Images & Assets

```
Root/
├── Knowledge_graph.png            ✅ Upload (Hình schema Knowledge Graph)
└── images/                        ✅ Upload (nếu có file ảnh)
```

### ✅ Teacher Tools

```
Teacher_Tools/
├── them_cau_hoi.html              ✅ Upload
├── HUONG_DAN_THEM_CAU_HOI.md     ✅ Upload
└── QUICK_REFERENCE.md             ✅ Upload
```

### ✅ Configuration Files (Bổ sung)

```
Root/
├── CNAME                          ✅ Upload (cho GitHub Pages custom domain)
├── run_pipeline.bat               ✅ Upload
├── run_pipeline.sh                ✅ Upload
└── upload_to_github.sh            ✅ Upload
```

### ✅ Data Files (Excel nhỏ)

```
Root/
├── teachers.xlsx                  ✅ Upload (0.01 MB - nhỏ, OK)
└── result_thcs.xlsx               ✅ Upload (0.01 MB - nhỏ, OK)
```

**Lưu ý**: File Excel nhỏ (< 1MB) có thể upload. File Excel lớn (> 5MB) nên loại trừ.

---

## ❌ KHÔNG UPLOAD LÊN GITHUB

### File đã được loại trừ (qua .gitignore):

```
❌ __pycache__/                    # Python cache
❌ *.pyc                           # Python bytecode
❌ .env                            # Environment variables (bảo mật)
❌ credentials.json                # API credentials (bảo mật)
❌ *.pdf                           # Sách giáo khoa (bản quyền)
❌ *.doc, *.docx                   # Giáo án (bản quyền)
❌ *.xlsx (file > 5MB)             # Dữ liệu raw lớn (file nhỏ < 1MB OK)
❌ node_modules/                   # NPM packages
❌ .DS_Store                        # macOS system file
❌ Thumbs.db                       # Windows thumbnail cache
❌ *.log                           # Log files
❌ *.tmp, *.bak                    # Temporary files
❌ *.db, *.sqlite                  # Database files
```

### File không nên upload (mặc dù không bị .gitignore):

```
⚠️ File TTL đã generate (tùy chọn):
   - KG_Design/kg_grade7.ttl
   - KG_Design/grade6/out/*.ttl
   
   Lý do: Có thể tái tạo từ CSV và Python scripts
   Khuyến nghị: KHÔNG upload để repository nhẹ hơn
```

### File TTL đã generate (Tùy chọn - có thể upload hoặc không):

```
⚠️ KG_Design/kg_grade7.ttl         # File đã generate, có thể tái tạo từ CSV
⚠️ KG_Design/grade6/out/*.ttl      # File đã generate, có thể tái tạo từ CSV
```

**Lưu ý**: 
- File `.ttl` là **output** được generate từ CSV và Python scripts
- Có thể **không upload** lên GitHub vì có thể tái tạo bằng cách chạy scripts
- Nếu upload lên GitHub: Giúp người khác có thể test ngay mà không cần build lại
- Nếu không upload: Repository nhẹ hơn, nhưng người khác cần chạy scripts để generate

**Khuyến nghị**: **KHÔNG upload** file `.ttl` lên GitHub, chỉ upload vào GraphDB Desktop

---

## 📝 CHECKLIST TRƯỚC KHI UPLOAD

### Trước khi upload lên GraphDB Desktop:

- [ ] Đã chạy script generate file TTL:
  ```bash
  # Khối 6
  cd KG_Design/grade6
  python export_ttl.py
  # Kết quả: 7 file .ttl trong thư mục out/
  
  # Khối 7 (bao gồm cả giáo viên & phân công)
  cd ../..
  cd KG_Design
  python build_kg_grade7.py
  # Kết quả: kg_grade7.ttl (bao gồm students, teachers, assignments) và kg_schema_grade7.ttl
  ```
- [ ] File TTL đã được tạo:
  - [ ] Khối 6: `KG_Design/grade6/out/*.ttl` (7 files)
  - [ ] Khối 7: `KG_Design/kg_grade7.ttl` (bao gồm giáo viên) và `kg_schema_grade7.ttl`
  - [ ] ⚠️ Khối 8: Chưa có - cần tạo script tương tự grade6
  - [ ] ⚠️ Khối 9: Chưa có - cần tạo script tương tự grade6
- [ ] GraphDB Desktop đã được khởi động (kiểm tra icon trong system tray)
- [ ] Đã tạo repository trong GraphDB Desktop:
  - [ ] Tên repository: `tin_hoc_thcs` (hoặc tên khác)
  - [ ] Ruleset: **OWL-Horst** (khuyến nghị) hoặc **RDFS**
- [ ] Đã import theo đúng thứ tự:
  - [ ] **Bước 1**: Import schema (`kg_schema_grade7.ttl` hoặc `skills.ttl` trước)
  - [ ] **Bước 2**: Import dữ liệu (các file còn lại)
- [ ] Đã test query SPARQL để kiểm tra dữ liệu:
  ```sparql
  # Đếm tổng số triples
  SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }
  
  # Kiểm tra học sinh
  PREFIX edu: <http://education.vn/ontology#>
  SELECT ?student ?name WHERE {
    ?student edu:fullName ?name .
  } LIMIT 10
  ```

### Trước khi upload lên GitHub:

- [ ] Đã xóa file không cần thiết:
  - [ ] `__pycache__/` directories (đã xóa ✅)
  - [ ] `*.pyc` files
  - [ ] File PDF, DOC, DOCX (nếu có)
  - [ ] File `.env` (nếu có)
  - [ ] File `credentials.json` (nếu có)
- [ ] Đã kiểm tra `.gitignore` đã đúng:
  - [ ] File `.gitignore` đã tồn tại
  - [ ] Đã bao gồm: `__pycache__/`, `*.pyc`, `.env`, `*.pdf`, `*.doc`, `*.docx`
- [ ] Đã kiểm tra file lớn:
  - [ ] File Excel < 1MB: OK (như `teachers.xlsx`, `result_thcs.xlsx`)
  - [ ] File Excel > 5MB: Nên loại trừ
- [ ] Đã test hệ thống hoạt động:
  - [ ] Web interface mở được (`index.html`)
  - [ ] Scripts Python chạy được (test 1-2 scripts)
  - [ ] API hoạt động (nếu có backend)
- [ ] Đã cập nhật `README.md` với thông tin đầy đủ:
  - [ ] Mô tả dự án
  - [ ] Hướng dẫn cài đặt
  - [ ] Link demo (nếu có)
- [ ] Đã commit và push lên GitHub:
  ```bash
  git init
  git add .
  git commit -m "Initial commit - Hệ thống hoàn chỉnh"
  git remote add origin https://github.com/USERNAME/REPO.git
  git push -u origin main
  ```
- [ ] Đã kiểm tra trên GitHub web interface:
  - [ ] README.md hiển thị đúng
  - [ ] Có đầy đủ thư mục
  - [ ] KHÔNG có file PDF, DOC, DOCX
  - [ ] KHÔNG có `__pycache__/`

---

## 🔄 QUY TRÌNH HOÀN CHỈNH

### Bước 1: Chuẩn bị dữ liệu
```bash
# 1. Generate file TTL từ CSV
cd KG_Design/grade6
python export_ttl.py

cd ..
python build_kg_grade7.py
```

### Bước 2: Upload vào GraphDB Desktop
1. Mở GraphDB Desktop
2. Tạo repository `tin_hoc_thcs`
3. Import các file TTL từ `KG_Design/grade6/out/` và `KG_Design/`
4. Test query SPARQL

### Bước 3: Chuẩn bị upload GitHub
```bash
# Xóa file không cần thiết
Remove-Item -Recurse -Force KG_Design\__pycache__

# Kiểm tra .gitignore
cat .gitignore

# Kiểm tra file sẽ upload
git status
```

### Bước 4: Upload lên GitHub
```bash
git init
git add .
git commit -m "Initial commit - Hệ thống hoàn chỉnh"
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

---

## 📊 TÓM TẮT

| Loại nội dung | GraphDB Desktop | GitHub |
|--------------|----------------|--------|
| **File TTL (.ttl)** | ✅ Bắt buộc | ⚠️ Tùy chọn (không khuyến nghị) |
| **File CSV** | ❌ Không | ✅ Bắt buộc |
| **Python Scripts** | ❌ Không | ✅ Bắt buộc |
| **HTML Files** | ❌ Không | ✅ Bắt buộc |
| **JSON Files** | ❌ Không | ✅ Bắt buộc |
| **Documentation** | ❌ Không | ✅ Bắt buộc |
| **Configuration** | ❌ Không | ✅ Bắt buộc |
| **Images** | ❌ Không | ✅ Bắt buộc |
| **Teacher Tools** | ❌ Không | ✅ Bắt buộc |
| **Excel Files (< 1MB)** | ❌ Không | ✅ Bắt buộc |
| **Excel Files (> 5MB)** | ❌ Không | ❌ Không upload |
| **CNAME (GitHub Pages)** | ❌ Không | ✅ Bắt buộc (nếu dùng custom domain) |
| **Teachers TTL** | ✅ Trong kg_grade7.ttl | ❌ Không (đã tích hợp) |
| **Khối 8 TTL** | ⚠️ Chưa có | ⚠️ Chưa có |
| **Khối 9 TTL** | ⚠️ Chưa có | ⚠️ Chưa có |

---

## ✅ HOÀN THÀNH!

Sau khi hoàn thành checklist trên, bạn sẽ có:
- ✅ Knowledge Graph đã được import vào GraphDB Desktop, sẵn sàng truy vấn
- ✅ Source code và tài liệu đã được upload lên GitHub, sẵn sàng chia sẻ

**Chúc bạn thành công! 🎉**

