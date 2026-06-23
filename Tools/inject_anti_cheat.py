import os
import glob

base_dir = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"

anti_cheat_js = """
    // --- ANTI-CHEAT & LOGIN LOGIC ---
    const APP_URL = "https://script.google.com/macros/s/AKfycbwW2sbPGFnGUG5Q7nVPTq3bqfC3kreSQJ5j7j_O2qzSu6e20sMDWlBvHkgwtMV4R-TG2Q/exec";

    function getDeviceId() {
        let did = localStorage.getItem('youpass_device_id');
        if(!did) {
            let fp = btoa(navigator.userAgent + screen.width + screen.height + navigator.language).substring(0, 15);
            did = fp + '_' + Math.random().toString(36).substr(2, 5);
            localStorage.setItem('youpass_device_id', did);
        }
        return did;
    }

    async function grantAccess() {
        const input = document.getElementById('nickname-input');
        let nickname = input ? input.value.trim().toUpperCase() : '';
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
        
        let deviceId = getDeviceId();
        
        // Bắt đầu thanh progress
        let progress = 10;
        if(progressFill) progressFill.style.width = progress + '%';
        if(statusText) statusText.innerText = "Đang kiểm tra thiết bị & IP...";

        try {
            // Lấy IP
            let ipData = {};
            try {
                let ipRes = await fetch('https://api.ipify.org?format=json');
                ipData = await ipRes.json();
            } catch(e) { console.log("IP fetch failed", e); }
            
            progress = 40;
            if(progressFill) progressFill.style.width = progress + '%';
            if(statusText) statusText.innerText = "Đang xác thực tài khoản...";

            // Gửi request lên server
            let loginRes = await fetch(APP_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'text/plain;charset=utf-8' },
                body: JSON.stringify({
                    action: 'login',
                    student_id: nickname,
                    device_id: deviceId,
                    ip: ipData.ip || 'unknown'
                })
            });
            
            let data = await loginRes.json();
            progress = 100;
            if(progressFill) progressFill.style.width = progress + '%';

            if (data.status === 'success') {
                if(statusText) statusText.innerText = "Xác nhận thành công! Chuẩn bị phòng học...";
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
            } else {
                // Thất bại
                if(statusText) statusText.innerText = "LỖI: " + data.message;
                if(statusText) statusText.style.color = "red";
                alert(data.message);
                // Quay lại form
                setTimeout(() => {
                    if(loadFields) loadFields.style.display = "none";
                    if(formFields) formFields.style.display = "block";
                    if(progressFill) progressFill.style.width = '0%';
                }, 2000);
            }
            
        } catch(err) {
            console.error(err);
            alert("Lỗi kết nối máy chủ! Vui lòng thử lại.");
            if(loadFields) loadFields.style.display = "none";
            if(formFields) formFields.style.display = "block";
        }
    }
"""

def inject_anti_cheat(html):
    # Find the block from `function grantAccess() {` up to `// Auto check login`
    import re
    # We replace the old grantAccess logic with the new async one
    pattern = re.compile(r'function grantAccess\(\)\s*\{.*?// Auto check login', re.DOTALL)
    
    if pattern.search(html):
        html = pattern.sub(anti_cheat_js + "\n    // Auto check login", html)
    
    return html

reading_tpl = os.path.join(base_dir, 'ReadingA1-C2/frontend/template_reading.html')
if os.path.exists(reading_tpl):
    with open(reading_tpl, 'r', encoding='utf-8') as f:
        html = f.read()
    html = inject_anti_cheat(html)
    with open(reading_tpl, 'w', encoding='utf-8') as f:
        f.write(html)

listening_tpl = os.path.join(base_dir, 'pte-listening-audios/template.html')
if os.path.exists(listening_tpl):
    with open(listening_tpl, 'r', encoding='utf-8') as f:
        html = f.read()
    html = inject_anti_cheat(html)
    with open(listening_tpl, 'w', encoding='utf-8') as f:
        f.write(html)

for file_path in glob.glob(os.path.join(base_dir, 'data/practicepteonline/reading/**/*.html'), recursive=True):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    html = inject_anti_cheat(html)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

for file_path in glob.glob(os.path.join(base_dir, 'data/practicepteonline/listening/**/*.html'), recursive=True):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    html = inject_anti_cheat(html)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

print("Injected Anti-Cheat Logic")
