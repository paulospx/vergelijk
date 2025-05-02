import argparse
import pandas as pd
from utils import show_delta_console, calculate_differences

def parse_arguments():
    parser = argparse.ArgumentParser(description="Compare information between two Excel files.")
    parser.add_argument(
        '--file1', 
        required=True, 
        help="Path to the first Excel file."
    )
    parser.add_argument(
        '--file2', 
        required=True, 
        help="Path to the second Excel file."
    )
    parser.add_argument(
        '--sheet', 
        required=True, 
        help="Name of the sheet containing the information to be compared."
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    
    print(f"- File 1: {args.file1}")
    print(f"- File 2: {args.file2}")
    print(f"- Sheet Name: {args.sheet}")

    # Read the files and store them in a dataframe
    df1 = pd.read_excel(args.file1, sheet_name=args.sheet)
    df2 = pd.read_excel(args.file2, sheet_name=args.sheet)


    # Generate a statistical analysis to calculare the differences between df1 and df2
    # Calculate the differences between the two dataframes
    



    # Show the differences from df1 columns and df2 columns
    col1 = sorted(df1.columns.tolist())
    col2 = sorted(df2.columns.tolist())

   
    # Display the differences between the two column lists as UX expert from Norman Nielsen group
    if col1 == col2:
        print(f"No differences between curves in {args.file1} and {args.file2} with sheet: {args.sheet}.")
    else:
        print(f"Differences between curves from {args.file1} and {args.file2}:")
        print(f"Curves in {args.file1} but not in {args.file2}:")
        for col in col1:
            if col not in col2:
                print(f" - {col}")

        print(f"Curves in {args.file2} but not in {args.file1}:")
        for col in col2:
            if col not in col1:
                print(f" - {col}")

    print()
    print("---")
    print()

    show_delta_console(df1, df2, args.file1, args.file2, args.sheet)


