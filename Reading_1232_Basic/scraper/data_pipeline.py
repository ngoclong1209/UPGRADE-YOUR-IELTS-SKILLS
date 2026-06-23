import os
import json
import time
from openai import OpenAI

# 1. Config API Key
OPENAI_API_KEY = "YOUR_API_KEY_HERE"

class OpenAIGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate_with_retry(self, prompt, max_retries=5):
        for attempt in range(max_retries):
            try:
                print("⏳ Đang gửi request tới OpenAI GPT-4o-mini...")
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a professional IELTS test creator. You output strictly valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={ "type": "json_object" },
                    temperature=0.7,
                    max_tokens=10000,
                    timeout=120
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e:
                print(f"⚠️ OpenAI API Error: {e}. Đợi 10s trước khi thử lại (Lần {attempt+1}/{max_retries})...")
                time.sleep(10)
        
        print("❌ Đã thử tối đa số lần nhưng thất bại. Bỏ qua bài này.")
        return None

class PipelineManager:
    def __init__(self):
        self.generator = OpenAIGenerator(OPENAI_API_KEY)
        
    def read_instructions(self, level):
        file_map = {
            "A1-A2": "../Reading A1-A2.md",
            "B1-B2": "../Reading B1-B2.md",
            "C1-C2": "../Reading C1-C2.md"
        }
        with open(file_map[level], "r", encoding="utf-8") as f:
            return f.read()

    def load_topics(self):
        return [
            "Higher education vs Vocational training",
            "Online learning / Distance education",
            "Climate change & Global warming",
            "Artificial Intelligence & Robotics",
            "Space Exploration",
            "Renewable Energy",
            "Public Transportation vs Private Cars",
            "The Role of the Internet in Modern Society",
            "Tourism and its Impacts",
            "Health and Diet"
        ]

    def build_prompt(self, level, topic, lesson_num):
        instructions = self.read_instructions(level)
        
        return f"""
        Act as an expert IELTS test creator. Create a Reading Test for level {level}.
        Topic: {topic}
        
        Follow these strict guidelines exactly:
        {instructions}
        
        Return ONLY a valid JSON object matching this exact structure (no markdown fences, just JSON):
        {{
            "test_id": "reading_{level.lower().replace('-','_')}_{lesson_num:03d}",
            "title": "Catchy title related to {topic}",
            "level": "{level}",
            "time_limit": 1200,
            "passage": "<h2>Passage Title</h2><p>HTML formatted passage here.</p>",
            "questions": [
                {{
                    "id": "q1",
                    "type": "multiple_choice",
                    "instruction": "Choose the correct letter, A, B, C or D.",
                    "text": "Question text",
                    "options": {{"A": "opt 1", "B": "opt 2", "C": "opt 3", "D": "opt 4"}},
                    "answer": "A",
                    "explanation": "Detailed explanation of why A is correct based on the passage."
                }}
            ],
            "vocabulary": [
                {{"word": "word1", "meaning": "definition in context"}}
            ],
            "tactics": "<h2>Hướng dẫn</h2><p>Specific tips for this passage...</p>"
        }}
        """

    def update_index(self, level, data, file_path):
        index_file = "../frontend/data/index.json"
        
        # Load existing index or create new
        if os.path.exists(index_file):
            try:
                with open(index_file, "r", encoding="utf-8") as f:
                    index_data = json.load(f)
            except json.JSONDecodeError:
                index_data = {"A1-A2": [], "B1-B2": [], "C1-C2": []}
        else:
            index_data = {"A1-A2": [], "B1-B2": [], "C1-C2": []}
            
        # Check if already in index
        relative_path = file_path.replace("../frontend/", "")
        existing = next((item for item in index_data.get(level, []) if item["file"] == relative_path), None)
        
        if not existing:
            if level not in index_data:
                index_data[level] = []
            
            index_data[level].append({
                "id": data.get("test_id", ""),
                "title": data.get("title", ""),
                "file": relative_path
            })
            
            # Save index.json
            with open(index_file, "w", encoding="utf-8") as f:
                json.dump(index_data, f, ensure_ascii=False, indent=2)
                
            # Save index_data.js for JSONP support
            index_js = "../frontend/data/index_data.js"
            with open(index_js, "w", encoding="utf-8") as f:
                f.write("window.indexData = " + json.dumps(index_data, ensure_ascii=False, indent=2) + ";\n")
                f.write("if(typeof onIndexDataLoaded === 'function') onIndexDataLoaded(window.indexData);\n")

    def run(self):
        topics = self.load_topics()
        
        target_allocation = {
            "A1-A2": 198,
            "B1-B2": 374,
            "C1-C2": 660
        }
        
        for level, total_lessons in target_allocation.items():
            out_dir = f"../frontend/data/{level}"
            os.makedirs(out_dir, exist_ok=True)
            
            for i in range(1, total_lessons + 1):
                file_path = os.path.join(out_dir, f"lesson_{i:03d}.json")
                
                # Checkpoint Check
                if os.path.exists(file_path):
                    print(f"⏩ Skipping {file_path} (Already exists)")
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        self.update_index(level, data, file_path)
                    except Exception as e:
                        print(f"⚠️ Error updating index for {file_path}: {e}")
                    continue
                
                # Assign topic round-robin
                topic = topics[(i-1) % len(topics)]
                
                print(f"🚀 Generating Lesson {i}/{total_lessons} for {level} (Topic: {topic})")
                prompt = self.build_prompt(level, topic, i)
                
                data = self.generator.generate_with_retry(prompt)
                
                if data:
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    js_path = file_path.replace(".json", ".js")
                    with open(js_path, "w", encoding="utf-8") as f:
                        f.write("window.lessonData = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")
                        f.write("if(typeof onLessonDataLoaded === 'function') onLessonDataLoaded(window.lessonData);\n")
                    
                    print(f"✅ Saved -> {file_path} and {js_path}")
                    
                    # Update index
                    self.update_index(level, data, file_path)
                
                # Sleep briefly to not overwhelm the API 
                # (GPT-4o-mini is very fast, but 1s helps prevent sudden spikes)
                time.sleep(1)
                
        print("🎉 PIPELINE FINISHED!")

if __name__ == "__main__":
    manager = PipelineManager()
    manager.run()
