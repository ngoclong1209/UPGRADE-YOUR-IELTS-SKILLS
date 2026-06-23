import asyncio
import json
import os
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        print("Connecting to Chrome...")
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        pages = context.pages
        
        for page in pages:
            if "youpass.vn" in page.url:
                print(f"Found YouPass page: {page.url}")
                # Evaluate localStorage
                ls = await page.evaluate("() => JSON.stringify(localStorage)")
                ls_data = json.loads(ls)
                print("\nLocalStorage Keys:")
                for k, v in ls_data.items():
                    print(f" - {k}: {v[:100]}...")
                
                # Let's save this localStorage data specifically!
                # We can write it into our own session.json format
                cookies = await context.cookies()
                
                storage_state = {
                    "cookies": cookies,
                    "origins": [
                        {
                            "origin": "https://youpass.vn",
                            "localStorage": [
                                {"name": k, "value": v} for k, v in ls_data.items()
                            ]
                        }
                    ]
                }
                
                session_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "session.json"))
                with open(session_path, "w", encoding="utf-8") as f:
                    json.dump(storage_state, f, ensure_ascii=False, indent=2)
                print(f"\nSuccessfully saved full storage state to {session_path}")
                break
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
