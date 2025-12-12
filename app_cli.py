import argparse
from pipeline import process_document, process_folder

def main():
    parser = argparse.ArgumentParser(description="Document AI Automation System")
    parser.add_argument("--file", type=str, help="Path to a single file")
    parser.add_argument("--folder", type=str, help="Path to a folder of files")
    args = parser.parse_args()

    if args.file:
        result = process_document(args.file)
        print(result)
    elif args.folder:
        df = process_folder(args.folder)
        print(df)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()