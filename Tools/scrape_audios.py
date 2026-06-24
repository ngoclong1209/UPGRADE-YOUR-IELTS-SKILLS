import os
import time
import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_audio_url(test_num):
    url = f"https://practicepteonline.com/ielts-listening-test-{test_num}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        audio_tags = soup.find_all('audio')
        for audio in audio_tags:
            src = audio.get('src')
            if not src:
                source = audio.find('source')
                if source:
                    src = source.get('src')
            if src:
                return urllib.parse.urljoin(url, src)
    except Exception as e:
        print(f"Error fetching test {test_num}: {e}")
    return None

def download_audio(url, path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        with requests.get(url, headers=headers, stream=True, timeout=15) as r:
            r.raise_for_status()
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    base_dir = "Listening_204_FullTest"
    if not os.path.exists(base_dir):
        print(f"Base dir {base_dir} not found!")
        return

    # There are up to 204 tests, but let's just check the existing folders
    for test_num in range(1, 205):
        test_dir = os.path.join(base_dir, f"Test_{test_num}")
        if not os.path.isdir(test_dir):
            continue
            
        audio_path = os.path.join(test_dir, f"audio_{test_num}.mp3")
        if os.path.exists(audio_path):
            print(f"Test {test_num}: Audio already exists.")
            continue
            
        print(f"Test {test_num}: Fetching URL...")
        audio_url = get_audio_url(test_num)
        if not audio_url:
            print(f"Test {test_num}: No audio URL found.")
            continue
            
        print(f"Test {test_num}: Downloading from {audio_url}...")
        success = download_audio(audio_url, audio_path)
        if success:
            print(f"Test {test_num}: Downloaded successfully.")
        else:
            print(f"Test {test_num}: Download failed.")
        
        # Polite delay
        time.sleep(1)

if __name__ == "__main__":
    main()
