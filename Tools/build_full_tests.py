import os
import docx
from bs4 import BeautifulSoup

BASE_DIR = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"
READING_DOCX_DIR = os.path.join(BASE_DIR, "Reading_docx")
LISTENING_DOCX_DIR = os.path.join(BASE_DIR, "Listening_docx")

READING_OUT_DIR = os.path.join(BASE_DIR, "Reading_315_FullTest")
LISTENING_OUT_DIR = os.path.join(BASE_DIR, "Listening_204_FullTest")

def parse_docx_to_html(docx_path):
    try:
        doc = docx.Document(docx_path)
        html_content = ""
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                html_content += f"<p>{text}</p>\n"
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
    <style>
        body {
            margin: 0; padding: 0; font-family: 'Quicksand', sans-serif;
            background: #fdf2f8; color: #333; overflow-x: hidden;
        }
        .main-layout {
            display: flex; height: 100vh; overflow: hidden;
        }
        .passage-pane {
            flex: 6; overflow-y: auto; padding: 30px;
            background: white; margin: 10px; border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            font-size: 1.15rem; line-height: 1.8;
            padding-bottom: 100px; /* For audio player */
        }
        .answer-pane {
            flex: 4; overflow-y: auto; padding: 30px;
            background: linear-gradient(145deg, #ffffff, #fff0f5);
            margin: 10px; border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        }
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
            position: fixed; bottom: 0; left: 0; width: 60%;
            background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(5px);
            padding: 10px 20px; box-shadow: 0 -5px 20px rgba(0,0,0,0.05);
            border-top-right-radius: 20px; z-index: 1000;
        }
        audio { width: 100%; outline: none; }
        /* LOGIN OVERLAY CSS */
        {LOGIN_CSS}
    </style>
</head>
<body>
    {LOGIN_HTML}
    
    <div class="main-layout" style="display: none;">
        <div class="passage-pane">
            <h1 style="color: #ff5e7e; font-family: 'DynaPuff', cursive; margin-top: 0;">{TEST_NAME}</h1>
            {DOC_CONTENT}
        </div>
        <div class="answer-pane">
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
    
    <script>
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
        .login-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.85); z-index: 99999; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(8px); }
        .login-box { background: linear-gradient(145deg, #ffffff, #fff0f5); padding: 40px; border-radius: 30px; width: 90%; max-width: 450px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); border: 4px solid #ffccd5; }
        .login-header { font-family: 'DynaPuff', cursive; font-size: 2.2rem; color: #ff85a2; margin-bottom: 10px; text-shadow: 2px 2px 0px rgba(255,133,162,0.2); }
        .login-subheader { font-size: 1rem; color: #8c6d7d; margin-bottom: 25px; font-family: 'Quicksand', sans-serif; }
        .login-input { width: 85%; padding: 18px 25px; font-size: 1.2rem; border: 3px solid #ffccd5; border-radius: 25px; outline: none; transition: 0.3s; margin-bottom: 25px; text-align: center; color: #5c404d; background: #fffafb; font-family: 'Quicksand', sans-serif; }
        .login-input:focus { border-color: #ff85a2; box-shadow: 0 0 15px rgba(255,133,162,0.3); }
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
            <div id="login-loading-fields" style="display: none; padding: 20px 0;">
                <div id="loading-status" style="font-size: 1.15rem; font-weight: 600; margin-bottom: 15px;">Đang kết nối...</div>
            </div>
        </div>
    </div>
"""

LOGIN_JS = """
<script>
    // const APP_URL = "https://script.google.com/macros/s/AKfycbx7lOgaMcHm0ofxpG3V9bi52rMbL7wBXIzAHovP5xBrp9XbyuZp7QNKbSg2-UTJoauyOg/exec";
    const APP_URL = "https://script.google.com/macros/s/AKfycbzgBPDHt8g35pxQllRcuVTWJq5OaQnuUuQAt93yGs_kqRVOly4Wd1A_jGtgxh5MaKOJMw/exec"; // NEWEST ONE FROM USER

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
                body: JSON.stringify({ action: 'login', student_id: nickname })
            });
            let data = await loginRes.json();

            if (data.status === 'success') {
                document.getElementById('loading-status').innerText = "Thành công!";
                setTimeout(() => {
                    document.getElementById('login-overlay').style.display = "none";
                    document.querySelector('.main-layout').style.display = "flex";
                    localStorage.setItem('youpass_student_id', nickname);
                }, 500);
            } else {
                alert("Lỗi: " + data.message);
                document.getElementById('login-loading-fields').style.display = "none";
                document.getElementById('login-form-fields').style.display = "block";
            }
        } catch(err) {
            alert("Lỗi kết nối máy chủ!");
            document.getElementById('login-loading-fields').style.display = "none";
            document.getElementById('login-form-fields').style.display = "block";
        }
    }

    window.addEventListener('DOMContentLoaded', () => {
        let sid = localStorage.getItem('youpass_student_id');
        if(sid) {
            document.getElementById('login-overlay').style.display = "none";
            document.querySelector('.main-layout').style.display = "flex";
        }
    });
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

def main():
    q_html = generate_questions_html()

    # 1. READINGS
    if not os.path.exists(READING_OUT_DIR):
        os.makedirs(READING_OUT_DIR)

    if os.path.exists(READING_DOCX_DIR):
        for f in os.listdir(READING_DOCX_DIR):
            if f.endswith('.docx') and not f.startswith('~'):
                name = f.replace('.docx', '')
                doc_html = parse_docx_to_html(os.path.join(READING_DOCX_DIR, f))
                
                out_dir = os.path.join(READING_OUT_DIR, name)
                os.makedirs(out_dir, exist_ok=True)
                out_file = os.path.join(out_dir, f"{name}.html")
                
                html = HTML_TEMPLATE.replace("{MODULE_TYPE}", "Reading Full Test")
                html = html.replace("{TEST_NAME}", name)
                html = html.replace("{DOC_CONTENT}", doc_html)
                html = html.replace("{QUESTIONS_HTML}", q_html)
                html = html.replace("{LOGIN_CSS}", LOGIN_CSS)
                html = html.replace("{LOGIN_HTML}", LOGIN_HTML_TMPL.replace("{MODULE_TEXT}", "315 bài thi Reading Full Test"))
                html = html.replace("{LOGIN_JS}", LOGIN_JS)
                html = html.replace("{AUDIO_HTML}", "")
                
                with open(out_file, 'w', encoding='utf-8') as out:
                    out.write(html)
                print(f"Generated Reading: {name}")

    # 2. LISTENINGS
    if not os.path.exists(LISTENING_OUT_DIR):
        os.makedirs(LISTENING_OUT_DIR)

    if os.path.exists(LISTENING_DOCX_DIR):
        for f in os.listdir(LISTENING_DOCX_DIR):
            if f.endswith('.docx') and not f.startswith('~'):
                name = f.replace('.docx', '')
                doc_html = parse_docx_to_html(os.path.join(LISTENING_DOCX_DIR, f))
                
                out_dir = os.path.join(LISTENING_OUT_DIR, name)
                os.makedirs(out_dir, exist_ok=True)
                out_file = os.path.join(out_dir, f"{name}.html")
                
                html = HTML_TEMPLATE.replace("{MODULE_TYPE}", "Listening Full Test")
                html = html.replace("{TEST_NAME}", name)
                html = html.replace("{DOC_CONTENT}", doc_html)
                html = html.replace("{QUESTIONS_HTML}", q_html)
                html = html.replace("{LOGIN_CSS}", LOGIN_CSS)
                html = html.replace("{LOGIN_HTML}", LOGIN_HTML_TMPL.replace("{MODULE_TEXT}", "204 bài thi Listening Full Test"))
                html = html.replace("{LOGIN_JS}", LOGIN_JS)
                
                # Audio logic: usually audio_X.mp3 where X is the test number
                # Or just ../../Listening_audios/audio_X.mp3
                # Let's try to extract number from name (e.g. Test_1 -> 1)
                test_num = "".join(filter(str.isdigit, name))
                audio_path = f"../../Listening_audios/audio_{test_num}.mp3"
                audio_html = f'''<div class="audio-fixed-bottom"><audio controls src="{audio_path}"></audio></div>'''
                
                html = html.replace("{AUDIO_HTML}", audio_html)
                
                with open(out_file, 'w', encoding='utf-8') as out:
                    out.write(html)
                print(f"Generated Listening: {name}")

if __name__ == "__main__":
    main()
