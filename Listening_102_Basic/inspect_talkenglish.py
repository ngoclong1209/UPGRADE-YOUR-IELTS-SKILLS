import requests
from bs4 import BeautifulSoup

url = 'https://www.talkenglish.com/listening/lessonlisten.aspx?ALID=101'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

print("--- AUDIO ---")
for audio in soup.find_all('audio'):
    print(audio)
    
for a in soup.find_all('a', href=True):
    if a['href'].endswith('.mp3'):
        print("A-Tag Audio:", a['href'])

print("\n--- SCRIPT ---")
script_div = soup.find(id='script')
if script_div:
    print(script_div.text.strip()[:200] + "...")
else:
    # Try finding it differently
    for div in soup.find_all('div'):
        if 'script' in str(div.get('id', '')).lower() or 'script' in str(div.get('class', '')).lower():
            print("Found div:", div.get('id'), div.get('class'))

print("\n--- QUESTIONS ---")
# Questions are usually in a form or a specific div
q_div = soup.find(id='question')
if q_div:
    print(q_div.text.strip()[:200] + "...")
else:
    for div in soup.find_all('div'):
        if 'question' in str(div.get('id', '')).lower() or 'question' in str(div.get('class', '')).lower():
            print("Found question div:", div.get('id'), div.get('class'))
            
# Print the whole text to find clues if needed
# print(soup.get_text()[:500])
