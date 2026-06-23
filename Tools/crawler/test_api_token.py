import requests
import json
import os

SESSION_PATH = "/Users/vungoclong/Desktop/Antigravity/Youpass.vn/crawler/session.json"

with open(SESSION_PATH, 'r') as f:
    session = json.load(f)

auth_token = None
# Find auth_token from cookies
for cookie in session.get('cookies', []):
    if cookie['name'] == 'auth_token':
        auth_token = cookie['value']
        break

if not auth_token:
    print("Could not find auth_token in session.json cookies.")
    # Try localStorage
    for origin in session.get('origins', []):
        for item in origin.get('localStorage', []):
            if item['name'] == 'auth_token':
                auth_token = item['value']
                break

if not auth_token:
    print("No auth_token found.")
    exit(1)

print("Using auth_token:", auth_token[:50] + "...")

headers = {
    "Authorization": f"Bearer {auth_token}",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Let's try to query the passage 35
urls = [
    "https://cms.youpass.vn/items/passage/35",
    "https://cms.youpass.vn/items/questions?filter[passage][_eq]=35",
]

for url in urls:
    print(f"\nFetching {url}...")
    r = requests.get(url, headers=headers)
    print("Status Code:", r.status_code)
    try:
        data = r.json()
        print("Data keys:", list(data.keys()))
        if "data" in data:
            if isinstance(data["data"], list):
                print(f"Items returned: {len(data['data'])}")
                if len(data['data']) > 0:
                    print("Sample item:", json.dumps(data["data"][0], indent=2)[:500])
            else:
                print("Data fields:", list(data["data"].keys()))
                print("Title:", data["data"].get("title"))
                print("Content length:", len(data["data"].get("content", "")))
                print("Audio ID:", data["data"].get("audio"))
    except Exception as e:
        print("Error parsing json:", e)
        print("Response text snippet:", r.text[:200])
