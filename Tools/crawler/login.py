import asyncio
import json
import os
from playwright.async_api import async_playwright

SESSION_PATH = os.path.join(os.path.dirname(__file__), "session.json")

async def run():
    async with async_playwright() as p:
        print("Launching browser. Please log in manually in the opened window...")
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto("https://youpass.vn/luyen-thi/ielts/listening")
        
        print("\n" + "="*60)
        print("INSTRUCTIONS:")
        print("1. Log in using Google or Email in the browser window.")
        print("2. Navigate to any IELTS practice exercise to ensure session is active.")
        print("3. Return to this terminal and press ENTER to save session state.")
        print("="*60 + "\n")
        
        input("Press Enter here AFTER you have successfully logged in...")
        
        # Extract cookies and localStorage
        storage_state = await context.storage_state()
        
        # Save to session.json
        with open(SESSION_PATH, "w", encoding="utf-8") as f:
            json.dump(storage_state, f, ensure_ascii=False, indent=2)
            
        print(f"Session state saved successfully to {SESSION_PATH}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
