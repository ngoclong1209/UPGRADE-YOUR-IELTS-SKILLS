import os
import glob
from bs4 import BeautifulSoup

LOGIN_CSS = """
    <style>
        /* [COPYING CSS FROM build_full_tests.py] */
        .login-overlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: rgba(0, 0, 0, 0.85); background-size: cover; background-position: center;
            display: flex; justify-content: center; align-items: center; z-index: 9999;
            backdrop-filter: blur(8px);
        }
        .login-box {
            background: rgba(255, 255, 255, 0.95); padding: 50px 40px; border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2); text-align: center; max-width: 450px; width: 90%;
            border: 2px solid #ffb6c1; position: relative; overflow: hidden;
        }
        .login-header {
            font-family: 'DynaPuff', cursive; font-size: 2.5rem; color: #ff5e7e;
            margin-bottom: 10px; text-shadow: 2px 2px 0px #ffe4e1;
        }
        .login-subheader { font-size: 1.1rem; color: #555; margin-bottom: 30px; font-weight: 500; }
        .login-input {
            width: 100%; padding: 15px; border: 2px solid #ffb6c1; border-radius: 12px;
            font-size: 1.1rem; margin-bottom: 25px; outline: none; transition: all 0.3s ease;
            text-align: center; box-sizing: border-box; font-family: 'Quicksand', sans-serif;
            font-weight: bold; color: #333;
        }
        .login-input:focus { border-color: #ff5e7e; box-shadow: 0 0 10px rgba(255, 94, 126, 0.3); }
        .submit-btn {
            background: linear-gradient(135deg, #ff85a2 0%, #ff5e7e 100%);
            color: white; border: none; padding: 15px 30px; font-size: 1.3rem;
            border-radius: 30px; cursor: pointer; font-family: 'DynaPuff', cursive;
            transition: all 0.3s ease; width: 100%; box-shadow: 0 5px 15px rgba(255, 94, 126, 0.4);
        }
        .submit-btn:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(255, 94, 126, 0.6); }
        .progress-container {
            width: 100%; background: #f0f0f0; border-radius: 10px;
            overflow: hidden; margin-top: 15px; display: none; height: 20px;
        }
        .progress-bar {
            height: 100%; background: linear-gradient(135deg, #ff85a2 0%, #ff5e7e 100%);
            width: 0%; transition: width 2s ease-in-out;
        }
        .payment-message {
            color: #d6336c; font-weight: bold; font-size: 1.1rem; 
            margin-top: 20px; display: none; line-height: 1.5;
        }
    </style>
"""

LOGIN_HTML_TMPL = """
    <div class="login-overlay" id="login-overlay">
        <div class="login-box">
            <div class="login-header">🍭 Study Room 🍭</div>
            <div class="login-subheader">Hệ thống: {MODULE_TEXT} ✨</div>
            <div id="login-form-fields">
                <input type="text" class="login-input" id="nickname-input" placeholder="Nhập ID học viên..." autofocus>
                <button class="submit-btn" onclick="grantAccess()">LET'S GO! 🌸</button>
            </div>
            
            <div id="login-loading-fields" style="display: none; padding: 10px 0;">
                <div id="loading-status" style="font-size: 1.15rem; font-weight: 600; color: #ff5e7e;">Đang kiểm tra ID...</div>
                <div class="payment-message" id="payment-message">
                    Khoá học của bạn có giá 1,599,000 VND đã được thanh toán bởi VŨ NGỌC LONG.
                </div>
                <div class="progress-container" id="progress-container">
                    <div class="progress-bar" id="progress-bar"></div>
                </div>
            </div>
        </div>
    </div>
"""

LOGIN_JS = """

    const APP_URL = "https://script.google.com/macros/s/AKfycbwK8uWktQHrSoCVdiBzqAZj0SsT5_FxxCksG2s0Iga-Ye1DF40l7h5-xgI_7Kk40YLn/exec";
    
    const backgrounds = [
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1920&q=80",
        "https://images.unsplash.com/photo-1490730141103-6cac27aaab94?auto=format&fit=crop&w=1920&q=80",
        "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?auto=format&fit=crop&w=1920&q=80",
        "https://images.unsplash.com/photo-1518655048521-f130df041f66?auto=format&fit=crop&w=1920&q=80",
        "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1920&q=80",
        "https://images.unsplash.com/photo-1506744626753-140081bb41cd?auto=format&fit=crop&w=1920&q=80",
        "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?auto=format&fit=crop&w=1920&q=80",
        "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1920&q=80",
        "https://images.unsplash.com/photo-1470071131384-001b85755536?auto=format&fit=crop&w=1920&q=80",
        "https://images.unsplash.com/photo-1458668383970-8ddd3927dded?auto=format&fit=crop&w=1920&q=80"
    ];

    function getDeviceId() {
        let id = localStorage.getItem('youpass_device_id');
        if (!id) {
            id = 'device_' + Math.random().toString(36).substr(2, 9) + Date.now();
            localStorage.setItem('youpass_device_id', id);
        }
        return id;
    }

    window.addEventListener('DOMContentLoaded', () => {
        let sid = localStorage.getItem('youpass_student_id');
        let mainLayout = document.querySelector('.main-layout') || document.querySelector('.container') || document.body.firstElementChild;
        let overlay = document.getElementById('login-overlay');
        
        // Hide main content initially
        if(mainLayout && mainLayout.id !== 'login-overlay') {
            if (mainLayout.style) {
                mainLayout.setAttribute('data-original-display', mainLayout.style.display || 'block');
                mainLayout.style.display = 'none';
            }
        }
        
        if(sid) {
            let nickInput = document.getElementById('nickname-input');
            if(nickInput) nickInput.value = sid;
        }
        
        let randomBg = backgrounds[Math.floor(Math.random() * backgrounds.length)];
        if(overlay) overlay.style.backgroundImage = `url(${randomBg})`;
    });

    async function grantAccess() {
        const input = document.getElementById('nickname-input');
        let nickname = input ? input.value.trim().toUpperCase() : '';
        if (!nickname) { alert("Vui lòng nhập ID!"); return; }
        
        document.getElementById('login-form-fields').style.display = "none";
        document.getElementById('login-loading-fields').style.display = "block";
        document.getElementById('loading-status').innerText = "Đang kiểm tra ID...";

        try {
            let loginRes = await fetch(APP_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'text/plain;charset=utf-8' },
                body: JSON.stringify({ action: 'login', student_id: nickname, device_id: getDeviceId() })
            });
            let data = await loginRes.json();

            if (data.status === 'success') {
                localStorage.setItem('youpass_student_id', nickname);
                
                document.getElementById('loading-status').style.display = "none";
                document.getElementById('payment-message').style.display = "block";
                document.getElementById('progress-container').style.display = "block";
                
                setTimeout(() => {
                    document.getElementById('progress-bar').style.width = "100%";
                }, 100);
                
                setTimeout(() => {
                    document.getElementById('login-overlay').style.display = "none";
                    let mainLayout = document.querySelector('.main-layout') || document.querySelector('.container') || document.body.firstElementChild;
                    if(mainLayout && mainLayout.id !== 'login-overlay') {
                        mainLayout.style.display = mainLayout.getAttribute('data-original-display') || '';
                    }
                }, 2200);
                
            } else {
                alert("Lỗi: " + data.message);
                document.getElementById('login-loading-fields').style.display = "none";
                document.getElementById('login-form-fields').style.display = "block";
            }
        } catch(err) {
            alert("Lỗi kết nối máy chủ! Có thể Apps Script chưa được cấp quyền 'Anyone' (Bất kỳ ai). Vui lòng báo Admin.");
            console.error("Fetch error:", err);
            document.getElementById('login-loading-fields').style.display = "none";
            document.getElementById('login-form-fields').style.display = "block";
        }
    }
"""

def inject_to_file(filepath, module_text):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Clean up old overlays and scripts
    for old_overlay in soup.find_all('div', id='login-overlay'):
        old_overlay.decompose()
    for old_overlay in soup.find_all('div', class_='login-overlay'):
        old_overlay.decompose()
    for old_modal in soup.find_all('div', id='student-modal'):
        old_modal.decompose()

    for script in soup.find_all('script'):
        if script.string:
            if 'const APP_URL' in script.string or 'function grantAccess' in script.string or 'youpass_student_id' in script.string or 'login-overlay' in script.string:
                script.decompose()

    # 2. Add Google Fonts
    head = soup.find('head')
    if head:
        if not soup.find('link', href=lambda x: x and 'DynaPuff' in x):
            head.append(soup.new_tag('link', href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300..700&family=DynaPuff:wght@400..700&family=Quicksand:wght@300..700&display=swap", rel="stylesheet"))
        
        # Inject CSS
        css_soup = BeautifulSoup(LOGIN_CSS, 'html.parser')
        head.append(css_soup)

    # 3. Inject HTML and JS
    body = soup.find('body')
    if body:
        # Prevent double injection
        if not body.find('div', id='login-overlay'):
            overlay_soup = BeautifulSoup(LOGIN_HTML_TMPL.replace("{MODULE_TEXT}", module_text), 'html.parser')
            body.insert(0, overlay_soup)

            js_script_tag = soup.new_tag('script')
            js_script_tag.string = LOGIN_JS
            body.append(js_script_tag)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    return True

def process_directory(base_dir, module_text):
    count = 0
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html') and not "debug" in file:
                filepath = os.path.join(root, file)
                if inject_to_file(filepath, module_text):
                    count += 1
    return count

if __name__ == "__main__":
    c1 = process_directory("Reading_1232_Basic", "1232 bài thi Reading Basic")
    print(f"Injected into {c1} Reading Basic files.")
    
    c2 = process_directory("Listening_102_Basic", "102 bài thi Listening Basic")
    print(f"Injected into {c2} Listening Basic files.")
