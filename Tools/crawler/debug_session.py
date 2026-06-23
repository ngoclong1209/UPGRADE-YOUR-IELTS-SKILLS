import asyncio
import os
from playwright.async_api import async_playwright

SESSION_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "crawler", "session.json"))
DEBUG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "debug"))

async def run():
    os.makedirs(DEBUG_DIR, exist_ok=True)
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=SESSION_PATH)
        page = await context.new_page()
        
        url = "https://youpass.vn/luyen-thi/ielts/listening?quiz_type=quiz&status=unfinished&passage=35"
        print(f"Navigating to {url}...")
        try:
            # wait_until='domcontentloaded' is much faster and less prone to analytics timeouts
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
        except Exception as e:
            print("Navigation warning:", e)
            
        print("Waiting for page load details...")
        await page.wait_for_timeout(8000)
        
        # Save screenshot and HTML
        screenshot_path = os.path.join(DEBUG_DIR, "screenshot.png")
        html_path = os.path.join(DEBUG_DIR, "page.html")
        
        await page.screenshot(path=screenshot_path)
        content = await page.content()
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"Screenshot saved to {screenshot_path}")
        print(f"HTML saved to {html_path}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
