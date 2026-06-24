import os
import re

def update_css_and_js(content):
    # 1. Update backgrounds and borders to Hello Kitty theme
    content = re.sub(r'background:\s*linear-gradient\(135deg,\s*#87ceeb\s*0%,\s*#e0f7fa\s*100%\);', r'background: linear-gradient(135deg, #ffe6ea 0%, #fdfbfb 100%);', content)
    content = re.sub(r'background:\s*#d7ccc8;\s*border:\s*5px\s*solid\s*#8d6e63;', r'background: rgba(255, 255, 255, 0.95); border: 5px solid #ffb6c1;', content)
    content = re.sub(r'background:\s*rgba\(129,\s*199,\s*132,\s*0\.5\);', r'background: rgba(255, 182, 193, 0.5);', content)
    content = re.sub(r'color:\s*#2e7d32;', r'color: #ff85a2;', content)
    
    # 2. Update flex ratio to 3:1 (75% and 25%)
    content = re.sub(r'flex:\s*0\s*0\s*83\.33%;', r'flex: 0 0 75%;', content)
    
    # 3. Add cloud-blank and cloud-badge CSS if not present
    if '.cloud-badge' not in content:
        cloud_css = """
        .cloud-badge {
            display: inline-block; background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
            color: #fff; font-weight: bold; font-size: 0.95em; padding: 3px 12px;
            border-radius: 20px; box-shadow: 0 4px 10px rgba(255, 154, 158, 0.4);
            margin: 0 5px; vertical-align: text-bottom; font-family: 'DynaPuff', cursive;
        }
        .cloud-blank {
            display: inline-block; width: 60px; height: 24px;
            background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
            border: 2px dashed #ff9a9e; border-radius: 12px; margin: 0 5px;
            vertical-align: bottom; box-shadow: inset 0 2px 5px rgba(0,0,0,0.05);
        }
        """
        content = content.replace('</style>', cloud_css + '\n    </style>')
    else:
        # Update existing cloud-badge colors
        content = re.sub(r'background:\s*linear-gradient\(135deg,\s*#a1c4fd.*?100%\);', r'background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);', content)
        content = re.sub(r'color:\s*#1a4a7b;', r'color: #fff;', content)
        content = re.sub(r'border:\s*2px\s*dashed\s*#a1c4fd;', r'border: 2px dashed #ff9a9e;', content)

    # 4. Inject JS to format blanks dynamically on load for the left pane
    js_formatter = r"""
        // Auto-format blanks and badges
        let leftPane = document.getElementById('left-pane') || document.querySelector('.passage-pane');
        if (leftPane) {
            let html = leftPane.innerHTML;
            html = html.replace(/(?<!<[^>]*)\b([1-3]?[0-9]|40)\.(?![^<]*>)/g, '<span class="cloud-badge">$1</span>');
            html = html.replace(/(?<!<[^>]*)\(([1-3]?[0-9]|40)\)(?![^<]*>)/g, '<span class="cloud-badge">$1</span>');
            html = html.replace(/_{3,}|\.{3,}/g, '<span class="cloud-blank"></span>');
            leftPane.innerHTML = html;
        }
    """
    if '// Auto-format blanks and badges' not in content:
        content = content.replace('</body>', f'    <script>{js_formatter}</script>\n</body>')
        
    return content

p102 = 'Listening_102_Basic/template.html'
if os.path.exists(p102):
    with open(p102, 'r') as f: c = f.read()
    c = update_css_and_js(c)
    with open(p102, 'w') as f: f.write(c)

p1232 = 'Reading_1232_Basic/frontend/template_reading.html'
if os.path.exists(p1232):
    with open(p1232, 'r') as f: c = f.read()
    c = update_css_and_js(c)
    with open(p1232, 'w') as f: f.write(c)

print("Done updating 102 and 1232 templates.")
