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

# Query a specific quiz details
quiz_id = 10129
urls = [
    f"https://api.youpass.vn/v1/quizzes/{quiz_id}",
    f"https://api.youpass.vn/v1/quizzes/practice/{quiz_id}",
    f"https://api.youpass.vn/v1/ielts/quizzes/{quiz_id}",
]

for url in urls:
    print(f"\nFetching quiz details from {url}...")
    r = requests.get(url, headers=headers)
    print("Status Code:", r.status_code)
    try:
        data = r.json()
        print("Keys:", list(data.keys()))
        if "data" in data:
            print("Data Keys:", list(data["data"].keys()))
            print("Snippet:", json.dumps(data["data"], indent=2)[:500])
    except Exception as e:
        print("Error parsing json:", e)
        print("Response snippet:", r.text[:200])
