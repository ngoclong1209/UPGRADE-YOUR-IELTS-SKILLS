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
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(8000)
        
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all text and print elements that look like exercise list items
        # Usually they are inside cards or grids
        print("\nListing all text blocks that look like exercises:")
        for div in soup.find_all(['div', 'a', 'p']):
            txt = div.get_text().strip()
            # If the text matches Cambridge or Test or Passage followed by number
            if re.search(r'(cambridge|test|passage|section)\s*\d+', txt, re.IGNORECASE):
                # Only print unique short lines
                lines = [line.strip() for line in txt.split('\n') if line.strip()]
                for line in lines:
                    if len(line) < 100:
                        print(" -", line)
                        
        await browser.close()

import re
if __name__ == "__main__":
    asyncio.run(run())
