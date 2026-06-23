import os
import glob
import subprocess

TARGET_URL = "https://script.google.com/macros/s/AKfycbwpA-N8yVVDrmFD4pZRkDpwOGqDJYLA_LSwh0WVrnL6rPxw4ionhhEAfV2b0df_hJaH/exec"

def check_category(category_dir, expected_count):
    if not os.path.exists(category_dir):
        print(f"ERROR: {category_dir} does not exist.")
        return
        
    test_folders = glob.glob(os.path.join(category_dir, "Test_*"))
    print(f"[{category_dir}] Found {len(test_folders)} folders (Expected {expected_count})")
    
    missing_index = []
    missing_url = []
    
    for folder in test_folders:
        index_file = os.path.join(folder, "index.html")
        if not os.path.exists(index_file):
            missing_index.append(folder)
            continue
            
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()
            if TARGET_URL not in content:
                missing_url.append(folder)
                
    if missing_index:
        print(f"  -> Missing index.html in {len(missing_index)} folders: {missing_index[:5]}...")
    if missing_url:
        print(f"  -> Missing correct WEB_APP_URL in {len(missing_url)} folders: {missing_url[:5]}...")
        
    if not missing_index and not missing_url:
        print(f"  -> All folders in {category_dir} are perfectly configured.")

print("Starting verification...")
check_category("reading", 315)
check_category("listening", 204)

print("\nChecking git status...")
os.system("git status")
