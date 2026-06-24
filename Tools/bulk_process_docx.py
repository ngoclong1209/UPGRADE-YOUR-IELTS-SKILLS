import os
import glob
from process_docx_ai import extract_text_from_docx, process_with_ai

DIRECTORIES = [
    "Listening_204_FullTest",
    "Reading_315_FullTest",
    "Listening_docx",
    "Reading_docx"
]

def main():
    for directory in DIRECTORIES:
        if not os.path.exists(directory):
            print(f"Directory {directory} not found, skipping...")
            continue
            
        print(f"Scanning directory: {directory}")
        # Find all docx files recursively
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".docx") and not file.startswith("~"):
                    docx_path = os.path.join(root, file)
                    json_path = docx_path.replace(".docx", ".json")
                    
                    if os.path.exists(json_path):
                        print(f"Skipping {docx_path}, JSON already exists.")
                        continue
                        
                    print(f"Processing {docx_path}...")
                    try:
                        text = extract_text_from_docx(docx_path)
                        # We print snippet of text to avoid huge logs
                        print(f"  Extracted {len(text)} characters.")
                        if len(text.strip()) == 0:
                            print(f"  Warning: Empty document {docx_path}")
                            continue
                            
                        json_result = process_with_ai(text)
                        
                        with open(json_path, "w", encoding="utf-8") as f:
                            f.write(json_result)
                            
                        print(f"  Success! Saved to {json_path}")
                        
                    except Exception as e:
                        print(f"  Failed to process {docx_path}: {e}")

if __name__ == "__main__":
    main()
