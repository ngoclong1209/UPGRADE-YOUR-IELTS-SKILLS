import re

path = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS/practicepteonline/reading/Test_1/Test_1.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

css_match = re.search(r'(\.login-overlay\s*\{.*?\/\*\s*5\.\s*Pixie Theme\s*\*\/\s*\.login-overlay\.theme-pixie.*?\.theme-pixie \.login-input\s*\{.*?\})', content, re.DOTALL | re.IGNORECASE)
html_match = re.search(r'(<div class="login-overlay" id="login-overlay">.*?</div>\s*</div>\s*</div>)', content, re.DOTALL)

if css_match:
    with open("overlay_css.txt", "w") as f:
        f.write(css_match.group(1))
if html_match:
    with open("overlay_html.txt", "w") as f:
        f.write(html_match.group(1))

print("Extracted", "CSS" if css_match else "NO CSS", "HTML" if html_match else "NO HTML")
