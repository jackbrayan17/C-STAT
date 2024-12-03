import pandas as pd

def filter_excel_file_single_sheet(input_file, output_file):
    # Load the Excel file
    df = pd.read_excel(input_file, sheet_name=0, header=None, engine='openpyxl')

    # Define relevant cells and ranges
    title_cells = ['A2816', 'A2838']
    country_ranges = [(2819, 2824), (2841, 2846)]
    date_row = 2814
    filter_row = 2815

    # Initialize a list to store combined filtered data
    all_filtered_data = []

    for index, title_cell in enumerate(title_cells):
        # Extract title from the specified cell
        title = df.loc[int(title_cell[1:]) - 1, 0]
        country_range = country_ranges[index]

        # Get countries
        countries = [df.loc[i - 1, 0] for i in range(country_range[0], country_range[1] + 1)]

        # Get dates and valid columns based on the filter row
        dates = df.loc[date_row - 1, 1:].values
        filters = df.loc[filter_row - 1, 1:].values

        # Identify valid columns (those where the filter row is NaN or contains 'Estim.')
        valid_columns = [col for col, value in enumerate(filters, start=1) if pd.isna(value) or 'Estim' in str(value)]

        # Get corresponding valid dates
        valid_dates = [dates[col - 1] for col in valid_columns]  # Subtract 1 because valid_columns starts from 1

        # Filter data for the valid dates and countries
        data = df.iloc[:, valid_columns]

        # Format filtered data: assign countries as columns and valid dates as index
        filtered_data = data.iloc[[i - 1 for i in range(country_range[0], country_range[1] + 1)], :].T
        filtered_data.columns = countries
        filtered_data.index = valid_dates

        # Add title as a column for differentiation
        filtered_data.insert(0, 'Title', title)

        # Append to the combined list
        all_filtered_data.append(filtered_data)

    # Combine all data into a single DataFrame
    combined_data = pd.concat(all_filtered_data)

    # Save the combined data to an Excel file
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        combined_data.to_excel(writer, sheet_name='Filtered Data')

# Example usage
filter_excel_file_single_sheet('input.xlsx', 'filt5.xlsx')
