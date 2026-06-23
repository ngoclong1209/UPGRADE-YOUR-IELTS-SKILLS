import pandas as pd
from openpyxl import load_workbook

def fix_excel():
    excel_path = "UPGRADE YOUR ILETS SKILLS.xlsx"
    print(f"Fixing {excel_path}...")
    
    df = pd.read_excel(excel_path, sheet_name="Students")
    
    # We will remove "Tạo Kế Hoạch" and add "Xoá Học Viên"
    if "Tạo Kế Hoạch" in df.columns:
        df.drop(columns=["Tạo Kế Hoạch"], inplace=True)
        
    headers = [
        "Họ và Tên", 
        "ID HỌC VIÊN", 
        "Device ID", 
        "Ngày Bắt Đầu", 
        "Reading 1323", 
        "Listening 102", 
        "Full Tests", 
        "Xoá Học Viên"
    ]
    
    for h in headers:
        if h not in df.columns:
            df[h] = ""
            
    df = df[headers]
    
    for i, row in df.iterrows():
        if pd.notna(row["Họ và Tên"]) and str(row["Họ và Tên"]).strip() != "":
            # Set to False by default
            df.at[i, "Xoá Học Viên"] = False
            # Ensure others are False initially to allow triggering
            df.at[i, "Reading 1323"] = False
            df.at[i, "Listening 102"] = False
            df.at[i, "Full Tests"] = False
            
    with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name="Students", index=False)
        
    print("Excel fixed successfully.")

if __name__ == "__main__":
    fix_excel()
