import os

def update_css():
    base_dir = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"
    
    files_to_update = [
        "Reading_1232_Basic/frontend/template_reading.html",
        "Reading_1232_Basic/frontend/index.html"
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

        # REVERT :root
        content = content.replace(
            "--bg-primary: #e0f7fa;", "--bg-primary: #fff5f7;"
        ).replace(
            "--bg-secondary: #ffffff;", "--bg-secondary: #fffafb;"
        ).replace(
            "--text-primary: #4e342e;", "--text-primary: #5c404d;"
        ).replace(
            "--text-secondary: #5d4037;", "--text-secondary: #8c6d7d;"
        ).replace(
            "--border-color: #8d6e63;", "--border-color: #ffccd5;"
        ).replace(
            "--accent: #81c784;", "--accent: #ff85a2;"
        ).replace(
            "--accent-hover: #4caf50;", "--accent-hover: #ff5e7e;"
        ).replace(
            "--accent-lilac: #87ceeb;", "--accent-lilac: #b19ffb;"
        ).replace(
            "--success-bg: #e8f5e9;", "--success-bg: #e2f9ee;"
        ).replace(
            "--error-bg: #ffebee;", "--error-bg: #fff0f2;"
        )

        # Update body background
        content = content.replace(
            "background: linear-gradient(135deg, #87ceeb 0%, #e0f7fa 50%, #ffffff 100%);",
            "background: linear-gradient(135deg, #fff0f5 0%, #e6e6fa 50%, #f0f8ff 100%);"
        ).replace(
            "background: linear-gradient(135deg, #87ceeb 0%, #e0f7fa 100%);",
            "background: linear-gradient(135deg, #ffe4e1 0%, #e0ffff 100%);"
        )
        
        # Update body::before, body::after
        content = content.replace(
            "background: radial-gradient(circle, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0) 70%); border-radius: 100px; height: 150px; width: 400px; filter: blur(5px);",
            "background: radial-gradient(circle, rgba(255,182,193,0.4) 0%, rgba(255,255,255,0) 70%);"
        )

        # Update fairytale-panel & level-section & login-box
        content = content.replace(
            "background: #d7ccc8;",
            "background: rgba(255, 255, 255, 0.82);"
        )
        
        content = content.replace(
            "border: 5px solid #8d6e63;",
            "border: 3px solid var(--border-color);"
        )
        
        # Resizer updates
        content = content.replace(
            "background: rgba(129, 199, 132, 0.5);",
            "background: rgba(255,133,162,0.1);"
        ).replace(
            "background: rgba(76, 175, 80, 0.8);",
            "background: rgba(255,133,162,0.5);"
        )

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"Reverted CSS in {len(files_to_update)} files to PINK/WHITE theme.")

if __name__ == "__main__":
    update_css()
