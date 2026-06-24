import os

OVERRIDE_STYLE = """
    <!-- FULL TEST THEME OVERRIDE -->
    <style>
        body {
            background: linear-gradient(135deg, #fff0f5 0%, #ffe4e1 100%) !important;
        }
        .main-layout {
            flex-direction: row !important;
            padding: 0 !important;
            gap: 0 !important;
            margin: 0 !important;
            background: transparent !important;
        }
        .resizer {
            background-color: #f0f0f0 !important;
            width: 10px !important;
            border: none !important;
        }
        .resizer::after {
            background-color: #ccc !important;
        }
        .passage-pane {
            background: rgba(255, 255, 255, 0.95) !important;
            border: 5px solid #ffb6c1 !important;
            border-radius: 20px !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05) !important;
            margin: 10px 0 10px 10px !important;
            padding: 30px !important;
        }
        .answer-pane {
            background: rgba(255, 255, 255, 0.95) !important;
            border: 5px solid #ffb6c1 !important;
            border-radius: 20px !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05) !important;
            margin: 10px 10px 10px 0 !important;
            padding: 30px !important;
        }
        .fairytale-panel {
            background: rgba(255, 255, 255, 0.95) !important;
            border: none !important;
            box-shadow: none !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
        }
        .sheet-title {
            color: #4caf50 !important;
            font-family: 'DynaPuff', cursive !important;
            text-align: center !important;
            font-size: 1.8rem !important;
            margin-bottom: 25px !important;
            border-bottom: none !important;
        }
        h1 {
            color: #4caf50 !important;
            text-shadow: none !important;
            font-family: 'DynaPuff', cursive !important;
        }
        header {
            background: rgba(255, 255, 255, 0.95) !important;
            border-bottom: 5px solid #ffb6c1 !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05) !important;
        }
        @media (max-width: 900px) {
            .main-layout {
                flex-direction: column !important;
            }
            .passage-pane {
                margin: 10px !important;
            }
            .answer-pane {
                margin: 10px !important;
            }
        }
    </style>
</head>
"""

def inject():
    base_dir = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"
    
    files_to_update = [
        "Reading_1232_Basic/frontend/template_reading.html",
        "Listening_102_Basic/template.html"
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

        # Check if already injected, if so, replace it
        if "<!-- FULL TEST THEME OVERRIDE -->" in content:
            start_idx = content.find("<!-- FULL TEST THEME OVERRIDE -->")
            end_idx = content.find("</head>", start_idx) + len("</head>")
            content = content[:start_idx] + OVERRIDE_STYLE.strip() + "\n" + content[end_idx:]
        else:
            content = content.replace("</head>", OVERRIDE_STYLE.strip() + "\n</head>")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"Injected FULL TEST THEME into {len(files_to_update)} files.")

if __name__ == "__main__":
    inject()
