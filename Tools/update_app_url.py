import os
import re

new_url = "https://script.google.com/macros/s/AKfycbwK8uWktQHrSoCVdiBzqAZj0SsT5_FxxCksG2s0Iga-Ye1DF40l7h5-xgI_7Kk40YLn/exec"

def update_files(root_dir):
    count = 0
    pattern = re.compile(r'https://script\.google\.com/macros/s/[A-Za-z0-9_-]+/exec')
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                new_content, num_subs = pattern.subn(new_url, content)
                
                if num_subs > 0:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    count += 1
    return count

total = 0
for d in ["Listening_204_FullTest", "Reading_315_FullTest", "Listening_102_Basic", "Reading_1232_Basic"]:
    if os.path.exists(d):
        c = update_files(d)
        print(f"Updated {c} files in {d}")
        total += c

print(f"Total files updated: {total}")
