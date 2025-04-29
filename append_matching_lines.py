import argparse
from utils import append_matching_lines

def parse_arguments():
    parser = argparse.ArgumentParser(description="Append matching lines from text files.")
    parser.add_argument(
        '--directory', 
        required=True, 
        help="Path to the Directory with files."
    )
    parser.add_argument(
        '--pattern', 
        required=True, 
        help="Pattern to match files (e.g., '*.txt')."
    )
    parser.add_argument(
        '--text', 
        required=True, 
        help="Text to search for in the files."
    )
    parser.add_argument(
        '--outputfile', 
        required=True, 
        help="Output file to append matching lines."
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    print(f"Directory: {args.directory}")
    print(f"Pattern: {args.pattern}")
    print(f"Search Text: {args.text}")
    print(f"Output File: {args.outputfile}")

    append_matching_lines(args.directory, args.pattern, args.text, args.outputfile)




