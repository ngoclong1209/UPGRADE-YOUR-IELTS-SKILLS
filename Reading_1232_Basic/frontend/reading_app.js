// reading_app.js

// SFX helper
function playSfx(id) { try { let a = document.getElementById(id); if(a) { a.currentTime = 0; a.play().catch(e=>{}); } } catch(e){} }

window.onLessonDataLoaded = function(data) {
    renderReadingTest(data);
    if(typeof startTimer === "function") startTimer();
};

document.addEventListener('DOMContentLoaded', () => {
    // 1. Fetch data from URL or fallback to sample_data
    const urlParams = new URLSearchParams(window.location.search);
    const testFile = urlParams.get('file');
    
    // Default to a JS version of sample data if available, else try loading the requested file
    const fileToLoad = testFile ? `data/${testFile}` : './sample_data.js';
    
    // Create new script to bypass CORS for file:// protocol
    const script = document.createElement('script');
    script.src = fileToLoad + '?t=' + new Date().getTime();
    script.onerror = () => {
        console.error('Error loading data');
        document.getElementById('passage-content').innerHTML = '<h3 style="color:red; text-align:center; padding: 20px;">Lỗi tải dữ liệu. Bài thi này chưa được tạo, hoặc trình duyệt chặn tải file! Hãy dùng Live Server.</h3>';
    };
    document.body.appendChild(script);
});

function renderReadingTest(data) {
    const passageContent = document.getElementById('passage-content');
    document.title = data.title + ' - IELTS Reading Practice';
    const testTitleEl = document.getElementById('test-title');
    if (testTitleEl) testTitleEl.innerText = data.title;
    const answerContent = document.querySelector('.answer-pane');

    // Auto-number paragraphs with A, B, C... to help with matching questions
    let rawPassage = data.passage || data.passage_html || "";
    let pMatchIndex = 0;
    // Replace <p> with <p>[Letter] but avoid duplicate numbering if already present
    rawPassage = rawPassage.replace(/<p([^>]*)>(.*?)(?=<\/p>|$)/gi, (match, attrs, pContent) => {
        // Check if content already starts with something like A., [A], or 1.
        // Strip out any leading HTML tags to check text content
        const cleanContent = pContent.replace(/<[^>]+>/g, '').trim();
        if (/^([A-Z]\.|\[[A-Z]\]|\d+\.)/i.test(cleanContent)) {
            return match;
        }
        
        let letter = String.fromCharCode(65 + pMatchIndex);
        pMatchIndex++;
        return `<p${attrs}><strong style="margin-right:8px; color:#17a2b8;">[${letter}]</strong> ${pContent}`;
    });

    let passageHtml = `
        <h2 style="margin-bottom: 20px; color: #333; text-align: center;">${data.title}</h2>
        <div style="font-size: 1.1rem; line-height: 1.8; color: #444; padding: 10px;">
            ${rawPassage}
        </div>
    `;
    passageContent.innerHTML = passageHtml;

    // Group questions by instruction
    let groups = [];
    let currentGroup = null;

    data.questions.forEach((q) => {
        if (!currentGroup || currentGroup.instruction !== q.instruction) {
            currentGroup = {
                id: 'group_' + groups.length,
                instruction: q.instruction,
                questions: []
            };
            groups.push(currentGroup);
        }
        currentGroup.questions.push(q);
    });

    // Store data globally to access during check
    window.currentTestData = data;

    // Render Questions
    let questionsHtml = `
        <h3 style="margin-bottom: 20px; color: #333;">Questions</h3>
        <form id="reading-form">
    `;

    groups.forEach((group, gIndex) => {
        questionsHtml += `
            <div class="question-group" id="${group.id}" style="margin-bottom: 30px; padding: 15px; border-radius: 8px; background: rgba(255,255,255,0.5); border: 1px solid #ddd;">
                <div style="color: #444; font-size: 1rem; margin-bottom: 15px; font-weight:bold;">${group.instruction || ''}</div>
        `;

        group.questions.forEach(q => {
            questionsHtml += `
                <div class="question-item" id="q-container-${q.id}" style="margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px dashed #eee;">
                    <p style="font-weight: bold; margin-bottom: 10px;">${q.id}. ${q.text || ''}</p>`;

            const typeStr = q.type || "";
            if (typeStr.includes("multiple_choice")) {
                let optionsObj = q.options || {};
                // If it's an array, convert to an object for consistent rendering
                if (Array.isArray(optionsObj)) {
                    const temp = {};
                    optionsObj.forEach((opt, idx) => {
                        // try to extract "A. text" or just use "A" -> "text"
                        const match = opt.match(/^([A-Z])[\.\)]\s*(.*)$/);
                        if (match) {
                            temp[match[1]] = opt;
                        } else {
                            temp[String.fromCharCode(65 + idx)] = opt; // Fallback to A, B, C
                        }
                    });
                    optionsObj = temp;
                }
                
                Object.entries(optionsObj).forEach(([key, val]) => {
                    questionsHtml += `
                        <div class="form-check" style="margin-bottom: 8px;">
                            <input class="form-check-input" type="radio" name="${q.id}" id="${q.id}_${key}" value="${key}">
                            <label class="form-check-label" for="${q.id}_${key}" style="cursor: pointer; font-size: 1.05em;">
                                <strong>${key}</strong>: ${val}
                            </label>
                        </div>
                    `;
                });
            } else if (typeStr.includes("yes_no_not_given")) {
                ['YES', 'NO', 'NOT GIVEN'].forEach(opt => {
                    questionsHtml += `
                        <div class="form-check form-check-inline" style="margin-right: 20px;">
                            <input class="form-check-input" type="radio" name="${q.id}" id="${q.id}_${opt.replace(/\s+/g, '')}" value="${opt}">
                            <label class="form-check-label" for="${q.id}_${opt.replace(/\s+/g, '')}" style="cursor: pointer; font-size: 1.05em;">${opt}</label>
                        </div>
                    `;
                });
            } else if (typeStr.includes("true_false_not_given")) {
                ['TRUE', 'FALSE', 'NOT GIVEN'].forEach(opt => {
                    questionsHtml += `
                        <div class="form-check form-check-inline" style="margin-right: 20px;">
                            <input class="form-check-input" type="radio" name="${q.id}" id="${q.id}_${opt.replace(/\s+/g, '')}" value="${opt}">
                            <label class="form-check-label" for="${q.id}_${opt.replace(/\s+/g, '')}" style="cursor: pointer; font-size: 1.05em;">${opt}</label>
                        </div>
                    `;
                });
            } else if (typeStr.includes("dropdown")) {
                let optionsObj = q.options || {};
                questionsHtml += `<select name="${q.id}" class="form-control mb-3" style="width: 100%; max-width: 400px;">
                    <option value="">-- Select an option --</option>`;
                if (Array.isArray(optionsObj)) {
                    optionsObj.forEach(val => {
                        questionsHtml += `<option value="${val}">${val}</option>`;
                    });
                } else {
                    Object.entries(optionsObj).forEach(([key, val]) => {
                        questionsHtml += `<option value="${key}">${key}: ${val}</option>`;
                    });
                }
                questionsHtml += `</select>`;
            } else if (typeStr.includes("matching")) {
                // matching_information, matching_headings, matching_features
                let selectOptions = [];
                let optionsObj = q.options || {};
                let parasObj = q.paragraphs || {};
                
                // Extract answer keys from options
                if (Array.isArray(optionsObj)) {
                    optionsObj.forEach((opt, idx) => {
                        const match = opt.match(/^([A-Z0-9ivxlcIVXLC]+)[\.\)]\s*(.*)$/);
                        if (match) selectOptions.push(match[1]);
                        else selectOptions.push(String(idx + 1));
                    });
                } else if (Object.keys(optionsObj).length > 0) {
                    selectOptions = Object.keys(optionsObj);
                } else if (Array.isArray(parasObj)) {
                    parasObj.forEach((p, idx) => selectOptions.push(String(idx + 1)));
                } else if (Object.keys(parasObj).length > 0) {
                    selectOptions = Object.keys(parasObj);
                }
                
                // Fallback: if no options or paragraphs were found, try to use unique values from answers
                if (selectOptions.length === 0 && q.answers && typeof q.answers === 'object') {
                    selectOptions = [...new Set(Object.values(q.answers))].sort();
                }
                
                if (selectOptions.length === 0 && !q.answers) {
                    questionsHtml += `<input type="text" name="${q.id}" class="form-control mb-3" placeholder="Enter your answer" style="width: 100%; max-width: 400px;">`;
                    // Skip the rest of matching logic
                } else if (q.answers && typeof q.answers === 'object') {
                    Object.keys(q.answers).forEach(subQ => {
                        let text = "";
                        // Fallback text to display next to the dropdown
                        if (!Array.isArray(optionsObj) && optionsObj[subQ]) text = optionsObj[subQ];
                        else if (!Array.isArray(parasObj) && parasObj[subQ]) text = parasObj[subQ];
                        else if (Array.isArray(optionsObj) && optionsObj[subQ-1]) text = optionsObj[subQ-1];
                        else if (Array.isArray(parasObj) && parasObj[subQ-1]) text = parasObj[subQ-1];
                        
                        questionsHtml += `
                            <div style="margin-bottom: 10px;">
                                <span style="display:inline-block; min-width:30px; font-weight:bold;">${subQ}</span>
                                <select name="${q.id}_${subQ}" class="form-control" style="width: 100%; max-width: 250px; padding: 6px; border-radius: 6px; border: 1px solid #ccc; display:inline-block; margin-right: 10px;">
                                    <option value="">-- Select --</option>`;
                        selectOptions.forEach(val => {
                            questionsHtml += `<option value="${val}">${val}</option>`;
                        });
                        questionsHtml += `</select>
                                <span style="font-size: 0.95em;">${text}</span>
                            </div>
                        `;
                    });
                } else {
                    // Single matching question
                    questionsHtml += `<select name="${q.id}" class="form-control" style="width: 100%; max-width: 300px; padding: 8px; border-radius: 6px; border: 1px solid #ccc;">
                        <option value="">-- Select an option --</option>`;
                    selectOptions.forEach(val => {
                        let text = "";
                        if (q.options && q.options[val]) text = q.options[val];
                        else if (q.paragraphs && q.paragraphs[val]) text = q.paragraphs[val];
                        questionsHtml += `<option value="${val}">${val} ${text ? '- ' + text : ''}</option>`;
                    });
                    questionsHtml += `</select>`;
                }
            } else {
                // Check if it's a known text input type
                const textInputTypes = ["fill", "sentence", "short", "summary", "table", "flow", "diagram", "note", "completion", "ending"];
                const isTextInput = textInputTypes.some(t => typeStr.includes(t));
                if (isTextInput) {
                    questionsHtml += `<input type="text" name="${q.id}" class="form-control mb-3" placeholder="Enter your answer" style="width: 100%; max-width: 400px;">`;
                } else {
                    questionsHtml += `<p class="text-danger">Unsupported question type: ${q.type}</p>`;
                }
            }
            // Placeholder for individual explanation/feedback
            questionsHtml += `<div class="q-feedback" id="feedback-${q.id}" style="display:none; margin-top:10px; font-size:0.95rem;"></div>`;

            questionsHtml += `</div>`;
        });

        // Add check button for this group
        questionsHtml += `
                <div style="text-align: right; margin-top: 10px;">
                    <button type="button" class="btn btn-sm check-group-btn" data-group-index="${gIndex}" style="background-color: #17a2b8; color: white; border:none; padding: 5px 15px; border-radius: 4px; cursor: pointer;">Check Answers</button>
                </div>
            </div>
        `;
    });

    questionsHtml += `
            <div style="text-align: center; margin-top: 30px;">
                <button type="button" id="btn-submit-reading" class="btn btn-primary" style="padding: 10px 30px; font-size: 1.1rem; border-radius: 30px; border: none; background: #ff9a9e; color: white; font-weight: bold; box-shadow: 0 4px 15px rgba(255, 154, 158, 0.4);">Nộp Toàn Bộ Bài</button>
            </div>
        </form>
        <div id="results-container" style="display: none; margin-top: 30px; padding: 20px; background: #fff; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);"></div>
    `;

    answerContent.innerHTML = questionsHtml;

    // Attach submit event for whole test
    document.getElementById('btn-submit-reading').addEventListener('click', () => {
        submitReadingTest(data);
    });

    // Attach event for group checking
    document.querySelectorAll('.check-group-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const gIndex = e.target.getAttribute('data-group-index');
            checkGroupAnswers(groups[gIndex], e.target);
        });
    });
}

function checkGroupAnswers(group, btnEl) {
    const form = document.getElementById('reading-form');
    const formData = new FormData(form);
    
    group.questions.forEach(q => {
        const feedbackEl = document.getElementById(`feedback-${q.id}`);
        const containerEl = document.getElementById(`q-container-${q.id}`);
        
        if (q.answers && typeof q.answers === 'object') {
            // Grouped matching question
            let allCorrect = true;
            let feedbackStr = '';
            Object.keys(q.answers).forEach(subQ => {
                const userAnswer = formData.get(`${q.id}_${subQ}`);
                const correctAnswer = q.answers[subQ];
                const isCorrect = userAnswer && userAnswer.toString().trim().toUpperCase() === correctAnswer.toString().trim().toUpperCase();
                if (!isCorrect) allCorrect = false;
                
                feedbackStr += `
                    <p style="margin: 0; color: ${isCorrect ? '#28a745' : '#dc3545'}">
                        <strong>${subQ} - Bạn chọn:</strong> ${userAnswer || 'Chưa trả lời'}
                        ${!isCorrect ? ` <br><strong>Đáp án đúng:</strong> ${correctAnswer}` : ''}
                    </p>
                `;
            });
            
            containerEl.style.backgroundColor = allCorrect ? '#f8fff9' : '#fff8f8';
            containerEl.style.borderLeft = `4px solid ${allCorrect ? '#28a745' : '#dc3545'}`;
            containerEl.style.paddingLeft = '10px';
            
            feedbackEl.style.display = 'block';
            feedbackEl.innerHTML = feedbackStr + `
                <p style="margin: 5px 0 0 0; color: #666; font-style: italic;">
                    <strong>Giải thích chung:</strong> ${q.explanation || ''}
                </p>
            `;
        } else {
            // Standard single answer question
            const userAnswer = formData.get(`${q.id}`);
            const correctAnswer = q.answer;
            const isCorrect = userAnswer && userAnswer.toString().trim().toUpperCase() === correctAnswer.toString().trim().toUpperCase();
            
            containerEl.style.backgroundColor = isCorrect ? '#f8fff9' : '#fff8f8';
            containerEl.style.borderLeft = `4px solid ${isCorrect ? '#28a745' : '#dc3545'}`;
            containerEl.style.paddingLeft = '10px';
            
            feedbackEl.style.display = 'block';
            feedbackEl.innerHTML = `
                <p style="margin: 0; color: ${isCorrect ? '#28a745' : '#dc3545'}">
                    <strong>Bạn chọn:</strong> ${userAnswer || 'Chưa trả lời'}
                    ${!isCorrect ? ` <br><strong>Đáp án đúng:</strong> ${correctAnswer}` : ''}
                </p>
                <p style="margin: 5px 0 0 0; color: #666; font-style: italic;">
                    <strong>Giải thích:</strong> ${q.explanation || ''}
                </p>
            `;
        }
    });
    
    // Hide or disable the button after checking
    btnEl.innerText = 'Checked';
    btnEl.disabled = true;
    btnEl.style.backgroundColor = '#6c757d';
}

function submitReadingTest(data) {
    const form = document.getElementById('reading-form');
    const formData = new FormData(form);
    const resultsContainer = document.getElementById('results-container');
    
    let score = 0;
    let totalQuestions = 0;
    let resultsHtml = `<h3 style="color: #333; text-align: center; margin-bottom: 20px;">Kết Quả</h3>`;

    data.questions.forEach(q => {
        if (q.answers && typeof q.answers === 'object') {
            // Grouped matching question
            let allCorrect = true;
            let subFeedbackStr = '';
            Object.keys(q.answers).forEach(subQ => {
                totalQuestions++;
                const userAnswer = formData.get(`${q.id}_${subQ}`);
                const correctAnswer = q.answers[subQ];
                const isCorrect = userAnswer && userAnswer.toString().trim().toUpperCase() === correctAnswer.toString().trim().toUpperCase();
                
                if (isCorrect) score++;
                else allCorrect = false;
                
                subFeedbackStr += `
                    <p style="margin: 5px 0 0 0; color: #555;">
                        ${subQ} - Bạn chọn: <strong style="color: ${isCorrect ? '#28a745' : '#dc3545'}">${userAnswer || 'Chưa trả lời'}</strong> 
                        ${!isCorrect ? `(Đáp án đúng: <strong>${correctAnswer}</strong>)` : ''}
                    </p>
                `;
            });
            
            resultsHtml += `
                <div style="margin-bottom: 15px; padding: 10px; border-left: 4px solid ${allCorrect ? '#28a745' : '#dc3545'}; background: ${allCorrect ? '#f8fff9' : '#fff8f8'};">
                    <p style="margin: 0; font-weight: bold;">Câu ${q.id}: ${q.text || 'Matching'}</p>
                    ${subFeedbackStr}
                    <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #666; font-style: italic;">Giải thích: ${q.explanation || ''}</p>
                </div>
            `;
        } else {
            // Standard single answer
            totalQuestions++;
            const userAnswer = formData.get(`${q.id}`);
            const correctAnswer = q.answer;
            const isCorrect = userAnswer && userAnswer.toString().trim().toUpperCase() === correctAnswer.toString().trim().toUpperCase();

            if (isCorrect) score++;

            resultsHtml += `
                <div style="margin-bottom: 15px; padding: 10px; border-left: 4px solid ${isCorrect ? '#28a745' : '#dc3545'}; background: ${isCorrect ? '#f8fff9' : '#fff8f8'};">
                    <p style="margin: 0; font-weight: bold;">Câu ${q.id}: ${q.text}</p>
                    <p style="margin: 5px 0 0 0; color: #555;">
                        Bạn chọn: <strong style="color: ${isCorrect ? '#28a745' : '#dc3545'}">${userAnswer || 'Chưa trả lời'}</strong> 
                        ${!isCorrect ? `(Đáp án đúng: <strong>${correctAnswer}</strong>)` : ''}
                    </p>
                    <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #666; font-style: italic;">Giải thích: ${q.explanation || ''}</p>
                </div>
            `;
        }
    });

    resultsHtml = `
        <div style="text-align: center; margin-bottom: 20px;">
            <h4 style="color: #ff9a9e; font-size: 1.5rem;">Điểm của bạn: ${score} / ${totalQuestions}</h4>
        </div>
    ` + resultsHtml;

    resultsContainer.innerHTML = resultsHtml;
    resultsContainer.style.display = 'block';

    // Play SFX based on score
    if (score === totalQuestions) {
        playSfx('sfx-win');
    } else {
        playSfx('sfx-wrong');
    }


    // Stop timer
    if (typeof timerInterval !== 'undefined') {
        clearInterval(timerInterval);
    }
}

// Timer logic
let timerInterval;
let secondsElapsed = 0;

function startTimer() {
    secondsElapsed = 0;
    const timerDisplay = document.getElementById('hud-time');
    if (!timerDisplay) return;
    
    if (typeof timerInterval !== 'undefined') {
        clearInterval(timerInterval);
    }
    
    timerInterval = setInterval(() => {
        secondsElapsed++;
        const m = Math.floor(secondsElapsed / 60);
        const s = secondsElapsed % 60;
        timerDisplay.textContent = `⏱️ Time: ${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    }, 1000);
}



// --- RESIZER LOGIC ---
document.addEventListener('DOMContentLoaded', () => {
    const resizer = document.getElementById('dragMe');
    const leftSide = document.querySelector('.passage-pane');
    const rightSide = document.querySelector('.answer-pane');

    if (resizer && leftSide && rightSide) {
        let x = 0;
        let leftWidth = 0;

        const mouseDownHandler = function(e) {
            x = e.clientX;
            leftWidth = leftSide.getBoundingClientRect().width;
            document.addEventListener('mousemove', mouseMoveHandler);
            document.addEventListener('mouseup', mouseUpHandler);
            resizer.classList.add('resizing');
            
            // Prevent text selection while dragging
            leftSide.style.userSelect = 'none';
            rightSide.style.userSelect = 'none';
        };

        const mouseMoveHandler = function(e) {
            const dx = e.clientX - x;
            const parentWidth = resizer.parentNode.getBoundingClientRect().width;
            const newLeftWidth = ((leftWidth + dx) * 100) / parentWidth;
            // Constrain between 20% and 80%
            if (newLeftWidth > 20 && newLeftWidth < 80) {
                leftSide.style.flex = `0 0 ${newLeftWidth}%`;
            }
        };

        const mouseUpHandler = function() {
            resizer.classList.remove('resizing');
            document.removeEventListener('mousemove', mouseMoveHandler);
            document.removeEventListener('mouseup', mouseUpHandler);
            
            // Restore text selection
            leftSide.style.userSelect = '';
            rightSide.style.userSelect = '';
        };

        resizer.addEventListener('mousedown', mouseDownHandler);
    }

    // --- HIGHLIGHT LOGIC ---
    const highlightMenu = document.getElementById('highlight-menu');
    const passageContent = document.getElementById('passage-content');
    const btnClearAll = document.getElementById('btn-clear-highlights');
    let currentSelectionRange = null;

    if (passageContent && highlightMenu) {
        passageContent.addEventListener('mouseup', (e) => {
            const selection = window.getSelection();
            if (selection.toString().trim().length > 0) {
                const range = selection.getRangeAt(0);
                const rect = range.getBoundingClientRect();
                currentSelectionRange = range;
                
                highlightMenu.style.display = 'flex';
                highlightMenu.style.top = `${window.scrollY + rect.top - 50}px`;
                highlightMenu.style.left = `${window.scrollX + rect.left + rect.width / 2 - highlightMenu.offsetWidth / 2}px`;
            } else {
                // Check if clicked on an existing highlight
                let target = e.target;
                if ((target.tagName === 'SPAN' || target.tagName === 'FONT') && target.style.backgroundColor) {
                    highlightMenu.style.display = 'flex';
                    highlightMenu.style.top = `${e.pageY - 50}px`;
                    highlightMenu.style.left = `${e.pageX - highlightMenu.offsetWidth / 2}px`;
                    
                    const range = document.createRange();
                    range.selectNodeContents(target);
                    const sel = window.getSelection();
                    sel.removeAllRanges();
                    sel.addRange(range);
                    currentSelectionRange = range;
                } else {
                    highlightMenu.style.display = 'none';
                }
            }
        });

        document.addEventListener('mousedown', (e) => {
            if (!highlightMenu.contains(e.target) && !passageContent.contains(e.target)) {
                highlightMenu.style.display = 'none';
            }
        });

        document.querySelectorAll('.hl-btn').forEach(btn => {
            btn.addEventListener('mousedown', (e) => {
                // Prevent selection clearing
                e.preventDefault();
            });
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const color = btn.getAttribute('data-color');
                if (currentSelectionRange) {
                    document.designMode = "on";
                    const sel = window.getSelection();
                    sel.removeAllRanges();
                    sel.addRange(currentSelectionRange);
                    
                    // Use hiliteColor or backColor depending on browser support
                    if (!document.execCommand("hiliteColor", false, color)) {
                        document.execCommand("backColor", false, color);
                    }
                    
                    document.designMode = "off";
                    highlightMenu.style.display = 'none';
                    sel.removeAllRanges();
                }
            });
        });

        const hlRemoveBtn = document.getElementById('hl-remove');
        if (hlRemoveBtn) {
            hlRemoveBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (currentSelectionRange) {
                    document.designMode = "on";
                    const sel = window.getSelection();
                    sel.removeAllRanges();
                    sel.addRange(currentSelectionRange);
                    // Standard way to clear formatting
                    document.execCommand("removeFormat", false, null);
                    // Also explicitly set transparent if removeFormat doesn't work for backgrounds
                    document.execCommand("hiliteColor", false, "transparent");
                    
                    // Fallback cleanup
                    let parent = currentSelectionRange.commonAncestorContainer;
                    if (parent.nodeType === 3) parent = parent.parentNode;
                    if ((parent.tagName === 'SPAN' || parent.tagName === 'FONT') && parent.style.backgroundColor) {
                        const text = document.createTextNode(parent.textContent);
                        parent.parentNode.replaceChild(text, parent);
                    }
                    
                    document.designMode = "off";
                    highlightMenu.style.display = 'none';
                    sel.removeAllRanges();
                }
            });
        }
    }

    if (btnClearAll && passageContent) {
        btnClearAll.addEventListener('click', () => {
            const spans = passageContent.querySelectorAll('span[style*="background-color"], font[style*="background-color"]');
            spans.forEach(span => {
                const text = document.createTextNode(span.textContent);
                span.parentNode.replaceChild(text, span);
            });
            // Also clean up any transparent backgrounds left by remove
            const transparentSpans = passageContent.querySelectorAll('span[style*="background-color: transparent"], font[style*="background-color: transparent"]');
            transparentSpans.forEach(span => {
                const text = document.createTextNode(span.textContent);
                span.parentNode.replaceChild(text, span);
            });
        });
    }
});
