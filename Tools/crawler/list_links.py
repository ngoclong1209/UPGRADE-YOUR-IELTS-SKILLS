import asyncio
import json
import os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

SESSION_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "crawler", "session.json"))

async def run():
    with open(SESSION_PATH, 'r') as f:
        session_data = json.load(f)
        
    auth_token = None
    for cookie in session_data.get('cookies', []):
        if cookie['name'] == 'auth_token':
            auth_token = cookie['value']
            break
            
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        
        if auth_token:
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
            
        page = await context.new_page()
        url = "https://youpass.vn/luyen-thi/ielts/listening?quiz_type=quiz&status=unfinished"
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(8000)
        
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        
        print("\nAll links on the page:")
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text().strip().replace('\n', ' ')
            # Print links that point to tests/quizzes
            if any(k in href for k in ['passage', 'quiz', 'mocktest']):
                print(f" - href: {href} | text: {text[:80]}")
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
