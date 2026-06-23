import asyncio
import json
import os
from playwright.async_api import async_playwright

SESSION_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "crawler", "session.json"))

async def run():
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
        print("Launching browser context...")
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
        
        # Listen to requests/responses
        context.on("request", lambda request: print(f"-> {request.method} {request.url[:150]}"))
        context.on("response", lambda response: print(f"<- {response.status} {response.url[:150]}"))
        
        page = await context.new_page()
        
        url = "https://youpass.vn/luyen-thi/ielts/listening?quiz_type=quiz&status=unfinished&passage=35"
        print(f"Navigating to {url}...")
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            print("Page navigated. Waiting for dynamic requests...")
            await page.wait_for_timeout(10000)
        except Exception as e:
            print("Err:", e)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
