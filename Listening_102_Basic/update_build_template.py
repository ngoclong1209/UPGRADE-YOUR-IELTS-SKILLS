import sys

with open('build_template.py', 'r') as f:
    content = f.read()

# Add Modal CSS
css_insert = """
        #student-modal {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.5); backdrop-filter: blur(5px);
            display: flex; align-items: center; justify-content: center;
            z-index: 9999;
        }
        .modal-content {
            background: #fff; padding: 2rem; border-radius: 20px;
            text-align: center; font-family: 'Fredoka', sans-serif;
            max-width: 400px; width: 90%;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .modal-content input {
            width: 80%; padding: 10px; margin: 15px 0;
            border: 2px solid var(--border-color); border-radius: 10px;
            font-size: 1.1rem; text-align: center;
        }
        .modal-content button {
            background: var(--accent); color: white; border: none;
            padding: 10px 25px; border-radius: 10px; font-size: 1.1rem;
            cursor: pointer; transition: background 0.2s;
        }
        .modal-content button:hover { background: var(--accent-hover); }
"""
content = content.replace('</style>', css_insert + '\n    </style>')

# Add Modal HTML
html_insert = """
    <div id="student-modal" style="display: none;">
        <div class="modal-content">
            <h2>👋 Xin chào!</h2>
            <p>Vui lòng nhập Tên hoặc Mã Học Viên của bạn để hệ thống lưu điểm nhé:</p>
            <input type="text" id="student-name-input" placeholder="Tên của bạn...">
            <br>
            <button onclick="saveStudentId()">Bắt đầu làm bài</button>
        </div>
    </div>
"""
content = content.replace('<body>', '<body>\n' + html_insert)

# Add JS tracking logic
js_insert = """
        const WEB_APP_URL = "YOUR_GOOGLE_APP_SCRIPT_WEB_APP_URL_HERE";

        // Student Auth Logic
        document.addEventListener('DOMContentLoaded', () => {
            const studentId = localStorage.getItem('student_id');
            const placeholder = document.getElementById('user-banner-placeholder');
            if (!studentId) {
                document.getElementById('student-modal').style.display = 'flex';
            } else {
                if(placeholder) placeholder.innerHTML = `<span style="background:var(--accent);color:#fff;padding:5px 15px;border-radius:20px;font-size:0.9rem;font-weight:bold;">👤 ${studentId} <a href="#" onclick="logout()" style="color:#fff;margin-left:10px;font-size:0.8rem;text-decoration:underline;">Đổi</a></span>`;
            }
        });

        function saveStudentId() {
            const name = document.getElementById('student-name-input').value.trim();
            if (name) {
                localStorage.setItem('student_id', name);
                document.getElementById('student-modal').style.display = 'none';
                location.reload();
            } else {
                alert("Bạn cần nhập tên để lưu điểm!");
            }
        }
        function logout() {
            localStorage.removeItem('student_id');
            location.reload();
        }

        function sendScoreToGoogle(score, total) {
            if (WEB_APP_URL === "YOUR_GOOGLE_APP_SCRIPT_WEB_APP_URL_HERE") return;
            const studentId = localStorage.getItem('student_id') || "Unknown";
            const pathParts = window.location.pathname.split('/');
            // Expects path like Basic/Lesson_1/index.html -> Basic_Lesson_1
            let lessonId = "Unknown_Lesson";
            if(pathParts.length >= 3) {
                lessonId = pathParts[pathParts.length - 3] + "_" + pathParts[pathParts.length - 2];
            }

            const payload = {
                userId: studentId,
                lessonId: lessonId,
                score: score + "/" + total,
                percent: Math.round((score / total) * 100)
            };

            fetch(WEB_APP_URL, {
                method: "POST",
                mode: "no-cors",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            }).catch(e => console.log("Tracking error", e));
        }
"""
content = content.replace('<script>', '<script>\n' + js_insert)

# Inject sendScoreToGoogle into grading logic inside build_template.py
# We will inject it inside the `if (isPerfect)` block and `if (isFinalAttempt)` blocks.
content = content.replace("document.getElementById('sfx-win').play().catch(e=>{});", "document.getElementById('sfx-win').play().catch(e=>{});\\n                sendScoreToGoogle(score, total);")
content = content.replace("document.getElementById('sfx-wrong').play().catch(e=>{});\\n                    unlockTranscript();", "document.getElementById('sfx-wrong').play().catch(e=>{});\\n                    sendScoreToGoogle(score, total);\\n                    unlockTranscript();")


with open('build_template.py', 'w') as f:
    f.write(content)

print("build_template.py updated successfully!")
