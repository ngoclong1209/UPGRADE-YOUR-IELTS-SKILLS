import re

with open('template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update WEB_APP_URL
old_url_pattern = r'const WEB_APP_URL = [\'"].*?[\'"];'
new_url = "const WEB_APP_URL = 'https://script.google.com/macros/s/AKfycbybyRTHMhPAbeYWfGbzAS3bZBukleErbcuiFSc2gQ443ezOkAZolL3ES0oOsWWIUbi5Bw/exec';"
content = re.sub(old_url_pattern, new_url, content)

# 2. Fix the input ID
content = content.replace("document.getElementById('student-id-input')", "document.getElementById('student-name-input')")
# Make sure the button ID is correct. The button in HTML is just `<button onclick="saveStudentId()">` (no ID).
# In JS, I did: `const btn = document.getElementById('save-student-btn');`. Let's add the ID to the button.
content = content.replace('<button onclick="saveStudentId()">Bắt đầu làm bài</button>', '<button id="save-student-btn" onclick="saveStudentId()">Bắt đầu làm bài</button>')

# 3. Add console.log for debugging
content = content.replace("document.addEventListener('DOMContentLoaded', () => {", "document.addEventListener('DOMContentLoaded', () => {\n            console.log('DOM Loaded!');")

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Template fixed!")
