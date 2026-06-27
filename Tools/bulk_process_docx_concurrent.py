import os
import glob
import json
import random
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from process_docx_ai import extract_text_from_docx, process_with_ai

DIRECTORIES = [
    "Listening_204_FullTest",
    "Reading_315_FullTest",
    "Listening_docx",
    "Reading_docx"
]

MODEL_POOL = [
    "oc/deepseek-v4-flash-free",
    "oc/minimax-m3-free",
    "oc/ling-2.6-1t-free",
    "oc/nemotron-3-super-free"
]

MAX_WORKERS = 5
MAX_RETRIES = 3

def process_single_file(docx_path):
    json_path = docx_path.replace(".docx", ".json")
    
    if os.path.exists(json_path):
        return f"Skipped (already exists): {json_path}"
        
    print(f"[{os.path.basename(docx_path)}] Extracting text...")
    try:
        text = extract_text_from_docx(docx_path)
    except Exception as e:
        return f"ERROR (Extract) {docx_path}: {e}"
        
    if not text:
        return f"Skipped (Empty text): {docx_path}"

    retries = 0
    while retries < MAX_RETRIES:
        if not MODEL_POOL:
            return f"ERROR: Model pool is empty! Cannot process {docx_path}"
            
        selected_model = random.choice(MODEL_POOL)
        print(f"[{os.path.basename(docx_path)}] Sending API using: {selected_model} (Try {retries+1}/{MAX_RETRIES})")
        
        try:
            result_json = process_with_ai(text, model_id=selected_model)
            
            # Verify JSON
            json.loads(result_json)
            
            with open(json_path, "w", encoding="utf-8") as f:
                f.write(result_json)
            return f"SUCCESS: {json_path} (Model: {selected_model})"
            
        except Exception as e:
            err_msg = str(e)
            print(f"[{os.path.basename(docx_path)}] Model {selected_model} failed: {err_msg[:200]}")
            retries += 1
            time.sleep(3) 
            
    return f"FAILED to process {docx_path} after {MAX_RETRIES} retries."

def main():
    files_to_process = []
    
    for directory in DIRECTORIES:
        if not os.path.exists(directory):
            print(f"Directory {directory} not found, skipping...")
            continue
            
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".docx") and not file.startswith("~"):
                    files_to_process.append(os.path.join(root, file))
                    
    print(f"Found {len(files_to_process)} docx files to process.")
    
    success_count = 0
    failed_count = 0
    completed_files = 0
    total_files = len(files_to_process)
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_single_file, docx): docx for docx in files_to_process}
        
        for future in as_completed(futures):
            try:
                result = future.result()
                print(result)
                completed_files += 1
                
                if "SUCCESS" in result or "Skipped" in result:
                    success_count += 1
                else:
                    failed_count += 1
                
                if "SUCCESS" in result:
                    filename = os.path.basename(futures[future])
                    msg = f"Đã xong: {filename}. Tiến độ: {completed_files}/{total_files}"
                    os.system(f"osascript -e 'display notification \"{msg}\" with title \"Antigravity JSON Extractor\" sound name \"Glass\"'")
                    
            except Exception as e:
                print(f"Worker generated an exception: {e}")
                failed_count += 1
                completed_files += 1
                
    print(f"\n--- PROCESSING COMPLETE ---")
    print(f"Total Success/Skipped: {success_count}")
    print(f"Total Failed: {failed_count}")

if __name__ == "__main__":
    main()
