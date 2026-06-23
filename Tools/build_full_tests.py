import os
import glob
import docx

BASE_DIR = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"
READING_OUT_DIR = os.path.join(BASE_DIR, "Reading_315_FullTest")
LISTENING_OUT_DIR = os.path.join(BASE_DIR, "Listening_204_FullTest")

def parse_docx_to_html(docx_path, module_type):
    try:
        doc = docx.Document(docx_path)
        html_content = ""
        letter_index = 0
        in_questions = False
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
                
            if text.lower().startswith("question"):
                in_questions = True
                
            p_html = ""
            for run in para.runs:
                run_text = run.text.replace("<", "&lt;").replace(">", "&gt;")
                if not run_text: continue
                if run.bold: run_text = f"<strong>{run_text}</strong>"
                if run.italic: run_text = f"<em>{run_text}</em>"
                if run.underline: run_text = f"<u>{run_text}</u>"
                p_html += run_text
                
            p_html = p_html.strip()
            
            if len(text) < 100 and not text.endswith('.') and not in_questions and "<strong>" in p_html:
                html_content += f'<h3 class="test-heading">{p_html}</h3>\n'
            else:
                if module_type == "Reading Full Test" and not in_questions and len(text) > 100:
                    letter = chr(65 + letter_index)
                    html_content += f'<div class="para-row"><div class="para-label">{letter}</div><div class="para-text"><p>{p_html}</p></div></div>\n'
                    letter_index += 1
                else:
                    html_content += f"<p>{p_html}</p>\n"
        return html_content
    except Exception as e:
        print(f"Error reading docx {docx_path}: {e}")
        return "<p>Nội dung đang được cập nhật...</p>"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{MODULE_TYPE} - {TEST_NAME}</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300..700&family=DynaPuff:wght@400..700&family=Quicksand:wght@300..700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../Assets/highlighter.css">
    <style>
        body {
            margin: 0; padding: 0; font-family: 'Quicksand', sans-serif;
            background: #fdf2f8; color: #333; overflow: hidden; height: 100vh;
        }
        .main-layout {
            display: flex; height: 100vh; width: 100vw;
        }
        .passage-pane {
            flex: 0 0 60%; overflow-y: auto; padding: 30px;
            background: white; border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            font-size: 1.15rem; line-height: 1.8;
            padding-bottom: 100px;
            margin: 10px 0 10px 10px;
        }
        .resizer {
            flex: 0 0 10px;
            cursor: col-resize;
            background: rgba(255,133,162,0.1);
            display: flex; align-items: center; justify-content: center;
            transition: background 0.3s;
        }
        .resizer:hover { background: rgba(255,133,162,0.5); }
        .resizer::after { content: '⋮'; color: #ff85a2; font-size: 20px; }
        .answer-pane {
            flex: 1 1 0%; overflow-y: auto; padding: 30px;
            background: linear-gradient(145deg, #ffffff, #fff0f5);
            margin: 10px 10px 10px 0; border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            padding-bottom: 100px;
        }
        
        /* New Typography and Formatting Styles */
        .test-heading {
            color: #ff5e7e; font-family: 'Fredoka', sans-serif;
            margin-top: 30px; margin-bottom: 15px; text-transform: uppercase;
        }
        .para-row {
            display: flex; align-items: flex-start; margin-bottom: 20px;
            background: #fffafb; padding: 15px; border-radius: 12px;
            border-left: 4px solid #ffccd5; transition: all 0.3s ease;
        }
        .para-row:hover { border-left-color: #ff5e7e; background: #fff5f7; }
        .para-label {
            background: #ff85a2; color: white; width: 35px; height: 35px;
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-weight: bold; flex-shrink: 0; margin-right: 15px; font-family: 'Fredoka', sans-serif;
        }
        .para-text p { margin: 0; }
        strong { color: #d6336c; }
        u { text-decoration-color: #ff85a2; }
        
        .q-row {
            display: flex; align-items: center; margin-bottom: 15px;
            background: white; padding: 10px 15px; border-radius: 12px;
            border: 2px solid #ffccd5;
        }
        .q-num {
            font-weight: bold; color: #ff85a2; font-size: 1.2rem;
            width: 40px;
        }
        .q-input {
            flex: 1; border: none; outline: none; font-size: 1.1rem;
            font-family: 'Quicksand', sans-serif;
            border-bottom: 2px dashed #ffccd5; background: transparent;
            padding: 5px;
        }
        .q-input:focus { border-bottom: 2px solid #ff85a2; }
        .submit-btn {
            width: 100%; padding: 18px; font-size: 1.2rem; color: white;
            background: linear-gradient(135deg, #ff85a2 0%, #ff5e7e 100%);
            border: none; border-radius: 25px; cursor: pointer; font-weight: 700;
            margin-top: 20px; box-shadow: 0 10px 20px rgba(255,94,126,0.3);
            font-family: 'Quicksand', sans-serif;
        }
        .audio-fixed-bottom {
            position: fixed; bottom: 0; left: 0; width: 100%;
            background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(5px);
            padding: 10px 20px; box-shadow: 0 -5px 20px rgba(0,0,0,0.05);
            border-top-right-radius: 20px; border-top-left-radius: 20px; z-index: 1000;
        }
        .audio-warning {
            color: #d6336c; font-weight: bold; text-align: center;
            padding: 10px; border-radius: 10px; background: #fff0f5;
            font-family: 'Quicksand', sans-serif;
        }
        audio { width: 100%; max-width: 800px; display: block; margin: 0 auto; outline: none; }
        
        {LOGIN_CSS}
    </style>
</head>
<body>
    {LOGIN_HTML}
    
    <div class="main-layout" style="display: none;">
        <div class="passage-pane" id="left-pane">
            <h1 style="color: #ff5e7e; font-family: 'DynaPuff', cursive; margin-top: 0;">{TEST_NAME}</h1>
            {DOC_CONTENT}
        </div>
        <div class="resizer" id="resizer"></div>
        <div class="answer-pane" id="right-pane">
            <h2 style="color: #ff5e7e; font-family: 'DynaPuff', cursive; margin-top: 0; text-align: center;">Answers (40 Questions)</h2>
            <div id="questions-container">
                {QUESTIONS_HTML}
            </div>
            <button class="submit-btn" id="btn-submit">SUBMIT ANSWERS 🌸</button>
            <div id="result-msg" style="text-align: center; margin-top: 15px; font-weight: bold; color: #2b9348; display: none;"></div>
        </div>
    </div>

    {AUDIO_HTML}

    {LOGIN_JS}
    <script src="../../Assets/highlighter.js"></script>
    <script>
        // Resizer Logic
        const resizer = document.getElementById('resizer');
        const leftPane = document.getElementById('left-pane');
        const rightPane = document.getElementById('right-pane');
        let isResizing = false;

        resizer.addEventListener('mousedown', (e) => {
            isResizing = true;
            document.body.style.cursor = 'col-resize';
            leftPane.style.pointerEvents = 'none';
            rightPane.style.pointerEvents = 'none';
        });

        document.addEventListener('mousemove', (e) => {
            if (!isResizing) return;
            let containerWidth = document.querySelector('.main-layout').offsetWidth;
            let newLeftWidth = (e.clientX / containerWidth) * 100;
            if (newLeftWidth > 20 && newLeftWidth < 80) {
                leftPane.style.flex = `0 0 ${newLeftWidth}%`;
                rightPane.style.flex = `1 1 0%`;
            }
        });

        document.addEventListener('mouseup', () => {
            if (isResizing) {
                isResizing = false;
                document.body.style.cursor = 'default';
                leftPane.style.pointerEvents = 'auto';
                rightPane.style.pointerEvents = 'auto';
            }
        });

        resizer.addEventListener('touchstart', (e) => {
            isResizing = true;
            leftPane.style.pointerEvents = 'none';
            rightPane.style.pointerEvents = 'none';
        });

        document.addEventListener('touchmove', (e) => {
            if (!isResizing) return;
            let touch = e.touches[0];
            let containerWidth = document.querySelector('.main-layout').offsetWidth;
            let newLeftWidth = (touch.clientX / containerWidth) * 100;
            if (newLeftWidth > 20 && newLeftWidth < 80) {
                leftPane.style.flex = `0 0 ${newLeftWidth}%`;
                rightPane.style.flex = `1 1 0%`;
            }
        });

        document.addEventListener('touchend', () => {
            if (isResizing) {
                isResizing = false;
                leftPane.style.pointerEvents = 'auto';
                rightPane.style.pointerEvents = 'auto';
            }
        });

        // Submit Logic
        document.getElementById('btn-submit').addEventListener('click', async () => {
            let btn = document.getElementById('btn-submit');
            let resultMsg = document.getElementById('result-msg');
            btn.innerText = "Submitting...";
            btn.disabled = true;

            let answers = [];
            for (let i = 1; i <= 40; i++) {
                let val = document.getElementById('q' + i).value.trim();
                answers.push(val);
            }

            let payload = {
                action: 'submit_full_test',
                student_id: localStorage.getItem('youpass_student_id') || 'UNKNOWN',
                module: '{MODULE_TYPE}',
                test_name: '{TEST_NAME}',
                answers: answers
            };

            try {
                let res = await fetch(APP_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
                    body: JSON.stringify(payload)
                });
                let data = await res.json();
                if (data.status === 'success') {
                    resultMsg.innerText = "✅ Đáp án của bạn đã được ghi nhận!";
                    resultMsg.style.display = 'block';
                    btn.innerText = "SUBMITTED!";
                } else {
                    alert("Lỗi: " + data.message);
                    btn.innerText = "SUBMIT ANSWERS 🌸";
                    btn.disabled = false;
                }
            } catch(e) {
                alert("Lỗi mạng! Không thể gửi.");
                btn.innerText = "SUBMIT ANSWERS 🌸";
                btn.disabled = false;
            }
        });
    </script>
</body>
</html>
"""

LOGIN_CSS = """
        .login-overlay { 
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
            background-size: cover; background-position: center; 
            z-index: 99999; display: flex; align-items: center; justify-content: center; 
        }
        .login-overlay::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.5); backdrop-filter: blur(8px); z-index: -1;
        }
        .login-box { 
            background: rgba(255, 255, 255, 0.95); padding: 40px; border-radius: 30px; 
            width: 90%; max-width: 450px; text-align: center; 
            box-shadow: 0 20px 50px rgba(0,0,0,0.3); border: 4px solid #ffccd5; 
            backdrop-filter: blur(10px);
        }
        .login-header { font-family: 'DynaPuff', cursive; font-size: 2.2rem; color: #ff85a2; margin-bottom: 10px; text-shadow: 2px 2px 0px rgba(255,133,162,0.2); }
        .login-subheader { font-size: 1rem; color: #8c6d7d; margin-bottom: 25px; font-family: 'Quicksand', sans-serif; }
        .login-input { width: 85%; padding: 18px 25px; font-size: 1.2rem; border: 3px solid #ffccd5; border-radius: 25px; outline: none; transition: 0.3s; margin-bottom: 25px; text-align: center; color: #5c404d; background: #fffafb; font-family: 'Quicksand', sans-serif; }
        .login-input:focus { border-color: #ff85a2; box-shadow: 0 0 15px rgba(255,133,162,0.3); }
        
        .progress-container {
            width: 100%; background-color: #f3f3f3; border-radius: 20px; 
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
<script>

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
                // If the layout was natively display:none in HTML, we shouldn't save 'none' as original.
                // We default it to 'flex' for main-layout and 'block' for others.
                let orig = mainLayout.style.display;
                if (orig === 'none' || orig === '') {
                    orig = mainLayout.classList.contains('main-layout') ? 'flex' : 'block';
                }
                mainLayout.setAttribute('data-original-display', orig);
                mainLayout.style.display = 'none';
            }
        }
        
        if(sid) {
            let nickInput = document.getElementById('nickname-input');
            if(nickInput) nickInput.value = sid;
        }
        
        let randomBg = backgrounds[Math.floor(Math.random() * backgrounds.length)];
        if(overlay) overlay.style.backgroundImage = `url(${randomBg})`;
        
        // Auto-focus logic
        let nickInput = document.getElementById('nickname-input');
        if(nickInput) nickInput.focus();
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
                        let targetDisplay = mainLayout.getAttribute('data-original-display') || 'block';
                        if(targetDisplay === 'none') {
                            targetDisplay = mainLayout.classList.contains('main-layout') ? 'flex' : 'block';
                        }
                        mainLayout.style.display = targetDisplay;
                    }
                    
                    // Show audio container if hidden
                    let audioContainer = document.querySelector('.audio-fixed-bottom');
                    if (audioContainer) audioContainer.style.display = 'block';
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
</script>
"""

def generate_questions_html():
    h = ""
    for i in range(1, 41):
        h += f'''
        <div class="q-row">
            <div class="q-num">{i}</div>
            <input type="text" class="q-input" id="q{i}" placeholder="Type answer...">
        </div>
        '''
    return h

def build_tests(base_dir, module_type, module_text):
    q_html = generate_questions_html()
    
    docx_files = glob.glob(os.path.join(base_dir, "**", "*.docx"), recursive=True)
    
    for docx_path in docx_files:
        if os.path.basename(docx_path).startswith('~'): continue
        
        name = os.path.basename(docx_path).replace('.docx', '')
        print(f"Building {name} from {docx_path}...")
        
        doc_html = parse_docx_to_html(docx_path, module_type)
        
        out_dir = os.path.dirname(docx_path)
        out_file = os.path.join(out_dir, f"{name}.html")
        
        html = HTML_TEMPLATE.replace("{MODULE_TYPE}", module_type)
        html = html.replace("{TEST_NAME}", name)
        html = html.replace("{DOC_CONTENT}", doc_html)
        html = html.replace("{QUESTIONS_HTML}", q_html)
        html = html.replace("{LOGIN_CSS}", LOGIN_CSS)
        html = html.replace("{LOGIN_HTML}", LOGIN_HTML_TMPL.replace("{MODULE_TEXT}", module_text))
        html = html.replace("{LOGIN_JS}", LOGIN_JS)
        
        if module_type == "Listening Full Test":
            test_num = "".join(filter(str.isdigit, name))
            audio_path_local = os.path.join(out_dir, f"audio_{test_num}.mp3")
            if os.path.exists(audio_path_local):
                audio_src = f"audio_{test_num}.mp3"
                audio_html = f'''<div class="audio-fixed-bottom"><audio controls src="{audio_src}"></audio></div>'''
            else:
                audio_html = f'''<div class="audio-fixed-bottom"><div class="audio-warning">⚠️ Audio file (audio_{test_num}.mp3) is missing. Vui lòng tải file âm thanh lên thư mục này.</div></div>'''
                
            html = html.replace("{AUDIO_HTML}", audio_html)
        else:
            html = html.replace("{AUDIO_HTML}", "")
            
        with open(out_file, 'w', encoding='utf-8') as out:
            out.write(html)

def main():
    if os.path.exists(READING_OUT_DIR):
        print(f"--- BUILDING READING 315 FULL TESTS ---")
        build_tests(READING_OUT_DIR, "Reading Full Test", "315 bài thi Reading Full Test")
    
    if os.path.exists(LISTENING_OUT_DIR):
        print(f"--- BUILDING LISTENING 204 FULL TESTS ---")
        build_tests(LISTENING_OUT_DIR, "Listening Full Test", "204 bài thi Listening Full Test")

if __name__ == "__main__":
    main()
