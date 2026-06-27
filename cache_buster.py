import os
import re

CACHE_META = """
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
"""

# HTML files to update
targets = [
    "Reading_1232_Basic/frontend/index.html",
    "Reading_1232_Basic/frontend/template_reading.html",
    "Listening_102_Basic/template.html",
    # Note: FullTest uses individual HTML files. We will run a mass replace on all .html files.
]

def add_cache_meta(content):
    if "Cache-Control" not in content:
        # Insert after <head>
        content = re.sub(r'(<head[^>]*>)', r'\1' + CACHE_META, content, flags=re.IGNORECASE)
    return content

count = 0
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = add_cache_meta(content)
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
            except Exception as e:
                print(f"Error on {path}: {e}")

print(f"Added cache-busting meta tags to {count} HTML files.")
