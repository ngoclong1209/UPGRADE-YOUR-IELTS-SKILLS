import os
import re

def fix_all():
    data_dir = '/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS/Reading_1232_Basic/frontend/data'
    log_file = '/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS/Reading_1232_Basic/fix_report.log'
    log_entries = []
    
    count = 0
    total = 0
    for root, dirs, files in os.walk(data_dir):
        for f in files:
            if f.endswith('.json') or f.endswith('.js'):
                # Ignore sample data and index files if necessary, or just process everything
                if 'sample_data' in f or 'index' in f:
                    # Actually, processing them is fine as it ensures consistency everywhere
                    pass
                
                path = os.path.join(root, f)
                total += 1
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read()
                except Exception as e:
                    continue
                
                original_content = content
                
                # Replace NOT_GIVEN -> NOT GIVEN
                content = content.replace('"NOT_GIVEN"', '"NOT GIVEN"')
                content = content.replace("'NOT_GIVEN'", "'NOT GIVEN'")
                
                # Targeted replacements for incorrect single letter answers
                content = re.sub(r'"answer"\s*:\s*"F"', '"answer": "FALSE"', content)
                content = re.sub(r'"answer"\s*:\s*"T"', '"answer": "TRUE"', content)
                content = re.sub(r'"answer"\s*:\s*"N"', '"answer": "NO"', content)
                content = re.sub(r'"answer"\s*:\s*"Y"', '"answer": "YES"', content)
                
                if content != original_content:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    log_entries.append(f"Fixed anomalies in: {path}")
                    count += 1

    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"Data Validation & Fix Report\n")
        f.write(f"============================\n")
        f.write(f"Total files scanned: {total}\n")
        f.write(f"Total files fixed: {count}\n\n")
        f.write("Details:\n")
        f.write("\n".join(log_entries))
        
    print(f"Done. Fixed {count}/{total} files. Check fix_report.log")

if __name__ == '__main__':
    fix_all()
