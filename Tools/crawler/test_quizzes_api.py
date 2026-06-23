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

# Query the quizzes API
url = "https://api.youpass.vn/v1/quizzes?page_size=20&page=1&types=2&types=10&status=published&is_test=true"
print(f"Fetching quizzes from {url}...")
r = requests.get(url, headers=headers)
print("Status Code:", r.status_code)
try:
    data = r.json()
    print("Data keys:", list(data.keys()))
    if "data" in data:
        items = data["data"]
        print(f"Number of quizzes returned: {len(items)}")
        if len(items) > 0:
            print("First quiz item details:")
            print(json.dumps(items[0], indent=2)[:1000])
except Exception as e:
    print("Error:", e)
    print("Response snippet:", r.text[:200])
