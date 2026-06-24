import os
import re

directories = [
    'Listening_102_Basic',
    'Reading_1232_Basic',
    'Listening_204_FullTest',
    'Reading_315_FullTest'
]

resizer_css = """
        .resizer {
            flex: 0 0 10px;
            cursor: col-resize;
            background: rgba(255, 182, 193, 0.5);
            display: flex; align-items: center; justify-content: center;
            transition: background 0.3s;
            z-index: 100;
        }
        .resizer:hover { background: rgba(255, 182, 193, 0.8); }
        .resizer::after { content: '⋮'; color: #ff85a2; font-size: 20px; }
"""

resizer_js = """
    <script>
        // --- Drag to Resize Logic ---
        document.addEventListener('DOMContentLoaded', () => {
            const resizer = document.getElementById('resizer');
            const mainLayout = document.querySelector('.main-layout');
            // Identify left and right panes dynamically based on DOM order inside main-layout
            if (!resizer || !mainLayout) return;
            
            let leftPane = resizer.previousElementSibling;
            let rightPane = resizer.nextElementSibling;
            
            if (!leftPane || !rightPane) return;
            
            let isResizing = false;

            resizer.addEventListener('mousedown', (e) => {
                isResizing = true;
                document.body.style.cursor = 'col-resize';
                leftPane.style.pointerEvents = 'none';
                rightPane.style.pointerEvents = 'none';
                e.preventDefault();
            });

            document.addEventListener('mousemove', (e) => {
                if (!isResizing) return;
                let containerWidth = mainLayout.offsetWidth;
                let newLeftWidth = (e.clientX / containerWidth) * 100;
                if (newLeftWidth > 20 && newLeftWidth < 80) {
                    leftPane.style.flex = `0 0 ${newLeftWidth}%`;
                    rightPane.style.flex = `1 1 0%`;
                }
            });

            document.addEventListener('mouseup', () => {
                if (isResizing) {
                    isResizing = false;
                    document.body.style.cursor = 'default';
                    leftPane.style.pointerEvents = 'auto';
                    rightPane.style.pointerEvents = 'auto';
                }
            });
            
            // Touch support for mobile/tablet
            resizer.addEventListener('touchstart', (e) => {
                isResizing = true;
                leftPane.style.pointerEvents = 'none';
                rightPane.style.pointerEvents = 'none';
            }, {passive: true});
            
            document.addEventListener('touchmove', (e) => {
                if (!isResizing) return;
                let containerWidth = mainLayout.offsetWidth;
                let touch = e.touches[0];
                let newLeftWidth = (touch.clientX / containerWidth) * 100;
                if (newLeftWidth > 20 && newLeftWidth < 80) {
                    leftPane.style.flex = `0 0 ${newLeftWidth}%`;
                    rightPane.style.flex = `1 1 0%`;
                }
            }, {passive: true});
            
            document.addEventListener('touchend', () => {
                if (isResizing) {
                    isResizing = false;
                    leftPane.style.pointerEvents = 'auto';
                    rightPane.style.pointerEvents = 'auto';
                }
            });
        });
    </script>
"""

count_modified = 0

for directory in directories:
    if not os.path.exists(directory):
        continue
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except:
                    continue
                
                original_content = content
                
                # We need to enforce left pane 60%, right pane flex 1
                # Check which one comes first
                idx_passage = content.find('class="passage-pane')
                idx_answer = content.find('class="answer-pane')
                if idx_passage == -1 or idx_answer == -1:
                    continue
                
                # Check if resizer is already injected
                if 'class="resizer"' not in content:
                    if idx_passage < idx_answer:
                        # passage is left
                        content = re.sub(r'(<div[^>]*class="[^"]*passage-pane[^"]*"[^>]*>.*?</div>)\s*(<div[^>]*class="[^"]*answer-pane[^"]*"[^>]*>)',
                                         r'\1\n        <div class="resizer" id="resizer"></div>\n        \2', content, flags=re.DOTALL)
                    else:
                        # answer is left
                        content = re.sub(r'(<div[^>]*class="[^"]*answer-pane[^"]*"[^>]*>.*?</div>)\s*(<div[^>]*class="[^"]*passage-pane[^"]*"[^>]*>)',
                                         r'\1\n        <div class="resizer" id="resizer"></div>\n        \2', content, flags=re.DOTALL)
                
                # Inject CSS if not present
                if '.resizer {' not in content and 'class="resizer"' in content:
                    content = content.replace('</style>', resizer_css + '\n    </style>')
                    
                # Inject JS if not present
                if 'resizer.addEventListener' not in content and 'class="resizer"' in content:
                    content = content.replace('</body>', resizer_js + '\n</body>')
                
                # Force flex ratio to 60 / 40
                if idx_passage < idx_answer:
                    content = re.sub(r'(\.passage-pane\s*\{[^}]*?)flex:\s*[^;]+;', r'\1flex: 0 0 60%;', content, count=0)
                    content = re.sub(r'(\.answer-pane\s*\{[^}]*?)flex:\s*[^;]+;', r'\1flex: 1 1 0%;', content, count=0)
                else:
                    content = re.sub(r'(\.answer-pane\s*\{[^}]*?)flex:\s*[^;]+;', r'\1flex: 0 0 60%;', content, count=0)
                    content = re.sub(r'(\.passage-pane\s*\{[^}]*?)flex:\s*[^;]+;', r'\1flex: 1 1 0%;', content, count=0)
                
                if original_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count_modified += 1

print(f"Added/Updated resizer logic and 60/40 ratio to {count_modified} HTML files.")
