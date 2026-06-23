import asyncio
import os
from playwright.async_api import async_playwright

USER_DATA_DIR = "/tmp/chrome_dev_profile"

async def run():
    async with async_playwright() as p:
        print("Launching persistent browser...")
        context = await p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=True
        )
        page = await context.new_page()
        
        url = "https://youpass.vn/luyen-thi/ielts/listening?quiz_type=quiz&status=unfinished&passage=35"
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(10000)
        
        # Let's check for audio tags
        audio_tags = await page.locator("audio").count()
        print("Audio tags found:", audio_tags)
        
        # Let's print all paragraph texts on the page to see if the passage text is there!
        paragraphs = await page.locator("p").all_inner_texts()
        print(f"Found {len(paragraphs)} paragraph elements.")
        print("Paragraphs snippet:")
        for p_text in paragraphs[:20]:
            p_clean = p_text.strip().replace('\n', ' ')
            if p_clean:
                print(" -", p_clean[:120])
                
        # Let's check for question elements (usually have classes or text)
        inputs = await page.locator("input").count()
        print("Input elements found:", inputs)
        
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())
