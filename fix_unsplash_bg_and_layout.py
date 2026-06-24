import os

base_dir = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"
files_to_update = [
    "Reading_1232_Basic/frontend/template_reading.html",
    "Reading_1232_Basic/frontend/index.html"
]

# Add all Listening_102_Basic files
for root, dirs, files in os.walk(os.path.join(base_dir, "Listening_102_Basic")):
    for file in files:
        if file.endswith('.html'):
            files_to_update.append(os.path.relpath(os.path.join(root, file), base_dir))

for rel_path in files_to_update:
    file_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # REMOVE THE RANDOM BACKGROUND LOGIC
    target_1 = "let randomBg = backgrounds[Math.floor(Math.random() * backgrounds.length)];"
    target_2 = "if(overlay) overlay.style.backgroundImage = `url(${randomBg})`;"
    target_3 = "if(overlay) overlay.style.backgroundImage = 'url(' + randomBg + ')';"

    content = content.replace(target_1, "// Removed random background logic")
    content = content.replace(target_2, "// Removed background image setting")
    content = content.replace(target_3, "// Removed background image setting")

    # FIX LISTENING LAYOUT: answer-pane (left) should be 60%, passage-pane (right) should be 1
    if "Listening_102_Basic" in rel_path:
        content = content.replace(".passage-pane {\n            flex: 0 0 60%;\n        }", ".passage-pane {\n            flex: 1;\n        }")
        content = content.replace(".answer-pane {\n            flex: 1;\n        }", ".answer-pane {\n            flex: 0 0 60%;\n        }")
        
        content = content.replace(".passage-pane { flex: 0 0 60%; }", ".passage-pane { flex: 1; }")
        content = content.replace(".answer-pane { flex: 1; }", ".answer-pane { flex: 0 0 60%; }")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done fixing background and layout!")
