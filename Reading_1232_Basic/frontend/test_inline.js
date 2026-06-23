
        const WEB_APP_URL = 'https://script.google.com/macros/s/AKfycbxsO2MduHv_ahBdMtEUcIe7YOKpHWP9Ss4X8tD003feSjp2D_Pp4PMgKkzGqMudteW6/exec';

        document.addEventListener('DOMContentLoaded', () => {
            console.log('DOM Loaded!');
            const studentId = localStorage.getItem('student_id');
            document.getElementById('student-modal').style.display = 'flex';
            if (studentId) {
                const input = document.getElementById('student-name-input');
                if (input) input.value = studentId;
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
                    deviceId: getDeviceId(),
                    lessonId: '{{TITLE}}'
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    localStorage.setItem('student_id', studentId);
                    document.getElementById('student-modal').style.display = 'none';
                    document.getElementById('main-layout').style.display = 'flex'; startTimer(); document.getElementById('audio-player-container').style.display = 'flex';
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
            const input = document.getElementById('student-name-input');
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



        
        // Timer Logic
        let timeLeft = 20 * 60; // 20 minutes
        const timerDisplay = document.getElementById('timer-display');
        let timerInterval;

        function startTimer() {
            timerInterval = setInterval(() => {
                timeLeft--;
                const minutes = Math.floor(timeLeft / 60);
                const seconds = timeLeft % 60;
                if(timerDisplay) {
                    timerDisplay.innerText = `⏱ ${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
                }
                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    document.getElementById('btn-submit').click();
                }
            }, 1000);
        }

        const correctAnswers = {{CORRECT_ANSWERS_JSON}}; 
        let attemptCount = 0;
        
        // Shuffle options logic
        document.addEventListener('DOMContentLoaded', () => {
            console.log('DOM Loaded!');
            const questions = document.querySelectorAll('.mc-question');
            
            questions.forEach((q, qIndex) => {
                const optionsContainer = q.querySelector('.mc-options');
                if (!optionsContainer) return;
                
                const labels = Array.from(optionsContainer.querySelectorAll('.mc-option-label'));
                
                // Extract inner htmls (which contains input and text)
                const optionsData = labels.map(label => {
                    const input = label.querySelector('input');
                    const textSpan = label.querySelector('.option-text');
                    return {
                        value: input.value,
                        name: input.name,
                        text: textSpan ? textSpan.innerHTML : label.innerText.replace(/^[A-D]\.\s*/, '').trim()
                    };
                });
                
                // Check for options that reference other options or positions
                const hasRelativeOptions = optionsData.some(opt => {
                    const t = opt.text.toLowerCase();
                    return t.includes("all of the above") || 
                           t.includes("none of the above") ||
                           t.includes("both a and b") ||
                           t.includes("neither a") ||
                           t.includes("a and c") ||
                           t.includes("b and c") ||
                           t.includes("a and b") ||
                           t.includes("a, b");
                });
                
                if (!hasRelativeOptions) {
                    // Shuffle data (Fisher-Yates)
                    for (let i = optionsData.length - 1; i > 0; i--) {
                        const j = Math.floor(Math.random() * (i + 1));
                        [optionsData[i], optionsData[j]] = [optionsData[j], optionsData[i]];
                    }
                }
                
                // Re-render
                const prefixLetters = ['A', 'B', 'C', 'D', 'E', 'F'];
                optionsContainer.innerHTML = '';
                
                optionsData.forEach((data, index) => {
                    const newLabel = document.createElement('label');
                    newLabel.className = 'mc-option-label';
                    newLabel.innerHTML = `
                        <input type="radio" name="${data.name}" value="${data.value}">
                        <span style="font-weight: 600; color: var(--accent-hover); min-width: 20px;">${prefixLetters[index]}.</span>
                        <span class="option-text">${data.text}</span>
                    `;
                    optionsContainer.appendChild(newLabel);
                });
            });
        });

        

        // Grading logic
        document.getElementById('btn-submit').addEventListener('click', function() {
            attemptCount++;
            let score = 0;
            const total = Object.keys(correctAnswers).length;
            
            // First pass: Calculate score
            for (const [qId, correctVal] of Object.entries(correctAnswers)) {
                const options = document.getElementsByName(qId);
                options.forEach(opt => {
                    if (opt.checked && opt.value === correctVal) {
                        score++;
                    }
                });
            }
            
            const isFinalAttempt = attemptCount >= 3;
            const isPerfect = (score === total);

            // Second pass: Update UI
            for (const [qId, correctVal] of Object.entries(correctAnswers)) {
                const options = document.getElementsByName(qId);
                
                options.forEach(opt => {
                    const labelDiv = opt.closest('.mc-option-label');
                    labelDiv.classList.remove('correct-answer', 'wrong-answer');
                    
                    if (opt.checked) {
                        if (opt.value === correctVal) {
                            labelDiv.classList.add('correct-answer');
                        } else {
                            labelDiv.classList.add('wrong-answer');
                        }
                    }
                    
                    // Show correct answers if final attempt or perfect score
                    if ((isFinalAttempt || isPerfect) && opt.value === correctVal && !opt.checked) {
                        labelDiv.classList.add('correct-answer');
                    }
                    
                    // Disable inputs if final attempt or perfect score
                    if (isFinalAttempt || isPerfect) {
                        opt.disabled = true;
                    }
                });
            }

            const resultDiv = document.getElementById('result-summary');
            resultDiv.style.display = 'block';
            
            if (isPerfect) {
                resultDiv.innerHTML = `🎉 Perfect! ${score} / ${total} (100%) 🎉`;
                resultDiv.style.backgroundColor = 'var(--success-bg)';
                resultDiv.style.color = '#279e6d';
                document.getElementById('sfx-win').play().catch(e=>{});
                sendScoreToGoogle(score, total);
                
                this.disabled = true;
                this.style.opacity = '0.5';
                this.style.cursor = 'not-allowed';
                this.textContent = 'Completed!';
            } else {
                if (isFinalAttempt) {
                    resultDiv.innerHTML = `Final Score: ${score} / ${total}. Transcript unlocked.`;
                    resultDiv.style.backgroundColor = 'var(--error-bg)';
                    resultDiv.style.color = '#d14357';
                    document.getElementById('sfx-wrong').play().catch(e=>{});
                    sendScoreToGoogle(score, total);
                    
                    this.disabled = true;
                    this.style.opacity = '0.5';
                    this.style.cursor = 'not-allowed';
                    this.textContent = 'Completed!';
                } else {
                    resultDiv.innerHTML = `Score: ${score} / ${total}. Try again!`;
                    resultDiv.style.backgroundColor = '#fff3cd';
                    resultDiv.style.color = '#856404';
                    document.getElementById('sfx-wrong').play().catch(e=>{});
                    this.textContent = `Thử Lại (Lần ${attemptCount}/3)`;
                }
            }
        });
        
        // Anti-Copy & Right Click Protections
        document.addEventListener('copy', (e) => {
            e.preventDefault();
            alert("🔒 Content is protected! Copying is disabled on this platform. ✨");
        });
        document.addEventListener('contextmenu', (e) => {
            e.preventDefault();
        });
        
