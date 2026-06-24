import re

# Read build_full_tests.py
with open('Tools/build_full_tests.py', 'r') as f:
    content = f.read()

css_match = re.search(r'LOGIN_CSS\s*=\s*"""(.*?)"""', content, re.DOTALL)
html_match = re.search(r'LOGIN_HTML_TMPL\s*=\s*"""(.*?)"""', content, re.DOTALL)
js_match = re.search(r'LOGIN_JS\s*=\s*"""\s*<script>(.*?)</script>\s*"""', content, re.DOTALL)

if not (css_match and html_match and js_match):
    print("Failed to find one of the components")
    exit(1)

css = css_match.group(1)
html = html_match.group(1)
js = js_match.group(1)

# Now read inject_basic_login.py and replace the constants
with open('Tools/inject_basic_login.py', 'r') as f:
    inject_content = f.read()

# Replace CSS
inject_content = re.sub(r'LOGIN_CSS\s*=\s*""".*?"""', f'LOGIN_CSS = """<style>{css}</style>"""', inject_content, flags=re.DOTALL)

# Replace HTML
inject_content = re.sub(r'LOGIN_HTML_TMPL\s*=\s*""".*?"""', f'LOGIN_HTML_TMPL = """{html}"""', inject_content, flags=re.DOTALL)

# Replace JS
inject_content = re.sub(r'LOGIN_JS\s*=\s*""".*?"""', f'LOGIN_JS = """{js}"""', inject_content, flags=re.DOTALL)

with open('Tools/inject_basic_login.py', 'w') as f:
    f.write(inject_content)

print("Successfully updated inject_basic_login.py")
