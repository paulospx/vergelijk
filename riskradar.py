import argparse
import pandas as pd
from utils import show_delta_console

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
    
    print(f"File 1: {args.file1}")
    print(f"File 2: {args.file2}")
    print(f"Sheet Name: {args.sheet}")

    # Read the files and store them in a dataframe
    df1 = pd.read_excel(args.file1, sheet_name=args.sheet)
    df2 = pd.read_excel(args.file2, sheet_name=args.sheet)

    show_delta_console(df1, df2, args.file1, args.file2, args.sheet)


