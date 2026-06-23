import requests
from bs4 import BeautifulSoup
import re

url = "https://practicepteonline.com/ielts-listening-tests-ielts-listening-practice-test-ielts-listening-pdf-ielts-cambridge-test/"
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(r.text, 'html.parser')

print("All links in content:")
links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    txt = a.get_text().strip()
    # Check if links are related to tests
    if any(k in href.lower() for k in ['test', 'practice', 'listening', 'reading', 'cambridge']):
        links.append((href, txt))

# Remove duplicates while keeping order
seen = set()
unique_links = []
for href, txt in links:
    if href not in seen:
        seen.add(href)
        unique_links.append((href, txt))

print(f"Found {len(unique_links)} unique links:")
for idx, (href, txt) in enumerate(unique_links[:100]):
    print(f" {idx}. href: {href} | text: {txt}")
