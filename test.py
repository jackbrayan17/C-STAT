import pandas as pd

def filter_excel_file(input_file, output_file):
    # Load the Excel file
    df = pd.read_excel(input_file, sheet_name=0, header=None, engine='openpyxl')

    # Define relevant cells and ranges
    title_cells = ['A2748', 'A2816', 'A2838', 'A2908', 'A2920', 'A2942', 'A2969']
    country_ranges = [
        (2750, 2755),
        (2819, 2824),
        (2841, 2846),
        (2911, 2916),
        (2923, 2928),
        (2945, 2950),
        (2972, 2977),
    ]
    date_rows = [2724, 2814, 2814, 2908, 2908, 2908, 2967]
    filter_rows = [2725, 2815, 2815, 2909, 2909, 2909, 2968]

    # Create a DataFrame to collect structured data
    structured_data = []

    for index, title_cell in enumerate(title_cells):
        title_row = int(title_cell[1:])
        title = df.loc[title_row - 1, 0]  # Get the title text
        country_range = country_ranges[index]
        date_row = date_rows[index]
        filter_row = filter_rows[index]

        # Get countries
        countries = [df.loc[i - 1, 0] for i in range(country_range[0], country_range[1] + 1)]

        # Get dates and valid columns based on the filter row
        dates = df.loc[date_row - 1, 1:].values
        filters = df.loc[filter_row - 1, 1:].values

        # Identify valid columns (those where the filter row is NaN or contains 'Estim')
        valid_columns = [col for col, value in enumerate(filters, start=1) if pd.isna(value) or 'Estim' in str(value)]

        # Get corresponding valid dates
        valid_dates = [dates[col - 1] for col in valid_columns]  # Subtract 1 because valid_columns starts from 1

        # Filter data for the valid dates and countries
        data = df.iloc[:, valid_columns]

        # Collect data in a structured format
        for i, country in enumerate(countries):
            for j, date in enumerate(valid_dates):
                value = data.iloc[i, j] if i < len(data) and j < len(data.columns) else None
                structured_data.append({
                    'Country Name': country,
                    'Year': date,
                    title: value
                })

    # Consolidate the structured data into a single DataFrame
    consolidated_df = pd.DataFrame(structured_data)

    # Pivot the DataFrame to organize by "Country Name" and "Year", with titles as columns
    final_df = consolidated_df.pivot_table(
        index=['Country Name', 'Year'],
        aggfunc='first'
    ).reset_index()

    # Save the final DataFrame to Excel
    final_df.to_excel(output_file, sheet_name='Filtered Data', index=False)

# Example usage
filter_excel_file('input.xlsx', 'filt5.xlsx')
