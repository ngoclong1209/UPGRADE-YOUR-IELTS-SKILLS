#!/usr/bin/env python3
"""
Unified IELTS JSON Extractor — Listening + Reading
Uses OmniRoute local proxy to extract structured JSON from HTML test files.
Handles SSE streaming responses.
"""

import os, sys, json, re, time, traceback
import urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Config ──────────────────────────────────────────────────────────────
OMNIROUTE_API_KEY = "sk-92d3ef3c86e600b6-ef9847-d92a108c"
OMNIROUTE_URL = "http://localhost:20128/v1/chat/completions"
MODEL = "auto/best-fast"
MAX_WORKERS = 3
PAUSE_BETWEEN = 1.0
MAX_RETRIES = 3

BASE = os.path.dirname(os.path.abspath(__file__))
LISTENING_DIR = os.path.join(BASE, "Listening_204_FullTest")
READING_DIR   = os.path.join(BASE, "Reading_315_FullTest")

# ── Prompts ─────────────────────────────────────────────────────────────

LISTENING_EXTRACT_SYSTEM = """You are an IELTS Listening test question extractor. Given the HTML content of a test page, extract ALL questions into JSON.

OUTPUT FORMAT (JSON only, no markdown fences, no commentary):
{
  "test_title": "IELTS Listening Practice - Test X",
  "sections": [
    {
      "section_name": "Part N: Questions X-Y",
      "instruction": "...",
      "passage_or_context": "...",
      "questions": [
        {
          "q_numbers": "1",
          "type": "fill_in_blank|multiple_choice|matching|map_labelling",
          "content": "...",
          "options": ["A ...", "B ..."]
        }
      ]
    }
  ]
}

RULES:
- Include ALL 40 questions. Each gets its own object with single q_numbers.
- fill_in_blank: use {{BLANK}} placeholder
- multiple_choice: include "options" array
- matching/map_labelling: include "options" from the box
- Ignore ANSWER KEY section
- Output ONLY valid JSON, nothing else"""

READING_EXTRACT_SYSTEM = """You are an IELTS Reading test question extractor. Given the HTML content of a test page, extract ALL questions into JSON.

OUTPUT FORMAT (JSON only, no markdown fences, no commentary):
{
  "test_title": "IELTS Reading Practice - Test X",
  "sections": [
    {
      "section_name": "Reading Passage N: Title",
      "instruction": "",
      "passage_or_context": "Full passage text...",
      "questions": [
        {
          "q_numbers": "1-8",
          "type": "yes_no_not_given|true_false_not_given|multiple_choice|matching|matching_information|matching_headings|matching_features|sentence_completion|summary_completion|short_answer|fill_in_blank|diagram_labelling|flow_chart",
          "content": "Question text...",
          "options": ["A ...", "B ..."]
        }
      ]
    }
  ]
}

RULES:
- Include ALL questions across all passages
- Include FULL reading passage text in passage_or_context
- For yes/no/not_given, true/false/not_given: include options array
- Group by passage and question range
- Ignore ANSWER KEY
- Output ONLY valid JSON, nothing else"""

PROCESSED_SYSTEM = """Transform a raw IELTS JSON into a "processed" version:
1. Consecutive fill_in_blank in same section → MERGE into ONE (q_numbers="1-5", content="(1) {{BLANK}} (2) {{BLANK}}...")
2. Consecutive matching with same options → MERGE into ONE
3. multiple_choice → keep separate
4. Keep section_name, instruction, passage_or_context unchanged
Output ONLY valid JSON, nothing else."""


# ── API Helper with SSE parsing ─────────────────────────────────────────

def call_api(system_prompt: str, user_content: str) -> str:
    """Call OmniRoute local proxy, handle SSE streaming response."""
    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.1,
        "max_tokens": 30000,
        "stream": False
    }).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OMNIROUTE_API_KEY}"
    }

    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(OMNIROUTE_URL, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=300) as resp:
                raw = resp.read().decode("utf-8")

            # Try parsing as normal JSON first
            try:
                result = json.loads(raw)
                content = result["choices"][0]["message"]["content"]
                return clean_response(content)
            except (json.JSONDecodeError, KeyError):
                pass

            # Parse as SSE stream
            content_parts = []
            for line in raw.split("\n"):
                line = line.strip()
                if line.startswith("data: ") and line != "data: [DONE]":
                    try:
                        chunk = json.loads(line[6:])
                        delta = chunk.get("choices", [{}])[0].get("delta", {})
                        c = delta.get("content", "")
                        if c:
                            content_parts.append(c)
                    except json.JSONDecodeError:
                        continue

            if content_parts:
                return clean_response("".join(content_parts))

            # If we got here, the response might be an error
            if "error" in raw.lower():
                raise Exception(f"API error: {raw[:300]}")
            raise Exception(f"Could not parse response: {raw[:300]}")

        except Exception as e:
            print(f"    ⚠ API attempt {attempt+1}/{MAX_RETRIES}: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep((attempt + 1) * 5)
            else:
                raise


def clean_response(text: str) -> str:
    """Strip markdown fences and whitespace."""
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*\n?', '', text)
    text = re.sub(r'\n?```\s*$', '', text)
    return text.strip()


def extract_passage_pane(html: str) -> str:
    """Extract passage-pane content from HTML."""
    m = re.search(r'<div class="passage-pane"[^>]*>(.*?)</div>\s*<div class="resizer"', html, re.DOTALL)
    if m:
        return m.group(1)
    m = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    return m.group(1) if m else html


def parse_json_response(text: str) -> dict:
    """Parse JSON, handling edge cases."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r'\{[\s\S]*\}', text)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    raise json.JSONDecodeError("Cannot parse JSON", text[:200], 0)


# ── Task processors ────────────────────────────────────────────────────

def process_extract_json(test_dir, test_name, test_type):
    html_path = os.path.join(test_dir, f"{test_name}.html")
    json_path = os.path.join(test_dir, f"{test_name}.json")

    if not os.path.exists(html_path):
        return f"⏭ {test_name}: no HTML"

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    body = extract_passage_pane(html)
    system = LISTENING_EXTRACT_SYSTEM if test_type == "listening" else READING_EXTRACT_SYSTEM

    content = call_api(system, f"Extract ALL questions from this IELTS {test_type} test HTML:\n\n{body}")
    data = parse_json_response(content)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return f"✅ {test_name}.json"


def process_create_processed(test_dir, test_name):
    json_path = os.path.join(test_dir, f"{test_name}.json")
    proc_path = os.path.join(test_dir, f"{test_name}_processed.json")

    with open(json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    raw_str = json.dumps(raw_data, indent=2, ensure_ascii=False)
    content = call_api(PROCESSED_SYSTEM, f"Transform this raw IELTS JSON into processed format:\n\n{raw_str}")
    data = parse_json_response(content)

    with open(proc_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return f"✅ {test_name}_processed.json"


def process_task(task):
    try:
        if task["task"] == "extract":
            msg = process_extract_json(task["dir"], task["name"], task["test_type"])
        else:
            msg = process_create_processed(task["dir"], task["name"])
        time.sleep(PAUSE_BETWEEN)
        return {"name": task["name"], "task": task["task"], "status": "ok", "msg": msg}
    except Exception as e:
        return {"name": task["name"], "task": task["task"], "status": "error",
                "msg": f"❌ {task['name']} ({task['task']}): {e}"}


# ── Scanner ─────────────────────────────────────────────────────────────

def scan_missing(base_dir, test_type):
    tasks = []
    if not os.path.isdir(base_dir):
        return tasks
    for item in sorted(os.listdir(base_dir)):
        d = os.path.join(base_dir, item)
        if not os.path.isdir(d) or not item.startswith("Test_"):
            continue
        json_f = os.path.join(d, f"{item}.json")
        proc_f = os.path.join(d, f"{item}_processed.json")
        html_f = os.path.join(d, f"{item}.html")
        if not os.path.exists(json_f):
            if os.path.exists(html_f):
                tasks.append({"dir": d, "name": item, "task": "extract", "test_type": test_type, "pri": 1})
        elif not os.path.exists(proc_f):
            tasks.append({"dir": d, "name": item, "task": "processed", "test_type": test_type, "pri": 2})
    return tasks


# ── Main ────────────────────────────────────────────────────────────────

def main():
    print("🔍 Scanning...\n")
    l_tasks = scan_missing(LISTENING_DIR, "listening")
    r_tasks = scan_missing(READING_DIR, "reading")

    le = sum(1 for t in l_tasks if t["task"] == "extract")
    lp = sum(1 for t in l_tasks if t["task"] == "processed")
    re_ = sum(1 for t in r_tasks if t["task"] == "extract")
    rp = sum(1 for t in r_tasks if t["task"] == "processed")

    print(f"📊 Listening: {le} missing .json, {lp} missing _processed.json")
    print(f"📊 Reading:   {re_} missing .json, {rp} missing _processed.json")

    all_tasks = sorted(l_tasks + r_tasks, key=lambda t: (t["pri"], t["name"]))
    total = len(all_tasks)
    print(f"\n🚀 Total: {total} tasks | {MAX_WORKERS} workers | Model: {MODEL}")
    print(f"   Endpoint: {OMNIROUTE_URL}")

    if not total:
        print("✅ Nothing to do!")
        return

    print("=" * 70)
    success = errors = done = 0
    failed_names = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_task, t): t for t in all_tasks}
        for future in as_completed(futures):
            done += 1
            r = future.result()
            print(f"  [{done}/{total}] {r['msg']}")
            if r["status"] == "ok":
                success += 1
            else:
                errors += 1
                failed_names.append(f"{r['name']}({r['task']})")

    print("\n" + "=" * 70)
    print(f"📊 Done: {success}✅  {errors}❌  / {total} total")
    if failed_names:
        print(f"❌ Failed: {', '.join(failed_names[:20])}")
        if len(failed_names) > 20:
            print(f"   ... and {len(failed_names)-20} more")
    else:
        print("🎉 All done!")


if __name__ == "__main__":
    main()
