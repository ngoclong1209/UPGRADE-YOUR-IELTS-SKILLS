import asyncio
import os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

USER_DATA_DIR = "/tmp/chrome_dev_profile"
DEBUG_DIR = "/Users/vungoclong/Desktop/Antigravity/Youpass.vn/debug"

async def run():
    os.makedirs(DEBUG_DIR, exist_ok=True)
    async with async_playwright() as p:
        print(f"Launching persistent browser context from {USER_DATA_DIR}...")
        # Launch persistent context
        context = await p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=True
        )
        page = await context.new_page()
        
        url = "https://youpass.vn/luyen-thi/ielts/listening?quiz_type=quiz&status=unfinished&passage=35"
        print(f"Navigating to {url}...")
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(8000)
        except Exception as e:
            print("Navigation warn:", e)
            
        # Check title and print text
        title = await page.title()
        print("Page Title:", title)
        
        # Save screenshot
        screenshot_path = os.path.join(DEBUG_DIR, "persistent_screenshot.png")
        await page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
        
        # Check if questions or sections are present
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Look for "Đăng nhập" button
        has_login = False
        for btn in soup.find_all('button'):
            if 'Đăng nhập' in btn.get_text():
                has_login = True
                break
                
        if has_login:
            print("Status: NOT LOGGED IN (found Đăng nhập button)")
        else:
            print("Status: LOGGED IN! (Đăng nhập button not found)")
            
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())
