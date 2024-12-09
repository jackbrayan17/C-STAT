# calc_variation/variation.py

import os
import pandas as pd
from tqdm import tqdm  # Progress bar library

# Suppress FutureWarning related to downcasting
pd.set_option('future.no_silent_downcasting', True)

# Expected sheet names
expected_sheets = ["actif", "passif", "cpte de result Charges", "cpte de result Produits"]

def get_unique_filename(base_name, extension):
    """Generate a unique filename to avoid overwriting files."""
    counter = 1
    while True:
        output_file = f"{base_name}{counter}{extension}"
        if not os.path.exists(output_file):
            return output_file
        counter += 1

def ensure_var_directory():
    """Ensure the 'var' directory exists."""
    var_directory = os.path.join(os.path.dirname(__file__), 'var')
    if not os.path.exists(var_directory):
        os.makedirs(var_directory)
    return var_directory

def read_sheets(file, sheet_names, progress_desc):
    """Read sheets from the provided Excel file."""
    data = {}
    all_sheets = pd.ExcelFile(file).sheet_names
    for sheet in tqdm(sheet_names, desc=progress_desc, unit="sheet"):
        if sheet in all_sheets:
            try:
                df = pd.read_excel(file, sheet_name=sheet, usecols=["Item", "Total"])
                df["Order"] = range(len(df))
                data[sheet] = df
            except Exception as e:
                print(f"Error reading sheet {sheet} in file {file}: {e}")
        else:
            print(f"Sheet '{sheet}' not found in file {file}. Skipping...")
    return data

def calculate_variation(file1, file2):
    """Calculate variation between two Excel files and save the result."""
    # Ensure 'var' directory exists
    var_directory = ensure_var_directory()
    
    # Create unique output file name
    output_file = get_unique_filename(os.path.join(var_directory, "var"), ".xlsx")
    
    data_et1 = read_sheets(file1, expected_sheets, progress_desc="File 1 Processing")
    data_et2 = read_sheets(file2, expected_sheets, progress_desc="File 2 Processing")

    summary = {}
    for sheet in tqdm(expected_sheets, desc="Processing Sheets", unit="sheet"):
        df1 = data_et1.get(sheet, pd.DataFrame(columns=["Item", "Total", "Order"]))
        df2 = data_et2.get(sheet, pd.DataFrame(columns=["Item", "Total", "Order"]))

        merged = pd.merge(
            df1, 
            df2, 
            on="Item", 
            how="outer", 
            suffixes=('_Trim1', '_Trim2')
        ).fillna(0).infer_objects()

        merged["Order"] = merged["Order_Trim1"].combine_first(merged["Order_Trim2"])
        merged = merged.sort_values(by="Order").drop(columns=["Order_Trim1", "Order_Trim2"])

        merged["Variation (FCFA)"] = merged["Total_Trim2"] - merged["Total_Trim1"]
        merged["Variation (%)"] = ((merged["Total_Trim2"] - merged["Total_Trim1"]) / merged["Total_Trim1"]) * 100

        # Replace 'inf' values with 100
        merged["Variation (%)"] = merged["Variation (%)"].replace([float('inf'), -float('inf')], 100)

        merged = merged.drop(columns=["Order"])
        summary[sheet] = merged

    # Save the summary to the Excel file
    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        for sheet_name in tqdm(expected_sheets, desc="Writing Sheets", unit="sheet"):
            if sheet_name in summary:
                summary[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Get the worksheet object
                worksheet = writer.sheets[sheet_name]
                
                # Set column widths and format
                for idx, col in enumerate(summary[sheet_name].columns):
                    max_len = max(
                        summary[sheet_name][col].astype(str).map(len).max(),
                        len(col)
                    )
                    worksheet.set_column(idx, idx, max_len + 2)  # Adjust column width

                    # Set specific format for numeric columns to avoid scientific notation
                    if summary[sheet_name][col].dtype in ['float64', 'int64']:
                        num_format = writer.book.add_format({'num_format': '0'})  # No scientific notation
                        worksheet.set_column(idx, idx, max_len + 2, num_format)

    return output_file
