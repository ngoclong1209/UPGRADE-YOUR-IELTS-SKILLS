import os
import re

BASE_DIR = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"

DIRS = [
    "ReadingA1-C2",
    "pte-listening-audios/Basic",
    "pte-listening-audios/Intermediate",
    "pte-listening-audios/Advanced",
    "practicepteonline/listening",
    "practicepteonline/reading"
]

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original = content
        
        # 1. grantAccess: show elements
        def replace_grant_access(m):
            # m.group(0) is the setTimeout callback block
            block = m.group(0)
            # Remove any existing display manipulation for layout to avoid duplication
            block = re.sub(r'let\s+(ml|ac|mh|ct|mainLayout|audioContainer|mainHeader|container)\s*=[^;]+;\s*if\([^\)]+\)\s*[a-zA-Z]+\.style\.display\s*=\s*["\'][^"\']+["\']\s*;', '', block)
            # Remove overlay hide logic to insert fresh
            block = re.sub(r'let\s+overlay\s*=[^;]+;\s*(//)?\s*if\(\s*overlay\s*\)\s*overlay\.style\.display\s*=\s*"none"\s*;', '', block)
            
            # insert fresh
            new_logic = """
                    let overlay = document.getElementById('login-overlay');
                    if(overlay) overlay.style.display = "none";
                    let ml = document.getElementById('main-layout'); if(ml) ml.style.display = 'flex';
                    let ac = document.getElementById('audio-player-container'); if(ac) ac.style.display = 'flex';
                    let mh = document.getElementById('main-header'); if(mh) mh.style.display = 'flex';
                    let ct = document.querySelector('.container'); if(ct) ct.style.display = 'block';
"""
            # Insert new_logic right after setTimeout(() => {
            return block.replace("setTimeout(() => {", "setTimeout(() => {" + new_logic)

        content = re.sub(r'setTimeout\(\(\)\s*=>\s*\{[\s\S]*?\},?\s*500\);', replace_grant_access, content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
            
        return False
    except Exception as e:
        print(f"Error {filepath}: {e}")
        return False

total = 0
for d in DIRS:
    search_dir = os.path.join(BASE_DIR, d)
    if not os.path.exists(search_dir): continue
    for root, _, files in os.walk(search_dir):
        for file in files:
            if file.endswith('.html'):
                if fix_file(os.path.join(root, file)):
                    total += 1

print(f"Fixed final grantAccess logic in {total} files.")
