import sys
import os
# import copy
import pandas as pd
import argparse

def xlsx2txt(xlsName):
    # Import the excel file
    xlsPd = pd.ExcelFile(xlsName)
    xlsSheets = xlsPd.sheet_names
    for sheet in xlsSheets:
        df = xlsPd.parse(sheet, header=None)
        for row_num, row in df.iterrows():
            sys.stdout.write("%s\t" % sheet)
            for col in range(len(row)):
                if pd.notna(row[col]):
                   sys.stdout.write("%s\t" % row[col])
                else:
                    sys.stdout.write("\t")
            sys.stdout.write("\n")

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='xlsx2txt',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="stdout receives tab-separated-values form of data in *.xls or *.xlsx",
        epilog="""Example:
python xlsx2txt.py old.xlsx > old.txt
python xlsx2txt.py new.xlsx > new.txt
diff old.txt new.txt
""",
        usage='%(prog)s spreadsheet')
    my_parser.add_argument('spreadsheet',type=str,help='path to spreadsheet.xls or spreadsheet.xlsx')
    args = my_parser.parse_args()

    xlsx2txt(args.spreadsheet)