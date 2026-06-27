import os
import json
import re

def check_file(filepath):
    issues = []
    content = ""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"Error reading file: {e}"]

    # Extract JSON part if it's a JS file
    if filepath.endswith('.js'):
        # Usually it's window.lessonData = {...};
        match = re.search(r'window\.(?:lessonData|testData)\s*=\s*(\{.*\});?', content, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            return ["Could not find JSON data in JS file using regex"]
    else:
        json_str = content

    try:
        data = json.loads(json_str)
    except Exception as e:
        return [f"JSON parse error: {e}"]

    if not isinstance(data, dict):
        return ["Root data is not a dict"]

    questions = data.get('questions', [])
    if not isinstance(questions, list):
        return ["'questions' is not a list"]

    for q in questions:
        if not isinstance(q, dict):
            continue
        q_id = q.get('id', 'unknown')
        q_type = q.get('type', '')
        answer = q.get('answer')
        answers = q.get('answers')
        
        # Check standard answer against options
        if answer is not None:
            ans_str = str(answer).strip().upper().replace('_', ' ')
            if 'yes_no_not_given' in q_type:
                if ans_str not in ['YES', 'NO', 'NOT GIVEN']:
                    issues.append(f"Q {q_id}: Invalid answer for Y/N/NG: {answer}")
            elif 'true_false_not_given' in q_type:
                if ans_str not in ['TRUE', 'FALSE', 'NOT GIVEN']:
                    issues.append(f"Q {q_id}: Invalid answer for T/F/NG: {answer}")

        # Check grouped answers
        if answers is not None and isinstance(answers, dict):
            for subQ, subAns in answers.items():
                if not subAns:
                    issues.append(f"Q {q_id}_{subQ}: Missing answer")
    return issues

def main():
    data_dir = 'frontend/data'
    total_files = 0
    total_issues = 0

    print("Checking data files for potential answer mismatches...")
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.js') or file.endswith('.json'):
                # Ignore index files
                if file.startswith('index') or file.startswith('sample'): continue
                
                filepath = os.path.join(root, file)
                total_files += 1
                issues = check_file(filepath)
                if issues:
                    print(f"Issues in {filepath}:")
                    for iss in issues:
                        print(f"  - {iss}")
                        total_issues += 1
    
    print(f"\nChecked {total_files} files.")
    if total_issues == 0:
        print("All checks passed! No issues found.")
    else:
        print(f"Found {total_issues} issues.")

if __name__ == '__main__':
    main()
