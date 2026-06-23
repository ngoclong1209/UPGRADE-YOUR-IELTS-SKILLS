import os
import subprocess

# 1. Update template.html
with open('template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix layout flexes
html = html.replace('.passage-pane {\n            flex: 2;', '.passage-pane {\n            flex: 1;')
html = html.replace('.answer-pane {\n            flex: 1;\n            overflow-y: auto;\n            padding: 2.5rem 2rem;\n            display: flex;\n            flex-direction: column;\n            flex-shrink: 0;\n            width: 400px;', 
                    '.answer-pane {\n            flex: 2;\n            overflow-y: auto;\n            padding: 2.5rem 2rem;\n            display: flex;\n            flex-direction: column;\n            flex-shrink: 0;')

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("template.html layout updated.")
