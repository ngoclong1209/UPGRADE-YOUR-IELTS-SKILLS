import os
import json

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False

    is_js = filepath.endswith('.js')
    
    # Simple search for the answers
    changed = False
    new_content = content
    
    # We can just use basic replace for the specific known issues
    if 'Invalid answer for T/F/NG: F' in content or '"answer": "F"' in content:
        new_content = new_content.replace('"answer": "F"', '"answer": "FALSE"')
        new_content = new_content.replace('"answer": "T"', '"answer": "TRUE"')
        new_content = new_content.replace('"answer": "NG"', '"answer": "NOT GIVEN"')
        changed = True
        
    if 'Invalid answer for Y/N/NG: N' in content or '"answer": "N"' in content:
        new_content = new_content.replace('"answer": "N"', '"answer": "NO"')
        new_content = new_content.replace('"answer": "Y"', '"answer": "YES"')
        changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
        
    return False

def main():
    data_dir = 'frontend/data'
    fixed_count = 0

    print("Fixing data files for anomalous answers via simple string replace...")
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.js'):
                if file.startswith('index') or file.startswith('sample'): continue
                
                filepath = os.path.join(root, file)
                if fix_file(filepath):
                    print(f"Fixed: {filepath}")
                    fixed_count += 1
    
    print(f"Fixed a total of {fixed_count} files.")

if __name__ == '__main__':
    main()
