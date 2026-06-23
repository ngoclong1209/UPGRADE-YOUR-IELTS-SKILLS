import asyncio
import json
import os
from playwright.async_api import async_playwright

SESSION_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "crawler", "session.json"))

async def run():
    async with async_playwright() as p:
        print("Launching browser to inspect requests...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=SESSION_PATH)
        page = await context.new_page()
        
        # Intercept and log all requests & responses
        page.on("request", lambda request: print(f"-> {request.method} {request.url[:120]}"))
        page.on("response", lambda response: print(f"<- {response.status} {response.url[:120]}"))
        
        url = "https://youpass.vn/luyen-thi/ielts/listening?quiz_type=quiz&status=unfinished&passage=35"
        print(f"Navigating to {url}...")
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(10000)
        except Exception as e:
            print("Err:", e)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
