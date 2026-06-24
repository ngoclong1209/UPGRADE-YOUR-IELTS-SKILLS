import os
import re

def update_css():
    base_dir = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"
    
    files_to_update = []
    
    # Add all Listening_102_Basic html files
    for root, dirs, files in os.walk(os.path.join(base_dir, "Listening_102_Basic")):
        for file in files:
            if file.endswith('.html'):
                files_to_update.append(os.path.relpath(os.path.join(root, file), base_dir))

    # Add all Reading_1232_Basic html files
    for root, dirs, files in os.walk(os.path.join(base_dir, "Reading_1232_Basic")):
        for file in files:
            if file.endswith('.html'):
                files_to_update.append(os.path.relpath(os.path.join(root, file), base_dir))

    print(f"Found {len(files_to_update)} files to update.")
    count = 0
    
    for rel_path in files_to_update:
        file_path = os.path.join(base_dir, rel_path)
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        if "<!-- FULL TEST THEME OVERRIDE -->" in content:
            new_override = """<!-- FULL TEST THEME OVERRIDE -->
    <style>
        body {
            background: linear-gradient(135deg, #fff0f5 0%, #ffe4e1 100%) !important;
        }
        .main-layout {
            border: 10px solid #ffb6c1 !important;
            box-shadow: 0 0 30px rgba(255, 182, 193, 0.5) !important;
            background: #ffffff !important;
        }
        .resizer {
            background: rgba(255, 182, 193, 0.5) !important;
            border-left: 1px solid #ffccd5 !important;
            border-right: 1px solid #ffccd5 !important;
        }
        .resizer::after {
            background: #ff85a2 !important;
            box-shadow: 0 0 10px rgba(255, 133, 162, 0.5) !important;
        }
        .sheet-title {
            background: linear-gradient(135deg, #ff85a2 0%, #ff5e7e 100%) !important;
            color: white !important;
            border-radius: 15px !important;
            padding: 15px 30px !important;
            box-shadow: 0 5px 15px rgba(255, 94, 126, 0.3) !important;
        }
        .login-box { 
            background: #d7ccc8 !important;
            border: 4px solid #ffccd5 !important;
        }
        .login-input { 
            border: 5px solid #8d6e63 !important;
            background: #ffffff !important;
            color: #5c404d !important;
        }
        .login-header {
            color: #2e7d32 !important; 
            text-shadow: 2px 2px 0px rgba(255,133,162,0.2) !important;
        }
        .login-input:focus { border-color: #2e7d32 !important; }
        .test-heading {
            color: #ff5e7e !important;
        }
        .passage-pane {
            flex: 0 0 60%;
        }
        .answer-pane {
            flex: 1;
        }
    </style>"""
            
            # Replace the old override block
            content = re.sub(
                r'<!-- FULL TEST THEME OVERRIDE -->\s*<style>.*?</style>',
                new_override,
                content,
                flags=re.DOTALL
            )
            changed = True
        
        # If it doesn't have the override, just inject it before </head>
        if "<!-- FULL TEST THEME OVERRIDE -->" not in content:
            new_override = """<!-- FULL TEST THEME OVERRIDE -->
    <style>
        body {
            background: linear-gradient(135deg, #fff0f5 0%, #ffe4e1 100%) !important;
        }
        .main-layout {
            border: 10px solid #ffb6c1 !important;
            box-shadow: 0 0 30px rgba(255, 182, 193, 0.5) !important;
            background: #ffffff !important;
        }
        .resizer {
            background: rgba(255, 182, 193, 0.5) !important;
            border-left: 1px solid #ffccd5 !important;
            border-right: 1px solid #ffccd5 !important;
        }
        .resizer::after {
            background: #ff85a2 !important;
            box-shadow: 0 0 10px rgba(255, 133, 162, 0.5) !important;
        }
        .sheet-title {
            background: linear-gradient(135deg, #ff85a2 0%, #ff5e7e 100%) !important;
            color: white !important;
            border-radius: 15px !important;
            padding: 15px 30px !important;
            box-shadow: 0 5px 15px rgba(255, 94, 126, 0.3) !important;
        }
        .login-box { 
            background: #d7ccc8 !important;
            border: 4px solid #ffccd5 !important;
        }
        .login-input { 
            border: 5px solid #8d6e63 !important;
            background: #ffffff !important;
            color: #5c404d !important;
        }
        .login-header {
            color: #2e7d32 !important; 
            text-shadow: 2px 2px 0px rgba(255,133,162,0.2) !important;
        }
        .login-input:focus { border-color: #2e7d32 !important; }
        .test-heading {
            color: #ff5e7e !important;
        }
        .passage-pane {
            flex: 0 0 60%;
        }
        .answer-pane {
            flex: 1;
        }
    </style>"""
            content = content.replace("</head>", new_override + "\n</head>")
            changed = True

        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1

    print(f"Fixed login box CSS in {count} files.")

if __name__ == "__main__":
    update_css()
