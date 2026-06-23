import requests
from bs4 import BeautifulSoup
import re

url = "https://practicepteonline.com/ielts-listening-test-1/"
print("Fetching:", url)
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
print("Status:", r.status_code)
print("Length of body:", len(r.text))

soup = BeautifulSoup(r.text, 'html.parser')

# Check for audio files
audios = []
for aud in soup.find_all(['audio', 'source']):
    src = aud.get('src')
    if src:
        audios.append(src)
print("\nAudio URLs found:")
for src in set(audios):
    print(" -", src)

# Check for download links or direct mp3 links
mp3s = re.findall(r'href=\"([^\"]+\.mp3)\"', r.text)
print("\nDirect MP3 links found in hrefs:")
for src in set(mp3s):
    print(" -", src)

# Let's inspect the page content text structure (first 2000 chars of entry-content)
content_div = soup.find(class_=re.compile(r'entry-content|post-content|content'))
if content_div:
    print("\nContent Div found! Text preview (first 1000 chars):")
    # Decompose script/style
    for s in content_div(['style', 'script']):
        s.decompose()
    print(content_div.get_text()[:1500])
else:
    print("\nNo content div found.")
