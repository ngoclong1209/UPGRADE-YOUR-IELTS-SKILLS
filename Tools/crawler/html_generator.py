import json
import os

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - YouPass Practice</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --bg-main: #0f172a;
            --bg-card: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
            --success: #10b981;
            --error: #ef4444;
            --success-bg: rgba(16, 185, 129, 0.15);
            --error-bg: rgba(239, 68, 68, 0.15);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            line-height: 1.6;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}

        header {{
            background-color: var(--bg-card);
            border-bottom: 1px solid var(--border);
            padding: 1rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-shrink: 0;
        }}

        .badge {{
            background: linear-gradient(135deg, #6366f1, #a855f7);
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .main-container {{
            display: flex;
            flex: 1;
            overflow: hidden;
        }}

        .panel {{
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow-y: auto;
            padding: 2rem;
        }}

        .panel-left {{
            border-right: 1px solid var(--border);
            background-color: rgba(30, 41, 59, 0.3);
        }}

        .panel-right {{
            background-color: var(--bg-main);
        }}

        h1 {{
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }}

        h2 {{
            font-size: 1.4rem;
            margin-bottom: 1.5rem;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.5rem;
        }}

        .passage-content {{
            font-size: 1.05rem;
            line-height: 1.8;
            color: #cbd5e1;
        }}

        .audio-container {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            position: sticky;
            top: 0;
            z-index: 10;
        }}

        audio {{
            width: 100%;
        }}

        .question-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
        }}

        .question-card:hover {{
            border-color: var(--primary);
            box-shadow: 0 4px 20px rgba(79, 70, 229, 0.1);
        }}

        .question-num {{
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 0.5rem;
        }}

        .question-text {{
            font-weight: 500;
            margin-bottom: 1rem;
            color: var(--text-main);
        }}

        /* Inputs formatting */
        input[type="text"] {{
            background: var(--bg-main);
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 0.6rem 1rem;
            border-radius: 6px;
            width: 100%;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.2s;
        }}

        input[type="text"]:focus {{
            border-color: var(--primary);
        }}

        .option-label {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            background: var(--bg-main);
            border: 1px solid var(--border);
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .option-label:hover {{
            border-color: var(--primary);
            background: rgba(79, 70, 229, 0.05);
        }}

        input[type="radio"], input[type="checkbox"] {{
            accent-color: var(--primary);
            width: 1.1rem;
            height: 1.1rem;
        }}

        /* Check answers section */
        .submit-container {{
            margin-top: 1.5rem;
            margin-bottom: 3rem;
        }}

        .btn {{
            background: var(--primary);
            color: white;
            border: none;
            padding: 0.85rem 2rem;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.2s;
            width: 100%;
        }}

        .btn:hover {{
            background: var(--primary-hover);
        }}

        /* Feedback styling */
        .feedback {{
            display: none;
            margin-top: 1rem;
            padding: 1rem;
            border-radius: 8px;
            font-size: 0.95rem;
        }}

        .feedback.correct {{
            background: var(--success-bg);
            border: 1px solid var(--success);
            color: #6ee7b7;
        }}

        .feedback.incorrect {{
            background: var(--error-bg);
            border: 1px solid var(--error);
            color: #fca5a5;
        }}

        .explanation-box {{
            display: none;
            margin-top: 1rem;
            padding: 1rem;
            background: rgba(15, 23, 42, 0.6);
            border-left: 4px solid var(--primary);
            border-radius: 0 8px 8px 0;
            font-size: 0.95rem;
            color: #cbd5e1;
        }}

        .explanation-box h4 {{
            margin-bottom: 0.5rem;
            color: var(--text-main);
            font-size: 1rem;
        }}

        .input-correct {{
            border-color: var(--success) !important;
            background-color: var(--success-bg) !important;
        }}

        .input-incorrect {{
            border-color: var(--error) !important;
            background-color: var(--error-bg) !important;
        }}

        .option-correct {{
            border-color: var(--success) !important;
            background-color: var(--success-bg) !important;
        }}

        .option-incorrect {{
            border-color: var(--error) !important;
            background-color: var(--error-bg) !important;
        }}

        /* Responsive */
        @media (max-width: 900px) {{
            body {{
                overflow: auto;
                height: auto;
            }}
            .main-container {{
                flex-direction: column;
                overflow: visible;
                height: auto;
            }}
            .panel {{
                overflow-y: visible;
                height: auto;
            }}
            .panel-left {{
                border-right: none;
                border-bottom: 1px solid var(--border);
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>YouPass Practice</h1>
        <span class="badge">{skill}</span>
    </header>

    <div class="main-container">
        <!-- Left Panel: Passage Text & Audio -->
        <div class="panel panel-left">
            <h2>Bài đọc / Nội dung bài nghe</h2>
            {audio_element}
            <div class="passage-content">
                {passage_content}
            </div>
        </div>

        <!-- Right Panel: Questions -->
        <div class="panel panel-right">
            <h2>Bài tập</h2>
            <form id="quiz-form" onsubmit="checkAnswers(event)">
                {questions_html}
                
                <div class="submit-container">
                    <button type="submit" class="btn">Nộp Bài / Kiểm Tra Đáp Án</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        const answerKey = {answer_key_json};

        function checkAnswers(event) {{
            event.preventDefault();
            
            // Show all feedback boxes and explanations
            document.querySelectorAll('.feedback').forEach(el => el.style.display = 'block');
            document.querySelectorAll('.explanation-box').forEach(el => el.style.display = 'block');
            
            // Grade each question
            for (const qId in answerKey) {{
                const qInfo = answerKey[qId];
                const type = qInfo.type;
                const correctAnswers = qInfo.correct; // Array or string
                
                let isCorrect = false;
                
                if (type === 'fill-in-the-blank') {{
                    const inputEl = document.getElementById(`q-${{qId}}`);
                    if (inputEl) {{
                        const userAns = inputEl.value.trim().toLowerCase();
                        
                        if (Array.isArray(correctAnswers)) {{
                            isCorrect = correctAnswers.some(ans => ans.trim().toLowerCase() === userAns);
                        }} else {{
                            isCorrect = correctAnswers.trim().toLowerCase() === userAns;
                        }}
                        
                        if (isCorrect) {{
                            inputEl.className = 'input-correct';
                        }} else {{
                            inputEl.className = 'input-incorrect';
                        }}
                    }}
                }} else if (type === 'single-choice') {{
                    const selected = document.querySelector(`input[name="q-${{qId}}"]:checked`);
                    const labels = document.querySelectorAll(`.label-q-${{qId}}`);
                    
                    labels.forEach(lbl => {{
                        lbl.className = 'option-label'; // Reset
                    }});

                    const userAns = selected ? selected.value : '';
                    isCorrect = (userAns.trim().toLowerCase() === correctAnswers.trim().toLowerCase());
                    
                    labels.forEach(lbl => {{
                        const radio = lbl.querySelector('input');
                        if (radio.value.trim().toLowerCase() === correctAnswers.trim().toLowerCase()) {{
                            lbl.classList.add('option-correct');
                        }} else if (selected && radio.value === userAns && !isCorrect) {{
                            lbl.classList.add('option-incorrect');
                        }}
                    }});
                }} else if (type === 'multiple-choice') {{
                    const selected = document.querySelectorAll(`input[name="q-${{qId}}"]:checked`);
                    const labels = document.querySelectorAll(`.label-q-${{qId}}`);
                    
                    labels.forEach(lbl => lbl.className = 'option-label');

                    const userAnswers = Array.from(selected).map(el => el.value.trim().toLowerCase());
                    const correctAnswersLower = correctAnswers.map(ans => ans.trim().toLowerCase());
                    
                    // Check if user matches exactly
                    isCorrect = userAnswers.length === correctAnswersLower.length && 
                                userAnswers.every(val => correctAnswersLower.includes(val));
                                
                    labels.forEach(lbl => {{
                        const cb = lbl.querySelector('input');
                        const cbVal = cb.value.trim().toLowerCase();
                        if (correctAnswersLower.includes(cbVal)) {{
                            lbl.classList.add('option-correct');
                        }} else if (userAnswers.includes(cbVal)) {{
                            lbl.classList.add('option-incorrect');
                        }}
                    }});
                }}

                // Show correct/incorrect feedback block
                const feedbackEl = document.getElementById(`feedback-${{qId}}`);
                if (feedbackEl) {{
                    if (isCorrect) {{
                        feedbackEl.className = 'feedback correct';
                        feedbackEl.innerHTML = '✓ Chính xác';
                    }} else {{
                        feedbackEl.className = 'feedback incorrect';
                        const displayAns = Array.isArray(correctAnswers) ? correctAnswers.join(' / ') : correctAnswers;
                        feedbackEl.innerHTML = `✗ Chưa chính xác. Đáp án đúng: <strong>${{displayAns}}</strong>`;
                    }}
                }}
            }}
        }}
    </script>
</body>
</html>
"""

def generate_questions_html(questions):
    html_chunks = []
    for q in questions:
        q_id = q['id']
        q_text = q['text']
        q_type = q['type']
        
        chunk = f'<div class="question-card">\n'
        chunk += f'  <div class="question-num">Câu hỏi {q_id}</div>\n'
        chunk += f'  <div class="question-text">{q_text}</div>\n'
        
        if q_type == 'fill-in-the-blank':
            chunk += f'  <input type="text" id="q-{q_id}" name="q-{q_id}" placeholder="Nhập đáp án tại đây...">\n'
        elif q_type in ['single-choice', 'multiple-choice']:
            input_type = 'radio' if q_type == 'single-choice' else 'checkbox'
            for idx, opt in enumerate(q.get('options', [])):
                chunk += f'  <label class="option-label label-q-{q_id}">\n'
                chunk += f'    <input type="{input_type}" name="q-{q_id}" value="{opt}"> {opt}\n'
                chunk += f'  </label>\n'
                
        chunk += f'  <div class="feedback" id="feedback-{q_id}"></div>\n'
        
        if q.get('explanation'):
            chunk += f'  <div class="explanation-box">\n'
            chunk += f'    <h4>Giải thích chi tiết:</h4>\n'
            chunk += f'    <p>{q["explanation"]}</p>\n'
            chunk += f'  </div>\n'
            
        chunk += f'</div>\n'
        html_chunks.append(chunk)
        
    return "\n".join(html_chunks)

def save_html(output_path, title, skill, passage_content, questions, has_audio=False):
    audio_element = '<div class="audio-container"><audio src="audio.mp3" controls></audio></div>' if has_audio else ''
    
    # Build answer key dict for JS
    answer_key = {}
    for q in questions:
        answer_key[q['id']] = {
            'type': q['type'],
            'correct': q['correct_answer']
        }
        
    questions_html = generate_questions_html(questions)
    
    html_content = HTML_TEMPLATE.format(
        title=title,
        skill=skill.capitalize(),
        audio_element=audio_element,
        passage_content=passage_content,
        questions_html=questions_html,
        answer_key_json=json.dumps(answer_key, ensure_ascii=False)
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated HTML exercise: {output_path}")
