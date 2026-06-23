import pandas as pd
from datetime import datetime, timedelta

excel_path = '/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS LISTENING/UPGRADE YOUR ILETS LISTENING.xlsx'

# Prepare list of lessons
basics = [f"Basic_Lesson_{i}" for i in range(1, 35)]
inters = [f"Intermediate_Lesson_{i}" for i in range(1, 35)]
advs = [f"Advanced_Lesson_{i}" for i in range(1, 35)]

# Mix them: 1 basic, 1 inter, 1 adv continuously
all_lessons = []
for i in range(34):
    all_lessons.append(basics[i])
    all_lessons.append(inters[i])
    all_lessons.append(advs[i])

# Total 102 lessons. Spread over 30 days.
start_date = datetime(2026, 6, 16)
end_date = datetime(2026, 7, 15)
num_days = (end_date - start_date).days + 1 # 30 days

# Distribute lessons over num_days
lessons_per_day = 102 // num_days
remainder = 102 % num_days

schedule = []
lesson_idx = 0
for day in range(num_days):
    current_date = start_date + timedelta(days=day)
    date_str = current_date.strftime("%d/%m/%Y")
    
    daily_count = lessons_per_day + (1 if day < remainder else 0)
    for _ in range(daily_count):
        if lesson_idx < len(all_lessons):
            schedule.append({
                "Ngày Học": date_str,
                "Tên Bài Tập": all_lessons[lesson_idx],
                "Trạng Thái": "Chưa Hoàn Thành",
                "Link Học": "https://ngoclong1209.github.io/pte-listening-audios/"
            })
            lesson_idx += 1

df = pd.DataFrame(schedule)

# Write to Excel
with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name='📅 Kế hoạch 30 ngày', index=False)

print("Successfully generated Study Plan!")
