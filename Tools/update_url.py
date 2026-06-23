import os
import glob
import re

new_url = "https://script.google.com/macros/s/AKfycbyxTfjW5Td-SAY5WOh9CsdaYM9iv4iJ6iYAvhr1ScgjF3FqYH-e_71xabgdWY6RRho/exec"

def update_files(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace any APP_URL assignment
                updated_content = re.sub(
                    r'const APP_URL = "https://script.google.com/macros/s/[^"]+/exec";',
                    f'const APP_URL = "{new_url}";',
                    content
                )
                
                if updated_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    count += 1
    print(f"Updated {count} files in {directory}")

update_files("/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS")
