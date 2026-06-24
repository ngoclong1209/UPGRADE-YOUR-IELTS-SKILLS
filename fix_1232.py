import os

def update_css():
    base_dir = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"
    files_to_update = [
        "Reading_1232_Basic/frontend/template_reading.html",
        "Reading_1232_Basic/frontend/index.html",
        "Listening_102_Basic/template.html",
        "Listening_102_Basic/index.html"
    ]

    for rel_path in files_to_update:
        file_path = os.path.join(base_dir, rel_path)
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update :root
        content = content.replace(
            "--bg-primary: #fff5f7;", "--bg-primary: #e0f7fa;"
        ).replace(
            "--bg-secondary: #fffafb;", "--bg-secondary: #ffffff;"
        ).replace(
            "--text-primary: #5c404d;", "--text-primary: #4e342e;"
        ).replace(
            "--text-secondary: #8c6d7d;", "--text-secondary: #5d4037;"
        ).replace(
            "--border-color: #ffccd5;", "--border-color: #8d6e63;"
        ).replace(
            "--accent: #ff85a2;", "--accent: #81c784;"
        ).replace(
            "--accent-hover: #ff5e7e;", "--accent-hover: #4caf50;"
        ).replace(
            "--accent-lilac: #b19ffb;", "--accent-lilac: #87ceeb;"
        ).replace(
            "--success-bg: #e2f9ee;", "--success-bg: #e8f5e9;"
        ).replace(
            "--error-bg: #fff0f2;", "--error-bg: #ffebee;"
        )
        # Handle index.html :root which has slightly different colors
        content = content.replace(
            "--bg-primary: #fff0f5;", "--bg-primary: #e0f7fa;"
        ).replace(
            "--bg-secondary: #fff;", "--bg-secondary: #ffffff;"
        ).replace(
            "--text-primary: #4a4a4a;", "--text-primary: #4e342e;"
        ).replace(
            "--text-secondary: #7a7a7a;", "--text-secondary: #5d4037;"
        ).replace(
            "--border-color: #ffe4e1;", "--border-color: #8d6e63;"
        ).replace(
            "--accent: #ffb6c1;", "--accent: #81c784;"
        ).replace(
            "--accent-hover: #ff69b4;", "--accent-hover: #4caf50;"
        )

        # Update body background
        content = content.replace(
            "background: linear-gradient(135deg, #fff0f5 0%, #e6e6fa 50%, #f0f8ff 100%);",
            "background: linear-gradient(135deg, #87ceeb 0%, #e0f7fa 50%, #ffffff 100%);"
        ).replace(
            "background: linear-gradient(135deg, #ffe4e1 0%, #e0ffff 100%);",
            "background: linear-gradient(135deg, #87ceeb 0%, #e0f7fa 100%);"
        )
        
        # Update body::before, body::after
        content = content.replace(
            "background: radial-gradient(circle, rgba(255,182,193,0.4) 0%, rgba(255,255,255,0) 70%);",
            "background: radial-gradient(circle, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0) 70%); border-radius: 100px; height: 150px; width: 400px; filter: blur(5px);"
        )

        # Update fairytale-panel & level-section (Wood style)
        content = content.replace(
            "background: rgba(255, 255, 255, 0.82);",
            "background: #d7ccc8;"
        ).replace(
            "background: rgba(255, 255, 255, 0.6);",
            "background: #d7ccc8;"
        )
        
        content = content.replace(
            "border: 3px solid var(--border-color);",
            "border: 5px solid #8d6e63;"
        ).replace(
            "border: 2px solid rgba(255,255,255,0.8);",
            "border: 5px solid #8d6e63;"
        )

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print("Updated CSS.")

if __name__ == "__main__":
    update_css()
