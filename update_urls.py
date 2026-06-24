import os
import re

directories = [
    "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS/Listening_102_Basic",
    "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS/Reading_1232_Basic",
    "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS/Listening_204_FullTest"
]

NEW_URL = "https://script.google.com/macros/s/AKfycbw8ggCZFiONZQ6eSuMczrjEyIKcsGk1ZNeK8CUjdsiiAgDon_bz7m5WmA61_ESoiuJb/exec"

url_pattern = re.compile(r'https://script\.google\.com/macros/s/[a-zA-Z0-9_-]+/exec')

count = 0
for directory in directories:
    if not os.path.exists(directory):
        continue
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content, num_subs = url_pattern.subn(NEW_URL, content)
                    
                    if num_subs > 0:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        count += 1
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

print(f"Updated URLs in {count} files.")
