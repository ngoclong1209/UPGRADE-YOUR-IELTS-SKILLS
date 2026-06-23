import os

OUTPUT_DIR = '.'
LEVELS = ['Basic', 'Intermediate', 'Advanced']

html = [
    '<!DOCTYPE html>',
    '<html lang="vi">',
    '<head>',
    '    <meta charset="UTF-8">',
    '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '    <title>Danh Sách Bài Học - IELTS Listening</title>',
    '    <script src="https://cdn.tailwindcss.com"></script>',
    '    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">',
    '    <style>',
    '        body { font-family: "Inter", sans-serif; background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); color: #333; min-height: 100vh; }',
    '        .glass-card { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1); }',
    '    </style>',
    '</head>',
    '<body class="py-10 px-4 sm:px-6 lg:px-8">',
    '    <div class="max-w-4xl mx-auto">',
    '        <header class="text-center mb-12">',
    '            <h1 class="text-4xl font-bold text-gray-900 tracking-tight mb-4">UPGRADE YOUR IELTS LISTENING</h1>',
    '            <p class="text-lg text-gray-600">Lộ trình luyện nghe Multiple Choice 3 cấp độ</p>',
    '        </header>',
    '        <div class="space-y-10">'
]

for level in LEVELS:
    level_dir = os.path.join(OUTPUT_DIR, level)
    if not os.path.isdir(level_dir):
        continue
        
    html.append(f'            <!-- {level} Section -->')
    html.append(f'            <section class="glass-card rounded-3xl p-8">')
    
    # Colors for different levels
    color = "indigo" if level == "Basic" else "blue" if level == "Intermediate" else "purple"
    
    html.append(f'                <h2 class="text-2xl font-bold text-{color}-600 mb-6 border-b border-gray-200 pb-3">{level} Level</h2>')
    html.append(f'                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">')
    
    # Get lessons and sort by number
    lessons = [d for d in os.listdir(level_dir) if os.path.isdir(os.path.join(level_dir, d)) and d.startswith('Lesson_')]
    lessons.sort(key=lambda x: int(x.split('_')[1]))
    
    for lesson in lessons:
        lesson_num = lesson.split('_')[1]
        link = f"{level}/{lesson}/index.html"
        html.append(f'                    <a href="{link}" class="flex items-center justify-center p-4 bg-white rounded-xl shadow-sm border border-gray-100 hover:border-{color}-300 hover:shadow-md transition-all duration-200 group">')
        html.append(f'                        <span class="font-medium text-gray-700 group-hover:text-{color}-600">Bài {lesson_num}</span>')
        html.append(f'                    </a>')
        
    html.append(f'                </div>')
    html.append(f'            </section>')

html.extend([
    '        </div>',
    '    </div>',
    '</body>',
    '</html>'
])

with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(html))
