import asyncio
import json
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
                
                # Check document.cookie
                cookie_str = await page.evaluate("() => document.cookie")
                print("\ndocument.cookie:")
                print(cookie_str)
                
                # Check sessionStorage
                ss = await page.evaluate("() => JSON.stringify(sessionStorage)")
                print("\nsessionStorage:")
                print(json.dumps(json.loads(ss), indent=2))
                
                # Check IndexedDB databases
                idb = await page.evaluate("""async () => {
                    if (!window.indexedDB.databases) return 'not supported';
                    const dbs = await window.indexedDB.databases();
                    return dbs.map(d => d.name);
                }""")
                print("\nIndexedDB Databases:")
                print(idb)
                
                # Let's inspect IndexedDB keys if there are any databases
                if isinstance(idb, list) and len(idb) > 0:
                    for db_name in idb:
                        print(f"Database: {db_name}")
                        # We can dump object store names or search for keys
                break
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
