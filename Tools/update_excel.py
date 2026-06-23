import pandas as pd

excel_path = 'UPGRADE YOUR ILETS SKILLS.xlsx'
xls = pd.ExcelFile(excel_path)
writer = pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace')

for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name)
    if 'URL' in df.columns:
        df['URL'] = df['URL'].astype(str).str.replace('ielts-reading-app', 'Reading_1232_Basic', regex=False)
        df['URL'] = df['URL'].astype(str).str.replace('ReadingA1-C2', 'Reading_1232_Basic', regex=False)
        df['URL'] = df['URL'].astype(str).str.replace('pte-listening-audios', 'Listening_102_Basic', regex=False)
        df['URL'] = df['URL'].astype(str).str.replace('practicepteonline/listening', 'Practice_FullTests/Listening_204_FullTest', regex=False)
        df['URL'] = df['URL'].astype(str).str.replace('practicepteonline/reading', 'Practice_FullTests/Reading_315_FullTest', regex=False)
    
    df.to_excel(writer, sheet_name=sheet_name, index=False)

writer.close()
print("Excel updated successfully.")
