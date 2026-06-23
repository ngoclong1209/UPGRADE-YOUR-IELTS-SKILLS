import os
import re
from bs4 import BeautifulSoup

BASE_DIR = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"

DIRS = [
    ("ReadingA1-C2", "1232 bài luyện tập đọc hiểu"),
    ("pte-listening-audios", "102 bài tập Nghe"),
    ("practicepteonline/listening", "204 bài thi Listening Full"),
    ("practicepteonline/reading", "315 bài thi Reading Full")
]

HTML_TEMPLATE = """
    <!-- UNIFIED LOGIN OVERLAY -->
    <div class="login-overlay" id="login-overlay" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.85); z-index: 99999; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(8px);">
        <div class="login-box" style="background: linear-gradient(145deg, #ffffff, #fff0f5); padding: 40px; border-radius: 30px; width: 90%; max-width: 450px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); border: 4px solid #ffccd5;">
            <div class="login-header" style="font-family: 'DynaPuff', cursive; font-size: 2.2rem; color: #ff85a2; margin-bottom: 10px; text-shadow: 2px 2px 0px rgba(255,133,162,0.2);">🍭 Study Room 🍭</div>
            <div class="login-subheader" style="font-size: 1rem; color: #8c6d7d; margin-bottom: 25px; font-family: 'Quicksand', sans-serif;">Enter your lovely nickname to join the lesson! ✨</div>
            
            <div id="login-form-fields">
                <input type="text" class="login-input" id="nickname-input" placeholder="Your cute name..." autofocus 
                    style="width: 100%; padding: 18px 25px; font-size: 1.2rem; border: 3px solid #ffccd5; border-radius: 25px; outline: none; transition: 0.3s; margin-bottom: 25px; text-align: center; color: #5c404d; background: #fffafb; font-family: 'Quicksand', sans-serif;"
                    onfocus="this.style.borderColor='#ff85a2'; this.style.boxShadow='0 0 15px rgba(255,133,162,0.3)';" 
                    onblur="this.style.borderColor='#ffccd5'; this.style.boxShadow='none';">
                <button class="check-btn" onclick="grantAccess()"
                    style="width: 100%; padding: 18px 30px; font-size: 1.2rem; color: white; background: linear-gradient(135deg, #ff85a2 0%, #ff5e7e 100%); border: none; border-radius: 25px; cursor: pointer; font-weight: 700; transition: 0.3s; box-shadow: 0 10px 20px rgba(255,94,126,0.3); font-family: 'Quicksand', sans-serif;"
                    onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 15px 25px rgba(255,94,126,0.4)';"
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 10px 20px rgba(255,94,126,0.3)';">
                    LET'S GO! 🌸
                </button>
            </div>

            <div id="login-loading-fields" style="display: none; padding: 20px 0;">
                <div class="loading-status" id="loading-status" style="font-family: 'Quicksand', sans-serif; font-size: 1.15rem; font-weight: 600; margin-bottom: 15px; color: #333;">Đang kết nối hệ thống...</div>
                <div class="progress-bar-container" style="width: 100%; height: 20px; background: rgba(0, 0, 0, 0.1); border-radius: 10px; overflow: hidden; margin-bottom: 25px; box-shadow: inset 0 2px 5px rgba(0,0,0,0.15);">
                    <div class="progress-bar-fill" id="progress-bar-fill" style="width: 0%; height: 100%; background: linear-gradient(90deg, #ff758c 0%, #ff7eb3 100%); border-radius: 10px; transition: width 0.1s linear;"></div>
                </div>
                <div class="payment-card" style="background: rgba(255, 255, 255, 0.95); border: 2.5px solid #e5e7eb; border-radius: 20px; padding: 20px; text-align: left; box-shadow: 0 10px 25px rgba(0,0,0,0.05); font-family: 'Quicksand', sans-serif;">
                    <div style="font-size: 1.1rem; font-weight: 700; color: #ff5e7e; margin-bottom: 12px; border-bottom: 2px dashed rgba(0,0,0,0.1); padding-bottom: 8px; text-align: center;">🎫 THÔNG TIN THANH TOÁN</div>
                    <div style="font-size: 0.95rem; line-height: 1.6; color: #333;">
                        <p style="margin: 6px 0;">💵 <b>Nội dung khoá học:</b> <span style="color: #2b9348; font-weight: bold;">1232 bài tập Đọc hiểu, 102 bài tập Nghe, 204 bài thi Listening Full, 315 bài thi Reading Full</span></p>
                        <p style="margin: 6px 0;">💰 <b>Giá trị:</b> <span style="color: #e91e63; font-weight: bold;">1,599,000 VND</span></p>
                        <p style="margin: 6px 0;">👤 <b>Đã được trả phí bởi:</b> <span style="color: #0077b6; font-weight: bold;">VŨ NGỌC LONG</span> <span id="payment-nickname-badge" style="font-size: 0.8rem; background: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 12px; font-weight: 700; margin-left: 5px;"></span></p>
                        <p style="margin: 6px 0; font-size: 0.85rem; color: #666; border-top: 1px solid rgba(0,0,0,0.08); padding-top: 8px;">⏱️ <b>Thời hạn sử dụng:</b> 1 năm.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
"""

JS_TEMPLATE = """
    const APP_URL = "https://script.google.com/macros/s/AKfycbx-KeSd_VIwmvrRRifyKl3CLMU3pc91_oURdunCnHBUYEn-UkHm3LwgCeTR5ltY1Afy/exec";

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
        if (!nickname) { alert("Vui lòng nhập tên của bạn! 🌸"); return; }
        
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
                    let mainLayout = document.querySelector('.main-layout');
                    if(mainLayout) mainLayout.style.display = "flex";
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
        let overlay = document.getElementById('login-overlay');
        let mainLayout = document.querySelector('.main-layout');
        if(sid) {
            if(overlay) overlay.style.display = "none";
            if(mainLayout) mainLayout.style.display = "flex";
            if(typeof startTimer === 'function') startTimer();
        } else {
            if(overlay) overlay.style.display = "flex";
            if(mainLayout) mainLayout.style.display = "none";
        }
    });
"""

def process_file(filepath, module_name):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')
        
        # 1. Remove old overlays
        for old_overlay in soup.find_all('div', id='login-overlay'):
            old_overlay.decompose()
        for old_overlay in soup.find_all('div', class_='login-overlay'):
            old_overlay.decompose()
        for old_modal in soup.find_all('div', id='student-modal'):
            old_modal.decompose()

        # 2. Remove old scripts
        for script in soup.find_all('script'):
            if script.string:
                if 'const APP_URL' in script.string or 'function grantAccess' in script.string or 'youpass_student_id' in script.string:
                    script.decompose()

        # 3. Add Google Fonts for DynaPuff/Quicksand if missing
        head = soup.find('head')
        if head:
            font_link = soup.new_tag('link', href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300..700&family=DynaPuff:wght@400..700&family=Quicksand:wght@300..700&display=swap", rel="stylesheet")
            if not soup.find('link', href=re.compile('DynaPuff')):
                head.append(font_link)

        # 4. Inject new overlay as first child of body
        body = soup.find('body')
        if body:
            html_with_text = HTML_TEMPLATE.replace("{MODULE_TEXT}", module_name)
            overlay_soup = BeautifulSoup(html_with_text, 'html.parser')
            body.insert(0, overlay_soup)

            # 5. Inject JS script as last child of body
            js_script_tag = soup.new_tag('script')
            js_script_tag.string = JS_TEMPLATE
            body.append(js_script_tag)
            
            # Add audio elements for SFX if they don't exist
            if not soup.find('audio', id='sfx-click'):
                audio_click = soup.new_tag('audio', id='sfx-click', src='https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3', preload='auto')
                body.append(audio_click)
            if not soup.find('audio', id='sfx-success'):
                audio_success = soup.new_tag('audio', id='sfx-success', src='https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3', preload='auto')
                body.append(audio_success)

        # Main Layout initialization - we want to hide it by default so it doesn't blink before DOMContentLoaded
        # Actually, our JS script does `mainLayout.style.display = "none"` if no sid.
        # But to prevent flicker, we can add a style to head or just let JS handle it.

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

total_processed = 0

for d, module_name in DIRS:
    search_dir = os.path.join(BASE_DIR, d)
    if not os.path.exists(search_dir):
        continue
    
    if d == "ReadingA1-C2":
        # Process the templates
        for template in ["frontend/template_reading.html", "frontend/index.html"]:
            tpath = os.path.join(search_dir, template)
            if os.path.exists(tpath):
                if process_file(tpath, module_name):
                    total_processed += 1
    elif d == "pte-listening-audios":
        # Process the template
        for template in ["template.html", "index.html"]:
            tpath = os.path.join(search_dir, template)
            if os.path.exists(tpath):
                if process_file(tpath, module_name):
                    total_processed += 1
    else:
        # Process all html files in practicepteonline
        for root, _, files in os.walk(search_dir):
            for file in files:
                if file.endswith('.html') and not "debug" in file:
                    filepath = os.path.join(root, file)
                    if process_file(filepath, module_name):
                        total_processed += 1

print(f"Injected universal login into {total_processed} files.")
