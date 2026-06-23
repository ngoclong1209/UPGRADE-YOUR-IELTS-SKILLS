# Nhật ký Phát triển Hệ thống PTE Listening Audios

Tài liệu này ghi lại toàn bộ quá trình xây dựng, thiết kế và khắc phục sự cố cho hệ thống luyện nghe PTE (PTE Listening Audios) tích hợp Google Sheets.

## 1. Khởi tạo & Xử lý Dữ liệu ban đầu
- **Xử lý file Excel kế hoạch**: Đọc dữ liệu từ file kế hoạch học tập (`UPGRADE YOUR ILETS LISTENING.xlsx`), trích xuất thông tin các phần nghe (Basic, Intermediate, Advanced) kéo dài đến năm 2026.
- **Tạo cấu trúc thư mục tự động**: Dùng Python script để tự động tạo 102 thư mục tương ứng với 102 bài học (từ `Basic/Lesson_1` đến các phần Advanced).
- **Trích xuất Audio**: Xử lý đường dẫn file audio cục bộ, copy các file âm thanh vào thư mục tương ứng cho từng bài học.
- **Tăng âm lượng Audio**: Sử dụng Python (thư viện `pydub`) để tăng âm lượng gốc của toàn bộ file audio lên 30% (tương tự chức năng Amplify trong Audacity) nhằm giúp học viên nghe rõ hơn.

## 2. Xây dựng Giao diện Website (HTML/JS)
- **Thiết kế trang làm bài**: Sử dụng Bootstrap và CSS custom để tạo giao diện làm bài nghe (có audio player, các câu trắc nghiệm nhiều lựa chọn/điền từ).
- **Cơ chế Login (Đăng nhập)**: Xây dựng Modal yêu cầu nhập `Nickname` để làm bài. 
- **Chống gian lận (Device Binding)**: Lập trình hàm tạo mã định danh thiết bị (`deviceId`) bằng cách thu thập thông tin trình duyệt, màn hình, user-agent để ngăn chặn việc chia sẻ tài khoản.
- **Chấm điểm tự động**: Lấy kết quả bài làm, so sánh với đáp án (từ thẻ script json), tính tổng số câu đúng và tỷ lệ phần trăm (%).
- **Tái tạo Website hàng loạt**: Viết script `rebuild_from_git.py` để quét lại giao diện `template.html` chuẩn mực nhất và nhân bản/áp dụng đè lên toàn bộ 102 thư mục bài học, đồng bộ hóa mọi thay đổi.

## 3. Lập trình Hệ thống Backend (Google Apps Script)
- **Bảng điều khiển Trung tâm (Google Sheets)**: Xây dựng cấu trúc các trang tính:
  - `Students`: Lưu thông tin học viên, Nickname, và `Device ID` (thiết bị độc quyền).
  - `HV_...` (Ví dụ: `HV_NGUYENHUNG`): Trang tính cá nhân của từng học viên được tự động sinh ra.
- **Tính năng Apps Script (Code.gs)**:
  - Cung cấp API `doPost` nhận yêu cầu Đăng nhập (`login`) và Nộp bài (`submit`) từ trang web gửi về.
  - **Kiểm tra thiết bị**: Khi học viên đăng nhập lần đầu, hệ thống ghi nhận `Device ID`. Lần sau nếu `Device ID` khác, hệ thống chặn đăng nhập và báo lỗi.
  - **Tạo Menu tự động**: Thêm menu công cụ tùy chỉnh trên thanh công cụ của Google Sheets để giáo viên có thể "Đồng bộ Học viên" (tạo tự động các sheet cá nhân và gắn link hyperlink vào tên ở sheet tổng) và "Dọn dẹp & Di cư dữ liệu cũ".

## 4. Cải tiến Logic Ghi nhận Điểm số (Nhật ký cá nhân)
- Ban đầu, kết quả đổ về một sheet `Submissions` chung, khiến việc theo dõi rất lộn xộn.
- **Cải tiến**: Đổi sang cơ chế Sheet cá nhân. Mỗi học viên có 1 sheet riêng.
- **Logic chèn điểm**: 
  - Khi có hành động mới, hệ thống tìm tên bài học (Ví dụ: `Basic Listening Lesson #01`). 
  - Nếu chưa có, tạo dòng mới. Nếu đã có, tìm cột trống tiếp theo trên cùng dòng đó (Lần 1, Lần 2, Lần 3...) để điền kết quả.
- **Ghi nhận ngay khi đăng nhập**: 
  - Yêu cầu: "Ghi nhận tất cả các lần đăng nhập, kể cả không làm bài thì thi 0/0".
  - Sửa HTML: Khi Fetch API hành động `login`, hệ thống gửi kèm `lessonId` (Tên bài học).
  - Sửa Apps Script: Khi nhận được action `login`, hệ thống lập tức chèn `0/0` vào sheet cá nhân của học viên đó. Nếu sau đó nộp bài thật, điểm thật sẽ được chèn vào ô bên cạnh.
  - Ghi nhận luôn cả các lần đăng nhập thất bại (Sai thiết bị) vào lịch sử để giáo viên theo dõi hành vi mờ ám.

## 5. Khắc phục Sự cố Triển khai trên GitHub Pages
- **Lỗi 404 File Not Found**: Sau khi push code hàng loạt, GitHub Pages báo lỗi 404 không truy cập được bất cứ bài nào.
- **Nguyên nhân**: Trong mã nguồn HTML, hệ thống dùng cú pháp Liquid template `{{TITLE}}` để Python tự thay thế tên bài học. Tuy nhiên, Jekyll (hệ thống build web mặc định của GitHub) tưởng nhầm đó là lệnh của nó, dẫn đến biên dịch lỗi (crash) toàn bộ kho lưu trữ.
- **Giải pháp**: Tạo và đẩy một file rỗng mang tên `.nojekyll` lên thư mục gốc của kho lưu trữ. File này "ra lệnh" cho GitHub bỏ qua việc kiểm tra bằng Jekyll và trực tiếp xuất bản các file HTML nguyên bản, lập tức khắc phục triệt để lỗi 404.
- **Lỗi không cập nhật bài khác ngoài bài 1**: Do thay đổi đường link API của Apps Script, nhưng chưa chạy lại lệnh `rebuild_from_git.py` để đè link mới (`WEB_APP_URL`) vào tất cả 102 bài. Đã xử lý bằng cách cập nhật link và chạy lại trình nhân bản.

---
**Kết luận**: Công cụ hiện tại là một hệ sinh thái tĩnh-động hoàn chỉnh. Phía Frontend là các file HTML tĩnh được lưu trữ miễn phí, siêu tốc độ trên GitHub Pages. Phía Backend sử dụng Google Apps Script như một API không máy chủ (Serverless), lưu trữ toàn bộ cơ sở dữ liệu trên Google Sheets một cách trực quan, bảo mật thiết bị tốt và tự động hóa cao dành cho Giáo viên.
