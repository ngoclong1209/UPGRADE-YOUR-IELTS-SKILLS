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
        
        # 1. Restore overlay hiding in grantAccess
        content = re.sub(
            r'//\s*if\s*\(\s*overlay\s*\)\s*overlay\.style\.display\s*=\s*"none"\s*;',
            r'if(overlay) overlay.style.display = "none";\n                    let ml = document.getElementById("main-layout"); if(ml) ml.style.display = "flex";\n                    let ac = document.getElementById("audio-player-container"); if(ac) ac.style.display = "flex";\n                    let mh = document.getElementById("main-header"); if(mh) mh.style.display = "flex";\n                    let ct = document.querySelector(".container"); if(ct) ct.style.display = "block";',
            content
        )
        
        # 2. In DOMContentLoaded, we remove any display: "none" for main components and remove startTimer.
        # Let's find the entire DOMContentLoaded block and replace it.
        # It usually looks like:
        # window.addEventListener('DOMContentLoaded', () => { ... });
        
        def replace_dom_content_loaded(match):
            # We want to keep the block but remove problematic lines
            inner = match.group(1)
            # Remove startTimer
            inner = re.sub(r'if\s*\(\s*typeof\s*startTimer\s*===\s*[\'"]function[\'"]\s*\)\s*startTimer\(\s*\)\s*;?', '', inner)
            inner = re.sub(r'startTimer\(\s*\)\s*;?', '', inner)
            # Remove hiding logic
            inner = re.sub(r'let\s+mainLayout[^;]+;\s*if\(mainLayout\)\s*mainLayout\.style\.display\s*=\s*"none"\s*;', '', inner)
            inner = re.sub(r'let\s+audioContainer[^;]+;\s*if\(audioContainer\)\s*audioContainer\.style\.display\s*=\s*"none"\s*;', '', inner)
            inner = re.sub(r'let\s+mainHeader[^;]+;\s*if\(mainHeader\)\s*mainHeader\.style\.display\s*=\s*"none"\s*;', '', inner)
            inner = re.sub(r'let\s+container[^;]+;\s*if\(container\)\s*container\.style\.display\s*=\s*"none"\s*;', '', inner)
            
            # Remove showing logic in DOMContentLoaded (since they start visible or are handled by CSS, 
            # and if we need them hidden, they are behind overlay anyway. Better to just leave them default).
            inner = re.sub(r'let\s+mainLayout[^;]+;\s*if\(mainLayout\)\s*mainLayout\.style\.display\s*=\s*"flex"\s*;', '', inner)
            inner = re.sub(r'let\s+audioContainer[^;]+;\s*if\(audioContainer\)\s*audioContainer\.style\.display\s*=\s*"flex"\s*;', '', inner)
            inner = re.sub(r'let\s+mainHeader[^;]+;\s*if\(mainHeader\)\s*mainHeader\.style\.display\s*=\s*""\s*;', '', inner)
            
            # Hide them initially (so they don't show behind transparent things)
            return "window.addEventListener('DOMContentLoaded', () => {" + inner + """
        let ml = document.getElementById('main-layout'); if(ml) ml.style.display = 'none';
        let ac = document.getElementById('audio-player-container'); if(ac) ac.style.display = 'none';
        let mh = document.getElementById('main-header'); if(mh) mh.style.display = 'none';
        let ct = document.querySelector('.container'); if(ct) ct.style.display = 'none';
    });"""

        content = re.sub(r"window\.addEventListener\('DOMContentLoaded',\s*\(\)\s*=>\s*\{([\s\S]*?)\}\);", replace_dom_content_loaded, content)
        
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

print(f"Fixed display logic in {total} files.")
