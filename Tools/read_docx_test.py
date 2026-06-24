import docx
import sys

def read_docx(file_path):
    doc = docx.Document(file_path)
    for i, p in enumerate(doc.paragraphs):
        if i > 20: break
        if p.text.strip():
            print(f"[{i}] {p.text.strip()}")

if __name__ == "__main__":
    read_docx(sys.argv[1])
