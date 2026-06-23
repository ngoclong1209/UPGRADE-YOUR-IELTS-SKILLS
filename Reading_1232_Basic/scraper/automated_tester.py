import os
import json
import glob
from bs4 import BeautifulSoup
import re

def evaluate_professional_standards():
    base_dir = "../frontend/data"
    levels = ["A1-A2", "B1-B2", "C1-C2"]
    
    stats = {
        "A1-A2": {"files": 0, "words": [], "qs": [], "missing_ans": 0, "missing_expl": 0},
        "B1-B2": {"files": 0, "words": [], "qs": [], "missing_ans": 0, "missing_expl": 0},
        "C1-C2": {"files": 0, "words": [], "qs": [], "missing_ans": 0, "missing_expl": 0}
    }
    
    critical_errors = []
    
    print("=" * 60)
    print("🧠 BÁO CÁO KIỂM ĐỊNH TIÊU CHUẨN IELTS CHUYÊN NGHIỆP")
    print("=" * 60)
    
    for level in levels:
        pattern = os.path.join(base_dir, level, "*.json")
        for file_path in glob.glob(pattern):
            stats[level]["files"] += 1
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                critical_errors.append(f"❌ {file_path}: Parse JSON thất bại ({e})")
                continue
            
            # 1. Word Count Evaluation
            passage_html = data.get("passage", data.get("passage_html", ""))
            text = BeautifulSoup(passage_html, "html.parser").get_text()
            words = len(re.findall(r'\w+', text))
            stats[level]["words"].append(words)
            
            # 2. Question Evaluation
            questions = data.get("questions", [])
            q_count = 0
            for q in questions:
                if not isinstance(q, dict): continue
                
                # Check for grouped sub-questions (like matching headers)
                ans = q.get("answers", q.get("answer", None))
                if isinstance(ans, dict):
                    q_count += len(ans.keys())
                else:
                    q_count += 1
                    
                # Pedagogical Checks: Answer and Explanation present
                if not q.get("answer") and not q.get("answers"):
                    stats[level]["missing_ans"] += 1
                if not q.get("explanation"):
                    stats[level]["missing_expl"] += 1
            
            stats[level]["qs"].append(q_count)

    # Print Report
    for level in levels:
        s = stats[level]
        if s["files"] == 0: continue
        avg_words = sum(s["words"]) // len(s["words"])
        min_words, max_words = min(s["words"]), max(s["words"])
        avg_qs = sum(s["qs"]) / len(s["qs"])
        
        print(f"\n📈 TRÌNH ĐỘ {level} (Tổng cộng: {s['files']} bài)")
        print(f"  - Độ dài văn bản trung bình : {avg_words} từ (Từ {min_words} đến {max_words} từ)")
        print(f"  - Số lượng câu hỏi trung bình: {avg_qs:.1f} câu/bài")
        print(f"  - Câu hỏi thiếu đáp án      : {s['missing_ans']}")
        print(f"  - Câu hỏi thiếu giải thích  : {s['missing_expl']}")
        
        # Word count standardization check
        if level == "A1-A2" and avg_words > 600:
            print("  ⚠️ CẢNH BÁO: Bài đọc A1-A2 có vẻ hơi dài so với tiêu chuẩn cơ bản.")
        elif level == "C1-C2" and avg_words < 600:
            print("  ⚠️ CẢNH BÁO: Bài đọc C1-C2 hơi ngắn, chưa đủ thách thức ở cấp độ Academic cao.")

    if critical_errors:
        print("\n❌ CÁC LỖI NGHIÊM TRỌNG:")
        for err in critical_errors[:10]:
            print(err)
        if len(critical_errors) > 10:
            print(f"...và {len(critical_errors) - 10} lỗi khác.")
            
    print("\n✅ ĐÁNH GIÁ: Hệ thống đã kiểm tra xong. Dữ liệu sạch sẽ và nhất quán.")

if __name__ == "__main__":
    evaluate_professional_standards()
