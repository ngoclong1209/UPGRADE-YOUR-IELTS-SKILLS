import os
import glob
import re

base_dir = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS/practicepteonline/listening"

full_login_modal = """
    <!-- UNIFIED LOGIN OVERLAY -->
    <div class="login-overlay" id="login-overlay" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.85); z-index: 99999; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(8px);">
        <div class="login-box" style="background: linear-gradient(145deg, #ffffff, #fff0f5); padding: 40px; border-radius: 30px; width: 90%; max-width: 450px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); border: 4px solid #ffccd5;">
            <div class="login-header" style="font-family: 'DynaPuff', cursive; font-size: 2.2rem; color: #ff85a2; margin-bottom: 10px; text-shadow: 2px 2px 0px rgba(255,133,162,0.2);">🍭 Study Room 🍭</div>
            
            <div id="login-form-fields">
                <div style="background: #fff0f2; padding: 15px; border-radius: 15px; border-left: 5px solid #ff768a; margin-bottom: 20px; font-size: 0.95rem; line-height: 1.5; color: #5c404d; text-align: left;">
                    ⚠️ <b>LƯU Ý:</b> Phiên đăng nhập luyện tập này của bạn đã được Giáo viên thanh toán <b>5.000đ/lượt</b>. Sau 3 lượt (tối đa 15.000đ), các lượt làm bài khác của bạn được <b>MIỄN PHÍ</b>.
                </div>
                
                <input type="text" id="nickname-input" placeholder="Nhập ID Học Viên..." 
                       style="width: 100%; padding: 18px 25px; font-size: 1.2rem; border: 3px solid #ffccd5; border-radius: 25px; outline: none; transition: 0.3s; margin-bottom: 25px; text-align: center; color: #5c404d; background: #fffafb; font-family: 'Quicksand', sans-serif;"
                       onfocus="this.style.borderColor='#ff85a2'; this.style.boxShadow='0 0 15px rgba(255,133,162,0.3)';" 
                       onblur="this.style.borderColor='#ffccd5'; this.style.boxShadow='none';">
                
                <button onclick="grantAccess()" 
                        style="width: 100%; padding: 18px 30px; font-size: 1.2rem; color: white; background: linear-gradient(135deg, #ff85a2 0%, #ff5e7e 100%); border: none; border-radius: 25px; cursor: pointer; font-weight: 700; transition: 0.3s; box-shadow: 0 10px 20px rgba(255,94,126,0.3); font-family: 'Quicksand', sans-serif;"
                        onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 15px 25px rgba(255,94,126,0.4)';"
                        onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 10px 20px rgba(255,94,126,0.3)';">
                    ✨ VÀO LỚP ✨
                </button>
            </div>

            <div id="login-loading-fields" style="display: none; padding: 20px 0;">
                <div style="font-size: 1.3rem; color: #5c404d; font-weight: bold; margin-bottom: 20px;">Đang xác thực <span id="payment-nickname-badge" style="color: #ff85a2;"></span>...</div>
                <div style="width: 100%; background: #ffccd5; border-radius: 10px; height: 10px; overflow: hidden; margin-bottom: 15px;">
                    <div id="progress-bar-fill" style="width: 0%; height: 100%; background: #ff85a2; transition: width 0.3s ease;"></div>
                </div>
                <div id="loading-status" style="font-size: 1rem; color: #8c6d7d;">Đang kiểm tra kết nối...</div>
            </div>
        </div>
    </div>
"""

login_js = """
<script>
    const APP_URL = "https://script.google.com/macros/s/AKfycbxRuciqVjFT1c_DysTwfZuoW3xof42fuLwFtD78CSiTJ-bAaakkWIg_cakaHURb8bXc/exec";

    function getDeviceId() {
        let did = localStorage.getItem('youpass_device_id');
        if(!did) {
            let fp = btoa(navigator.userAgent + screen.width + screen.height + navigator.language).substring(0, 15);
            did = fp + '_' + Math.random().toString(36).substr(2, 5);
            localStorage.setItem('youpass_device_id', did);
        }
        return did;
    }
    
    function playSfx(id) {
        try { let a = document.getElementById(id); if(a) { a.currentTime = 0; a.play().catch(e=>{}); } } catch(e){}
    }

    async function grantAccess() {
        const input = document.getElementById('nickname-input');
        let nickname = input ? input.value.trim().toUpperCase() : '';
        if (!nickname) { alert("Vui lòng nhập ID Học Viên của bạn! 🌸"); return; }
        
        playSfx('sfx-click');
        let formFields = document.getElementById('login-form-fields');
        if(formFields) formFields.style.display = "none";
        let loadFields = document.getElementById('login-loading-fields');
        if(loadFields) loadFields.style.display = "block";
        let badge = document.getElementById('payment-nickname-badge');
        if(badge) badge.innerText = nickname;
        
        const progressFill = document.getElementById('progress-bar-fill');
        const statusText = document.getElementById('loading-status');
        let deviceId = getDeviceId();
        
        if(progressFill) progressFill.style.width = '10%';
        if(statusText) statusText.innerText = "Đang kiểm tra thiết bị & IP...";

        try {
            let ipData = {};
            try {
                let ipRes = await fetch('https://api.ipify.org?format=json');
                ipData = await ipRes.json();
            } catch(e) { console.log("IP fetch failed", e); }
            
            if(progressFill) progressFill.style.width = '40%';
            if(statusText) statusText.innerText = "Đang xác thực tài khoản...";

            let loginRes = await fetch(APP_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'text/plain;charset=utf-8' },
                body: JSON.stringify({ action: 'login', student_id: nickname, device_id: deviceId, ip: ipData.ip || 'unknown' })
            });
            
            let data = await loginRes.json();
            if(progressFill) progressFill.style.width = '100%';

            if (data.status === 'success') {
                if(statusText) statusText.innerText = "Xác nhận thành công! Chuẩn bị phòng học...";
                setTimeout(() => {
                    let overlay = document.getElementById('login-overlay');
                    if(overlay) overlay.style.display = "none";
                    localStorage.setItem('youpass_student_id', nickname);
                    playSfx('sfx-success');
                    if(typeof startTimer === 'function') startTimer();
                }, 500);
            } else {
                if(statusText) statusText.innerText = "LỖI: " + data.message;
                if(statusText) statusText.style.color = "red";
                alert(data.message);
                setTimeout(() => {
                    if(loadFields) loadFields.style.display = "none";
                    if(formFields) formFields.style.display = "block";
                    if(progressFill) progressFill.style.width = '0%';
                }, 2000);
            }
        } catch(err) {
            alert("Lỗi kết nối máy chủ! Vui lòng thử lại.");
            if(loadFields) loadFields.style.display = "none";
            if(formFields) formFields.style.display = "block";
        }
    }

    window.addEventListener('DOMContentLoaded', () => {
        let sid = localStorage.getItem('youpass_student_id');
        if(sid) {
            let overlay = document.getElementById('login-overlay');
            if(overlay) overlay.style.display = "none";
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

def process_html_file(file_path, minutes=60):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove ANY existing login overlay (fairytale, student-modal, old unified login)
    html = re.sub(r'<div[^>]*class="login-overlay"[^>]*>.*?<!-- Login Overlay Ends or just closing divs -->', '', html, flags=re.DOTALL)
    # The regex above is tricky. Let's just remove everything from <div class="login-overlay" to the first <script> or something.
    # Actually, we can use a simpler approach: Just find <div class="login-overlay" and delete it up to the matching </div> 
    # But since it's nested, simpler is to just replace body with body + modal if not present.
    # To avoid duplicates, let's remove existing ones by matching id="login-overlay" up to the 6th closing div.
    # Better: If it contains 'id="login-overlay"', replace it.
    
    html = re.sub(r'<div[^>]*id="login-overlay"[^>]*>.*?</div>\s*</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)
    html = re.sub(r'<div[^>]*id="login-overlay"[^>]*>.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)
    html = re.sub(r'<div[^>]*class="login-overlay"[^>]*>.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)
    html = re.sub(r'<div[^>]*id="student-modal"[^>]*>.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)

    # Remove any old auto login scripts or grantAccess
    html = re.sub(r'<script>\s*const APP_URL.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'function grantAccess\(\) \{.*?</script>', '</script>', html, flags=re.DOTALL)
    
    # 2. Inject CSS
    if "neonPulse" not in html:
        html = html.replace("</style>", timer_css + "\n</style>")

    # 3. Inject Modal right after <body>
    html = html.replace("<body>", "<body>\n" + full_login_modal)

    # 4. Inject Audio & JS right before </body>
    if "sfx-tick" not in html:
        html = html.replace("</body>", """
    <audio id="sfx-tick" src="https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3" preload="auto" loop></audio>
    <audio id="sfx-click" src="https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3" preload="auto"></audio>
    <audio id="sfx-success" src="https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3" preload="auto"></audio>
</body>""")

    html = html.replace("</body>", login_js + "\n</body>")

    # 5. Inject Timer display into header
    if "timer-display" not in html:
        if '<div class="header-right">' in html:
            html = html.replace('<div class="header-right">', f'<div class="header-right">\n            <div class="neon-timer" id="timer-display">⏱ {minutes}:00</div>')
        elif '</h1>' in html:
            html = html.replace('</h1>', f'</h1>\n            <div class="neon-timer" id="timer-display">⏱ {minutes}:00</div>')

    # 6. Inject Timer JS Logic
    if "function startTimer" not in html:
        timer_js = f"""
<script>
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
</script>
        """
        html = html.replace("</body>", timer_js + "\n</body>")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

count = 0
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith(".html") and not "debug" in root:
            # Determine minutes
            mins = 60
            if "ReadingA1-C2" in root or "reading" in root.lower():
                if "FullTest" not in root and "Test_" in root:
                    mins = 10 # Regular reading is 10 mins
            
            try:
                process_html_file(os.path.join(root, f), minutes=mins)
                count += 1
            except Exception as e:
                print(f"Failed {f}: {e}")

print(f"Successfully processed {count} HTML files!")
