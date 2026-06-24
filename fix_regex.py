import os
import re

file_path = 'Tools/build_full_tests.py'
with open(file_path, 'r') as f:
    content = f.read()

# Badges regex to allow any 1 or 2 digit numbers
content = content.replace(r'([1-3]?[0-9]|40)', r'([0-9]{1,2})')

# Blanks regex to allow 2 or more
content = content.replace(r'_{3,}|\.{3,}', r'_{2,}|\.{3,}')

with open(file_path, 'w') as f:
    f.write(content)

print("Fixed regex in build_full_tests.py")
