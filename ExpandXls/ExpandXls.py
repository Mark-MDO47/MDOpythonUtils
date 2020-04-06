import sys
import os
import copy
import pandas as pd
import argparse


argFname = 1
argNumArgs = argFname+1 # first arg is our name, i.e. ExpandXls.py

def usage():
    print("Usage: %s filename.xlsx" % (sys.argv[0]))

def ExpandXls(xlsName):
    # Import the excel file
    xlsPd = pd.ExcelFile(xlsName)
    xlsSheets = xlsPd.sheet_names
    for idx, sheet in enumerate(xlsSheets):
        # print("%d %s" % (idx, sheet))
        df = xlsPd.parse(xlsSheets[idx], header=None)
        for row_num, row in df.iterrows():
            # print("%s len %s" % (type(row), len(row)))
            sys.stdout.write("%s\t" % sheet)
            for col in range(len(row)):
                if pd.notna(row[col]):
                   sys.stdout.write("%s\t" % row[col])
                else:
                    sys.stdout.write("\t")
            sys.stdout.write("\n")



if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='ExpandXls',
        description="stdout receives tab-separated-values form of data in *.xls or *.xlsx",
        usage='%(prog)s spreadsheet',)
    my_parser.add_argument('spreadsheet',type=str,help='path to spreadsheet.xls or spreadsheet.xlsx')
    args = my_parser.parse_args()

    ExpandXls(args.spreadsheet)