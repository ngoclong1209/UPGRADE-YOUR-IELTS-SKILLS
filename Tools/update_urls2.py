import os
import re

def update_urls(root_dir, new_url):
    pattern = re.compile(r"const WEB_APP_URL = 'https://script\.google\.com/macros/s/[a-zA-Z0-9_-]+/exec';")
    replacement = f"const WEB_APP_URL = '{new_url}';"
    
    count = 0
    for dirpath, _, filenames in os.walk(root_dir):
        if '.git' in dirpath:
            continue
            
        for filename in filenames:
            if filename.endswith('.html') or filename.endswith('.js'):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    new_content, num_subs = pattern.subn(replacement, content)
                    
                    if num_subs > 0:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        count += 1
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
                    
    print(f"Updated URL in {count} files.")

if __name__ == "__main__":
    new_url = "https://script.google.com/macros/s/AKfycbwpA-N8yVVDrmFD4pZRkDpwOGqDJYLA_LSwh0WVrnL6rPxw4ionhhEAfV2b0df_hJaH/exec"
    update_urls(".", new_url)
