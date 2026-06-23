import os

html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PTE & IELTS Listening Master</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300..700&family=DynaPuff:wght@400..700&family=Quicksand:wght@300..700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #fff0f5;
            --bg-secondary: #fff;
            --accent: #ffb6c1;
            --accent-hover: #ff69b4;
            --text-primary: #4a4a4a;
            --text-secondary: #7a7a7a;
            --border-color: #ffe4e1;
        }}
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Quicksand', sans-serif;
            background: linear-gradient(135deg, #ffe4e1 0%, #e0ffff 100%);
            color: var(--text-primary);
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }}
        /* Magical floating background bubbles */
        body::before, body::after {{
            content: '';
            position: fixed;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(255,182,193,0.4) 0%, rgba(255,255,255,0) 70%);
            z-index: -1;
            animation: float-bg 15s ease-in-out infinite alternate;
        }}
        body::before {{ top: -100px; left: -100px; }}
        body::after {{ bottom: -100px; right: -100px; animation-delay: -7s; }}
        
        @keyframes float-bg {{
            0% {{ transform: translate(0, 0) scale(1); }}
            100% {{ transform: translate(50px, 50px) scale(1.5); }}
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 60px;
            position: relative;
        }}
        .header h1 {{
            font-family: 'DynaPuff', cursive;
            font-size: 4.5rem;
            color: var(--accent-hover);
            margin: 0;
            text-shadow: 3px 3px 0 #fff, 6px 6px 0 rgba(255, 105, 180, 0.2);
            animation: float 3s ease-in-out infinite;
        }}
        .header p {{
            font-family: 'Fredoka', sans-serif;
            font-size: 1.5rem;
            color: #8b7d8b;
            margin-top: 15px;
            font-weight: 500;
        }}
        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}
        
        .level-section {{
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 40px;
            padding: 50px;
            margin-bottom: 60px;
            border: 2px solid rgba(255,255,255,0.8);
            box-shadow: 0 20px 40px rgba(0,0,0,0.05);
            position: relative;
            overflow: hidden;
        }}
        /* Inner decorative blob */
        .level-section::before {{
            content: '';
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.3), transparent);
            transform: rotate(45deg);
            animation: shine 8s infinite linear;
            pointer-events: none;
        }}
        @keyframes shine {{
            0% {{ transform: translateX(-100%) rotate(45deg); }}
            100% {{ transform: translateX(100%) rotate(45deg); }}
        }}

        .level-title {{
            font-family: 'Fredoka', sans-serif;
            font-size: 2.8rem;
            margin-top: 0;
            margin-bottom: 40px;
            display: inline-block;
            padding-bottom: 10px;
            position: relative;
            z-index: 1;
        }}
        .basic-title {{ color: #4facfe; border-bottom: 4px dashed #4facfe; }}
        .int-title {{ color: #43e97b; border-bottom: 4px dashed #43e97b; }}
        .adv-title {{ color: #fa709a; border-bottom: 4px dashed #fa709a; }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
            gap: 25px;
            position: relative;
            z-index: 1;
        }}
        .lesson-card {{
            background: #fff;
            border-radius: 25px;
            padding: 25px 15px;
            text-align: center;
            text-decoration: none;
            color: var(--text-primary);
            font-family: 'Fredoka', sans-serif;
            font-weight: 700;
            font-size: 1.3rem;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 3px solid transparent;
            box-shadow: 0 8px 20px rgba(0,0,0,0.04);
            position: relative;
        }}
        
        .lesson-card::after {{
            content: '🎵';
            font-size: 1.5rem;
            position: absolute;
            top: -15px;
            right: -10px;
            opacity: 0;
            transform: scale(0) rotate(-20deg);
            transition: all 0.3s ease;
        }}

        .lesson-card.basic-card:hover {{
            background: #4facfe; color: #fff; border-color: #4facfe;
            transform: translateY(-12px) scale(1.05) rotate(-2deg);
            box-shadow: 0 15px 30px rgba(79,172,254,0.3);
        }}
        .lesson-card.int-card:hover {{
            background: #43e97b; color: #fff; border-color: #43e97b;
            transform: translateY(-12px) scale(1.05) rotate(2deg);
            box-shadow: 0 15px 30px rgba(67,233,123,0.3);
        }}
        .lesson-card.adv-card:hover {{
            background: #fa709a; color: #fff; border-color: #fa709a;
            transform: translateY(-12px) scale(1.05) rotate(-2deg);
            box-shadow: 0 15px 30px rgba(250,112,154,0.3);
        }}
        
        .lesson-card:hover::after {{
            opacity: 1;
            transform: scale(1) rotate(10deg);
        }}

        @media (max-width: 768px) {{
            .header h1 {{ font-size: 3rem; }}
            .level-section {{ padding: 30px; border-radius: 30px; }}
            .grid {{ grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 15px; }}
            .lesson-card {{ padding: 15px 10px; font-size: 1.1rem; border-radius: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✨ Listening Master ✨</h1>
            <p>Hành trình chinh phục điểm tối đa</p>
        </div>
"""

def generate_section(title, level, color_class, count):
    html = f'''
        <div class="level-section">
            <h2 class="level-title {color_class}">{title}</h2>
            <div class="grid">
'''
    card_class = color_class.replace('-title', '-card')
    for i in range(1, count + 1):
        html += f'''
                <a href="{level}/Lesson_{i}/index.html" class="lesson-card {card_class}">Bài {i}</a>
'''
    html += '''
            </div>
        </div>
'''
    return html

html += generate_section("🌟 Basic Level", "Basic", "basic-title", 34)
html += generate_section("🔥 Intermediate Level", "Intermediate", "int-title", 34)
html += generate_section("👑 Advanced Level", "Advanced", "adv-title", 34)

html += """
    </div>
</body>
</html>
"""

with open("/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS LISTENING/pte-listening-audios/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Beautiful index.html created!")
