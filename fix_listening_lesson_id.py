import os
import re

base_dir = '/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS/Listening_102_Basic'

count = 0
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file == 'index.html':
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find something like: lessonId: 'Basic Listening Lesson #01'
            # and replace it with: lessonId: 'Basic_Lesson_1'
            
            def replacer(match):
                level = match.group(1) # Basic, Intermediate, Advanced
                num = int(match.group(2)) # 01 -> 1
                return f"lessonId: '{level}_Lesson_{num}'"

            new_content = re.sub(r"lessonId:\s*'([^' ]+) Listening Lesson #(\d+)'", replacer, content)

            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1

print(f"Fixed {count} files.")
