import os
import re

directories = [
    'Listening_102_Basic',
    'Reading_1232_Basic'
]

count = 0
for directory in directories:
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                new_content = re.sub(r'(\.passage-pane\s*\{[^}]*?)flex:\s*\d+;', r'\1flex: 0 0 60%;', content, count=0)
                new_content = re.sub(r'(\.answer-pane\s*\{[^}]*?)flex:\s*\d+;', r'\1flex: 1 1 40%;', content, count=0)
                
                if new_content != content:
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    count += 1

print(f"Updated {count} HTML files with new flex ratios.")
