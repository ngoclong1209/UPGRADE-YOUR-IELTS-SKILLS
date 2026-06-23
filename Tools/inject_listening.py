listening_file = 'pte-listening-audios/template.html'
with open(listening_file, 'r', encoding='utf-8') as f:
    html = f.read()

old_modal = """    <div id="student-modal" style="display: none;">
        <div class="modal-content">
            <h2>👋 Xin chào!</h2>
            <p>Vui lòng nhập Tên hoặc Mã Học Viên của bạn để hệ thống lưu điểm nhé:</p>
            <input type="text" id="student-name-input" placeholder="Tên của bạn...">
            <br>
            <button id="save-student-btn" onclick="saveStudentId()">Bắt đầu làm bài</button>
        </div>
    </div>"""

new_modal = """    <div class="login-overlay theme-aladdin" id="student-modal" style="display: none;">
        <div class="login-box">
            <div class="login-header">👋 XIN CHÀO!</div>
            <div class="login-subheader">Vui lòng nhập Mã Học Viên để bắt đầu</div>
            <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; margin-bottom: 20px; font-size: 0.95rem; line-height: 1.4; border: 1px dashed #fbbf24; color: #fef08a;">
                ⚠️ <b>LƯU Ý:</b> Phiên đăng nhập luyện tập này của bạn đã được Giáo viên thanh toán <b>5,000đ/lượt</b>. Sau 3 lượt (tối đa 15,000đ), các lượt làm bài tiếp theo của bạn sẽ được MIỄN PHÍ. Vui lòng làm bài nghiêm túc!
            </div>
            <input type="text" class="login-input" id="student-name-input" placeholder="Nhập ID học viên..." />
            <button class="check-btn" id="save-student-btn" onclick="saveStudentId()">🚀 BẮT ĐẦU LÀM BÀI</button>
        </div>
    </div>"""

html = html.replace(old_modal, new_modal)

with open(listening_file, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated Listening template.")
