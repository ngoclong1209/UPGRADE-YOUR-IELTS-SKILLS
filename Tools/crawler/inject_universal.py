import os
import re

BASE_DIR = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"

DIRS = [
    ("ReadingA1-C2", "1232 bài luyện tập đọc hiểu"),
    ("pte-listening-audios/Basic", "102 bài nghe"),
    ("pte-listening-audios/Intermediate", "102 bài nghe"),
    ("pte-listening-audios/Advanced", "102 bài nghe"),
    ("practicepteonline/listening", "204 listening test full"),
    ("practicepteonline/reading", "315 reading test full")
]

with open("overlay_css.txt", "r", encoding="utf-8") as f:
    css_content = f.read()

with open("overlay_html.txt", "r", encoding="utf-8") as f:
    html_content = f.read()

with open("overlay_js.txt", "r", encoding="utf-8") as f:
    js_content = f.read()

def inject_file(filepath, module_text):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original = content
        
        css_pattern = r'\.login-overlay\s*\{.*?(?:\.theme-[a-zA-Z0-9_-]+\s+\.login-input\s*\{.*?\}|\/\*\s*5\.\s*Pixie Theme\s*\*\/\s*\.login-overlay\.theme-pixie.*?\.theme-pixie \.login-input\s*\{.*?\})'
        if re.search(css_pattern, content, re.DOTALL | re.IGNORECASE):
            content = re.sub(css_pattern, css_content, content, count=1, flags=re.DOTALL | re.IGNORECASE)
        else:
            if "</head>" in content:
                content = content.replace("</head>", f"<style>\n{css_content}\n</style>\n</head>")
                
        custom_html = html_content.replace(
            '<div style="font-size: 1.1rem; font-weight: 700; color: #ff5e7e; margin-bottom: 12px; border-bottom: 2px dashed rgba(0,0,0,0.1); padding-bottom: 8px; text-align: center;">🎫 THÔNG TIN HỌC LIỆU & THANH TOÁN</div>',
            '<div style="font-size: 1.1rem; font-weight: 700; color: #ff5e7e; margin-bottom: 12px; border-bottom: 2px dashed rgba(0,0,0,0.1); padding-bottom: 8px; text-align: center;">🎫 THÔNG TIN THANH TOÁN</div>'
        )
        
        old_payment_details = r'<div style="font-size: 0\.95rem; line-height: 1\.6; color: #333;">\s*<p style="margin: 6px 0;">💵 <b>Bài luyện tập:.*?</div>'
        new_payment_details = f'''<div style="font-size: 1rem; line-height: 1.6; color: #333; text-align: center;">
                        ⚠️ Toàn bộ <b>{module_text}</b> của bạn đã được <b>VŨ NGỌC LONG</b> TRẢ PHÍ <b style="color: #e91e63;">1,599,000 VND</b>, được sử dụng trong thời hạn 1 năm.
                    </div>'''
        custom_html = re.sub(old_payment_details, new_payment_details, custom_html, flags=re.DOTALL)
        
        html_pattern = r'<div class="login-overlay"[^>]*>.*?</div>\s*</div>\s*</div>'
        if re.search(html_pattern, content, re.DOTALL):
            content = re.sub(html_pattern, custom_html, content, count=1, flags=re.DOTALL)
        else:
            html_pattern_alt = r'<div class="login-overlay"[^>]*>.*?<div id="login-loading-fields".*?</div>\s*</div>\s*</div>'
            if re.search(html_pattern_alt, content, re.DOTALL):
                content = re.sub(html_pattern_alt, custom_html, content, count=1, flags=re.DOTALL)
            elif "<body>" in content:
                content = content.replace("<body>", f"<body>\n<!-- UNIFIED LOGIN OVERLAY -->\n{custom_html}\n")
        
        js_grant_pattern = r'(async\s+)?function\s+grantAccess\s*\(\)\s*\{.*?\n\s*\}'
        content = re.sub(js_grant_pattern, '', content, flags=re.DOTALL)
        
        js_complete_pattern = r'function\s+completeLogin\s*\([^\)]*\)\s*\{.*?\n\s*\}'
        content = re.sub(js_complete_pattern, '', content, flags=re.DOTALL)
        
        js_dom_pattern = r'window\.addEventListener\(\'DOMContentLoaded\',\s*\(\)\s*=>\s*\{.*?(?:let\s+ml\s*=\s*document\.getElementById\(\'main-layout\'\).*?|if\s*\(typeof\s+initLogin).*?\n\s*\}\);'
        content = re.sub(js_dom_pattern, '', content, flags=re.DOTALL)
        
        if "</script>" in content:
            parts = content.rsplit("</script>", 1)
            content = parts[0] + "\n" + js_content + "\n</script>" + parts[1]
            
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
            
        return False
    except Exception as e:
        print(f"Error {filepath}: {e}")
        return False

total = 0
for d, module_text in DIRS:
    search_dir = os.path.join(BASE_DIR, d)
    if not os.path.exists(search_dir): continue
    for root, _, files in os.walk(search_dir):
        for file in files:
            if file.endswith('.html') or file.endswith('.htm'):
                if inject_file(os.path.join(root, file), module_text):
                    total += 1

print(f"Fixed login interface in {total} files.")
