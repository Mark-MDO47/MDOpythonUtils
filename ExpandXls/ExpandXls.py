import sys
import os
import copy
import pandas as pd

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
    if len(sys.argv) != argNumArgs:
        print("ERROR: expect filename.xls* as argument")
        usage()
        exit(-1)
    if (-1 == sys.argv[argFname].find(".xls")) or (False == os.path.isfile(sys.argv[argFname])):
        print("ERROR: %s is not valid filename.xls*" % sys.argv[argFname])
        usage()
        exit(-1)

    ExpandXls(sys.argv[argFname])