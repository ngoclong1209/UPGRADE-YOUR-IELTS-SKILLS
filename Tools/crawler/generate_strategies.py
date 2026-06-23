import os
import re
import json
import base64
import time
import requests
from bs4 import BeautifulSoup

DATA_DIR = "/Users/vungoclong/Desktop/Antigravity/Youpass.vn/data/practicepteonline"

# 4 User-provided free API keys for rotation
API_KEYS = [
    "AIzaSyA4vuWPz06w99UP552xbsBDFA7N0IJ-FU0",
    "AIzaSyCxWLlomNMVoi5uOEijVfIOQMdrjaRLv7g",
    "AIzaSyB4_8QnRSmUMn2-jpOpEwGpKs6G3MMftl8",
    "AIzaSyBN1dRn8bY0vXoE2WD6BT92tw5joeSpGYM"
]

def get_next_key(index):
    return API_KEYS[index % len(API_KEYS)]

def generate_strategy_for_test(test_folder, test_type, idx_num, initial_key_index):
    html_path = os.path.join(test_folder, f"Test_{idx_num}.html")
    strategy_path = os.path.join(test_folder, "strategies.json")
    
    if os.path.exists(strategy_path):
        return initial_key_index
        
    if not os.path.exists(html_path):
        return initial_key_index
        
    print(f"Generating missing strategies for {test_type.capitalize()} Test {idx_num}...")
    
    # Read the current HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    # Extract passage/description content
    passage_el = soup.find(class_="content-html")
    passage_text = passage_el.get_text() if passage_el else ""
    
    # Extract answers
    answers = []
    script_tags = soup.find_all('script')
    for script in script_tags:
        if script.text and 'const answers = ' in script.text:
            m = re.search(r'const answers\s*=\s*(\[.*?\]);', script.text, re.DOTALL)
            if m:
                try:
                    answers = json.loads(m.group(1))
                except Exception as e:
                    print(f"Error parsing answers json: {e}")
                    
    if not answers:
        print(f"No answers found for {html_path}. Skipping.")
        return initial_key_index

    # Prepare prompt payloads
    parts_payload = []
    if test_type == "listening":
        audio_filename = f"audio_{idx_num}.mp3"
        audio_path = os.path.join(test_folder, audio_filename)
        if os.path.exists(audio_path):
            try:
                print(f"Encoding audio {audio_filename} to Base64...")
                with open(audio_path, "rb") as af:
                    base64_audio = base64.b64encode(af.read()).decode('utf-8')
                parts_payload.append({
                    "inlineData": {
                        "mimeType": "audio/mp3",
                        "data": base64_audio
                    }
                })
                print("Audio successfully loaded.")
            except Exception as e:
                print(f"Error reading audio file: {e}")

    prompt = f"""
You are a 9.0/9.0 IELTS expert. Analyze this {test_type} exercise and its correct answers.
Generate an elite, question-level test-taking strategy/tactic for EACH question from Q1 to Q{len(answers)}.

Exercise Text / Context:
\"\"\"
{passage_text[:6000]}
\"\"\"

Correct Answers:
{json.dumps(answers, ensure_ascii=False)}

For each question index (1-based), generate a JSON object with:
- "type_tip": An elite, short general trick for this question type (e.g. T/F/NG, Gap fill, MCQ). Do NOT reveal the answer here.
- "scan_target": Specific keywords to scan in the text/audio. 
  * If Reading: Name the keywords and locate the exact paragraph/sentence (e.g. "Scan for 'economic crisis' in Paragraph 2").
  * If Listening: Transcribe the EXACT TAPE SCRIPT snippet / sentence from the audio where the answer is spoken.
- "analysis_logic": How to logically match keywords or avoid trap options. Keep it under 2 sentences.

Output MUST be a JSON array of objects matching the size of the answers array.
Example Output Format:
[
  {{
    "q_num": 1,
    "type_tip": "For True/False/Not Given, identify qualifiers like 'only' or 'often'.",
    "scan_target": "Locate 'early civilization' in Paragraph 1: 'The dawn of early civilization began in...'",
    "analysis_logic": "Compare the text's assertion with the question statement to see if they contradict."
  }}
]
"""
    parts_payload.append({"text": prompt})
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": parts_payload}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    # Retry loop with key rotation
    max_retries = 8
    key_idx = initial_key_index
    
    for attempt in range(max_retries):
        api_key = get_next_key(key_idx)
        print(f"Attempt {attempt+1}/{max_retries} using Key index {key_idx % len(API_KEYS)} ({api_key[:8]}...)")
        
        # Call gemini-flash-latest (which maps to Gemini 1.5 Flash stable with fresh quota)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
        
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=180)
            if r.status_code == 200:
                res_data = r.json()
                text_response = res_data['candidates'][0]['content']['parts'][0]['text']
                text_response = re.sub(r'^```json\s*', '', text_response.strip())
                text_response = re.sub(r'\s*```$', '', text_response)
                
                strategies = json.loads(text_response)
                with open(strategy_path, 'w', encoding='utf-8') as sf:
                    json.dump(strategies, sf, ensure_ascii=False, indent=2)
                print(f"Successfully saved strategies for {test_folder}")
                return key_idx + 1 # Proceed key index
            elif r.status_code == 429:
                print(f"Rate limited (429) for key {api_key[:8]}... Rotating key and waiting...")
                key_idx += 1
                time.sleep(12) # Wait longer for limit cooling
            else:
                print(f"API Error ({r.status_code}): {r.text}. Retrying with next key...")
                key_idx += 1
                time.sleep(5)
        except Exception as e:
            print(f"Exception on attempt: {e}. Retrying with next key...")
            key_idx += 1
            time.sleep(5)
            
    print(f"Failed to generate strategies for {test_folder} after {max_retries} attempts.")
    return key_idx

def main():
    key_idx = 0
    
    for test_type in ["listening", "reading"]:
        type_dir = os.path.join(DATA_DIR, test_type)
        if not os.path.exists(type_dir):
            continue
        
        folders = [f for f in os.listdir(type_dir) if os.path.isdir(os.path.join(type_dir, f)) and f.startswith("Test_")]
        
        def get_num(name):
            try:
                return int(name.split('_')[1])
            except:
                return 9999
        folders.sort(key=get_num)
        
        for folder in folders:
            idx_num = get_num(folder)
            if idx_num > 20:
                continue # Limit to first 20 tests
                
            test_folder = os.path.join(type_dir, folder)
            strategy_path = os.path.join(test_folder, "strategies.json")
            
            if os.path.exists(strategy_path):
                continue
                
            try:
                key_idx = generate_strategy_for_test(test_folder, test_type, idx_num, key_idx)
                # Polite gap between tests
                time.sleep(10)
            except Exception as e:
                print(f"Error in outer loop for {folder}: {e}")

if __name__ == "__main__":
    main()
