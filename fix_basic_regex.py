import os

directories = [
    'Listening_102_Basic',
    'Reading_1232_Basic'
]

old_1 = r'''html.replace(/(?<!<[^>]*)\b([1-3]?[0-9]|40)\.(?![^<]*>)/g, '<span class="cloud-badge">$1</span>');'''
new_1 = r'''html.replace(/(?<!<[^>]*)\b([0-9]{1,2})\.(?![^<]*>)/g, '<span class="cloud-badge">$1</span>');'''

old_2 = r'''html.replace(/(?<!<[^>]*)\(([1-3]?[0-9]|40)\)(?![^<]*>)/g, '<span class="cloud-badge">$1</span>');'''
new_2 = r'''html.replace(/(?<!<[^>]*)\(([0-9]{1,2})\)(?![^<]*>)/g, '<span class="cloud-badge">$1</span>');'''

old_3 = r'''html.replace(/_{3,}|\.{3,}/g, '<span class="cloud-blank"></span>');'''
new_3 = r'''html.replace(/_{2,}|\.{3,}/g, '<span class="cloud-blank"></span>');'''

count = 0
for directory in directories:
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                new_content = content.replace(old_1, new_1)
                new_content = new_content.replace(old_2, new_2)
                new_content = new_content.replace(old_3, new_3)
                
                if new_content != content:
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    count += 1

print(f'Updated JS regex in {count} HTML files.')
