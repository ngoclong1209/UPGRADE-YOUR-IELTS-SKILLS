import asyncio
import json
import os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

SESSION_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "crawler", "session.json"))
DEBUG_DIR = "/Users/vungoclong/Desktop/Antigravity/Youpass.vn/debug"

async def run():
    os.makedirs(DEBUG_DIR, exist_ok=True)
    
    with open(SESSION_PATH, 'r') as f:
        session_data = json.load(f)
        
    auth_token = None
    for cookie in session_data.get('cookies', []):
        if cookie['name'] == 'auth_token':
            auth_token = cookie['value']
            break
            
    if not auth_token:
        print("Error: auth_token not found in session.json")
        return
        
    async with async_playwright() as p:
        print("Launching headless Chromium...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        
        # Inject cookie
        await context.add_cookies([
            {
                "name": "auth_token",
                "value": auth_token,
                "domain": ".youpass.vn",
                "path": "/",
                "secure": True,
                "httpOnly": False
            }
        ])
        print("Injected auth_token cookie.")
        
        page = await context.new_page()
        
        url = "https://youpass.vn/luyen-thi/ielts/listening?quiz_type=quiz&status=unfinished&passage=35"
        print(f"Navigating to {url}...")
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(8000)
        except Exception as e:
            print("Navigation warn:", e)
            
        # Check login status
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        
        has_login = False
        for btn in soup.find_all('button'):
            if 'Đăng nhập' in btn.get_text():
                has_login = True
                break
                
        if has_login:
            print("Status: NOT LOGGED IN (found Đăng nhập button)")
            # Save debug HTML to see what's on screen
            with open(os.path.join(DEBUG_DIR, "inject_fail.html"), "w") as f:
                f.write(content)
        else:
            print("Status: LOGGED IN! (Đăng nhập button not found)")
            with open(os.path.join(DEBUG_DIR, "inject_success.html"), "w") as f:
                f.write(content)
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
