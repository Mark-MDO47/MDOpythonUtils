#
# Author: Mark Olson 2020-04-04
#
# This trivial code must have been written dozens of times, but I needed a version for myself.
# The working part of this code uses pandas, a freely available library, and can be written in 15 lines or less.
#
# xlsx2txt - create text form of values in *.xls or *.xlsx; allows quick comparison of files
#
# example: python xlsx2txt.py file.xlsx > file.txt
#  - reads the values from tabs/cells in file.xlsx (not formulas, formatting, etc.)
#  - writes tab-separated-variable version to stdout in form tabname\tA1\tA2\t...
#  - gotchas: has no real error checking; will barf on UnicodeEncodeError and other errors
#

import sys
# import os
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
                    try:
                        sys.stdout.write("%s\t" % row[col])
                    except:
                        sys.stderr.write("Error - BAD_CHARS in file:|%s| tab:|%s| row:%d col:%d\n" % (xlsName, sheet, row_num, col))
                        sys.stdout.write("BAD_CHARS\t")
                else:
                    sys.stdout.write("\t")
            sys.stdout.write("\n")

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='xlsx2txt',
        formatter_class=argparse.RawTextHelpFormatter,
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
