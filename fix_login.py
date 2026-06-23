import re

def update_file(filename, is_script_tag_wrapped=False):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    new_js = """
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
    if is_script_tag_wrapped:
        new_js = f"<script>\n{new_js}</script>\n"

    # In Tools/build_full_tests.py, it's defined as LOGIN_JS = """\n<script>...</script>\n"""
    # In Tools/inject_basic_login.py, it's defined as LOGIN_JS = """\nconst APP_URL..."""
    
    if "LOGIN_JS = " in content:
        import ast
        # regex replacement
        pattern = re.compile(r'LOGIN_JS\s*=\s*\"\"\"(.*?)\"\"\"', re.DOTALL)
        content = pattern.sub(f'LOGIN_JS = """\n{new_js}"""', content)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename}")

update_file('Tools/build_full_tests.py', True)
update_file('Tools/inject_basic_login.py', False)
