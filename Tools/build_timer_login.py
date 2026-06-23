import os
import glob
import re

login_overlay_html = """
    <div class="login-overlay" id="login-overlay" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.85); z-index: 99999; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(8px);">
        <div class="login-box" style="background: linear-gradient(145deg, #ffffff, #fff0f5); padding: 40px; border-radius: 30px; width: 90%; max-width: 450px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); border: 4px solid var(--border-color, #ffccd5);">
            <div class="login-header" style="font-family: 'DynaPuff', cursive; font-size: 2rem; color: var(--accent, #ff85a2); margin-bottom: 10px; text-shadow: 2px 2px 0px rgba(255,133,162,0.2);">🍭 Study Room Login 🍭</div>
            <div class="login-subheader" style="color: var(--text-secondary, #8c6d7d); font-size: 1.1rem; margin-bottom: 25px; font-weight: 500;">Enter your lovely nickname to join the lesson! ✨</div>
            
            <div id="login-form-fields">
                <input type="text" class="login-input" id="nickname-input" placeholder="Your cute name..." style="width: 100%; padding: 15px 20px; font-size: 1.2rem; border: 3px solid var(--border-color, #ffccd5); border-radius: 15px; margin-bottom: 20px; outline: none; transition: all 0.3s;" autofocus>
                <button class="check-btn" onclick="grantAccess()" style="width: 100%; padding: 15px; font-size: 1.2rem; font-weight: bold; background: var(--success, #4ad99d); color: white; border: none; border-radius: 15px; cursor: pointer; transition: all 0.2s;">LET'S GO! 🌸</button>
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
                            ⚠️ <b>LƯU Ý:</b> Phiên đăng nhập luyện tập này của bạn đã được Giáo viên thanh toán <b>5.000đ/lượt</b>. Sau 3 lượt (tối đa 15.000đ) thì các lượt làm bài khác của bạn được MIỄN PHÍ.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
"""

welcome_banner_html = """
    <!-- Welcome Celebration Portal -->
    <div class="welcome-banner" id="welcome-banner" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(255,255,255,0.9); z-index: 99998; display: none; align-items: center; justify-content: center; flex-direction: column;">
        <canvas id="fireworks-canvas" style="position: absolute; top:0; left:0; width:100%; height:100%; pointer-events: none;"></canvas>
        <div class="welcome-text" style="font-family: 'DynaPuff', cursive; font-size: 3rem; color: var(--accent, #ff85a2); text-shadow: 2px 2px 0px rgba(0,0,0,0.1);">🦄 ACCESS GRANTED! 🦄</div>
        <div class="welcome-name" id="welcome-user-name" style="font-size: 1.5rem; color: #333; margin-top: 20px; font-weight: bold;">Welcome, Student! ✨</div>
    </div>
"""

js_logic = """
<script>
    function playSfx(id) {
        let el = document.getElementById(id);
        if(el) {
            el.currentTime = 0;
            el.play().catch(e=>console.log(e));
        }
    }
    function grantAccess() {
        const input = document.getElementById('nickname-input');
        let nickname = input.value ? input.value.trim() : '';
        if (!nickname) {
            alert("Please enter your student code! 🌸");
            return;
        }
        playSfx('sfx-click');
        
        document.getElementById('login-form-fields').style.display = "none";
        document.getElementById('login-loading-fields').style.display = "block";
        document.getElementById('payment-nickname-badge').innerText = nickname;
        
        const progressFill = document.getElementById('progress-bar-fill');
        const statusText = document.getElementById('loading-status');
        
        let progress = 0;
        let interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 100) progress = 100;
            progressFill.style.width = progress + '%';
            
            if (progress > 30 && progress < 70) {
                statusText.innerText = "Đang kiểm tra thanh toán...";
            } else if (progress >= 70 && progress < 100) {
                statusText.innerText = "Xác nhận thành công! Chuẩn bị phòng học...";
            }
            
            if (progress === 100) {
                clearInterval(interval);
                setTimeout(() => {
                    document.getElementById('login-overlay').style.display = "none";
                    document.getElementById('welcome-banner').style.display = "flex";
                    document.getElementById('welcome-user-name').innerText = "Chào mừng, " + nickname + "! ✨";
                    playSfx('sfx-success');
                    
                    if(document.getElementById('main-header')) document.getElementById('main-header').style.display = "flex";
                    localStorage.setItem('youpass_student_id', nickname);
                    
                    setTimeout(() => {
                        document.getElementById('welcome-banner').style.opacity = '0';
                        setTimeout(() => {
                            document.getElementById('welcome-banner').style.display = "none";
                            // START TIMER
                            if(typeof startTimer === 'function') startTimer();
                        }, 500);
                    }, 2000);
                }, 500);
            }
        }, 300);
    }
    
    // Auto-login logic
    window.addEventListener('DOMContentLoaded', () => {
        let sid = localStorage.getItem('youpass_student_id');
        if(sid) {
            let inp = document.getElementById('nickname-input');
            if(inp) inp.value = sid;
            document.getElementById('login-overlay').style.display = "none";
            if(document.getElementById('main-header')) document.getElementById('main-header').style.display = "flex";
            if(typeof startTimer === 'function') startTimer();
        }
    });
</script>
"""

with open('build_timer_login.py', 'w') as f:
    f.write("print('Script written')")
