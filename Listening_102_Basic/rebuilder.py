import os
import re
import json
from bs4 import BeautifulSoup

LEVELS = ['Basic', 'Intermediate', 'Advanced']
OUTPUT_DIR = '.'

with open('template.html', 'r', encoding='utf-8') as f:
    TEMPLATE = f.read()

def build_questions_html(questions):
    html = []
    for q in questions:
        q_id = q['id']
        html.append(f'<div class="mc-question">')
        html.append(f'  <h3 class="mc-title">{q["text"]}</h3>')
        html.append(f'  <div class="mc-options">')
        for opt in q['options']:
            val = opt['value']
            text = opt['text']
            html.append(f'    <label class="mc-option-label">')
            html.append(f'      <input type="radio" name="{q_id}" value="{val}">')
            html.append(f'      <span class="option-text">{text}</span>')
            html.append(f'    </label>')
        html.append(f'  </div>')
        html.append(f'</div>')
    return "\n".join(html)

def rebuild_lesson(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        old_html = f.read()
    
    soup = BeautifulSoup(old_html, 'html.parser')
    
    # 1. Title
    h1 = soup.find('h1')
    title = h1.text.strip() if h1 else "Lesson"
    
    # 2. Transcript
    transcript_html = ""
    transcript_section = soup.find(id='transcript-section')
    if transcript_section:
        prose = transcript_section.find(class_=re.compile('prose'))
        if prose:
            transcript_html = "".join(str(c) for c in prose.contents).strip()
    
    # 3. Questions
    questions = []
    quiz_container = soup.find(id='quiz-container')
    if quiz_container:
        q_divs = quiz_container.find_all('div', recursive=False)
        for div in q_divs:
            h3 = div.find('h3')
            if not h3: continue
            q_text = h3.text.strip()
            
            options = []
            labels = div.find_all('label')
            q_id = None
            for lbl in labels:
                inp = lbl.find('input')
                span = lbl.find('span')
                if inp and span:
                    val = inp.get('value')
                    name = inp.get('name')
                    if not q_id: q_id = name
                    # We can remove the "A. " from the option text if it starts with it since the new template adds it dynamically based on position
                    opt_text = span.text.strip()
                    opt_text = re.sub(r'^[A-Z]\.\s*', '', opt_text)
                    options.append({'value': val, 'text': opt_text})
            
            if options and q_id:
                questions.append({
                    'id': q_id,
                    'text': q_text,
                    'options': options
                })
    
    # 4. Answers map
    answers_map = {}
    ans_match = re.search(r'const correctAnswers = ({.*?});', old_html)
    if ans_match:
        try:
            answers_map = json.loads(ans_match.group(1))
        except:
            pass
            
    # 5. Audio URL
    audio_url = 'audio.mp3'
            
    q_html = build_questions_html(questions)
    
    page_html = TEMPLATE
    page_html = page_html.replace('{{TITLE}}', title)
    page_html = page_html.replace('{{AUDIO_URL}}', audio_url)
    page_html = page_html.replace('{{QUESTIONS_HTML}}', q_html)
    page_html = page_html.replace('{{TRANSCRIPT_HTML}}', transcript_html)
    page_html = page_html.replace('{{CORRECT_ANSWERS_JSON}}', json.dumps(answers_map))
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(page_html)

def main():
    count = 0
    for level in LEVELS:
        level_dir = os.path.join(OUTPUT_DIR, level)
        if not os.path.exists(level_dir):
            continue
            
        for lesson_folder in os.listdir(level_dir):
            if lesson_folder.startswith('Lesson_'):
                html_path = os.path.join(level_dir, lesson_folder, 'index.html')
                if os.path.exists(html_path):
                    rebuild_lesson(html_path)
                    count += 1
    print(f"Successfully rebuilt {count} HTML files!")

if __name__ == '__main__':
    main()
