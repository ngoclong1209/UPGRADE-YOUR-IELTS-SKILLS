import os

def update_css():
    base_dir = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"
    files_to_update = [
        "Listening_102_Basic/template.html",
        "Listening_102_Basic/index.html",
        "Reading_1232_Basic/frontend/template.html",
        "Reading_1232_Basic/frontend/index.html"
    ]

    for rel_path in files_to_update:
        file_path = os.path.join(base_dir, rel_path)
        if not os.path.exists(file_path):
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

    print("Updated CSS in 102 and 1232 files.")

def update_build_full_tests():
    file_path = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS/Tools/build_full_tests.py"
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update body in HTML_TEMPLATE
    content = content.replace(
        "background: #fdf2f8; color: #333;",
        "background: linear-gradient(135deg, #87ceeb 0%, #e0f7fa 100%); color: #4e342e;"
    )
    
    # Update passage-pane and answer-pane in HTML_TEMPLATE
    content = content.replace(
        "background: white; border-radius: 20px;",
        "background: #d7ccc8; border: 5px solid #8d6e63; border-radius: 20px;"
    ).replace(
        "background: linear-gradient(145deg, #ffffff, #fff0f5);",
        "background: #d7ccc8; border: 5px solid #8d6e63;"
    )
    
    # Update resizer
    content = content.replace(
        "background: rgba(255,133,162,0.1);",
        "background: rgba(129, 199, 132, 0.5);"
    ).replace(
        "background: rgba(255,133,162,0.5);",
        "background: rgba(76, 175, 80, 0.8);"
    ).replace(
        "color: #ff85a2;",
        "color: #2e7d32;"
    )

    # Update .test-heading
    content = content.replace(
        "color: #ff5e7e;",
        "color: #4caf50;"
    )

    # Update .para-row
    content = content.replace(
        "background: #fffafb;",
        "background: #ffffff;"
    ).replace(
        "border-left: 4px solid #ffccd5;",
        "border-left: 4px solid #8d6e63;"
    ).replace(
        "border-left-color: #ff5e7e; background: #fff5f7;",
        "border-left-color: #4caf50; background: #e8f5e9;"
    )

    # Update .para-label
    content = content.replace(
        "background: #ff85a2;",
        "background: #4caf50;"
    )
    
    # Update strong / u
    content = content.replace(
        "color: #d6336c;",
        "color: #e65100;"
    ).replace(
        "text-decoration-color: #ff85a2;",
        "text-decoration-color: #4caf50;"
    )
    
    # Update .q-row
    content = content.replace(
        "border: 2px solid #ffccd5;",
        "border: 2px solid #8d6e63;"
    ).replace(
        "color: #ff85a2;",
        "color: #388e3c;"
    ).replace(
        "border-bottom: 2px dashed #ffccd5;",
        "border-bottom: 2px dashed #8d6e63;"
    )

    # Update LOGIN_CSS
    content = content.replace(
        "background: linear-gradient(135deg, #fdf2f8 0%, #e6e6fa 50%, #f0f8ff 100%);",
        "background: linear-gradient(135deg, #87ceeb 0%, #e0f7fa 100%);"
    ).replace(
        "background: rgba(255, 255, 255, 0.85);",
        "background: #d7ccc8;"
    ).replace(
        "border: 3px solid #ffccd5;",
        "border: 5px solid #8d6e63;"
    ).replace(
        "box-shadow: 0 20px 50px rgba(255, 182, 193, 0.3), inset 0 0 20px rgba(255, 255, 255, 0.5);",
        "box-shadow: 0 20px 50px rgba(0,0,0,0.2), inset 0 0 20px rgba(255,255,255,0.2);"
    )
    
    # Update #submit-btn
    content = content.replace(
        "background: linear-gradient(45deg, #ff85a2, #ff5e7e);",
        "background: linear-gradient(45deg, #81c784, #4caf50);"
    ).replace(
        "box-shadow: 0 4px 15px rgba(255, 133, 162, 0.4);",
        "box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);"
    ).replace(
        "background: linear-gradient(45deg, #ff5e7e, #ff85a2);",
        "background: linear-gradient(45deg, #4caf50, #81c784);"
    )

    # Replace audio-bar
    content = content.replace(
        "background: rgba(255, 255, 255, 0.95);",
        "background: #d7ccc8;"
    ).replace(
        "border-top: 3px solid #ffccd5;",
        "border-top: 4px solid #8d6e63;"
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Updated CSS in build_full_tests.py.")

if __name__ == "__main__":
    update_css()
    update_build_full_tests()
