import os
import glob

BASE_DIR = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"
DIRS = [
    os.path.join(BASE_DIR, "Listening_102_Basic"),
    os.path.join(BASE_DIR, "Reading_1232_Basic")
]

def inject_files():
    for d in DIRS:
        if not os.path.exists(d):
            continue
        html_files = glob.glob(os.path.join(d, "**", "*.html"), recursive=True)
        for filepath in html_files:
            # Calculate depth relative to BASE_DIR
            rel_path = os.path.relpath(filepath, BASE_DIR)
            depth = len(rel_path.split(os.sep)) - 1
            
            # depth 1 = root folder, e.g. Reading_1232_Basic/index.html (needs ../Assets)
            # depth 2 = e.g. Reading_1232_Basic/frontend/index.html (needs ../../Assets)
            # depth 3 = e.g. Listening_102_Basic/Basic/Lesson_1/index.html (needs ../../../Assets)
            
            back_steps = "../" * depth
            
            CSS_LINK = f'<link rel="stylesheet" href="{back_steps}Assets/highlighter.css">'
            JS_LINK = f'<script src="{back_steps}Assets/highlighter.js"></script>'
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            modified = False
            
            # Remove any wrong paths injected previously (e.g. strict ../../)
            WRONG_CSS_LINK = '<link rel="stylesheet" href="../../Assets/highlighter.css">'
            WRONG_JS_LINK = '<script src="../../Assets/highlighter.js"></script>'
            if WRONG_CSS_LINK in content and depth != 2:
                content = content.replace(WRONG_CSS_LINK, '')
            if WRONG_JS_LINK in content and depth != 2:
                content = content.replace(WRONG_JS_LINK, '')
                
            if CSS_LINK not in content:
                content = content.replace('</head>', f'    {CSS_LINK}\n</head>')
                modified = True
                
            if JS_LINK not in content:
                content = content.replace('</body>', f'    {JS_LINK}\n</body>')
                modified = True
                
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Injected correctly: {filepath} with depth {depth}")

if __name__ == "__main__":
    inject_files()
