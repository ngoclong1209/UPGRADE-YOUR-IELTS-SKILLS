import os
import re

# 1. Update template_reading.html (10 min timer, ticking sound, login payment notice, device ip)
reading_file = 'ReadingA1-C2/frontend/template_reading.html'
with open(reading_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Add neon timer CSS
neon_css = """
        @keyframes neonPulse {
            from { box-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #ff0055, 0 0 20px #ff0055; text-shadow: 0 0 5px #fff, 0 0 10px #ff0055, 0 0 15px #ff0055; }
            to { box-shadow: 0 0 2px #fff, 0 0 5px #fff, 0 0 7px #ff0055, 0 0 10px #ff0055; text-shadow: 0 0 2px #fff, 0 0 5px #ff0055, 0 0 7px #ff0055; }
        }
        .neon-timer {
            font-size: 1.8rem !important; 
            font-family: 'DynaPuff', cursive; 
            color: #ffeb3b !important; 
            animation: neonPulse 1.2s infinite alternate; 
            padding: 4px 15px; 
            border-radius: 12px; 
            background: rgba(0,0,0,0.85); 
            border: 2px solid #ff0055; 
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
"""
html = html.replace('</style>\n</head>', neon_css + '\n</style>\n</head>')

# Add audio tags
audio_tags = """
    <!-- Hidden audio elements for SFX -->
    <audio id="sfx-tick" src="https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3" preload="auto" loop></audio>
"""
html = html.replace('<!-- Hidden audio elements for SFX -->', audio_tags)

# Replace timer UI
html = html.replace('<span id="timer-display" style="font-size: 1.1rem;">⏱ 20:00</span>', '<span id="timer-display" class="neon-timer">⏱ 10:00</span>')

# Update modal HTML
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

# Update timer logic
html = html.replace('let timeLeft = 20 * 60; // 20 minutes', 'let timeLeft = 10 * 60; // 10 minutes')

tick_logic = """
                if(timeLeft <= 60 && timeLeft > 0) {
                    const tickAudio = document.getElementById('sfx-tick');
                    if(tickAudio && tickAudio.paused) {
                        tickAudio.play().catch(e=>{});
                    }
                }
                if (timeLeft <= 0) {
                    const tickAudio = document.getElementById('sfx-tick');
                    if(tickAudio) { tickAudio.pause(); }
                    clearInterval(timerInterval);
                    document.getElementById('btn-submit').click();
                }
"""
# Replace the end of the timer logic
html = re.sub(r'if \(timeLeft <= 0\) \{[\s\S]*?clearInterval\(timerInterval\);[\s\S]*?document\.getElementById\(\'btn-submit\'\)\.click\(\);[\s\S]*?\}', tick_logic, html)

with open(reading_file, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated Reading template.")
