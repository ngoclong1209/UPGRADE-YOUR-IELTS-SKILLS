import os
import json
import re
import requests
from bs4 import BeautifulSoup
from html_generator import save_html
from docx_generator import save_docx

SESSION_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "session.json"))
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

class YouPassScraper:
    def __init__(self):
        self.auth_token = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.load_session()
        
    def load_session(self):
        if not os.path.exists(SESSION_PATH):
            print(f"Error: {SESSION_PATH} not found. Please run login_cdp.py first.")
            return False
            
        with open(SESSION_PATH, 'r') as f:
            session = json.load(f)
            
        # Find auth_token in cookies
        for cookie in session.get('cookies', []):
            if cookie['name'] == 'auth_token':
                self.auth_token = cookie['value']
                break
                
        if self.auth_token:
            self.headers["Authorization"] = f"Bearer {self.auth_token}"
            print("Successfully loaded auth token from session.json.")
            return True
        else:
            print("Warning: auth_token cookie not found in session.json.")
            return False

    def clean_filename(self, text):
        # Keep alphanumeric, spaces, and hyphens, then replace spaces with underscores
        cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '', text)
        return cleaned.strip().replace(' ', '_')

    def scrape_quiz(self, quiz_id):
        print(f"\nScraping quiz {quiz_id}...")
        url = f"https://api.youpass.vn/v1/quizzes/{quiz_id}"
        r = requests.get(url, headers=self.headers)
        
        if r.status_code != 200:
            print(f"Failed to fetch quiz {quiz_id}. Status: {r.status_code}")
            return False
            
        data = r.json().get("data", {})
        if not data:
            print("No data field in response.")
            return False
            
        title = data.get("title", f"Quiz_{quiz_id}")
        quiz_type = data.get("type")
        
        # Map quiz type to skill
        # Type 1 and 9 -> Reading
        # Type 2 and 10 -> Listening
        # Type 7 -> Writing
        # Type 8 -> Speaking
        skill = "other"
        if quiz_type in [1, 9]:
            skill = "reading"
        elif quiz_type in [2, 10]:
            skill = "listening"
        elif quiz_type == 7:
            skill = "writing"
        elif quiz_type == 8:
            skill = "speaking"
            
        # Create scientific directory structure
        # data/<skill>/single/quiz_<id>_<title>/
        clean_title = self.clean_filename(title)
        folder_name = f"quiz_{quiz_id}_{clean_title}"
        folder_path = os.path.join(DATA_DIR, skill, "single", folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Process parts (Passages and questions)
        parts = data.get("parts", [])
        if not parts:
            print("No parts found in quiz.")
            return False
            
        # Gather all content and questions across parts
        full_content_html = ""
        all_questions = []
        
        for p_idx, part in enumerate(parts):
            part_title = part.get("title", f"Part {p_idx+1}")
            part_content = part.get("content") or ""
            
            full_content_html += f"<h3>{part_title}</h3>\n{part_content}\n"
            
            # Format questions
            questions = part.get("questions", [])
            for q in questions:
                q_id = q.get("order") or q.get("id") or len(all_questions) + 1
                q_text = q.get("title") or q.get("content") or f"Question {q_id}"
                
                # Determine question type
                api_type = q.get("type", "").upper()
                q_type = "fill-in-the-blank"
                options = []
                correct = ""
                
                if "RADIO" in api_type or "SINGLE" in api_type:
                    q_type = "single-choice"
                    radio_options = q.get("single_choice_radio") or []
                    for opt in radio_options:
                        txt = opt.get("text", "")
                        options.append(txt)
                        if opt.get("correct") is True:
                            correct = txt
                elif "MULTIPLE" in api_type or "CHECKBOX" in api_type:
                    q_type = "multiple-choice"
                    multi_options = q.get("mutilple_choice") or q.get("single_choice_radio") or []
                    correct = []
                    for opt in multi_options:
                        txt = opt.get("text", "")
                        options.append(txt)
                        if opt.get("correct") is True:
                            correct.append(txt)
                else:
                    # Gap fill / blanks
                    q_type = "fill-in-the-blank"
                    correct = q.get("correct_answer") or q.get("answer") or ""
                    
                explanation = q.get("explain") or q.get("description") or ""
                
                all_questions.append({
                    "id": q_id,
                    "text": q_text,
                    "type": q_type,
                    "options": options,
                    "correct_answer": correct,
                    "explanation": explanation
                })
                
        # Clean HTML to plain text for Word doc
        soup = BeautifulSoup(full_content_html, "html.parser")
        passage_text = soup.get_text(separator="\n")
        
        # Audio File (for Listening)
        has_audio = False
        audio_id = data.get("listening")
        if audio_id and skill == "listening":
            audio_url = f"https://cms.youpass.vn/assets/{audio_id}"
            audio_dest = os.path.join(folder_path, "audio.mp3")
            print(f"Downloading audio: {audio_url} ...")
            try:
                ar = requests.get(audio_url, headers=self.headers, stream=True)
                if ar.status_code == 200:
                    with open(audio_dest, 'wb') as f:
                        for chunk in ar.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Audio saved to {audio_dest}")
                    has_audio = True
                else:
                    print(f"Failed to download audio. Status: {ar.status_code}")
            except Exception as e:
                print(f"Error downloading audio: {e}")
                
        # Save HTML
        html_dest = os.path.join(folder_path, f"{folder_name}.html")
        save_html(html_dest, title, skill, full_content_html, all_questions, has_audio=has_audio)
        
        # Save DOCX
        docx_dest = os.path.join(folder_path, f"{folder_name}.docx")
        save_docx(docx_dest, title, skill, passage_text, all_questions)
        
        # Save raw JSON metadata for backup
        metadata_dest = os.path.join(folder_path, "metadata.json")
        with open(metadata_dest, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully scraped and saved quiz: {title}")
        return True

    def crawl_all_quizzes(self, limit=10):
        """Crawls quizzes catalog up to limit"""
        print(f"Crawling all quizzes list (limit {limit})...")
        url = "https://api.youpass.vn/v1/quizzes?page_size=50&page=1&status=published&is_test=true"
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            print("Failed to fetch quizzes list.")
            return
            
        quizzes = r.json().get("data", {}).get("items", [])
        print(f"Found {len(quizzes)} quizzes to process.")
        
        count = 0
        for item in quizzes:
            if count >= limit:
                break
            q_id = item.get("id")
            if q_id:
                try:
                    self.scrape_quiz(q_id)
                    count += 1
                except Exception as e:
                    print(f"Error processing quiz {q_id}: {e}")
                    
        print(f"\nFinished crawling {count} quizzes.")

if __name__ == "__main__":
    scraper = YouPassScraper()
    # Test scrape quiz 10129
    scraper.scrape_quiz(10129)
