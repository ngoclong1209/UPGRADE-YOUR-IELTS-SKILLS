import asyncio
import os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

USER_DATA_DIR = "/tmp/chrome_dev_profile"
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DEBUG_DIR = "/Users/vungoclong/Desktop/Antigravity/Youpass.vn/debug"

async def run():
    os.makedirs(DEBUG_DIR, exist_ok=True)
    async with async_playwright() as p:
        print(f"Launching persistent headful Chrome context from {USER_DATA_DIR}...")
        
        # Kill any stray Chrome first
        os.system("pkill -f 'Google Chrome'")
        await asyncio.sleep(1)
        
        # Launch persistent context using system Google Chrome (headless=False)
        context = await p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            executable_path=CHROME_PATH,
            headless=False
        )
        page = await context.new_page()
        
        url = "https://youpass.vn/luyen-thi/ielts/listening?quiz_type=quiz&status=unfinished&passage=35"
        print(f"Navigating to {url}...")
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(8000)
        except Exception as e:
            print("Navigation warn:", e)
            
        title = await page.title()
        print("Page Title:", title)
        
        # Save screenshot
        screenshot_path = os.path.join(DEBUG_DIR, "persistent_headful_chrome_screenshot.png")
        await page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
        
        content = await page.content()
        with open(os.path.join(DEBUG_DIR, "chrome_headful_page.html"), "w", encoding="utf-8") as f:
            f.write(content)
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check login status
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
