import pandas as pd
from openpyxl import load_workbook

def fix_excel():
    excel_path = "UPGRADE YOUR ILETS SKILLS.xlsx"
    print(f"Fixing {excel_path}...")
    
    df = pd.read_excel(excel_path, sheet_name="Students")
    
    # Rename Mã số to ID HỌC VIÊN
    rename_map = {"Mã số": "ID HỌC VIÊN"}
    df.rename(columns=rename_map, inplace=True)
    
    headers = [
        "Họ và Tên", 
        "ID HỌC VIÊN", 
        "Device ID", 
        "Ngày Bắt Đầu", 
        "Reading 1323", 
        "Listening 102", 
        "Full Tests", 
        "Tạo Kế Hoạch"
    ]
    
    # Rename existing columns to drop the "(Tick)" part if present, or just ensure they exist
    for col in df.columns:
        if "Reading" in col: df.rename(columns={col: "Reading 1323"}, inplace=True)
        if "Listening" in col: df.rename(columns={col: "Listening 102"}, inplace=True)
        if "Full Tests" in col: df.rename(columns={col: "Full Tests"}, inplace=True)
        if "Tạo Kế Hoạch" in col: df.rename(columns={col: "Tạo Kế Hoạch"}, inplace=True)
        
    for h in headers:
        if h not in df.columns:
            df[h] = ""
            
    df = df[headers]
    
    # Pre-fill checkboxes for existing students to True (boolean) so they generate correctly
    # If a student has a name, let's just make their first 3 packages True and "Tạo Kế Hoạch" False
    for i, row in df.iterrows():
        if pd.notna(row["Họ và Tên"]) and str(row["Họ và Tên"]).strip() != "":
            df.at[i, "Reading 1323"] = True
            df.at[i, "Listening 102"] = True
            df.at[i, "Full Tests"] = False
            df.at[i, "Tạo Kế Hoạch"] = False
            
    with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name="Students", index=False)
        
    print("Excel fixed successfully.")

if __name__ == "__main__":
    fix_excel()
