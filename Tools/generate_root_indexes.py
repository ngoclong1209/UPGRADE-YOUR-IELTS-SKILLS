import os

def generate_index(folder_name, count):
    title = f"{folder_name.capitalize()} Tests"
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            color: #4f46e5;
            margin-bottom: 2rem;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 1rem;
        }}
        .test-card {{
            background: white;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            text-decoration: none;
            color: #334155;
            font-weight: 600;
            transition: all 0.2s ease;
            border: 1px solid #e2e8f0;
        }}
        .test-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px rgba(0,0,0,0.1);
            border-color: #4f46e5;
            color: #4f46e5;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="grid">
"""
    for i in range(1, count + 1):
        html += f'        <a href="Test_{i}/index.html" class="test-card">Test {i}</a>\n'

    html += """    </div>
</body>
</html>
"""
    
    path = os.path.join("/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS/practicepteonline", folder_name, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {path}")

generate_index("reading", 315)
generate_index("listening", 204)
