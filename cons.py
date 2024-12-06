import pandas as pd
import os

# File path
file_path = "filt1.xlsx"

# Load all sheets
excel_file = pd.ExcelFile(file_path)
sheets = excel_file.sheet_names

# Initialize an empty DataFrame
combined_df = pd.DataFrame()

# Iterate through each sheet
for sheet_name in sheets:
    # Load the sheet into a DataFrame
    sheet_df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Add 'Sheet Name' column
    sheet_df['Sheet Name'] = sheet_name
    
    # Ensure 'Year' and 'Country' columns exist
    if 'Year' not in sheet_df.columns:
        sheet_df['Year'] = None  # Placeholder
    if 'Country' not in sheet_df.columns:
        sheet_df['Country'] = None  # Placeholder

    # Append the DataFrame
    combined_df = pd.concat([combined_df, sheet_df], ignore_index=True)

# Determine output file name
base_output_path = "combined_sheets"
output_path = f"{base_output_path}.xlsx"
counter = 1

while os.path.exists(output_path):
    output_path = f"{base_output_path}{counter}.xlsx"
    counter += 1

# Save the combined DataFrame to the new file
combined_df.to_excel(output_path, index=False)

print(f"Combined data saved to {output_path}")