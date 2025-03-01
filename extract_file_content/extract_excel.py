import pandas as pd

def extract_text_from_excel(excel_path):
    text = ""
    xls = pd.ExcelFile(excel_path)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        text += df.to_string() + "\n"
    return text

if __name__ == "__main__":
    # Test
    excel_file = "D:\\test\\Financial Sample.xlsx"
    extracted_text = extract_text_from_excel(excel_file)
    print(extracted_text)
