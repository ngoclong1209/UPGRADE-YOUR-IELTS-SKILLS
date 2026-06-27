#!/usr/bin/env python3
"""
Extract IELTS Listening test questions from HTML files into JSON format
using OmniRoute API (OpenAI-compatible).

Processes all test folders that are missing .json files.
Produces both Test_X.json and Test_X_processed.json.
"""

import os
import json
import re
import time
import urllib.request
import urllib.error

# ── Config ──────────────────────────────────────────────────────────────
OMNIROUTE_API_KEY = "sk-92d3ef3c86e600b6-ef9847-d92a108c"
OMNIROUTE_BASE_URL = "https://api.omniroute.io/v1/chat/completions"
MODEL = "google/gemini-2.5-flash"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FULLTEST_DIR = os.path.join(BASE_DIR, "Listening_204_FullTest")

# ── Reference JSON (Test_1) for few-shot prompt ─────────────────────────
REFERENCE_JSON = r'''{
  "test_title": "IELTS Listening Practice - Test 1",
  "sections": [
    {
      "section_name": "Part 1: Questions 1-5",
      "instruction": "Complete the table below. Write ONE WORD OR A NUMBER.",
      "questions": [
        {"q_numbers": "1", "type": "fill_in_blank", "content": "{{BLANK}}"},
        {"q_numbers": "2", "type": "fill_in_blank", "content": "{{BLANK}}"}
      ]
    },
    {
      "section_name": "Part 2: Questions 11-13",
      "instruction": "Choose the correct letter A, B or C.",
      "passage_or_context": "WINRIDGE FOREST RAILWAY PARK",
      "questions": [
        {
          "q_numbers": "11", "type": "multiple_choice",
          "content": "Simon's idea for a theme park came from",
          "options": ["A his childhood hobby","B his interest in landscape design","C his visit to another park"]
        }
      ]
    },
    {
      "section_name": "Part 2: Questions 14-18",
      "instruction": "Choose FIVE answers from the box and write the correct letter A-H.",
      "questions": [
        {
          "q_numbers": "14", "type": "matching",
          "content": "Simon {{BLANK}}",
          "options": ["A advertising","B animal care","C building","D educational links","E engine maintenance","F food and drink","G sales","H staffing"]
        }
      ]
    }
  ]
}'''

REFERENCE_PROCESSED = r'''{
  "test_title": "IELTS Listening Practice - Test 1",
  "sections": [
    {
      "section_name": "Part 1: Questions 1-5",
      "instruction": "Complete the table below. Write ONE WORD OR A NUMBER.",
      "questions": [
        {"q_numbers": "1-5", "type": "fill_in_blank", "content": "(1) {{BLANK}} (2) {{BLANK}} (3) {{BLANK}} (4) {{BLANK}} (5) {{BLANK}}"}
      ]
    },
    {
      "section_name": "Part 2: Questions 14-18",
      "instruction": "Choose FIVE answers from the box and write the correct letter A-H.",
      "questions": [
        {
          "q_numbers": "14-18", "type": "matching",
          "content": "Match each person to their current main area of work: 14. Simon {{BLANK}} 15. Liz {{BLANK}} 16. Sarah {{BLANK}} 17. Duncan {{BLANK}} 18. Judith {{BLANK}}",
          "options": ["A advertising","B animal care","C building","D educational links","E engine maintenance","F food and drink","G sales","H staffing"]
        }
      ]
    }
  ]
}'''

SYSTEM_PROMPT = """You are an IELTS test question extractor. You will receive the HTML content of an IELTS Listening test page.
Your job is to extract ALL questions and output them in a specific JSON format.

RULES:
1. Output ONLY valid JSON - no markdown fences, no commentary.
2. Include ALL 40 questions (questions 1-40).
3. Question types: "fill_in_blank", "multiple_choice", "matching", "map_labelling"
4. For fill_in_blank: use {{BLANK}} as placeholder for answers
5. For multiple_choice: include "options" array with letter-prefixed choices (e.g. "A some option")
6. For matching: include "options" array with the letter-choices from the box
7. For map_labelling: include the item text and {{BLANK}} placeholder, with "options" array of letter choices
8. Group questions by their Part and question range as shown in the HTML
9. Include "passage_or_context" only if there's a clear context heading
10. The "instruction" should capture the exact wording (e.g. "Write ONE WORD ONLY", "Choose the correct letter, A, B or C")
11. Each question gets its own object with a single q_numbers value (e.g. "1", "2", etc.)

IMPORTANT: Ignore the answer key section. Only extract the QUESTIONS.
"""

PROCESSED_SYSTEM_PROMPT = """You are an IELTS test question processor. You will receive a JSON of IELTS test questions (Test_X.json format).
Your job is to produce a "processed" version with these changes:

RULES:
1. Output ONLY valid JSON - no markdown fences, no commentary.
2. For consecutive fill_in_blank questions in the same section: MERGE them into ONE question object.
   - q_numbers becomes a range like "1-5" or "21-30"
   - content becomes a single string with all blanks: "(1) {{BLANK}} (2) {{BLANK}} ..."
   - If there's context text around the blanks, preserve it inline
3. For consecutive matching questions sharing the same options: MERGE them into ONE question object.
   - q_numbers becomes a range like "14-18"
   - content lists all items: "14. Simon {{BLANK}} 15. Liz {{BLANK}} ..."
   - Keep the shared options array
4. For multiple_choice: keep each question separate (do NOT merge)
5. For map_labelling: MERGE consecutive ones sharing same options into one object
6. Keep all section_name, instruction, passage_or_context fields unchanged
"""


def call_omniroute(system_prompt: str, user_content: str, max_retries: int = 3) -> str:
    """Call OmniRoute API with retries."""
    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.1,
        "max_tokens": 16000
    }).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OMNIROUTE_API_KEY}"
    }

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(OMNIROUTE_BASE_URL, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                content = result["choices"][0]["message"]["content"]
                # Strip markdown code fences if present
                content = re.sub(r'^```(?:json)?\s*\n?', '', content.strip())
                content = re.sub(r'\n?```\s*$', '', content.strip())
                return content
        except (urllib.error.URLError, urllib.error.HTTPError, Exception) as e:
            print(f"  ⚠ Attempt {attempt+1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                wait = (attempt + 1) * 10
                print(f"  ⏳ Retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise


def extract_html_body(html_content: str) -> str:
    """Extract only the passage-pane content from HTML to reduce token usage."""
    # Try to extract just the passage-pane div content
    match = re.search(r'<div class="passage-pane"[^>]*>(.*?)</div>\s*<div class="resizer"', html_content, re.DOTALL)
    if match:
        return match.group(1)
    # Fallback: extract body content
    match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL)
    if match:
        return match.group(1)
    return html_content


def find_missing_tests() -> list:
    """Find all Test_X folders missing Test_X.json."""
    missing = []
    for item in sorted(os.listdir(FULLTEST_DIR)):
        test_dir = os.path.join(FULLTEST_DIR, item)
        if os.path.isdir(test_dir) and item.startswith("Test_"):
            json_file = os.path.join(test_dir, f"{item}.json")
            if not os.path.exists(json_file):
                html_file = os.path.join(test_dir, f"{item}.html")
                if os.path.exists(html_file):
                    missing.append(item)
    return missing


def process_test(test_name: str):
    """Process a single test: extract JSON from HTML, then create processed version."""
    test_dir = os.path.join(FULLTEST_DIR, test_name)
    html_path = os.path.join(test_dir, f"{test_name}.html")
    json_path = os.path.join(test_dir, f"{test_name}.json")
    processed_path = os.path.join(test_dir, f"{test_name}_processed.json")

    print(f"\n{'='*60}")
    print(f"📝 Processing {test_name}...")
    print(f"{'='*60}")

    # Step 1: Read HTML
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    body_content = extract_html_body(html_content)

    # Step 2: Extract questions via OmniRoute
    print(f"  🔄 Step 1/2: Extracting questions from HTML...")
    user_msg = f"""Here is a reference example of the expected output format:
{REFERENCE_JSON}

Now extract ALL questions from this IELTS Listening test HTML:

{body_content}"""

    raw_json_str = call_omniroute(SYSTEM_PROMPT, user_msg)

    try:
        raw_data = json.loads(raw_json_str)
    except json.JSONDecodeError as e:
        print(f"  ❌ Failed to parse JSON for {test_name}: {e}")
        print(f"  Raw response (first 500 chars): {raw_json_str[:500]}")
        # Save raw response for debugging
        debug_path = os.path.join(test_dir, f"{test_name}_debug.txt")
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(raw_json_str)
        return False

    # Save Test_X.json
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Saved {test_name}.json")

    # Step 3: Create processed version via OmniRoute
    print(f"  🔄 Step 2/2: Creating processed version...")
    time.sleep(2)  # Brief pause between API calls

    proc_user_msg = f"""Here is a reference example showing how to transform the raw JSON into the processed format:

INPUT (raw):
{REFERENCE_JSON}

OUTPUT (processed):
{REFERENCE_PROCESSED}

Now process this raw JSON into the processed format:

{json.dumps(raw_data, indent=2, ensure_ascii=False)}"""

    proc_json_str = call_omniroute(PROCESSED_SYSTEM_PROMPT, proc_user_msg)

    try:
        proc_data = json.loads(proc_json_str)
    except json.JSONDecodeError as e:
        print(f"  ❌ Failed to parse processed JSON for {test_name}: {e}")
        debug_path = os.path.join(test_dir, f"{test_name}_processed_debug.txt")
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(proc_json_str)
        return False

    # Save Test_X_processed.json
    with open(processed_path, "w", encoding="utf-8") as f:
        json.dump(proc_data, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Saved {test_name}_processed.json")

    return True


def main():
    missing = find_missing_tests()
    print(f"🔍 Found {len(missing)} tests missing JSON files:")
    for t in missing:
        print(f"  - {t}")

    if not missing:
        print("✅ All tests already have JSON files!")
        return

    success = 0
    failed = []
    for i, test_name in enumerate(missing, 1):
        print(f"\n[{i}/{len(missing)}] ", end="")
        try:
            if process_test(test_name):
                success += 1
            else:
                failed.append(test_name)
        except Exception as e:
            print(f"  ❌ Error processing {test_name}: {e}")
            failed.append(test_name)

        # Rate limiting pause between tests
        if i < len(missing):
            print("  ⏳ Pausing 3s before next test...")
            time.sleep(3)

    print(f"\n{'='*60}")
    print(f"📊 SUMMARY")
    print(f"{'='*60}")
    print(f"  ✅ Success: {success}/{len(missing)}")
    if failed:
        print(f"  ❌ Failed:  {', '.join(failed)}")
    else:
        print(f"  🎉 All tests processed successfully!")


if __name__ == "__main__":
    main()
