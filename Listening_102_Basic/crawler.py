import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import re

LEVELS = {
    'Basic': 'https://www.talkenglish.com/listening/listenbasic.aspx',
    'Intermediate': 'https://www.talkenglish.com/listening/listenintermediate.aspx',
    'Advanced': 'https://www.talkenglish.com/listening/listenadvanced.aspx'
}

BASE_URL = 'https://www.talkenglish.com'
OUTPUT_DIR = '.'

with open('template.html', 'r', encoding='utf-8') as f:
    TEMPLATE = f.read()

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser')

def crawl_lesson_list(url):
    soup = get_soup(url)
    lessons = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'lessonlisten.aspx' in href.lower():
            full_url = urllib.parse.urljoin(BASE_URL + '/listening/', href)
            title = a.text.strip()
            lessons.append({'title': title, 'url': full_url})
    
    seen = set()
    unique_lessons = []
    for l in lessons:
        if l['url'] not in seen:
            seen.add(l['url'])
            unique_lessons.append(l)
            
    return unique_lessons

def crawl_lesson_data(url):
    soup = get_soup(url)
    
    # 1. Audio
    audio_url = None
    for audio in soup.find_all('audio'):
        for src in audio.find_all('source'):
            if src['src'].endswith('.mp3'):
                audio_url = urllib.parse.urljoin(BASE_URL, src['src'])
                break
        if audio_url: break
    
    if not audio_url:
        for a in soup.find_all('a', href=True):
            if a['href'].endswith('.mp3'):
                audio_url = urllib.parse.urljoin(BASE_URL, a['href'])
                break
                
    # 2. Transcript
    transcript_html = ""
    div3 = soup.find(id='div3')
    if div3:
        # Get inner HTML
        transcript_html = "".join(str(item) for item in div3.contents).strip()
    
    # 3. Questions and Answers
    questions_data = []
    correct_answers_map = {}
    div1 = soup.find(id='div1')
    if div1:
        # Extract correct answers
        ans_input = div1.find('input', {'name': 'CorrectAnswers'})
        if ans_input:
            ans_str = ans_input.get('value', '')
            for i, char in enumerate(ans_str):
                correct_answers_map[f'q{i+1}'] = char.lower()
        
        # We need to parse questions manually because HTML is unstructured (just <br> tags)
        # Convert div1 to string and split by <br />
        # But bs4 might have parsed <br/> as <br/>
        html_str = "".join(str(c) for c in div1.contents)
        # Hacky but effective regex for talkenglish specific format
        q_blocks = re.split(r'(?=\d+\.\s)', html_str)
        
        q_idx = 1
        for block in q_blocks:
            if re.match(r'^\d+\.', block.strip()):
                # This block starts with a number. e.g. "1. What day... <br> <input ...> a ... <br>"
                lines = [l.strip() for l in re.split(r'<br\s*/?>', block) if l.strip()]
                
                if not lines: continue
                q_text = lines[0] # "1. What day..."
                
                options = []
                for line in lines[1:]:
                    if '<input' in line and 'type="radio"' in line:
                        # Extract value and text
                        val_match = re.search(r'value="(.*?)"', line)
                        if val_match:
                            val = val_match.group(1)
                            # The text is everything after the >
                            text_part = re.sub(r'<input.*?>', '', line).strip()
                            options.append({'value': val, 'text': text_part})
                
                if options:
                    questions_data.append({
                        'id': f'q{q_idx}',
                        'text': q_text,
                        'options': options
                    })
                    q_idx += 1
                
    return {
        'audio_url': audio_url,
        'transcript': transcript_html,
        'questions': questions_data,
        'answers': correct_answers_map
    }

def build_questions_html(questions):
    html = []
    for q in questions:
        q_id = q['id']
        html.append(f'<div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">')
        html.append(f'  <h3 class="text-lg font-medium text-gray-900 mb-4">{q["text"]}</h3>')
        html.append(f'  <div class="space-y-3">')
        for opt in q['options']:
            val = opt['value']
            text = opt['text']
            html.append(f'    <label class="option-label flex items-center p-4 border border-gray-200 rounded-xl cursor-pointer">')
            html.append(f'      <input type="radio" name="{q_id}" value="{val}" class="w-5 h-5 text-indigo-600 focus:ring-indigo-500 border-gray-300">')
            html.append(f'      <span class="ml-3 block text-gray-700">{val.upper()}. {text}</span>')
            html.append(f'    </label>')
        html.append(f'  </div>')
        html.append(f'</div>')
    return "\n".join(html)

def download_file(url, path):
    if os.path.exists(path):
        return # Skip if already downloaded
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

def main():
    for level, url in LEVELS.items():
        print(f"Crawling level: {level}")
        level_dir = os.path.join(OUTPUT_DIR, level)
        os.makedirs(level_dir, exist_ok=True)
        
        lessons = crawl_lesson_list(url)
        print(f"Found {len(lessons)} lessons for {level}")
        
        for i, lesson in enumerate(lessons):
            lesson_folder = f"Lesson_{i+1}"
            lesson_dir = os.path.join(level_dir, lesson_folder)
            os.makedirs(lesson_dir, exist_ok=True)
            
            print(f"  Fetching: {lesson['title']} ({lesson['url']})")
            data = crawl_lesson_data(lesson['url'])
            
            if data['audio_url']:
                audio_ext = data['audio_url'].split('.')[-1]
                audio_filename = f"audio.{audio_ext}"
                audio_path = os.path.join(lesson_dir, audio_filename)
                print(f"    Downloading audio...")
                download_file(data['audio_url'], audio_path)
            else:
                audio_filename = ""
                
            # Render HTML
            q_html = build_questions_html(data['questions'])
            
            page_html = TEMPLATE
            page_html = page_html.replace('{{TITLE}}', lesson['title'])
            page_html = page_html.replace('{{LEVEL}}', level)
            page_html = page_html.replace('{{AUDIO_URL}}', audio_filename)
            page_html = page_html.replace('{{QUESTIONS_HTML}}', q_html)
            page_html = page_html.replace('{{TRANSCRIPT_HTML}}', data['transcript'])
            page_html = page_html.replace('{{CORRECT_ANSWERS_JSON}}', json.dumps(data['answers']))
            
            html_path = os.path.join(lesson_dir, 'index.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(page_html)
                
            print(f"    Saved {html_path}")
            
        # Optional: slow down requests slightly if needed
        import time
        time.sleep(1)

if __name__ == '__main__':
    main()
