import requests
import json

SESSION_PATH = "/Users/vungoclong/Desktop/Antigravity/Youpass.vn/crawler/session.json"

with open(SESSION_PATH, 'r') as f:
    session = json.load(f)

auth_token = None
for cookie in session.get('cookies', []):
    if cookie['name'] == 'auth_token':
        auth_token = cookie['value']
        break

headers = {
    "Authorization": f"Bearer {auth_token}",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

types_map = {}

page = 1
while True:
    url = f"https://api.youpass.vn/v1/quizzes?page_size=100&page={page}&status=published&is_test=true"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        items = data.get("data", {}).get("items", [])
        if not items:
            print(f"Finished at page {page}")
            break
        print(f"Page {page} fetched {len(items)} items.")
        for item in items:
            t = item.get("type")
            title = item.get("title")
            if t not in types_map:
                types_map[t] = []
            types_map[t].append(title)
        page += 1
    else:
        print(f"Error page {page}: {r.status_code}")
        break

print("\nAll Unique Types Found across the entire system:")
for t, titles in types_map.items():
    print(f"Type {t}: total_count={len(titles)}, samples={titles[:5]}")
