import pandas as pd

def explore_excel(file_path):
    # Load the excel file to see sheet names
    xl = pd.ExcelFile(file_path)
    print(f"Sheet names: {xl.sheet_names}")
    
    for sheet in xl.sheet_names:
        print(f"\n--- Sheet: {sheet} ---")
        df = pd.read_excel(file_path, sheet_name=sheet)
        print(f"Colums: {df.columns.tolist()}")
        print(f"Shape: {df.shape}")
        print("First 5 rows:")
        print(df.head())
        print("\nMissing values:")
        print(df.isnull().sum())

if __name__ == "__main__":
    file_path = "/home/david/Escritorio/ML_HeatEnthalpyFormation/data/raw/SI_data_2020.xlsx"
    explore_excel(file_path)
