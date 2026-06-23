import asyncio
import json
import os
from playwright.async_api import async_playwright

SESSION_PATH = os.path.join(os.path.dirname(__file__), "session.json")

async def run():
    async with async_playwright() as p:
        print("Connecting to running Google Chrome instance on port 9222...")
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            print("Connected successfully!")
        except Exception as e:
            print(f"Error: Could not connect to Chrome: {e}")
            return

        contexts = browser.contexts
        if not contexts:
            print("No contexts found.")
            return
            
        context = contexts[0]
        pages = context.pages
        page = None
        
        print("Open tabs in Chrome:")
        for p_obj in pages:
            print(f" - {p_obj.url}")
            if "youpass.vn" in p_obj.url:
                page = p_obj
                
        if not page:
            print("\nWARNING: No tab found with 'youpass.vn' in the URL.")
            print("Please open a tab in Chrome, go to youpass.vn, log in, and leave the tab open.")
            print("Once done, the script will wait and detect it.")
            
            # Poll for the tab to appear
            for _ in range(30):
                await asyncio.sleep(2)
                pages = context.pages
                for p_obj in pages:
                    if "youpass.vn" in p_obj.url:
                        page = p_obj
                        print(f"Detected YouPass tab: {page.url}")
                        break
                if page:
                    break
                    
        if not page:
            print("Failed to find YouPass tab after waiting.")
            return
            
        print("\nSaving session from YouPass tab...")
        # Get cookies and storage
        storage_state = await context.storage_state()
        
        with open(SESSION_PATH, "w", encoding="utf-8") as f:
            json.dump(storage_state, f, ensure_ascii=False, indent=2)
            
        print(f"Session state saved successfully to {SESSION_PATH}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
