import os
import pandas as pd

def combine_excel_files(folder_path, output_file):
    # Get a list of all Excel files in the specified folder
    excel_files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]

    # Initialize an empty DataFrame to store the combined data
    combined_df = pd.DataFrame(columns=['Target IP', 'Traceroute Result'])

    # Read each Excel file and concatenate the data
    for excel_file in sorted(excel_files):  # Sorting for ascending order
        file_path = os.path.join(folder_path, excel_file)
        df = pd.read_excel(file_path)
        combined_df = pd.concat([combined_df, df])

    # Save the combined DataFrame to a new Excel file
    combined_df.to_excel(output_file, index=False)
    print(f"Combined data saved to {output_file}")

folder_path = r'C:\\Users\\Mmile\\OneDrive\\Desktop\\CS School Files\\traceroute' # folder with all the excel files
output_file = 'combined_results2.xlsx'
combine_excel_files(folder_path, output_file)
