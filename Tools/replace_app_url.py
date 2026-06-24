import os
import re

NEW_URL = 'https://script.google.com/macros/s/AKfycbw8ggCZFiONZQ6eSuMczrjEyIKcsGk1ZNeK8CUjdsiiAgDon_bz7m5WmA61_ESoiuJb/exec'
TARGET_DIRS = [
    "Reading_1232_Basic",
    "Listening_102_Basic",
    "Reading_315_FullTest",
    "Listening_204_FullTest"
]

def replace_in_dir(directory):
    count = 0
    pattern = re.compile(r'const\s+APP_URL\s*=\s*"https://script\.google\.com/macros/s/[^"]+/exec";')
    replacement = f'const APP_URL = "{NEW_URL}";'
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if pattern.search(content):
                    new_content = pattern.sub(replacement, content)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
    return count

total = 0
for d in TARGET_DIRS:
    print(f"Scanning {d}...")
    c = replace_in_dir(d)
    print(f"Updated {c} files in {d}")
    total += c

print(f"Total files updated: {total}")
