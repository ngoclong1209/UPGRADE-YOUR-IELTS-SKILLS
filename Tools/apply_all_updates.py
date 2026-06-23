import os
import glob
import re

base_dir = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"

payment_text = """
                        <p style="margin: 6px 0; font-size: 0.85rem; color: #666; border-top: 1px dashed rgba(0,0,0,0.15); padding-top: 8px;">
                            ⚠️ <b>LƯU Ý:</b> Phiên đăng nhập luyện tập này của bạn đã được Giáo viên thanh toán <b>5.000đ/lượt</b>. Sau 3 lượt (tối đa 15.000đ) thì các lượt làm bài khác của bạn được MIỄN PHÍ. Vui lòng làm bài nghiêm túc!
                        </p>
"""

def replace_payment_text(html):
    # If the file already has the payment card with the old text, replace it.
    old_text_pattern = re.compile(r'<p[^>]*>💳\s*<b>Hình thức thanh toán:</b>[^<]*</p>', re.IGNORECASE)
    if old_text_pattern.search(html):
        html = old_text_pattern.sub(payment_text.strip(), html)
    else:
        # Check if the simplified notice exists, and replace it
        simple_notice_pattern = re.compile(r'<div[^>]*>[\s]*⚠️ <b>LƯU Ý:</b> Phiên đăng nhập luyện tập này của bạn đã được Giáo viên thanh toán <b>5,000đ/lượt</b>[^<]*</div>', re.IGNORECASE)
        if simple_notice_pattern.search(html):
            html = simple_notice_pattern.sub("", html) # Just remove it, we will inject the full modal later if needed
    return html

full_login_modal = """
    <div class="login-overlay" id="login-overlay" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.85); z-index: 99999; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(8px);">
        <div class="login-box" style="background: linear-gradient(145deg, #ffffff, #fff0f5); padding: 40px; border-radius: 30px; width: 90%; max-width: 450px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); border: 4px solid var(--border-color, #ffccd5);">
            <div class="login-header" style="font-family: 'DynaPuff', cursive; font-size: 2rem; color: var(--accent, #ff85a2); margin-bottom: 10px; text-shadow: 2px 2px 0px rgba(255,133,162,0.2);">🍭 Study Room Login 🍭</div>
            <div class="login-subheader" style="color: var(--text-secondary, #8c6d7d); font-size: 1.1rem; margin-bottom: 25px; font-weight: 500;">Enter your lovely nickname to join the lesson! ✨</div>
            
            <div id="login-form-fields">
                <input type="text" class="login-input" id="nickname-input" placeholder="Nhập ID học viên..." style="width: 100%; padding: 15px 20px; font-size: 1.2rem; border: 3px solid var(--border-color, #ffccd5); border-radius: 15px; margin-bottom: 20px; outline: none; transition: all 0.3s;" autofocus>
                <button class="check-btn" onclick="grantAccess()" style="width: 100%; padding: 15px; font-size: 1.2rem; font-weight: bold; background: var(--success, #4ad99d); color: white; border: none; border-radius: 15px; cursor: pointer; transition: all 0.2s;">🚀 BẮT ĐẦU LÀM BÀI</button>
            </div>

            <div id="login-loading-fields" style="display: none; margin-top: 10px;">
                <div class="loading-status" id="loading-status" style="font-family: 'Fredoka', sans-serif; font-size: 1.15rem; font-weight: 600; margin-bottom: 15px; color: #333;">Đang kết nối hệ thống học tập...</div>
                <div class="progress-bar-container" style="width: 100%; height: 20px; background: rgba(0, 0, 0, 0.1); border-radius: 10px; overflow: hidden; margin-bottom: 25px; box-shadow: inset 0 2px 5px rgba(0,0,0,0.15);">
                    <div class="progress-bar-fill" id="progress-bar-fill" style="width: 0%; height: 100%; background: linear-gradient(90deg, #ff758c 0%, #ff7eb3 100%); border-radius: 10px; transition: width 0.1s linear;"></div>
                </div>
                <div class="payment-card" style="background: rgba(255, 255, 255, 0.95); border: 2.5px solid var(--border-color, #ffccd5); border-radius: 20px; padding: 20px; text-align: left; box-shadow: 0 10px 25px rgba(0,0,0,0.05); font-family: 'Fredoka', sans-serif;">
                    <div style="font-size: 1.1rem; font-weight: 700; color: #ff5e7e; margin-bottom: 12px; border-bottom: 2px dashed rgba(0,0,0,0.1); padding-bottom: 8px; text-align: center;">🎫 THÔNG TIN HỌC LIỆU & THANH TOÁN</div>
                    <div style="font-size: 0.95rem; line-height: 1.6; color: #333;">
                        <p style="margin: 6px 0;">💵 <b>Bài luyện tập:</b> <span style="color: #2b9348; font-weight: bold;">Nghe hiểu & Đọc hiểu</span></p>
                        <p style="margin: 6px 0;">💰 <b>Giá trị bài học:</b> <span style="color: #e91e63; font-weight: bold;">5.000 VND</span></p>
                        <p style="margin: 6px 0;">👤 <b>Đã được thanh toán bởi:</b> <span style="color: #0077b6; font-weight: bold;">VŨ NGỌC LONG</span> <span id="payment-nickname-badge" style="font-size: 0.8rem; background: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 12px; font-weight: 700; margin-left: 5px;"></span></p>
                        <p style="margin: 6px 0; font-size: 0.85rem; color: #666; border-top: 1px dashed rgba(0,0,0,0.15); padding-top: 8px;">
                            ⚠️ <b>LƯU Ý:</b> Phiên đăng nhập luyện tập này của bạn đã được Giáo viên thanh toán <b>5.000đ/lượt</b>. Sau 3 lượt (tối đa 15.000đ) thì các lượt làm bài khác của bạn được MIỄN PHÍ. Vui lòng làm bài nghiêm túc!
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
"""

login_js = """
<script>
    function playSfx(id) {
        let el = document.getElementById(id);
        if(el) {
            el.currentTime = 0;
            el.play().catch(e=>{});
        }
    }
    function grantAccess() {
        const input = document.getElementById('nickname-input');
        let nickname = input ? input.value.trim() : '';
        if (!nickname) {
            alert("Vui lòng nhập ID Học Viên của bạn! 🌸");
            return;
        }
        playSfx('sfx-click');
        
        let formFields = document.getElementById('login-form-fields');
        if(formFields) formFields.style.display = "none";
        let loadFields = document.getElementById('login-loading-fields');
        if(loadFields) loadFields.style.display = "block";
        let badge = document.getElementById('payment-nickname-badge');
        if(badge) badge.innerText = nickname;
        
        const progressFill = document.getElementById('progress-bar-fill');
        const statusText = document.getElementById('loading-status');
        
        let progress = 0;
        let interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 100) progress = 100;
            if(progressFill) progressFill.style.width = progress + '%';
            
            if (progress > 30 && progress < 70) {
                if(statusText) statusText.innerText = "Đang kiểm tra thanh toán...";
            } else if (progress >= 70 && progress < 100) {
                if(statusText) statusText.innerText = "Xác nhận thành công! Chuẩn bị phòng học...";
            }
            
            if (progress === 100) {
                clearInterval(interval);
                setTimeout(() => {
                    let overlay = document.getElementById('login-overlay');
                    if(overlay) overlay.style.display = "none";
                    
                    let wBanner = document.getElementById('welcome-banner');
                    if(wBanner) wBanner.style.display = "flex";
                    
                    let wName = document.getElementById('welcome-user-name');
                    if(wName) wName.innerText = "Chào mừng, " + nickname + "! ✨";
                    
                    playSfx('sfx-success');
                    
                    let header = document.getElementById('main-header');
                    if(header) header.style.display = "flex";
                    
                    localStorage.setItem('youpass_student_id', nickname);
                    
                    setTimeout(() => {
                        if(wBanner) {
                            wBanner.style.opacity = '0';
                            setTimeout(() => {
                                wBanner.style.display = "none";
                                if(typeof startTimer === 'function') startTimer();
                            }, 500);
                        } else {
                            if(typeof startTimer === 'function') startTimer();
                        }
                    }, 2000);
                }, 500);
            }
        }, 300);
    }

    // Auto check login
    window.addEventListener('DOMContentLoaded', () => {
        let sid = localStorage.getItem('youpass_student_id');
        if(sid) {
            let overlay = document.getElementById('login-overlay');
            if(overlay) overlay.style.display = "none";
            let header = document.getElementById('main-header');
            if(header) header.style.display = "flex";
            if(typeof startTimer === 'function') startTimer();
        } else {
            let overlay = document.getElementById('login-overlay');
            if(overlay) overlay.style.display = "flex";
        }
    });
</script>
"""

timer_css = """
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
            margin-left: 15px;
        }
"""

def inject_timer_and_login(html, minutes=60):
    # 1. Inject CSS if not present
    if "neonPulse" not in html:
        html = html.replace("</style>", timer_css + "\n</style>")
    
    # 2. Inject audio if not present
    if "sfx-tick" not in html:
        html = html.replace("</body>", """
    <audio id="sfx-tick" src="https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3" preload="auto" loop></audio>
    <audio id="sfx-click" src="https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3" preload="auto"></audio>
    <audio id="sfx-success" src="https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3" preload="auto"></audio>
</body>""")

    # 3. Inject login modal if simple one is found, OR replace old login-overlay
    if 'id="student-modal"' in html:
        html = re.sub(r'<div[^>]*id="student-modal"[^>]*>.*?</div>\s*</div>', full_login_modal, html, flags=re.DOTALL)
        html = re.sub(r'<div[^>]*id="student-modal"[^>]*>.*?</div>', full_login_modal, html, flags=re.DOTALL)
    elif '<div class="login-overlay"' in html:
        # Replaces existing login overlay text
        html = replace_payment_text(html)
    else:
        # Just inject it after body
        html = html.replace("<body>", "<body>\n" + full_login_modal)

    # Inject login JS logic
    if "function grantAccess" not in html:
        html = html.replace("</body>", login_js + "\n</body>")
    else:
        # Make sure auto-login has startTimer
        if "startTimer()" not in html:
            html = html.replace("grantAccess() {", "grantAccess() {\nif(typeof startTimer === 'function') setTimeout(startTimer, 2000);")

    # 4. Inject Timer display into header
    if "timer-display" not in html:
        # Add to header-left or header-right
        if '<div class="header-right">' in html:
            html = html.replace('<div class="header-right">', f'<div class="header-right">\n            <div class="neon-timer" id="timer-display">⏱ {minutes}:00</div>')
        elif '</h1>' in html:
            html = html.replace('</h1>', f'</h1>\n            <div class="neon-timer" id="timer-display">⏱ {minutes}:00</div>')

    # 5. Inject Timer JS Logic
    if "function startTimer" not in html:
        timer_js = f"""
        let timeLeft = {minutes} * 60;
        let timerInterval;
        function startTimer() {{
            const display = document.getElementById('timer-display');
            if(!display) return;
            timerInterval = setInterval(() => {{
                timeLeft--;
                let m = Math.floor(timeLeft / 60);
                let s = timeLeft % 60;
                display.innerText = `⏱ ${{m < 10 ? '0' : ''}}${{m}}:${{s < 10 ? '0' : ''}}${{s}}`;
                
                if(timeLeft <= 60 && timeLeft > 0) {{
                    const tickAudio = document.getElementById('sfx-tick');
                    if(tickAudio && tickAudio.paused) {{
                        tickAudio.play().catch(e=>{{}});
                    }}
                }}
                
                if (timeLeft <= 0) {{
                    clearInterval(timerInterval);
                    const tickAudio = document.getElementById('sfx-tick');
                    if(tickAudio) tickAudio.pause();
                    let btn = document.getElementById('btn-submit');
                    if(btn) btn.click();
                }}
            }}, 1000);
        }}
        """
        html = html.replace("</script>\n</body>", timer_js + "\n</script>\n</body>")

    return html

# Update Reading template (10 mins)
reading_tpl = os.path.join(base_dir, 'ReadingA1-C2/frontend/template_reading.html')
if os.path.exists(reading_tpl):
    with open(reading_tpl, 'r', encoding='utf-8') as f:
        html = f.read()
    html = inject_timer_and_login(html, minutes=10)
    with open(reading_tpl, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated Reading Template")

# Update Listening template
listening_tpl = os.path.join(base_dir, 'pte-listening-audios/template.html')
if os.path.exists(listening_tpl):
    with open(listening_tpl, 'r', encoding='utf-8') as f:
        html = f.read()
    html = inject_timer_and_login(html, minutes=60) # Note: listening might not need a timer, but won't hurt if we use same logic
    with open(listening_tpl, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated Listening Template")

# Update Full tests
for file_path in glob.glob(os.path.join(base_dir, 'data/practicepteonline/reading/**/*.html'), recursive=True):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    html = inject_timer_and_login(html, minutes=60)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
print("Updated Reading Full Tests")

for file_path in glob.glob(os.path.join(base_dir, 'data/practicepteonline/listening/**/*.html'), recursive=True):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    html = inject_timer_and_login(html, minutes=60)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
print("Updated Listening Full Tests")

