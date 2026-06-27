import os
import json
import re

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    is_js = filepath.endswith('.js')
    prefix = ""
    suffix = ""
    
    if is_js:
        match = re.search(r'(window\.(?:lessonData|testData)\s*=\s*)(\{.*\})(;?\s*)$', content, re.DOTALL)
        if match:
            prefix = match.group(1)
            json_str = match.group(2)
            suffix = match.group(3)
        else:
            return False
    else:
        json_str = content

    try:
        data = json.loads(json_str)
    except Exception as e:
        return False

    if not isinstance(data, dict):
        return False

    questions = data.get('questions', [])
    if not isinstance(questions, list):
        return False

    changed = False

    for q in questions:
        if not isinstance(q, dict):
            continue
        q_type = q.get('type', '')
        answer = q.get('answer')
        
        if answer is not None:
            ans_str = str(answer).strip().upper()
            
            if 'yes_no_not_given' in q_type:
                mapping = {'Y': 'YES', 'N': 'NO', 'NG': 'NOT GIVEN', 'A': 'YES', 'B': 'NO', 'C': 'NOT GIVEN'}
                if ans_str in mapping:
                    q['answer'] = mapping[ans_str]
                    changed = True
                    
            elif 'true_false_not_given' in q_type:
                mapping = {'T': 'TRUE', 'F': 'FALSE', 'NG': 'NOT GIVEN', 'A': 'TRUE', 'B': 'FALSE', 'C': 'NOT GIVEN'}
                if ans_str in mapping:
                    q['answer'] = mapping[ans_str]
                    changed = True

    if changed:
        new_json_str = json.dumps(data, ensure_ascii=False)
        new_content = prefix + new_json_str + suffix
        if not is_js:
            new_content = new_json_str
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
        
    return False

def main():
    data_dir = 'frontend/data'
    fixed_count = 0

    print("Fixing data files for anomalous answers...")
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.js') or file.endswith('.json'):
                if file.startswith('index') or file.startswith('sample'): continue
                
                filepath = os.path.join(root, file)
                if fix_file(filepath):
                    print(f"Fixed: {filepath}")
                    fixed_count += 1
    
    print(f"Fixed a total of {fixed_count} files.")

if __name__ == '__main__':
    main()
