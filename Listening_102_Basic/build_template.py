import os

with open('/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS LISTENING/pte-listening-audios/extracted_style.css', 'r') as f:
    css = f.read()

template_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{TITLE}}}} - IELTS Listening Practice</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300..700&family=DynaPuff:wght@400..700&family=Quicksand:wght@300..700&display=swap" rel="stylesheet">
    {css}
    <style>
        /* Additional styles for Multiple Choice */
        .mc-question {{
            margin-bottom: 2rem;
            background: #ffffff;
            padding: 1.5rem;
            border-radius: 20px;
            border: 2px solid var(--border-color);
            box-shadow: 0 4px 10px rgba(255, 182, 193, 0.05);
        }}
        .mc-title {{
            font-family: 'Fredoka', sans-serif;
            font-weight: 600;
            color: var(--text-primary);
            font-size: 1.1rem;
            margin-bottom: 1rem;
        }}
        .mc-options {{
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }}
        .mc-option-label {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1rem;
            border-radius: 14px;
            border: 2px solid var(--border-color);
            cursor: pointer;
            transition: all 0.2s ease;
            background: var(--bg-secondary);
        }}
        .mc-option-label:hover {{
            border-color: var(--accent);
            background: #fff;
        }}
        .mc-option-label.correct-answer {{
            border-color: var(--success) !important;
            background-color: var(--success-bg) !important;
            color: #279e6d !important;
            font-weight: 600;
        }}
        .mc-option-label.wrong-answer {{
            border-color: var(--error) !important;
            background-color: var(--error-bg) !important;
            color: #d14357 !important;
        }}
        input[type="radio"] {{
            accent-color: var(--accent);
            transform: scale(1.2);
        }}
        .nav-back {{
            display: inline-block;
            margin-top: 1rem;
            font-family: 'Fredoka', sans-serif;
            color: var(--accent-hover);
            text-decoration: none;
            font-weight: 600;
            transition: transform 0.2s;
        }}
        .nav-back:hover {{
            transform: translateX(-5px);
        }}
        #transcript-lock {{
            text-align: center;
            padding: 3rem 1rem;
            color: var(--text-secondary);
            font-family: 'Fredoka', sans-serif;
            font-size: 1.2rem;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 20px;
            border: 2px dashed var(--border-color);
        }}
    </style>
</head>
<body>

    <header id="main-header">
        <div class="header-left">
            <h1>{{{{TITLE}}}}</h1>
            <div id="user-banner-placeholder"></div>
        </div>
        <div class="header-right">
            <a href="../../index.html" class="nav-back">← Back to Index</a>
        </div>
    </header>

    <div class="main-layout" id="main-layout">
        <!-- Swapped Panes: Answer Pane is now on the left -->
        <div class="answer-pane fairytale-panel">
            <div class="sheet-title">✏️ Answer Sheet</div>
            
            <div class="answer-grid" id="quiz-container">
                {{{{QUESTIONS_HTML}}}}
            </div>
            
            <button class="check-btn" id="btn-submit">🧁 Check Full Test 🧁</button>
            <div class="score-display" id="result-summary" style="display: none; margin-top: 1rem; text-align: center; font-weight: bold; font-size: 1.2rem; padding: 10px; border-radius: 12px;"></div>
            
        </div>
        
        <div class="passage-pane fairytale-panel">
            <div class="hud-header">
                <span>🌸 AUDIO TRANSCRIPT</span>
                <span class="hud-status">✨ HAPPY LEARNING! ✨</span>
            </div>
            
            <div id="transcript-lock">
                🔒 Transcript is locked.<br>
                <span style="font-size: 0.9rem; font-family: 'Quicksand', sans-serif;">Score 100% or try 3 times to unlock!</span>
            </div>
            
            <div class="content-html" id="transcript-content" style="display: none;">
                {{{{TRANSCRIPT_HTML}}}}
            </div>
        </div>
    </div>

    <div class="audio-fixed-bottom" id="audio-player-container">
        <audio src="{{{{AUDIO_URL}}}}" controls></audio>
    </div>

    <!-- Hidden audio elements for SFX -->
    <audio id="sfx-win" src="../../assets/sfx/gamewinner.mp3" preload="auto"></audio>
    <audio id="sfx-wrong" src="../../assets/sfx/incorrectanswersfx.mp3" preload="auto"></audio>

    <script>
        const correctAnswers = {{{{CORRECT_ANSWERS_JSON}}}}; 
        let attemptCount = 0;
        
        // Shuffle options logic
        document.addEventListener('DOMContentLoaded', () => {{
            const questions = document.querySelectorAll('.mc-question');
            
            questions.forEach((q, qIndex) => {{
                const optionsContainer = q.querySelector('.mc-options');
                if (!optionsContainer) return;
                
                const labels = Array.from(optionsContainer.querySelectorAll('.mc-option-label'));
                
                // Extract inner htmls (which contains input and text)
                const optionsData = labels.map(label => {{
                    const input = label.querySelector('input');
                    const textSpan = label.querySelector('.option-text');
                    return {{
                        value: input.value,
                        name: input.name,
                        text: textSpan ? textSpan.innerHTML : label.innerText.replace(/^[A-D]\.\s*/, '').trim()
                    }};
                }});
                
                // Shuffle data (Fisher-Yates)
                for (let i = optionsData.length - 1; i > 0; i--) {{
                    const j = Math.floor(Math.random() * (i + 1));
                    [optionsData[i], optionsData[j]] = [optionsData[j], optionsData[i]];
                }}
                
                // Re-render
                const prefixLetters = ['A', 'B', 'C', 'D', 'E', 'F'];
                optionsContainer.innerHTML = '';
                
                optionsData.forEach((data, index) => {{
                    const newLabel = document.createElement('label');
                    newLabel.className = 'mc-option-label';
                    newLabel.innerHTML = `
                        <input type="radio" name="${{data.name}}" value="${{data.value}}">
                        <span style="font-weight: 600; color: var(--accent-hover); min-width: 20px;">${{prefixLetters[index]}}.</span>
                        <span class="option-text">${{data.text}}</span>
                    `;
                    optionsContainer.appendChild(newLabel);
                }});
            }});
        }});

        function unlockTranscript() {{
            document.getElementById('transcript-lock').style.display = 'none';
            document.getElementById('transcript-content').style.display = 'block';
        }}

        // Grading logic
        document.getElementById('btn-submit').addEventListener('click', function() {{
            attemptCount++;
            let score = 0;
            const total = Object.keys(correctAnswers).length;
            
            // First pass: Calculate score
            for (const [qId, correctVal] of Object.entries(correctAnswers)) {{
                const options = document.getElementsByName(qId);
                options.forEach(opt => {{
                    if (opt.checked && opt.value === correctVal) {{
                        score++;
                    }}
                }});
            }}
            
            const isFinalAttempt = attemptCount >= 3;
            const isPerfect = (score === total);

            // Second pass: Update UI
            for (const [qId, correctVal] of Object.entries(correctAnswers)) {{
                const options = document.getElementsByName(qId);
                
                options.forEach(opt => {{
                    const labelDiv = opt.closest('.mc-option-label');
                    labelDiv.classList.remove('correct-answer', 'wrong-answer');
                    
                    if (opt.checked) {{
                        if (opt.value === correctVal) {{
                            labelDiv.classList.add('correct-answer');
                        }} else {{
                            labelDiv.classList.add('wrong-answer');
                        }}
                    }}
                    
                    // Show correct answers if final attempt or perfect score
                    if ((isFinalAttempt || isPerfect) && opt.value === correctVal && !opt.checked) {{
                        labelDiv.classList.add('correct-answer');
                    }}
                    
                    // Disable inputs if final attempt or perfect score
                    if (isFinalAttempt || isPerfect) {{
                        opt.disabled = true;
                    }}
                }});
            }}

            const resultDiv = document.getElementById('result-summary');
            resultDiv.style.display = 'block';
            
            if (isPerfect) {{
                resultDiv.innerHTML = `🎉 Perfect! ${{score}} / ${{total}} (100%) 🎉`;
                resultDiv.style.backgroundColor = 'var(--success-bg)';
                resultDiv.style.color = '#279e6d';
                document.getElementById('sfx-win').play().catch(e=>{{}});
                unlockTranscript();
                this.disabled = true;
                this.style.opacity = '0.5';
                this.style.cursor = 'not-allowed';
                this.textContent = 'Completed!';
            }} else {{
                if (isFinalAttempt) {{
                    resultDiv.innerHTML = `Final Score: ${{score}} / ${{total}}. Transcript unlocked.`;
                    resultDiv.style.backgroundColor = 'var(--error-bg)';
                    resultDiv.style.color = '#d14357';
                    document.getElementById('sfx-wrong').play().catch(e=>{{}});
                    unlockTranscript();
                    this.disabled = true;
                    this.style.opacity = '0.5';
                    this.style.cursor = 'not-allowed';
                    this.textContent = 'Completed!';
                }} else {{
                    resultDiv.innerHTML = `Score: ${{score}} / ${{total}}. Try again!`;
                    resultDiv.style.backgroundColor = '#fff3cd';
                    resultDiv.style.color = '#856404';
                    document.getElementById('sfx-wrong').play().catch(e=>{{}});
                    this.textContent = `Thử Lại (Lần ${{attemptCount}}/3)`;
                }}
            }}
        }});
        
        // Anti-Copy & Right Click Protections
        document.addEventListener('copy', (e) => {{
            e.preventDefault();
            alert("🔒 Content is protected! Copying is disabled on this platform. ✨");
        }});
        document.addEventListener('contextmenu', (e) => {{
            e.preventDefault();
        }});
        
    </script>
</body>
</html>
"""

with open('/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS LISTENING/pte-listening-audios/template.html', 'w') as f:
    f.write(template_html)
print("template.html updated")
