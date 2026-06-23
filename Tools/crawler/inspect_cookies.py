import asyncio
from playwright.async_api import async_playwright

USER_DATA_DIR = "/tmp/chrome_dev_profile"
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

async def run():
    async with async_playwright() as p:
        print("Launching persistent Chrome...")
        context = await p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            executable_path=CHROME_PATH,
            headless=False
        )
        
        # Check context cookies
        cookies = await context.cookies()
        print("\nCookies in Playwright context:")
        for c in cookies:
            if 'youpass.vn' in c['domain']:
                print(f" - {c['name']}: {c['value'][:50]}... (domain: {c['domain']})")
                
        # Navigate to YouPass
        page = await context.new_page()
        await page.goto("https://youpass.vn/home")
        await page.wait_for_timeout(5000)
        print("Final URL:", page.url)
        
        # Get document.cookie in page
        cookie_str = await page.evaluate("() => document.cookie")
        print("\ndocument.cookie in page:")
        print(cookie_str)
        
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())
