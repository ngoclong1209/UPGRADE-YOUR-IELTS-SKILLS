import os
import re

BASE_DIR = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"

CONFIG = [
    {
        "dirs": ["ReadingA1-C2"],
        "msg": "1,232 bài luyện tập đọc hiểu của bạn đã được VŨ NGỌC LONG TRẢ PHÍ 1,232,000 VND, được sử dụng trong thời hạn 1 năm."
    },
    {
        "dirs": ["pte-listening-audios/Basic", "pte-listening-audios/Intermediate", "pte-listening-audios/Advanced"],
        "msg": "102 bài nghe của bạn đã được VŨ NGỌC LONG TRẢ PHÍ 1,232,000 VND, được sử dụng trong thời hạn 1 năm."
    },
    {
        "dirs": ["practicepteonline/listening"],
        "msg": "204 listening test full của bạn đã được VŨ NGỌC LONG TRẢ PHÍ 1,232,000 VND, được sử dụng trong thời hạn 1 năm."
    },
    {
        "dirs": ["practicepteonline/reading"],
        "msg": "315 reading test full của bạn đã được VŨ NGỌC LONG TRẢ PHÍ 1,232,000 VND, được sử dụng trong thời hạn 1 năm."
    }
]

def update_file(filepath, msg):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # 1. Enable the login overlay by changing its inline style from display: none to display: flex
        content = re.sub(r'id="login-overlay"\s*style="([^"]*)display:\s*none;?', lambda m: f'id="login-overlay" style="{m.group(1)}display: flex;', content)
        
        # 2. Update the warning text
        # Find the div with background: #fff0f2 and replace its inner HTML starting with ⚠️ <b>LƯU Ý:</b>
        content = re.sub(
            r'(<div[^>]*>)\s*⚠️\s*<b>LƯU Ý:</b>.*?(</div>)',
            f'\\1\n                    ⚠️ <b>LƯU Ý:</b> {msg}\n                \\2',
            content,
            flags=re.DOTALL
        )
        
        # 3. Remove the LOGIN DISABLED block in DOMContentLoaded
        # It looks like:
        # window.addEventListener('DOMContentLoaded', () => {
        #     // LOGIN DISABLED - auto show content
        #     let overlay = document.getElementById('login-overlay');
        #     if(overlay) overlay.style.display = "none";
        #     ...
        #     if(typeof startTimer === 'function') startTimer();
        # });
        # We will replace it with an empty DOMContentLoaded or just remove the overlay hiding part.
        
        # Let's just find and remove the lines that hide the overlay
        content = re.sub(r"// LOGIN DISABLED - auto show content\s*let overlay = document\.getElementById\('login-overlay'\);\s*if\(overlay\) overlay\.style\.display = \"none\";", "", content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
            
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

total_updated = 0
for config in CONFIG:
    msg = config["msg"]
    for d in config["dirs"]:
        search_dir = os.path.join(BASE_DIR, d)
        if not os.path.exists(search_dir):
            continue
            
        for root, _, files in os.walk(search_dir):
            for file in files:
                if file.endswith('.html'):
                    filepath = os.path.join(root, file)
                    if update_file(filepath, msg):
                        total_updated += 1

print(f"Updated {total_updated} HTML files with custom login screens.")
