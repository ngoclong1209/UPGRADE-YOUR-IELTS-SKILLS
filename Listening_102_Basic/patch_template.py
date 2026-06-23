with open('template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Hide main layout initially
content = content.replace('<div class="main-layout">', '<div class="main-layout" id="main-layout" style="display: none;">')

# 2. Update the javascript
js_replacement = """
        document.addEventListener('DOMContentLoaded', () => {
            const studentId = localStorage.getItem('student_id');
            if (!studentId) {
                document.getElementById('student-modal').style.display = 'flex';
            } else {
                // Perform silent login check
                verifyLogin(studentId, true);
            }
        });

        function getDeviceId() {
            let did = localStorage.getItem('device_id');
            if (!did) {
                did = 'dev_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
                localStorage.setItem('device_id', did);
            }
            return did;
        }

        function verifyLogin(studentId, silent = false) {
            const btn = document.getElementById('save-student-btn');
            if(btn) {
                btn.disabled = true;
                btn.textContent = 'Đang xác thực...';
            }
            
            fetch(WEB_APP_URL, {
                redirect: "follow",
                method: "POST",
                headers: {
                    "Content-Type": "text/plain;charset=utf-8",
                },
                body: JSON.stringify({
                    action: 'login',
                    userId: studentId,
                    deviceId: getDeviceId()
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    localStorage.setItem('student_id', studentId);
                    document.getElementById('student-modal').style.display = 'none';
                    document.getElementById('main-layout').style.display = 'flex';
                } else {
                    alert(data.message || 'Lỗi xác thực!');
                    localStorage.removeItem('student_id');
                    document.getElementById('student-modal').style.display = 'flex';
                    if(btn) {
                        btn.disabled = false;
                        btn.textContent = 'Lưu Lại';
                    }
                }
            })
            .catch(e => {
                console.log(e);
                alert("Lỗi kết nối máy chủ. Vui lòng thử lại!");
                if(btn) {
                    btn.disabled = false;
                    btn.textContent = 'Lưu Lại';
                }
            });
        }

        function saveStudentId() {
            const input = document.getElementById('student-id-input');
            const studentId = input.value.trim().toUpperCase();
            
            if (studentId.length < 3) {
                alert('Vui lòng nhập mã học viên hợp lệ (Ít nhất 3 ký tự)!');
                return;
            }
            verifyLogin(studentId, false);
        }

        function sendScoreToGoogle(score, total) {
            if (WEB_APP_URL === "YOUR_GOOGLE_APP_SCRIPT_WEB_APP_URL_HERE") return;
            const percent = Math.round((score / total) * 100);
            
            const payload = {
                action: 'submit',
                userId: localStorage.getItem('student_id') || "UNKNOWN",
                deviceId: getDeviceId(),
                lessonId: '{{TITLE}}',
                score: `${score}/${total}`,
                percent: percent
            };

            fetch(WEB_APP_URL, {
                redirect: "follow",
                method: "POST",
                headers: {
                    "Content-Type": "text/plain;charset=utf-8",
                },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'error') {
                    alert('Cảnh báo: ' + data.message);
                }
            })
            .catch(e => console.log("Tracking error", e));
        }
"""

import re
# Regex replace the script blocks
content = re.sub(
    r"document\.addEventListener\('DOMContentLoaded', \(\) => \{.*?function sendScoreToGoogle[^\}]+\}",
    js_replacement.strip(),
    content,
    flags=re.DOTALL
)

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Template patched successfully!")
