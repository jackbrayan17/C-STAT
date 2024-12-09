import pandas as pd

def filter_excel_file(input_file, output_file):
    # Load the Excel file
    df = pd.read_excel(input_file, sheet_name=0, header=None, engine='openpyxl')

    title_cells = ['A9','A1767','A1911','A1992','A2003','A2023','A2132','A2273','A2748', 'A2816', 'A2838', 'A2908', 'A2920', 'A2942', 'A2969']
    country_ranges = [
        (10,14),
        (1768, 1773),
        (1912,1917),
        (1993, 1998),
        (2004,2009),
        (2004,2009),
        (2133,2138),
        (2274,2279),
        (2750, 2755),
        (2819, 2824),
        (2841, 2846),
        (2911, 2916),
        (2923, 2928),
        (2945, 2950),
        (2972, 2977),
    ]
    date_rows = [5,1724,1907,1989,1989,1989,2076,2271,2724, 2814, 2814, 2906, 2906, 2906, 2967]
    filter_rows = [7,1726,1909,1991,1991,1991,2078,2273,2725, 2815, 2815, 2907, 2907, 2907, 2968]

    # Initialize a dictionary to store filtered data
    filtered_data = {}

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

        # Format filtered data: assign countries as row indices and valid dates as column headers
        filtered_data[title] = data.iloc[[i - 1 for i in range(country_range[0], country_range[1] + 1)], :].T
        filtered_data[title].columns = countries
        filtered_data[title].index = valid_dates  # Set valid dates as the index (column headers)

    # Save the filtered data to an Excel file
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for title, data in filtered_data.items():
            data.to_excel(writer, sheet_name=title[:30])  # Sheet names truncated to 30 characters

# Example usage
filter_excel_file('input.xlsx', 'filter.xlsx')
