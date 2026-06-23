# TỔNG QUAN DỰ ÁN IELTS / PTE PRACTICE

## Cấu trúc Hệ Thống
Dự án bao gồm 3 kho lưu trữ (repository) chính, phục vụ các kỹ năng và module bài tập khác nhau:

### 1. `practicepteonline` (Full Tests)
- **Nội dung:** 204 bài thi Listening Full (Test 1 - Test 204) và 315 bài thi Reading Full (Test 1 - Test 315).
- **Kiến trúc:** Mỗi bài test được lưu ở một thư mục riêng biệt chứa tệp `index.html`, `Test_X.html`, file âm thanh `audio_X.mp3`, v.v.
- **Tích hợp Đăng nhập:** Tiêm mã đăng nhập và script xác thực trực tiếp vào toàn bộ các file `.html` bằng script Python (`inject_universal_login_bs4.py`).

### 2. `ReadingA1-C2` (1232 Bài Đọc Hiểu)
- **Nội dung:** 1232 bài đọc hiểu phân loại theo các cấp độ A1-C2.
- **Kiến trúc:** Ứng dụng Single Page Application (SPA). Toàn bộ 1232 bài đọc dùng chung một khuôn mẫu hiển thị là `frontend/template_reading.html` và nạp dữ liệu câu hỏi từ file JSON trên đường truyền (ví dụ `?file=data_1.json`). Màn hình chính nằm ở `frontend/index.html`.
- **Tích hợp Đăng nhập:** Mã đăng nhập được nhúng trực tiếp vào tệp `frontend/template_reading.html` và `frontend/index.html`. Do tính chất nạp động, mọi bài học đều tự động thừa hưởng màn hình đăng nhập này.

### 3. `pte-listening-audios` (102 Bài Nghe Cơ Bản)
- **Nội dung:** 102 bài nghe chia làm 3 trình độ: Basic, Intermediate, Advanced.
- **Kiến trúc:** Sử dụng cơ chế template build tĩnh. Khuôn mẫu chung được khai báo tại tệp `template.html` ở thư mục gốc. Script Python `rebuilder.py` sẽ biên dịch và đẩy cấu trúc mới nhất xuống tất cả 102 thư mục bài học (ví dụ: `Advanced/Lesson_12/index.html`).
- **Tích hợp Đăng nhập:** Giao diện đăng nhập được nhúng vào `template.html`, sau đó thông qua lệnh `python3 rebuilder.py` để ghi đè (build lại) hàng loạt vào 102 file HTML của các bài nghe.

## Hệ thống Đăng nhập Đồng nhất (Study Room)
- **Google Apps Script:** Tất cả dữ liệu đăng nhập được lưu và xác thực tại backend Apps Script (`apps_script_final.js` URL `https://script.google.com/macros/s/AKfycbx-KeSd_VIwmvrRRifyKl3CLMU3pc91_oURdunCnHBUYEn-UkHm3LwgCeTR5ltY1Afy/exec`).
- **Cơ chế hoạt động:** 
  1. Người học nhập ID tại lớp phủ đăng nhập (`main-layout` bị ẩn đi, hiện form login).
  2. Client gửi Ajax qua Apps Script để xác thực.
  3. Nếu khớp, Apps Script trả về thành công kèm Tên hiển thị. Client lưu thông tin vào `localStorage`, ẩn lớp phủ, và hiện giao diện bài tập lên.
- **Định dạng bảng giá:** 1,599,000 VND / Thời hạn: 1 năm.

## Các Công cụ (Scripts) Quản lý
- `inject_universal_login_bs4.py`: Script do Antigravity phát triển dùng thư viện BeautifulSoup4. Nó tự động truy xuất tất cả các files và template của 3 repository trên, an toàn xoá mã đăng nhập cũ hỏng, và đắp lớp giao diện đăng nhập mới nhất vào đầu thẻ `<body>`.
- `crawler/scrape_pte.py`: Tool thu thập và cào lại dữ liệu từ web khi bị mất file.
- `apps_script_final.js`: Tệp nguồn (lưu cục bộ) dùng để triển khai lên Google Apps Script, xử lý CORS, GET, POST requests.

## Tình trạng Hiện tại
Toàn bộ dự án đã được đồng bộ hóa thành công lên GitHub với cấu trúc không lỗi (bugs-free), màn hình đăng nhập hiển thị chính xác mọi thông tin, và đã giải quyết triệt để vấn đề "màn hình trắng" hay "lỗi 404".
