import pandas as pd
excel_path = '/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS/UPGRADE YOUR ILETS SKILLS.xlsx'
xls = pd.ExcelFile(excel_path)
for sheet_name in xls.sheet_names:
    print(f"Sheet: {sheet_name}")
    df = pd.read_excel(xls, sheet_name)
    print(f"Columns: {list(df.columns)}")
    print(f"First row: {df.head(1).to_dict('records')}")
    print("-" * 50)
