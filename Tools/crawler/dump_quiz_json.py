import requests
import json
import os

SESSION_PATH = "/Users/vungoclong/Desktop/Antigravity/Youpass.vn/crawler/session.json"

with open(SESSION_PATH, 'r') as f:
    session = json.load(f)

auth_token = None
for cookie in session.get('cookies', []):
    if cookie['name'] == 'auth_token':
        auth_token = cookie['value']
        break

if not auth_token:
    print("No token found.")
    exit(1)

headers = {
    "Authorization": f"Bearer {auth_token}",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Fetch details of quiz 10129 and save to file
url = "https://api.youpass.vn/v1/quizzes/10129"
r = requests.get(url, headers=headers)
if r.status_code == 200:
    data = r.json()
    os.makedirs("/Users/vungoclong/Desktop/Antigravity/Youpass.vn/debug", exist_ok=True)
    dest = "/Users/vungoclong/Desktop/Antigravity/Youpass.vn/debug/quiz_10129.json"
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved quiz details to {dest}")
else:
    print("Failed to fetch. Status:", r.status_code)
