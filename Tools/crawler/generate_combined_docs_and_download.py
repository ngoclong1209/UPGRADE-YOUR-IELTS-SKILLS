import os
import requests
import time
from docx import Document
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = "/Users/vungoclong/Desktop/Antigravity/Youpass.vn/data/practicepteonline"
AUDIO_DIR = os.path.join(BASE_DIR, "listening_audios")

os.makedirs(AUDIO_DIR, exist_ok=True)

def download_audio(i):
    url = f"https://cdn.jsdelivr.net/gh/ngoclong1209/pte-listening-audios/Test_{i}/audio_{i}.mp3"
    dest_path = os.path.join(AUDIO_DIR, f"audio_{i}.mp3")
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000000:
        print(f"Audio {i} already exists and is valid. Skipping.")
        return
    
    max_retries = 5
    backoff = 2
    for attempt in range(max_retries):
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                with open(dest_path, "wb") as f:
                    f.write(r.content)
                print(f"Downloaded audio {i}")
                return
            elif r.status_code == 404:
                # If 404, maybe it's named audio.mp3?
                alt_url = f"https://cdn.jsdelivr.net/gh/ngoclong1209/pte-listening-audios/Test_{i}/audio.mp3"
                r_alt = requests.get(alt_url, timeout=30)
                if r_alt.status_code == 200:
                    with open(dest_path, "wb") as f:
                        f.write(r_alt.content)
                    print(f"Downloaded audio {i} (from alt URL)")
                    return
                print(f"Failed audio {i}: HTTP 404 on both URLs")
                return
            else:
                print(f"Attempt {attempt+1} for audio {i} failed: HTTP {r.status_code}")
        except Exception as e:
            print(f"Attempt {attempt+1} for audio {i} error: {e}")
        time.sleep(backoff)
        backoff *= 2
    print(f"Failed to download audio {i} after {max_retries} attempts.")

print("Starting concurrent audio downloads with retry logic...")
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(download_audio, range(1, 101))

# Function to merge documents
def merge_docx_files(test_type, output_name):
    print(f"Merging {test_type} tests 1-100...")
    merged_doc = Document()
    first = True
    
    for i in range(1, 101):
        docx_path = os.path.join(BASE_DIR, test_type, f"Test_{i}", f"Test_{i}.docx")
        if not os.path.exists(docx_path):
            print(f"Warning: {docx_path} does not exist. Skipping.")
            continue
            
        print(f"Appending {test_type} Test {i}...")
        sub_doc = Document(docx_path)
        
        if not first:
            merged_doc.add_page_break()
        first = False
        
        # Append elements
        for element in sub_doc.element.body:
            merged_doc.element.body.append(element)
            
    output_path = os.path.join(BASE_DIR, output_name)
    merged_doc.save(output_path)
    print(f"Saved merged docx to {output_path}")

try:
    merge_docx_files("listening", "listening_1_100.docx")
    merge_docx_files("reading", "reading_1_100.docx")
except Exception as e:
    print(f"Error merging files: {e}")
