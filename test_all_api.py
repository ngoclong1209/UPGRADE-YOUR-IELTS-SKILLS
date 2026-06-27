import os
import re
import json
import asyncio
import aiohttp

APP_URL = "https://script.google.com/macros/s/AKfycbwZV0v_osCIN3-6lZuXwmxaFlaMdNTFi4t0RYMxXL6Z6eUkPqpe2B4RJKJg2amP9uRJSg/exec"

def get_lessons():
    generated_lessons = []
    
    # 1. Reading_1232_Basic
    base_dir = "Reading_1232_Basic/frontend/data"
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.js'):
                folder = os.path.basename(root)
                lessonId = f"Reading {folder} - {file.replace('.js', '')}"
                generated_lessons.append(("submit_score", lessonId))

    # 2. Listening_102_Basic
    base_dir2 = "Listening_102_Basic"
    for root, dirs, files in os.walk(base_dir2):
        for file in files:
            if file.endswith('.html') and file != 'template.html':
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    match = re.search(r"lessonId:\s*['\"]([^'\"]+)['\"]", content)
                    if match:
                        generated_lessons.append(("submit_score", match.group(1)))

    # 3. Reading_315_FullTest
    base_dir3 = "Reading_315_FullTest"
    for root, dirs, files in os.walk(base_dir3):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    match = re.search(r"test_name:\s*['\"]([^'\"]+)['\"]", content)
                    if match:
                        generated_lessons.append(("submit_full_test", match.group(1), "Reading Full Test"))

    # 4. Listening_204_FullTest
    base_dir4 = "Listening_204_FullTest"
    for root, dirs, files in os.walk(base_dir4):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    match = re.search(r"test_name:\s*['\"]([^'\"]+)['\"]", content)
                    if match:
                        generated_lessons.append(("submit_full_test", match.group(1), "Listening Full Test"))

    return generated_lessons

async def send_request(session, sem, lesson):
    async with sem:
        if lesson[0] == "submit_score":
            payload = {
                "action": "submit_score",
                "userId": "long01",
                "deviceId": "test_script_dev",
                "lessonId": lesson[1],
                "score": "0/10",
                "percent": 0
            }
        else:
            payload = {
                "action": "submit_full_test",
                "student_id": "long01",
                "module": lesson[2],
                "test_name": lesson[1],
                "answers": [""] * 40
            }
            
        try:
            async with session.post(APP_URL, json=payload, headers={'Content-Type': 'text/plain;charset=utf-8'}, ssl=False) as resp:
                text = await resp.text()
                try:
                    data = json.loads(text)
                    return (lesson, data.get('status'), data.get('message'))
                except:
                    return (lesson, "error", "Invalid JSON: " + text[:50])
        except Exception as e:
            return (lesson, "error", str(e))

async def main():
    lessons = get_lessons()
    print(f"Testing {len(lessons)} lessons...")
    sem = asyncio.Semaphore(10) # limit concurrent requests
    
    # Use connector with ssl=False
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [send_request(session, sem, l) for l in lessons]
        results = await asyncio.gather(*tasks)
        
    success_count = 0
    not_in_plan_count = 0
    max_attempts_count = 0
    other_errors = {}
    
    for (l, status, msg) in results:
        if status == 'success':
            success_count += 1
        else:
            if "không có trong kế hoạch" in str(msg):
                not_in_plan_count += 1
            elif "MAX_ATTEMPTS_REACHED" in str(msg):
                max_attempts_count += 1
            else:
                other_errors[msg] = other_errors.get(msg, 0) + 1

    print(f"Tested {len(results)} lessons.")
    print(f"Success (Appended / Checked in sheet): {success_count}")
    print(f"Max Attempts Reached (Found in sheet but full): {max_attempts_count}")
    print(f"Not in plan (Failed lookup): {not_in_plan_count}")
    print(f"Other errors: {other_errors}")
    
    if not_in_plan_count > 0:
        print("\nSaving failed lessons to failed_lessons.txt")
        with open('failed_lessons.txt', 'w') as f:
            for (l, status, msg) in results:
                if "không có trong kế hoạch" in str(msg):
                    f.write(str(l) + "\n")

asyncio.run(main())
